'use strict';
// Minimal DOM stub to execute CXW v2 widget initial renders with demo data.
function El(tag){
  return {
    tagName:(tag||'DIV').toUpperCase(), _attrs:{}, _html:'', style:{}, parentNode:null, nextSibling:null,
    classList:{ _s:{}, add:function(c){this._s[c]=1;}, remove:function(c){delete this._s[c];},
      toggle:function(c,f){ if(f===undefined)f=!this._s[c]; if(f)this._s[c]=1; else delete this._s[c]; return f;},
      contains:function(c){return !!this._s[c];} },
    getAttribute:function(k){return (k in this._attrs)?this._attrs[k]:null;},
    setAttribute:function(k,v){this._attrs[k]=String(v);},
    hasAttribute:function(k){return k in this._attrs;},
    removeAttribute:function(k){delete this._attrs[k];},
    addEventListener:function(){}, removeEventListener:function(){},
    appendChild:function(n){n.parentNode=this;(this._children=this._children||[]).push(n);return n;},
    insertBefore:function(n){n.parentNode=this;return n;},
    removeChild:function(n){return n;},
    querySelector:function(){return null;},
    querySelectorAll:function(){return [];},
    closest:function(){return null;},
    get innerHTML(){return this._html;}, set innerHTML(v){this._html=String(v);},
    get textContent(){return this._txt||'';}, set textContent(v){this._txt=String(v);}
  };
}
var doc={ createElement:function(t){return El(t);}, getElementById:function(){return null;},
  querySelectorAll:function(){return [];}, querySelector:function(){return null;},
  addEventListener:function(){}, documentElement:{scrollTop:0,clientHeight:800,scrollHeight:2000}, body:{scrollTop:0} };
var d=doc, W=El('div');
var location={hash:'#bookcol-01'};
var localStorage={ _s:{}, getItem:function(k){return this._s[k]||null;}, setItem:function(k,v){this._s[k]=v;}, removeItem:function(k){delete this._s[k];} };
var window={ matchMedia:function(){return {matches:false};}, requestAnimationFrame:function(f){return 0;}, devicePixelRatio:2, html2canvas:null, jspdf:null };
var history={replaceState:function(){}};
function addEventListener(){} function removeEventListener(){} function setTimeout(f){return 0;} function requestAnimationFrame(){return 0;}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function fmtWon(n){return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g,',');}
function roundk(n){return Math.round(n/1000)*1000;}
var DEMO={
 'bookcol-01':{slug:'bookcol-01',title:'녹아내리는 내 돈',hook:'물가가 돈을 녹여요',thumb:'🧊',premium:false,free:true,pair:'booktool-portfolio',related:['bookcol-04'],connect:{tools:['booktool-portfolio'],kits:['kit-investstart']}},
 'booktool-portfolio':{slug:'booktool-portfolio',title:'포트폴리오 배분기',hook:'자산배분',thumb:'⚖️',premium:true},
 'bookcol-04':{slug:'bookcol-04',title:'5년만 미뤄도',hook:'복리 격차',thumb:'⏳',premium:false},
 'kit-investstart':{slug:'kit-investstart',title:'투자 첫걸음 키트',hook:'첫 매수',thumb:'🌱',premium:false}
};
function findItem(s){return DEMO[s]||null;}
function itemHref(it){return '#'+it.slug;}
function wireTool(slug,el){ /* stub existing engine */ }
var CXW={ w:{}, calc:{ erode:function(base,rate,y){var w=base/Math.pow(1+rate,y);return {worth:w,lost:base-w,fillPct:w/base*100};} }, mount:function(root){return root;} };

// ---- load the injected v2 code in this scope ----
var fs=require('fs');
var code=fs.readFileSync('/tmp/bbfb2/_gen/_v2_footer_inject.js','utf8');
eval(code);

// ---- demo markup per widget ----
function mk(attrs){var e=El('div');for(var k in attrs)e._attrs[k]=attrs[k];return e;}
var cases={
 'compare-pro': mk({'data-cols':'["청년도약계좌","청년미래적금"]','data-rows':'[{"label":"금리","cells":["6.0%","5.0%"],"best":0},{"label":"한도","cells":["70만","50만"],"best":0}]','data-caption':'예시'}),
 'decision-tree': mk({'data-tree':'{"start":"q1","nodes":{"q1":{"q":"소득이 있나요?","opts":[{"label":"네","to":"r1"},{"label":"아니오","to":"r2"}]}},"results":{"r1":{"title":"가입 가능","desc":"조건 충족","badge":"결론"},"r2":{"title":"대상 아님","desc":"소득 필요","badge":"결론"}}}'}),
 'step-guide': mk({'data-steps':'[{"img":"a.webp","cap":"앱을 여세요","badges":[{"x":50,"y":40,"label":"1"}]},{"img":"b.webp","cap":"메뉴 선택"}]','data-aspect':'16/10'}),
 'term-chip': mk({'data-term':'ISA','data-def':'개인종합자산관리계좌'}),
 'timeline-h': mk({'data-events':'[{"date":"2026.01","title":"가입"},{"date":"2031.01","title":"만기"}]'}),
 'summary-card': mk({'data-title':'핵심 요약','data-points':'["첫째","둘째"]','data-check':'1','data-key':'demo'}),
 'related-rail': mk({'data-slug':'bookcol-01'}),
 'sim-frame': mk({'data-calc':'compound_goal'})
};
var pass=0,fail=0;
Object.keys(cases).forEach(function(name){
  var fn=CXW.w[name];
  if(typeof fn!=='function'){console.log('  ** FAIL '+name+': not registered');fail++;return;}
  try{
    var el=cases[name]; fn(el);
    var html=el._html||'';
    var ok=html.length>20 && html.indexOf('cxw-')>=0;
    // related-rail may hide if no data -> but demo has related, expect cards
    if(name==='related-rail') ok = html.indexOf('cxw-rr-card')>=0;
  if(name==='term-chip') ok = el.classList.contains('cxw-term') && (el._children&&el._children.length>0) && el.getAttribute('role')==='button';
    console.log((ok?'  OK   ':'  ** FAIL ')+name+'  (html '+html.length+' bytes)');
    ok?pass++:fail++;
  }catch(e){console.log('  ** FAIL '+name+': '+e.message);fail++;}
});
// registry + sim + export presence
console.log('  '+((CXW.sim&&CXW.sim.compound_goal&&CXW.sim.save_plan&&CXW.sim.inflation_real)?'OK   ':'** FAIL ')+'CXW.sim registry (3 calculators)');
console.log('  '+((typeof CXW.exportCard==='function'&&typeof CXW.enhanceExports==='function')?'OK   ':'** FAIL ')+'exportCard + enhanceExports API');
console.log('  '+((CXW.reader&&typeof CXW.reader.init==='function')?'OK   ':'** FAIL ')+'CXW.reader.init');
console.log('  '+((typeof CXW.calc.futureValue==='function'&&typeof CXW.calc.monthlyForGoal==='function')?'OK   ':'** FAIL ')+'calc registry extended');
// sim run sanity
try{var r=CXW.sim.compound_goal.run({p0:1000,m:50,y:15,r:6});console.log('  OK   sim compound_goal run -> '+r.primary.value);}catch(e){console.log('  ** FAIL sim run: '+e.message);fail++;}
console.log('\nGATE4 WIDGET SMOKE: pass='+pass+' fail='+fail+' -> '+(fail===0?'PASS':'FAIL'));
process.exit(fail===0?0:1);
