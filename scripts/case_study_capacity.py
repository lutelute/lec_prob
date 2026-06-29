#!/usr/bin/env python3
"""ケーススタディ：実データ（日次ピーク需要）→ 分布推定 → 6形式の容量決定。
notes/07_case_study.md の数値はすべてこのスクリプトの出力（再現可能）。
実行: python scripts/case_study_capacity.py
"""
import csv
import math
import os

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_demand():
    xs = []
    with open(os.path.join(HERE, "data", "daily_peak_demand.csv")) as f:
        for row in csv.DictReader(f):
            xs.append(float(row["demand_mw10k"]))
    return np.array(xs)


def main():
    d = load_demand()
    n = len(d)
    mu, sd = d.mean(), d.std(ddof=1)
    # 正規当てはめの妥当性（簡易）：歪度・尖度・分位点の一致
    sk, ku = stats.skew(d), stats.kurtosis(d)
    print(f"# データ: {n}日, 平均 mu={mu:.2f}, 標準偏差 sd={sd:.2f}")
    print(f"# 歪度={sk:.3f}, 尖度(超過)={ku:.3f}  (0に近いほど正規的)")

    N = stats.norm(mu, sd)
    # コスト（不足は余剰よりずっと痛い）
    cs, co = 10.0, 1.0
    crit = cs / (cs + co)
    print(f"# コスト: 不足cs={cs}, 余剰co={co} -> 臨界比 cs/(cs+co)={crit:.3f}")

    # 6形式の容量決定 q*
    eps = 0.05          # チャンス制約: 供給不足を5%以下に
    alpha = 0.95        # CVaR 信頼水準
    k = 2.0             # ロバスト: mu ± k*sd の箱
    forms = {}
    forms["①決定論(平均)"] = mu
    forms["②期待コスト最小"] = N.ppf(crit)                      # newsvendor
    forms["③ロバスト(箱±kσ)"] = mu + k * sd                    # 最悪需要に備える
    forms["④チャンス制約(ε=5%)"] = N.ppf(1 - eps)
    # ⑤ CVaR 最小化（newsvendor の CVaR は不足側テールの条件付き期待を抑える分位点）
    # 不足コスト主体の問題では、CVaR_alpha 最適は概ね (1 - (1-alpha)*co/cs) 分位点に対応する保守化。
    q_cvar = N.ppf(1 - (1 - alpha) * co / cs)
    forms["⑤CVaR最小(α=95%)"] = q_cvar
    # ⑥ 分布ロバスト（平均と分散のみ既知 = Scarf の安全在庫）
    # q = mu + sd * ( sqrt(crit/(1-crit)) - sqrt((1-crit)/crit) ) / 2 ... Scarf newsvendor
    r = crit
    scarf_safety = 0.5 * (math.sqrt(r / (1 - r)) - math.sqrt((1 - r) / r))
    forms["⑥分布ロバスト(Scarf)"] = mu + sd * scarf_safety

    print("\n# 6形式の最適容量 q* と 供給不足の確率 P(D>q*):")
    for name, q in sorted(forms.items(), key=lambda kv: kv[1]):
        pshort = 1 - N.cdf(q)
        print(f"  {name:22s} q*={q:7.2f}   不足確率={pshort*100:5.1f}%")

    # 平均で決めた場合の損失 vs 期待最小の損失（罠の数値化）
    def exp_loss(q):
        m = mu - q
        eshort = m * N.cdf(m / sd) + sd * stats.norm.pdf(m / sd)  # E[(D-q)+]
        eexcess = eshort + (q - mu)
        return cs * eshort + co * eexcess

    q_det, q_opt = mu, N.ppf(crit)
    print(f"\n# 平均で決める q={q_det:.1f}: 期待損失={exp_loss(q_det):.2f}")
    print(f"# 期待最小  q={q_opt:.1f}: 期待損失={exp_loss(q_opt):.2f}")
    print(f"# 平均で決める無駄 = {exp_loss(q_det) - exp_loss(q_opt):.2f} "
          f"({(exp_loss(q_det)/exp_loss(q_opt)-1)*100:.0f}% 余計)")


if __name__ == "__main__":
    main()
