# 處理指標與策略選幣邏輯
# strategy.py

from indicators import calculate_crypto_indicators
from models import predict_winrate
from etf_scoring import get_tp_sl_by_symbol

# ⛳ 傳入清單如：[{"symbol": "BTCUSDT"}, {"symbol": "ETHUSDT"}]
def run_strategy(crypto_list):
    print("🎯 開始分析加密貨幣...")
    selected = []

    unit_investment = 10000  # 每單 1 萬美金（可調整）

    for item in crypto_list:
        symbol = item["symbol"]
        print(f"🔍 分析 {symbol}")

        # 取得技術指標
        df = item.get("df")  # 可事先傳入 DataFrame
        indicators = calculate_crypto_indicators(df if df is not None else item["source"]())

        if not indicators or indicators.get("price", 0) == 0:
            print(f"⚠️ {symbol} 無法取得價格或指標")
            continue

        # 勝率評估（多 / 空）
        win_long = predict_winrate(indicators, direction="long")
        win_short = predict_winrate(indicators, direction="short")

        if win_long >= win_short:
            direction = "long"
            winrate = win_long
        else:
            direction = "short"
            winrate = win_short

        if winrate < 0.65:
            print(f"❌ {symbol} 勝率過低 ({round(winrate, 2)})，跳過\n")
            continue

        # 投資金額（依照勝率分級）
        if winrate >= 0.85:
            capital = unit_investment * 1.5
        elif winrate >= 0.75:
            capital = unit_investment * 1.2
        else:
            capital = unit_investment

        # 計算出場價格
        entry = indicators["price"]
        tp_pct, sl_pct = get_tp_sl_by_symbol(symbol)
        tp_price = round(entry * (1 + tp_pct), 2) if direction == "long" else round(entry * (1 - tp_pct), 2)
        sl_price = round(entry * (1 - sl_pct), 2) if direction == "long" else round(entry * (1 + sl_pct), 2)

        result = {
            "symbol": symbol,
            "direction": direction,
            "price": entry,
            "tp_price": tp_price,
            "sl_price": sl_price,
            "winrate": round(winrate, 3),
            "capital": round(capital, 2),
            "indicators": indicators,
            "score": round((winrate + 0.1), 3),  # 可再改進綜合分數計算方式
        }

        print(f"✅ {symbol} → {direction.upper()}｜勝率 {winrate:.2f}｜投入 ${capital}\n")
        selected.append(result)

    return selected
