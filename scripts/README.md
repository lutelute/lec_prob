# scripts/ — 図・データ生成スクリプト

ノートで使う図は、ここに置いた**再生成可能な Python スクリプト**から生成します（`figures/` に出力）。
SVG を直接編集せず、必ずスクリプトを編集して再生成してください（再現性のため）。

## 実行方法

```bash
# リポジトリ直下で（venv 推奨）
python3 scripts/00_flaw_of_averages.py     # → figures/00_flaw_of_averages.svg
python3 scripts/01_bayes_base_rate.py      # → figures/01_bayes_base_rate.svg
python3 scripts/02_pdf_cdf_interval.py     # → figures/02_pdf_cdf_interval.svg
```

すべて一括：

```bash
for f in scripts/[0-9]*.py; do python3 "$f"; done
```

## ファイル

| スクリプト | 図 | 対応ノート |
|---|---|---|
| `00_flaw_of_averages.py` | 平均で計画する2つの罠（期待コスト曲線） | `notes/00_why_probability.md` |
| `01_bayes_base_rate.py` | 基準率の誤謬（1000件内訳＋事後確率曲線） | `notes/01_events_and_probability.md` |
| `02_pdf_cdf_interval.py` | 確率＝面積＝CDFの差 | `notes/02_*`／`apps/pdf_cdf_visualizer/` |
| `_style.py` | 共通スタイル（日本語フォント設定） | — |

## メモ
- 日本語フォントは `_style.setup_japanese_font()` が自動選択（macOS: Hiragino Sans 等）。
  見つからない環境では警告を出して継続（ラベルが豆腐になる）。
- matplotlib の文字に `≤` などの記号を使うときは mathtext（`$\leq$`）を使う（フォント非対応対策）。
- 依存：`numpy`, `scipy`, `matplotlib`（`requirements.txt`）。
