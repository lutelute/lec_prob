---
title: "演習（発展）— Module 3 期待値・分散・相関"
module: 3
level: advanced
prerequisites: ["notes/03_expectation_variance_covariance.md"]
estimated_time: 40–55 分
solutions: "../solutions/03_expectation_variance_covariance_solutions.md"
---

# 演習（発展）★★★ — Module 3

> 学習目標：VaR と CVaR の使い分け、リスク尺度の選択を意思決定として論じる。

## A3-1 ★★★（20分）
**学習目標**：VaR vs CVaR。
VaR と CVaR の違いを「境界 vs 平均」「凸性」「最適化のしやすさ」の3点で説明し、なぜ Module 6 で CVaR が好まれるか論ぜよ。

## A3-2 ★★★（20分）
**学習目標**：分散と CVaR の順位逆転。
平均コストが等しい2案で、片方は分散が小さいが稀に巨大損失（重い裾）、もう片方は分散が大きいが損失に上限（有界）とする。分散と CVaR で順位が食い違いうることを説明し、どちらの指標で意思決定すべきか、状況設定（損失の非対称性・回復可能性）とともに論ぜよ。

## A3-3 ★★★（15分）
**学習目標**：相関と予備力。
正味負荷 $L=D-P$ の標準偏差が大きいほど、必要な予備力（リザーブ）が増えると考えられる。需要とPVの相関 $\rho_{DP}$ が予備力量に与える影響を、$\mathrm{Var}(L)$ の式と Module 6 のチャンス制約（$P(\text{不足})\le\varepsilon$）を結びつけて定性的に論ぜよ。
