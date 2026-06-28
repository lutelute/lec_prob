"""
06_optimization_comparison.py — Module 6「同じ問題、6形式、違う決定」

実行:
    python3 scripts/06_optimization_comparison.py
出力:
    figures/06_optimization_comparison.svg

容量調達問題を6形式で解き、最適決定 x* を需要分布上に重ねて比較する。
数理は apps/stochastic_optimization_comparator/core.py を再利用（単一の真実源）。
"""
from __future__ import annotations

import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from _style import setup_japanese_font  # noqa: E402

setup_japanese_font()

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE, "figures")
sys.path.insert(0, os.path.join(BASE, "apps", "stochastic_optimization_comparator"))
import core  # noqa: E402

COLORS = {
    "①決定論": "#9aa0a6", "②期待値最小化": "#4285f4", "④チャンス制約": "#34a853",
    "⑥分布ロバスト": "#a142f4", "⑤CVaR最小化": "#f9ab00", "③ロバスト": "#ea4335",
}
ORDER = ["①決定論", "④チャンス制約", "②期待値最小化", "⑥分布ロバスト", "⑤CVaR最小化", "③ロバスト"]


def main() -> None:
    mean, std = 100.0, 15.0
    res = {r.name: r for r in core.solve_all(mean=mean, std=std, cs=10, co=1,
                                             eps=0.1, alpha=0.9, k_robust=3.0)}
    dist = core.make_dist(mean, std)

    fig, (axT, axB) = plt.subplots(2, 1, figsize=(10, 6.5),
                                   gridspec_kw={"height_ratios": [3, 2]})

    # 上：需要分布 + x* 縦線
    xs = np.linspace(dist.ppf(0.001), dist.ppf(0.999), 500)
    axT.plot(xs, dist.pdf(xs), color="#999", lw=2)
    axT.fill_between(xs, dist.pdf(xs), color="#999", alpha=0.12)
    ymax = float(dist.pdf(xs).max())
    for i, name in enumerate(ORDER):
        r = res[name]
        axT.axvline(r.x, color=COLORS[name], lw=2.2)
        axT.text(r.x, ymax * (1.02 + 0.08 * (i % 3)), f"{name}\n{r.x:.0f}",
                 color=COLORS[name], fontsize=8, ha="center")
    axT.set_title("同じ問題・6形式：最適容量 x* を需要分布上に重ねる（c_s=10, c_o=1）")
    axT.set_xlabel("容量 x / 需要 ξ"); axT.set_ylabel("密度")
    axT.set_ylim(0, ymax * 1.45)

    # 下：x* 棒（保守性順）＋ 期待費用注記
    names = ORDER
    xstar = [res[n].x for n in names]
    axB.barh(range(len(names)), xstar, color=[COLORS[n] for n in names])
    for i, n in enumerate(names):
        axB.text(res[n].x + 0.5, i, f"x*={res[n].x:.1f}, E[C]={res[n].expected_cost:.1f}, "
                 f"P(不足)={res[n].shortage_prob:.2f}", va="center", fontsize=8)
    axB.set_yticks(range(len(names))); axB.set_yticklabels(names, fontsize=9)
    axB.set_xlabel("最適決定 x*")
    axB.set_xlim(90, 175)
    axB.set_title("← 平均重視・楽観・安   |   尾部/最悪重視・保守・高 →")
    axB.invert_yaxis()

    fig.suptitle("形式の選択が決定を支配する（x*：100〜137）", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    os.makedirs(FIG_DIR, exist_ok=True)
    out = os.path.join(FIG_DIR, "06_optimization_comparison.svg")
    fig.savefig(out)
    print(f"[saved] {out}")
    for n in names:
        r = res[n]
        print(f"  {n:14s} x*={r.x:7.2f}  E[C]={r.expected_cost:7.2f}  "
              f"P(不足)={r.shortage_prob:.3f}  CVaR={r.cvar:6.2f}")


if __name__ == "__main__":
    main()
