

import sys, os
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

def build_portal(fin_df, cash_df, bs_df, symbol):
	colors = ["#00bfae", "#ff6f61", "#ffd600", "#8e24aa", "#43a047", "#039be5", "#f4511e", "#c0ca33", "#5e35b1", "#00897b"]
	years = fin_df.columns.tolist()
	traces = []
	groups = []  # (group_name, index in traces slice)
	# 損益
	for i, idx in enumerate(fin_df.index):
		y = fin_df.loc[idx].values
		traces.append(go.Scatter(
			x=years, y=y, mode='lines+markers', name=f'損益:{idx}',
			line=dict(width=3, color=colors[i % len(colors)]), marker=dict(size=7)
		))
	groups.append(("損益", len(traces)))
	# キャッシュフロー
	start_cash = len(traces)
	for i, idx in enumerate(cash_df.index):
		y = cash_df.loc[idx].values
		traces.append(go.Scatter(
			x=years, y=y, mode='lines+markers', name=f'CF:{idx}',
			line=dict(width=3, dash='dot', color=colors[(i+3) % len(colors)]), marker=dict(size=7)
		))
	groups.append(("キャッシュフロー", len(traces)))
	# バランスシート
	for i, idx in enumerate(bs_df.index):
		y = bs_df.loc[idx].values
		traces.append(go.Scatter(
			x=years, y=y, mode='lines+markers', name=f'BS:{idx}',
			line=dict(width=3, dash='dash', color=colors[(i+6) % len(colors)]), marker=dict(size=7)
		))
	groups.append(("バランスシート", len(traces)))

	fig = go.Figure(traces)
	fig.update_layout(
		title=f"主要財務指標 (初期表示: 損益)",
		template='plotly_dark',
		height=640,
		legend=dict(orientation='h', yanchor='bottom', y=1.02, x=0, font=dict(size=11)),
		margin=dict(t=90, b=50, l=60, r=30),
		font=dict(family='Meiryo, Yu Gothic, sans-serif'),
	)
	fig.update_xaxes(title='年度', type='category')
	fig.update_yaxes(title='金額（おおよそ）', tickformat=',')

	# 初期で損益以外非表示
	n_fin = len(fin_df.index)
	for j, tr in enumerate(fig.data):
		if j >= n_fin:
			tr.visible = False

	div = pyo.plot(fig, include_plotlyjs=True, output_type='div', show_link=False)

	style_block = """
<style>
/* reuse stylish theme */
:root { --bg-gradient: linear-gradient(135deg,#141e30,#243b55); --panel-bg: rgba(255,255,255,0.55); --panel-border: rgba(255,255,255,0.25); --text-color:#222; --accent:#6a35ff; --accent-grad:linear-gradient(90deg,#7f5cff,#5f9dff); --shadow:0 4px 14px -4px rgba(0,0,0,.35); }
body.dark { --bg-gradient: radial-gradient(circle at 20% 20%,#101522,#05070b 70%); --panel-bg: rgba(40,46,66,0.55); --panel-border: rgba(255,255,255,0.08); --text-color:#eee; --accent:#9d7bff; --accent-grad:linear-gradient(90deg,#9d7bff,#46c2ff); --shadow:0 6px 18px -6px rgba(0,0,0,.55); }
html,body{height:100%;}
body{margin:0;padding:18px;font-family: 'Segoe UI','Helvetica Neue',Arial,sans-serif;color:var(--text-color);background:#111;background-image:var(--bg-gradient);background-attachment:fixed;}
h1{margin:4px 0 18px;font-weight:600;letter-spacing:.5px;background:var(--accent-grad);-webkit-background-clip:text;color:transparent;}
.stars{position:fixed;inset:0;pointer-events:none;z-index:0;background:repeating-radial-gradient(circle at 10% 20%,rgba(255,255,255,.4)0 1px,transparent 1px 60px),repeating-radial-gradient(circle at 80% 60%,rgba(255,255,255,.35)0 1px,transparent 1px 50px);animation: twinkle 14s linear infinite;opacity:.30;}
@keyframes twinkle { from{transform:translateY(0);} to{transform:translateY(60px);} }
.panel{position:relative;z-index:1;background:var(--panel-bg);backdrop-filter:blur(10px) saturate(160%);padding:14px 18px;border-radius:18px;border:1px solid var(--panel-border);box-shadow:var(--shadow);margin-bottom:22px;}
button{margin:4px 6px 4px 0;background:var(--accent-grad);color:#fff;border:none;padding:7px 14px;font-size:12px;border-radius:999px;cursor:pointer;font-weight:500;letter-spacing:.5px;box-shadow:0 3px 8px -2px rgba(0,0,0,.4);}
button:hover{filter:brightness(1.1);} button:active{transform:translateY(2px);} 
.theme-toggle{float:right;}
.footer{margin-top:40px;font-size:11px;opacity:.6;text-align:center;}
</style>
"""

	# JS: show groups (f-string を避け、{ } エスケープ不要化)
	import json
	group_json = json.dumps(groups, ensure_ascii=False)
	js = """
<script>
const groupBounds = __GROUP_JSON__; // [ [name, endIndex], ... ]
function showGroup(name) {
	const div = document.querySelector('.js-plotly-plot');
	if(!window.Plotly || !div) return;
	let endPrev = 0;
	for (let i=0;i<groupBounds.length;i++) {
		const g = groupBounds[i];
		const end = g[1];
		for (let t=endPrev; t<end; t++) {
			const vis = (g[0] === name);
			Plotly.restyle(div, {visible:[vis]}, [t]);
		}
		endPrev = end;
	}
}
function toggleTheme() {
	const b=document.body; const btn=document.getElementById('themeBtn');
	b.classList.toggle('dark');
	btn.textContent = b.classList.contains('dark') ? 'LIGHT' : 'DARK';
}
</script>
""".replace('__GROUP_JSON__', group_json)

	html_parts = [
		'<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8" />',
		f'<title>財務まとめ - {symbol}</title>',
		style_block,
		'</head><body class="dark">',
		'<div class="stars"></div>',
		f'<h1>財務まとめ ({symbol})</h1>',
			'<div class="panel">表示グループ: ' + ' '.join([f'<button onclick="showGroup(\''+g[0]+'\')">'+g[0]+'</button>' for g in groups]) + '<button class="theme-toggle" id="themeBtn" onclick="toggleTheme()">LIGHT</button></div>',
			div,
		js,
		'<div class="footer">Generated portal</div>',
		'</body></html>'
	]
	return '\n'.join(html_parts)


def main():
	if len(sys.argv) > 1:
		symbol = sys.argv[1]
	else:
		symbol = '2267.T'
	base_dir = f'data/{symbol}/'
	fin_df = load_and_select(base_dir + 'financials.csv', financials_items)
	cash_df = load_and_select(base_dir + 'cashflow.csv', cashflow_items)
	bs_df = load_and_select(base_dir + 'balance_sheet.csv', balancesheet_items)
	html = build_portal(fin_df, cash_df, bs_df, symbol)
	out_path = os.path.join(base_dir, 'all_financials_summary_graph.html')
	with open(out_path, 'w', encoding='utf-8') as f:
		f.write(html)
	print(f'まとめグラフポータルを {out_path} に出力しました。ブラウザを開きます。')
	import webbrowser; webbrowser.open('file://' + os.path.abspath(out_path))

if __name__ == '__main__':
	main()
