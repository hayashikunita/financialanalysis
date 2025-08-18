



import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
pio.renderers.default = "browser"

# financial_analysis_summary.csvをグラフ表示するスクリプト

import sys
if len(sys.argv) > 1:
    symbol = sys.argv[1]
else:
    symbol = '2267.T'
csv_path = f'data/{symbol}/financial_analysis_summary.csv'
df = pd.read_csv(csv_path, index_col=0)

# 指標リスト（数値のみ抽出、空欄や全NaNは除外）
metrics = [col for col in df.columns if df[col].notna().any()]
years = df.index.tolist()

print('表示したい指標を選んでください:')
for i, metric in enumerate(metrics):
    print(f'{i}: {metric}')

while True:
    try:
        idx = int(input('指標番号を入力（終了は-1）: '))
        if idx == -1:
            print('終了します。')
            break
        if idx < 0 or idx >= len(metrics):
            print('範囲外です。')
            continue
        metric = metrics[idx]
        values = df[metric]
        if metric in ['企業価値(EV)', '理論株価']:
            trace = go.Bar(
                x=years,
                y=values,
                name=metric,
                text=[f'{v:.2f}' if pd.notna(v) else '' for v in values],
                textposition='auto'
            )
        else:
            trace = go.Scatter(
                x=years,
                y=values,
                mode='lines+markers+text',
                name=metric,
                text=[f'{v:.2f}' if pd.notna(v) else '' for v in values],
                textposition='top center'
            )
        layout = go.Layout(title=metric, xaxis=dict(title='年度'), yaxis=dict(title=metric))
        fig = go.Figure(data=[trace], layout=layout)
        fig.show()
    except Exception as e:
        print(f'エラー: {e}')
