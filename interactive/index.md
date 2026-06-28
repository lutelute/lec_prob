---
title: ブラウザで動かす（インタラクティブ・ツール）
---

# ▶ ブラウザで動かす — インタラクティブ・ツール

**インストール不要・その場で動く**ツール群です。スライダーを動かすと図と数値が即座に更新されます。
すべてブラウザ内（JavaScript + Plotly.js）で完結し、GitHub Pages 上でそのまま動作します。
数理は教材の数値と一致するよう検証済み（[`interactive/lib/stats.js`](lib/stats.js)）。

> 各ツールは下に**埋め込み表示**されます。広い画面で使いたいときは「**全画面で開く**」を押してください。

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:18px 0">
  <a href="#t1" style="display:block;padding:12px 14px;border:1px solid #dadce0;border-radius:10px;text-decoration:none;color:inherit;border-left:4px solid #4285f4"><b>① PDF・CDF・区間確率</b><br><span style="color:#5f6368;font-size:.85em">密度≠確率・面積＝CDF差（M2）</span></a>
  <a href="#t2" style="display:block;padding:12px 14px;border:1px solid #dadce0;border-radius:10px;text-decoration:none;color:inherit;border-left:4px solid #34a853"><b>② ベイズ更新</b><br><span style="color:#5f6368;font-size:.85em">基準率の誤謬（M1）</span></a>
  <a href="#t3" style="display:block;padding:12px 14px;border:1px solid #dadce0;border-radius:10px;text-decoration:none;color:inherit;border-left:4px solid #a142f4"><b>③ モンテカルロ収束</b><br><span style="color:#5f6368;font-size:.85em">1/√N・希少事象・SAA（M5）</span></a>
  <a href="#t4" style="display:block;padding:12px 14px;border:1px solid #dadce0;border-radius:10px;text-decoration:none;color:inherit;border-left:4px solid #ea4335"><b>④ 6形式コンパレータ</b><br><span style="color:#5f6368;font-size:.85em">到達点：x*が100〜137（M6）</span></a>
  <a href="#t5" style="display:block;padding:12px 14px;border:1px solid #dadce0;border-radius:10px;text-decoration:none;color:inherit;border-left:4px solid #f9ab00"><b>⑤ 蓄電池運用</b><br><span style="color:#5f6368;font-size:.85em">SoC・アービトラージ（M6b）</span></a>
</div>

---

## 1. PDF・CDF・区間確率ビジュアライザ（Module 2） {#t1}

確率は密度の「高さ」ではなく区間の「**面積**」。その面積は CDF の「**差**」でもある——を体感する。
正規／対数正規／指数／一様を切り替え、区間・点プローブを動かして「密度≠確率」を確かめる。

[▶ 全画面で開く](pdf_cdf.html){target=_blank}

<iframe src="pdf_cdf.html" title="PDF・CDF・区間確率" loading="lazy" data-fit
  style="width:100%;height:1500px;border:1px solid #dadce0;border-radius:10px;margin:8px 0"></iframe>

関連ノート：[Module 2 確率変数と分布](../notes/02_random_variables_and_distributions.md)。

---

## 2. ベイズ更新ビジュアライザ — 基準率の誤謬（Module 1） {#t2}

感度99%の優秀な警報でも、故障が稀なら「警報＝本物」とは限らない。事前確率・感度・誤警報率を動かし、
事後確率・1000件の内訳・事後vs基準率曲線・逐次更新を観察する。

[▶ 全画面で開く](bayes.html){target=_blank}

<iframe src="bayes.html" title="ベイズ更新・基準率の誤謬" loading="lazy" data-fit
  style="width:100%;height:1560px;border:1px solid #dadce0;border-radius:10px;margin:8px 0"></iframe>

関連ノート：[Module 1 事象と確率](../notes/01_events_and_probability.md)。

---

## 3. モンテカルロ収束ビジュアライザ（Module 5） {#t3}

平均は 1/√N で速く収束、希少事象（尾）は遅い、SAA はシナリオ数で収束——を3モードで体感する。
「🎲 再サンプリング」で、モンテカルロ自体のばらつき（特に小N・希少事象）を観察する。

[▶ 全画面で開く](montecarlo.html){target=_blank}

<iframe src="montecarlo.html" title="モンテカルロ収束" loading="lazy" data-fit
  style="width:100%;height:1200px;border:1px solid #dadce0;border-radius:10px;margin:8px 0"></iframe>

関連ノート：[Module 5 シナリオとモンテカルロ](../notes/05_scenarios_and_monte_carlo.md)。

---

## 4. 確率的最適化コンパレータ — 6形式（Module 6・到達点） {#t4}

同じ容量調達問題を **決定論／期待値／ロバスト／チャンス制約／CVaR／分布ロバスト** の6形式で解き、
最適決定 x* が **100〜137** と変わるのを体感する。コスト非対称性・ε・α・k を動かして「なぜこの形式を選ぶか」を学ぶ。

[▶ 全画面で開く](comparator.html){target=_blank}

<iframe src="comparator.html" title="6形式コンパレータ" loading="lazy" data-fit
  style="width:100%;height:1500px;border:1px solid #dadce0;border-radius:10px;margin:8px 0"></iframe>

関連ノート：[Module 6 不確実性下の最適化](../notes/06_optimization_under_uncertainty.md)。

---

## 5. 蓄電池運用ビジュアライザ — アービトラージと SoC（Module 6b） {#t5}

安いとき充電・高いとき放電。蓄電池の SoC ダイナミクスを可視化し、価格プロファイル・容量・効率・閾値を動かして
「エネルギーの時間シフトで価値を生む」を体感する。

[▶ 全画面で開く](battery.html){target=_blank}

<iframe src="battery.html" title="蓄電池運用" loading="lazy" data-fit
  style="width:100%;height:780px;border:1px solid #dadce0;border-radius:10px;margin:8px 0"></iframe>

関連ノート：[Module 6b 二段階確率計画](../notes/06b_two_stage_stochastic_programming.md)。

---

> **5本すべてブラウザ内で動作**します（インストール不要）。Streamlit版（ローカル/Community Cloud 実行）の解説は各 `apps/*/` を参照。

<script>
// 同一オリジンの iframe を中身の高さに自動フィット（内部スクロール・余白を解消、内容変更に追従）
(function(){
  function fit(f){ try{ var h=f.contentDocument.body.scrollHeight; if(h>120) f.style.height=(h+16)+'px'; }catch(e){} }
  function fitAll(){ document.querySelectorAll('iframe[data-fit]').forEach(fit); }
  document.querySelectorAll('iframe[data-fit]').forEach(function(f){
    f.addEventListener('load', function(){ fit(f); [300,800,1600].forEach(function(d){ setTimeout(function(){ fit(f); }, d); }); });
  });
  var t; window.addEventListener('resize', function(){ clearTimeout(t); t=setTimeout(fitAll, 250); });
  setTimeout(fitAll, 1000);
})();
</script>
> 進捗は [development log](../development_log.md) を参照。
