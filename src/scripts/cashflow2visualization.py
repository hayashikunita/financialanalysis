

import os
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots

def set_japanese_font():
	pass  # Plotlyは日本語フォント設定不要


def visualize_financials_csv(file_path):
	# 項目名をインデックス、年度を列名として読み込む
	df = pd.read_csv(file_path, index_col=0)
	print(f"Loaded {file_path} shape: {df.shape}")
	# 欠損値を除外
	df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)
	# 数値データのみ抽出
	df = df.apply(pd.to_numeric, errors='coerce')

	# キャッシュフロー関連の代表項目（日本語ラベル）
	main_items = {
		'Operating Cash Flow': '営業活動によるキャッシュフロー',
		'Investing Cash Flow': '投資活動によるキャッシュフロー',
		'Financing Cash Flow': '財務活動によるキャッシュフロー',
		'End Cash Position': '期末現金残高',
		'Beginning Cash Position': '期首現金残高',
		'Cash And Cash Equivalents': '現金及び現金同等物',
		'Free Cash Flow': 'フリーキャッシュフロー',
		'Capital Expenditure': '設備投資',
		'Depreciation': '減価償却費',
		'Change In Cash': '現金増減',
		'Net Income': '純利益',
		'Other Investing Cash Flow Items Total': 'その他投資活動キャッシュフロー合計',
		'Other Financing Cash Flow Items Total': 'その他財務活動キャッシュフロー合計',
		'Other Operating Cash Flow Items Total': 'その他営業活動キャッシュフロー合計',
	}
	# データに存在する代表項目のみ抽出
	selected = [item for item in main_items if item in df.index]
	# 代表項目がなければ最初の5項目
	if not selected:
		selected = df.index[:5]
		main_items = {k: k for k in selected}

	# ドロップダウン式で1つのグラフに項目切り替え
	colors = ["#00bfae", "#ff6f61", "#ffd600", "#8e24aa", "#43a047", "#039be5", "#f4511e", "#c0ca33", "#5e35b1", "#00897b"]
	traces = []
	buttons = []
	for i, idx in enumerate(selected):
		y = df.loc[idx].values
		text_labels = [f'{int(v):,}' if pd.notnull(v) else '' for v in y]
		pct_change = [None] + [((y[j] - y[j-1]) / y[j-1] * 100) if pd.notnull(y[j]) and pd.notnull(y[j-1]) and y[j-1] != 0 else None for j in range(1, len(y))]
		hover_texts = []
		for v, pct, col in zip(y, pct_change, df.columns):
			label = f"{main_items.get(idx, idx)}<br>年度: {col}<br>金額: {int(v):,} 円" if pd.notnull(v) else ""
			if pct is not None:
				label += f"<br>前年比: {pct:+.2f}%"
			hover_texts.append(label)
		traces.append(go.Scatter(
			x=df.columns,
			y=y,
			mode='lines+markers+text',
			name=main_items.get(idx, idx),
			line=dict(width=3, color=colors[i % len(colors)]),
			marker=dict(size=8, color=colors[i % len(colors)], symbol='circle'),
			text=text_labels,
			textposition='top center',
			hovertext=hover_texts,
			hoverinfo='text',
			hoverlabel=dict(bgcolor=colors[i % len(colors)], font_size=14, font_family="Meiryo, Yu Gothic, IPAexGothic, MS Gothic, sans-serif"),
			visible=(i==0)
		))
		buttons.append(dict(
			label=main_items.get(idx, idx),
			method='update',
			args=[{'visible': [j==i for j in range(len(selected))]},
				  {'title': f'2267.T {main_items.get(idx, idx)} 財務推移'}]
		))
	fig = go.Figure(traces)
	fig.update_yaxes(
		title=dict(text='金額（円）', font=dict(size=14, color="#ffd600")),
		tickformat=',',
		showgrid=True, gridcolor="#444", zerolinecolor="#888",
		color="#fff",
		tickfont=dict(size=12, color="#fff")
	)
	fig.update_xaxes(
		title_text='年度',
		showgrid=True, gridcolor="#444", zerolinecolor="#888",
		color="#fff", tickfont=dict(size=12, color="#fff")
	)
	fig.update_layout(
		title_text=f'2267.T {main_items.get(selected[0], selected[0])} 財務推移',
		title_font=dict(size=22, color="#ffd600"),
		height=500,
		showlegend=False,
		font=dict(family='Meiryo, Yu Gothic, IPAexGothic, MS Gothic, sans-serif', color="#fff"),
		template="plotly_dark",
		paper_bgcolor="#222",
		plot_bgcolor="#222",
		margin=dict(t=80, b=40, l=60, r=40),
		updatemenus=[dict(
			type='dropdown',
			direction='down',
			buttons=buttons,
			x=1.15,
			y=1.1,
			showactive=True,
			font=dict(color="#ffd600", size=16, family="Meiryo, Yu Gothic, IPAexGothic, MS Gothic, sans-serif")
		)]
	)
	html_path = 'financials_dropdown_visualization.html'
	pyo.plot(fig, filename=html_path, auto_open=True)

import sys


def main():
	if len(sys.argv) > 1:
		symbol = sys.argv[1]
	else:
		symbol = '2267.T'
	file_path = f'data/{symbol}/cashflow.csv'
	visualize_financials_csv(file_path)

if __name__ == '__main__':
	main()
