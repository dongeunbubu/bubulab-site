'use strict';
// Node DOM-stub smoke for CXW v2.2 new widgets (stat-hero, line-trend).
// Extracts the real widget source from contents__FOOTER.html via sentinels and
// mounts demos under a minimal DOM stub, for both reduced-motion and animating paths.
const fs = require('fs');
const SRC = fs.readFileSync('/tmp/bbfb2/imweb_cdn/contents__FOOTER.html', 'utf8');

function extract(tag){
  const re = new RegExp('\\/\\* __SMK_'+tag+'0__[\\s\\S]*?__SMK_'+tag+'1__ \\*\\/');
  const m = SRC.match(re);
  if(!m) throw new Error('sentinel block not found: '+tag);
  return m[0];
}
const HELP = extract('H');
const SH   = extract('SH');
const LT   = extract('LT');

let FAIL = 0, PASS = 0;
function ok(cond, msg){ if(cond){PASS++;} else {FAIL++; console.log('  FAIL:', msg);} }

// ---- DOM stub ----
let rafCalls = 0;
let clock = 0;
function makeChild(){
  const store = {};
  return {
    style:{}, className:'', textContent:'', innerHTML:'', hidden:false,
    getAttribute(n){
      if(n in store) return store[n];
      // plausible defaults so animation read-paths execute
      if(n==='data-w') return '50';
      if(n==='data-mcto') return '1234';
      if(n==='data-len') return '25';
      if(n==='width') return '50';
      if(n==='stroke-dasharray') return '10 90';
      if(n==='data-name') return '계열';
      if(n==='data-xl') return '2020';
      if(n==='data-vl') return '3%';
      return null;
    },
    setAttribute(n,v){ store[n]=String(v); },
    hasAttribute(n){ return n in store; },
    classList:{ add(){}, remove(){}, contains(){ return false; } },
    addEventListener(){}, removeEventListener(){},
    getBoundingClientRect(){ return {left:0,top:0,width:8,height:8}; },
    querySelector(){ return makeChild(); },
    querySelectorAll(){ return [makeChild(), makeChild()]; },
    focus(){}
  };
}
function makeEl(attrs){
  const store = Object.assign({}, attrs||{});
  const cl = { _s:{}, add(){ for(const a of arguments) this._s[a]=1; },
               remove(){ for(const a of arguments) delete this._s[a]; },
               contains(c){ return !!this._s[c]; } };
  const el = {
    _html:'', style:{}, className:'', hidden:false, tabIndex:0, classList:cl,
    getAttribute(n){ return (n in store)? String(store[n]) : null; },
    setAttribute(n,v){ store[n]=String(v); },
    hasAttribute(n){ return n in store; },
    addEventListener(){}, removeEventListener(){}, dispatchEvent(){},
    getBoundingClientRect(){ return {left:0,top:0,width:10,height:10}; },
    appendChild(){}, removeChild(){}, focus(){},
    querySelector(){ return makeChild(); },
    querySelectorAll(){ return [makeChild(), makeChild()]; }
  };
  Object.defineProperty(el,'innerHTML',{ get(){return this._html;}, set(v){this._html=String(v);} });
  return el;
}

function runCase(rmVal){
  const label = rmVal ? 'reduced-motion' : 'animating';
  // ---- injected deps (locals visible to direct eval) ----
  const rm = rmVal;
  function easeOut(t){ return 1-Math.pow(1-t,3); }
  function IO(cb){ this.observe=function(t){ cb([{isIntersecting:true, target:t}]); }; this.unobserve=function(){}; this.disconnect=function(){}; }
  function raf(cb){ rafCalls++; if(rafCalls>200000) return 0; clock+=100000; cb(clock); return 0; }
  const IntersectionObserver = IO;
  const requestAnimationFrame = raf;
  const window = { IntersectionObserver: IO, requestAnimationFrame: raf, matchMedia(){ return {matches:rmVal}; } };
  const document = { createElement(){ return makeChild(); } };
  function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function fmtNum(n){ n=Math.round((parseFloat(n)||0)*100)/100; return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,','); }
  function attr(el,a,dv){ const v=el.getAttribute(a); return v==null?dv:v; }
  function J(el,a){ const r=el.getAttribute(a); if(!r) return null; try{ return JSON.parse(r); }catch(e){ return null; } }
  const MCPAL = ['#B33A4C','#5E8C7F','#C9A84C','#9C6BA8','#D67A89','#7C243B','#7FB08A','#E08696'];
  const W2 = {};

  // define helpers + both widgets from the REAL file source (direct eval -> shares this scope)
  // eslint-disable-next-line no-eval
  eval(HELP + '\n' + SH + '\n' + LT);

  ok(typeof W2['stat-hero']==='function', label+': stat-hero registered');
  ok(typeof W2['line-trend']==='function', label+': line-trend registered');

  // ---- stat-hero demo (with sparkline series) ----
  try{
    const sh = makeEl({
      'data-value':'12,345', 'data-suffix':'만원', 'data-caption':'데모 통계',
      'data-label':'월 30만원, 3년이면 이만큼', 'data-delta':'+12%', 'data-trend':'up',
      'data-series':'[1200,2450,3720,5010,6330,7680]'
    });
    W2['stat-hero'](sh);
    ok(sh._html.indexOf('cxw-sh-v')>=0, label+': stat-hero renders big number');
    ok(sh._html.indexOf('cxw-sh-line')>=0, label+': stat-hero renders sparkline');
    ok(sh._html.indexOf('cxw-sh-delta')>=0, label+': stat-hero renders delta pill');
  }catch(e){ FAIL++; console.log('  FAIL: stat-hero threw ['+label+']:', e && e.message); }

  // ---- stat-hero without series (no spark) ----
  try{
    const sh2 = makeEl({ 'data-value':'42', 'data-unit':'%', 'data-label':'맥락' });
    W2['stat-hero'](sh2);
    ok(sh2._html.indexOf('cxw-sh-v')>=0, label+': stat-hero(no series) renders');
    ok(sh2._html.indexOf('cxw-sh-spark')<0, label+': stat-hero(no series) omits spark');
  }catch(e){ FAIL++; console.log('  FAIL: stat-hero(no series) threw ['+label+']:', e && e.message); }

  // ---- line-trend demo (2 series: base rate vs savings rate) ----
  try{
    const lt = makeEl({
      'data-x':'["2019","2020","2021","2022","2023","2024"]',
      'data-series':'[{"name":"기준금리","values":[1.75,0.5,1.0,3.25,3.5,3.5]},{"name":"적금금리","color":"#5E8C7F","values":[2.1,1.3,1.8,4.2,4.4,3.9]}]',
      'data-unit':'%', 'data-caption':'기준금리 vs 적금금리'
    });
    W2['line-trend'](lt);
    ok(lt._html.indexOf('cxw-lt-line')>=0, label+': line-trend renders lines');
    ok(lt._html.indexOf('cxw-lt-dot')>=0, label+': line-trend renders dots');
    ok(lt._html.indexOf('cxw-lt-legend')>=0, label+': line-trend renders 2-series legend');
    ok(lt._html.indexOf('cxw-lt-tip')>=0, label+': line-trend renders tooltip node');
    ok((lt._html.match(/cxw-lt-line/g)||[]).length===2, label+': line-trend has 2 line paths');
  }catch(e){ FAIL++; console.log('  FAIL: line-trend threw ['+label+']:', e && e.message); }

  // ---- line-trend single numeric series ----
  try{
    const lt2 = makeEl({ 'data-x':'["A","B","C","D"]', 'data-series':'[1,2,3,4]', 'data-unit':'%' });
    W2['line-trend'](lt2);
    ok(lt2._html.indexOf('cxw-lt-line')>=0, label+': line-trend(single) renders');
  }catch(e){ FAIL++; console.log('  FAIL: line-trend(single) threw ['+label+']:', e && e.message); }
}

console.log('CXW v2.2 new-widget smoke (node DOM stub)');
runCase(true);
runCase(false);
console.log('  rAF stub invocations:', rafCalls);
console.log('RESULT: PASS='+PASS+' FAIL='+FAIL);
process.exit(FAIL? 1 : 0);
