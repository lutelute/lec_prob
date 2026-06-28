"""
gen_sample_data.py — 教材用の合成データ生成（再現可能）

実行:
    python3 scripts/gen_sample_data.py
出力:
    data/daily_peak_demand.csv   日次最大需要[万kW]（2年, 季節性+曜日+ノイズ）
    data/pv_daily_factor.csv     日次PV設備利用率[0-1]（季節性+天候ノイズ, 右歪み）

教材方針：
- 季節性・曜日効果・非定常を意図的に入れ、「iid 仮定の限界」「観測≠真の分布」を体験させる。
- 乱数は固定シードで再現可能。真の生成過程をコメントに明記（学習者が答え合わせできる）。
"""
from __future__ import annotations

import csv
import os

import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

SEED = 20260628
DAYS = 730  # 2年


def main() -> None:
    rng = np.random.default_rng(SEED)
    t = np.arange(DAYS)

    # --- 日次最大需要 [万kW] ---
    # 真の過程：ベース100 + 年周期(夏冬2山) + 曜日(週末-8) + 緩やかな増加トレンド + ガウスノイズ
    season = 12 * np.cos(2 * np.pi * (t - 15) / 365.25) \
        + 10 * np.cos(4 * np.pi * (t - 15) / 365.25)   # 夏冬の2山
    weekday = np.where((t % 7) >= 5, -8.0, 0.0)         # 週末は需要減
    trend = 0.004 * t                                   # 2年で約+3
    noise = rng.normal(0, 5, DAYS)
    demand = 100 + season + weekday + trend + noise

    # --- 日次PV設備利用率 [0-1]（右歪み：曇天で低い日が出る）---
    # ベース利用率(夏高・冬低) を平均にした Beta 系の歪み分布
    pv_mean = 0.18 + 0.10 * np.cos(2 * np.pi * (t - 172) / 365.25)  # 夏至付近で高い
    pv_mean = np.clip(pv_mean, 0.05, 0.45)
    # 天候：晴れの日は高め、曇天はゼロ近くへ（混合で右歪み/下に重い）
    cloud = rng.beta(2.0, 2.0, DAYS)            # 0-1 の天候係数
    pv = np.clip(pv_mean * (0.4 + 1.2 * cloud) + rng.normal(0, 0.02, DAYS), 0.0, 0.9)

    os.makedirs(DATA_DIR, exist_ok=True)

    d1 = os.path.join(DATA_DIR, "daily_peak_demand.csv")
    with open(d1, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["day_index", "weekday", "demand_mw10k"])
        for i in range(DAYS):
            w.writerow([i, int(t[i] % 7), round(float(demand[i]), 2)])

    d2 = os.path.join(DATA_DIR, "pv_daily_factor.csv")
    with open(d2, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["day_index", "pv_capacity_factor"])
        for i in range(DAYS):
            w.writerow([i, round(float(pv[i]), 4)])

    # --- 要約統計（本文・検証用に表示）---
    def summ(name, x):
        print(f"{name}: n={len(x)} mean={x.mean():.3f} std={x.std(ddof=1):.3f} "
              f"min={x.min():.3f} p50={np.median(x):.3f} max={x.max():.3f}")

    print("[saved]", d1)
    print("[saved]", d2)
    summ("demand", demand)
    summ("pv    ", pv)
    # 夏(6-8月相当: day 152-243) と 冬(day 0-59,335-) の平均差（季節性=非定常の証拠）
    summer = demand[(t % 365 >= 152) & (t % 365 <= 243)]
    winter = demand[(t % 365 <= 59) | (t % 365 >= 335)]
    print(f"季節性チェック: 夏平均={summer.mean():.1f} 冬平均={winter.mean():.1f} "
          f"差={summer.mean()-winter.mean():.1f}（→ 全期間を1分布で扱う危うさ）")


if __name__ == "__main__":
    main()
