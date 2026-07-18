const fs=require('fs');
const SRC=fs.readFileSync('/tmp/bbfb2/imweb_cdn/contents__FOOTER.html','utf8');
const ex=t=>SRC.match(new RegExp('\\/\\* __SMK_'+t+'0__[\\s\\S]*?__SMK_'+t+'1__ \\*\\/'))[0];
const HELP=ex('H'),SH=ex('SH'),LT=ex('LT');
// reduced-motion path => final state, deterministic output
const rm=true;
function easeOut(t){return 1-Math.pow(1-t,3);}
function IO(cb){this.observe=t=>cb([{isIntersecting:true,target:t}]);this.unobserve=()=>{};}
const window={IntersectionObserver:IO,requestAnimationFrame:cb=>cb(0)};
const IntersectionObserver=IO,requestAnimationFrame=window.requestAnimationFrame;
const document={createElement:()=>mk()};
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function fmtNum(n){n=Math.round((parseFloat(n)||0)*100)/100;return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,',');}
function attr(el,a,d){const v=el.getAttribute(a);return v==null?d:v;}
function J(el,a){const r=el.getAttribute(a);if(!r)return null;try{return JSON.parse(r);}catch(e){return null;}}
const MCPAL=['#B33A4C','#5E8C7F','#C9A84C','#9C6BA8','#D67A89','#7C243B','#7FB08A','#E08696'];
const W2={};
function mk(){return{style:{},className:'',textContent:'',innerHTML:'',hidden:false,getAttribute:()=>null,setAttribute(){},classList:{add(){},remove(){},contains:()=>false},addEventListener(){},getBoundingClientRect:()=>({left:0,top:0,width:8,height:8}),querySelector:()=>null,querySelectorAll:()=>[]};}
function makeEl(a){const s=Object.assign({},a);const el={_html:'',style:{},className:'',classList:{_s:{},add(){for(const x of arguments)this._s[x]=1;},remove(){},contains(c){return!!this._s[c];}},getAttribute(n){return n in s?String(s[n]):null;},setAttribute(n,v){s[n]=String(v);},addEventListener(){},getBoundingClientRect:()=>({left:0,top:0,width:10,height:10}),querySelector:()=>mk(),querySelectorAll:()=>[mk(),mk()]};Object.defineProperty(el,'innerHTML',{get(){return this._html;},set(v){this._html=String(v);}});return el;}
eval(HELP+'\n'+SH+'\n'+LT);
const sh=makeEl({'data-value':'7','data-unit':'%','data-caption':'7% 적금의 힘','data-label':'월 30만원, 3년이면','data-delta':'+4%p','data-trend':'up','data-series':'[1200,2450,3720,5010,6330,7680]'});
W2['stat-hero'](sh);
const lt=makeEl({'data-x':'["2019","2020","2021","2022"]','data-series':'[{"name":"기준금리","values":[1.75,0.5,3.25,3.5]},{"name":"적금금리","color":"#5E8C7F","values":[2.1,1.3,4.2,4.4]}]','data-unit':'%','data-caption':'기준금리 vs 적금금리'});
W2['line-trend'](lt);
function tagBalance(h){const o=(h.match(/<(?!\/)[a-zA-Z][^>]*?(?<!\/)>/g)||[]).length;const c=(h.match(/<\/[a-zA-Z]/g)||[]).length;const self=(h.match(/<[^>]*\/>/g)||[]).length;return {open:o,close:c,self};}
console.log('--- stat-hero innerHTML (final state) ---');
console.log(sh._html);
console.log('tag balance approx:',JSON.stringify(tagBalance(sh._html)));
console.log('\n--- line-trend innerHTML (first 700 chars) ---');
console.log(lt._html.slice(0,700));
console.log('...\n[len]',lt._html.length,'line paths:',(lt._html.match(/cxw-lt-line/g)||[]).length,'dots:',(lt._html.match(/cxw-lt-dot/g)||[]).length);
console.log('tag balance approx:',JSON.stringify(tagBalance(lt._html)));
