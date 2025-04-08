# 技術指標計算
import pandas as pd
import numpy as np
import ta
from ta.trend import MACD, CCIIndicator, ADXIndicator, EMAIndicator, SuperTrend
from ta.momentum import RSIIndicator, StochasticOscillator, TSIIndicator, ROCIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator

def calculate_crypto_indicators(df):
    try:
        if df.empty or len(df) < 50:
            raise ValueError("歷史資料不足")

        close = df["Close"]
        high = df["High"]
        low = df["Low"]
        volume = df["Volume"]

        rsi = RSIIndicator(close).rsi().iloc[-1]
        macd = MACD(close)
        macd_diff = macd.macd_diff().iloc[-1]
        macd_trend = "bullish" if macd_diff > 0 else "bearish"

        bb = BollingerBands(close)
        bb_b = ((close - bb.bollinger_lband()) / (bb.bollinger_hband() - bb.bollinger_lband())).iloc[-1]
        bb_width = (bb.bollinger_hband() - bb.bollinger_lband()).iloc[-1] / close.iloc[-1]

        adx = ADXIndicator(high, low, close)
        adx_val = adx.adx().iloc[-1]
        plus_di = adx.adx_pos().iloc[-1]
        minus_di = adx.adx_neg().iloc[-1]

        atr = AverageTrueRange(high, low, close).average_true_range().iloc[-1]
        obv = OnBalanceVolumeIndicator(close, volume).on_balance_volume().iloc[-1]
        cci = CCIIndicator(high, low, close).cci().iloc[-1]

        stoch = StochasticOscillator(high, low, close)
        stoch_k = stoch.stoch().iloc[-1]
        stoch_d = stoch.stoch_signal().iloc[-1]

        vwap = (close * volume).rolling(window=30).sum() / volume.rolling(window=30).sum()
        vwap_val = vwap.iloc[-1]

        supertrend = SuperTrend(high, low, close, window=10, multiplier=3.0).super_trend()
        supertrend_trend = "bullish" if close.iloc[-1] > supertrend.iloc[-1] else "bearish"

        donchian_high = high.rolling(window=20).max().iloc[-1]
        donchian_low = low.rolling(window=20).min().iloc[-1]
        tsi = TSIIndicator(close).tsi().iloc[-1]
        roc = ROCIndicator(close).roc().iloc[-1]

        return {
            "RSI": round(rsi, 2),
            "MACD": macd_trend,
            "BB_B": round(bb_b, 2),
            "BB_width": round(bb_width, 4),
            "ADX": round(adx_val, 2),
            "+DI": round(plus_di, 2),
            "-DI": round(minus_di, 2),
            "ATR": round(atr, 2),
            "OBV": round(obv, 2),
            "CCI": round(cci, 2),
            "STOCH_K": round(stoch_k, 2),
            "STOCH_D": round(stoch_d, 2),
            "VWAP": round(vwap_val, 2),
            "Supertrend": supertrend_trend,
            "Donchian_High": round(donchian_high, 2),
            "Donchian_Low": round(donchian_low, 2),
            "TSI": round(tsi, 2),
            "ROC": round(roc, 2),
            "price": round(close.iloc[-1], 2)
        }

    except Exception as e:
        print(f"❌ 指標錯誤: {e}")
        return {}
