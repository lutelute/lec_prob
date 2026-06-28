---
title: ブラウザで動かす（インタラクティブ・ツール）
---

# ▶ ブラウザで動かす — インタラクティブ・ツール

**インストール不要・その場で動く**ツール群です。スライダーを動かすと図と数値が即座に更新されます。
すべてブラウザ内（JavaScript + Plotly.js）で完結し、GitHub Pages 上でそのまま動作します。
数理は教材の数値と一致するよう検証済み（[`interactive/lib/stats.js`](lib/stats.js)）。

> 各ツールは下に**埋め込み表示**されます。広い画面で使いたいときは「**全画面で開く**」を押してください。

---

## 1. PDF・CDF・区間確率ビジュアライザ（Module 2）

確率は密度の「高さ」ではなく区間の「**面積**」。その面積は CDF の「**差**」でもある——を体感する。
正規／対数正規／指数／一様を切り替え、区間・点プローブを動かして「密度≠確率」を確かめる。

[▶ 全画面で開く](pdf_cdf.html){target=_blank}

<iframe src="pdf_cdf.html" title="PDF・CDF・区間確率" loading="lazy"
  style="width:100%;height:880px;border:1px solid #dadce0;border-radius:10px;margin:8px 0"></iframe>

関連ノート：[Module 2 確率変数と分布](../notes/02_random_variables_and_distributions.md)。

---

## 2. ベイズ更新ビジュアライザ — 基準率の誤謬（Module 1）

感度99%の優秀な警報でも、故障が稀なら「警報＝本物」とは限らない。事前確率・感度・誤警報率を動かし、
事後確率・1000件の内訳・事後vs基準率曲線・逐次更新を観察する。

[▶ 全画面で開く](bayes.html){target=_blank}

<iframe src="bayes.html" title="ベイズ更新・基準率の誤謬" loading="lazy"
  style="width:100%;height:900px;border:1px solid #dadce0;border-radius:10px;margin:8px 0"></iframe>

関連ノート：[Module 1 事象と確率](../notes/01_events_and_probability.md)。

---

## 3. モンテカルロ収束ビジュアライザ（Module 5）

平均は 1/√N で速く収束、希少事象（尾）は遅い、SAA はシナリオ数で収束——を3モードで体感する。
「🎲 再サンプリング」で、モンテカルロ自体のばらつき（特に小N・希少事象）を観察する。

[▶ 全画面で開く](montecarlo.html){target=_blank}

<iframe src="montecarlo.html" title="モンテカルロ収束" loading="lazy"
  style="width:100%;height:760px;border:1px solid #dadce0;border-radius:10px;margin:8px 0"></iframe>

関連ノート：[Module 5 シナリオとモンテカルロ](../notes/05_scenarios_and_monte_carlo.md)。

---

> このページは順次拡充します。今後追加予定：6形式コンパレータ、蓄電池運用。
> 進捗は [development log](../development_log.md) を参照。
