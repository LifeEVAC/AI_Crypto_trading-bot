import ccxt
import os
import time

# ✅ 建立 OKX 交易連線
def create_okx_client():
    return ccxt.okx({
        'apiKey': os.getenv("OKX_API_KEY"),
        'secret': os.getenv("OKX_API_SECRET"),
        'password': os.getenv("OKX_API_PASSWORD"),
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot',  # 也可以改成 margin, future, swap
        }
    })

# ✅ 市價下單：做多用 "buy"，做空用 "sell"
def place_order(symbol="BTC/USDT", side="buy", amount=0.001):
    try:
        exchange = create_okx_client()
        order = exchange.create_market_order(symbol, side, amount)
        print(f"✅ 成功下單：{side.upper()} {symbol} @ 市價 × {amount}")
        return order
    except Exception as e:
        print(f"❌ 下單失敗：{e}")
        return None

# ✅ 自動監控價格：達到止盈 / 止損 就平倉
def monitor_position(entry_price, direction, symbol="BTC/USDT", amount=0.001,
                     take_profit_pct=0.02, stop_loss_pct=0.015):
    exchange = create_okx_client()

    # 計算 TP / SL 價格
    if direction == "long":
        take_profit = entry_price * (1 + take_profit_pct)
        stop_loss = entry_price * (1 - stop_loss_pct)
    else:  # short
        take_profit = entry_price * (1 - take_profit_pct)
        stop_loss = entry_price * (1 + stop_loss_pct)

    print(f"\n🎯 開始監控價格：{symbol}")
    print(f"🟢 TP 價格：{round(take_profit, 2)}")
    print(f"🔴 SL 價格：{round(stop_loss, 2)}")

    while True:
        try:
            ticker = exchange.fetch_ticker(symbol)
            price = ticker["last"]
            print(f"📉 當前價格：{price}")

            if direction == "long":
                if price >= take_profit:
                    print("✅ 觸及止盈！市價賣出")
                    exchange.create_market_order(symbol, "sell", amount)
                    break
                elif price <= stop_loss:
                    print("🛑 觸及止損！市價賣出")
                    exchange.create_market_order(symbol, "sell", amount)
                    break
            else:  # short
                if price <= take_profit:
                    print("✅ 觸及止盈！市價買回")
                    exchange.create_market_order(symbol, "buy", amount)
                    break
                elif price >= stop_loss:
                    print("🛑 觸及止損！市價買回")
                    exchange.create_market_order(symbol, "buy", amount)
                    break

            time.sleep(10)  # 每 10 秒檢查一次

        except Exception as e:
            print(f"⚠️ 監控錯誤：{e}")
            time.sleep(5)
