
import pandas as pd

# ファイルパス
financials_path = 'data/2267.T/financials.csv'
cashflow_path = 'data/2267.T/cashflow.csv'
balancesheet_path = 'data/2267.T/balance_sheet.csv'

# DataFrameとして読み込み
df_financials = pd.read_csv(financials_path, index_col=0)
df_cashflow = pd.read_csv(cashflow_path, index_col=0)
df_balancesheet = pd.read_csv(balancesheet_path, index_col=0)

# 確認用出力

# --- 財務分析 ---
years = df_financials.columns.tolist()
analysis = pd.DataFrame(index=years)

# 売上高成長率
try:
	sales = df_financials.loc['Total Revenue']
	analysis['売上高成長率(%)'] = sales.pct_change() * 100
except Exception:
	pass
# 営業利益率
try:
	analysis['営業利益率(%)'] = (df_financials.loc['Operating Income'] / df_financials.loc['Total Revenue']) * 100
except Exception:
	pass
# 純利益率
try:
	analysis['純利益率(%)'] = (df_financials.loc['Net Income'] / df_financials.loc['Total Revenue']) * 100
except Exception:
	pass
# 営業CFマージン
try:
	analysis['営業CFマージン(%)'] = (df_cashflow.loc['Operating Cash Flow'] / df_financials.loc['Total Revenue']) * 100
except Exception:
	pass
# フリーCFマージン
try:
	analysis['フリーCFマージン(%)'] = (df_cashflow.loc['Free Cash Flow'] / df_financials.loc['Total Revenue']) * 100
except Exception:
	pass
# 自己資本比率
try:
	analysis['自己資本比率(%)'] = (df_balancesheet.loc['Stockholders Equity'] / df_balancesheet.loc['Total Assets']) * 100
except Exception:
	pass
# 流動比率
try:
	analysis['流動比率(%)'] = (df_balancesheet.loc['Current Assets'] / df_balancesheet.loc['Current Liabilities']) * 100
except Exception:
	pass
# 有利子負債比率
try:
	analysis['有利子負債比率(%)'] = (df_balancesheet.loc['Total Liabilities Net Minority Interest'] / df_balancesheet.loc['Total Assets']) * 100
except Exception:
	pass

# ROA（総資産利益率）
try:
	analysis['ROA(%)'] = (df_financials.loc['Net Income'] / df_balancesheet.loc['Total Assets']) * 100
except Exception:
	pass

# ROE（自己資本利益率）
try:
	analysis['ROE(%)'] = (df_financials.loc['Net Income'] / df_balancesheet.loc['Stockholders Equity']) * 100
except Exception:
	pass

# インタレストガバレッジレシオ（Interest Coverage Ratio）
try:
	# 営業利益 / 支払利息（支払利息項目がなければ空欄）
	if 'Interest Expense' in df_financials.index:
		analysis['インタレストガバレッジレシオ'] = df_financials.loc['Operating Income'] / abs(df_financials.loc['Interest Expense'])
except Exception:
	pass

# 固定長期適合率
try:
	# 固定資産 / (株主資本 + 固定負債)
	if 'Total Non Current Assets' in df_balancesheet.index and 'Stockholders Equity' in df_balancesheet.index and 'Total Non Current Liabilities Net Minority Interest' in df_balancesheet.index:
		analysis['固定長期適合率(%)'] = (df_balancesheet.loc['Total Non Current Assets'] / (df_balancesheet.loc['Stockholders Equity'] + df_balancesheet.loc['Total Non Current Liabilities Net Minority Interest'])) * 100
except Exception:
	pass

# 企業価値（EV: Enterprise Value）
try:
	# EV = 時価総額 + 有利子負債 - 現金及び現金同等物
	if 'Share Issued' in df_balancesheet.index and 'Stockholders Equity' in df_balancesheet.index and 'Total Debt' in df_balancesheet.index and 'Cash And Cash Equivalents' in df_balancesheet.index:
		# 仮に株価を取得できない場合は株主資本を時価総額とみなす
		market_cap = df_balancesheet.loc['Stockholders Equity']
		enterprise_value = market_cap + df_balancesheet.loc['Total Debt'] - df_balancesheet.loc['Cash And Cash Equivalents']
		analysis['企業価値(EV)'] = enterprise_value
except Exception:
	pass

# 理論株価（簡易版：BPS×PBR=株価）
try:
	# BPS = 株主資本 / 発行済株式数
	if 'Stockholders Equity' in df_balancesheet.index and 'Share Issued' in df_balancesheet.index:
		bps = df_balancesheet.loc['Stockholders Equity'] / df_balancesheet.loc['Share Issued']
		# PBR（仮に1倍とする）
		analysis['理論株価'] = bps * 1
except Exception:
	pass

# 結果表示
print('\n財務分析サマリー')
print(analysis.round(2))


# 出力先ディレクトリ（元CSVと同じ場所）
output_dir = 'data/2267.T/'
csv_path = output_dir + 'financial_analysis_summary.csv'
analysis.round(2).to_csv(csv_path, encoding='utf-8-sig')
print(f'分析サマリーを {csv_path} に保存しました。')
