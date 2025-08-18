
import yfinance as yf
import pandas as pd
import os
import sys

def fetch_fundamentals(ticker: str, output_dir: str = 'data'):
	# ティッカーからyfinanceでデータ取得
	stock = yf.Ticker(ticker)
	print(f"Fetching data for {ticker}...")
	print(stock)
	# 財務諸表（損益計算書、貸借対照表、キャッシュフロー）取得
	financials = stock.financials
	print(financials)
	balance_sheet = stock.balance_sheet
	cashflow = stock.cashflow
	info = stock.info

	# 保存先ディレクトリ（output_dir/ティッカー名）を作成
	save_dir = os.path.join(output_dir, ticker)
	os.makedirs(save_dir, exist_ok=True)
	print(f"Saving data to {save_dir}...")

	# CSV保存（ティッカー名ディレクトリ内に格納）
	financials.to_csv(os.path.join(save_dir, 'financials.csv'))
	balance_sheet.to_csv(os.path.join(save_dir, 'balance_sheet.csv'))
	cashflow.to_csv(os.path.join(save_dir, 'cashflow.csv'))
	# infoはdictなのでDataFrame化
	pd.DataFrame([info]).to_csv(os.path.join(save_dir, 'info.csv'), index=False)

	print(f"{ticker}の財務データを{output_dir}に保存しました。")

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="ヤフーファイナンスから財務データを取得してCSV保存")
	parser.add_argument("ticker", type=str, help="取得したい銘柄のティッカー（例: 7203.T）")
	parser.add_argument("--output_dir", type=str, default="data", help="CSV保存先ディレクトリ")
	args = parser.parse_args()
	fetch_fundamentals(args.ticker, output_dir=args.output_dir)
    # uv run scripts\yahoo2finance.py 7203.T --output_dir data