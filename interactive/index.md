---
title: ブラウザで動かす（インタラクティブ・ツール）
---

# ▶ ブラウザで動かす — インタラクティブ・ツール

**インストール不要・その場で動く**ツール群です。各ツールの「**▶ ここで動かす**」ボタンを押すと読み込まれ、
**スライダーを動かすと図と数値が即座に変わります**。すべてブラウザ内（JavaScript + Plotly.js）で完結します。

!!! note "🎓 はじめての人は：[学習コース（順番に触る・進捗つき）](course.html){target=_blank}"
    **読む→触る→自分の問題で使う→確かめる**の一本道（約40分）。開いた項目に ✓ が付き、「▶ 次はこれ」が光ります。迷ったらここから。

!!! success "🧮 実務で使う計算機（学習デモでなく、実際の決定に）"
    - **[決定計算機](calculator.html){target=_blank}**：自分の需要データ＋コスト → 6形式の推奨確保量・供給不足確率・期待コストを表で出しCSV/印刷。「どれだけ確保するか」（在庫・予備力・発注）。
    - **[やる/やらない計算機](gonogo.html){target=_blank}**：成功確率と損得 → 期待値・**損益分岐確率**・後悔で「やるべきか」。（投資・新製品・設備更新）。
    計算はすべて手元のブラウザ内。

!!! tip "まず全体像を俯瞰したいなら"
    🗺 **[全体地図（2D俯瞰アトラス）](map.html){target=_blank}** … 全概念・ツールを2次元配置、ミニ可視化カード＋カテゴリゾーン＋推奨順路。クリックで各ページへ。
    📐 **[全体ブループリント（仕様書版）](blueprint.html){target=_blank}** … モノスペースの技術設計図（印刷可）。
    どちらも概念・モジュール・8ツールを1枚で俯瞰できます。

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:18px 0">
  <a href="#t1" style="display:block;padding:12px 14px;border:1px solid #dadce0;border-radius:10px;text-decoration:none;color:inherit;border-left:4px solid #4285f4"><b>① PDF・CDF・区間確率</b><br><span style="color:#5f6368;font-size:.85em">密度≠確率・面積＝CDF差（M2）</span></a>
  <a href="#t2" style="display:block;padding:12px 14px;border:1px solid #dadce0;border-radius:10px;text-decoration:none;color:inherit;border-left:4px solid #34a853"><b>② ベイズ更新</b><br><span style="color:#5f6368;font-size:.85em">基準率の誤謬（M1）</span></a>
  <a href="#t3" style="display:block;padding:12px 14px;border:1px solid #dadce0;border-radius:10px;text-decoration:none;color:inherit;border-left:4px solid #a142f4"><b>③ モンテカルロ収束</b><br><span style="color:#5f6368;font-size:.85em">1/√N・希少事象・SAA（M5）</span></a>
  <a href="#t4" style="display:block;padding:12px 14px;border:1px solid #dadce0;border-radius:10px;text-decoration:none;color:inherit;border-left:4px solid #ea4335"><b>④ 6形式コンパレータ</b><br><span style="color:#5f6368;font-size:.85em">到達点：x*が100〜137（M6）</span></a>
  <a href="#t5" style="display:block;padding:12px 14px;border:1px solid #dadce0;border-radius:10px;text-decoration:none;color:inherit;border-left:4px solid #f9ab00"><b>⑤ 蓄電池運用</b><br><span style="color:#5f6368;font-size:.85em">SoC・アービトラージ（M6b）</span></a>
  <a href="#t6" style="display:block;padding:12px 14px;border:1px solid #dadce0;border-radius:10px;text-decoration:none;color:inherit;border-left:4px solid #00897b"><b>⑥ 理解度チェック</b><br><span style="color:#5f6368;font-size:.85em">8問で確かめる（全体）</span></a>
</div>

!!! tip "使い方"
    各ツールの「**▶ ここで動かす**」を押す → ツールが下に開く → **左のスライダーを動かす**と右の図・数値がリアルタイムで更新されます。広い画面で使うなら「**全画面で開く**」。

---

## 1. PDF・CDF・区間確率ビジュアライザ（Module 2） {#t1}

確率は密度の「高さ」ではなく区間の「**面積**」。その面積は CDF の「**差**」でもある——を体感する。
正規／対数正規／指数／一様を切り替え、区間・点プローブを動かして「密度≠確率」を確かめる。

[▶ 全画面で開く](pdf_cdf.html){target=_blank} ／ [Module 2 のノート](../notes/02_random_variables_and_distributions.md)

<div class="tool-embed" data-src="pdf_cdf.html" data-h="1540"></div>

---

## 2. ベイズ更新ビジュアライザ — 基準率の誤謬（Module 1） {#t2}

感度99%の優秀な警報でも、故障が稀なら「警報＝本物」とは限らない。事前確率・感度・誤警報率を動かし、
事後確率・1000件の内訳・逐次更新を観察する。

[▶ 全画面で開く](bayes.html){target=_blank} ／ [Module 1 のノート](../notes/01_events_and_probability.md)

<div class="tool-embed" data-src="bayes.html" data-h="1600"></div>

---

## 3. モンテカルロ収束ビジュアライザ（Module 5） {#t3}

平均は 1/√N で速く収束、希少事象（尾）は遅い、SAA はシナリオ数で収束——を3モードで体感する。
「🎲 再サンプリング」で、モンテカルロ自体のばらつきを観察する。

[▶ 全画面で開く](montecarlo.html){target=_blank} ／ [Module 5 のノート](../notes/05_scenarios_and_monte_carlo.md)

<div class="tool-embed" data-src="montecarlo.html" data-h="1220"></div>

---

## 4. 確率的最適化コンパレータ — 6形式（Module 6・到達点） {#t4}

同じ容量調達問題を **決定論／期待値／ロバスト／チャンス制約／CVaR／分布ロバスト** の6形式で解き、
最適決定 x* が **100〜137** と変わるのを体感する。コスト非対称性・ε・α・k を動かす。

[▶ 全画面で開く](comparator.html){target=_blank} ／ [Module 6 のノート](../notes/06_optimization_under_uncertainty.md)

<div class="tool-embed" data-src="comparator.html" data-h="1520"></div>

---

## 5. 蓄電池運用ビジュアライザ — アービトラージと SoC（Module 6b） {#t5}

安いとき充電・高いとき放電。SoC ダイナミクスを可視化し、価格・容量・効率・閾値を動かす。
価格予測誤差 σ を上げると「予測の価値（EVPI 直感）」も現れる。

[▶ 全画面で開く](battery.html){target=_blank} ／ [Module 6b のノート](../notes/06b_two_stage_stochastic_programming.md)

<div class="tool-embed" data-src="battery.html" data-h="900"></div>

---

## 6. 理解度チェック — 触って確かめる8問（全モジュール） {#t6}

学んだことが身についたか、8問で確かめる。選ぶと正誤と解説が出て、**どこを復習すればよいか**が分かる。
密度≠確率・基準率の誤謬・形式選択・平均の罠・1/√N・偶然/認識・CVaR・EVPI を横断。

[▶ 全画面で開く](quiz.html){target=_blank}

<div class="tool-embed" data-src="quiz.html" data-h="560"></div>

---

> **8本すべてブラウザ内で動作**します（インストール不要）。Streamlit版（ローカル実行）の解説は各 `apps/*/` を参照。

<style>
.tool-embed{margin:10px 0}
.tool-embed .ld-btn{display:inline-flex;align-items:center;gap:8px;cursor:pointer;border:0;
  background:#4285f4;color:#fff;font-weight:700;font-size:1rem;padding:14px 22px;border-radius:10px}
.tool-embed .ld-btn:hover{background:#3367d6}
.tool-embed .ld-hint{display:block;color:#5f6368;font-size:.85rem;margin-top:6px}
.tool-embed iframe{width:100%;border:1px solid #dadce0;border-radius:10px}
</style>
<script>
(function(){
  function load(box){
    var src=box.dataset.src, h=box.dataset.h||'1200';
    var f=document.createElement('iframe');
    f.src=src; f.style.height=h+'px'; f.setAttribute('title',src);
    f.addEventListener('load',function(){
      function fit(){ try{var hh=f.contentDocument.body.scrollHeight; if(hh>120) f.style.height=(hh+16)+'px';}catch(e){} }
      [200,800,1600].forEach(function(d){ setTimeout(fit,d); });
    });
    box.innerHTML=''; box.appendChild(f);
  }
  document.querySelectorAll('.tool-embed').forEach(function(box){
    var btn=document.createElement('button'); btn.className='ld-btn'; btn.type='button';
    btn.innerHTML='▶ ここで動かす（読み込む）';
    var hint=document.createElement('span'); hint.className='ld-hint';
    hint.textContent='ボタンを押すとツールが開きます。スライダーを動かすと図がリアルタイムで変わります。';
    btn.addEventListener('click',function(){ load(box); });
    box.appendChild(btn); box.appendChild(hint);
    // アンカー(#tN)で来たら自動で読み込む
    if(location.hash && document.querySelector(location.hash) &&
       document.querySelector(location.hash).parentElement &&
       document.querySelector(location.hash).closest('h2') &&
       box.previousElementSibling){ /* no-op: 明示クリックに任せる */ }
  });
})();
</script>
