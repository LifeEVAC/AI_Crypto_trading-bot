from indicators_btc import fetch_ohlcv, calculate_crypto_indicators
from bitcoin_models import predict_btc_winrate
from okx_trade import place_order, monitor_position, check_balance

SYMBOL = "BTC/USDT"
TRADE_AMOUNT = 0.001
TP_PERCENT = 0.02
SL_PERCENT = 0.015
MIN_WINRATE = 0.8

def main():
    print("🚀 啟動主程序 main.py")
    
    # ✅ 步驟1：取得歷史資料
    try:
        print("📈 取得 BTC 歷史資料...")
        df = fetch_ohlcv(SYMBOL)
        print("✅ 資料筆數：", len(df))
    except Exception as e:
        print(f"❌ 步驟1失敗：歷史資料無法取得 → {e}")
        return

    # ✅ 步驟2：技術指標
    try:
        print("🧠 計算技術指標...")
        indicators = calculate_crypto_indicators(df)
        if not indicators:
            print("❌ 步驟2失敗：技術指標錯誤")
            return
    except Exception as e:
        print(f"❌ 步驟2錯誤：{e}")
        return

    # ✅ 步驟3：AI 預測
    try:
        print("🧮 AI 預測多空勝率...")
        win_long = predict_btc_winrate(indicators, "long")
        win_short = predict_btc_winrate(indicators, "short")
    except Exception as e:
        print(f"❌ 步驟3錯誤：AI 模型預測錯誤 → {e}")
        return

    # ✅ 勝率比較
    direction = "long" if win_long >= win_short else "short"
    winrate = max(win_long, win_short)
    print(f"\n✅ 預測方向：{direction.upper()} | 勝率：{round(winrate*100, 2)}%")
    print(f"💰 價格：{indicators['price']} | RSI: {indicators['RSI']} | MACD: {indicators['MACD']}")

    # ✅ 步驟4：檢查勝率
    if winrate < MIN_WINRATE:
        print("🟡 勝率未達標，今天不下單")
        return

    # ✅ 步驟5：下單
    try:
        print("💳 檢查 USDT 餘額...")
        usdt_balance = check_balance("USDT")
        if usdt_balance < 10:
            print(f"❌ 餘額不足（{usdt_balance} USDT）→ 不執行下單")
            return
    except Exception as e:
        print(f"⚠️ 餘額查詢錯誤：{e}")

    try:
        print(f"📤 送出下單請求：{direction.upper()} {SYMBOL}")
        side = "buy" if direction == "long" else "sell"
        order = place_order(SYMBOL, side=side, amount=TRADE_AMOUNT)
        print("📦 下單結果：", order)
        if not order:
            print("❌ 下單未成功，取消監控")
            return
    except Exception as e:
        print(f"❌ 下單錯誤：{e}")
        return

    # ✅ 步驟6：進入監控
    try:
        print("📡 進入價格監控...")
        monitor_position(
            entry_price=indicators["price"],
            direction=direction,
            symbol=SYMBOL,
            amount=TRADE_AMOUNT,
            take_profit_pct=TP_PERCENT,
            stop_loss_pct=SL_PERCENT
        )
    except Exception as e:
        print(f"❌ 監控失敗：{e}")

if __name__ == "__main__":
    main()
