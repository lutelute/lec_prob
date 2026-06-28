/* stats.js — ブラウザ内インタラクティブツール共通の確率・統計ヘルパー（依存なし）
 * 正規・対数正規・指数・一様の pdf/cdf/ppf、erf、数値積分、乱数など。
 * 教材の数値（例：N(100,15) で P(85<=X<=115)=0.6827）と一致するよう検証済み。
 */
(function (global) {
  'use strict';

  // 誤差関数（Abramowitz & Stegun 7.1.26、|誤差|<1.5e-7）
  function erf(x) {
    const s = x < 0 ? -1 : 1;
    x = Math.abs(x);
    const t = 1 / (1 + 0.3275911 * x);
    const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
      - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
    return s * y;
  }

  // 標準正規の分位点（Acklam の有理近似、|誤差|<1.15e-9）
  function normSInv(p) {
    if (p <= 0) return -Infinity;
    if (p >= 1) return Infinity;
    const a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
      1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00];
    const b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
      6.680131188771972e+01, -1.328068155288572e+01];
    const c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
      -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00];
    const d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
      3.754408661907416e+00];
    const pl = 0.02425, ph = 1 - pl;
    let q, r;
    if (p < pl) {
      q = Math.sqrt(-2 * Math.log(p));
      return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
        ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);
    } else if (p <= ph) {
      q = p - 0.5; r = q * q;
      return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q /
        (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
    } else {
      q = Math.sqrt(-2 * Math.log(1 - p));
      return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
        ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);
    }
  }

  // 標準正規 pdf
  function normSPdf(z) { return Math.exp(-0.5 * z * z) / Math.sqrt(2 * Math.PI); }

  // 正規
  function normPdf(x, mu, s) { return normSPdf((x - mu) / s) / s; }
  function normCdf(x, mu, s) { return 0.5 * (1 + erf((x - mu) / (s * Math.SQRT2))); }
  function normPpf(p, mu, s) { return mu + s * normSInv(p); }

  // 対数正規（平均 mean・標準偏差 sd を指定 → 内部で μ_log, σ_log）
  function lnParams(mean, sd) {
    const s2 = Math.log(1 + (sd * sd) / (mean * mean));
    return { mu: Math.log(mean) - s2 / 2, sigma: Math.sqrt(s2) };
  }
  function lnPdf(x, mean, sd) {
    if (x <= 0) return 0;
    const { mu, sigma } = lnParams(mean, sd);
    return normSPdf((Math.log(x) - mu) / sigma) / (x * sigma);
  }
  function lnCdf(x, mean, sd) {
    if (x <= 0) return 0;
    const { mu, sigma } = lnParams(mean, sd);
    return 0.5 * (1 + erf((Math.log(x) - mu) / (sigma * Math.SQRT2)));
  }
  function lnPpf(p, mean, sd) {
    const { mu, sigma } = lnParams(mean, sd);
    return Math.exp(mu + sigma * normSInv(p));
  }

  // 指数（率 rate, 平均 1/rate）
  function expPdf(x, rate) { return x < 0 ? 0 : rate * Math.exp(-rate * x); }
  function expCdf(x, rate) { return x < 0 ? 0 : 1 - Math.exp(-rate * x); }
  function expPpf(p, rate) { return -Math.log(1 - p) / rate; }

  // 一様 U(a,b)
  function uniPdf(x, a, b) { return (x >= a && x <= b) ? 1 / (b - a) : 0; }
  function uniCdf(x, a, b) { return x < a ? 0 : (x > b ? 1 : (x - a) / (b - a)); }
  function uniPpf(p, a, b) { return a + p * (b - a); }

  // 台形則による数値積分（区間確率＝面積の確認用）
  function trapz(f, a, b, n) {
    n = n || 2000;
    const h = (b - a) / n;
    let s = 0.5 * (f(a) + f(b));
    for (let i = 1; i < n; i++) s += f(a + i * h);
    return s * h;
  }

  // 線形グリッド
  function linspace(a, b, n) {
    const out = new Array(n);
    for (let i = 0; i < n; i++) out[i] = a + (b - a) * i / (n - 1);
    return out;
  }

  // 決定論的な擬似乱数（再現性のため。seed 文字列 or 数値）
  function mulberry32(seed) {
    let a = (typeof seed === 'string')
      ? Array.from(seed).reduce((h, c) => (h * 31 + c.charCodeAt(0)) | 0, 7)
      : (seed | 0);
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  // Box-Muller で標準正規乱数生成器
  function gaussianGen(rng) {
    let spare = null;
    return function () {
      if (spare !== null) { const v = spare; spare = null; return v; }
      let u, v, s;
      do { u = 2 * rng() - 1; v = 2 * rng() - 1; s = u * u + v * v; } while (s >= 1 || s === 0);
      const m = Math.sqrt(-2 * Math.log(s) / s);
      spare = v * m; return u * m;
    };
  }

  global.LP = {
    erf, normSInv, normSPdf,
    normPdf, normCdf, normPpf,
    lnPdf, lnCdf, lnPpf, lnParams,
    expPdf, expCdf, expPpf,
    uniPdf, uniCdf, uniPpf,
    trapz, linspace, mulberry32, gaussianGen,
  };
})(typeof window !== 'undefined' ? window : this);
