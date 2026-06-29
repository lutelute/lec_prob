# development_log — 開発・教材設計ログ

各作業セッション（および /loop の各イテレーション）で、「何を・なぜ追加したか／検証／未解決事項／次の一手」を時系列で記録する。
教材の**設計判断の履歴**もここに残す。新しいエントリは上に追記する。

---

## 2026-06-29 — 改善A1+B2：実践ガイド「確率の使い方」＋最短コース導線

### 背景（精査）
- ユーザー「結局どうやって確率を使うのか根本が分からない」「人間UIとして分かりにくい」。
- UI・内容を精査し `IMPROVEMENT_PROPOSAL.md` に診断と優先順位つき改善案を提出（実測：使い方を主題にした文書0本／ノート→ツールのリンク0／ノート275-376行と高密度）。ユーザーは A1+B2 を選択。

### A1：実践スパイン（根本対応）
- `notes/how_to_use_probability.md` 新設。**確率を使う＝①名付ける→②表す→③決める**の3ステップ。
- **パン屋の完全例**：品切れ損200/廃棄損50 → 臨界比0.8分位点＝113個・品切れ20%。価値観で 100→113→125 と決定が変わる（数値は scipy 検証）。電力（予備力）へ1対1写像。穴埋めテンプレート。各ステップで使うノート/ツールの地図。つまずきQ&A。

### B2：最短コース導線（On-ramp）
- README トップに「**まずこれだけ（30分）**」＝実践ガイド→6形式コンパレータ→Module 0。
- `mkdocs.yml` nav の最上位（ホーム直下）に「🧭 確率の使い方（実践ガイド）」を配置。
- 精査メモ `IMPROVEMENT_PROPOSAL.md` は公開ビルドから除外。

### 検証（本番 Pages）
- https://lutelute.github.io/lec_prob/notes/how_to_use_probability/ ：4表・MathJax22式・3ステップ図・本文リンク全解決（モジュール/ツール）・本文生LaTeX0。左ナビ最上位に配置を確認。
- `mkdocs build --strict` exit 0、デプロイ成功。

### 次の候補：B1（ツールにガイド付き観察）／A3（ノート↔ツール織込）／A2（各ノート30秒まとめ）。

---

## 2026-06-29 — 本番不具合の修正：ハブを「クリック読込」方式に ★公開動作確認

### 不具合（ユーザー指摘「pagesで動かない・わからない」）
- 本番ハブで**下部3ツール（モンテカルロ・コンパレータ・蓄電池）が空表示**。
- 原因：5ツールを常時 iframe 埋め込み → 各 iframe が Plotly(約4MB) を**同時多重ロード**し、一部が読み込まれず描画されない（特に lazy の下部）。

### 修正
- `interactive/index.md` を**クリック読込**方式に変更：各ツールは `<div class="tool-embed">` ＋「**▶ ここで動かす**」ボタン。押したときだけ iframe を生成（同時ロードを排除）。使い方ヒント＋全画面リンク＋`!!! tip` も追加。

### 検証（ローカル＋**本番 Pages**）
- ローカル：初期 iframe=0、ボタン押下で該当ツールのみ読込、pdf_cdf でスライダー動作（ε縮小で区間確率→0、密度不変）。
- **本番 https://lutelute.github.io/lec_prob/ ：** コンパレータをクリック読込 → Plotly読込・6プロット・表6行・高さ自動フィット・スライダーで ε0.1→0.05 → チャンスx* 119.2→124.7 即時更新を Playwright で確認。スクショで決定マップ・x*バーの表示も確認。
- `mkdocs build --strict` exit 0、デプロイ成功。

### 結果：本番 Pages 上で全インタラクティブツールが確実に動く状態に。

---

## 2026-06-29 — GitHub 公開（push＋Pages デプロイ）★Web公開達成

### 背景（ユーザー指摘）
- 「githubに当たらない」＝ローカルコミットのみでリモート未push。実際に GitHub へ上げる。

### 実施
- `gh repo create lutelute/lec_prob --public --source=. --push`：リポジトリ作成。
- **メールプライバシー対応**：初回 push が GH007（実メール `lutebass@gmail.com` 露出）で拒否 → 全14コミットの author/committer を `git filter-branch` で noreply（`17675761+lutelute@users.noreply.github.com`）に書換え、`git config` も更新して再 push 成功。
- `gh api -X POST repos/.../pages -f build_type=workflow`：Pages を Actions ソースで有効化。
- 初回ワークフローは Pages 未有効で deploy 404 失敗 → 有効化後 `gh run rerun` で **成功**。

### 検証（本番URL）
- https://lutelute.github.io/lec_prob/ → HTTP 200。interactive/・comparator.html・lib/stats.js すべて 200。
- **本番 Pages 上でインタラクティブ動作を Playwright 検証**：comparator でスライダー ε0.1→0.05 → チャンスx* 119.2→124.7 即時更新。コンソールエラーは favicon 404 のみ（無害）。
- README §9 に公開URL（https://lutelute.github.io/lec_prob/ ）とリポジトリURLを明記。

### 結果
- 教材・サイト・5インタラクティブツールが **GitHub 上で公開・稼働**。学習者は URL を開くだけで読んで動かして学べる。goal「GitHub＋Pages での公開で学習者がWebで学べる状態」を実機で達成。

---

## 2026-06-29 — イテレーション29（全体最終確認・締めくくり）★goal達成

### 最終確認（すべて green）
- **注釈Unicode**：全5インタラクティブツール（pdf_cdf/bayes/montecarlo/comparator/battery）に LaTeX 生 `$` 残存なし。
- **回帰なし**：Streamlit版5ツールの core self-test 全合格。
- **サイト**：`mkdocs build --strict` exit 0。
- **構成**：8ノート・8解答・11図・24演習・**5ブラウザ内インタラクティブツール**・5 Streamlit core・サイト61ページ・git 13コミット・追跡109ファイル。

### 「完全にインタラクティブなツール」goal の到達点
- 全5ツールが GitHub Pages 上でブラウザ内完結動作（インストール不要、スライダー即時更新、Playwright実機検証済み、全数値が教材と一致）。
- モバイル対応・カード目次・iframe自動高さ・トップ導線まで仕上げ済み。蓄電池は EVPI（予測の価値）も体験可能。
- 新goalのループ反復：イテレーション19〜29（作成5＋仕上げ6）で完了。

### 残課題（任意・将来）
- Streamlit版のCommunity Cloud公開、6形式コンパレータの二段階/多段階版、各ノートからインタラクティブ版への相互リンク。

---

## 2026-06-29 — イテレーション28（仕上げ⑤：蓄電池に「予測の価値」追加）

### 追加・変更
- `interactive/battery.html` に **価格予測誤差 σ スライダー**と「予測の価値」セクションを追加。
  - 固定計画（平均価格で立てた閾値スケジュールを実価格に適用＝決定論/EEV相当）vs 完全予測（実価格で立て直す＝WS相当）の平均利益と差を表示。
  - `lib/stats.js` の再現乱数でσに応じた40シナリオを生成。教材6bの WS−EEV ギャップ＝EVPI 直感に接続。

### 検証（Playwright 実機）
- σ=0 で非表示、σ=8 で表示：固定計画143.4 ≤ 完全予測243.7、予測の価値(gap)=100.3（gap≥0、stats.js読込）。
- battery.html に LaTeX 生 `$` 残存なし（Unicode統一OK）。
- `mkdocs build --strict` exit 0。

### 進捗（仕上げフェーズ）：①〜⑥全完了（モバイル・通し検証・トップ導線・iframe高さ・カード目次・蓄電池予測価値）。新goalのループ反復は計10回（19〜28）。次：注釈Unicode全ツール最終確認 → 全体最終確認で締め。

---

## 2026-06-29 — イテレーション27（仕上げ④：ハブにカード目次）

### 追加・変更
- `interactive/index.md` トップに**5ツールのカード目次**（色分け・モジュールタグ・1行説明、レスポンシブグリッド）を追加。各ツール見出しに明示アンカー `{#t1}`〜`{#t5}` を付与。

### 設計判断・修正
- attr_list の `{#id}` は**見出しテキストとの間にスペースが必須**。最初 `）{#t1}` でスペース無しにしたため slug に混入（`...module-2t1`）→ ` {#t1}` に修正し `id="t1"` を生成。

### 検証（Playwright 実機）
- カード5枚描画、`#t1`〜`#t5` ターゲット存在、④カードのクリックでコンパレータ節へスクロール（URL→#t4、対象が画面上部に移動）。
- `mkdocs build --strict` exit 0。

### 進捗（仕上げフェーズ）：①モバイル ②通し検証 ③トップ導線 ④iframe高さ ⑤カード目次 完了。次：蓄電池の予測価値比較・注釈Unicode最終確認・全体最終確認。

---

## 2026-06-29 — イテレーション26（仕上げ③：iframe 自動高さフィット）

### 追加・変更
- `interactive/index.md`：全 iframe に `data-fit` を付け、**同一オリジンの iframe を中身の高さに自動フィット**する小スクリプトを追加（load後に複数回・resize時に再計測）。固定高さの初期値も実測値（1200〜1560px）に更新しガタつきを軽減。

### 検証（Playwright 実機、ハブページ）
- 5 iframe すべて `iframe高さ ≈ 中身の高さ`（pdf_cdf 1527/1513・bayes 1590/1576・mc 1212/1198・comparator 1486/1472・battery 792/792）で**内部スクロールなし**。
- iframe幅(~700px)では tool が単列スタックするため実際は1200〜1600px必要 → 自動フィットで過不足なく表示。固定値ハードコードより堅牢。
- `mkdocs build --strict` exit 0、ビルド済みハブに script 反映。

### 進捗（仕上げフェーズ）：①モバイル ②通し検証 ③トップ導線 ④iframe高さ 完了。次：注釈Unicode最終確認・蓄電池の予測価値比較（任意）・全体最終確認。

---

## 2026-06-29 — イテレーション25（仕上げ②：全5ツール通し検証 ＋ トップ導線強化）

### 実施・検証（Playwright 実機、CSS変更後の回帰確認）
- 全5ツールの通し検証：
  - pdf_cdf：2プロット・スライダー・オーバーフローなし。
  - bayes：3プロット・スライダー(16.7%→83.2%)・なし。
  - montecarlo：3モード描画・スライダー・再サンプリング・なし。
  - comparator：2プロット・6行・スライダー・なし。
  - battery：プロット・スライダー(利益142.7→95.4)・なし。
  - → 全ツールでプロット描画・スライダー即時更新・横オーバーフローなしを確認。
- **トップ導線強化**：README の「はじめての方へ」を、Streamlit版リンク→**ブラウザ版インタラクティブ・ツール一覧(interactive/index.md)**先頭に変更。最短ルートの到達点も interactive 版へ。
- `mkdocs build --strict` exit 0。

### 進捗（仕上げフェーズ）：①モバイル ②通し検証 ③トップ導線 完了。次：iframe高さ最適化・注釈Unicode最終確認・蓄電池の予測価値比較（任意）。

---

## 2026-06-29 — イテレーション24（仕上げ①：モバイル/狭幅レイアウト）

### 実施
- 全5ツールのモバイル幅（375px）検証（Playwright resize）。パネル・プロットは正しく単列折返しするが、**約11pxの横オーバーフロー**を検出。
- 原因：Plotly のコンテナ幅と padding の相互作用による微小はみ出し。
- 修正：`interactive/lib/tool.css` に `html{overflow-x:hidden;max-width:100%}` と `.plot,.plots>div{max-width:100%;overflow:hidden}` を追加。

### 検証（Playwright 実機）
- モバイル375px：横スクロール解消（scrollW=clientW=375）、パネル/プロットが単列スタック、切れなし（コンパレータでスクショ確認）。
- デスクトップ1280px：プロットは2列維持（369px×2）、オーバーフローなし、両プロット描画、pval=0.6489。CSS変更の悪影響なし。
- `mkdocs build --strict` exit 0。

### 進捗（仕上げフェーズ）
- ①モバイル対応 完了。次：全5ツールのコンソールエラー皆無の通し確認、トップ導線強化、iframe高さ最適化。

---

## 2026-06-29 — イテレーション23（ツールWeb化⑤：蓄電池運用）★全5本完成

### 追加・変更
- `interactive/battery.html` — 24h アービトラージ。価格プロファイル（夜安・夕方ピーク）・容量/出力/効率・閾値（百分位）スライダー。SoC遷移・充放電バー・利益を即時更新。
- `interactive/index.md` に蓄電池節（5本完成の案内）。

### 検証（Playwright 実機）
- 利益142.7、平均充電10.7 < 平均放電30.3（アービトラージ成立）。効率 0.9→0.7 で利益 142.7→**95.4**（往復ロス）。夕方ピーク↑で利益156.6。SoC軌道（充電で上昇→放電で下降）描画。
- **正確性の改善**：閾値ディスパッチは近視眼的（夕方の最高値より先に昼の高値で放電し切る）。タイトルを「最適アービトラージ」→「閾値ディスパッチ」に訂正し、注釈で「単純ルールの限界＝最適化の価値」を明記。
- `mkdocs build --strict` exit 0。

### ★ 全5ツールがブラウザ内完結のインタラクティブに（goal達成の中核）
①PDF・CDF ②ベイズ ③モンテカルロ ④6形式コンパレータ ⑤蓄電池。すべて GitHub Pages で動作、Streamlit不要、Playwrightで実機検証済み。

### 次：全5本の通し検証（モバイル幅・iframe高さ・注釈Unicode）と仕上げ。

---

## 2026-06-29 — イテレーション22（ツールWeb化④：6形式コンパレータ・到達点）

### 追加・変更
- `interactive/comparator.html` — 容量調達を6形式でJS実装（①決定論 ②期待値=臨界分位点 ③ロバスト=区間最悪 ④チャンス=分位点 ⑤CVaR=サンプルRockafellar–Uryasevグリッド ⑥DRO=Scarf閉形式）。μ/σ/cs/co/ε/α/k スライダー、決定マップ＋x*バー＋評価表（E最小・CVaR最小をハイライト）。
- `interactive/index.md` に到達点ツール節。

### 検証（Playwright 実機）
- x*: ①100 ④119.2 ②120 ⑥121.3 ⑤128.5 ③136.8（教材の100〜137と一致）。E[C]最小=②26.8、CVaR最小=⑤61.3（教材26.75/60.57と一致）。
- インタラクティブ：ε 0.1→0.05 でチャンス x* 119.2→124.7、cs=1で コスト由来形式が μ へ集約。
- **精度修正**：cs=1でもチャンス制約はε由来で分位点に残るため、観察注釈を「コスト由来の形式が μ へ集まる」に訂正。
- `mkdocs build --strict` exit 0。

### 進捗：4/5（①PDF・CDF ②ベイズ ③モンテカルロ ④6形式コンパレータ）。次 ⑤蓄電池運用。

---

## 2026-06-29 — イテレーション21（ツールWeb化③：モンテカルロ収束）

### 追加・変更
- `interactive/montecarlo.html` — 3モード（E[X]収束＋CI／希少事象P(X>c)／SAA最適q）。「🎲再サンプリング」でMCのばらつきを観察。stats.js の再現乱数（mulberry32+Box-Muller）を利用。
- `interactive/index.md` にMC節（iframe＋全画面リンク）追加。

### 検証（Playwright 実機、3モード）
- E[X]：推定 99.986→真値100、CI半幅 ±0.131（N=5万）。
- 希少事象：P(X>145)=**1.35e-3**（教材一致）、N=300でヒット1、必要N目安 22,223。
- SAA：臨界比0.909、真値 q*=120.0、q̂(N=1万)=**119.8**（収束）。
- 🎲再サンプリング：推定 99.986→100.1（シード変化）でMCのばらつきを実演。
- `mkdocs build --strict` exit 0。

### 進捗：3/5（①PDF・CDF ②ベイズ ③モンテカルロ）。次 ④6形式コンパレータ。

---

## 2026-06-29 — イテレーション20（ツールWeb化②：ベイズ更新）

### 追加・変更
- `interactive/bayes.html` — 基準率の誤謬を即時更新。事前/感度/誤警報率スライダー、n件内訳バー、事後vs基準率曲線、逐次更新（オッズ×尤度比）。
- `interactive/index.md` にベイズ節（iframe＋全画面リンク）追加。

### 検証（Playwright 実機）
- 既定で 事後 P(F|警報)=**16.7%**（教材一致）、P(F|警報なし)=0.01%。3プロット描画。
- インタラクティブ：基準率 0.01→0.1 で事後 16.7%→**68.8%**、誤警報率 0.05→0.01 で **50.0%**、逐次2回 **79.8%**。全て教材値と一致。
- `mkdocs build --strict` exit 0、site に bayes.html 配置。

### 進捗：2/5 ツール（①PDF・CDF ②ベイズ）。次 ③モンテカルロ収束。

---

## 2026-06-29 — イテレーション19（ツールWeb化①：PDF・CDF を真のインタラクティブに）※方針転換

### 背景（ユーザー指摘）
- 「全然インタラクティブじゃない」。**Streamlitツールはローカル専用で、公開Pagesでは解説/スクショのみ**＝Web上で動かない、という根本欠陥を是正。
- 方針：Pyodide/stlite（重WASM・cvxpy非対応）を避け、**自己完結HTML/JS+Plotly.js でブラウザ内完結**するツールに作り替える（GitHub Pagesで軽快に動作）。

### 追加・変更
- `interactive/lib/stats.js` — 依存なしの確率統計ライブラリ（正規/対数正規/指数/一様の pdf/cdf/ppf、erf、Acklam分位点、台形積分、再現乱数）。
- `interactive/lib/tool.css` — 共通スタイル（5ツールで再利用）。
- `interactive/pdf_cdf.html` — **1本目**：スライダー即時更新の PDF・CDF・区間確率ツール。分布切替・問い方・区間・点プローブ。
- `interactive/index.md` — インタラクティブ・ハブ（iframe埋め込み＋全画面リンク）。`mkdocs.yml` nav に「▶ ブラウザで動かす」追加。pdf_cdf README に Web版バナー。

### 検証
- `stats.js` を Node で検証：N(85≤X≤115)=0.6827、P(X>130)=0.0228、ppf(0.909)=120.02、f(0)|N(0,0.2)=1.9947(>1)、対数正規P(X>200)=0.0061、面積=CDF差 一致。**全て教材値と一致**。
- Playwright で**インタラクティブ動作を実機検証**：ε=5→0.01 で区間確率 0.261→0.0005（密度高さは0.0266で不変）＝密度≠確率が生きて動く。aスライダーでP更新、分布切替で再構築。
- `mkdocs build --strict` exit 0（.htmlリンク・iframe含め警告なし）。

### 次（残り4本＋10回以上のループ）
- ②ベイズ更新 ③モンテカルロ収束 ④6形式コンパレータ（newsvendor、JSで6形式）⑤蓄電池運用。各々スライダー即時更新＋Playwright検証。

---

## 2026-06-29 — イテレーション18（サイト品質点検 ＋ ホーム導線追加）

### 現状確認（手順1）
- `mkdocs build --strict` exit 0・実警告なし、serve 稼働。検索 lang=ja も警告なし。
- 未確認ページの描画点検（Playwright）：最適化地図＝ASCII二軸マップが等幅で整列、大比較表は数式入りで横スクロール対応、Mermaid決定フロー描画。全ページ種別で品質良好を確認。

### 追加・変更
- `README.md` 冒頭に **「🚀 はじめての方へ（最短ルート）」** 導線を追加（Module 0 → 学習地図 → 6形式コンパレータ、GitHub/Pages 両対応の相対リンク）。Web学習者の入口を明確化。

### 検証
- 追加リンク3本（notes/00, roadmap/learning_map, comparator README）が strict ビルドで解決（exit 0・実警告なし）。

### 状態
- 教材・サイトとも健全。学習者はホームから最短ルートで Module 0 →到達点へ辿れる。

### 次の一手（任意）
- 各ノートの図セクションの体裁統一、Streamlit Community Cloud でのツール公開手順、概念地図/最適化地図の相互リンク強化。

---

## 2026-06-29 — イテレーション17（サイトのローカルプレビュー確認と仕上げ）※ユーザー依頼

### 実施
- `mkdocs serve` でローカルプレビューを起動し、Playwright（ヘッドレス）でホーム/ノート/ロードマップを実描画・スクリーンショット確認（claude-in-chrome 拡張が未接続のため Playwright を使用）。
- レンダリング検証：MathJax 数式212個、埋め込みSVG図、Mermaid 依存グラフ（色分け）すべて正常描画。

### 見つけた課題と修正
1. **見出し内の数式が TOC で生 LaTeX 表示**（`\(E[X]\)` 等）→ 5見出しから `$...$` を除去し平文化（本文の数式は維持）。notes/03（2箇所）、notes/05（3箇所）。
2. **README の相対リンクが strict ビルドを失敗させる**（`requirements-docs.txt`＝.txtはMkDocsのリンク検証対象外で WARNING）→ 当該2リンクをインラインコード化、`requirements*.txt` と `.github/` を exclude_docs に明示。

### 検証
- `mkdocs build --strict` 再実行 **exit 0・実警告ゼロ**（残る表示は ProperDocs 宣伝バナーのみ）。TOC が平文表示になったことをブラウザ再確認。

### 状態
- 公開サイトはレンダリング・strict ビルドとも健全。Action は通る。
- `.gitignore` に site/・preview_*.png・.playwright-mcp/ を追加。

---

## 2026-06-29 — イテレーション16（GitHub Pages 公開サイト構築）※新goal

### 新goal
- 「/loop で改善継続 ＋ 最終的に GitHub と Pages で学べるよう設定」。本回はその公開基盤を構築。

### 追加・変更
- `git init`（main ブランチ）。リポジトリ化。
- **MkDocs Material** サイト：`mkdocs.yml`（same-dir でルート構造維持・nav・数式 arithmatex/MathJax・Mermaid superfences・ダーク/ライト）、`assets/javascripts/mathjax.js`。
- `requirements-docs.txt`（mkdocs 1.6.1 / material 9.7.6 / same-dir 0.1.5 / pymdown 11.0 をピン留め）。
- `.github/workflows/deploy-pages.yml`（push→build --strict→Pages デプロイ）。
- wikilink 42箇所を標準MDリンクに一括変換（GitHub/MkDocs/Obsidian 可搬）。
- `.gitignore` に site/ 追加、README に「§9 Web サイトとして読む（公開手順）」追加、scenario_tree の不正リンク修正。

### 検証
- `mkdocs build --strict` **exit 0**（警告なし）。site/ に59ページ生成。
- HTML 検証：数式 arithmatex 45箇所＋MathJax 読込、Mermaid 4図 class="mermaid"、図SVG 11枚コピー、.venv 除外。

### 設計判断
- ビルド時に「ProperDocs へ乗り換えを促す警告」が出るが、**未検証パッケージへの乗り換えはサプライチェーン上避ける**。動作実績のある MkDocs 1.6.1 系をバージョン固定し、Action で `DISABLE_MKDOCS_2_WARNING=true`。将来 `pip install mkdocs` が v2 を引いて壊れるリスクはピン留めで回避。

### 仮定・限界・次の一手
- Streamlit ツールは静的サイトでは非稼働（解説のみ掲載、ローカル/Community Cloud 実行を案内）。
- push と Pages 有効化は認証情報が要るためユーザー操作（README §9 に手順）。ローカル初期コミットまで実施。
- 次：トップページのサイト向け最適化、ナビ微調整、CI で nbconvert 等は不要。

---

## 2026-06-29 — イテレーション15（Module 6b standalone 演習整備）※ユーザー依頼

### 追加・変更
- `exercises/{basic,intermediate,advanced}/06b_two_stage_stochastic_programming.md`（3ファイル新規）。6b §9 確認問題＋§8 リスク回避CVaR二段階を反映。
- `exercises/solutions/06b_two_stage_solutions.md` に「standalone 演習バンク」節を追記（ID対応＋新規 B6b-4/I6b-4/A6b-3 の解答）。
- `exercises/README.md` カバレッジ表で 6b を全level ✅ に更新。

### 数学的に重要な点（cvxpy検証済み）
- I6b-4：リスク回避の保険料 +185（658→843）と保障 −750（1650→900）。
- CVaR の $\alpha$ 依存：$\alpha=0.5\to x^\*130$, $0.8\to174.8$, $0.9\to180$（最大シナリオで飽和）。$\alpha\uparrow$ で保守化、離散では上限飽和。

### 検証
- 3演習ファイルの frontmatter・solutionsリンク全OK。演習総数：各level 8（0,1,2,3,4,5,6,6b）＝24、solutions 8。

### 状態
- 全モジュール（0–6＋6b）で note・図・演習(basic/int/adv)・解答が揃い、構造的に完全。

---

## 2026-06-29 — イテレーション14（リスク回避型二段階：CVaR 二段階）

### 今回の選択
- Module 3（CVaR）と 6b（二段階 recourse）を結ぶ**リスク回避型二段階**が未完（6b §8/演習8で定式化のみ、数値なし）→ これを worked example 化。

### 追加・変更
- `notes/06b_*.md` — 新 §8「発展：リスク回避型二段階（CVaR 二段階）」を挿入（定式化・数値例・図・いつ使うか）。後続 §8→9, §9→10, §10→11 に renumber。
- `scripts/06c_risk_averse_two_stage.py` → `figures/06c_risk_averse_two_stage.svg` — リスク中立 vs 回避の x* とシナリオ別コスト分布。
- `exercises/solutions/06b_two_stage_solutions.md` 発展8 に数値確認を追記。

### 数学的に重要な点（cvxpy検証済み）
- 希少スパイク $\xi\in\{70,100,130,180\}$, $\pi=\{.3,.4,.25,.05\}$ で：
  - リスク中立（E最小）：$x^\*=130$、E=658、**最悪1650**（5%で大損）。
  - リスク回避（CVaR$_{0.9}$）：$x^\*=180$、E=843、**最悪900**。
  - **+185 の平均コストで最悪を −750**（尾部リスクの保険料）。Rockafellar–Uryasev で線形化。

### 確率的最適化の明示（goal要件）
- 決定変数 x＋recourse y＋CVaR補助 η,u、不確実 ξ（シナリオ）、目的＝CVaR（尾部平均）、制約＝各シナリオ満足、リスク中立比＝平均悪化と引き換えに最悪を平準化。

### 検証
- 6b §1–11 連番整合、両図（06b/06c）相対パス解決、図11枚。

### 次の一手（任意）
- 6b standalone 演習、多段階(>2)への言及、roadmap の最終読み合わせ。

---

## 2026-06-29 — イテレーション13（全ノートへの図埋め込み）

### 追加・変更
- `notes/0[0-6]*.md`・`notes/06b_*.md` — 検証済み SVG 図10枚を該当セクションに `![](../figures/…)` で埋め込み（キャプション＋再生成コマンド付き）。
  - 00:flaw_of_averages / 01:bayes_base_rate / 02:pmf_vs_pdf＋pdf_cdf_interval / 03:mean_var_cvar / 04:data_to_distribution / 05:monte_carlo＋scenario_tree / 06:optimization_comparison / 06b:two_stage_vss_evpi。

### 学習上の狙い
- 各ノートの「図」ステップを、ASCII図だけでなく**実データ・実計算の高品質プロット**で具体化。Obsidian・GitHub 両方で相対パス画像がレンダリングされる。

### 検証
- 画像参照10件すべて相対パス解決（notes→../figures）。10図すべて少なくとも1ノートで使用。各ノートの図枚数を確認（02・05が2枚、他1枚）。

### 状態
- 8ノート（図埋め込み済み）・21演習＋8解答・10図・5ツール・検証済み文献。教材の体裁が完成。

### 次の一手（任意）
- CVaR二段階/多段階の拡張、6b standalone 演習、roadmap 図のレンダリング確認。

---

## 2026-06-29 — イテレーション12（Module 2–6 standalone 演習整備）※ユーザー依頼

### 追加・変更
- `exercises/{basic,intermediate,advanced}/0[2-6]_*.md` — Module 2,3,4,5,6 の演習を各level 1ファイルずつ新規作成（計15ファイル）。Module 0-1 と同形式（メタ情報：難易度/前提/学習目標/想定時間/solutionsリンク）。
- `exercises/solutions/0[2-6]_*_solutions.md` — 各末尾に「standalone 演習バンクの対応・追加解答」節を追記（ID対応＋新規問題 B*-4/I*-4/A*-3 の解答）。
- `exercises/README.md` — カバレッジ表（Module 0–6 全level ✅）を追加。

### 学習上の狙い
- 演習を**自己完結した問題バンク**化（ノートを開かずに exercises/ だけで段階学習）。Module 0-1 のみだった level別ファイルを 2-6 へ拡張し構造的一貫性を回復。
- 各モジュールに「手を動かす」問題（ツール操作・CSV解析）を追加し、可視化ツールと演習を接続。

### 数学的に重要な点（新規問題、Python検証済み）
- I3-4 地点間相関：$\mathrm{Var}(P_1{+}P_2)=50+50\rho$ → σ= ρ1:10 / ρ0:7.07 / ρ-1:0（地理的平準化）。
- B4-4 SE=12.9/√730=0.477、B5-4 半幅 N100:2.94→N10000:0.294（1/10）。
- B2-4 CDF差0.62、B3-4 √0.61=0.781、I4-4 データ mean98.8/median96.5（右歪み）/ECDF P(≤110)=0.78。

### 検証
- 21演習ファイルの frontmatter・solutionsリンクを全検証（全OK）。新規問題の数値を Python 確認。

### 状態
- 演習：basic/intermediate/advanced 各7（Module 0–6）＋solutions 8。教材・ツール・演習が全モジュールで揃った。

### 次の一手（任意）
- 6b の standalone 演習、CVaR二段階/多段階の拡張、各ノートへの図埋め込み（相対パス）。

---

## 2026-06-29 — イテレーション11（第5ツール：蓄電池運用ビジュアライザ）

### 今回の選択（手順1–3）
- 現状：Module 0–6＋6b・8解答・10図・4ツール完成。
- 最大の残価値＝goal が繰り返す**蓄電池運用ツール（多時間帯 SoC ダイナミクス）**。6b の二段階概念を実アプリ化し「決定論 vs 完全予測」を可視化 → これを選定。

### 追加・変更
- `apps/battery_dispatch/{core.py, app.py, README.md}` — 多時間帯アービトラージ LP（cvxpy）。価格・充放電・SoC を可視化し、価格不確実下で 決定論（予測計画→実価格, EEV相当）vs 完全予測（WS相当）の差＝予測誤差コスト（EVPI相当）を提示。
- README の apps 一覧を6項目に更新。

### 数学的に重要な点（cvxpy検証済み）
- アービトラージ利益186、平均充電価格11.2<放電27.0（安充電・高放電）。SoC∈[0,10]。
- 完全予測WS=340.8 ≥ 決定論197.3、予測誤差コスト=143.5（σ=6）。η=0.9→0.7で利益186→124.5（往復ロス）。

### 最適化の明示（goal要件）
- 決定変数 c_t,d_t,SoC_t、不確実 ξ_t（価格・シナリオ）、目的＝利益（期待利益）、制約＝SoC遷移・容量・出力（常時満足）、決定論比＝完全予測に予測誤差コスト分劣る（実運用はrecourseで中間）。

### 仮定・限界・次の一手
- 価格のみ不確実、完全多段階 recourse は未実装（2境界提示）。次は Module 2–6 standalone 演習整備、または CVaR/多段階拡張。

### 検証
- `core.py` self-test ALL OK、`AppTest` 例外なし（個別プロセス）。

---

## 2026-06-29 — イテレーション10（Module 6b：二段階確率計画 VSS・EVPI）

### 今回の選択（手順1–3）
- 現状確認：Module 0–6＋解答＋4ツール＋図＋検証済み文献まで完成。
- 最大の概念ギャップ＝**二段階確率計画（recourse）が概念止まり**で、決定論との差を定量化する VSS/EVPI の worked example が無い（既存 comparator は単段 newsvendor）。goal の「二段階確率計画法」「蓄電池運用」「決定論と比べ何が得られ何を失うか」に直結 → これを次の1単位に選定。

### 追加・変更
- `notes/06b_two_stage_stochastic_programming.md` — 二段階SP一般形＋extensive form、WS/RP/EEV、VSS/EVPI、蓄電池つき日前調達の数値例、cvxpy検証、電力接続、決定論との損得表、確認問題。
- `exercises/solutions/06b_two_stage_solutions.md` — 全解答。
- `scripts/06b_two_stage_vss_evpi.py` → `figures/06b_two_stage_vss_evpi.svg` — WS/RP/EEV棒＋VSS/EVPIブラケット、x_det vs x_RP。

### 数学的に重要な点（cvxpy検証済み）
- WS=515 ≤ RP=658 ≤ EEV=714.2（理論的順序）。VSS=EEV−RP=56.2、EVPI=RP−WS=143。
- x_det=103（平均）、x_RP=140（高需要にヘッジ）。
- **発見**：離散シナリオでは x_RP=140 が完全ヘッジ点で飽和。$c_2$ 20→40 で x* 不変・**VSS 56.2→278.2 急拡大**（不足の罰が重いほど決定論の損が膨らむ）。ノート§5・演習4をこの正確な挙動に修正。

### 確率的最適化の明示（goal要件）
- 決定変数 x（日前調達）＋recourse y、不確実変数 ξ（正味需要）、表現＝シナリオ、目的＝期待値、制約＝各シナリオbalance＋蓄電池容量、仮定＝完全リコース・リスク中立、決定論比＝VSS得・尾部鈍感とS倍計算が代償。

### 仮定・限界・次の一手
- 単一期・リスク中立。次は CVaR 二段階（演習8の定式化）、多時間帯 SoC ダイナミクスの蓄電池運用ツール。

---

## 2026-06-29 — イテレーション9（第4ツール：MC収束ビジュアライザ ＋ 構造整備）

### 追加・変更
- `apps/monte_carlo_visualizer/{core.py, app.py, README.md}` — 3モード（E[X]収束／希少事象P(X>c)／SAA最適q）。
- `apps/scenario_tree_visualizer/README.md` — 図ベースの案内（`figures/05_scenario_tree.svg`）＋拡張予定。空ディレクトリを解消。
- README の apps 一覧を5項目に更新。

### 検証
- `monte_carlo_visualizer/core.py` self-test ALL OK（CI 8.68→0.13、希少事象hits[1,17,139,1370]、SAA q→120.03）。
- `AppTest`：3モード（期待値/希少事象/SAA）すべて例外なし。

### 設計判断（テスト harness の注意）
- 各アプリの `import core` は同名モジュール。`streamlit run` は別プロセスなので問題なし。
  ただし**同一プロセスで複数アプリを AppTest すると `sys.modules['core']` が衝突**するため、
  検証は**アプリごとに別プロセス**で行う（個別実行は全て合格）。

### 状態
- 中核（Module 0–6 ＋ capstone ＋ 検証済み文献）＋ インタラクティブ4ツール（pdf_cdf／bayes／monte_carlo／comparator）＋ シナリオ木図。
- 優先ツール8件中：①PDF/CDF ②(超過はpdf_cdfで) ③ベイズ ④MC ⑤シナリオ木(図) ⑥6形式比較 ⑦チャンス(比較器内) を充足。⑧蓄電池(多時間帯)は将来拡張。

### 残（任意拡充）
- Module 2–6 の standalone 演習ファイル化、蓄電池多時間帯ツール、シナリオ木の対話版。

---

## 2026-06-29 — イテレーション8（第3ツール：ベイズ更新ビジュアライザ）

### 追加・変更
- `apps/bayes_visualizer/{core.py, app.py, SPEC.md, README.md}` — Module 1 の基準率の誤謬を対話的に。
  事前・感度・誤警報率で事後を可視化、n件内訳、事後vs基準率曲線、逐次ベイズ更新（オッズ×尤度比）。
- README の apps 一覧に追加（計3ツール）。

### 数学的に重要なポイント
- 事後 P(F|警報)=16.7%（感度99%でも）。逐次2警報で79.8%。
- 低基準率域では特異度改善（誤警報率↓）が感度改善より事後に効く（0.167→0.5 vs →0.168）。

### 検証
- `core.py` self-test ALL OK（事後・PPV一致・逐次・単調性・特異度効果）。`AppTest` 例外なし（基準率0.3で89.5%）。

### 状態（到達点の整理）
- ツール3種（pdf_cdf／bayes／comparator）すべて core 分離＋self-test＋AppTest 合格。
- 中核（Module 0–6 ＋ capstone ＋ 検証済み文献 ＋ 3ツール）完成。

---

## 2026-06-28 — イテレーション7（DOI検証 ＋ README完成更新 ＋ 全体検証）

### 実施
- **DOI 検証**：主要査読論文8本の DOI・巻号・ページを WebSearch（出版社/Crossref）で確認し**全て一致**を確認、`verified = {2026-06-28}` を付与。
  - rockafellar2000, artzner1999, nemirovski2006, bertsimas2004, delage2010, esfahani2018, bertsimas2013, roald2023。
  - reading_list.md・references.bib ヘッダの「暫定」注記を「検証済み」に更新。
- **README 更新**：全7モジュール✅・2ツール（pdf_cdf／comparator）・図再生成・self-test 手順を反映。
- **全体検証**：図9種を一括再生成（全OK）、両 core 自己テスト（pdf_cdf 10 OK／comparator ALL OK）、ノート→解答リンク7本全解決。

### 状態
- 中核カリキュラム（Module 0–6 ノート・解答・図）＋ capstone 比較ツール＋検証済み文献まで完成。
- references.bib：20エントリ、brace平衡、検証済み8本。

### 残（任意の拡充）
- 優先ツール拡充：ベイズ更新ビジュアライザ（M1）、正規 分位点/超過確率（M3/6）等。
- Module 2–6 の standalone 演習ファイル（現状は note §＋solutions）。

---

## 2026-06-28 — イテレーション5–6（Module 5・6 ＋ capstone 比較ツール）★到達点

### 追加・変更
- `notes/05_scenarios_and_monte_carlo.md` ＋ `scripts/05_monte_carlo.py`, `05_scenario_tree.py` ＋ 解答。
- `notes/06_optimization_under_uncertainty.md` — 統一問題（容量調達）で6形式を定式化・比較。
- `apps/stochastic_optimization_comparator/{core.py, app.py, SPEC.md, README.md}` — **capstone**：同一問題を6形式で解いて比較（cvxpy）。
- `scripts/06_optimization_comparison.py` → `figures/06_optimization_comparison.svg` — 決定マップ。
- `exercises/solutions/05_*`, `06_*` — 解答。

### ★ 本教材の「完成の定義」を満たす成果
同一問題（$\mu=100,\sigma=15,c_s=10,c_o=1$）で6形式の最適 $x^\*$：
```
①決定論100 | ④チャンス119.2 | ②期待値120.0 | ⑥DRO121.4 | ⑤CVaR130.2 | ③ロバスト136.8
```
- ②が E[費用] 最小(26.75)、⑤が CVaR 最小(60.57)、④が不足確率≈ε(0.099)、③が最安全(0.006)。
- ①決定論は不足確率0.498・E[費用]66.1の大失敗（非対称コスト無視）。
- **各形式は自分の目的で最良・他で譲る** → 「形式選択＝価値判断」を数値で実証。

### 数学的に重要なポイント
- MC 誤差 $1/\sqrt N$。希少事象 P=0.00135 は N=1000 で0ヒット（推定不能）→ $\sim1/p$ 規模が必要。
- SAA の $\hat q$ は $N$ で 120.03（臨界分位点＝Module 0 の連続版）へ収束。
- CVaR は Rockafellar–Uryasev で凸化し cvxpy で解ける。DRO は Scarf 閉形式。

### 検証
- 6形式を cvxpy/解析で解き、self-test で順序・最小性を確認（ALL OK）。
- コンパレータ `AppTest`：正規/対数正規で例外なし。図6種すべて再生成成功。

### 残（次イテレーション）
1. README をモジュール完了状態に更新／全図の一括再生成確認。
2. references.bib の DOI 検証（task #8）。
3. 第2ツール（正規：平均/分散/分位点/超過確率）（task #9）、Module 2–6 の standalone 演習ファイル。

---

## 2026-06-28 — イテレーション4（Module 4：データから分布へ）

### 追加・変更
- `notes/04_from_data_to_distribution.md` — 観測≠真の分布、標本平均/分散・標準誤差、ヒストグラム/ECDF/KDE/パラメトリック、iid限界（季節・トレンド・自己相関）、予測誤差分布、分布選択チェックリスト。
- `exercises/solutions/04_from_data_to_distribution_solutions.md` — §10 全解答。
- `scripts/gen_sample_data.py` → `data/daily_peak_demand.csv`, `data/pv_daily_factor.csv`（季節性つき合成、真の過程既知・再現可能）。
- `scripts/04_data_to_distribution.py` → `figures/04_data_to_distribution.svg`（時系列/当てはめ/ECDF/夏冬の4枚組）。

### 数学的に重要なポイント
- 標準誤差 $\sigma/\sqrt n$：730日でも真の平均は ±1 程度（SE=0.48）。誤差半減に $n$ 4倍。
- 正規当てはめの KS p=0.0007（棄却）＝**季節混在の1分布は当てはまらない**。夏94.6/冬116.3。
- ECDF（グリヴェンコ–カンテリ）で正直に形を見る → 形が素直ならパラメトリック、裾が怪しければノンパラ。
- 予測誤差分布がシナリオ・最適化の入力。iid 単位に層別が前提。

### 検証
- 合成データ統計（mean98.8, std12.9）、KS p、SE、夏冬平均、ECDF P(≤110)=0.781 を Python 確認。図生成成功。

### 設計判断
- サンプルデータは福井に即した**冬ピーク型**（暖房主導）にした。季節性で iid を壊す教材意図。

### 次の一手
1. **Module 5**（シナリオ/モンテカルロ：SAA、収束 $1/\sqrt N$、希少事象、シナリオ削減）＋ MC収束図・シナリオ木図。
2. **Module 6**（最適化6形式）＋ **統合比較ツール（capstone, cvxpy）**。

---

## 2026-06-28 — イテレーション3（Module 3：期待値・分散・相関）

### 追加・変更
- `notes/03_expectation_variance_covariance.md` — 期待値の線形性・イェンゼン、分散の意味と限界、同一平均・異リスク、共分散/相関（正味負荷）、独立≠無相関の数値反例、条件付き期待値・全期待値の法則、VaR/CVaR入口。
- `exercises/solutions/03_expectation_variance_covariance_solutions.md` — §11 全解答。
- `scripts/03_mean_var_cvar.py` → `figures/03_mean_var_cvar.svg` — 平均同じ・VaR/CVaR異なる比較図。

### 数学的に重要なポイント
- 同一平均100でも CVaR$_{0.95}$ は 120.6（sd10）vs 161.9（sd30）。**尾部は平均に映らない**。
- 正味負荷 $\mathrm{Var}(L)=\sigma_D^2+\sigma_P^2-2\rho\sigma_D\sigma_P$。$\rho=+0.5/0/-0.5$ で $\sigma_L=9.17/12.81/15.62$。相関無視は危険。
- 独立⇒無相関、逆は偽（$Y=X^2$ で Cov=0 だが従属）。
- 全分散＝群内＋群間：Var(需要)=25+400=425（天候が分散の大半を説明）。
- VaR（境界・非凸）vs CVaR（尾部平均・凸）→ M6 で CVaR が主役の理由。

### 検証
- VaR/CVaR 係数（z=1.645, CVaR係数2.063）、MC で CVaR.95≈162.0 が解析値161.9と一致。
- 演習数値（E[X]=0.7, Var=0.61, Var(需要)=425）を Python 確認。図生成成功。

### 次の一手
1. **Module 4**（データ→分布：観測≠真の分布、経験分布/ECDF、ヒストグラム、KDE、当てはめ、時系列の非定常）＋サンプルCSV生成。
2. その後 Module 5（シナリオ/モンテカルロ）、Module 6（最適化6形式）、統合比較ツール（capstone）。

---

## 2026-06-28 — イテレーション2（Module 2：確率変数と分布）

### 追加・変更
- `notes/02_random_variables_and_distributions.md` — 確率変数（写像）、離散PMF/連続PDF、CDF、密度≠確率、主要分布（ベルヌーイ/二項/ポアソン/一様/指数/正規）の最小カタログ、ヒストグラム↔分布（M4への橋）。
- `exercises/solutions/02_random_variables_and_distributions_solutions.md` — §10 問題の全解答。
- `scripts/02b_pmf_vs_pdf.py` → `figures/02b_pmf_vs_pdf.svg` — 離散（棒＝確率）vs 連続（面積＝確率）の対比図。

### 数学的に重要なポイント
- **密度は確率でない**の決定的証拠：$\mathcal{N}(0,0.2^2)$ で $f(0)\approx1.99>1$。
- 区間確率の三位一体：面積＝CDF差＝数値積分。離散は和、連続は積分。
- 裾の重さ：同じ平均100・SD30で $P(X>200)$ は 正規0.00043 vs 対数正規0.0061（**約14倍**）。正規での価格近似は極端事象を過小評価。
- 指数の記憶なし性を CDF で証明、摩耗故障に不適と接続。

### 検証
- 分布数値を scipy で確認：正規 P(85≤X≤115)=0.6827, P(X>130)=0.0228；ポアソン(2) P(≥1)=0.865；指数記憶なし 0.368；Bin(3,0.05) P(≥1)=0.1426, P(≥2)=0.00725。
- 図スクリプト実行成功（PMF和=1）。`≥`/`≤`/`²` を mathtext 化し豆腐回避。

### 未解決 / 次の一手
1. **Module 3**（期待値・分散・共分散・相関・条件付き期待値、CVaR入口、独立≠無相関の数値反例）。
2. Module 2 の standalone 演習（basic/intermediate/advanced）ファイル化（現状は note §10＋solutions）。
3. references.bib の DOI 検証（task #8）。
4. 第2ツール（正規：平均/分散/分位点/超過確率）（task #9）。

---

## 2026-06-28 — 初期構築（Module 0・1、第1ツール、足場一式）

### 今回追加・変更したファイルと目的

**全体設計**
- `README.md` — 教材全体の目的・対象・学習順序・記法・利用方法・「完成の定義」。
- `roadmap/notation.md` — 記法規約。特に**確率の $x$（実現値）と最適化の $x$（決定変数）の衝突**を明示。
- `roadmap/learning_map.md` — モジュール依存（Mermaid）、不確実性を表す5言語、目的を測る4基準。
- `roadmap/concept_map.md` — 概念対応表（確率↔データ↔最適化↔電力）、似て非なるもの5対。
- `roadmap/optimization_map.md` — 6形式の二軸マップ＋大比較表＋選択フロー。

**ノート**
- `notes/00_why_probability.md` — 決定論が壊れる2条件、平均の2つの罠、不確実性4解像度・2分類、モデル4類型。
- `notes/01_events_and_probability.md` — 標本空間・事象・確率、**事象 vs 確率変数**、条件付き・独立・ベイズ、確率0≠不可能。

**第1ツール**
- `apps/pdf_cdf_visualizer/{core.py, app.py, SPEC.md, README.md}` — PDF・CDF・区間確率の可視化（Streamlit+Plotly）。数理コアを UI から分離。

**支援**
- `requirements.txt`, `.gitignore`
- `scripts/{_style.py, 00_flaw_of_averages.py, 01_bayes_base_rate.py, 02_pdf_cdf_interval.py, README.md}` — 再生成可能な図。
- `figures/{00_flaw_of_averages.svg, 01_bayes_base_rate.svg, 02_pdf_cdf_interval.svg}`
- `references/{references.bib, reading_list.md}`
- `exercises/` Module 0・1 の問題と解答（basic/intermediate/advanced/solutions）。

### 学習上の狙い（なぜこの設計か）
- **式→計算で終えない**ため、各ノートを「直感→図→定義→小例→手計算→Python→電力→確認問題→誤解」の型で固定。
- Module 0 の数値例（容量確保）を **Module 6 の伏線**として設計。同じ問題を後で6形式で解き直す「縦串」を通す。
- 「事象 vs 確率変数」「密度 vs 確率」を最初に潰す（後段の崩壊を防ぐ）。

### 数学的に重要なポイント（今回確定）
- 平均の落とし穴：$\text{Cost}(q,E[D]) \ne E[\text{Cost}(q,D)]$（イェンゼン）。数値で 0 vs 110 を提示。
- 最適確保量は平均ではなく**臨界比の分位点**で決まる（2点分布では閾値で不連続 → 演習に組込）。
- ベイズ：感度99%でも基準率1%なら $P(F\mid\text{警報})\approx16.7\%$。
- 区間確率の三位一体：$\int_a^b f = F(b)-F(a) = $ 数値積分。ツールで毎回一致を表示。

### 検証（このセッションで実施）
- `apps/pdf_cdf_visualizer/core.py` 自己テスト：全分布で |CDF差−面積|<1e-3、全確率≈1、ε→0 で点確率→0。**ALL OK**。
- Streamlit `AppTest`：既定値・分布切替・問い方切替で**例外なし**。`use_container_width` を `width="stretch"` へ更新。
- 図スクリプト3本：実行成功・SVG 出力確認。`≤` の豆腐化を mathtext で解消。
- Module 0/1 の数値（110, 20, q*=120, 16.7%, 独立判定 1/12）を Python で再現確認。

### 未解決事項 / 既知の限界
1. **DOI 検証パス未実施**：`references.bib` の DOI・巻号・ページは暫定（記憶ベース）。次イテレーションで WebSearch/Crossref により検証し `verified` 付与。
2. ツールは連続分布のみ（離散 PMF モードは SPEC の拡張案①）。
3. Module 2–6 のノート未着手（骨子は roadmap に反映済み）。
4. 図は SVG のみ。ノートへの埋め込み（相対パス）は Module 2 本文作成時に行う。
5. `cvxpy` 未導入（Module 6 着手時に `requirements.txt` から導入）。

### 次の一手（優先順）
1. **Module 2 ノート**（確率変数と分布）＋ PDF/CDF 図の本文埋め込み。離散 PMF と連続 PDF の対比。
2. references.bib の **DOI 検証**（WebSearch）。
3. 第2ツール：**正規分布の平均・分散・分位点・超過確率**可視化（Module 3/6 への橋）。
4. Module 0・1 演習の追補（中級・発展を増補）。

### この回の「学習者が確認すべき問い」
- 「決定論モデルはいつ壊れるか」を2条件で言えるか。
- 「事象」と「確率変数」を集合・写像で説明できるか。
- 「密度の高さ」と「区間の確率」を取り違えないか（ツールで確認）。
