/* stats.test.mjs — interactive/lib/stats.js の数値テスト（Node 実行・依存なし）
 * 期待値は scipy で確定（教材の数値と一致）。実行: node interactive/lib/stats.test.mjs
 * すべてのインタラクティブツールは stats.js に依存するため、ここが正しければ各ツールの数理も正しい。
 */
import { readFileSync } from 'node:fs';
import { createContext, runInContext } from 'node:vm';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const code = readFileSync(join(here, 'stats.js'), 'utf8');
const ctx = { window: {} };
createContext(ctx);
runInContext(code, ctx);          // stats.js は window.LP に公開
const L = ctx.window.LP;

let pass = 0, fail = 0;
const approx = (name, got, exp, tol = 1e-4) => {
  if (Number.isFinite(got) && Math.abs(got - exp) <= tol) { pass++; }
  else { fail++; console.error(`✗ ${name}: got ${got}, expected ${exp} (±${tol})`); }
};

// 正規分布（教材の中心例 N(100,15)）— 期待値は scipy
approx('normCdf(115;100,15)', L.normCdf(115, 100, 15), 0.841345);
approx('normCdf(85;100,15)',  L.normCdf(85, 100, 15), 0.158655);
approx('P(85<=X<=115)=68.27%', L.normCdf(115,100,15) - L.normCdf(85,100,15), 0.682689);
approx('normPdf(100;100,15)', L.normPdf(100, 100, 15), 0.026596);
approx('normPpf(0.8;100,15)', L.normPpf(0.8, 100, 15), 112.624319, 1e-2);
approx('normPpf(0.95;100,15)', L.normPpf(0.95, 100, 15), 124.672804, 1e-2);
approx('normSInv(0.975)', L.normSInv(0.975), 1.959964, 1e-3);

// 指数・一様・対数正規
approx('expCdf(1;rate1)', L.expCdf(1, 1), 0.632121);
approx('uniCdf(0.3;0,1)', L.uniCdf(0.3, 0, 1), 0.300000);
approx('lnPdf(50;mean60,sd30)', L.lnPdf(50, 60, 30), 0.016702, 1e-4);
approx('lnCdf(50;mean60,sd30)', L.lnCdf(50, 60, 30), 0.440472, 1e-3);

// 整合性（恒等式）：PPF∘CDF≈恒等、PDF の全積分≈1
approx('CDF(PPF(0.37))=0.37', L.normCdf(L.normPpf(0.37, 100, 15), 100, 15), 0.37, 1e-3);
approx('∫pdf dx ≈ 1', L.trapz(x => L.normPdf(x, 100, 15), 10, 190), 1.0, 1e-3);

console.log(`stats.js test: ${pass} passed, ${fail} failed`);
process.exit(fail === 0 ? 0 : 1);
