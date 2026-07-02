# 確率的最適化コンパレータ（capstone）

本教材の**到達点**。同じ容量調達問題（newsvendor 型）を **6つの最適化形式**で解き、
最適決定 $x^\*$ と評価指標（期待費用・不足確率・CVaR）の違いを1画面で比較します。
パラメータを動かしながら、**「なぜこの形式を選ぶのか」**を自分の言葉で言えるようにするためのツールです。

関連ノート：[`notes/06_optimization_under_uncertainty.md`](../../notes/06_optimization_under_uncertainty.md)、
[`roadmap/optimization_map.md`](../../roadmap/optimization_map.md)。

---

## 1. 統一問題

$$
C(x,\xi)=c_s\max(\xi-x,0)+c_o\max(x-\xi,0),\qquad \xi\sim \text{需要分布（正規/対数正規）}.
$$

不足単価 $c_s$ ≫ 過剰単価 $c_o$ の**非対称性**が、形式ごとに違う $x^\*$ を生みます。

## 2. 6形式（同じ問題、違う決定）

| 形式 | 最適化対象 | x* の決まり方 |
|---|---|---|
| ①決定論 | 1点（平均） | $x=\mu$ |
| ②期待値最小化 | 平均費用 | 臨界分位点 $F^{-1}(c_s/(c_s+c_o))$ |
| ③ロバスト | 区間内最悪値 | $(c_s\overline\xi+c_o\underline\xi)/(c_s+c_o)$ |
| ④チャンス制約 | 違反確率 ≤ ε | $F^{-1}(1-\varepsilon)$ |
| ⑤CVaR最小化 | 尾部の平均 | Rockafellar–Uryasev（cvxpy/SAA） |
| ⑥分布ロバスト | 最悪分布の期待値 | Scarf（平均・分散） |

既定パラメータ（$\mu=100,\sigma=15,c_s=10,c_o=1,\varepsilon=0.1,\alpha=0.9$）での代表値：

```
①決定論 100.0 | ④チャンス 119.2 | ②期待値 120.0 | ⑥DRO 121.4 | ⑤CVaR 130.2 | ③ロバスト 136.8
   ←―― 平均重視・楽観・安 ――|―― 尾部/最悪重視・保守・高 ――→
```

各形式は**自分の目的では最良**（②は E[費用] 最小、⑤は CVaR 最小、④は不足確率≈ε）。
①決定論は平均すら最小化しない（非対称コストを無視するため）。

## 3. 実行方法

```bash
python3 -m venv --system-site-packages .venv && source .venv/bin/activate
pip install streamlit cvxpy           # まだなら
streamlit run apps/stochastic_optimization_comparator/app.py
```

数理コアの自己テスト（Streamlit 不要、第6章 §8 の検証値を再現）：

```bash
python3 apps/stochastic_optimization_comparator/core.py
```

依存：`numpy`, `scipy`, `cvxpy`, `plotly`, `streamlit`。
（cvxpy が無くても CVaR はグリッド探索でフォールバック動作します。）

## 4. 操作できるパラメータ

| パラメータ | 効果（観察ポイント） |
|---|---|
| μ, σ | 需要の中心・広がり |
| 分布（正規/対数正規） | 右裾の重さ → CVaR/チャンスの x* が上振れ |
| c_s, c_o | **非対称性**。1:1 に近づけると全形式が μ へ集まる |
| ε（チャンス） | 小さくすると x* 上昇（安全側） |
| α（CVaR） | 上げると x* 上昇（深い尾部を抑制） |
| k（ロバスト幅 ±kσ） | 広げると x* 急上昇（過度に保守的） |
| N（シナリオ数） | SAA/評価の精度 |

## 5. よくある誤解（アプリ内にも掲載）

- ロバストが常に最良 → 過度に保守的で高コスト。保守性は価値判断。
- 期待値最小化なら安心 → 平均は尾部に鈍感。稀な大損は CVaR/チャンスで。
- チャンス制約と CVaR は同じ → 前者は違反“確率”、後者は違反の“深さ”（CVaR は凸）。
- ロバスト＝分布ロバスト → 前者は確率なしの集合最悪、後者は分布族の最悪期待値。

## 6. 電力への接続

UC＝二段階/ロバスト、蓄電池＝期待値/CVaR、OPF＝チャンス制約、予備力＝チャンス/CVaR、出力抑制＝ロバスト/DRO。
実務は複数形式を解いて比較（Roald et al. 2023）。

## 7. ファイル構成

```
apps/stochastic_optimization_comparator/
├── app.py    ← Streamlit UI（決定マップ・評価表・解説）
├── core.py   ← 6形式の x* と評価（cvxpy）。self-test 付き、streamlit 非依存
├── SPEC.md   ← 設計仕様・受け入れ基準・拡張案
└── README.md ← 本ファイル
```
