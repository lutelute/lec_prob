---
title: "演習（中級）— 第6章 不確実性下の最適化"
module: 6
level: intermediate
prerequisites: ["notes/06_optimization_under_uncertainty.md"]
estimated_time: 35–50 分
solutions: "../solutions/06_optimization_under_uncertainty_solutions.md"
---

# 演習（中級）★★ — 第6章

> 学習目標：形式どうしの違い（集合 vs 確率、違反確率 vs 深さ、ロバスト vs DRO）を説明する。

## I6-1 ★★（12分）
**学習目標**：ロバスト vs チャンス制約。
ロバスト最適化とチャンス制約の違いを、「集合の最悪 vs 確率 $1-\varepsilon$」「分布の要否」で説明せよ。本例の $x^\*$（137 vs 119）に触れよ。

## I6-2 ★★（12分）
**学習目標**：チャンス制約 vs CVaR。
チャンス制約と CVaR の違いを、「違反確率 vs 違反の深さ」「凸性」で述べ、なぜ CVaR が解きやすいか説明せよ。

## I6-3 ★★（10分）
**学習目標**：ロバスト vs 分布ロバスト。
ロバストと分布ロバストの違いを、本例の $x^\*$（137 vs 121）とともに説明せよ。「確率を使わない／部分的に使う」の観点で。

## I6-4 ★★（12分）
**学習目標**：パラメータと保守性。
`apps/stochastic_optimization_comparator` で、(a) ロバスト幅 $k$ を 1→4、(b) CVaR の $\alpha$ を 0.5→0.99、(c) チャンスの $\varepsilon$ を 0.3→0.01 と動かし、各 $x^\*$ がどちらへ動くか観察し、保守性との関係を1文ずつで述べよ。
