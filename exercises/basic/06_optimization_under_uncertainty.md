---
title: "演習（初級）— Module 6 不確実性下の最適化"
module: 6
level: basic
prerequisites: ["notes/06_optimization_under_uncertainty.md", "apps/stochastic_optimization_comparator"]
estimated_time: 25–35 分
solutions: "../solutions/06_optimization_under_uncertainty_solutions.md"
---

# 演習（初級）★ — Module 6

> 学習目標：3形式の要約、非対称コストが決定を動かすこと、ε と決定の関係を使う。

## B6-1 ★（8分）
**学習目標**：3形式の要約。
決定論・期待値最小化・ロバストの3形式について、「何を不確実とし／何を最適化するか」を1文ずつで述べよ。

## B6-2 ★（7分）
**学習目標**：非対称コストと決定。
統一問題で $c_s=10,c_o=1$ のとき、期待値最小化の最適 $x^\*$ が平均100より大きい理由を述べよ（臨界比に言及）。

## B6-3 ★（5分）
**学習目標**：ε と決定。
チャンス制約 $P(\xi>x)\le\varepsilon$ で $\varepsilon$ を 0.1→0.05 と小さくすると $x^\*$ はどう動くか。理由を述べよ。

## B6-4 ★（10分）
**学習目標**：比較ツールで体感。
`apps/stochastic_optimization_comparator` を起動し、既定設定で6形式の $x^\*$ を読み取り、最も小さい形式と最も大きい形式を答えよ。$c_s$ を $c_o$ に近づけると $x^\*$ 群はどう変わるか観察せよ。
