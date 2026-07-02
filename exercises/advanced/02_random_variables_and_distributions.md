---
title: "演習（発展）— 第2章 確率変数と分布"
module: 2
level: advanced
prerequisites: ["notes/02_random_variables_and_distributions.md", "apps/pdf_cdf_visualizer"]
estimated_time: 35–50 分
solutions: "../solutions/02_random_variables_and_distributions_solutions.md"
---

# 演習（発展）★★★ — 第2章

> 学習目標：裾の重さがリスク結論を変えること、PMF/PDF/CDF の統一を論じる。

## A2-1 ★★★（20分）
**学習目標**：裾の重さ（正規 vs 対数正規）。
同じ平均100・標準偏差30の正規と対数正規で、超過確率 $P(X>c)$（$c=150,200,250$）を比較するとどちらが大きくなりやすいか。裾の重さの観点で論じ、価格モデルに正規を使う危険を述べよ。（`apps/pdf_cdf_visualizer` で確認可。）

## A2-2 ★★★（15分）
**学習目標**：PMF/PDF/CDF の統一。
PMF と PDF を統一的に CDF から導く方法（離散はジャンプ幅、連続は微分）を説明し、「PDF と CDF は同じ情報の別表現」を自分の言葉でまとめよ。

## A2-3 ★★★（15分）
**学習目標**：分布選択を意思決定に接続。
ある地点の風力出力を確率分布で表したい。値域（0〜定格）・歪み・ゼロの頻度を考慮して候補分布を2つ挙げ、それぞれの長所短所を述べよ。さらに、その分布の**右裾**が 第6章のどの最適化（チャンス制約／CVaR）に効くか予想せよ。
