"""
core.py — 蓄電池運用ツールの数理コア（UI非依存）

多時間帯の蓄電池アービトラージ（SoC ダイナミクス）と、価格不確実性下での
「決定論（予測で計画）vs 完全予測（perfect foresight）」の比較。
Module 6b（二段階・VSS/EVPI）の多時間帯版に相当する直感を与える。

`python core.py` で自己テスト。
"""
from __future__ import annotations

import numpy as np

try:
    import cvxpy as cp
    HAS_CVXPY = True
except Exception:  # pragma: no cover
    HAS_CVXPY = False


def price_profile(T: int = 24, base: float = 20.0, day_amp: float = 12.0,
                  eve_amp: float = 8.0, eve_hour: int = 19) -> np.ndarray:
    """典型的な日内価格 [円/kWh 相当]：夜安・日中やや高・夕方ピーク。"""
    h = np.arange(T)
    daily = day_amp * np.sin((h - 9) / 24 * 2 * np.pi)        # 日中高・未明低
    evening = eve_amp * np.exp(-(((h - eve_hour + T) % T) ** 2) / 6.0)  # 夕方の山
    return base + daily + evening


def optimize_dispatch(prices: np.ndarray, cap: float = 10.0, pmax: float = 3.0,
                      eff: float = 0.90, soc0_frac: float = 0.5,
                      soc_end_frac: float = 0.5) -> dict:
    """価格 prices に対する利益最大化の充放電計画（LP, cvxpy）。

    変数: 充電 c_t≥0, 放電 d_t≥0, 蓄電量 soc_t。
    SoC: soc_{t+1} = soc_t + √η·c_t − d_t/√η（往復効率 η）。
    目的: max Σ p_t (d_t − c_t)。
    """
    T = len(prices)
    rt = np.sqrt(eff)
    if not HAS_CVXPY:
        return _greedy_dispatch(prices, cap, pmax, eff, soc0_frac, soc_end_frac)
    c = cp.Variable(T, nonneg=True)
    d = cp.Variable(T, nonneg=True)
    soc = cp.Variable(T + 1, nonneg=True)
    cons = [soc[0] == cap * soc0_frac, soc[T] == cap * soc_end_frac]
    for t in range(T):
        cons += [soc[t + 1] == soc[t] + rt * c[t] - d[t] / rt,
                 soc[t + 1] <= cap, c[t] <= pmax, d[t] <= pmax]
    profit = prices @ (d - c)
    cp.Problem(cp.Maximize(profit), cons).solve(solver=cp.CLARABEL)
    return {"charge": np.maximum(c.value, 0), "discharge": np.maximum(d.value, 0),
            "soc": soc.value, "profit": float(profit.value)}


def _greedy_dispatch(prices, cap, pmax, eff, soc0_frac, soc_end_frac):
    """cvxpy が無い場合の素朴なフォールバック（近似）。"""
    T = len(prices)
    rt = np.sqrt(eff)
    soc = np.full(T + 1, cap * soc0_frac)
    c = np.zeros(T); d = np.zeros(T)
    thr_lo, thr_hi = np.percentile(prices, 33), np.percentile(prices, 66)
    for t in range(T):
        if prices[t] <= thr_lo:
            c[t] = min(pmax, (cap - soc[t]) / rt)
        elif prices[t] >= thr_hi:
            d[t] = min(pmax, soc[t] * rt)
        soc[t + 1] = soc[t] + rt * c[t] - d[t] / rt
    return {"charge": c, "discharge": d, "soc": soc, "profit": float(prices @ (d - c))}


def evaluate_schedule(prices: np.ndarray, charge: np.ndarray, discharge: np.ndarray) -> float:
    """固定スケジュール（charge/discharge）を別の価格で評価した実現利益。"""
    return float(prices @ (discharge - charge))


def make_scenarios(mean_prices: np.ndarray, sigma: float, n: int, seed: int = 0) -> np.ndarray:
    """平均価格にノイズを乗せた価格シナリオ（n×T）。負価格は0で打ち切り。"""
    rng = np.random.default_rng(seed)
    noise = rng.normal(0, sigma, size=(n, len(mean_prices)))
    return np.maximum(mean_prices[None, :] + noise, 0.0)


def compare_under_uncertainty(mean_prices, sigma, n, cap, pmax, eff, seed=0) -> dict:
    """決定論（予測=平均で計画→実価格で評価）vs 完全予測（各シナリオで再最適化）。

    返り値:
      det_profit  : 予測で立てた計画を実シナリオに適用した平均利益（EEV相当）
      ws_profit   : 各シナリオで完全予測のもと最適化した平均利益（WS相当）
      gap         : ws − det = 予測誤差のコスト＝完全予測の価値（EVPI相当）
    """
    scen = make_scenarios(mean_prices, sigma, n, seed)
    plan = optimize_dispatch(mean_prices, cap, pmax, eff)  # 予測で計画
    det = np.mean([evaluate_schedule(s, plan["charge"], plan["discharge"]) for s in scen])
    ws = np.mean([optimize_dispatch(s, cap, pmax, eff)["profit"] for s in scen])
    return {"det_profit": float(det), "ws_profit": float(ws), "gap": float(ws - det),
            "plan": plan, "scenarios": scen}


# ---------------------------------------------------------------------------
def _selftest():
    print("=== battery_dispatch self-test ===")
    ok = True
    p = price_profile()
    r = optimize_dispatch(p)
    # 1) 安いとき充電・高いとき放電
    cavg = (p * r["charge"]).sum() / max(r["charge"].sum(), 1e-9)
    davg = (p * r["discharge"]).sum() / max(r["discharge"].sum(), 1e-9)
    c1 = cavg < davg and r["profit"] > 0
    ok &= c1
    print(f"[{'OK' if c1 else 'NG'}] 利益={r['profit']:.1f}, 平均充電価格{cavg:.1f}<放電{davg:.1f}")
    # 2) SoC が容量内
    c2 = r["soc"].min() >= -1e-6 and r["soc"].max() <= 10 + 1e-6
    ok &= c2
    print(f"[{'OK' if c2 else 'NG'}] SoC∈[{r['soc'].min():.2f},{r['soc'].max():.2f}] ⊂ [0,10]")
    # 3) 完全予測 ≥ 決定論（予測誤差のコスト ≥ 0）
    comp = compare_under_uncertainty(p, sigma=6.0, n=40, cap=10, pmax=3, eff=0.9, seed=1)
    c3 = comp["gap"] >= -1e-6 and comp["ws_profit"] >= comp["det_profit"] - 1e-6
    ok &= c3
    print(f"[{'OK' if c3 else 'NG'}] WS={comp['ws_profit']:.1f} ≥ det={comp['det_profit']:.1f}, "
          f"予測誤差コスト(gap)={comp['gap']:.1f}")
    # 4) 効率を下げると利益が下がる（往復ロス）
    r_lo = optimize_dispatch(p, eff=0.7)
    c4 = r_lo["profit"] <= r["profit"] + 1e-6
    ok &= c4
    print(f"[{'OK' if c4 else 'NG'}] η=0.9利益{r['profit']:.1f} ≥ η=0.7利益{r_lo['profit']:.1f}")
    print("=== result:", "ALL OK" if ok else "CHECK", "===")


if __name__ == "__main__":
    _selftest()
