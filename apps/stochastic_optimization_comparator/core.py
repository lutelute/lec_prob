"""
core.py — 確率的最適化コンパレータの数理コア（UI非依存）

統一問題（容量調達 / newsvendor）:
    C(x, ξ) = c_s · max(ξ - x, 0) + c_o · max(x - ξ, 0)
    ξ: 不確実な需要（正規 or 対数正規, 平均 mean・標準偏差 std）

6形式の最適決定 x* を計算し、共通の指標（期待費用・不足確率・CVaR）で評価する。
`python core.py` で自己テスト（Module 6 §8 の検証値を再現）。
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats

try:
    import cvxpy as cp
    HAS_CVXPY = True
except Exception:  # pragma: no cover
    HAS_CVXPY = False


# ---------------------------------------------------------------------------
# 不確実性（平均・標準偏差で正規/対数正規を指定）
# ---------------------------------------------------------------------------
def make_dist(mean: float, std: float, kind: str = "normal"):
    if kind == "lognormal":
        s2 = np.log(1.0 + (std / mean) ** 2)
        s = np.sqrt(s2)
        return stats.lognorm(s=s, scale=np.exp(np.log(mean) - s2 / 2))
    return stats.norm(mean, std)


def cost(x, xi, cs, co):
    return cs * np.maximum(xi - x, 0.0) + co * np.maximum(x - xi, 0.0)


# ---------------------------------------------------------------------------
# 各形式の最適決定 x*
# ---------------------------------------------------------------------------
def x_deterministic(mean):
    return float(mean)


def x_expected(dist, cs, co):
    # 臨界分位点 F^{-1}(cs/(cs+co))
    return float(dist.ppf(cs / (cs + co)))


def x_robust(mean, std, cs, co, k=3.0):
    # 区間 [mean-k*std, mean+k*std] の最悪を最小化
    a, b = mean - k * std, mean + k * std
    return float((cs * b + co * a) / (cs + co))


def x_chance(dist, eps):
    # P(ξ > x) <= eps  ->  x = F^{-1}(1-eps)
    return float(dist.ppf(1.0 - eps))


def x_cvar_saa(samples, cs, co, alpha):
    """CVaR_alpha 最小化（Rockafellar–Uryasev + SAA, cvxpy）。"""
    if not HAS_CVXPY:
        return _x_cvar_grid(samples, cs, co, alpha)
    S = len(samples)
    x = cp.Variable()
    eta = cp.Variable()
    u = cp.Variable(S, nonneg=True)
    c = cs * cp.pos(samples - x) + co * cp.pos(x - samples)
    prob = cp.Problem(cp.Minimize(eta + cp.sum(u) / ((1 - alpha) * S)), [u >= c - eta])
    prob.solve(solver=cp.CLARABEL)
    return float(x.value)


def _x_cvar_grid(samples, cs, co, alpha, lo=None, hi=None, n=2001):
    """cvxpy が無い場合のフォールバック（グリッド探索で CVaR 最小化）。"""
    lo = samples.min() if lo is None else lo
    hi = samples.max() if hi is None else hi
    xs = np.linspace(lo, hi, n)
    best_x, best = xs[0], np.inf
    for xx in xs:
        c = np.sort(cost(xx, samples, cs, co))
        k = int(np.ceil(alpha * len(c)))
        cv = c[k:].mean() if k < len(c) else c[-1]
        if cv < best:
            best, best_x = cv, xx
    return float(best_x)


def x_dro_scarf(mean, std, cs, co):
    # Scarf newsvendor: 平均・分散のみ既知のときの最悪分布に最適
    return float(mean + std / 2.0 * (np.sqrt(cs / co) - np.sqrt(co / cs)))


# ---------------------------------------------------------------------------
# 評価（共通サンプルで各 x* を採点）
# ---------------------------------------------------------------------------
def evaluate(x, samples, cs, co, alpha=0.9):
    c = cost(x, samples, cs, co)
    cs_sorted = np.sort(c)
    k = int(np.ceil(alpha * len(cs_sorted)))
    cvar = float(cs_sorted[k:].mean()) if k < len(cs_sorted) else float(cs_sorted[-1])
    return {
        "expected_cost": float(c.mean()),
        "shortage_prob": float((samples > x).mean()),  # P(不足)
        "cvar": cvar,
        "worst_cost": float(c.max()),
    }


@dataclass
class FormResult:
    name: str
    x: float
    expected_cost: float
    shortage_prob: float
    cvar: float
    note: str


def solve_all(mean=100.0, std=15.0, cs=10.0, co=1.0, eps=0.1, alpha=0.9,
              k_robust=3.0, kind="normal", n_samples=20000, seed=0) -> list[FormResult]:
    dist = make_dist(mean, std, kind)
    rng = np.random.default_rng(seed)
    samples = dist.rvs(size=n_samples, random_state=rng)

    forms = {
        "①決定論": (x_deterministic(mean), "平均で計画（非対称無視）"),
        "②期待値最小化": (x_expected(dist, cs, co), f"臨界分位点 {cs/(cs+co):.3f}"),
        "③ロバスト": (x_robust(mean, std, cs, co, k_robust), f"区間±{k_robust:.0f}σの最悪"),
        "④チャンス制約": (x_chance(dist, eps), f"P(不足)≤{eps}"),
        "⑤CVaR最小化": (x_cvar_saa(samples, cs, co, alpha), f"最悪{1-alpha:.0%}の平均"),
        "⑥分布ロバスト": (x_dro_scarf(mean, std, cs, co), "Scarf(平均・分散)"),
    }
    out = []
    for name, (x, note) in forms.items():
        ev = evaluate(x, samples, cs, co, alpha)
        out.append(FormResult(name, float(x), ev["expected_cost"],
                              ev["shortage_prob"], ev["cvar"], note))
    return out


# ---------------------------------------------------------------------------
# 自己テスト
# ---------------------------------------------------------------------------
def _selftest():
    print("=== stochastic_optimization_comparator self-test ===")
    print("cvxpy:", "available" if HAS_CVXPY else "NOT available (grid fallback)")
    res = solve_all()
    print(f"{'形式':14s} {'x*':>8s} {'E[cost]':>9s} {'P(不足)':>8s} {'CVaR.9':>8s}  note")
    for r in res:
        print(f"{r.name:14s} {r.x:8.2f} {r.expected_cost:9.2f} "
              f"{r.shortage_prob:8.3f} {r.cvar:8.2f}  {r.note}")
    xs = {r.name: r.x for r in res}
    # 期待される並び（Module 6 §8）
    checks = [
        ("①<②", xs["①決定論"] < xs["②期待値最小化"]),
        ("②<⑤", xs["②期待値最小化"] < xs["⑤CVaR最小化"]),
        ("⑤<③", xs["⑤CVaR最小化"] < xs["③ロバスト"]),
        ("①≈100", abs(xs["①決定論"] - 100) < 1e-6),
        ("②≈120", abs(xs["②期待値最小化"] - 120.03) < 1.0),
        ("③≈136.8", abs(xs["③ロバスト"] - 136.82) < 1.0),
    ]
    ok = all(c for _, c in checks)
    for n, c in checks:
        print(f"  [{'OK' if c else 'NG'}] {n}")
    # ②は最小の期待費用のはず
    ec = {r.name: r.expected_cost for r in res}
    min_ec = min(ec, key=ec.get)
    print(f"  最小E[cost] = {min_ec}（②期待値最小化のはず）",
          "[OK]" if min_ec == "②期待値最小化" else "[NG]")
    ok &= (min_ec == "②期待値最小化")
    print("=== result:", "ALL OK" if ok else "CHECK", "===")


if __name__ == "__main__":
    _selftest()
