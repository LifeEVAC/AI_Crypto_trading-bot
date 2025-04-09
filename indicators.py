# indicators_btc.py（精簡版）

import ccxt
import pandas as pd
from ta.trend import MACD, SuperTrend
from ta.momentum import RSIIndicator


def fetch_ohlcv(symbol="BTC/USDT", timeframe="1h", limit=100):
    exchange = ccxt.binance()
    since = exchange.milliseconds() - limit * 60 * 60 * 1000
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "Open", "High", "Low", "Close", "Volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


def calculate_crypto_indicators(df):
    try:
        if df.empty or len(df) < 50:
            raise ValueError("歷史資料不足")

        close = df["Close"]
        high = df["High"]
        low = df["Low"]
        volume = df["Volume"]

        # === RSI ===
        rsi = RSIIndicator(close).rsi().iloc[-1]

        # === MACD ===
        macd_diff = MACD(close).macd_diff().iloc[-1]
        macd_trend = "bullish" if macd_diff > 0 else "bearish"

        # === VWAP（成交量加權平均）===
        vwap = (close * volume).rolling(window=30).sum() / volume.rolling(window=30).sum()
        vwap_val = vwap.iloc[-1]

        # === Supertrend ===
        supertrend = SuperTrend(high, low, close, window=10, multiplier=3.0).super_trend()
        supertrend_trend = "bullish" if close.iloc[-1] > supertrend.iloc[-1] else "bearish"

        return {
            "RSI": round(rsi, 2),
            "MACD": macd_trend,
            "VWAP": round(vwap_val, 2),
            "Supertrend": supertrend_trend,
            "price": round(close.iloc[-1], 2)
        }

    except Exception as e:
        print(f"❌ 指標錯誤: {e}")
        return {}
