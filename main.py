# main.py — 搭配 OKX 現貨交易 + BTC Scalping 策略

from indicators_btc import fetch_ohlcv, calculate_crypto_indicators
from bitcoin_models import predict_btc_winrate
from okx_trade import place_order, monitor_position

# 參數設定
SYMBOL = "BTC/USDT"
TRADE_AMOUNT = 0.001  # 每次下單的數量（可依資金調整）
TP_PERCENT = 0.02     # 止盈比例：+2%
SL_PERCENT = 0.015    # 止損比例：-1.5%
MIN_WINRATE = 0.8     # 勝率門檻，達標才進場

def main():
    print("📈 取得 BTC 歷史資料...")
    df = fetch_ohlcv(SYMBOL)

    print("🧠 計算技術指標...")
    indicators = calculate_crypto_indicators(df)

    if not indicators:
        print("❌ 指標錯誤，跳過")
        return

    print("🤖 AI 預測多空勝率...")
    win_long = predict_btc_winrate(indicators, direction="long")
    win_short = predict_btc_winrate(indicators, direction="short")

    # 選擇方向
    if win_long >= win_short:
        direction = "long"
        winrate = win_long
    else:
        direction = "short"
        winrate = win_short

    # 顯示結果
    print(f"\n✅ 預測方向：{direction.upper()}")
    print(f"🎯 勝率：{round(winrate * 100, 2)}%")
    print(f"💰 現價：{indicators['price']}")
    print(f"📊 RSI: {indicators['RSI']} | MACD: {indicators['MACD']} | Supertrend: {indicators['Supertrend']}")
    print(f"📈 VWAP: {indicators['VWAP']} | ADX: {indicators['ADX']} | OBV: {indicators['OBV']}")

    # 判斷是否進場
    if winrate >= MIN_WINRATE:
        print(f"\n🚀 勝率達標 → 市價下單 {direction.upper()} × {TRADE_AMOUNT} BTC")
        side = "buy" if direction == "long" else "sell"
        order = place_order(SYMBOL, side=side, amount=TRADE_AMOUNT)
        if order:
            monitor_position(
                entry_price=indicators["price"],
                direction=direction,
                symbol=SYMBOL,
                amount=TRADE_AMOUNT,
                take_profit_pct=TP_PERCENT,
                stop_loss_pct=SL_PERCENT
            )
        else:
            print("❌ 下單失敗，無法監控 TP/SL")
    else:
        print("\n🟡 勝率不足，略過交易")

if __name__ == "__main__":
    main()
