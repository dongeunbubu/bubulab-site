'use strict';
/* free_smoke.js — 무료 단독 페이지 FOOTER 엔진 마운트 스모크
   사용: node free_smoke.js <BODY.html> <FOOTER.html> <slug>
   검증: 엔진 로드 무예외 · #cxRoot에 js 클래스 · related-rail 위젯 렌더 · 엔드 모듈(#cxEnd) 렌더 */
const fs = require('fs'), vm = require('vm');
const [bodyPath, footPath, slug] = process.argv.slice(2);
const bodyHtml = fs.readFileSync(bodyPath, 'utf8');
const footHtml = fs.readFileSync(footPath, 'utf8');

const snapM = bodyHtml.match(/id="cxSnap">([\s\S]*?)<\/script>/);
if (!snapM) { console.error('cxSnap 없음'); process.exit(1); }
const relM = bodyHtml.match(/data-related='([^']+)'/);
const relJson = relM ? relM[1] : '["booktool-youthchoice"]';

function El(tag) {
  const el = {
    tagName: (tag || 'DIV').toUpperCase(), _attrs: {}, _html: '', _txt: '',
    style: { setProperty() {} }, parentNode: null, nextSibling: null, hidden: false,
    checked: false, offsetHeight: 40, offsetWidth: 300, offsetTop: 0, offsetLeft: 0,
    clientHeight: 800, clientWidth: 800, scrollTop: 0,
    classList: {
      _s: {}, add(...c) { c.forEach(x => this._s[x] = 1); }, remove(...c) { c.forEach(x => delete this._s[x]); },
      toggle(c, f) { if (f === undefined) f = !this._s[c]; if (f) this._s[c] = 1; else delete this._s[c]; return !!f; },
      contains(c) { return !!this._s[c]; }
    },
    getAttribute(k) { return (k in el._attrs) ? el._attrs[k] : null; },
    setAttribute(k, v) { el._attrs[k] = String(v); },
    hasAttribute(k) { return k in el._attrs; },
    removeAttribute(k) { delete el._attrs[k]; },
    addEventListener() {}, removeEventListener() {},
    appendChild(n) { if (n) n.parentNode = el; return n; },
    insertBefore(n) { if (n) n.parentNode = el; return n; },
    removeChild(n) { return n; },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    closest() { return null; },
    getBoundingClientRect() { return { top: 0, left: 0, width: 300, height: 40, bottom: 40, right: 300 }; },
    focus() {}, blur() {}, click() {},
    get innerHTML() { return el._html; }, set innerHTML(v) { el._html = String(v); },
    get textContent() { return el._txt; }, set textContent(v) { el._txt = String(v); }
  };
  return el;
}

const elRoot = El('div');   elRoot._attrs.id = 'cxRoot';
const elSnap = El('script'); elSnap._txt = snapM[1];
const elReader = El('section'); elReader._attrs['data-free-slug'] = slug;
const elBody = El('div');
const elEnd = El('div');
const widget = El('div');
widget._attrs['data-cx-w'] = 'related-rail';
widget._attrs['data-related'] = relJson;
widget._attrs['data-title'] = '이 칼럼과 함께 보면 좋아요';
elBody.querySelectorAll = sel => (sel && sel.indexOf('data-cx-w') >= 0) ? [widget] : [];

const byId = { cxRoot: elRoot, cxSnap: elSnap, cxReader: elReader, cxRdBody: elBody, cxEnd: elEnd };
const documentStub = {
  getElementById: id => byId[id] || null,
  createElement: t => El(t),
  querySelector: () => null,
  querySelectorAll: () => [],
  addEventListener() {}, removeEventListener() {},
  documentElement: { scrollTop: 0, clientHeight: 800, scrollHeight: 2400, style: { setProperty() {} } },
  body: El('body'), head: El('head'), hidden: false, readyState: 'complete'
};
const sandbox = {
  console, JSON, Math, Date, parseFloat, parseInt, isNaN, String, Number, Array, Object, RegExp, Error,
  document: documentStub,
  window: {},
  location: { hash: '', href: 'https://bubulab.co.kr/x' },
  localStorage: { getItem: () => null, setItem() {}, removeItem() {} },
  history: { replaceState() {} },
  addEventListener() {}, removeEventListener() {},
  setTimeout: () => 0, clearTimeout() {}, setInterval: () => 0, clearInterval() {},
  requestAnimationFrame: () => 0, cancelAnimationFrame() {},
  scrollTo() {}, navigator: { userAgent: 'smoke' }, performance: { now: () => 0 }
};
sandbox.window = sandbox;   // window.fetch undefined → 네트워크 스킵
vm.createContext(sandbox);

const blocks = [];
footHtml.replace(/<script>([\s\S]*?)<\/script>/g, (m, js) => { blocks.push(js); return m; });
if (!blocks.length) { console.error('script 블록 없음'); process.exit(1); }
try {
  blocks.forEach((js, i) => vm.runInContext(js, sandbox, { filename: 'blk' + i + '.js', timeout: 20000 }));
} catch (e) {
  console.error('로드 예외: ' + (e && e.stack ? e.stack.split('\n').slice(0, 4).join(' | ') : e));
  process.exit(1);
}

const checks = [
  ['cxRoot js 클래스', elRoot.classList.contains('js')],
  ['related-rail 렌더', widget._html.indexOf('cxw-rr-') >= 0],
  ['related-rail 카드', widget._html.indexOf('cxw-rr-card') >= 0],
  ['엔드 모듈 렌더', elEnd._html.indexOf('cx-em') >= 0],
  ['엔드 모듈 무료 카드', elEnd._html.indexOf('cx-em-card') >= 0],
  ['엔드 모듈 칼럼 이동', elEnd._html.indexOf('cx-pnbtn') >= 0],
  ['리더 기준일 메타', elReader._attrs['data-basis-date'] === '2026-07']
];
let ok = true;
const parts = checks.map(([k, v]) => { if (!v) ok = false; return k + ':' + (v ? 'PASS' : 'FAIL'); });
console.log('mount ' + (ok ? 'PASS' : 'FAIL') + ' · ' + parts.join(' · ') + ' · end=' + elEnd._html.length + 'B rail=' + widget._html.length + 'B');
process.exit(ok ? 0 : 1);
