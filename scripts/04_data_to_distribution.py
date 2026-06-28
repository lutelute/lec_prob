"""
04_data_to_distribution.py — Module 4「観測データ ≠ 真の分布」

実行:
    python3 scripts/04_data_to_distribution.py
出力:
    figures/04_data_to_distribution.svg
前提:
    data/daily_peak_demand.csv（無ければ gen_sample_data.py を先に実行）

4枚組:
  (a) 時系列（季節性=非定常）
  (b) ヒストグラム + 正規当てはめ + KDE（混在で当てはまり不良）
  (c) ECDF vs 当てはめ正規CDF（Glivenko-Cantelli の素直な推定）
  (d) 夏 vs 冬 のヒストグラム（1分布で扱う危うさ）
"""
from __future__ import annotations

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from scipy import stats  # noqa: E402
from _style import setup_japanese_font  # noqa: E402

setup_japanese_font()

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE, "figures")
DATA = os.path.join(BASE, "data", "daily_peak_demand.csv")


def load():
    arr = np.genfromtxt(DATA, delimiter=",", names=True)
    return arr["day_index"].astype(int), arr["demand_mw10k"]


def main() -> None:
    t_idx, x = load()
    t = t_idx % 365
    n = len(x)
    mu, sd = stats.norm.fit(x)

    fig, ax = plt.subplots(2, 2, figsize=(11.5, 8))

    # (a) 時系列
    ax[0, 0].plot(t_idx, x, lw=0.7, color="#4285f4")
    ax[0, 0].set_title("(a) 時系列：季節でうねる（非定常）")
    ax[0, 0].set_xlabel("日 index"); ax[0, 0].set_ylabel("需要 [万kW]")
    ax[0, 0].grid(alpha=0.3)

    # (b) ヒストグラム + 正規 + KDE
    ax[0, 1].hist(x, bins=30, density=True, color="#cfe2ff", edgecolor="white", label="ヒストグラム")
    xs = np.linspace(x.min(), x.max(), 300)
    ax[0, 1].plot(xs, stats.norm(mu, sd).pdf(xs), "r-", lw=2, label=f"正規当てはめ N({mu:.0f},{sd:.0f}²)")
    kde = stats.gaussian_kde(x)
    ax[0, 1].plot(xs, kde(xs), color="#34a853", lw=2, ls="--", label="KDE")
    ax[0, 1].set_title("(b) 当てはめ：正規は形が合わない")
    ax[0, 1].set_xlabel("需要 [万kW]"); ax[0, 1].set_ylabel("密度")
    ax[0, 1].legend(fontsize=8)

    # (c) ECDF vs 正規CDF
    xsort = np.sort(x); ecdf = np.arange(1, n + 1) / n
    ax[1, 0].step(xsort, ecdf, where="post", color="#4285f4", lw=2, label="ECDF（データ）")
    ax[1, 0].plot(xs, stats.norm(mu, sd).cdf(xs), "r-", lw=2, label="当てはめ正規CDF")
    ax[1, 0].set_title("(c) ECDF vs 正規CDF：ずれ＝当てはめ不良")
    ax[1, 0].set_xlabel("需要 [万kW]"); ax[1, 0].set_ylabel("累積確率")
    ax[1, 0].legend(fontsize=8); ax[1, 0].grid(alpha=0.3)

    # (d) 夏 vs 冬
    summer = x[(t >= 152) & (t <= 243)]
    winter = x[(t <= 59) | (t >= 335)]
    bins = np.linspace(x.min(), x.max(), 25)
    ax[1, 1].hist(summer, bins=bins, density=True, alpha=0.6, color="#fbbc04", label=f"夏 (μ={summer.mean():.0f})")
    ax[1, 1].hist(winter, bins=bins, density=True, alpha=0.6, color="#4285f4", label=f"冬 (μ={winter.mean():.0f})")
    ax[1, 1].set_title("(d) 夏 vs 冬：別分布（層別が必要）")
    ax[1, 1].set_xlabel("需要 [万kW]"); ax[1, 1].set_ylabel("密度")
    ax[1, 1].legend(fontsize=8)

    fig.suptitle("観測データ ≠ 真の分布：季節を混ぜた1分布は当てはまらない", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    os.makedirs(FIG_DIR, exist_ok=True)
    out = os.path.join(FIG_DIR, "04_data_to_distribution.svg")
    fig.savefig(out)
    print(f"[saved] {out}")

    ks = stats.kstest(x, "norm", args=(mu, sd))
    print(f"fit N({mu:.2f},{sd:.2f}), KS stat={ks.statistic:.4f}, p={ks.pvalue:.4g}")
    print(f"SE(mean) = {sd/np.sqrt(n):.3f}; 夏μ={summer.mean():.1f} 冬μ={winter.mean():.1f}")


if __name__ == "__main__":
    main()
