# crypto_symbols.py

def get_crypto_symbols():
    """
    精選 Bybit 支援之高市值、高流動性的 USDT 永續合約幣種（適用 scalping 多空雙向）
    資料來源：手動整理 Bybit 永續熱門幣種
    """
    return [
        "BTCUSDT",  # Bitcoin
        "ETHUSDT",  # Ethereum
        "SOLUSDT",  # Solana
        "BNBUSDT",  # BNB
        "XRPUSDT",  # Ripple
        "DOGEUSDT", # Dogecoin
        "OPUSDT",   # Optimism
        "ARBUSDT",  # Arbitrum
        "INJUSDT",  # Injective
        "LDOUSDT"   # Lido DAO
    ]
