# okx_trade.py
import ccxt
import os

def create_okx_client():
    return ccxt.okx({
        'apiKey': os.getenv("OKX_API_KEY"),
        'secret': os.getenv("OKX_API_SECRET"),
        'password': os.getenv("OKX_API_PASSWORD"),
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot',
        }
    })

def place_order(symbol="BTC/USDT", side="buy", amount=0.001):
    try:
        exchange = create_okx_client()
        order = exchange.create_market_order(symbol, side, amount)
        print(f"✅ 下單成功：{order}")
        return order
    except Exception as e:
        print(f"❌ 下單失敗: {e}")
        return None
