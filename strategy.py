# strategy_btc.py

from indicators import calculate_crypto_indicators
from bitcoin_models import predict_btc_winrate

def run_strategy(crypto_list):
    print("\n🎯 開始分析比特幣 scalping 機會...")
    selected = []

    unit_investment = 1000  # 每筆固定投資金額

    for item in crypto_list:
        symbol = item["symbol"]
        print(f"🔍 分析 {symbol}")

        # 取得技術指標
        df = item.get("df")
        indicators = calculate_crypto_indicators(df if df is not None else item["source"]())

        if not indicators or indicators.get("price", 0) == 0:
            print(f"⚠️ {symbol} 無法取得價格或指標\n")
            continue

        # 預測做多 / 做空勝率
        win_long = predict_btc_winrate(indicators, direction="long")
        win_short = predict_btc_winrate(indicators, direction="short")

        # 選擇較高勝率方向
        if win_long >= win_short:
            direction = "long"
            winrate = win_long
        else:
            direction = "short"
            winrate = win_short

        if winrate < 0.65:
            print(f"❌ {symbol} 勝率過低（{winrate}），略過\n")
            continue

        entry = indicators["price"]

        # 固定 TP/SL 比例
        tp_pct = 0.035
        sl_pct = 0.025
        tp_price = round(entry * (1 + tp_pct), 2) if direction == "long" else round(entry * (1 - tp_pct), 2)
        sl_price = round(entry * (1 - sl_pct), 2) if direction == "long" else round(entry * (1 + sl_pct), 2)

        result = {
            "symbol": symbol,
            "direction": direction,
            "price": entry,
            "tp_price": tp_price,
            "sl_price": sl_price,
            "winrate": winrate,
            "capital": unit_investment,
            "score": round((winrate - 0.5) / 0.45, 3),  # 正規化分數 0～1
            "tp_pct": tp_pct,
            "sl_pct": sl_pct,
            "indicators": indicators
        }

        print(f"✅ {symbol} → {direction.upper()} ｜勝率: {winrate}，TP: {tp_price}，SL: {sl_price}\n")
        selected.append(result)

    return selected
