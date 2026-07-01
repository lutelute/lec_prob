/* steps.js — 触って学ぶツール共通：5ステップ誘導エンジン（依存なし）
 * 使い方：
 *   const wiz = LPSteps.create({
 *     steps: [{key:'prob', t:'問題', c:'var(--blue)'}, ...],
 *     autoKey: 'vary',               // このstepの間だけ自動再生を許す（省略可）
 *     onEnter: (key, idx) => {...},  // ステップに入る瞬間に1回だけ呼ばれる。既定値の設定などステップ固有の準備はここで
 *     onRender: (key, idx) => {...}, // 状態が変わるたび（ステップ遷移・スライダー操作の両方）に呼ばれる。描画・説明文の更新
 *     onAutoTick: () => {...},       // 自動再生の1フレーム。状態を更新し必要な再描画を行うこと
 *     ids: {stepper,prev,next,auto,reset}  // 省略時は既定のid名を使う
 *   });
 *   wiz.goStep(0);   // 初期表示
 *   wiz.stopAuto();  // スライダー等をユーザーが直接動かしたら呼ぶ
 *
 * 担当範囲：ステップタブの描画・前へ/次へ/自動ボタンの配線・自動再生ループ・ステップ番号の状態管理のみ。
 * パラメータの既定値やリセット時の値はツール側の責務（stepIdx===0への遷移はツールがresetBtnで呼ぶ）。
 */
window.LPSteps = (function () {
  function create(opts) {
    var steps = opts.steps;
    var autoKey = opts.autoKey || null;
    var onEnter = opts.onEnter || function () {};
    var onRender = opts.onRender || function () {};
    var onAutoTick = opts.onAutoTick || function () {};
    var ids = Object.assign({ stepper: 'stepper', prev: 'prevBtn', next: 'nextBtn', auto: 'autoBtn' }, opts.ids || {});
    var $ = function (id) { return document.getElementById(id); };
    var stepIdx = 0;
    var auto = false;

    function renderStepper() {
      var el = $(ids.stepper);
      if (!el) return;
      el.innerHTML = steps.map(function (s, i) {
        var cls = 'stp' + (i === stepIdx ? ' active' : (i < stepIdx ? ' done' : ''));
        return '<button type="button" class="' + cls + '" data-i="' + i + '" role="tab" aria-selected="' + (i === stepIdx) + '" style="--c:' + s.c + '">' +
          '<span class="n">' + (i < stepIdx ? '✓' : (i + 1)) + '</span><span class="t">' + s.t + '</span></button>';
      }).join('');
      el.querySelectorAll('.stp').forEach(function (b) {
        b.addEventListener('click', function () { goStep(+b.dataset.i); });
      });
    }

    function updateNavButtons() {
      if ($(ids.prev)) $(ids.prev).disabled = (stepIdx === 0);
      if ($(ids.next)) $(ids.next).disabled = (stepIdx === steps.length - 1);
    }

    function stopAuto() {
      auto = false;
      if ($(ids.auto)) $(ids.auto).textContent = '⏵ 自動';
    }
    function startAuto() {
      if (auto) return;
      auto = true;
      if ($(ids.auto)) $(ids.auto).textContent = '⏸ 停止';
      requestAnimationFrame(tick);
    }
    function tick() {
      if (!auto) return;
      onAutoTick();
      requestAnimationFrame(tick);
    }

    function goStep(i) {
      i = Math.max(0, Math.min(steps.length - 1, i));
      stepIdx = i;
      var key = steps[i].key;
      if (key !== autoKey) stopAuto();
      onEnter(key, i);
      renderStepper();
      updateNavButtons();
      onRender(key, i);
      if (key === autoKey) startAuto();
    }

    if ($(ids.prev)) $(ids.prev).addEventListener('click', function () { goStep(stepIdx - 1); });
    if ($(ids.next)) $(ids.next).addEventListener('click', function () { goStep(stepIdx + 1); });
    if ($(ids.auto)) $(ids.auto).addEventListener('click', function () {
      if (auto) { stopAuto(); }
      else if (autoKey && steps[stepIdx].key !== autoKey) {
        goStep(steps.findIndex(function (s) { return s.key === autoKey; }));
      } else { startAuto(); }
    });

    return {
      goStep: goStep,
      stopAuto: stopAuto,
      startAuto: startAuto,
      stepIdx: function () { return stepIdx; },
      key: function () { return steps[stepIdx].key; }
    };
  }
  return { create: create };
})();
