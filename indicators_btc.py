# ✅ 自訂 SuperTrend 類別（放在檔案最前面）
import pandas as pd

class SuperTrend:
    def __init__(self, high, low, close, window=10, multiplier=3):
        self.high = high
        self.low = low
        self.close = close
        self.window = window
        self.multiplier = multiplier

    def super_trend(self):
        df = pd.DataFrame({
            "high": self.high,
            "low": self.low,
            "close": self.close
        })

        hl2 = (df["high"] + df["low"]) / 2
        df["tr"] = pd.concat([
            df["high"] - df["low"],
            (df["high"] - df["close"].shift()).abs(),
            (df["low"] - df["close"].shift()).abs()
        ], axis=1).max(axis=1)

        df["atr"] = df["tr"].rolling(self.window).mean()
        df["upper_band"] = hl2 + self.multiplier * df["atr"]
        df["lower_band"] = hl2 - self.multiplier * df["atr"]

        df["in_uptrend"] = True
        for i in range(1, len(df)):
            if df["close"][i] > df["upper_band"][i - 1]:
                df["in_uptrend"][i] = True
            elif df["close"][i] < df["lower_band"][i - 1]:
                df["in_uptrend"][i] = False
            else:
                df["in_uptrend"][i] = df["in_uptrend"][i - 1]
                if df["in_uptrend"][i] and df["lower_band"][i] < df["lower_band"][i - 1]:
                    df["lower_band"][i] = df["lower_band"][i - 1]
                if not df["in_uptrend"][i] and df["upper_band"][i] > df["upper_band"][i - 1]:
                    df["upper_band"][i] = df["upper_band"][i - 1]

        trend = ["bullish" if x else "bearish" for x in df["in_uptrend"]]
        return pd.Series(trend, index=df.index)
