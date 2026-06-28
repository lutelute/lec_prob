"""
app.py — 蓄電池運用ビジュアライザ（Streamlit + Plotly）

起動:
    streamlit run apps/battery_dispatch/app.py

多時間帯の蓄電池アービトラージ（SoC ダイナミクス）を可視化し、
価格不確実性下で「決定論（予測で計画）vs 完全予測」の差を見せる。
Module 6b（二段階・VSS/EVPI）の多時間帯版の直感。数理は core.py に分離。
"""
from __future__ import annotations

import os
import sys

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core  # noqa: E402

st.set_page_config(page_title="蓄電池運用ビジュアライザ", layout="wide")

st.title("蓄電池運用ビジュアライザ — アービトラージと不確実性")
st.caption("安いとき充電・高いとき放電。SoC ダイナミクスを可視化し、価格が不確実なとき"
           "『予測で計画する（決定論）』と『完全予測』の差を見る。")

sb = st.sidebar
sb.header("蓄電池の諸元")
cap = sb.slider("容量 [MWh]", 2.0, 20.0, 10.0, 1.0)
pmax = sb.slider("最大出力 [MW]", 1.0, 8.0, 3.0, 0.5)
eff = sb.slider("往復効率 η", 0.60, 1.0, 0.90, 0.01)
sb.header("価格プロファイル")
base = sb.slider("ベース価格", 5.0, 40.0, 20.0, 1.0)
day_amp = sb.slider("日内変動の振幅", 0.0, 25.0, 12.0, 1.0)
eve_amp = sb.slider("夕方ピークの高さ", 0.0, 20.0, 8.0, 1.0)
sb.header("価格の不確実性")
sigma = sb.slider("価格予測誤差 σ", 0.0, 15.0, 6.0, 0.5)
n_scen = sb.select_slider("シナリオ数", [20, 50, 100], value=50)

prices = core.price_profile(base=base, day_amp=day_amp, eve_amp=eve_amp)
T = len(prices)
hours = np.arange(T)
res = core.optimize_dispatch(prices, cap, pmax, eff)

# --- メイン図：価格＋充放電＋SoC ---
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=hours, y=prices, name="価格", line=dict(color="#ea4335", width=2.5)),
              secondary_y=False)
fig.add_trace(go.Bar(x=hours, y=res["charge"], name="充電", marker_color="#4285f4", opacity=0.6),
              secondary_y=True)
fig.add_trace(go.Bar(x=hours, y=-res["discharge"], name="放電", marker_color="#34a853", opacity=0.6),
              secondary_y=True)
fig.add_trace(go.Scatter(x=np.arange(T + 1), y=res["soc"], name="SoC [MWh]",
                         line=dict(color="#f9ab00", width=2, dash="dot")), secondary_y=True)
fig.update_yaxes(title_text="価格", secondary_y=False)
fig.update_yaxes(title_text="充放電 [MW] / SoC [MWh]", secondary_y=True)
fig.update_xaxes(title_text="時刻 [h]")
fig.update_layout(title=f"最適アービトラージ（利益 {res['profit']:.1f}）：安い時間に充電・高い時間に放電",
                  height=430, barmode="relative", legend=dict(orientation="h", y=-0.2))
st.plotly_chart(fig, width="stretch")

m1, m2, m3 = st.columns(3)
m1.metric("アービトラージ利益", f"{res['profit']:.1f}")
m2.metric("平均充電価格", f"{(prices*res['charge']).sum()/max(res['charge'].sum(),1e-9):.1f}")
m3.metric("平均放電価格", f"{(prices*res['discharge']).sum()/max(res['discharge'].sum(),1e-9):.1f}")

# --- 不確実性の比較 ---
st.subheader("価格が不確実なとき：決定論（予測で計画）vs 完全予測")
if sigma > 0:
    comp = core.compare_under_uncertainty(prices, sigma, n_scen, cap, pmax, eff, seed=0)
    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("決定論（予測計画→実価格）", f"{comp['det_profit']:.1f}",
               help="平均価格で立てた固定スケジュールを、実際の価格シナリオに適用した平均利益（EEV相当）。")
    cc2.metric("完全予測（各シナリオ最適）", f"{comp['ws_profit']:.1f}",
               help="各シナリオの実価格を知ってから最適化した平均利益（WS相当、理想上限）。")
    cc3.metric("予測誤差のコスト = 完全予測の価値", f"{comp['gap']:.1f}",
               help="WS − 決定論。予測が完璧なら更にこれだけ稼げる（EVPI相当）。")
    # 価格シナリオの帯
    figs = go.Figure()
    for s in comp["scenarios"][:30]:
        figs.add_trace(go.Scatter(x=hours, y=s, line=dict(color="rgba(150,150,150,0.3)", width=1),
                                  showlegend=False))
    figs.add_trace(go.Scatter(x=hours, y=prices, name="予測（平均）", line=dict(color="#ea4335", width=3)))
    figs.update_layout(title="価格シナリオ（灰）と予測平均（赤）", xaxis_title="時刻 [h]",
                       yaxis_title="価格", height=320)
    st.plotly_chart(figs, width="stretch")
    st.info(
        f"**観察**：σ={sigma} の予測誤差があると、固定計画（決定論 {comp['det_profit']:.0f}）は"
        f" 完全予測（{comp['ws_profit']:.0f}）に **{comp['gap']:.0f} 及ばない**。"
        " これが Module 6b の WS−EEV ギャップ（予測の価値）の多時間帯版。"
        " 実際の運用では価格が判明するたびに再最適化（recourse）するので、両者の中間に位置する。"
    )
else:
    st.caption("σ=0（不確実性なし）では決定論＝完全予測。σ を上げると差が現れる。")

with st.expander("🎯 学習目標 と 数学", expanded=False):
    st.markdown(
        """
**学習目標**
- 蓄電池は**エネルギーの時間シフト**（安→高）で価値を生む。SoC ダイナミクスがその制約。
- 価格が不確実だと、固定計画は完全予測に劣る＝**予測誤差のコスト**（Module 6b の EVPI 直感）。

**最適化の明示**
- 決定変数：充電 $c_t$、放電 $d_t$、蓄電量 $\\mathrm{SoC}_t$。
- 不確実変数：価格 $\\xi_t$（シナリオで表現）。
- 目的：利益 $\\max \\sum_t \\xi_t (d_t - c_t)$（決定論）／期待利益（確率的）。
- 制約：$\\mathrm{SoC}_{t+1}=\\mathrm{SoC}_t+\\sqrt\\eta\\,c_t-d_t/\\sqrt\\eta$、$0\\le\\mathrm{SoC}\\le$容量、出力上限（常時満足）。
        """
    )
    st.latex(r"\max_{c,d,\mathrm{SoC}}\ \sum_t \xi_t (d_t - c_t)\quad \text{s.t.}\quad \mathrm{SoC}_{t+1}=\mathrm{SoC}_t+\sqrt\eta\,c_t-\frac{d_t}{\sqrt\eta},\ 0\le\mathrm{SoC}_t\le \bar S")

with st.expander("⚠️ よくある誤解 / ⚡ 接続", expanded=False):
    st.markdown(
        """
**誤解**：効率100%でなくても損しない → 往復効率 η<1 で η を下げると利益減（充放電ロス）。
**誤解**：予測が当たれば固定計画で十分 → 価格は外れる。再最適化(recourse)が価値を生む。
**誤解**：容量を増やせば必ず儲かる → 価格差と出力・効率の制約で頭打ち。

**接続**：Module 6b（二段階・VSS/EVPI）の多時間帯版。実務は確率的 UC・経済負荷配分の一部。
関連：`notes/06b_two_stage_stochastic_programming.md`、`apps/stochastic_optimization_comparator/`。
        """
    )

st.divider()
st.caption("数理は core.py（self-test 可）。LP は cvxpy（CLARABEL）。決定論アービトラージ＋予測誤差コストの可視化。")
