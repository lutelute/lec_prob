"""
app.py — PDF・CDF・区間確率ビジュアライザ（Streamlit + Plotly）

起動:
    streamlit run apps/pdf_cdf_visualizer/app.py

学習目標（このツールで体得すること）:
    1. f(x)（密度の高さ）は確率ではない。確率は区間の「面積」である。
    2. P(a≤X≤b) は PDF の面積であり、同時に CDF の差 F(b)-F(a) でもある。
    3. 連続変数では P(X=x)=0。区間を縮めると確率は0へ向かう（高さは残る）。
数理は core.py に分離（streamlit 不要で自己テスト可能）。
"""
from __future__ import annotations

import os
import sys

import numpy as np
import plotly.graph_objects as go
import streamlit as st

# `streamlit run` はスクリプトのディレクトリを sys.path に入れるが、
# テスト実行（AppTest）等では入らない。どちらでも import core できるようにする。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core  # noqa: E402

st.set_page_config(page_title="PDF・CDF・区間確率ビジュアライザ", layout="wide")

C_PDF = "#4285f4"      # 密度の曲線（青）
C_AREA = "#34a853"     # 面積＝確率（緑）
C_CDF = "#ea4335"      # 累積分布（赤）
C_PROBE = "#f9ab00"    # 点プローブ（橙）


# ---------------------------------------------------------------------------
# サイドバー：分布・パラメータ・問い方・区間
# ---------------------------------------------------------------------------
st.sidebar.header("① 分布を選ぶ")
dist_name = st.sidebar.selectbox("分布", list(core.DISTRIBUTIONS.keys()))
spec = core.DISTRIBUTIONS[dist_name]

st.sidebar.header("② パラメータ")
values: dict[str, float] = {}
for p in spec.params:
    values[p.key] = st.sidebar.slider(p.label, p.vmin, p.vmax, p.default, p.step)
dist = spec.make(values)

xmin, xmax = core.support_range(dist)
xmin = float(np.floor(xmin))
xmax = float(np.ceil(xmax))

st.sidebar.header("③ 何を問うか")
query = st.sidebar.radio(
    "確率の問い方",
    ["区間 P(a≤X≤b)", "左裾 P(X≤b)", "右裾・超過 P(X>a)"],
)

st.sidebar.header("④ 区間・閾値")
span = xmax - xmin
a_default = xmin + 0.35 * span
b_default = xmin + 0.65 * span
step = max(round(span / 200, 3), 1e-3)
a = st.sidebar.slider("a（下限／右裾の閾値）", xmin, xmax, float(round(a_default, 2)), step)
b = st.sidebar.slider("b（上限／左裾の閾値）", xmin, xmax, float(round(b_default, 2)), step)
if a > b:
    a, b = b, a

st.sidebar.header("⑤ 点プローブ（密度≠確率の実験）")
x0 = st.sidebar.slider("点 x₀", xmin, xmax, float(round((a + b) / 2, 2)), step)
eps = st.sidebar.select_slider(
    "微小半幅 ε（区間 [x₀-ε, x₀+ε]）",
    options=[5.0, 2.0, 1.0, 0.5, 0.2, 0.1, 0.05, 0.01],
    value=1.0,
)


# ---------------------------------------------------------------------------
# 計算：問い方に応じて塗る領域と確率を決める
# ---------------------------------------------------------------------------
xs = core.grid(dist, n=700)
pdf = dist.pdf(xs)
cdf = dist.cdf(xs)

if query.startswith("区間"):
    lo, hi = a, b
    prob = core.interval_prob_cdf(dist, lo, hi)
    formula = r"P(a \le X \le b) = F(b) - F(a) = \int_a^b f(x)\,dx"
    label = f"P({lo:.2f} ≤ X ≤ {hi:.2f})"
elif query.startswith("左裾"):
    lo, hi = xmin, b
    prob = float(dist.cdf(b))
    formula = r"P(X \le b) = F(b) = \int_{-\infty}^{b} f(x)\,dx"
    label = f"P(X ≤ {b:.2f})"
else:  # 右裾・超過
    lo, hi = a, xmax
    prob = float(1.0 - dist.cdf(a))
    formula = r"P(X > a) = 1 - F(a) = \int_{a}^{\infty} f(x)\,dx"
    label = f"P(X > {a:.2f})"

prob_area = core.interval_prob_area(dist, lo, hi)


# ---------------------------------------------------------------------------
# 図1：PDF（密度）＋ 塗りつぶし面積 ＋ 点プローブ
# ---------------------------------------------------------------------------
def make_pdf_fig() -> go.Figure:
    fig = go.Figure()
    # 密度曲線
    fig.add_trace(go.Scatter(x=xs, y=pdf, mode="lines",
                             line=dict(color=C_PDF, width=3), name="密度 f(x)"))
    # 確率＝面積（塗りつぶし）
    mask = (xs >= lo) & (xs <= hi)
    fig.add_trace(go.Scatter(
        x=xs[mask], y=pdf[mask], mode="lines", fill="tozeroy",
        line=dict(color=C_AREA, width=0), fillcolor="rgba(52,168,83,0.35)",
        name=f"面積 = {label}"))
    # 点プローブ：高さ f(x0) を縦線で（これは確率ではない）
    f_x0 = float(dist.pdf(x0))
    fig.add_trace(go.Scatter(
        x=[x0, x0], y=[0, f_x0], mode="lines+markers",
        line=dict(color=C_PROBE, width=2, dash="dot"),
        marker=dict(size=8), name=f"高さ f(x₀)={f_x0:.4f}"))
    fig.add_annotation(x=x0, y=f_x0, text=f"f(x₀)={f_x0:.4f}<br>（高さ＝確率ではない）",
                       showarrow=True, arrowhead=2, ax=40, ay=-40,
                       font=dict(color=C_PROBE))
    fig.update_layout(
        title="PDF：確率は『面積』、密度は『高さ』",
        xaxis_title="x", yaxis_title="確率密度 f(x)",
        height=430, margin=dict(t=50, b=40), legend=dict(orientation="h", y=-0.2))
    return fig


# ---------------------------------------------------------------------------
# 図2：CDF（累積）＋ 同じ確率を「縦の差」として表示
# ---------------------------------------------------------------------------
def make_cdf_fig() -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=cdf, mode="lines",
                             line=dict(color=C_CDF, width=3), name="累積 F(x)"))
    Fa, Fb = float(dist.cdf(lo)), float(dist.cdf(hi))
    # F(lo), F(hi) の水平線と点
    for xv, Fv, name in [(lo, Fa, "F(a)"), (hi, Fb, "F(b)")]:
        fig.add_trace(go.Scatter(x=[xmin, xv], y=[Fv, Fv], mode="lines",
                                 line=dict(color="gray", width=1, dash="dot"),
                                 showlegend=False))
        fig.add_trace(go.Scatter(x=[xv], y=[Fv], mode="markers",
                                 marker=dict(color=C_CDF, size=9),
                                 name=f"{name}={Fv:.3f}"))
    # 確率＝縦の差（F(hi)-F(lo)）を矢印で
    fig.add_trace(go.Scatter(x=[xmin + 0.02 * span, xmin + 0.02 * span],
                             y=[Fa, Fb], mode="lines",
                             line=dict(color=C_AREA, width=6),
                             name=f"差 = {prob:.4f}"))
    fig.add_annotation(x=xmin + 0.02 * span, y=(Fa + Fb) / 2,
                       text=f"高さの差<br>= {prob:.4f}", showarrow=True,
                       arrowhead=2, ax=60, ay=0, font=dict(color=C_AREA))
    fig.update_layout(
        title="CDF：同じ確率が『縦の高さの差』として現れる",
        xaxis_title="x", yaxis_title="累積確率 F(x)", yaxis_range=[-0.03, 1.03],
        height=430, margin=dict(t=50, b=40), legend=dict(orientation="h", y=-0.2))
    return fig


# ---------------------------------------------------------------------------
# メイン
# ---------------------------------------------------------------------------
st.title("PDF・CDF・区間確率ビジュアライザ")
st.caption("確率は密度の『高さ』ではなく区間の『面積』。その面積は CDF の『差』でもある——を体で覚えるツール。")

m1, m2, m3 = st.columns(3)
m1.metric(label, f"{prob:.4f}")
m2.metric("同じ確率（PDF を数値積分した面積）", f"{prob_area:.4f}",
          help="CDF 差と一致するはず。ズレがほぼ0なら『面積＝CDF差』を確認できた。")
m3.metric("|CDF差 − 面積|（一致の検証）", f"{abs(prob - prob_area):.2e}")

st.latex(formula)

c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(make_pdf_fig(), width="stretch")
with c2:
    st.plotly_chart(make_cdf_fig(), width="stretch")

# --- 点プローブの実験パネル ---
st.subheader("実験：密度の高さ vs 点まわりの確率")
demo = core.point_interval_demo(dist, x0, eps)
d1, d2, d3 = st.columns(3)
d1.metric("密度の高さ f(x₀)", f"{demo['f_height']:.4f}",
          help="x₀ をどこに置いても、これは確率ではない（1を超えることもある）。")
d2.metric(f"P(x₀-ε ≤ X ≤ x₀+ε)  (ε={eps})", f"{demo['p_interval']:.5f}",
          help="ε を小さくすると0へ向かう。点 P(X=x₀)=0 の意味。")
d3.metric("近似 f(x₀)·2ε", f"{demo['approx']:.5f}",
          help="微小区間では『面積 ≒ 高さ × 幅』。だから密度は『単位幅あたりの確率』。")
st.info(
    "**観察**：ε を 5 → 0.01 と小さくすると、真ん中（区間確率）は 0 に近づくのに、"
    "左（密度の高さ）は変わりません。**高さは確率ではなく、幅を掛けて初めて確率（面積）になる**。"
    "これが『連続変数で P(X=x)=0 なのに X は必ず何かの値をとる』の数理です。"
)

# ---------------------------------------------------------------------------
# 学習用の解説（折りたたみ）
# ---------------------------------------------------------------------------
with st.expander("🎯 学習目標 と 観察すべき点", expanded=False):
    st.markdown(
        """
**学習目標**
1. 密度 f(x)（高さ）と確率（面積）を取り違えない。
2. `P(a≤X≤b)` が **PDF の面積** であり **CDF の差 F(b)−F(a)** でもあると分かる。
3. 区間を縮めると確率→0（点の確率は0）。密度は残る。

**観察すべき点**
- σ（正規）を大きくすると山は**低く広く**なる。高さ（密度）が下がっても全面積は常に1。
- 「左裾 / 右裾」を切り替えると、CDF 上では F(b)（左裾）と 1−F(a)（右裾・超過）に対応。
- 一様分布で a,b を広げると密度の高さ 1/(b−a) が下がる：**広い区間ほど1点の密度は低い**。
        """
    )

with st.expander("🧮 数学的な対応式", expanded=False):
    st.markdown("**PDF・CDF・区間確率の関係**")
    st.latex(r"F_X(x) = P(X \le x) = \int_{-\infty}^{x} f_X(t)\,dt, \qquad f_X(x) = \frac{d}{dx}F_X(x)")
    st.latex(r"P(a \le X \le b) = \int_a^b f_X(x)\,dx = F_X(b) - F_X(a)")
    st.latex(r"P(X = x) = \int_x^x f_X(t)\,dt = 0 \quad(\text{連続変数})")
    st.markdown("**微小区間の近似（なぜ密度を『密度』と呼ぶか）**")
    st.latex(r"P(x_0 - \varepsilon \le X \le x_0 + \varepsilon) \approx f_X(x_0)\cdot 2\varepsilon")
    st.caption("→ f(x) は『単位幅あたりの確率』。だから高さ自体は確率でなく、幅を掛けて面積にして初めて確率。")

with st.expander("⚠️ よくある誤解", expanded=False):
    st.markdown(
        """
| 誤解 | 正しい理解 |
|---|---|
| f(x) は「x が出る確率」 | f(x) は密度（高さ）。確率は区間の面積。 |
| 密度は1以下のはず | 密度は1を超えてよい（例：σが小さい正規、狭い一様）。面積が1。 |
| P(X=x) は小さいが正 | 連続変数では厳密に0。 |
| `≤` と `<` で確率が変わる | 連続変数では P(X=a)=0 なので `P(a≤X≤b)=P(a<X<b)`。 |
| CDF と PDF は別の情報 | 同じ情報の別表現。PDF を積分→CDF、CDF を微分→PDF。 |
        """
    )

with st.expander("✏️ ミニ演習（ヒント付き）", expanded=False):
    st.markdown(
        """
1. 正規分布 μ=100, σ=15 で、`P(85 ≤ X ≤ 115)` はおよそいくつ？
   <details><summary>ヒント</summary>μ±1σ の区間。約 0.68。スライダーで a=85, b=115 にして確認。</details>
2. 同じ分布で「右裾・超過」を選び、`P(X > 130)`（=2σ 超え）を読め。
   <details><summary>ヒント</summary>片側 2σ 超過は約 0.023。容量130万kWの超過確率と読める。</details>
3. 一様 U(60,140) で密度の高さは？　区間を U(60,100) に狭めると高さは？
   <details><summary>ヒント</summary>1/(140−60)=1/80=0.0125 → 1/40=0.025。狭いほど高い。</details>
4. 点プローブで ε を 1 → 0.01 にすると区間確率は約何分の1になる？
   <details><summary>ヒント</summary>幅が 1/100 なので確率もおよそ 1/100。面積≒高さ×幅だから。</details>
        """,
        unsafe_allow_html=True,
    )

with st.expander("⚡ 電力・エネルギーへの接続", expanded=False):
    st.markdown(f"**この分布の電力的な読み替え**：{spec.power_reading}")
    st.markdown(spec.note)
    st.markdown(
        """
- **超過確率**：`P(X > 容量)` は供給支障・制約違反の確率。右裾の面積そのもの。
  → Module 6 の**チャンス制約** `P(g(x,ξ)≤0) ≥ 1−ε` は、まさにこの面積を ε 以下に抑える話。
- **分位点**：CDF を逆に読むと「90%の日はこの需要以下」という設計値（VaR）になる。
- **裾の重さ**：対数正規は右に重い裾をもつ。正規で価格や需要を近似すると、**スパイク（極端事象）を過小評価**しがち。Module 3・4 で再訪。
        """
    )

st.divider()
st.caption(
    "関連ノート: notes/02_random_variables_and_distributions.md（密度≠確率の本論）／ "
    "notes/01_events_and_probability.md（確率0≠不可能）／ roadmap/notation.md（記号）。"
)
