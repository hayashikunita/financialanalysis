# financialanalysis

日本株などのティッカーを指定して Yahoo Finance から財務データを取得し、指標計算とインタラクティブな可視化ポータル (Plotly + HTML/CSS/JS) を生成するツール群です。

## 主な機能

1. データ取得 (`yahoo2finance.py`)
	- yfinance を用いて 損益計算書 / 貸借対照表 / キャッシュフロー / info を CSV 保存
2. 指標計算 (`alldata2analysisdata.py`)
	- 成長率 / 利益率 / CF マージン / ROA / ROE / 自己資本比率 / EV / 理論株価 などを算出し `financial_analysis_summary.csv` を出力
3. 分析ポータル (`analysisdata2graph.py`)
	- 複数指標をチェックボックスでオン/オフ、フィルタ、テーブル表示、ダーク/ライト切替
4. 代表財務グループ比較ポータル (`alldata2visualization.py`)
	- 損益 / キャッシュフロー / バランスシート グループをワンクリックで切替表示 (グラフは Plotly)
5. 個別ステートメント可視化 (`financials2visualization.py`, `balancesheet2visualization.py` など)
	- ドロップダウンで代表項目を切替
例１
<img width="1888" height="776" alt="image" src="https://github.com/user-attachments/assets/720095b6-5253-40b3-90cd-447d7e3d4072" />

例２
<img width="1873" height="788" alt="image" src="https://github.com/user-attachments/assets/50666e13-d04f-4e49-beaa-9a7a8a2ff15c" />

例３
<img width="1886" height="778" alt="image" src="https://github.com/user-attachments/assets/70079f9d-c3e5-4be2-bbbb-4066cea19055" />

## 依存ライブラリ

`pyproject.toml` 参照。主要: pandas, plotly, yfinance, kaleido (静的画像化に利用可)。

## 推奨環境

Python 3.13+ (記載要件). Windows PowerShell での利用想定。

## 使い方 (基本フロー)

1. ティッカーの財務データ取得
```powershell
uv run src\scripts\yahoo2finance.py 7203.T --output_dir data
```
	生成: `data/7203.T/financials.csv`, `balance_sheet.csv`, `cashflow.csv`, `info.csv`

2. 財務指標計算
```powershell
uv run src\scripts\alldata2analysisdata.py 7203.T
```
	生成: `data/7203.T/financial_analysis_summary.csv`

3. 指標ポータル生成 (分析指標まとめ)
```powershell
uv run src\scripts\analysisdata2graph.py 7203.T
```
	出力: `data/7203.T/financial_analysis_portal.html` (自動でブラウザ起動)

4. 代表財務グループ可視化 (損益/CF/BS の切替)
```powershell
uv run src\scripts\alldata2visualization.py 7203.T
```
	出力: `data/7203.T/all_financials_summary_graph.html`

5. (任意) 個別ステートメント可視化
```powershell
uv run src\scripts\financials2visualization.py 7203.T
uv run src\scripts\balancesheet2visualization.py 7203.T
```

## 出力ファイル一覧 (例: 7203.T)

| 種別 | パス | 説明 |
|------|------|------|
| 取得データ | `data/7203.T/financials.csv` | 損益計算書 (yfinance) |
| 取得データ | `data/7203.T/balance_sheet.csv` | 貸借対照表 |
| 取得データ | `data/7203.T/cashflow.csv` | キャッシュフロー |
| 取得データ | `data/7203.T/info.csv` | 企業概要等 |
| 分析結果 | `data/7203.T/financial_analysis_summary.csv` | 算出した指標表 |
| 分析ポータル | `data/7203.T/financial_analysis_portal.html` | 指標多数の操作ポータル |
| グループ可視化 | `data/7203.T/all_financials_summary_graph.html` | 損益/CF/BS グループ切替グラフ |

## 各ポータルの操作

### `financial_analysis_portal.html`
- 指標フィルタ: テキスト入力で左側チェックボックスを絞り込み
- 全選択/全解除: チェック状態を一括変更
- 全表示/全非表示: チャート DOM 表示切替 (高速)
- 表を隠す: DataTables テーブル表示切替
- LIGHT / DARK: テーマ切替 (アニメ背景/ガラス風パネル)

### `all_financials_summary_graph.html`
- 損益 / キャッシュフロー / バランスシート ボタン: 該当グループのみ可視化 (Plotly trace の visible を切替)
- LIGHT / DARK テーマ切替

## スクリーンショット (キャプチャ) について

以下のディレクトリに PNG を配置してください (まだ空でも可):

```
docs/captures/
  financial_analysis_portal_light.png
  financial_analysis_portal_dark.png
  all_financials_summary_graph_light.png
  all_financials_summary_graph_dark.png
```

README から参照されるよう、将来追加する画像名は上記を推奨。画像を追加したら以下のように埋め込めます:

例１
<img width="1844" height="820" alt="image" src="https://github.com/user-attachments/assets/f34c449a-f79e-411c-b553-2c10af928776" />
例２
<img width="1841" height="746" alt="image" src="https://github.com/user-attachments/assets/29ad178b-aff9-404b-bb13-b609233cb25c" />
例３
<img width="1849" height="820" alt="image" src="https://github.com/user-attachments/assets/99c3c902-47dc-4bc1-8a74-58b11c9ae7d2" />

## よくあるトラブルシュート

| 症状 | 対処 |
|------|------|
| 取得 CSV が空/列が無い | yfinance の一時的失敗。しばらく待つ / ティッカー確認 |
| グラフが真っ白 | ブラウザキャッシュをクリア / JS コンソールエラー確認 |
| 指標が NaN | 元データに項目欠損。`alldata2analysisdata.py` 内 try/except によりスキップ済 |
| 文字化け | フォント無い場合は OS に日本語フォント導入 |

## 拡張アイデア (未実装)

- main パイプライン統合 (一括実行スクリプト) の自動生成
- 期間選択 (年度スライダー)
- 複数銘柄比較オーバーレイ
- 指標式のツールチップ表示

## ライセンス

`LICENSE` を参照。

---
更新日: 2025-08-19
