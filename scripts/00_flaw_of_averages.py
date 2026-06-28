"""
00_flaw_of_averages.py — Module 0「平均で計画する2つの罠」の再現と作図

実行:
    python3 scripts/00_flaw_of_averages.py
出力:
    figures/00_flaw_of_averages.svg
    （標準出力に数値も表示）

題材: 容量 q を前もって確保。需要 D∈{80,120} 各0.5。
      不足は単価10、過剰は単価1（非対称）。
      → 平均で評価する罠・平均に向けて最適化する罠を示す。
"""
from __future__ import annotations

import os

import numpy as np

# matplotlib は GUI 無しで保存できるバックエンドに
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from _style import setup_japanese_font  # noqa: E402

setup_japanese_font()

FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")

# --- モデル定義 ---
D_VALS = np.array([80.0, 120.0])
D_PROB = np.array([0.5, 0.5])
C_SHORT, C_OVER = 10.0, 1.0


def cost(q, D):
    return C_SHORT * np.maximum(D - q, 0) + C_OVER * np.maximum(q - D, 0)


def expected_cost(q):
    return float(np.sum(D_PROB * cost(q, D_VALS)))


def main() -> None:
    mean_D = float(np.sum(D_PROB * D_VALS))
    print(f"平均需要 E[D] = {mean_D}")
    print(f"罠1  Cost(100, E[D]) = {cost(100, mean_D):.1f}   ← 平均を代入したコスト（幻）")
    print(f"罠1  E[Cost(100, D)] = {expected_cost(100):.1f}   ← 実際の期待コスト")

    qs = np.arange(80, 141)
    ec = np.array([expected_cost(q) for q in qs])
    q_star = int(qs[np.argmin(ec)])
    print(f"罠2  最適 q* = {q_star}   期待コスト = {expected_cost(q_star):.1f}")
    print(f"     平均向け q=100 の期待コスト = {expected_cost(100):.1f}（{expected_cost(100)/expected_cost(q_star):.1f}倍悪い）")

    # --- 作図 ---
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(qs, ec, color="#4285f4", lw=2.5, label=r"期待コスト $E[\mathrm{Cost}(q,D)]$")

    # q=100（平均で計画）と q*=120（最適）を強調
    ax.scatter([100], [expected_cost(100)], color="#ea4335", zorder=5, s=70)
    ax.annotate(f"平均で計画 q=100\n期待コスト {expected_cost(100):.0f}",
                xy=(100, expected_cost(100)), xytext=(101, expected_cost(100) + 18),
                color="#ea4335", fontsize=10,
                arrowprops=dict(arrowstyle="->", color="#ea4335"))
    ax.scatter([q_star], [expected_cost(q_star)], color="#34a853", zorder=5, s=70)
    ax.annotate(f"最適 q*={q_star}\n期待コスト {expected_cost(q_star):.0f}",
                xy=(q_star, expected_cost(q_star)), xytext=(q_star - 26, expected_cost(q_star) + 30),
                color="#34a853", fontsize=10,
                arrowprops=dict(arrowstyle="->", color="#34a853"))

    # 「平均を代入したコスト=0」の幻ライン
    ax.axhline(0, color="gray", ls=":", lw=1)
    ax.text(82, 4, "Cost(100, E[D])=0 は幻（実際は110）", color="gray", fontsize=9)

    ax.set_xlabel("確保容量 q [万kW]")
    ax.set_ylabel("期待コスト")
    ax.set_title("平均で計画する2つの罠（非対称コスト：不足10 / 過剰1）")
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()

    os.makedirs(FIG_DIR, exist_ok=True)
    out = os.path.join(FIG_DIR, "00_flaw_of_averages.svg")
    fig.savefig(out)
    print(f"[saved] {out}")


if __name__ == "__main__":
    main()
