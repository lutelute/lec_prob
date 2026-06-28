"""
core.py — モンテカルロ収束ビジュアライザの数理コア（UI非依存）

Module 5 の「平均は速く・尾（希少事象）は遅い」を対話的に学ぶための計算。
推定対象を選び、サンプル数 N を増やしたときの逐次推定と信頼区間の収束を返す。
`python core.py` で自己テスト。
"""
from __future__ import annotations

import numpy as np
from scipy import stats


def make_dist(mean: float, std: float, kind: str = "normal"):
    if kind == "lognormal":
        s2 = np.log(1.0 + (std / mean) ** 2)
        return stats.lognorm(s=np.sqrt(s2), scale=np.exp(np.log(mean) - s2 / 2))
    return stats.norm(mean, std)


def running_mean_ci(samples: np.ndarray):
    """逐次標本平均と 95%CI 半幅（標準誤差 s/√n を逐次に）。"""
    n = np.arange(1, len(samples) + 1)
    run = np.cumsum(samples) / n
    # 逐次標準偏差（ddof=1 近似）
    csum2 = np.cumsum(samples ** 2)
    var = np.maximum(csum2 / n - run ** 2, 0.0) * n / np.maximum(n - 1, 1)
    ci = 1.96 * np.sqrt(var) / np.sqrt(n)
    return run, ci


def estimate_expectation(dist, n_max: int, seed: int = 0):
    """E[X] の逐次推定。true は解析平均。"""
    rng = np.random.default_rng(seed)
    s = dist.rvs(size=n_max, random_state=rng)
    run, ci = running_mean_ci(s)
    return {"true": float(dist.mean()), "estimate": run, "ci": ci}


def estimate_exceedance(dist, threshold: float, Ns, seed: int = 0):
    """P(X > threshold) を各 N で推定（希少事象の難しさ）。true は解析値。"""
    rng = np.random.default_rng(seed)
    s = dist.rvs(size=int(max(Ns)), random_state=rng)
    indic = (s > threshold).astype(float)
    ests, hits = [], []
    for N in Ns:
        ests.append(float(indic[:N].mean()))
        hits.append(int(indic[:N].sum()))
    return {"true": float(dist.sf(threshold)), "Ns": list(Ns),
            "estimates": ests, "hits": hits}


def saa_newsvendor(dist, cs: float, co: float, Ns, seed: int = 0):
    """容量問題の SAA 最適 q の収束（true は臨界分位点）。"""
    rng = np.random.default_rng(seed)
    s = dist.rvs(size=int(max(Ns)), random_state=rng)
    qs = np.linspace(float(dist.ppf(0.001)), float(dist.ppf(0.999)), 601)
    q_true = float(dist.ppf(cs / (cs + co)))
    out = []
    for N in Ns:
        ss = s[:N]
        ec = [np.mean(cs * np.maximum(ss - q, 0) + co * np.maximum(q - ss, 0)) for q in qs]
        out.append(float(qs[int(np.argmin(ec))]))
    return {"true": q_true, "Ns": list(Ns), "q_hat": out}


# ---------------------------------------------------------------------------
def _selftest():
    print("=== monte_carlo_visualizer self-test ===")
    ok = True
    d = make_dist(100, 15, "normal")

    r = estimate_expectation(d, 50000, seed=42)
    conv = abs(r["estimate"][-1] - 100) < 1.0
    ci_shrinks = r["ci"][-1] < r["ci"][9]
    ok &= conv and ci_shrinks
    print(f"[{'OK' if conv and ci_shrinks else 'NG'}] E[X]: 推定={r['estimate'][-1]:.3f}(true100), "
          f"CI {r['ci'][9]:.3f}->{r['ci'][-1]:.3f}")

    e = estimate_exceedance(d, 145, [1000, 10000, 100000, 1000000], seed=42)
    rare_ok = e["hits"][0] <= 5 and abs(e["estimates"][-1] - e["true"]) / e["true"] < 0.2
    ok &= rare_ok
    print(f"[{'OK' if rare_ok else 'NG'}] P(X>145)={e['true']:.5f}: hits {e['hits']}, est_last={e['estimates'][-1]:.5f}")

    s = saa_newsvendor(d, 10, 1, [20, 100, 1000, 10000], seed=42)
    saa_ok = abs(s["q_hat"][-1] - s["true"]) < 1.0
    ok &= saa_ok
    print(f"[{'OK' if saa_ok else 'NG'}] SAA q: {[round(x,1) for x in s['q_hat']]} -> true {s['true']:.2f}")

    print("=== result:", "ALL OK" if ok else "CHECK", "===")


if __name__ == "__main__":
    _selftest()
