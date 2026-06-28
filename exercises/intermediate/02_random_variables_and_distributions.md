---
title: "演習（中級）— Module 2 確率変数と分布"
module: 2
level: intermediate
prerequisites: ["notes/02_random_variables_and_distributions.md"]
estimated_time: 30–40 分
solutions: "../solutions/02_random_variables_and_distributions_solutions.md"
---

# 演習（中級）★★ — Module 2

> 学習目標：正規の裾の確率を計算・解釈し、「密度は確率でない」を数値で示す。

## I2-1 ★★（10分）
**学習目標**：正規の裾＝超過確率。
$X\sim\mathcal{N}(100,15^2)$ で $P(X>130)$ と $P(X\le85)$ を求め、それぞれを電力的に解釈せよ（容量超過／過剰設備）。

## I2-2 ★★（10分）
**学習目標**：密度 > 1。
$\mathcal{N}(0,0.2^2)$ の $x=0$ の密度 $f(0)$ を計算し、1を超えることを示せ。これを根拠に「密度は確率でない」を説明せよ。

## I2-3 ★★（10分）
**学習目標**：指数の記憶なし性とその限界。
指数分布の記憶なし性 $P(X>s+t\mid X>s)=P(X>t)$ を CDF を使って示し、なぜ**摩耗故障**には不適かを述べよ。

## I2-4 ★★（10分）
**学習目標**：分布選択（現象との対応）。
次の各量に最も適切な分布を選び、理由を1文で：(a) 3台中の故障台数、(b) 年間故障件数、(c) 故障間隔、(d) 多数要因の和としての予測誤差。
選択肢：二項／ポアソン／指数／正規。
