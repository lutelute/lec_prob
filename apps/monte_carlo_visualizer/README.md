# モンテカルロ収束ビジュアライザ

第5章の核心——**平均は $1/\sqrt N$ で速く収束、希少事象（尾）は遅い、SAA はシナリオ数で収束**——を
対話的に体感するツールです。

関連ノート：[`notes/05_scenarios_and_monte_carlo.md`](../../notes/05_scenarios_and_monte_carlo.md)。

## 1. 3つの実験モード

| モード | 何を見るか | 学び |
|---|---|---|
| 期待値 E[X] の収束 | 逐次推定＋95%CI が真値へ | CI 幅は $1/\sqrt N$。点推定に CI を添える |
| 希少事象 P(X>c) | 各 N での推定とヒット数 | 小Nで0ヒット＝確率0と誤推定。$\sim$数十/p 必要 |
| SAA：容量問題の最適 q | シナリオ数で q̂ が臨界分位点へ | 少シナリオは決定がぶれる |

## 2. 実行

```bash
streamlit run apps/monte_carlo_visualizer/app.py
python3 apps/monte_carlo_visualizer/core.py   # 自己テスト
```
依存：`numpy`, `scipy`, `plotly`, `streamlit`。

## 3. 操作パラメータ
分布（正規/対数正規）、μ, σ、実験モード、閾値 c（希少事象）、c_s/c_o（SAA）、最大N、シード。

## 4. 観察すべき点
- 期待値：N×100 で CI 幅が ÷10。対数正規にすると分散大で収束が遅い。
- 希少事象：c を上げると真値 p が小さくなり、必要 N が急増（小Nでヒット0）。
- SAA：N が小さいと q̂ が大きくぶれる＝有限シナリオの不確実性。

## 5. 数学

$$\mathrm{SE}(\hat\theta_N)=\sigma/\sqrt N,\qquad \hat\theta_N\to\theta\ (N\to\infty).$$

希少事象は重点サンプリング・層別・極値理論で対処（ノート §5）。

## 6. ファイル
```
apps/monte_carlo_visualizer/
├── app.py   ← 3モードの収束図
├── core.py  ← 推定ロジック（self-test 付き）
└── README.md
```
