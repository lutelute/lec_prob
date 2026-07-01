/* a11y.js — インタラクティブツール共通のアクセシビリティ強化（依存なし）
 * スライダーへ aria-label、出力へ aria-live、セグメントへ aria-pressed、図へ role=img を自動付与。
 * 各ツールで <script src="lib/a11y.js"></script> を読むだけ。
 */
(function () {
  function clean(s) { return (s || '').replace(/\s+/g, ' ').trim(); }
  function run() {
    // レンジスライダー：直近の label からアクセシブル名を付与
    document.querySelectorAll('input[type=range]').forEach(function (r) {
      if (!r.getAttribute('aria-label')) {
        var box = r.closest('.ctl') || r.parentElement;
        var lab = box && box.querySelector('label');
        if (lab) {
          var t = lab.cloneNode(true);
          t.querySelectorAll('.val').forEach(function (v) { v.remove(); }); // 現在値spanは除外（SRはスライダー値を別途読む）
          r.setAttribute('aria-label', clean(t.textContent));
        }
      }
    });
    // 出力（指標・注釈・推奨・感度・導出）：値の変化を読み上げ
    document.querySelectorAll('.metrics, #note, .note, .summ, .rec, #sens, #marg, #outv, #tableWrap').forEach(function (el) {
      if (!el.getAttribute('aria-live')) el.setAttribute('aria-live', 'polite');
    });
    // セグメント切替：role=button + aria-pressed（class 'on' を監視して同期）
    var segBtns = document.querySelectorAll('.seg button, .seg2 button');
    segBtns.forEach(function (b) {
      b.setAttribute('role', 'button');
      b.setAttribute('aria-pressed', b.classList.contains('on') ? 'true' : 'false');
    });
    if (segBtns.length) {
      var mo = new MutationObserver(function (muts) {
        muts.forEach(function (m) {
          var b = m.target;
          if (b.matches && b.matches('.seg button, .seg2 button'))
            b.setAttribute('aria-pressed', b.classList.contains('on') ? 'true' : 'false');
        });
      });
      segBtns.forEach(function (b) { mo.observe(b, { attributes: true, attributeFilter: ['class'] }); });
    }
    // Plotly 図：スクリーンリーダ向けに役割と説明
    document.querySelectorAll('.plot').forEach(function (p) {
      if (!p.getAttribute('role')) {
        p.setAttribute('role', 'img');
        p.setAttribute('aria-label', 'インタラクティブな図。数値は近くの指標・表に文字で表示されます。');
      }
    });
    // メインコンテンツにランドマーク（スクリーンリーダが本文へ直接移動できる）
    var wrap = document.querySelector('.wrap');
    if (wrap && !wrap.getAttribute('role')) wrap.setAttribute('role', 'main');
    // 全画面で開いたとき（iframe埋め込みでない）だけ、戻り導線フッターを出す
    try {
      if (window.self === window.top && !document.querySelector('.lp-toolnav')) {
        var host = document.querySelector('.wrap') || document.body;
        var nav = document.createElement('nav');
        nav.className = 'lp-toolnav';
        nav.setAttribute('aria-label', '戻る');
        nav.innerHTML = '← <a href="course.html">🎓 学習コース</a> · <a href="map.html">🗺 手法マップ</a> · <a href="../">🏠 ホーム</a>';
        host.appendChild(nav);
      }
    } catch (e) {}
  }
  if (document.readyState !== 'loading') run();
  else document.addEventListener('DOMContentLoaded', run);
})();
