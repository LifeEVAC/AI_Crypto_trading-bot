# exchange_trade.py

import os
from bybit import bybit
import math

# 初始化 API（需要設在 Render 環境變數中）
api_key = os.getenv("BYBIT_API_KEY")
api_secret = os.getenv("BYBIT_API_SECRET")

client = bybit(test=False, api_key=api_key, api_secret=api_secret)

def place_order(symbol, side, qty, tp_price, sl_price):
    """
    發送市價單 + 條件 TP/SL（市價止盈止損）
    - symbol: "BTCUSDT"
    - side: "Buy" 或 "Sell"
    - qty: 數量（整數）
    - tp_price / sl_price: USD 價格
    """
    try:
        # 先送出市價單
        order = client.Order.Order_new(
            side=side,
            symbol=symbol,
            order_type="Market",
            qty=qty,
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False
        ).result()

        print(f"✅ 市價下單成功：{symbol} {side} x{qty}")

        # 設定 TP / SL
        client.Positions.Positions_trading_stop(
            symbol=symbol,
            take_profit=tp_price,
            stop_loss=sl_price
        ).result()

        print(f"🎯 已設定 TP / SL：TP={tp_price}, SL={sl_price}")

    except Exception as e:
        print(f"❌ 下單失敗：{symbol} - {e}")

def execute_orders(results, live=False):
    """
    根據選股結果執行下單流程
    """
    for res in results:
        symbol = res["symbol"]
        side = "Buy" if res["direction"] == "long" else "Sell"
        price = res["price"]
        capital = res["capital"]
        tp_pct = res["tp_pct"]
        sl_pct = res["sl_pct"]

        # 換算合約數量（以 1x 槓桿下單，精確到小數點 3 位）
        qty = round(capital / price, 3)

        tp_price = round(price * (1 + tp_pct), 2) if side == "Buy" else round(price * (1 - tp_pct), 2)
        sl_price = round(price * (1 - sl_pct), 2) if side == "Buy" else round(price * (1 + sl_pct), 2)

        if live:
            place_order(symbol, side, qty, tp_price, sl_price)
        else:
            print(f"📦 模擬下單 {symbol} {side} x{qty}｜TP: {tp_price}｜SL: {sl_price}")
