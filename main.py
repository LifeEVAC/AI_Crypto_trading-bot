
import os
import json
from strategy import run_strategy
from exchange_trade import execute_orders
from sheets_writer import sync_all_to_sheet
from crypto_symbols import get_all_symbols

def write_google_service_account():
    key_json = os.getenv("GOOGLE_SERVICE_KEY")
    if key_json:
        with open("service_account.json", "w") as f:
            json.dump(json.loads(key_json), f)

write_google_service_account()

def main():
    print("🔁 啟動 Crypto AI 自動選幣流程...")
    symbol_list = get_all_symbols()
    LIVE_TRADING = False

    results = run_strategy(symbol_list)

    if not results:
        print("⚠️ 今日無推薦幣種。")
        return

    execute_orders(results, live=LIVE_TRADING)
    sync_all_to_sheet(results, is_live_trade=LIVE_TRADING)
    print("✅ AI 自動選幣流程結束！")

if __name__ == "__main__":
    main()
