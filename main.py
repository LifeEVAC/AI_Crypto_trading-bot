# main.py

import os
from crypto_symbols import get_crypto_symbols
from indicators import calculate_all_indicators
from bitcoin_models import predict_btc_winrate
from strategy import run_strategy
from exchange_trade import execute_orders
from sheets_writer import sync_all_to_sheet

def main():
    print("🚀 啟動 AI 加密貨幣交易機器人...\n")

    # ✅ Step 1：取得加密貨幣追蹤清單（可修改為 top10, 自選清單等）
    symbols = get_crypto_symbols()

    # ✅ Step 2：進行策略分析（傳入 symbol、分析指標、預測勝率）
    results = run_strategy(
        symbols=symbols,
        indicator_func=calculate_all_indicators,
        model_func=predict_btc_winrate
    )

    if not results:
        print("⚠️ 今日無推薦交易。")
        return

    # ✅ Step 3：是否進行真實交易？
    LIVE_TRADING = False  # 若要真實下單，改成 True 並設定 API 金鑰

    # ✅ Step 4：執行下單（支援模擬 or 真實下單）
    execute_orders(results, live=LIVE_TRADING)

    # ✅ Step 5：寫入 Google Sheets（追蹤紀錄）
    sync_all_to_sheet(results, is_live_trade=LIVE_TRADING)

    print("\n✅ 本日交易完成。")

if __name__ == "__main__":
    main()
