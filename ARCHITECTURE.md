---
title: 構成と拡張ガイド（ARCHITECTURE）
---

# 構成と拡張ガイド

この教材を**壊さず増やす**ための地図。新しいノート・演習・図・ツールを足すときの作法と、品質を保つ仕組みをまとめる。

## 全体構成

| 層 | 場所 | 役割 |
|---|---|---|
| 本文 | `notes/*.md` | 概念。冒頭に「30秒まとめ＋ツール導線」。図→定義→数値例→検証の順。 |
| 演習 | `exercises/{basic,intermediate,advanced,solutions}/` | 各モジュール3難易度＋解答。 |
| 触って学ぶ（公開） | `interactive/*.html` + `interactive/lib/` | **ブラウザ内で動く**素のJS+Plotly。`lib/stats.js`（確率関数）と`lib/tool.css`を共有。 |
| 数理コア（ローカル） | `apps/*/core.py` | Streamlit版の計算核（cvxpy等）。`python core.py`で self-test。 |
| 図 | `figures/*.svg`（一部 `scripts/*.py` で再生成） | 概念図・教材図。 |
| サイト | `mkdocs.yml` + GitHub Actions | MkDocs Material で `main` push 時に自動公開。 |

## 「単一の真実源」＝検証済み参照値

同じ数理が **JS（公開ツール）と Python（コア）の2か所**にある。乖離を防ぐ仕組み：

- **真実源は「検証済み参照値」**（scipy / 解析解 / cvxpy 最適値）。コードではなく数値が正。
- `interactive/lib/stats.test.mjs` … `stats.js` を **scipy 参照値**で検証（`node interactive/lib/stats.test.mjs`）。
- `apps/*/core.py` … 各コアに **self-test**（`python core.py`）。
- **CI**（`.github/workflows/test.yml`）が push 毎に両方を実行。どちらかが参照値からずれたら赤になる。

> 数値を変える変更をしたら、対応する期待値を**両方**のテストに反映すること。

## 拡張レシピ

**ノートを足す** → `notes/NN_xxx.md` を作り、冒頭に `!!! abstract "30秒まとめ"`（何の話か／分かること／使う場面＋ツール導線）。`mkdocs.yml` の nav に追加。数式は `$...$`、図は `![](../figures/...)`（**生 `<img>` は使わない**＝パス未補正）。

**演習を足す** → `exercises/<難易度>/NN_xxx.md` ＋ `solutions/`。難易度・前提・所要時間を明記。

**触って学ぶツールを足す** → `interactive/foo.html` を作り、`lib/tool.css`・Plotly CDN・`lib/stats.js` を読む。`window.LP` の関数を使う（**生 LaTeX は不可**＝Unicodeで `√`・`≤`）。`interactive/index.md` のカードと節に追加。新しい数理を入れたら `stats.js` に足し、`stats.test.mjs` に期待値を追加。

**埋め込み** → 単一ツールはページに直接 `iframe`（`src="../../interactive/foo.html"`）。複数を1ページに置くときは**クリック読込**（同時に重い Plotly を多重ロードしない）。

## 約束ごと

- 公開ツール（`interactive/*.html`）は **MathJax 無し** → 注釈は Unicode。
- ノートは MathJax あり → LaTeX 可。
- 文章・コメント・UI は日本語。数値は必ず手計算 or 参照値で裏取り。
- 秘密情報（鍵・ログ）はコミットしない（`.gitignore` 済み）。
