import ccxt
import pandas as pd
from ta.trend import MACD, ADXIndicator
from ta.momentum import RSIIndicator
from ta.volume import OnBalanceVolumeIndicator
from ta.volatility import BollingerBands

# ✅ 自訂 SuperTrend 函式
def calculate_supertrend(df, period=10, multiplier=3.0):
    hl2 = (df['High'] + df['Low']) / 2
    atr = df['High'].rolling(period).max() - df['Low'].rolling(period).min()
    atr = atr.rolling(period).mean()
    upperband = hl2 + multiplier * atr
    lowerband = hl2 - multiplier * atr
    trend = []
    for i in range(len(df)):
        if i < period:
            trend.append("bullish")
        elif df['Close'][i] > upperband[i - 1]:
            trend.append("bullish")
        elif df['Close'][i] < lowerband[i - 1]:
            trend.append("bearish")
        else:
            trend.append(trend[-1])
    return trend

# ✅ 抓取資料
def fetch_ohlcv(symbol="BTC/USDT", timeframe="1h", limit=100):
    exchange = ccxt.okx({
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot',
        }
    })
    since = exchange.milliseconds() - limit * 60 * 60 * 1000
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "Open", "High", "Low", "Close", "Volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

# ✅ 計算所有技術指標
def calculate_crypto_indicators(df):
    try:
        if df.empty or len(df) < 50:
            raise ValueError("歷史資料不足")

        close = df["Close"]
        high = df["High"]
        low = df["Low"]
        volume = df["Volume"]

        rsi = RSIIndicator(close).rsi().iloc[-1]
        macd_diff = MACD(close).macd_diff().iloc[-1]
        macd_trend = "bullish" if macd_diff > 0 else "bearish"

        vwap = (close * volume).rolling(window=30).sum() / volume.rolling(window=30).sum()
        vwap_val = vwap.iloc[-1]

        supertrend_list = calculate_supertrend(df)
        supertrend_trend = supertrend_list[-1]

        adx_val = ADXIndicator(high, low, close).adx().iloc[-1]
        obv = OnBalanceVolumeIndicator(close, volume).on_balance_volume().iloc[-1]

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
