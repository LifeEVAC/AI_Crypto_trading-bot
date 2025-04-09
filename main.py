# main.py — 搭配 OKX 現貨交易 + BTC Scalping 策略

from indicators_btc import fetch_ohlcv, calculate_crypto_indicators
from bitcoin_models import predict_btc_winrate
from okx_trade import place_order, monitor_position

SYMBOL = "BTC/USDT"
TRADE_AMOUNT = 0.001  # 每次交易金額（可調整）
TP_PERCENT = 0.02     # 止盈 +2%
SL_PERCENT = 0.015    # 止損 -1.5%
MIN_WINRATE = 0.8     # 最小進場勝率條件

def main():
    print("📈 取得 BTC 歷史資料...")
    df = fetch_ohlcv(SYMBOL)

    print("🧠 計算技術指標...")
    indicators = calculate_crypto_indicators(df)

    if not indicators:
        print("❌ 指標計算失敗，無法進行預測。")
        return

    print("🤖 預測做多 / 做空 勝率...")
    win_long = predict_btc_winrate(indicators, direction="long")
    win_short = predict_btc_winrate(indicators, direction="short")

    # 選擇方向（勝率高者）
    if win_long >= win_short:
        direction = "long"
        winrate = win_long
    else:
        direction = "short"
        winrate = win_short

    # 顯示分析結果
    print(f"\n✅ 預測方向：{direction.upper()}")
    print(f"🎯 預測勝率：{round(winrate * 100, 2)}%")
    print(f"💰 當前價格：{indicators['price']}")
    print(f"📊 RSI: {indicators['RSI']} / MACD: {indicators['MACD']} / Supertrend: {indicators['Supertrend']}")
    print(f"📈 VWAP: {indicators['VWAP']} / ADX: {indicators['ADX']} / OBV: {indicators['OBV']}")

    # ✅ 是否進行下單
    if winrate >= MIN_WINRATE:
        print(f"\n🚀 勝率達標，準備下單：{direction.upper()} {SYMBOL}")
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
        print("\n🟡 勝率不足，今日不下單")

if __name__ == "__main__":
    main()
