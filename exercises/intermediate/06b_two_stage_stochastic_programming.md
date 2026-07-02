---
title: "演習（中級）— 第6b章 二段階確率計画（VSS・EVPI）"
module: 6.5
level: intermediate
prerequisites: ["notes/06b_two_stage_stochastic_programming.md"]
estimated_time: 35–50 分
solutions: "../solutions/06b_two_stage_solutions.md"
---

# 演習（中級）★★ — 第6b章

> 学習目標：VSS が変わる条件、non-anticipativity、リスク中立 vs リスク回避を説明する。

## I6b-1 ★★（12分）
**学習目標**：飽和と VSS の拡大。
§4 の2点問題で実時間価格 $c_2$ を 20→40 に上げると、確率的解 $x^\*$ と VSS はどう変わるか。離散シナリオで $x^\*$ が**飽和**する一方 VSS が拡大する理由を述べよ（Python で確認可）。

## I6b-2 ★★（10分）
**学習目標**：VSS が小さい状況。
「VSS が小さい問題では確率的最適化を導入する意味が薄い」とはどういう状況か。分散・非対称性の観点で説明せよ。

## I6b-3 ★★（10分）
**学習目標**：non-anticipativity。
第1段 $x$ を全シナリオ共通にする制約（non-anticipativity）を外すと何が起きるか。それが WS（wait-and-see）に対応する理由を述べよ。

## I6b-4 ★★（13分）
**学習目標**：リスク中立 vs リスク回避の読み取り。
§8.2 の表（中立 $x^\*$=130, E=658, 最悪1650 ／ 回避 $x^\*$=180, E=843, 最悪900）について：
1. リスク回避が払った「保険料」（平均の悪化）と「得た保障」（最悪の改善）をそれぞれ数値で答えよ。
2. CVaR の信頼水準 $\alpha$ を 0.9→0.99 に上げると $x^\*$ はどちらへ動くと予想されるか。理由とともに。
