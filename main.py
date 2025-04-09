from indicators_btc import fetch_ohlcv, calculate_crypto_indicators
from bitcoin_models import predict_btc_winrate

def main():
    print("🚀 啟動 AI Bitcoin Scalping 策略...")

    # 抓取 BTC 近 100 小時資料（1h K 線）
    df = fetch_ohlcv("BTC/USDT", "1h", limit=100)

    # 計算指標
    indicators = calculate_crypto_indicators(df)

    if not indicators:
        print("⚠️ 無法取得指標，策略終止")
        return

    price = indicators["price"]

    # 做多 / 做空 預測勝率
    long_prob = predict_btc_winrate(indicators, direction="long")
    short_prob = predict_btc_winrate(indicators, direction="short")

    print("📊 當前價格：$", price)
    print("📈 做多勝率：", long_prob)
    print("📉 做空勝率：", short_prob)

    # 決策邏輯
    if long_prob >= 0.75 and long_prob > short_prob:
        print(f"✅ 建議做多（勝率 {long_prob}）")
    elif short_prob >= 0.75 and short_prob > long_prob:
        print(f"✅ 建議做空（勝率 {short_prob}）")
    else:
        print("🟡 尚未達下單門檻，觀望中...")

if __name__ == "__main__":
    main()
