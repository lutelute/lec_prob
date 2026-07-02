# シナリオ木ビジュアライザ（図ベース＋拡張予定）

第5章–6 の**二段階シナリオ木**（第1段の決定 → 不確実性の分岐 → 第2段のリコース）を扱います。

現状は**再生成可能な静的図**で提供しています：

- 図：[`figures/05_scenario_tree.svg`](../../figures/05_scenario_tree.svg)
- 生成：`python3 scripts/05_scenario_tree.py`

```
第1段 決定 x ┬─ ξ1 (π1) ─ 第2段 y1
 (今決める)  ├─ ξ2 (π2) ─ 第2段 y2     min  第1段費用 + E[第2段費用]
             └─ ξ3 (π3) ─ 第2段 y3
```

## 概念の対応
- 第1段＝事前に決める（蓄電池容量・起動停止・予約予備力）。
- 分岐＝不確実性 ξ（需要・PV・価格）が判明。
- 第2段＝リコース（充放電・出力再配分・緊急融通）。
- 期待値・確率・CVaR はシナリオ上の**重み付き和**で書ける（第5章 §2）。

## インタラクティブ版との関係
シナリオ確率を動かして期待値・決定がどう変わるかは、
**確率的最適化コンパレータ**（[`apps/stochastic_optimization_comparator`](../stochastic_optimization_comparator/README.md)）で
シナリオ数 N を変えながら体感できます（同一問題を6形式で比較）。

## 拡張予定（SPEC）
- 確率付きシナリオを編集 → 期待値/CVaR/二段階の解が更新されるインタラクティブ木。
- シナリオ削減（Wasserstein/クラスタリング）の前後比較。

関連ノート：[`notes/05_scenarios_and_monte_carlo.md`](../../notes/05_scenarios_and_monte_carlo.md) §6、
[`notes/06_optimization_under_uncertainty.md`](../../notes/06_optimization_under_uncertainty.md) §3。
