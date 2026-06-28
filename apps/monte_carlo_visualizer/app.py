"""
app.py — モンテカルロ収束ビジュアライザ（Streamlit + Plotly）

起動:
    streamlit run apps/monte_carlo_visualizer/app.py

Module 5 の「平均は速く・尾（希少事象）は遅い」「SAA はシナリオ数で収束」を対話的に。
数理は core.py に分離。
"""
from __future__ import annotations

import os
import sys

import numpy as np
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core  # noqa: E402

st.set_page_config(page_title="モンテカルロ収束ビジュアライザ", layout="wide")

st.title("モンテカルロ収束ビジュアライザ")
st.caption("平均は 1/√N で速く収束、希少事象（尾）は遅い。SAA はシナリオ数で最適解が収束する——を体感する。")

sb = st.sidebar
sb.header("分布")
mean = sb.slider("平均 μ", 50.0, 150.0, 100.0, 1.0)
std = sb.slider("標準偏差 σ", 1.0, 40.0, 15.0, 1.0)
kind = sb.selectbox("分布", ["normal", "lognormal"],
                    format_func=lambda s: {"normal": "正規", "lognormal": "対数正規(右裾)"}[s])
sb.header("実験の種類")
mode = sb.radio("推定対象", ["期待値 E[X] の収束", "希少事象 P(X>c)", "SAA：容量問題の最適 q"])
seed = sb.number_input("乱数シード", 0, 9999, 42, 1)

dist = core.make_dist(mean, std, kind)

if mode.startswith("期待値"):
    n_max = sb.select_slider("最大サンプル数 N", [1000, 10000, 50000, 200000], value=50000)
    r = core.estimate_expectation(dist, n_max, seed)
    ns = np.arange(1, n_max + 1)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ns, y=r["estimate"], mode="lines",
                             line=dict(color="#4285f4", width=1.2), name="逐次推定"))
    fig.add_trace(go.Scatter(x=ns, y=r["estimate"] + r["ci"], mode="lines",
                             line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=ns, y=r["estimate"] - r["ci"], mode="lines", fill="tonexty",
                             line=dict(width=0), fillcolor="rgba(66,133,244,0.15)", name="95%CI"))
    fig.add_hline(y=r["true"], line=dict(color="#ea4335", dash="dash"),
                  annotation_text=f"真値 {r['true']:.2f}")
    fig.update_xaxes(type="log", title="サンプル数 N（対数）")
    fig.update_yaxes(title="E[X] の推定", range=[r["true"] - 8, r["true"] + 8])
    fig.update_layout(height=460, title="逐次推定と95%CI（N×100 で CI 幅 ÷10）")
    st.plotly_chart(fig, width="stretch")
    c1, c2 = st.columns(2)
    c1.metric("最終推定値", f"{r['estimate'][-1]:.3f}", help=f"真値 {r['true']:.2f}")
    c2.metric("95%CI 半幅（N最大）", f"±{r['ci'][-1]:.3f}", help="1/√N で縮む")
    st.info("**観察**：CI 幅は $1/\\sqrt N$。精度10倍にはサンプル100倍。点推定だけでなく必ず CI を添える。")

elif mode.startswith("希少事象"):
    c = sb.slider("閾値 c（超過確率を推定）", float(mean), float(mean + 4 * std),
                  float(mean + 3 * std), 1.0)
    Ns = [300, 1000, 3000, 10000, 30000, 100000, 300000, 1000000]
    e = core.estimate_exceedance(dist, c, Ns, seed)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Ns, y=e["estimates"], mode="lines+markers",
                             line=dict(color="#a142f4", width=2), name="MC推定"))
    fig.add_hline(y=e["true"], line=dict(color="#ea4335", dash="dash"),
                  annotation_text=f"真値 {e['true']:.5f}")
    fig.update_xaxes(type="log", title="サンプル数 N（対数）")
    fig.update_yaxes(title=f"P(X>{c:.0f}) の推定")
    fig.update_layout(height=440, title="希少事象は小Nで不安定（0ヒットで確率0と誤推定も）")
    st.plotly_chart(fig, width="stretch")
    st.dataframe([{"N": n, "ヒット数": h, "推定値": round(es, 6)}
                  for n, h, es in zip(e["Ns"], e["hits"], e["estimates"])],
                 width="stretch", hide_index=True)
    st.warning(f"真値 P(X>{c:.0f})={e['true']:.5f}。小Nでヒット0なら**確率0と誤推定**。"
               f" 安定推定にはおおむね $\\gtrsim$ 数十/p ≈ {int(30/max(e['true'],1e-9)):,} サンプルが目安。")

else:  # SAA
    cs = sb.slider("不足単価 c_s", 1.0, 20.0, 10.0, 1.0)
    co = sb.slider("過剰単価 c_o", 1.0, 20.0, 1.0, 1.0)
    Ns = [10, 20, 50, 100, 300, 1000, 3000, 10000]
    s = core.saa_newsvendor(dist, cs, co, Ns, seed)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Ns, y=s["q_hat"], mode="lines+markers",
                             line=dict(color="#34a853", width=2), name="SAA q̂"))
    fig.add_hline(y=s["true"], line=dict(color="#ea4335", dash="dash"),
                  annotation_text=f"真の最適 {s['true']:.2f}")
    fig.update_xaxes(type="log", title="シナリオ数 N（対数）")
    fig.update_yaxes(title="SAA 最適容量 q̂")
    fig.update_layout(height=440, title="SAA：シナリオ数で最適解が臨界分位点へ収束")
    st.plotly_chart(fig, width="stretch")
    st.info(f"真の最適 q* = 臨界比 {cs/(cs+co):.3f} 分位点 = {s['true']:.2f}（Module 0 の連続版）。"
            " 少シナリオでは q̂ がぶれる＝**有限シナリオの不確実性**。")

with st.expander("🎯 学習目標 と 数学", expanded=False):
    st.markdown("**学習目標**：① 平均の収束 $1/\\sqrt N$ ② 希少事象の難しさ（$\\sim1/p$ サンプル）③ SAA の収束。")
    st.latex(r"\mathrm{SE}(\hat\theta_N)=\frac{\sigma}{\sqrt N},\qquad \hat\theta_N\xrightarrow{N\to\infty}\theta")
    st.caption("関連：notes/05_scenarios_and_monte_carlo.md。希少事象は重点サンプリング/層別/極値理論で対処。")

st.divider()
st.caption("数理は core.py（self-test 可）。Module 5：シナリオとモンテカルロの対話版。")
