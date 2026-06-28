"""
06c_risk_averse_two_stage.py — Module 6b「リスク中立 vs リスク回避（CVaR）二段階」

実行:
    python3 scripts/06c_risk_averse_two_stage.py
出力:
    figures/06c_risk_averse_two_stage.svg

希少な高需要スパイク(180)を含むシナリオで、
リスク中立(期待値最小)とリスク回避(CVaR最小)の第1段決定 x* と
シナリオ別コスト分布を対比。リスク回避は平均を犠牲に最悪を平準化する。
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
XI = np.array([70., 100., 130., 180.])
PI = np.array([0.30, 0.40, 0.25, 0.05])   # 稀な180
S = len(XI)


def scen_cost(x):
    return np.array([C1 * x + (C2 * max(d - x, 0) - V * min(max(x - d, 0), B)) for d in XI])


def solve_risk_neutral():
    x = cp.Variable(nonneg=True)
    sh = cp.Variable(S, nonneg=True); su = cp.Variable(S, nonneg=True); st = cp.Variable(S, nonneg=True)
    cons = []
    for s in range(S):
        cons += [x + sh[s] - su[s] == XI[s], st[s] <= su[s], st[s] <= B]
    Q = [C2 * sh[s] - V * st[s] for s in range(S)]
    cp.Problem(cp.Minimize(C1 * x + sum(PI[s] * Q[s] for s in range(S))), cons).solve(solver=cp.CLARABEL)
    return float(x.value)


def solve_risk_averse(alpha):
    x = cp.Variable(nonneg=True); eta = cp.Variable(); u = cp.Variable(S, nonneg=True)
    sh = cp.Variable(S, nonneg=True); su = cp.Variable(S, nonneg=True); st = cp.Variable(S, nonneg=True)
    cons = []
    for s in range(S):
        cons += [x + sh[s] - su[s] == XI[s], st[s] <= su[s], st[s] <= B]
    Q = [C2 * sh[s] - V * st[s] for s in range(S)]
    total = [C1 * x + Q[s] for s in range(S)]
    cons += [u[s] >= total[s] - eta for s in range(S)]
    obj = eta + 1.0 / (1 - alpha) * sum(PI[s] * u[s] for s in range(S))
    cp.Problem(cp.Minimize(obj), cons).solve(solver=cp.CLARABEL)
    return float(x.value)


def main() -> None:
    xN = solve_risk_neutral()
    xA = solve_risk_averse(0.90)
    cN, cA = scen_cost(xN), scen_cost(xA)
    meanN, meanA = float(PI @ cN), float(PI @ cA)
    worstN, worstA = float(cN.max()), float(cA.max())
    print(f"リスク中立 x*={xN:.0f} E={meanN:.0f} worst={worstN:.0f} costs={cN.round(0)}")
    print(f"リスク回避 x*={xA:.0f} E={meanA:.0f} worst={worstA:.0f} costs={cA.round(0)}")

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.5, 4.6))

    # 左：第1段決定 x* と シナリオ分布
    axL.bar(XI, PI, width=8, color="#ccc", label="シナリオ確率 π")
    axL.axvline(xN, color="#4285f4", lw=2.5, label=f"リスク中立 x*={xN:.0f}")
    axL.axvline(xA, color="#ea4335", lw=2.5, ls="--", label=f"リスク回避 x*={xA:.0f}")
    axL.set_xlabel("正味需要 ξ"); axL.set_ylabel("確率")
    axL.set_title("リスク回避は希少スパイク(180)まで事前ヘッジ")
    axL.legend(fontsize=8)

    # 右：シナリオ別コスト（リスク回避は尾を平準化）
    w = 0.35
    idx = np.arange(S)
    axR.bar(idx - w/2, cN, w, color="#4285f4", label=f"中立 (E={meanN:.0f}, 最悪={worstN:.0f})")
    axR.bar(idx + w/2, cA, w, color="#ea4335", label=f"回避 (E={meanA:.0f}, 最悪={worstA:.0f})")
    axR.set_xticks(idx); axR.set_xticklabels([f"ξ={int(d)}\nπ={p:.2f}" for d, p in zip(XI, PI)], fontsize=8)
    axR.set_ylabel("総コスト")
    axR.set_title("中立は稀な大損(1650)を許容、回避は平準化($\\leq$900)")
    axR.legend(fontsize=8)

    fig.suptitle("リスク回避(CVaR)二段階：平均を犠牲に最悪を抑える（+185の平均で最悪を−750）", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.95))

    os.makedirs(FIG_DIR, exist_ok=True)
    out = os.path.join(FIG_DIR, "06c_risk_averse_two_stage.svg")
    fig.savefig(out)
    print(f"[saved] {out}")


if __name__ == "__main__":
    main()
