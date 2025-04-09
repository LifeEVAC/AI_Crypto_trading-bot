from indicators_btc import fetch_ohlcv, calculate_crypto_indicators
from bitcoin_models import predict_btc_winrate
from okx_trade import place_order, monitor_position

SYMBOL = "BTC/USDT"
TRADE_AMOUNT = 0.001        # 每次交易金額
TP_PERCENT = 0.02           # 止盈 2%
SL_PERCENT = 0.015          # 止損 1.5%
MIN_WINRATE = 0.8           # 最小進場勝率

def main():
    print("🚀 啟動 BTC 策略交易機器人")
    
    # Step 1: 抓取歷史資料
    print("\n📈 抓取 BTC 歷史資料中...")
    df = fetch_ohlcv(SYMBOL)
    if df is None or len(df) == 0:
        print("❌ 無法取得歷史資料，結束程式。")
        return

    # Step 2: 計算技術指標
    print("\n📊 計算技術指標中...")
    indicators = calculate_crypto_indicators(df)
    if not indicators:
        print("❌ 指標計算失敗，結束程式。")
        return

    # Step 3: 預測勝率
    print("\n🧠 AI 預測勝率中...")
    win_long = predict_btc_winrate(indicators, direction="long")
    win_short = predict_btc_winrate(indicators, direction="short")

    # Step 4: 判斷方向
    direction = "long" if win_long >= win_short else "short"
    winrate = max(win_long, win_short)

    print(f"\n✅ 預測方向：{direction.upper()}")
    print(f"🎯 勝率預估：{round(winrate * 100, 2)}%")
    print(f"💰 價格：{indicators['price']}")
    print(f"📊 RSI: {indicators['RSI']} / MACD: {indicators['MACD']} / Supertrend: {indicators['Supertrend']}")
    print(f"📈 VWAP: {indicators['VWAP']} / ADX: {indicators['ADX']} / OBV: {indicators['OBV']}")

    # Step 5: 判斷是否進場
    if winrate >= MIN_WINRATE:
        print(f"\n🚀 勝率達標，開始下單 {direction.upper()} {SYMBOL}")
        side = "buy" if direction == "long" else "sell"
        order = place_order(SYMBOL, side=side, amount=TRADE_AMOUNT)
        if order:
            print("🟢 下單成功，進入止盈止損監控...")
            monitor_position(
                entry_price=indicators["price"],
                direction=direction,
                symbol=SYMBOL,
                amount=TRADE_AMOUNT,
                take_profit_pct=TP_PERCENT,
                stop_loss_pct=SL_PERCENT
            )
        else:
            print("❌ 下單失敗，請檢查 API 或餘額")
    else:
        print("\n🟡 勝率不足，今日不下單")

if __name__ == "__main__":
    main()
