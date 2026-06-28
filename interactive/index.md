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

> このページは順次拡充します。今後追加予定：ベイズ更新、モンテカルロ収束、6形式コンパレータ、蓄電池運用。
> 進捗は [development log](../development_log.md) を参照。
