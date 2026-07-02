---
title: 読書ガイド（章別）
type: reference
updated: 2026-06-28
status: 主要査読論文8本の DOI 検証済み（2026-06-28）
---

# 読書ガイド

各章に対応する文献を、**読む順序**つきで示します。書誌情報は [`references.bib`](references.bib)。

> ✅ **書誌の確認状況**：主要な査読論文8本（CVaR・リスク尺度・ロバスト・DRO・チャンス制約・電力応用）の
> DOI・巻号・ページを 2026-06-28 に出版社/Crossref で確認済み（`references.bib` の `verified` フィールド）。
> 教科書の Springer/Princeton DOI は書名・年を確認済み（DOI 桁の最終確認は任意）。

---

## 第0章：なぜ確率が必要か
- `savage2012flaw` — 「平均の落とし穴」を一般向けに。第0章の動機づけ。
- `birge2011introduction` 第1章 — 確率計画の問題意識（決定論との対比）。

## 第1章：事象と確率
- `ross2019first` 第2–3章 — 標本空間・事象・条件付き確率・独立。
- `blitzstein2019introduction` 第1–2章 — ベイズの直感、基準率の誤謬。
- `bertsekas2008introduction` 第1章 — 公理的構成を簡潔に。

## 第2章：確率変数と分布
- `ross2019first` 第4–6章 — 離散・連続、PMF/PDF/CDF。
- `blitzstein2019introduction` 第3–5章 — 分布の関係、変換。

## 第3章：期待値・分散・相関
- `ross2019first` 第7章 — 期待値の線形性、共分散。
- `rockafellar2000optimization` — CVaR の定義と最適化（リスク尺度の入口）。
- `artzner1999coherent` — リスク尺度の公理（なぜ分散だけでは足りないか）。

## 第4章：データから分布へ
- `wasserman2004all` 第6–9章 — 経験分布、ノンパラ推定、最尤。
- `casella2002statistical` 第7章 — 点推定の枠組み。

## 第5章：シナリオとモンテカルロ
- `birge2011introduction` 第8–9章 — サンプル平均近似（SAA）、シナリオ生成。
- `shapiro2014lectures` — SAA の収束理論（発展）。

## 第6章：不確実性下の最適化
- 期待値・二段階：`birge2011introduction`、`shapiro2014lectures`
- ロバスト：`bental2009robust`、`bertsimas2004price`
- チャンス制約：`nemirovski2006convex`
- CVaR：`rockafellar2000optimization`、`artzner1999coherent`
- 分布ロバスト：`delage2010distributionally`、`esfahani2018data`
- 凸最適化の土台：`boyd2004convex`

## 電力システム応用（横断）
- `conejo2010decision` — 電力市場×確率計画の標準テキスト。
- `morales2014integrating` — 再エネ統合の運用問題。
- `bertsimas2013adaptive` — ロバスト×起動停止計画（UC）。
- `roald2023power` — 不確実性下の電力系統最適化レビュー（全体俯瞰に最適）。

---

## 読み方の指針
1. **まず本教材のノート**で直感と最小例を掴む。
2. 対応章を**該当箇所だけ**読む（通読しない）。
3. 数式は本教材の記法（[`../roadmap/notation.md`](../roadmap/notation.md)）に翻訳して読む。
4. 電力応用は `roald2023power` で地図を持ってから個別論文へ。
