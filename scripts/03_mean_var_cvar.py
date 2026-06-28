"""
03_mean_var_cvar.py — Module 3「平均は同じ、リスクが違う」

実行:
    python3 scripts/03_mean_var_cvar.py
出力:
    figures/03_mean_var_cvar.svg

同一平均(100)の2つのコスト分布 A:N(100,10^2), B:N(100,30^2) に対し、
平均・VaR_0.95・CVaR_0.95 を重ねて、要約量を変えると見えるリスクが変わることを示す。
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


def var_cvar(mu, sd, alpha=0.95):
    z = stats.norm.ppf(alpha)
    var = mu + z * sd
    cvar = mu + sd * stats.norm.pdf(z) / (1 - alpha)
    return var, cvar


def main() -> None:
    x = np.linspace(40, 220, 800)
    cases = [("A: N(100,10²)", 100, 10, "#4285f4"), ("B: N(100,30²)", 100, 30, "#ea4335")]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=False)
    for ax, (name, mu, sd, c) in zip(axes, cases):
        pdf = stats.norm(mu, sd).pdf(x)
        ax.plot(x, pdf, color=c, lw=2.5)
        var, cvar = var_cvar(mu, sd)
        # 尾部（CVaRが拾う領域）を塗る
        m = x >= var
        ax.fill_between(x[m], pdf[m], color=c, alpha=0.25)
        # 平均・VaR・CVaR の縦線
        ax.axvline(mu, color="gray", ls="--", lw=1.5)
        ax.axvline(var, color="#f9ab00", ls=":", lw=1.8)
        ax.axvline(cvar, color="#34a853", ls="-.", lw=1.8)
        ax.text(mu, ax.get_ylim()[1]*0.92, f"平均={mu}", color="gray", fontsize=8, ha="center")
        ax.text(var, ax.get_ylim()[1]*0.55, f"VaR={var:.0f}", color="#b8860b", fontsize=8, ha="left")
        ax.text(cvar, ax.get_ylim()[1]*0.35, f"CVaR={cvar:.0f}", color="#1e7e34", fontsize=8, ha="left")
        ax.set_title(name)
        ax.set_xlabel("コスト")
        ax.set_ylabel("確率密度")
        ax.grid(alpha=0.3)

    fig.suptitle("平均はどちらも100。だが VaR/CVaR（尾部）で大きく差がつく", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.95))

    os.makedirs(FIG_DIR, exist_ok=True)
    out = os.path.join(FIG_DIR, "03_mean_var_cvar.svg")
    fig.savefig(out)
    print(f"[saved] {out}")
    for name, mu, sd, _ in cases:
        v, cv = var_cvar(mu, sd)
        print(f"  {name}: 平均={mu} VaR.95={v:.1f} CVaR.95={cv:.1f}")


if __name__ == "__main__":
    main()
