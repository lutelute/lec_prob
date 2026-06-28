"""
app.py — ベイズ更新ビジュアライザ（Streamlit + Plotly）

起動:
    streamlit run apps/bayes_visualizer/app.py

Module 1 の「基準率の誤謬」を対話的に学ぶ。保護リレー（故障 F / 警報）を題材に、
事前確率・感度・誤警報率を動かして事後確率がどう決まるかを観察する。
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

st.set_page_config(page_title="ベイズ更新ビジュアライザ", layout="wide")

st.title("ベイズ更新ビジュアライザ — 基準率の誤謬")
st.caption("保護リレー例：感度99%の優秀な警報でも、故障が稀なら『警報＝本物』とは限らない。"
           "事前・感度・誤警報率を動かして、事後確率の決まり方を体感する。")

sb = st.sidebar
sb.header("パラメータ")
prior = sb.slider("事前確率 P(F)（基準率：故障の起こりやすさ）", 0.001, 0.5, 0.01, 0.001, format="%.3f")
sens = sb.slider("感度 P(警報 | F)", 0.50, 1.0, 0.99, 0.01)
fpr = sb.slider("誤警報率 P(警報 | ¬F)（=1−特異度）", 0.001, 0.5, 0.05, 0.001, format="%.3f")
n_cases = sb.select_slider("内訳の母数 n", [100, 1000, 10000], value=1000)
n_seq = sb.slider("逐次：独立な警報の回数", 1, 6, 2)

post_pos = core.posterior_positive(prior, sens, fpr)
post_neg = core.posterior_negative(prior, sens, fpr)
cc = core.confusion_counts(n_cases, prior, sens, fpr)

# --- メトリクス ---
m1, m2, m3 = st.columns(3)
m1.metric("事後 P(F | 警報あり)", f"{post_pos:.1%}",
          help="警報が鳴ったとき実際に故障している確率。感度が高くても基準率が低いと小さい。")
m2.metric("事後 P(F | 警報なし)", f"{post_neg:.3%}",
          help="警報が鳴らなければ故障の可能性はさらに下がる。")
m3.metric("感度 P(警報|F)（比較用）", f"{sens:.0%}",
          help="これと『P(F|警報)』を混同するのが基準率の誤謬。両者は別物。")

if post_pos < 0.5 and sens >= 0.9:
    st.warning(f"⚠️ 感度 {sens:.0%} の優秀な警報でも、事後は **{post_pos:.1%}**。"
               f" 警報の多く（{cc['FP']:.0f}/{cc['alarms']:.0f} 件）は誤警報。これが**基準率の誤謬**。")

c1, c2 = st.columns(2)

# --- 1000件の内訳 ---
with c1:
    fig = go.Figure(go.Bar(
        x=["真陽性<br>故障&警報", "偽陽性<br>正常&警報", "偽陰性<br>故障&無警報", "真陰性<br>正常&無警報"],
        y=[cc["TP"], cc["FP"], cc["FN"], cc["TN"]],
        marker_color=["#34a853", "#ea4335", "#fbbc04", "#cccccc"],
        text=[f"{v:.1f}" for v in [cc["TP"], cc["FP"], cc["FN"], cc["TN"]]],
        textposition="outside"))
    fig.update_layout(
        title=f"{n_cases}件の内訳：警報{cc['alarms']:.1f}件中 本物{cc['TP']:.1f}件 → {post_pos:.1%}",
        yaxis_title=f"件数 / {n_cases}件", height=380)
    st.plotly_chart(fig, width="stretch")

# --- 事後 vs 基準率 曲線 ---
with c2:
    bs = np.linspace(0.001, 0.5, 300)
    posts = [core.posterior_positive(b, sens, fpr) for b in bs]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=bs, y=posts, mode="lines",
                              line=dict(color="#4285f4", width=3), name="P(F|警報)"))
    fig2.add_trace(go.Scatter(x=[prior], y=[post_pos], mode="markers",
                              marker=dict(color="#ea4335", size=12), name="現在"))
    fig2.add_hline(y=0.5, line=dict(color="gray", dash="dot"))
    fig2.update_layout(title="事後確率は基準率に強く依存", xaxis_title="基準率 P(F)",
                       yaxis_title="P(F | 警報)", yaxis_range=[0, 1], height=380)
    st.plotly_chart(fig2, width="stretch")

# --- 逐次更新 ---
st.subheader("逐次ベイズ更新：独立な警報を重ねる")
path = core.update_path(prior, sens, fpr, n_seq)
fig3 = go.Figure(go.Scatter(
    x=list(range(n_seq + 1)), y=path, mode="lines+markers",
    line=dict(color="#a142f4", width=3), marker=dict(size=9),
    text=[f"{p:.1%}" for p in path], textposition="top center"))
fig3.add_hline(y=0.5, line=dict(color="gray", dash="dot"), annotation_text="50%")
fig3.update_layout(xaxis_title="観測した警報の回数", yaxis_title="事後 P(F)",
                   yaxis_range=[0, 1], height=320,
                   title="独立な警報を重ねると事後確率が更新される（今日の事後＝明日の事前）")
st.plotly_chart(fig3, width="stretch")
st.info(
    f"1回の警報では {path[1]:.1%} でも、独立な警報を {n_seq} 回重ねると **{path[-1]:.1%}**。"
    " ベイズ更新では『今日の事後が明日の事前』になる。"
    " ただし**警報が独立**（共通原因がない）という仮定が要る（Module 1 §7）。"
)

with st.expander("🎯 学習目標 と 観察点", expanded=False):
    st.markdown(
        """
**学習目標**：$P(\\text{警報}|F)$（感度）と $P(F|\\text{警報})$（事後）は別物、と腹落ちさせる。

**観察点**
- **基準率 P(F) を下げる** → 事後が急落（感度99%でも事後17%）。偽陽性の母数が効く。
- **誤警報率を下げる**（特異度↑） → 低基準率では感度を上げるより事後が改善。
- **逐次更新** → 独立な複数警報で事後が跳ね上がる（1回17%→2回80%）。
- **P(F)=P(F|警報)** にならないことを、感度メトリクスと見比べて確認。
        """
    )

with st.expander("🧮 数学的な対応", expanded=False):
    st.latex(r"P(F\mid \text{警報}) = \frac{P(\text{警報}\mid F)\,P(F)}{P(\text{警報}\mid F)P(F) + P(\text{警報}\mid \neg F)P(\neg F)}")
    st.latex(r"\text{オッズ更新：}\quad \frac{P(F)}{P(\neg F)} \times \underbrace{\frac{P(\text{警報}\mid F)}{P(\text{警報}\mid\neg F)}}_{\text{尤度比 LR}^+}")
    st.caption("独立な警報 k 回で事前オッズに (LR⁺)^k を掛ける。今日の事後＝明日の事前。")

with st.expander("⚠️ よくある誤解 / ⚡ 電力への接続", expanded=False):
    st.markdown(
        """
**誤解**：感度99%の警報なら鳴れば99%本物 → 基準率が低いと事後は大きく下がる（17%等）。
**誤解**：$P(A|B)=P(B|A)$ → 一般に異なる。ベイズで反転が必要。

**電力**：保護リレーの不要動作（nuisance trip）・警報の洪水。低基準率では**誤警報率の低減（特異度）**が事後信頼度に効く。
状態推定・異常検知でも、事前（基準率）を無視すると誤判定が増える。
関連：`notes/01_events_and_probability.md` §6–7。
        """
    )

st.divider()
st.caption("数理は core.py（self-test 可）。Module 1 の基準率の誤謬・条件付き確率の対話版。")
