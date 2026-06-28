"""
01_bayes_base_rate.py — Module 1「保護リレーの誤報（基準率の効果）」の作図

実行:
    python3 scripts/01_bayes_base_rate.py
出力:
    figures/01_bayes_base_rate.svg

左：1000件あたりの内訳（真陽性 vs 偽陽性）→ 警報の多くが偽陽性。
右：事後確率 P(故障|警報) が基準率 P(F) に強く依存する様子。
"""
from __future__ import annotations

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from _style import setup_japanese_font  # noqa: E402

setup_japanese_font()

FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")


def posterior(pf, sens=0.99, fpr=0.05):
    """P(F|警報) = sens*pf / (sens*pf + fpr*(1-pf))"""
    return sens * pf / (sens * pf + fpr * (1 - pf))


def main() -> None:
    sens, fpr = 0.99, 0.05
    pf = 0.01
    p_post = posterior(pf, sens, fpr)
    print(f"基準率 P(F)={pf}, 感度={sens}, 誤警報率={fpr}")
    print(f"P(故障|警報) = {p_post:.4f}")

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.3))

    # 左：1000件の内訳
    n = 1000
    n_fault = n * pf
    tp = n_fault * sens              # 真陽性
    fn = n_fault * (1 - sens)        # 偽陰性
    fp = n * (1 - pf) * fpr          # 偽陽性
    tn = n * (1 - pf) * (1 - fpr)    # 真陰性
    cats = ["真陽性\n(故障&警報)", "偽陽性\n(正常&警報)", "偽陰性\n(故障&無警報)", "真陰性\n(正常&無警報)"]
    vals = [tp, fp, fn, tn]
    colors = ["#34a853", "#ea4335", "#fbbc04", "#cccccc"]
    bars = axL.bar(cats, vals, color=colors)
    for bar, v in zip(bars, vals):
        axL.text(bar.get_x() + bar.get_width() / 2, v + 8, f"{v:.1f}", ha="center", fontsize=9)
    axL.set_ylabel("件数 / 1000件")
    axL.set_title(f"警報が鳴った {tp+fp:.1f} 件のうち\n本物は {tp:.1f} 件 → P(故障|警報)={p_post:.1%}")
    axL.tick_params(axis="x", labelsize=8)

    # 右：事後確率 vs 基準率
    pfs = np.linspace(0.001, 0.3, 300)
    axR.plot(pfs, posterior(pfs, sens, fpr), color="#4285f4", lw=2.5)
    axR.scatter([pf], [p_post], color="#ea4335", zorder=5, s=60)
    axR.annotate(f"P(F)={pf}→{p_post:.1%}", xy=(pf, p_post),
                 xytext=(pf + 0.04, p_post - 0.05), color="#ea4335", fontsize=9,
                 arrowprops=dict(arrowstyle="->", color="#ea4335"))
    axR.set_xlabel("基準率 P(F)（故障の起こりやすさ）")
    axR.set_ylabel("事後確率 P(故障|警報)")
    axR.set_title("事後確率は基準率に強く依存する")
    axR.grid(alpha=0.3)
    axR.set_ylim(0, 1)

    fig.suptitle("基準率の誤謬：感度99%でも、低い基準率だと警報の多くは偽陽性", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.95))

    os.makedirs(FIG_DIR, exist_ok=True)
    out = os.path.join(FIG_DIR, "01_bayes_base_rate.svg")
    fig.savefig(out)
    print(f"[saved] {out}")


if __name__ == "__main__":
    main()
