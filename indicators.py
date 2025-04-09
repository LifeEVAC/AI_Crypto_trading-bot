# indicators_btc.py（針對 bitcoin_models.py 對應設計）

import ccxt
import pandas as pd
from ta.trend import MACD, SuperTrend, ADXIndicator
from ta.momentum import RSIIndicator
from ta.volume import OnBalanceVolumeIndicator
from ta.volatility import BollingerBands


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

        # === ADX ===
        adx_val = ADXIndicator(high, low, close).adx().iloc[-1]

        # === OBV ===
        obv = OnBalanceVolumeIndicator(close, volume).on_balance_volume().iloc[-1]

        # === BB Width ===
        bb = BollingerBands(close)
        bb_width = (bb.bollinger_hband() - bb.bollinger_lband()).iloc[-1] / close.iloc[-1]

        return {
            "RSI": round(rsi, 2),
            "MACD": macd_trend,
            "VWAP": round(vwap_val, 2),
            "Supertrend": supertrend_trend,
            "ADX": round(adx_val, 2),
            "OBV": round(obv, 2),
            "BB_width": round(bb_width, 4),
            "price": round(close.iloc[-1], 2)
        }

    except Exception as e:
        print(f"❌ 指標錯誤: {e}")
        return {}
