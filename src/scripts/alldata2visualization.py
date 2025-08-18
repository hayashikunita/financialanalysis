

import sys
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo

# 代表項目（日本語ラベル）を各種定義
financials_items = {
	'Total Revenue': '売上高',
	'Operating Revenue': '営業収益',
	'Gross Profit': '売上総利益',
	'Operating Income': '営業利益',
	'EBITDA': 'EBITDA',
	'EBIT': 'EBIT',
	'Net Income': '純利益',
}
cashflow_items = {
	'Operating Cash Flow': '営業活動によるCF',
	'Investing Cash Flow': '投資活動によるCF',
	'Financing Cash Flow': '財務活動によるCF',
	'Free Cash Flow': 'フリーCF',
	'End Cash Position': '期末現金残高',
}
balancesheet_items = {
	'Total Assets': '総資産',
	'Total Liabilities': '総負債',
	'Shareholders Equity': '株主資本',
	'Common Stock Equity': '普通株主資本',
	'Retained Earnings': '利益剰余金',
	'Treasury Stock': '自己株式',
	'Ordinary Shares Number': '普通株式数',
	'Share Issued': '発行株式数',
	'Working Capital': '運転資本',
	'Net Tangible Assets': '純有形資産',
	'Tangible Book Value': '有形簿価',
}

def load_and_select(file_path, items_dict):
	df = pd.read_csv(file_path, index_col=0)
	selected = {k: v for k, v in items_dict.items() if k in df.index}
	# 代表項目がなければ最初の5項目
	if not selected:
		selected = {k: k for k in df.index[:5]}
	df_selected = df.loc[list(selected.keys())]
	df_selected.index = [selected[k] for k in df_selected.index]
	return df_selected

def plot_summary(fin_df, cash_df, bs_df):
	import plotly.graph_objs as go
	colors = ["#00bfae", "#ff6f61", "#ffd600", "#8e24aa", "#43a047", "#039be5", "#f4511e", "#c0ca33", "#5e35b1", "#00897b"]
	years = fin_df.columns.tolist()
	traces = []
	# 損益
	for i, idx in enumerate(fin_df.index):
		y = fin_df.loc[idx].values
		traces.append(go.Scatter(
			x=years, y=y, mode='lines+markers+text',
			name=f'損益: {idx}', line=dict(width=3, color=colors[i % len(colors)]),
			marker=dict(size=8, color=colors[i % len(colors)], symbol='circle'),
			text=[f'{int(v):,}' if pd.notnull(v) else '' for v in y],
			textposition='top center',
			hoverinfo='x+y+name',
			visible=True
		))
	# キャッシュフロー
	for i, idx in enumerate(cash_df.index):
		y = cash_df.loc[idx].values
		traces.append(go.Scatter(
			x=years, y=y, mode='lines+markers+text',
			name=f'CF: {idx}', line=dict(width=3, color=colors[i % len(colors)]),
			marker=dict(size=8, color=colors[i % len(colors)], symbol='circle'),
			text=[f'{int(v):,}' if pd.notnull(v) else '' for v in y],
			textposition='top center',
			hoverinfo='x+y+name',
			visible=False
		))
	# バランスシート
	for i, idx in enumerate(bs_df.index):
		y = bs_df.loc[idx].values
		traces.append(go.Scatter(
			x=years, y=y, mode='lines+markers+text',
			name=f'BS: {idx}', line=dict(width=3, color=colors[i % len(colors)]),
			marker=dict(size=8, color=colors[i % len(colors)], symbol='circle'),
			text=[f'{int(v):,}' if pd.notnull(v) else '' for v in y],
			textposition='top center',
			hoverinfo='x+y+name',
			visible=False
		))
	n_fin = len(fin_df.index)
	n_cash = len(cash_df.index)
	n_bs = len(bs_df.index)
	buttons = [
		dict(label='損益', method='update',
			args=[{'visible': [True]*n_fin + [False]*(n_cash+n_bs)},
				  {'title': '主要財務指標グラフ（損益）'}]),
		dict(label='キャッシュフロー', method='update',
			args=[{'visible': [False]*n_fin + [True]*n_cash + [False]*n_bs},
				  {'title': '主要財務指標グラフ（キャッシュフロー）'}]),
		dict(label='バランスシート', method='update',
			args=[{'visible': [False]*(n_fin+n_cash) + [True]*n_bs},
				  {'title': '主要財務指標グラフ（バランスシート）'}]),
	]
	fig = go.Figure(traces)
	fig.update_layout(
		title='主要財務指標グラフ（損益）',
		height=600, width=900,
		template='plotly_dark',
		font=dict(family='Meiryo, Yu Gothic, IPAexGothic, MS Gothic, sans-serif', color='#fff'),
		paper_bgcolor='#222', plot_bgcolor='#222',
		margin=dict(t=80, b=40, l=60, r=40),
		updatemenus=[dict(
			type='buttons',
			direction='right',
			buttons=buttons,
			x=0.5, y=1.15,
			showactive=True,
			font=dict(color='#ffd600', size=16, family='Meiryo, Yu Gothic, IPAexGothic, MS Gothic, sans-serif')
		)]
	)
	fig.update_xaxes(title_text='年度', showgrid=True, gridcolor='#444', zerolinecolor='#888', color='#fff', tickfont=dict(size=12, color='#fff'))
	fig.update_yaxes(title_text='金額（円）', tickformat=',', showgrid=True, gridcolor='#444', zerolinecolor='#888', color='#fff', tickfont=dict(size=12, color='#fff'))
	html_path = 'all_financials_summary_graph.html'
	pyo.plot(fig, filename=html_path, auto_open=True)
	print(f'まとめグラフを {html_path} に保存・表示しました。')

def main():
	fin_df = load_and_select('data/2267.T/financials.csv', financials_items)
	cash_df = load_and_select('data/2267.T/cashflow.csv', cashflow_items)
	bs_df = load_and_select('data/2267.T/balance_sheet.csv', balancesheet_items)
	plot_summary(fin_df, cash_df, bs_df)

if __name__ == '__main__':
	main()
