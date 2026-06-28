"""
05_scenario_tree.py — Module 5「二段階シナリオ木」

実行:
    python3 scripts/05_scenario_tree.py
出力:
    figures/05_scenario_tree.svg

第1段の決定 x（今決める）→ 不確実性 ξ が3シナリオで分岐（確率 π）→
各シナリオで第2段のリコース決定 y。Module 6 の二段階確率計画の骨格。
"""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from _style import setup_japanese_font  # noqa: E402

setup_japanese_font()

FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")


def box(ax, x, y, text, color, w=0.16, h=0.12):
    p = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.01",
                       fc=color, ec="#333", lw=1.2, zorder=3)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=9, zorder=4)


def main() -> None:
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    # 第1段ノード
    box(ax, 0.12, 0.5, "第1段 決定 x\n(今決める)", "#cfe2ff", w=0.18, h=0.16)

    scen = [("ξ₁ 楽観 (π=0.25)", 0.82, "y₁ 調整", "#e6f4ea"),
            ("ξ₂ 基準 (π=0.50)", 0.5, "y₂ 調整", "#fef7e0"),
            ("ξ₃ 悲観 (π=0.25)", 0.18, "y₃ 調整", "#fce8e6")]

    for label, yy, ylab, col in scen:
        # 枝
        ax.plot([0.21, 0.46], [0.5, yy], color="#888", lw=1.5, zorder=1)
        box(ax, 0.56, yy, label, col, w=0.24, h=0.12)
        ax.plot([0.68, 0.80], [yy, yy], color="#888", lw=1.5, zorder=1)
        box(ax, 0.89, yy, ylab, "#eee", w=0.14, h=0.1)

    ax.text(0.12, 0.27, "ここで未来は不明", ha="center", fontsize=8, color="#555")
    ax.text(0.56, 0.04, "不確実性 ξ が判明（分岐）", ha="center", fontsize=9, color="#555")
    ax.text(0.89, 0.04, "判明後に調整", ha="center", fontsize=9, color="#555")

    ax.text(0.5, 0.96,
            "二段階確率計画：min  第1段費用(x) + E[ 第2段費用(x, ξ, y) ]",
            ha="center", fontsize=11)
    ax.text(0.5, 0.90,
            "第1段＝蓄電池容量/起動停止（事前）、第2段＝充放電/出力調整（リアルタイム）",
            ha="center", fontsize=8.5, color="#444")

    os.makedirs(FIG_DIR, exist_ok=True)
    out = os.path.join(FIG_DIR, "05_scenario_tree.svg")
    fig.savefig(out)
    print(f"[saved] {out}")


if __name__ == "__main__":
    main()
