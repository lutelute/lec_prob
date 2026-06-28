"""
core.py — ベイズ更新ビジュアライザの数理コア（UI非依存）

Module 1 の「基準率の誤謬（base-rate fallacy）」を対話的に学ぶための計算。
保護リレー例：故障 F、警報 alarm。
    事前 P(F)=prior, 感度 P(alarm|F)=sens, 誤警報率 P(alarm|¬F)=fpr。
`python core.py` で自己テスト（Module 1 §6 の検証値 16.7% などを再現）。
"""
from __future__ import annotations


def posterior_positive(prior: float, sens: float, fpr: float) -> float:
    """P(F | alarm) = sens·prior / (sens·prior + fpr·(1-prior))。"""
    num = sens * prior
    den = sens * prior + fpr * (1.0 - prior)
    return num / den if den > 0 else 0.0


def posterior_negative(prior: float, sens: float, fpr: float) -> float:
    """P(F | no alarm) = (1-sens)·prior / ((1-sens)·prior + (1-fpr)·(1-prior))。"""
    num = (1.0 - sens) * prior
    den = (1.0 - sens) * prior + (1.0 - fpr) * (1.0 - prior)
    return num / den if den > 0 else 0.0


def confusion_counts(n: int, prior: float, sens: float, fpr: float) -> dict:
    """n 件あたりの内訳（期待値）。TP/FP/FN/TN。"""
    n_f = n * prior
    n_nf = n * (1.0 - prior)
    tp = n_f * sens
    fn = n_f * (1.0 - sens)
    fp = n_nf * fpr
    tn = n_nf * (1.0 - fpr)
    return {"TP": tp, "FN": fn, "FP": fp, "TN": tn,
            "alarms": tp + fp, "ppv": tp / (tp + fp) if (tp + fp) > 0 else 0.0}


def _odds(p: float) -> float:
    return p / (1.0 - p) if p < 1.0 else float("inf")


def _prob(o: float) -> float:
    return o / (1.0 + o)


def sequential_update(prior: float, sens: float, fpr: float,
                      n_pos: int, n_neg: int = 0) -> float:
    """独立な観測（警報 n_pos 回・無警報 n_neg 回）後の事後確率（オッズ更新）。

    posterior_odds = prior_odds · (LR+)^n_pos · (LR-)^n_neg,
      LR+ = sens/fpr,  LR- = (1-sens)/(1-fpr)。
    """
    lr_pos = sens / fpr if fpr > 0 else float("inf")
    lr_neg = (1.0 - sens) / (1.0 - fpr) if fpr < 1.0 else 0.0
    o = _odds(prior) * (lr_pos ** n_pos) * (lr_neg ** n_neg)
    return _prob(o)


def update_path(prior: float, sens: float, fpr: float, n_pos: int) -> list[float]:
    """警報を 0,1,2,...,n_pos 回観測したときの事後確率の系列（逐次更新の可視化用）。"""
    return [sequential_update(prior, sens, fpr, k, 0) for k in range(n_pos + 1)]


# ---------------------------------------------------------------------------
def _selftest() -> None:
    print("=== bayes_visualizer self-test ===")
    ok = True

    # Module 1 §6 の値：prior .01, sens .99, fpr .05 → 16.7%
    p = posterior_positive(0.01, 0.99, 0.05)
    c1 = abs(p - 0.16667) < 1e-3
    ok &= c1
    print(f"[{'OK' if c1 else 'NG'}] P(F|alarm) = {p:.4f} (期待 0.1667)")

    # 内訳の PPV が posterior と一致
    cc = confusion_counts(1000, 0.01, 0.99, 0.05)
    c2 = abs(cc["ppv"] - p) < 1e-9
    ok &= c2
    print(f"[{'OK' if c2 else 'NG'}] PPV={cc['ppv']:.4f} == posterior  (alarms={cc['alarms']:.1f}, TP={cc['TP']:.1f})")

    # 逐次更新：1回でベイズ単発と一致、2回で約0.798
    s1 = sequential_update(0.01, 0.99, 0.05, 1)
    s2 = sequential_update(0.01, 0.99, 0.05, 2)
    c3 = abs(s1 - p) < 1e-9 and abs(s2 - 0.7983) < 1e-2
    ok &= c3
    print(f"[{'OK' if c3 else 'NG'}] 逐次: 1警報={s1:.4f}, 2警報={s2:.4f} (期待 ≈0.80)")

    # 基準率を上げると事後も上がる（単調）
    ps = [posterior_positive(b, 0.99, 0.05) for b in [0.01, 0.05, 0.1, 0.3]]
    c4 = all(ps[i] < ps[i+1] for i in range(len(ps)-1))
    ok &= c4
    print(f"[{'OK' if c4 else 'NG'}] 事後は基準率に単調増加: {[round(x,3) for x in ps]}")

    # 特異度を上げる(fpr↓)効果 > 感度を上げる効果（低基準率域）
    base = posterior_positive(0.01, 0.99, 0.05)
    by_sens = posterior_positive(0.01, 1.0, 0.05)     # 感度最大
    by_spec = posterior_positive(0.01, 0.99, 0.01)    # 誤警報率↓
    c5 = (by_spec - base) > (by_sens - base)
    ok &= c5
    print(f"[{'OK' if c5 else 'NG'}] 低基準率では特異度改善が有効: base={base:.3f} 感度↑={by_sens:.3f} 特異度↑={by_spec:.3f}")

    print("=== result:", "ALL OK" if ok else "CHECK", "===")


if __name__ == "__main__":
    _selftest()
