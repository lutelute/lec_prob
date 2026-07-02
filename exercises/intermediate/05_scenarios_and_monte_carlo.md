---
title: "演習（中級）— 第5章 シナリオとモンテカルロ"
module: 5
level: intermediate
prerequisites: ["notes/05_scenarios_and_monte_carlo.md"]
estimated_time: 30–45 分
solutions: "../solutions/05_scenarios_and_monte_carlo_solutions.md"
---

# 演習（中級）★★ — 第5章

> 学習目標：希少事象の難しさ、SAA の収束、CI を添える理由を説明する。

## I5-1 ★★（12分）
**学習目標**：希少事象の難しさ。
$P(X>145)=0.00135$ を MC で推定するとき、$N=1000$ で何が起きるか。安定推定に必要なサンプル規模の目安と理由を述べよ。

## I5-2 ★★（10分）
**学習目標**：SAA の収束。
SAA でシナリオ数を 20→10,000 と増やすと容量問題の $\hat q$ はどう動くか（真値120.03へ）。なぜ収束するのか。

## I5-3 ★★（8分）
**学習目標**：CI を添える。
モンテカルロ結果に CI を必ず添えるべき理由を、点推定だけ報告する危険とともに述べよ。

## I5-4 ★★（12分）
**学習目標**：手を動かす（収束の体感）。
`apps/monte_carlo_visualizer`（または自作スクリプト）で、(a) $E[X]$ の収束と CI、(b) 希少事象の不安定さ、(c) SAA の $\hat q$ 収束を観察し、それぞれ1文で気づきを書け。
