"""
app.py — 確率的最適化コンパレータ（Streamlit + Plotly）

起動:
    streamlit run apps/stochastic_optimization_comparator/app.py

同じ容量調達問題を6形式（決定論/期待値/ロバスト/チャンス制約/CVaR/分布ロバスト）で解き、
最適決定 x* と評価指標（期待費用・不足確率・CVaR）の違いを1画面で比較する。
本教材の到達点：「なぜこの形式を選ぶか」をパラメータを動かして体感する。
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

st.set_page_config(page_title="確率的最適化コンパレータ", layout="wide")

# 形式ごとの色（保守性：青=楽観 → 赤=保守）
COLORS = {
    "①決定論": "#9aa0a6",
    "②期待値最小化": "#4285f4",
    "④チャンス制約": "#34a853",
    "⑥分布ロバスト": "#a142f4",
    "⑤CVaR最小化": "#f9ab00",
    "③ロバスト": "#ea4335",
}

st.title("確率的最適化コンパレータ")
st.caption("同じ容量調達問題を6形式で解く。決定 x* がどう変わるかで「なぜこの形式を選ぶか」を学ぶ。")

# ---------------------------------------------------------------------------
# サイドバー
# ---------------------------------------------------------------------------
sb = st.sidebar
sb.header("問題設定")
mean = sb.slider("需要の平均 μ", 50.0, 150.0, 100.0, 1.0)
std = sb.slider("需要の標準偏差 σ", 1.0, 40.0, 15.0, 1.0)
kind = sb.selectbox("需要の分布", ["normal", "lognormal"],
                    format_func=lambda s: {"normal": "正規", "lognormal": "対数正規(右裾)"}[s])
sb.header("コスト（非対称性が鍵）")
cs = sb.slider("不足の単価 c_s", 1.0, 20.0, 10.0, 1.0)
co = sb.slider("過剰の単価 c_o", 1.0, 20.0, 1.0, 1.0)
sb.header("リスクのパラメータ")
eps = sb.slider("チャンス制約 ε（許容不足確率）", 0.01, 0.30, 0.10, 0.01)
alpha = sb.slider("CVaR 信頼水準 α", 0.50, 0.99, 0.90, 0.01)
k_robust = sb.slider("ロバスト集合の幅 k（±kσ）", 1.0, 4.0, 3.0, 0.5)
n_samples = sb.select_slider("シナリオ数 N（SAA/評価）", [2000, 5000, 20000, 50000], value=20000)

res = core.solve_all(mean=mean, std=std, cs=cs, co=co, eps=eps, alpha=alpha,
                     k_robust=k_robust, kind=kind, n_samples=n_samples, seed=0)
order = ["①決定論", "②期待値最小化", "④チャンス制約", "⑥分布ロバスト", "⑤CVaR最小化", "③ロバスト"]
res = sorted(res, key=lambda r: order.index(r.name))
dist = core.make_dist(mean, std, kind)

# 「各指標のベスト」を判定
best_ec = min(res, key=lambda r: r.expected_cost).name
best_cv = min(res, key=lambda r: r.cvar).name

# ---------------------------------------------------------------------------
# 上段：決定マップ（x* を需要分布の上に重ねる）
# ---------------------------------------------------------------------------
c1, c2 = st.columns([3, 2])

with c1:
    xs = np.linspace(dist.ppf(0.001), dist.ppf(0.999), 400)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=dist.pdf(xs), mode="lines",
                             line=dict(color="#bbb", width=2), name="需要 ξ の分布", fill="tozeroy",
                             fillcolor="rgba(180,180,180,0.15)"))
    ymax = float(dist.pdf(xs).max())
    for r in res:
        fig.add_trace(go.Scatter(
            x=[r.x, r.x], y=[0, ymax * 1.05], mode="lines",
            line=dict(color=COLORS[r.name], width=2.5),
            name=f"{r.name}: x*={r.x:.1f}"))
    fig.update_layout(title="決定マップ：6形式の最適容量 x* を需要分布上に表示",
                      xaxis_title="容量 x / 需要 ξ", yaxis_title="密度",
                      height=420, legend=dict(font=dict(size=10)))
    st.plotly_chart(fig, width="stretch")

with c2:
    # x* の棒（保守性の順）
    fig2 = go.Figure(go.Bar(
        x=[r.x for r in res], y=[r.name for r in res], orientation="h",
        marker_color=[COLORS[r.name] for r in res],
        text=[f"{r.x:.1f}" for r in res], textposition="outside"))
    fig2.update_layout(title="最適決定 x*（上ほど楽観/安、下ほど保守/高）",
                       xaxis_title="x*", height=420, margin=dict(l=10))
    st.plotly_chart(fig2, width="stretch")

# ---------------------------------------------------------------------------
# 中段：評価表
# ---------------------------------------------------------------------------
st.subheader("評価：同じサンプルで各 x* を採点")
rows = []
for r in res:
    rows.append({
        "形式": r.name,
        "最適 x*": round(r.x, 2),
        "期待費用 E[C]": round(r.expected_cost, 2),
        "不足確率 P(ξ>x)": round(r.shortage_prob, 3),
        f"CVaR_{alpha:.2f}": round(r.cvar, 2),
        "ねらい": r.note,
    })
st.dataframe(rows, width="stretch", hide_index=True)
st.success(
    f"**期待費用が最小**：{best_ec}（定義どおり②が平均を最小化）／ "
    f"**CVaR が最小**：{best_cv}（⑤が尾部を最小化）／ "
    f"**不足確率**：④はほぼ ε={eps} に一致、③は最小（最も安全だが高コスト）。"
)
st.info(
    "**各形式は『自分の目的』では最良だが、他指標では譲る**。これが「どれを選ぶか＝価値判断」の核心。"
    " 例えば①決定論は平均すら最小化しない（非対称コストを無視するため）。"
)

# ---------------------------------------------------------------------------
# 解説
# ---------------------------------------------------------------------------
with st.expander("🎯 学習目標 と 観察すべき点", expanded=False):
    st.markdown(
        """
**学習目標**：同じ問題で形式を変えると決定 x* がどう動くかを体感し、「なぜこの形式か」を言語化する。

**観察すべき点**
- **c_s/c_o（非対称性）を 1 に近づける** → 全形式が μ へ集まる（Module 0 の罠が消える）。
- **ε を小さく** → チャンス制約の x* が上昇（より安全側）。
- **α を上げる** → CVaR の x* が上昇（より深い尾部を抑える）。
- **k（ロバスト幅）を広げる** → ロバストの x* が急上昇（過度に保守的）。
- **分布を対数正規に** → 右裾が重く、CVaR/チャンスの x* が上振れ（裾の効果）。
        """
    )

with st.expander("🧭 どの形式を選ぶか", expanded=False):
    st.markdown(
        """
| 重視すること | 形式 |
|---|---|
| 不確実性が小さい/対称 | ①決定論 |
| 平均費用（多数回運用） | ②期待値最小化 |
| 分布を仮定したくない/最悪に必ず備える | ③ロバスト |
| 制約遵守の確率（信頼度規格） | ④チャンス制約 |
| 破滅的損失（尾部）の回避 | ⑤CVaR |
| データ少・分布形が不確か（平均分散は既知） | ⑥分布ロバスト |

実務では**複数形式を解いて比較**するのが正攻法（Roald et al. 2023）。
        """
    )

with st.expander("🧮 数学的な対応", expanded=False):
    st.latex(r"C(x,\xi)=c_s\max(\xi-x,0)+c_o\max(x-\xi,0)")
    st.latex(r"\text{②}\ \min_x E[C]\quad \text{③}\ \min_x\max_{\xi\in\mathcal U}C\quad \text{④}\ P(\xi>x)\le\varepsilon")
    st.latex(r"\text{⑤}\ \min_{x,\eta}\Big\{\eta+\tfrac{1}{1-\alpha}E[(C-\eta)^+]\Big\}\quad \text{⑥}\ \min_x\sup_{\mathbb P\in\mathcal P}E_{\mathbb P}[C]")
    st.caption("②=分位点, ③=区間最悪, ④=超過確率, ⑤=Rockafellar–Uryasev, ⑥=Scarf(平均・分散)。")

with st.expander("⚠️ よくある誤解 / ⚡ 電力への接続", expanded=False):
    st.markdown(
        """
**誤解**：ロバストが常に最良 → 過度に保守的で高コスト。保守性は価値判断。
**誤解**：チャンス制約と CVaR は同じ → 前者は違反“確率”、後者は違反の“深さ”（凸で解きやすい）。

**電力**：UC＝二段階/ロバスト、蓄電池＝期待値/CVaR、OPF＝チャンス制約、予備力＝チャンス/CVaR、出力抑制＝ロバスト/DRO。
関連ノート：`notes/06_optimization_under_uncertainty.md`、`roadmap/optimization_map.md`。
        """
    )

st.divider()
st.caption("統一問題＝容量調達(newsvendor)。c_s≫c_o の非対称性が形式間の決定差を生む。数理は core.py（self-test 可）。")
