"""
05_monte_carlo.py — Module 5「モンテカルロ収束と希少事象」

実行:
    python3 scripts/05_monte_carlo.py
出力:
    figures/05_monte_carlo.svg

左：E[X] (X~N(100,15)) の逐次推定が真値100へ、±1.96σ/√N の帯とともに収束。
右：希少事象 P(X>145)=0.00135 の推定が小Nで不安定（0ヒット）→大Nで安定。
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

FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")


def main() -> None:
    rng = np.random.default_rng(42)
    mu, sd = 100.0, 15.0
    Nmax = 50000
    s = rng.normal(mu, sd, Nmax)

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    # 左：E[X] 逐次推定 + CI帯
    ns = np.arange(1, Nmax + 1)
    run = np.cumsum(s) / ns
    ci = 1.96 * sd / np.sqrt(ns)
    axL.plot(ns, run, color="#4285f4", lw=1, label="逐次推定 $\\hat\\theta_N$")
    axL.fill_between(ns, mu - ci, mu + ci, color="#4285f4", alpha=0.15, label="±1.96σ/√N")
    axL.axhline(mu, color="#ea4335", ls="--", lw=1.5, label="真値 100")
    axL.set_xscale("log")
    axL.set_xlabel("サンプル数 N（対数）"); axL.set_ylabel("E[X] の推定")
    axL.set_ylim(mu - 12, mu + 12)
    axL.set_title("(左) 平均は 1/√N で速く収束")
    axL.legend(fontsize=8); axL.grid(alpha=0.3)

    # 右：希少事象 P(X>145)
    c = 145.0
    ptrue = float(1 - stats.norm(mu, sd).cdf(c))
    Ns = [300, 1000, 3000, 10000, 30000, 100000, 300000, 1000000]
    ests = []
    for N in Ns:
        ss = rng.normal(mu, sd, N)
        ests.append((ss > c).mean())
    axR.plot(Ns, ests, "o-", color="#a142f4", label="MC推定")
    axR.axhline(ptrue, color="#ea4335", ls="--", lw=1.5, label=f"真値 {ptrue:.5f}")
    axR.set_xscale("log")
    axR.set_xlabel("サンプル数 N（対数）"); axR.set_ylabel("P(X>145) の推定")
    axR.set_title("(右) 希少事象は小Nで不安定（0ヒットも）")
    axR.legend(fontsize=8); axR.grid(alpha=0.3)
    axR.annotate("N小：0ヒット＝確率0と誤推定", xy=(Ns[0], ests[0]),
                 xytext=(Ns[0]*1.5, ptrue*1.8), fontsize=8, color="#a142f4",
                 arrowprops=dict(arrowstyle="->", color="#a142f4"))

    fig.suptitle("モンテカルロ：平均は速く、尾（希少事象）は遅い", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.95))

    os.makedirs(FIG_DIR, exist_ok=True)
    out = os.path.join(FIG_DIR, "05_monte_carlo.svg")
    fig.savefig(out)
    print(f"[saved] {out}")
    print("rare event true p =", round(ptrue, 6), " estimates:", [round(e, 6) for e in ests])


if __name__ == "__main__":
    main()
