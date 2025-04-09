# exchange_trade.py

import os
from bybit import bybit
import math

# ✅ 使用測試網（testnet=True）
client = bybit(
    test=True,
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET")
)

def place_order(symbol, side, qty, tp_price, sl_price):
    """
    發送市價單 + 附帶 TP / SL（使用測試網模擬）
    """
    try:
        order = client.Order.Order_new(
            side=side,
            symbol=symbol,
            order_type="Market",
            qty=qty,
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False
        ).result()

        print(f"✅ 模擬下單成功：{symbol} {side} x{qty}")

        # TP / SL
        client.Positions.Positions_trading_stop(
            symbol=symbol,
            take_profit=tp_price,
            stop_loss=sl_price
        ).result()

        print(f"🎯 設定 TP={tp_price} / SL={sl_price} 完成")

    except Exception as e:
        print(f"❌ 模擬下單失敗：{symbol} - {e}")

def execute_orders(results, live=False):
    """
    執行模擬或真實交易（測試環境預設 live=False）
    """
    for res in results:
        symbol = res["symbol"]
        side = "Buy" if res["direction"] == "long" else "Sell"
        price = res["price"]
        capital = res["capital"]
        tp_pct = res["tp_pct"]
        sl_pct = res["sl_pct"]

        qty = round(capital / price, 3)
        tp_price = round(price * (1 + tp_pct), 2) if side == "Buy" else round(price * (1 - tp_pct), 2)
        sl_price = round(price * (1 - sl_pct), 2) if side == "Buy" else round(price * (1 + sl_pct), 2)

        if live:
            place_order(symbol, side, qty, tp_price, sl_price)
        else:
            print(f"🧪 模擬：{symbol} {side} x{qty}｜TP: {tp_price}｜SL: {sl_price}")
