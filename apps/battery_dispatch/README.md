# 蓄電池運用ビジュアライザ

多時間帯の**蓄電池アービトラージ**（安いとき充電・高いとき放電）を SoC ダイナミクスとともに可視化し、
価格が不確実なとき**「予測で計画する（決定論）」と「完全予測」の差**を見せるツールです。
Module 6b（二段階・VSS/EVPI）の**多時間帯版の直感**を与えます。

関連ノート：[`notes/06b_two_stage_stochastic_programming.md`](../../notes/06b_two_stage_stochastic_programming.md)。

## 1. 何が体験できるか
1. 蓄電池は**エネルギーの時間シフト**で価値を生む（安→高）。SoC・出力・効率がその制約。
2. 価格が不確実だと、固定計画は完全予測に劣る＝**予測誤差のコスト**（EVPI 直感）。
3. 往復効率 η<1 のロス、容量・出力の頭打ちを体感。

## 2. 最適化の明示
- **決定変数**：充電 $c_t$、放電 $d_t$、蓄電量 $\mathrm{SoC}_t$。
- **不確実変数**：価格 $\xi_t$（シナリオで表現）。
- **目的**：利益 $\max\sum_t \xi_t(d_t-c_t)$（決定論）／期待利益（確率的）。
- **制約**（常時満足）：$\mathrm{SoC}_{t+1}=\mathrm{SoC}_t+\sqrt\eta\,c_t-d_t/\sqrt\eta$、$0\le\mathrm{SoC}\le\bar S$、$0\le c_t,d_t\le P_{\max}$。
- **決定論と比べて**：完全予測（WS）は固定計画（決定論, EEV相当）より高利益。差＝予測誤差のコスト（EVPI相当）。実運用は価格判明ごとに再最適化(recourse)するため両者の**中間**。

## 3. 実行
```bash
streamlit run apps/battery_dispatch/app.py
python3 apps/battery_dispatch/core.py   # 自己テスト（cvxpy）
```
依存：`numpy`, `cvxpy`, `plotly`, `streamlit`（cvxpy 無しは貪欲法でフォールバック）。

## 4. 操作パラメータ
容量・最大出力・往復効率、価格プロファイル（ベース/日内振幅/夕方ピーク）、予測誤差 σ、シナリオ数。

## 5. 観察すべき点
- 充電は価格の谷、放電は山。平均充電価格 < 平均放電価格。
- η を下げると利益減（往復ロス）。容量を増やしても価格差・出力で頭打ち。
- σ を上げると「決定論 vs 完全予測」の差（予測の価値）が拡大。σ=0 で一致。

## 6. 限界・拡張
- 価格のみ不確実（需要・PV は固定）。完全な多段階 recourse は未実装（決定論=固定計画 と 完全予測=WS の2境界を提示）。
- 拡張：多段階確率的 dispatch、CVaR でのリスク回避運用、需要・PV 同時不確実。

## 7. ファイル
```
apps/battery_dispatch/
├── app.py   ← 価格・充放電・SoC・不確実性比較
├── core.py  ← dispatch LP と決定論/完全予測比較（self-test 付き）
└── README.md
```
