import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
import os, sys, html

r"""
ブラウザ上で全指標を操作しながら閲覧できるポータル。
機能:
 - 指標チェックボックスで複数同時表示/非表示
 - 全表示/全非表示ボタン
 - 指標名フィルタ入力
 - 元データテーブル(DataTablesで検索/ソート)
 - 数値は自動数値化 (カンマ/全角マイナス対応)
使い方:
 uv run src\scripts\analysisdata2graph_browser.py 3030.T
 出力: data/<symbol>/financial_analysis_portal.html を自動オープン
"""

if len(sys.argv) > 1:
    symbol = sys.argv[1]
else:
    symbol = '2267.T'

csv_path = f'data/{symbol}/financial_analysis_summary.csv'
if not os.path.exists(csv_path):
    print(f'ファイルがありません: {csv_path}')
    sys.exit(1)

# 読み込み
df = pd.read_csv(csv_path, index_col=0)

# 有効指標抽出
metrics = [c for c in df.columns if df[c].notna().any()]
years = df.index.tolist()

# 数値化ヘルパ
clean_df = pd.DataFrame(index=df.index)
for m in metrics:
    ser = df[m].astype(str).str.replace(',', '').str.replace('−', '-').str.strip()
    clean_df[m] = pd.to_numeric(ser, errors='coerce')

fig_divs = []
plotly_js_included = False
for i, m in enumerate(metrics):
    values = clean_df[m]
    if values.notna().sum() == 0:
        continue
    is_bar = m in ['企業価値(EV)', '理論株価']
    if is_bar:
        trace = go.Bar(x=years, y=values, name=m, text=[f'{v:,.2f}' if pd.notna(v) else '' for v in values], textposition='auto')
    else:
        trace = go.Scatter(x=years, y=values, mode='lines+markers', name=m, text=[f'{v:.2f}' if pd.notna(v) else '' for v in values], textposition='top center')
    layout = go.Layout(title=m, xaxis=dict(title='年度', type='category'), yaxis=dict(title=m), margin=dict(l=60, r=20, t=50, b=50))
    fig = go.Figure(data=[trace], layout=layout)
    div = pyo.plot(fig, include_plotlyjs=not plotly_js_included, output_type='div', show_link=False)
    plotly_js_included = True
    fig_divs.append((m, div))

# Data table (元のdfそのまま / HTMLエスケープ)
styled_df = df.copy()
html_table = styled_df.to_html(classes='display compact', border=0)

style_block = f"""
<style>
:root {{ --bg-gradient: linear-gradient(135deg,#1b1f3a,#3a1b4d,#052b45); --panel-bg: rgba(255,255,255,0.65); --panel-border: rgba(255,255,255,0.25); --text-color:#222; --accent:#6a35ff; --accent-grad:linear-gradient(90deg,#7f5cff,#5f9dff); --shadow:0 4px 14px -4px rgba(0,0,0,.35); --chart-card-bg:rgba(255,255,255,0.55); }}
body.dark {{ --bg-gradient: radial-gradient(circle at 20% 20%,#1e2950,#090d18 60%); --panel-bg: rgba(40,46,66,0.55); --panel-border: rgba(255,255,255,0.08); --text-color:#eee; --accent:#9d7bff; --accent-grad:linear-gradient(90deg,#9d7bff,#46c2ff); --shadow:0 6px 18px -6px rgba(0,0,0,.55); --chart-card-bg:rgba(33,39,58,0.55); }}
html,body{{height:100%;}}
body{{font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;margin:0;padding:18px;color:var(--text-color);background:#111;background-image:var(--bg-gradient);background-attachment:fixed;animation:bgShift 18s ease-in-out infinite alternate;}}
@keyframes bgShift {{ 0%{{filter:hue-rotate(0deg);}} 100%{{filter:hue-rotate(35deg);}} }}
h1{{margin:4px 0 22px;font-weight:600;letter-spacing:.5px;background:var(--accent-grad);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 2px 6px rgba(0,0,0,.35));}}
.stars{{position:fixed;inset:0;pointer-events:none;z-index:0;background:repeating-radial-gradient(circle at 10% 20%,rgba(255,255,255,.4)0 1px,transparent 1px 60px),repeating-radial-gradient(circle at 80% 60%,rgba(255,255,255,.35)0 1px,transparent 1px 50px);animation: twinkle 12s linear infinite;opacity:.35;}}
@keyframes twinkle {{ from{{transform:translateY(0);}} to{{transform:translateY(60px);}} }}
.controls{{position:relative;z-index:1;background:var(--panel-bg);backdrop-filter:blur(10px) saturate(160%);-webkit-backdrop-filter:blur(10px) saturate(160%);padding:14px 16px;border-radius:16px;border:1px solid var(--panel-border);box-shadow:var(--shadow);margin-bottom:20px;}}
.metric-list{{columns:3;-webkit-columns:3;-moz-columns:3;font-size:13px;column-gap:18px;}}
.metric-item{{break-inside:avoid;display:block;margin:4px 0;padding:3px 6px;border-radius:6px;transition:background .25s;}} .metric-item:hover{{background:rgba(255,255,255,.25);}}
body.dark .metric-item:hover{{background:rgba(255,255,255,.07);}}
.chart-container{{position:relative;z-index:1;border:1px solid var(--panel-border);padding:10px 10px 14px;border-radius:18px;margin-bottom:26px;background:var(--chart-card-bg);backdrop-filter:blur(8px) saturate(160%);-webkit-backdrop-filter:blur(8px) saturate(160%);box-shadow:var(--shadow);transition:transform .35s, box-shadow .35s;}}
.chart-container:hover{{transform:translateY(-4px);box-shadow:0 10px 28px -8px rgba(0,0,0,.55);}}
.table-wrap{{margin-top:38px;z-index:1;position:relative;background:var(--panel-bg);padding:14px 18px 24px;border-radius:18px;border:1px solid var(--panel-border);backdrop-filter:blur(10px) saturate(160%);box-shadow:var(--shadow);}}
button{{margin-right:8px;margin-top:6px;background:var(--accent-grad);color:#fff;border:none;padding:8px 16px;font-size:13px;border-radius:999px;cursor:pointer;font-weight:500;letter-spacing:.5px;box-shadow:0 3px 8px -2px rgba(0,0,0,.4);transition:filter .25s, transform .25s;}} button:hover{{filter:brightness(1.08);}} button:active{{transform:translateY(2px);}}
#filterBox{{width:230px;padding:8px 10px;border-radius:10px;border:1px solid var(--panel-border);background:rgba(255,255,255,.65);backdrop-filter:blur(6px);outline:none;}} body.dark #filterBox{{background:rgba(30,35,52,.65);color:var(--text-color);}}
input[type=checkbox]{{accent-color:var(--accent);}} body.dark input[type=checkbox]{{filter:brightness(1.1);}}
table.dataTable{{width:100%!important;background:transparent;}} table.dataTable thead th{{background:linear-gradient(90deg,rgba(255,255,255,.35),rgba(255,255,255,.15));border-bottom:none;}} body.dark table.dataTable thead th{{background:linear-gradient(90deg,rgba(255,255,255,.08),rgba(255,255,255,.02));color:var(--text-color);}} table.dataTable tbody td{{background:transparent;}}
.footer-note{{margin-top:60px;font-size:11px;opacity:.65;text-align:center;}} a{{color:var(--accent);text-decoration:none;}} a:hover{{text-decoration:underline;}}
.theme-toggle{{float:right;margin-top:-4px;}}
</style>
"""
html_parts = [
  '<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8" />',
  f'<title>財務分析ポータル - {html.escape(symbol)}</title>',
  '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>',
  '<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>',
  '<link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.min.css" />',
  '<script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>',
  style_block,
  '</head><body class="dark">',
  '<div class="stars"></div>'
]
html_parts.append(f'<h1>財務分析ポータル ({html.escape(symbol)})</h1>')
html_parts.append('<div class="controls">')
html_parts.append('<div style="margin-bottom:8px;">指標フィルタ: <input id="filterBox" type="text" placeholder="例: ROE" oninput="filterMetrics()" />')
html_parts.append('<button onclick="checkAll(true)">全選択</button><button onclick="checkAll(false)">全解除</button>')
html_parts.append('<button onclick="toggleAllCharts(true)">全表示</button><button onclick="toggleAllCharts(false)">全非表示</button>')
html_parts.append('<button onclick="toggleTable()" id="tblBtn">表を隠す</button>')
html_parts.append('<button class="theme-toggle" onclick="toggleTheme()" id="themeBtn">LIGHT</button>')
html_parts.append('</div>')
html_parts.append('<div class="metric-list" id="metricList">')
for i, (m, _) in enumerate(fig_divs):
    checked = 'checked' if i < 6 else ''  # 最初の数個だけ表示
    safe = html.escape(m)
    html_parts.append(f'<label class="metric-item"><input type="checkbox" class="metricChk" data-target="chart_{i}" onchange="onMetricToggle(this)" {checked}/> {safe}</label>')
html_parts.append('</div></div>')

for i, (m, div) in enumerate(fig_divs):
    style = '' if i < 6 else 'style="display:none;"'
    html_parts.append(f'<div id="chart_{i}" class="chart-container" {style}>{div}</div>')

html_parts.append('<div class="table-wrap" id="tableWrap"><h2>元データ</h2>')
html_parts.append(html_table)
html_parts.append('</div>')

html_parts.append("""
<script>
function onMetricToggle(cb) {{
  const id = cb.getAttribute('data-target');
  const el = document.getElementById(id);
  if (!el) return;
  el.style.display = cb.checked ? 'block' : 'none';
}}
function checkAll(state) {{
  document.querySelectorAll('.metricChk').forEach(cb => {{ cb.checked = state; onMetricToggle(cb); }});
}}
function toggleAllCharts(state) {{
  document.querySelectorAll('.metricChk').forEach(cb => {{ cb.checked = state; onMetricToggle(cb); }});
}}
function filterMetrics() {{
  const q = document.getElementById('filterBox').value.toLowerCase();
  document.querySelectorAll('#metricList label').forEach(lab => {{
    const txt = lab.textContent.toLowerCase();
    lab.style.display = txt.indexOf(q) !== -1 ? 'inline-block' : 'none';
  }});
}}
function toggleTable() {{
  const w = document.getElementById('tableWrap');
  const b = document.getElementById('tblBtn');
  if (w.style.display === 'none') {{ w.style.display = 'block'; b.textContent='表を隠す'; }} else {{ w.style.display='none'; b.textContent='表を表示'; }}
}}
$(document).ready(function() {{
  $('table.display').DataTable({{ paging:false, searching:true, info:false, order:[] }});
}});
function toggleTheme(){
  const b=document.body;const btn=document.getElementById('themeBtn');
  b.classList.toggle('dark');
  btn.textContent = b.classList.contains('dark') ? 'LIGHT' : 'DARK';
}
</script>
""")

html_parts.append('</body></html>')

out_path = f'data/{symbol}/financial_analysis_portal.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_parts))

print(f'ポータルを {out_path} に出力しました。ブラウザを開きます。')
import webbrowser
webbrowser.open('file://' + os.path.abspath(out_path))
