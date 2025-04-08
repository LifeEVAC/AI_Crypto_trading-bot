# 胜率預測模型
# models.py

def predict_winrate(indicators, direction="long"):
    """
    根據技術指標與方向，回傳預測勝率（0.0 ~ 0.95）
    """

    score = 0
    total = 0

    # ===== 基礎指標分數 =====
    if direction == "long":
        if indicators["RSI"] > 55: score += 1
        if indicators["MACD"] == "bullish": score += 1
        if indicators["MA_cross"] == "golden": score += 1
        if indicators["BB_B"] > 0.5: score += 1
        if indicators["ADX"] > 20 and indicators["+DI"] > indicators["-DI"]: score += 1
        if indicators["CCI"] > 0: score += 1
        if indicators["STOCH_K"] > 50: score += 1
        if indicators["OBV"] > 0: score += 1
        if indicators["BB_width"] > 0.03: score += 1
        if indicators["ATR"] > 0: score += 1
        if indicators["Volume_surge"]: score += 1
        total = 11

    else:
        if indicators["RSI"] < 45: score += 1
        if indicators["MACD"] == "bearish": score += 1
        if indicators["MA_cross"] == "death": score += 1
        if indicators["BB_B"] < 0.5: score += 1
        if indicators["ADX"] > 20 and indicators["-DI"] > indicators["+DI"]: score += 1
        if indicators["CCI"] < 0: score += 1
        if indicators["STOCH_K"] < 50: score += 1
        if indicators["OBV"] < 0: score += 1
        if indicators["BB_width"] > 0.03: score += 1
        if indicators["ATR"] > 0: score += 1
        if indicators["Volume_surge"]: score += 1
        total = 11

    # ===== 超級指標邏輯（每命中一組 +1 分）=====
    super_score = 0

    if direction == "long":
        if (
            indicators["RSI"] > 55 and
            indicators["MACD"] == "bullish" and
            indicators["MA_cross"] == "golden"
        ):
            super_score += 1  # 多頭三重奏

        if (
            indicators["ADX"] > 25 and
            indicators["+DI"] > indicators["-DI"] and
            indicators["OBV"] > 0
        ):
            super_score += 1  # 趨勢能量共振

    else:
        if (
            indicators["RSI"] < 45 and
            indicators["MACD"] == "bearish" and
            indicators["MA_cross"] == "death"
        ):
            super_score += 1  # 空頭三重奏

        if (
            indicators["ADX"] > 25 and
            indicators["-DI"] > indicators["+DI"] and
            indicators["OBV"] < 0
        ):
            super_score += 1  # 趨勢放空共振

    # ===== 最終勝率計算 =====
    base_winrate = 0.6 + 0.03 * score  # 每個指標給 3%
    total_winrate = base_winrate + 0.025 * super_score  # 每個超級指標給 2.5%

    return round(min(total_winrate, 0.95), 3)
