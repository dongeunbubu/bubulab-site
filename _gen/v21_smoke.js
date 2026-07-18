'use strict';
const fs=require('fs');
const FOOT='/tmp/bbfb2/imweb_cdn/contents__FOOTER.html';
const src=fs.readFileSync(FOOT,'utf8');
const startMark='/* ================= CX v2.1 · 신규 위젯 3종';
const endMark=' function fetchBody(slug,routeId,it){';
const si=src.indexOf(startMark), ei=src.indexOf(endMark);
if(si<0||ei<0||ei<si){console.error('SMOKE FAIL: block markers not found');process.exit(1);}
const block=src.slice(si,ei); // the inserted IIFE

// ---- minimal DOM shim ----
function node(){return {classList:{add(){},remove(){},contains(){return false;}},style:{},_a:{},innerHTML:'',textContent:'',offsetWidth:0,
  getAttribute(k){return (k in this._a)?this._a[k]:null;},setAttribute(k,v){this._a[k]=String(v);},
  querySelector(){return node();},querySelectorAll(){return [];},addEventListener(){},dispatchEvent(){return true;},appendChild(){},closest(){return null;}};}
function el(attrs){const n=node();n._a=Object.assign({},attrs);
  n.className='';n.querySelector=function(sel){return node();};n.querySelectorAll=function(){return [];};return n;}
const document={addEventListener(){},getElementById(){return null;},createElement(){return node();},documentElement:{scrollTop:0},body:{scrollTop:0}};
const window={matchMedia(){return {matches:false};}};
global.window=window;global.document=document;
global.CustomEvent=function(t,o){this.type=t;this.detail=o&&o.detail;};
global.requestAnimationFrame=function(f){f(0);};global.setTimeout=function(f){try{f();}catch(e){}return 0;};
global.addEventListener=function(){};global.removeEventListener=function(){};global.scrollTo=function(){};
// in-scope names the block expects:
var d=document, rm=false;
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function fmtWon(n){return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g,',');}
function findItem(){return null;}function itemHref(x){return '#'+(x&&x.slug);}function liveColumns(){return [];}
var CXW={w:{},calc:{futureValue:(p0,m,r,y)=>{r=r/100/12;var n=Math.round(y*12);return p0*Math.pow(1+r,n)+(r>0?m*((Math.pow(1+r,n)-1)/r):m*n);},erode:(b,rt,y)=>({worth:b/Math.pow(1+rt,y)})},mount(){},enhanceExports(){}};

eval(block); // registers CXW.w['mini-chart'|'evidence-card'|'slider-calc'] + CXW.rrail

let fails=0; function ok(c,m){if(c){console.log('  ok  '+m);}else{console.log('  FAIL '+m);fails++;}}
ok(typeof CXW.w['mini-chart']==='function','mini-chart registered');
ok(typeof CXW.w['evidence-card']==='function','evidence-card registered');
ok(typeof CXW.w['slider-calc']==='function','slider-calc registered');
ok(CXW.rrail&&typeof CXW.rrail.build==='function','rrail.build exposed');

// mount mini-chart (all 3 types)
['bar','stack','donut'].forEach(t=>{const e=el({'data-type':t,'data-items':JSON.stringify([{label:'A',value:60},{label:'B',value:40}]),'data-caption':'demo','data-unit':'만원'});
  CXW.w['mini-chart'](e); ok(e.innerHTML.indexOf('<svg')>=0 && e.innerHTML.indexOf('cxw-mc')>=0, 'mini-chart '+t+' → svg output');});
// evidence-card
{const e=el({'data-kind':'발표','data-title':'2026년 최저임금 확정','data-source':'고용노동부','data-date':'2026.07.01','data-note':'전년 대비 인상'});
 CXW.w['evidence-card'](e); ok(e.innerHTML.indexOf('cxw-ev-card')>=0 && e.innerHTML.indexOf('2026')>=0,'evidence-card → scrap card output');}
// slider-calc (reuses CXW.calc.futureValue)
{const e=el({'data-calc':'futureValue','data-args':JSON.stringify([0,'$',5,10]),'data-label':'매달 저축','data-min':'0','data-max':'100','data-def':'30','data-unit':'만원','data-out-label':'10년 뒤 잔고','data-format':'won','data-out-unit':'원','data-caption':'demo'});
 CXW.w['slider-calc'](e); ok(e.innerHTML.indexOf('cxw-slc-range')>=0 && e.innerHTML.indexOf('cxw-slc-out')>=0,'slider-calc → slider+output render');}
console.log(fails?('SMOKE: '+fails+' FAIL'):'SMOKE: all passed');
process.exit(fails?2:0);
