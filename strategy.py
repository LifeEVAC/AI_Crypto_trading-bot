# strategy_btc.py

from indicators import calculate_crypto_indicators
from logic_winrate import logic_predict_winrate  # ✅ 替代原模型預測

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

        # ✅ 使用邏輯式勝率預測系統
        win_long, reason_long = logic_predict_winrate(indicators, direction="long")
        win_short, reason_short = logic_predict_winrate(indicators, direction="short")

        # 選擇較高勝率方向
        if win_long >= win_short:
            direction = "long"
            winrate = win_long
            reasons = reason_long
        else:
            direction = "short"
            winrate = win_short
            reasons = reason_short

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
            "indicators": indicators,
            "reasons": reasons
        }

        print(f"✅ {symbol} → {direction.upper()} ｜勝率: {winrate}，TP: {tp_price}，SL: {sl_price}")
        print(f"📋 原因：{', '.join(reasons)}\n")

        selected.append(result)

    return selected
