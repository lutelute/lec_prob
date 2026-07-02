---
title: ブラウザで動かす（インタラクティブ・ツール）
---

# ▶ ブラウザで動かす — インタラクティブ・ツール

<p class="lead" style="font-size:.72rem;max-width:44rem"><b>インストール不要・その場で動く</b>ツール群。各ツールの「<b>▶ ここで動かす</b>」を押すと読み込まれ、<b>スライダーを動かすと図と数値が即座に変わります</b>。すべてブラウザ内（JavaScript + Plotly.js）で完結。広い画面で使うなら各ツールの「全画面で開く」から。</p>

!!! note "はじめての人は：[学習コース（順番に触る・進捗つき）](course.html){target=_blank}"
    **読む→触る→自分の問題で使う→確かめる**の一本道（約40分）。迷ったらここから。

    実務で使うなら → [決定計算機](calculator.html){target=_blank}（在庫・予備力・発注を実データで）／[やる・やらない計算機](gonogo.html){target=_blank}（成功確率と損得で判断）。
    確率的最適化6形式を俯瞰したいなら → [手法マップ](map.html){target=_blank}（依存関係を対話的に）／[ブループリント](blueprint.html){target=_blank}（1枚の仕様書・印刷可）。

<div class="cards c3" style="margin:18px 0">
  <a class="card" href="#t1"><span class="ch"><span class="nm">① PDF・CDF・区間確率</span><span class="kd">第2章</span></span><span class="tags"><span class="tag t-sp">連続分布</span><span class="tag t-sp">面積＝確率</span></span><span class="use">密度≠確率・面積＝CDF差</span></a>
  <a class="card" href="#t2"><span class="ch"><span class="nm">② ベイズ更新</span><span class="kd">第1章</span></span><span class="tags"><span class="tag t-ev">事象</span><span class="tag t-ev">条件付き</span></span><span class="use">基準率の誤謬</span></a>
  <a class="card" href="#t3"><span class="ch"><span class="nm">③ モンテカルロ収束</span><span class="kd">第5章</span></span><span class="tags"><span class="tag t-me">1/√N</span><span class="tag t-me">SAA</span></span><span class="use">収束・希少事象</span></a>
  <a class="card" href="#t4"><span class="ch"><span class="nm">④ 6形式の解剖</span><span class="kd">第6章 · 数式×図</span></span><span class="tags"><span class="tag t-op">項⇔図が光る</span><span class="tag t-op">意味の結合</span></span><span class="use">数式のどこが図のどこか</span></a>
  <a class="card" href="#t5"><span class="ch"><span class="nm">⑤ 6形式コンパレータ</span><span class="kd">第6章 · 到達点</span></span><span class="tags"><span class="tag t-op">最適化</span><span class="tag t-op">x*=100〜137</span></span><span class="use">形式の選択で決定が変わる</span></a>
  <a class="card" href="#t6"><span class="ch"><span class="nm">⑥ 蓄電池運用</span><span class="kd">第6b章</span></span><span class="tags"><span class="tag t-to">SoC</span><span class="tag t-to">予測の価値</span></span><span class="use">アービトラージ・EVPI直感</span></a>
  <a class="card" href="#t7"><span class="ch"><span class="nm">⑦ 理解度チェック</span><span class="kd">ALL</span></span><span class="tags"><span class="tag t-er">10問</span></span><span class="use">どこを復習すべきかが分かる</span></a>
</div>

---

## 1. PDF・CDF・区間確率ビジュアライザ（第2章） {#t1}

確率は密度の「高さ」ではなく区間の「**面積**」。その面積は CDF の「**差**」でもある——を体感する。
正規／対数正規／指数／一様を切り替え、区間・点プローブを動かして「密度≠確率」を確かめる。

[▶ 全画面で開く](pdf_cdf.html){target=_blank} ／ [第2章のノート](../notes/02_random_variables_and_distributions.md)

<div class="tool-embed" data-src="pdf_cdf.html" data-h="1540"></div>

---

## 2. ベイズ更新ビジュアライザ — 基準率の誤謬（第1章） {#t2}

感度99%の優秀な警報でも、故障が稀なら「警報＝本物」とは限らない。事前確率・感度・誤警報率を動かし、
事後確率・1000件の内訳・逐次更新を観察する。

[▶ 全画面で開く](bayes.html){target=_blank} ／ [第1章のノート](../notes/01_events_and_probability.md)

<div class="tool-embed" data-src="bayes.html" data-h="1600"></div>

---

## 3. モンテカルロ収束ビジュアライザ（第5章） {#t3}

平均は 1/√N で速く収束、希少事象（尾）は遅い、SAA はシナリオ数で収束——を3モードで体感する。
「🎲 再サンプリング」で、モンテカルロ自体のばらつきを観察する。

[▶ 全画面で開く](montecarlo.html){target=_blank} ／ [第5章のノート](../notes/05_scenarios_and_monte_carlo.md)

<div class="tool-embed" data-src="montecarlo.html" data-h="1220"></div>

---

## 4. 6形式の解剖 — 数式のどこが、図のどこか（第6章） {#t4}

6形式の**数式・図・意味を強く結ぶ**。形式を切り替えると数式と図が同時に変わり、
**数式の下線の項に触れると、図の対応する場所が光る**。スライダーで数式内の数値と最適解 x* が即応。
コンパレータの**前に**触ると、6本のバーの意味が数式から読めるようになる。

[▶ 全画面で開く](anatomy.html){target=_blank} ／ [第6章のノート](../notes/06_optimization_under_uncertainty.md)

<div class="tool-embed" data-src="anatomy.html" data-h="1000"></div>

---

## 5. 確率的最適化コンパレータ — 6形式（第6章・到達点） {#t5}

同じ容量調達問題を **決定論／期待値／ロバスト／チャンス制約／CVaR／分布ロバスト** の6形式で解き、
最適決定 x* が **100〜137** と変わるのを体感する。コスト非対称性・ε・α・k を動かす。

[▶ 全画面で開く](comparator.html){target=_blank} ／ [第6章のノート](../notes/06_optimization_under_uncertainty.md)

<div class="tool-embed" data-src="comparator.html" data-h="1520"></div>

---

## 6. 蓄電池運用ビジュアライザ — アービトラージと SoC（第6b章） {#t6}

安いとき充電・高いとき放電。SoC ダイナミクスを可視化し、価格・容量・効率・閾値を動かす。
価格予測誤差 σ を上げると「予測の価値（EVPI 直感）」も現れる。

[▶ 全画面で開く](battery.html){target=_blank} ／ [第6b章のノート](../notes/06b_two_stage_stochastic_programming.md)

<div class="tool-embed" data-src="battery.html" data-h="900"></div>

---

## 7. 理解度チェック — 触って確かめる10問（全章） {#t7}

学んだことが身についたか、10問で確かめる。選ぶと正誤と解説が出て、**どこを復習すればよいか**が分かる。
密度≠確率・基準率の誤謬・形式選択・平均の罠・1/√N・偶然/認識・CVaR・EVPI を横断。

[▶ 全画面で開く](quiz.html){target=_blank}

<div class="tool-embed" data-src="quiz.html" data-h="560"></div>

---

> **9本すべてブラウザ内で動作**します（インストール不要）。Streamlit版（ローカル実行）の解説は各 `apps/*/` を参照。

<style>
.tool-embed{margin:10px 0}
.tool-embed .ld-btn{display:inline-flex;align-items:center;gap:8px;cursor:pointer;
  border:1px solid var(--ink);background:var(--ink);color:#fff;font-weight:700;font-size:.95rem;
  padding:13px 22px;border-radius:0;font-family:var(--jp)}
.tool-embed .ld-btn:hover{background:#000}
.tool-embed .ld-hint{display:block;color:var(--ink-3);font-size:.8rem;margin-top:6px}
.tool-embed iframe{width:100%;border:1px solid var(--ink);border-radius:0;background:#fff}
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
  });
})();
</script>
