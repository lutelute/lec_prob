#!/usr/bin/env python3
"""ケーススタディの図：日次ピーク需要のヒストグラム＋正規当てはめ＋6形式の最適容量 q*。
出力: figures/07_demand_hist.svg
実行: python scripts/fig_case_study.py
"""
import csv
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _style import setup_japanese_font

import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    setup_japanese_font()
    xs = []
    with open(os.path.join(HERE, "data", "daily_peak_demand.csv")) as f:
        for row in csv.DictReader(f):
            xs.append(float(row["demand_mw10k"]))
    d = np.array(xs)
    mu, sd = d.mean(), d.std(ddof=1)
    N = stats.norm(mu, sd)
    cs, co = 10.0, 1.0
    crit = cs / (cs + co)
    r = crit
    qs = {
        "①決定論 98.8": (mu, "#9aa0a6"),
        "②期待最小 116": (N.ppf(crit), "#4285f4"),
        "④チャンス制約 120": (N.ppf(0.95), "#34a853"),
        "③ロバスト 125": (mu + 2 * sd, "#ea4335"),
        "⑤CVaR 132": (N.ppf(1 - 0.05 * co / cs), "#f9ab00"),
    }

    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    ax.hist(d, bins=28, density=True, color="#cfe0ff", edgecolor="#7aa0e6",
            linewidth=0.6, label="実データ（730日）")
    grid = np.linspace(d.min() - 5, d.max() + 18, 400)
    ax.plot(grid, N.pdf(grid), color="#1a3a8f", lw=2.2,
            label=f"正規当てはめ N({mu:.0f},{sd:.0f}²)")
    ymax = N.pdf(mu) * 1.15
    for label, (q, c) in qs.items():
        ax.axvline(q, color=c, lw=2, ls="--")
        ax.text(q, ymax * (0.72 + 0.05 * (hash(label) % 5)), label, rotation=90,
                va="top", ha="right", fontsize=8.5, color=c)
    ax.set_xlabel("日次ピーク需要 / 確保容量")
    ax.set_ylabel("確率密度")
    ax.set_title("実データから決定へ：需要分布の上に並ぶ6形式の最適容量 q*")
    ax.set_ylim(0, ymax)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    out = os.path.join(HERE, "figures", "07_demand_hist.svg")
    fig.savefig(out)
    print("saved", out)


if __name__ == "__main__":
    main()
