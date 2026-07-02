---
title: "演習（初級）— 第2章 確率変数と分布"
module: 2
level: basic
prerequisites: ["notes/02_random_variables_and_distributions.md"]
estimated_time: 20–30 分
solutions: "../solutions/02_random_variables_and_distributions_solutions.md"
---

# 演習（初級）★ — 第2章

> 学習目標：質量と密度の区別、CDF の読み、点確率0を**用語として**使えるようにする。

## B2-1 ★（5分）
**学習目標**：質量 vs 密度。
「確率質量 $p_X(x)$」と「確率密度 $f_X(x)$」の違いを、「足して1」「積分して1」を使って1文ずつで説明せよ。

## B2-2 ★（5分）
**学習目標**：離散の区間確率（和）。
$X\sim\mathrm{Bin}(3,0.05)$（独立3台、各故障率0.05）で $P(X\ge1)$ を求めよ。

## B2-3 ★（5分）
**学習目標**：連続の点確率。
連続変数で $P(X=x)=0$ なのに分布が意味を持つのはなぜか。確率は何（点／区間）で測るか。

## B2-4 ★（10分）
**学習目標**：CDF の読み・PDFとの関係。
ある連続変数の CDF が $F(80)=0.16,\ F(110)=0.78$ である。
1. $P(80\le X\le110)$ を求めよ。
2. $P(X>110)$ を求めよ。
3. 「PDF を積分すると CDF、CDF を微分すると PDF」を1文で説明せよ。
