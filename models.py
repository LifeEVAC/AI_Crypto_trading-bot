# bitcoin_models.py

def predict_btc_winrate(indicators, direction="long"):
    """
    專業版 Bitcoin 核心策略邏輯：
    - 著重動能、趨勢、爆發力、主力參與度
    - 精簡高信賴指標，專為 BTC scalping 最佳化
    - 預測勝率介於 0.5 ～ 0.95
    """

    score = 0
    total = 0

    # ✅ 核心指標（必要）
    # [1] Supertrend 趨勢方向
    if indicators.get("Supertrend") == ("bullish" if direction == "long" else "bearish"):
        score += 1
    total += 1

    # [2] RSI 動能方向
    if direction == "long" and indicators.get("RSI", 50) > 55:
        score += 1
    elif direction == "short" and indicators.get("RSI", 50) < 45:
        score += 1
    total += 1

    # [3] MACD 多空轉折
    if indicators.get("MACD") == ("bullish" if direction == "long" else "bearish"):
        score += 1
    total += 1

    # [4] VWAP 位置判斷（主力成本）
    if direction == "long" and indicators.get("price", 0) > indicators.get("VWAP", 0):
        score += 1
    elif direction == "short" and indicators.get("price", 0) < indicators.get("VWAP", 0):
        score += 1
    total += 1

    # ✅ 強信心條件（加分機制）
    # [5] ADX 趨勢強度
    if indicators.get("ADX", 0) > 25:
        score += 0.5
    total += 0.5

    # [6] OBV 多空能量趨勢
    if direction == "long" and indicators.get("OBV", 0) > 0:
        score += 0.5
    elif direction == "short" and indicators.get("OBV", 0) < 0:
        score += 0.5
    total += 0.5

    # [7] 布林帶壓縮準備爆發
    if indicators.get("BB_width", 1) < 0.03:
        score += 0.5
    total += 0.5

    # === 勝率推估 ===
    base = 0.5
    boost = (score / total) * 0.45  # 最多額外 +0.45
    return round(min(base + boost, 0.95), 3)
