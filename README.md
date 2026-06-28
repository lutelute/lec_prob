# lec_prob — 確率・確率分布・確率的最適化の段階的学習環境

> **一言で言うと**：確率を「答えを出す計算手法」ではなく、
> **「何を不確実な量としてモデル化し、どの確率表現と最適化形式を選び、その選択が意思決定へどう影響するか」を説明できるようになるための言語**として学ぶ教材群です。

> **🚀 はじめての方へ**
> - **▶ インストール不要・ブラウザですぐ動くインタラクティブ・ツール5本**：[ツール一覧](interactive/index.md)
>   — PDF/CDF・ベイズ更新・モンテカルロ収束・6形式コンパレータ・蓄電池運用。スライダーで即時更新。
> - **体系的に学ぶ最短ルート**：[Module 0：なぜ確率が必要か](notes/00_why_probability.md)（平均で計画する罠を体感）→ [学習地図](roadmap/learning_map.md)（全体像）→ 到達点の[6形式コンパレータ](interactive/index.md)で **同じ問題の最適決定が形式により 100〜137 と変わる**ことを確かめる。
>
> この教材の「合格」＝同じ意思決定問題を 決定論／期待値／ロバスト／チャンス制約／CVaR／分布ロバスト で比較し、**「なぜこの形式を選ぶか」を自分の言葉で説明できる**こと。

---

## 1. この教材は誰のためか

- 確率の基礎（事象・確率変数・分布・期待値）に不安が残っている。
- けれども将来は **電力・エネルギーシステム、制御、最適化、データ解析** に確率を応用したい。
- 公式を暗記して問題を解くのではなく、**「なぜその確率表現を選ぶのか」を自分の言葉で語れる**ようになりたい。

そういう学習者を主対象にしています。数式は使いますが、**必ず直感・図・小さな数値例を先に置き、式はその後**に出します。

---

## 2. この教材が一貫して問い続けること

すべてのノート・ツール・演習は、最終的に次の5つの問いに答えるために存在します。

1. **何が不確実なのか。** （需要か、PV出力か、価格か、故障か）
2. **その不確実性を、どの言語で表すべきか。** — 事象 / 確率変数 / 確率分布 / 有限シナリオ / 不確実性集合 のどれか。
3. **何を「良い結果」とみなすのか。** — 平均的な性能 / 最悪ケース / 制約違反確率 / 尾部リスク のどれを重視するか。
4. **その選択は、数式上どこに現れるのか。** — 目的関数 / 制約 / 分布仮定 のどれを変えるのか。
5. **その代償は何か。** — 必要なデータ、計算量、保守性（過度な安全余裕）、仮定が崩れたときの脆さ。

> この5問は、各ノートの冒頭にも再掲されます。迷ったらここに戻ってください。

---

## 3. 学習の全体像（モジュール構成）

| Module | テーマ | 中心的な問い | 状態 |
|---|---|---|---|
| **0** | なぜ確率が必要か | 決定論モデルはいつ壊れるか | ✅ ノート・演習・図 |
| **1** | 事象と確率 | 事象と確率変数は何が違うか | ✅ ノート・演習・図 |
| **2** | 確率変数と分布 | 密度の高さと確率は何が違うか | ✅ ノート・解答・図・ツール |
| **3** | 期待値・分散・相関 | 平均が同じでもリスクが違うとは | ✅ ノート・解答・図 |
| **4** | データから分布へ | 観測値と真の分布は何が違うか | ✅ ノート・解答・図・データ |
| **5** | シナリオとモンテカルロ | 分布を捨てているのか近似か | ✅ ノート・解答・図 |
| **6** | 不確実性下の最適化 | 期待値/最悪値/確率/尾部のどれを最適化するか | ✅ ノート・解答・図・**比較ツール** |

各 `notes/0X_*.md`／`exercises/solutions/0X_*_solutions.md`／`figures/0X_*.svg` が対応。
依存関係の図は [`roadmap/learning_map.md`](roadmap/learning_map.md) を参照してください。

**Deep-dive**：`notes/06b_two_stage_stochastic_programming.md` — 二段階確率計画（recourse）と「確率的にする価値」VSS・EVPI を、蓄電池つき日前調達の worked example（cvxpy 検証）で扱う。

> **全7モジュールのノート・解答・図、および到達点の「6形式比較ツール」まで実装・検証済み**（各数値は Python/cvxpy で検証）。進捗の詳細は [`development_log.md`](development_log.md)。

### 学習順序の指針

- **最短ルート（直感重視）**：00 → 01 → 02 → 05 → 06。まず「不確実性をどう表すか」と「最適化でどう使うか」の骨格をつかむ。
- **標準ルート**：00 → 01 → 02 → 03 → 04 → 05 → 06 を順番に。
- **応用から逆算したい人**：06 の冒頭の比較表を先に眺め、出てくる用語（期待値・CVaR・チャンス制約）を 02–05 で埋める。

---

## 4. リポジトリ構造

```
lec_prob/
├── README.md                  ← いまここ（全体設計）
├── development_log.md          ← 各成果物の作成意図・未解決事項・次にやること
├── requirements.txt            ← Python 依存パッケージ
├── roadmap/                    ← 概念地図・依存関係・記法規約
│   ├── learning_map.md         ← モジュール依存関係（Mermaid）
│   ├── concept_map.md          ← 概念どうしのつながり
│   ├── optimization_map.md     ← 最適化6形式の二軸マップ
│   └── notation.md             ← 記法規約（教材全体で統一）
├── notes/                      ← 本文（Markdown + LaTeX、Obsidian対応）
├── exercises/                  ← 演習（basic / intermediate / advanced / solutions）
├── apps/                       ← インタラクティブツール（Streamlit / Plotly）
│   ├── pdf_cdf_visualizer/             ← PDF・CDF・区間確率の可視化（Module 2）
│   ├── bayes_visualizer/              ← ベイズ更新・基準率の誤謬（Module 1）
│   ├── monte_carlo_visualizer/        ← MC収束・希少事象・SAA（Module 5）
│   ├── scenario_tree_visualizer/      ← 二段階シナリオ木（図ベース, Module 5–6）
│   ├── battery_dispatch/              ← 蓄電池アービトラージ・SoC・予測価値（Module 6b, cvxpy）
│   └── stochastic_optimization_comparator/ ← capstone：6形式を同一問題で比較（Module 6, cvxpy）
├── notebooks/                  ← Jupyter（探索用）
├── figures/                    ← 図（SVG または再生成スクリプトの出力）
├── scripts/                    ← 図・データ生成スクリプト（再現可能）
├── data/                       ← サンプルデータ（CSV）
└── references/                 ← 文献（references.bib + reading_list.md）
```

---

## 5. 各ノートの共通フォーマット

すべてのノートは次の順序を守ります（**式だけで終わらせない**ための型）。

1. **YAML frontmatter**（学習目標・前提知識・想定時間・重要な仮定・参考文献）
2. **現象・直感** — 何に困っているのか
3. **図・可視化** — 数式の前にイメージをつかむ
4. **数学的定義** — 記号と意味を1文ずつ
5. **小さな数値例** — 手で追える規模
6. **手計算 → Python検証** — 直感と計算の一致／不一致を確認
7. **電力・エネルギーへの接続** — 需要・PV・価格・故障・需給制約
8. **理解確認問題**（初級・中級・発展）
9. **よくある誤解の整理**

---

## 6. 実装方針

- **記述**：Markdown を中心に、数式は LaTeX。Obsidian でそのまま読める構造（`[[wikilink]]` と相対リンクを併用）。
- **コード**：Python を基本。可視化は **Plotly**、インタラクティブツールは **Streamlit**。数理最適化は **cvxpy**（必要に応じて Pyomo）。
- **図**：可能な限り**再生成可能な Python スクリプト**（`scripts/`）として管理。出力は `figures/`。
- **再現性**：各ツール／スクリプトに実行手順を README で明記。
- **演習**：各問題に *難易度・前提知識・学習目標・想定所要時間* を明記。
- **数式**：各数式に**意味を述べる日本語を1文以上**添える。

### 環境構築

```bash
# 仮想環境（任意）
python3 -m venv .venv && source .venv/bin/activate

# 依存パッケージ
pip install -r requirements.txt

# 第1ツール（PDF・CDF・区間確率）を起動
streamlit run apps/pdf_cdf_visualizer/app.py

# 到達点：6形式の比較ツールを起動
streamlit run apps/stochastic_optimization_comparator/app.py

# 図の再生成（任意）
for f in scripts/[0-9]*.py; do python3 "$f"; done

# 数理コアの自己テスト（Streamlit 不要）
python3 apps/pdf_cdf_visualizer/core.py
python3 apps/stochastic_optimization_comparator/core.py
```

> Obsidian で読む場合：このフォルダ（`lec_prob`）を Vault として開くと、ノート間リンクと数式（要：MathJax）がそのまま機能します。

---

## 7. 進捗の記録

各作業セッションで「何を・なぜ追加したか／未解決事項／次の一手」を [`development_log.md`](development_log.md) に時系列で記録します。教材の**設計判断の履歴**もここに残します。

---

## 8. このリポジトリの「完成」の定義

学習者が、**同じ一つの意思決定問題**（例：蓄電池の充放電計画）を、

- 決定論的最適化
- シナリオベース確率計画
- 期待値最小化
- ロバスト最適化
- チャンス制約
- CVaR最小化

の各形式で定式化・比較し、**「いま自分はなぜこの形式を選ぶのか」を自分の言葉で説明できる**状態。これがゴールです。

---

## 9. Web サイトとして読む（GitHub Pages）

この教材は **MkDocs（Material テーマ）** で静的サイト化され、**GitHub Pages** で公開できます。
数式（MathJax）・Mermaid 図・SVG 図・全ノート/演習/ツール解説がブラウザで読めます。

### ローカルでプレビュー
```bash
pip install -r requirements-docs.txt
mkdocs serve            # http://127.0.0.1:8000 でライブプレビュー
# 静的ビルド（site/ に出力）
mkdocs build --strict
```

### GitHub に公開する手順
1. GitHub にリポジトリを作成し、`main` ブランチを push する。
   ```bash
   git remote add origin https://github.com/<ユーザー名>/lec_prob.git
   git push -u origin main
   ```
2. リポジトリの **Settings → Pages → Build and deployment → Source** を **GitHub Actions** に設定する。
3. 以降、`main` への push で `.github/workflows/deploy-pages.yml` が自動でビルド・公開する。
4. 公開 URL：`https://<ユーザー名>.github.io/lec_prob/`

> **依存のピン留め**：サイトのビルド依存は `requirements-docs.txt` で固定（MkDocs 2.0 の後方非互換リスクを避けるため）。
> 学習者は、リポジトリ（GitHub 上で Markdown を直接閲覧）でも、Pages サイト（整形済み）でも、Obsidian（Vault として開く）でも、同じ教材を読めます。

> **ツールについて**：インタラクティブツール（Streamlit）は静的サイトでは動きません。サイトには各ツールの解説を載せ、
> 実行はローカル（`streamlit run apps/.../app.py`）または Streamlit Community Cloud で行ってください。

---

## 10. ライセンスと引用

教材内で引用する文献は [`references/references.bib`](references/references.bib) に書誌情報・DOIを集約します。教科書・査読論文・IEEE Transactions / IEEE PES 資料・主要国際誌を優先します。
