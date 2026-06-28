"""
02b_pmf_vs_pdf.py — Module 2「離散PMF（棒＝確率）vs 連続PDF（面積＝確率）」

実行:
    python3 scripts/02b_pmf_vs_pdf.py
出力:
    figures/02b_pmf_vs_pdf.svg

左：離散 Bin(3,0.05)。棒の高さがそのまま確率（足して1）。
右：連続 N(100,15)。確率は曲線の下の面積（積分して1）。高さは密度＝確率ではない。
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
C_DISC, C_CONT, C_AREA = "#a142f4", "#4285f4", "#34a853"


def main() -> None:
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.3))

    # 左：離散 PMF（棒＝確率）
    B = stats.binom(3, 0.05)
    ks = np.arange(0, 4)
    pmf = B.pmf(ks)
    bars = axL.bar(ks, pmf, width=0.25, color=C_DISC, alpha=0.85)
    for k, p in zip(ks, pmf):
        axL.text(k, p + 0.015, f"{p:.4f}", ha="center", fontsize=9)
    # P(X>=2) を強調
    for k in [2, 3]:
        bars[k].set_color("#ea4335")
    axL.text(2.5, 0.35, "$P(X\\geq 2)$=和\n=0.0073", color="#ea4335", ha="center", fontsize=9)
    axL.set_title("離散 PMF：棒の高さ＝確率（足して1）")
    axL.set_xlabel("故障台数 k（3台中、各 p=0.05）")
    axL.set_ylabel("確率 p(k)")
    axL.set_xticks(ks)
    axL.set_ylim(0, 1.0)
    axL.grid(alpha=0.3, axis="y")

    # 右：連続 PDF（面積＝確率）
    N = stats.norm(100, 15)
    x = np.linspace(40, 160, 500)
    axR.plot(x, N.pdf(x), color=C_CONT, lw=2.5)
    a, b = 85, 115
    m = (x >= a) & (x <= b)
    axR.fill_between(x[m], N.pdf(x[m]), color=C_AREA, alpha=0.35)
    f100 = float(N.pdf(100))
    axR.vlines(100, 0, f100, color="#f9ab00", ls=":", lw=1.5)
    axR.annotate("高さ f(100)=密度\n（確率ではない）", xy=(100, f100),
                 xytext=(118, f100 * 0.92), color="#f9ab00", fontsize=9,
                 arrowprops=dict(arrowstyle="->", color="#f9ab00"))
    axR.text(100, f100 * 0.28, "面積 = $P(85\\leq X\\leq 115)$\n= 0.683",
             ha="center", color="#1e7e34", fontsize=9)
    axR.set_title("連続 PDF：面積＝確率（積分して1）")
    axR.set_xlabel("需要 x [万kW]  $N(100,15^2)$")
    axR.set_ylabel("確率密度 f(x)")
    axR.grid(alpha=0.3)

    fig.suptitle("離散は『質量（棒）』、連続は『密度（面積）』— どちらも全体は1", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.95))

    os.makedirs(FIG_DIR, exist_ok=True)
    out = os.path.join(FIG_DIR, "02b_pmf_vs_pdf.svg")
    fig.savefig(out)
    print(f"[saved] {out}")
    print("PMF check sum =", round(float(stats.binom(3, 0.05).pmf(range(4)).sum()), 6))
    print("P(85<=X<=115) =", round(float(stats.norm(100, 15).cdf(115) - stats.norm(100, 15).cdf(85)), 4))


if __name__ == "__main__":
    main()
