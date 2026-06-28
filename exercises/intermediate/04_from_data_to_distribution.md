---
title: "演習（中級）— Module 4 データから分布へ"
module: 4
level: intermediate
prerequisites: ["notes/04_from_data_to_distribution.md"]
estimated_time: 30–45 分
solutions: "../solutions/04_from_data_to_distribution_solutions.md"
---

# 演習（中級）★★ — Module 4

> 学習目標：iid の限界（季節性・非定常）、n−1 補正、値域・歪みの観点で分布選択を判断する。

## I4-1 ★★（12分）
**学習目標**：iid の限界（季節性）。
サンプル需要に正規分布を当てはめると適合度が悪い（KS 検定 p≈0.0007）。理由を「季節性・非定常」で説明し（夏94.6 vs 冬116.3）、改善策を述べよ。

## I4-2 ★★（8分）
**学習目標**：ベッセル補正。
なぜ標本分散は $n-1$ で割るのか（直感で）。$n$ で割るとどちらに偏るか。

## I4-3 ★★（10分）
**学習目標**：分布選択（値域・歪み）。
PV出力データに正規分布を当てはめる危険を2つ挙げよ（値域・歪みの観点）。代替案を1つ示せ。

## I4-4 ★★（12分）
**学習目標**：手を動かす（CSV→統計量）。
`data/daily_peak_demand.csv` を読み込み、(a) 標本平均・標準偏差、(b) 中央値と平均の差から歪みの有無、(c) ECDF で $P(\text{需要}\le110)$ を概算せよ（Python 可）。`data/` のデータは季節性を含む点に注意。
