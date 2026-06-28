"""
02_pdf_cdf_interval.py — 「確率＝面積＝CDFの差」を示す静的図

実行:
    python3 scripts/02_pdf_cdf_interval.py
出力:
    figures/02_pdf_cdf_interval.svg

左：PDF の下の面積として P(a≤X≤b)。
右：同じ確率が CDF の縦の差 F(b)-F(a) として現れる。
インタラクティブ版は apps/pdf_cdf_visualizer/。
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

C_PDF, C_AREA, C_CDF = "#4285f4", "#34a853", "#ea4335"


def main() -> None:
    mu, sigma = 100.0, 15.0
    dist = stats.norm(mu, sigma)
    a, b = 85.0, 115.0  # ≈ μ±1σ
    prob = float(dist.cdf(b) - dist.cdf(a))
    print(f"N({mu},{sigma}^2): P({a}≤X≤{b}) = {prob:.4f}（≈0.68, μ±1σ）")

    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 600)
    pdf, cdf = dist.pdf(x), dist.cdf(x)

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.3))

    # 左：PDF と面積
    axL.plot(x, pdf, color=C_PDF, lw=2.5)
    mask = (x >= a) & (x <= b)
    axL.fill_between(x[mask], pdf[mask], color=C_AREA, alpha=0.35)
    # 点の高さ（密度≠確率）
    f0 = float(dist.pdf(mu))
    axL.vlines(mu, 0, f0, color="#f9ab00", ls=":", lw=1.5)
    axL.annotate(f"密度の高さ f(100)={f0:.4f}\n（確率ではない）", xy=(mu, f0),
                 xytext=(mu + 8, f0 * 0.95), color="#f9ab00", fontsize=9,
                 arrowprops=dict(arrowstyle="->", color="#f9ab00"))
    axL.text(mu, f0 * 0.25, f"面積 = $P({a:.0f}\\leq X\\leq {b:.0f})$\n= {prob:.3f}",
             ha="center", color="#1e7e34", fontsize=10)
    axL.set_title("PDF：確率は『面積』")
    axL.set_xlabel("x（需要 [万kW] と読める）")
    axL.set_ylabel("確率密度 f(x)")
    axL.grid(alpha=0.3)

    # 右：CDF と縦の差
    axR.plot(x, cdf, color=C_CDF, lw=2.5)
    Fa, Fb = float(dist.cdf(a)), float(dist.cdf(b))
    for xv, Fv, name in [(a, Fa, "F(a)"), (b, Fb, "F(b)")]:
        axR.plot([x[0], xv], [Fv, Fv], color="gray", ls=":", lw=1)
        axR.plot([xv, xv], [0, Fv], color="gray", ls=":", lw=1)
        axR.scatter([xv], [Fv], color=C_CDF, zorder=5)
        axR.annotate(f"{name}={Fv:.3f}", xy=(xv, Fv), xytext=(xv + 1, Fv - 0.08), fontsize=9)
    axR.annotate("", xy=(x[0] + 3, Fb), xytext=(x[0] + 3, Fa),
                 arrowprops=dict(arrowstyle="<->", color=C_AREA, lw=2))
    axR.text(x[0] + 4, (Fa + Fb) / 2, f"差 = F(b)-F(a)\n= {prob:.3f}",
             color="#1e7e34", fontsize=10, va="center")
    axR.set_ylim(-0.03, 1.03)
    axR.set_title("CDF：同じ確率は『縦の差』")
    axR.set_xlabel("x")
    axR.set_ylabel("累積確率 F(x)")
    axR.grid(alpha=0.3)

    fig.suptitle("確率 = PDF の面積 = CDF の差（数値は一致する）", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    os.makedirs(FIG_DIR, exist_ok=True)
    out = os.path.join(FIG_DIR, "02_pdf_cdf_interval.svg")
    fig.savefig(out)
    print(f"[saved] {out}")


if __name__ == "__main__":
    main()
