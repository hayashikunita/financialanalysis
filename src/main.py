import subprocess, sys, os

def run(cmd: list):
	print(f"[RUN] {' '.join(cmd)}")
	r = subprocess.run(cmd, capture_output=True, text=True)
	if r.returncode != 0:
		print(r.stdout)
		print(r.stderr, file=sys.stderr)
		raise SystemExit(f"コマンド失敗: {' '.join(cmd)}")
	if r.stdout.strip():
		print(r.stdout)
	return r

def main():
	if len(sys.argv) < 2:
		print("使用法: uv run src/main.py <TICKER>  (例: uv run src/main.py 7203.T)")
		sys.exit(1)
	ticker = sys.argv[1]

	base = os.path.dirname(__file__)
	scripts_dir = os.path.join(base, 'scripts')

	# 1. Yahooから財務データ取得
	run([sys.executable, os.path.join(scripts_dir, 'yahoo2finance.py'), ticker, '--output_dir', 'data'])

	# 2. 分析CSV生成
	run([sys.executable, os.path.join(scripts_dir, 'alldata2analysisdata.py'), ticker])

	# 3. 個別指標グラフ自動HTML (analysisdata2graph_v2 が最新仕様ならそちらでも可)
	run([sys.executable, os.path.join(scripts_dir, 'analysisdata2graph.py'), ticker])

	# 3.5 全体財務可視化まとめ (alldata2visualization)
	vis_script = os.path.join(scripts_dir, 'alldata2visualization.py')
	if os.path.exists(vis_script):
		run([sys.executable, vis_script, ticker])

	# 4. 総合ブラウザポータル生成
	browser_script = os.path.join(scripts_dir, 'analysisdata2graph_browser.py')
	if os.path.exists(browser_script):
		run([sys.executable, browser_script, ticker])

	print("一連の処理が完了しました。")

if __name__ == '__main__':
	main()
