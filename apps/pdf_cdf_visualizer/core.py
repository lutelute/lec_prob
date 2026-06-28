"""
core.py — PDF・CDF・区間確率ビジュアライザの数理コア（UIから分離）

ここには Streamlit に依存しない純粋な計算だけを置く。
- 分布の定義（パラメータ仕様つき）
- PDF / CDF の評価
- 区間確率の3通りの計算（面積・CDF差・scipy）→ 一致を確認するための土台

UI（app.py）と分離してあるので、`python core.py` で自己テストできる。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from scipy import stats
from scipy.integrate import trapezoid


# ---------------------------------------------------------------------------
# パラメータ仕様：スライダー生成のためのメタ情報
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Param:
    key: str
    label: str
    vmin: float
    vmax: float
    default: float
    step: float


@dataclass(frozen=True)
class DistSpec:
    """1つの分布の定義。params から scipy の凍結分布を作る factory を持つ。"""
    name: str
    params: list[Param]
    factory: Callable[[dict], stats.rv_continuous]
    # 学習用の電力的な読み替え（X を何だと思うか）
    power_reading: str
    note: str = ""

    def make(self, values: dict) -> "stats.rv_frozen":
        return self.factory(values)


# ---------------------------------------------------------------------------
# 分布カタログ
# ---------------------------------------------------------------------------
def _normal(v: dict):
    # X ~ N(mu, sigma^2)
    return stats.norm(loc=v["mu"], scale=v["sigma"])


def _lognormal(v: dict):
    # log X ~ N(mu_log, sigma_log^2)。scipy では s=sigma_log, scale=exp(mu_log)
    return stats.lognorm(s=v["sigma_log"], scale=np.exp(v["mu_log"]))


def _exponential(v: dict):
    # X ~ Exp(rate)。平均は 1/rate。scipy は scale=1/rate
    rate = max(v["rate"], 1e-6)
    return stats.expon(scale=1.0 / rate)


def _uniform(v: dict):
    # X ~ U(a, b)。scipy は loc=a, scale=b-a
    a, b = v["a"], v["b"]
    if b <= a:
        b = a + 1e-6
    return stats.uniform(loc=a, scale=b - a)


DISTRIBUTIONS: dict[str, DistSpec] = {
    "正規分布 Normal": DistSpec(
        name="正規分布 Normal",
        params=[
            Param("mu", "平均 μ", -50.0, 150.0, 100.0, 1.0),
            Param("sigma", "標準偏差 σ", 0.5, 40.0, 15.0, 0.5),
        ],
        factory=_normal,
        power_reading="X = 明日の最大需要[万kW]。左右対称な予測誤差の素朴なモデル。",
        note="対称・釣鐘型。裾は軽い（極端事象を過小評価しがち）。",
    ),
    "対数正規 Lognormal": DistSpec(
        name="対数正規 Lognormal",
        params=[
            Param("mu_log", "対数平均 μ_log", 2.0, 6.0, 4.5, 0.05),
            Param("sigma_log", "対数標準偏差 σ_log", 0.05, 1.2, 0.4, 0.05),
        ],
        factory=_lognormal,
        power_reading="X = 電力市場価格[円/kWh] や需要。正の値・右に重い裾（スパイク）。",
        note="非負・右歪み。価格や需要など「下限0で時々大きく跳ねる」量に向く。",
    ),
    "指数分布 Exponential": DistSpec(
        name="指数分布 Exponential",
        params=[
            Param("rate", "率 λ（平均=1/λ）", 0.02, 1.0, 0.1, 0.01),
        ],
        factory=_exponential,
        power_reading="X = 設備の故障間隔[時間]。記憶なし性をもつ待ち時間モデル。",
        note="非負・単調減少の密度。x=0 付近が最も密度が高い。",
    ),
    "一様分布 Uniform": DistSpec(
        name="一様分布 Uniform",
        params=[
            Param("a", "下限 a", -20.0, 100.0, 60.0, 1.0),
            Param("b", "上限 b", -20.0, 200.0, 140.0, 1.0),
        ],
        factory=_uniform,
        power_reading="X = 出力抑制の指令値[%]。区間内で『どれも同程度ありうる』粗いモデル。",
        note="区間内一定。密度の高さは 1/(b-a) で、a,b を広げると平らに低くなる。",
    ),
}


# ---------------------------------------------------------------------------
# 評価ユーティリティ
# ---------------------------------------------------------------------------
def support_range(dist, q_lo: float = 0.001, q_hi: float = 0.999,
                  pad: float = 0.05) -> tuple[float, float]:
    """描画用の x 範囲。分位点で両裾を切り、少し余白を付ける。"""
    lo = float(dist.ppf(q_lo))
    hi = float(dist.ppf(q_hi))
    if not np.isfinite(lo):
        lo = float(dist.ppf(0.005))
    if not np.isfinite(hi):
        hi = float(dist.ppf(0.995))
    span = hi - lo
    return lo - pad * span, hi + pad * span


def grid(dist, n: int = 600) -> np.ndarray:
    lo, hi = support_range(dist)
    return np.linspace(lo, hi, n)


def interval_prob_cdf(dist, a: float, b: float) -> float:
    """P(a <= X <= b) を CDF の差で。連続分布では P(X=a)=0 なので等号は無関係。"""
    a, b = (a, b) if a <= b else (b, a)
    return float(dist.cdf(b) - dist.cdf(a))


def interval_prob_area(dist, a: float, b: float, n: int = 4000) -> float:
    """P(a <= X <= b) を密度の数値積分（台形則）で。CDF差と一致するはず。"""
    a, b = (a, b) if a <= b else (b, a)
    xs = np.linspace(a, b, n)
    return float(trapezoid(dist.pdf(xs), xs))


def point_interval_demo(dist, x0: float, eps: float) -> dict:
    """点 x0 まわりの微小区間 [x0-eps, x0+eps] の確率を、密度の高さと対比する。

    返り値:
      f_height    : 密度 f(x0)（確率ではない！）
      p_interval  : P(x0-eps <= X <= x0+eps)（区間の面積＝確率）
      approx      : f(x0)*2eps（微小区間の近似：面積 ≒ 高さ×幅）
    """
    f_height = float(dist.pdf(x0))
    p_interval = interval_prob_cdf(dist, x0 - eps, x0 + eps)
    approx = f_height * 2.0 * eps
    return {"f_height": f_height, "p_interval": p_interval, "approx": approx}


# ---------------------------------------------------------------------------
# 自己テスト：3通りの確率計算が一致すること等を確認
# ---------------------------------------------------------------------------
def _selftest() -> None:
    print("=== core.py self-test ===")
    ok = True

    # 1) 各分布で「区間確率：面積 ≈ CDF差 ≈ scipy」一致
    for name, spec in DISTRIBUTIONS.items():
        v = {p.key: p.default for p in spec.params}
        dist = spec.make(v)
        lo, hi = support_range(dist)
        a, b = lo + 0.3 * (hi - lo), lo + 0.6 * (hi - lo)
        p_cdf = interval_prob_cdf(dist, a, b)
        p_area = interval_prob_area(dist, a, b)
        diff = abs(p_cdf - p_area)
        status = "OK" if diff < 1e-3 else "NG"
        ok &= diff < 1e-3
        print(f"[{status}] {name:22s} P(a≤X≤b): CDF差={p_cdf:.5f} 面積={p_area:.5f} |Δ|={diff:.2e}")

    # 2) 全区間の確率は 1
    for name, spec in DISTRIBUTIONS.items():
        v = {p.key: p.default for p in spec.params}
        dist = spec.make(v)
        total = float(dist.cdf(dist.ppf(0.99999)) - dist.cdf(dist.ppf(1e-5)))
        status = "OK" if abs(total - 1.0) < 1e-3 else "NG"
        ok &= abs(total - 1.0) < 1e-3
        print(f"[{status}] {name:22s} 全確率 ≈ {total:.5f}")

    # 3) 点まわりの微小区間 → 確率は eps→0 で 0 に、面積 ≒ 高さ×幅
    dist = DISTRIBUTIONS["正規分布 Normal"].make({"mu": 100, "sigma": 15})
    x0 = 100.0
    print("--- 点まわりデモ（X=100, μ=100,σ=15）---")
    prev = None
    for eps in [5.0, 1.0, 0.2, 0.01]:
        d = point_interval_demo(dist, x0, eps)
        print(f"  eps={eps:5.2f}: f(x0)(高さ)={d['f_height']:.5f}  "
              f"P(区間)={d['p_interval']:.6f}  近似f*2eps={d['approx']:.6f}")
        prev = d["p_interval"]
    shrink_ok = prev < 1e-3
    ok &= shrink_ok
    print(f"[{'OK' if shrink_ok else 'NG'}] eps→0 で P(区間)→0（点の確率は0）")

    print("=== result:", "ALL OK" if ok else "FAILED", "===")


if __name__ == "__main__":
    _selftest()
