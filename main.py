# main.py（搭配 OKX + BTC 策略核心）

from indicators_btc import fetch_ohlcv, calculate_crypto_indicators
from bitcoin_models import predict_btc_winrate

SYMBOL = "BTC/USDT"

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

    # 判斷方向
    if win_long >= win_short:
        direction = "long"
        winrate = win_long
    else:
        direction = "short"
        winrate = win_short

    # 顯示結果
    print(f"\n✅ 方向判斷：{direction.upper()}")
    print(f"📊 勝率預估：{winrate}")
    print(f"💰 價格：{indicators['price']}")
    print(f"📉 RSI: {indicators['RSI']} / MACD: {indicators['MACD']} / Supertrend: {indicators['Supertrend']}")
    print(f"📈 VWAP: {indicators['VWAP']} / ADX: {indicators['ADX']} / OBV: {indicators['OBV']}")

if __name__ == "__main__":
    main()
