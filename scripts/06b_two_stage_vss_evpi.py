"""
06b_two_stage_vss_evpi.py — Module 6b「VSS・EVPI と二段階の決定」

実行:
    python3 scripts/06b_two_stage_vss_evpi.py
出力:
    figures/06b_two_stage_vss_evpi.svg

左：WS ≤ RP ≤ EEV と VSS/EVPI のギャップ。
右：シナリオ分布上に決定論 x_det と確率的 x_RP を重ねる。
"""
from __future__ import annotations

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import cvxpy as cp  # noqa: E402
from _style import setup_japanese_font  # noqa: E402

setup_japanese_font()

FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")

C1, C2, V, B = 5.0, 20.0, 4.0, 15.0
XI = np.array([70., 100., 140.]); PI = np.array([0.3, 0.4, 0.3])


def Q(x, d):
    return C2 * max(d - x, 0) + (-V) * min(max(x - d, 0), B)


def solve_rp():
    x = cp.Variable(nonneg=True)
    sh = cp.Variable(3, nonneg=True); su = cp.Variable(3, nonneg=True); st = cp.Variable(3, nonneg=True)
    cons = []
    for s in range(3):
        cons += [x + sh[s] - su[s] == XI[s], st[s] <= su[s], st[s] <= B]
    obj = C1 * x + PI @ (C2 * sh - V * st)
    cp.Problem(cp.Minimize(obj), cons).solve(solver=cp.CLARABEL)
    return float(obj.value), float(x.value)


def metrics():
    mean_xi = float(PI @ XI)
    RP, x_RP = solve_rp()
    xs = np.linspace(0, 200, 2001)
    x_det = float(xs[np.argmin([C1 * xx + Q(xx, mean_xi) for xx in xs])])
    EEV = C1 * x_det + sum(p * Q(x_det, d) for p, d in zip(PI, XI))
    WS = float(PI @ np.array([C1 * d for d in XI]))
    return dict(WS=WS, RP=RP, EEV=EEV, x_det=x_det, x_RP=x_RP,
                VSS=EEV - RP, EVPI=RP - WS, mean=mean_xi)


def main() -> None:
    m = metrics()
    print({k: round(v, 2) for k, v in m.items()})

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.5, 4.6))

    # 左：WS/RP/EEV の棒 + VSS/EVPI ブラケット
    names = ["WS\n完全予測", "RP\n確率的", "EEV\n決定論"]
    vals = [m["WS"], m["RP"], m["EEV"]]
    cols = ["#34a853", "#4285f4", "#ea4335"]
    axL.bar(names, vals, color=cols, width=0.6)
    for i, v in enumerate(vals):
        axL.text(i, v + 4, f"{v:.1f}", ha="center", fontsize=10)
    # VSS（RP→EEV）, EVPI（WS→RP）
    axL.annotate("", xy=(2, m["EEV"]), xytext=(1, m["EEV"]),
                 arrowprops=dict(arrowstyle="<->", color="#b8860b"))
    axL.text(1.5, m["EEV"] + 12, f"VSS={m['VSS']:.1f}", ha="center", color="#b8860b", fontsize=9)
    axL.annotate("", xy=(1, m["RP"]), xytext=(0, m["RP"]),
                 arrowprops=dict(arrowstyle="<->", color="#1e7e34"))
    axL.text(0.5, m["RP"] + 12, f"EVPI={m['EVPI']:.1f}", ha="center", color="#1e7e34", fontsize=9)
    axL.set_ylabel("期待コスト（小さいほど良い）")
    axL.set_title("$WS \\leq RP \\leq EEV$：確率的にする価値(VSS)と完全予測の価値(EVPI)")
    axL.set_ylim(0, m["EEV"] * 1.2)

    # 右：シナリオ分布 + 決定 x
    axR.bar(XI, PI, width=6, color="#bbb", label="シナリオ確率 π")
    axR.axvline(m["x_det"], color="#ea4335", lw=2.5, label=f"決定論 x_det={m['x_det']:.0f}")
    axR.axvline(m["x_RP"], color="#4285f4", lw=2.5, ls="--", label=f"確率的 x_RP={m['x_RP']:.0f}")
    axR.axvline(m["mean"], color="#999", lw=1, ls=":", label=f"平均 {m['mean']:.0f}")
    axR.set_xlabel("正味需要 ξ [単位]"); axR.set_ylabel("確率")
    axR.set_title("確率的解は高需要にヘッジ（x_RP > x_det）")
    axR.legend(fontsize=8)

    fig.suptitle("二段階確率計画：決定論より VSS 分お得、完全予測には EVPI 分及ばない", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.95))

    os.makedirs(FIG_DIR, exist_ok=True)
    out = os.path.join(FIG_DIR, "06b_two_stage_vss_evpi.svg")
    fig.savefig(out)
    print(f"[saved] {out}")


if __name__ == "__main__":
    main()
