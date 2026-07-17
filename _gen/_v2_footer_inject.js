
 /* ================= CXW v2 · 확장 위젯 + exportCard + Reader v2 (선언형 data-cx-w, cx- 접두) ================= */
 /* 계약: 기존 CXW.mount(root) 유지. 신규 위젯은 CXW.w[name]에 등록되어 [data-cx-w=name]로 자동 마운트.
    calc 레지스트리 확장은 CXW.sim(시뮬레이터)·CXW.calc(순수식). exportCard 훅은 CXW.mount/ wireTool 래핑으로 공통 적용. */
 (function(){
  if(typeof CXW==='undefined'||!CXW||!CXW.w)return;
  var W2=CXW.w, doc=d;
  function J(el,a){var r=el.getAttribute(a);if(!r)return null;try{return JSON.parse(r);}catch(e){return null;}}
  function numify(v){var n=parseFloat(String(v==null?'':v).replace(/[^0-9.\-]/g,''));return isNaN(n)?null:n;}
  function attr(el,a,dv){var v=el.getAttribute(a);return v==null?dv:v;}
  function slugFromHash(){return (location.hash||'').replace(/^#/,'').trim();}

  /* ---- calc 레지스트리 확장: 시뮬레이터(sim-frame 공용) ---- */
  CXW.calc.futureValue=function(p0,monthly,ratePct,years){var r=ratePct/100/12,n=Math.max(0,Math.round(years*12));var fvP=p0*Math.pow(1+r,n);var fvM=r>0?monthly*((Math.pow(1+r,n)-1)/r):monthly*n;return fvP+fvM;};
  CXW.calc.monthlyForGoal=function(goal,months,ratePct){var r=ratePct/100/12,n=Math.max(1,Math.round(months));if(r<=0)return goal/n;return goal*r/(Math.pow(1+r,n)-1);};
  var SIM={
   compound_goal:{
    title:'복리로 얼마가 될까',
    fields:[
     {k:'p0',label:'지금 있는 돈',unit:'만원',min:0,max:100000,step:10,def:1000},
     {k:'m',label:'매달 넣을 돈',unit:'만원',min:0,max:1000,step:1,def:50},
     {k:'y',label:'기간',unit:'년',min:1,max:40,step:1,def:15},
     {k:'r',label:'연 수익률',unit:'%',min:0,max:15,step:0.5,def:6}
    ],
    formula:'미래가치 = 원금×(1+월수익률)^개월 + 월납입×[((1+월수익률)^개월−1)/월수익률]',
    run:function(v){var fv=CXW.calc.futureValue(v.p0*10000,v.m*10000,v.r,v.y);var paid=(v.p0+v.m*12*v.y)*10000;return {primary:{label:v.y+'년 뒤 예상 잔고',value:fmtWon(roundk(fv))+'원'},lines:[{label:'내가 넣은 돈',value:fmtWon(roundk(paid))+'원'},{label:'불어난 돈',value:fmtWon(roundk(Math.max(0,fv-paid)))+'원'}]};}
   },
   save_plan:{
    title:'목표까지 매달 얼마',
    fields:[
     {k:'goal',label:'목표 금액',unit:'만원',min:100,max:100000,step:10,def:3000},
     {k:'mo',label:'기간',unit:'개월',min:6,max:600,step:1,def:36},
     {k:'r',label:'연 이자',unit:'%',min:0,max:10,step:0.1,def:3}
    ],
    formula:'월 납입 = 목표×월이자 / [(1+월이자)^개월 − 1]  (이자 0이면 목표/개월)',
    run:function(v){var m=CXW.calc.monthlyForGoal(v.goal*10000,v.mo,v.r);var plain=v.goal*10000/Math.max(1,v.mo);return {primary:{label:'매달 넣을 돈',value:fmtWon(roundk(m))+'원'},lines:[{label:'이자 없이 단순 저축',value:fmtWon(roundk(plain))+'원'},{label:'이자가 아껴주는 몫',value:fmtWon(roundk(Math.max(0,plain-m)))+'원/월'}]};}
   },
   inflation_real:{
    title:'물가를 빼면 남는 값',
    fields:[
     {k:'amt',label:'지금 금액',unit:'만원',min:100,max:200000,step:10,def:10000},
     {k:'y',label:'기간',unit:'년',min:1,max:40,step:1,def:20},
     {k:'inf',label:'물가상승률',unit:'%',min:0,max:8,step:0.1,def:2.5}
    ],
    formula:'실질가치 = 금액 / (1+물가상승률)^년',
    run:function(v){var c=CXW.calc.erode(v.amt*10000,v.inf/100,v.y);return {primary:{label:v.y+'년 뒤 실질 구매력',value:fmtWon(roundk(c.worth))+'원'},lines:[{label:'사라진 구매력',value:fmtWon(roundk(c.lost))+'원'},{label:'남는 비율',value:Math.round(c.fillPct)+'%'}]};}
   }
  };
  CXW.sim=SIM;

  /* ---- compare-pro: 비교표(열 하이라이트·행 정렬·모바일 카드화) ---- */
  W2['compare-pro']=function(el){
   var cols=J(el,'data-cols')||[], rows=J(el,'data-rows')||[];
   if(!cols.length||!rows.length)return;
   var hiCol=(el.getAttribute('data-hi')!=null?parseInt(el.getAttribute('data-hi'),10):-1), sortCol=-1, sortDir=1;
   var cap=el.getAttribute('data-caption')||'';
   function build(){
    var order=rows.map(function(r,i){return {r:r,i:i};});
    if(sortCol>=0)order.sort(function(a,b){var x=numify(a.r.cells[sortCol]),y=numify(b.r.cells[sortCol]);if(x==null&&y==null)return a.i-b.i;if(x==null)return 1;if(y==null)return -1;return (x-y)*sortDir;});
    var h='<div class="cxw-cpro-wrap"><table class="cxw-cpro"><thead><tr><th class="cxw-cpro-corner" scope="col"></th>';
    cols.forEach(function(c,ci){h+='<th scope="col"'+(ci===hiCol?' class="cxw-cpro-hi"':'')+'><button type="button" class="cxw-cpro-hbtn" data-col="'+ci+'">'+esc(c)+'<span class="cxw-cpro-ar" aria-hidden="true">'+(sortCol===ci?(sortDir>0?'▲':'▼'):'⇅')+'</span></button></th>';});
    h+='</tr></thead><tbody>';
    order.forEach(function(o){var r=o.r;h+='<tr><th class="cxw-cpro-rh" scope="row">'+esc(r.label)+'</th>';
     (r.cells||[]).forEach(function(cell,ci){var best=(r.best===ci),cls=[];if(ci===hiCol)cls.push('cxw-cpro-hi');if(best)cls.push('cxw-cpro-best');
      h+='<td data-lab="'+esc(cols[ci]||'')+'"'+(cls.length?' class="'+cls.join(' ')+'"':'')+'>'+esc(cell)+(best?'<span class="cxw-cpro-tick" aria-hidden="true"> ✔</span>':'')+'</td>';});
     h+='</tr>';});
    h+='</tbody></table></div>'+(cap?'<div class="cxw-cpro-cap">'+esc(cap)+'</div>':'');
    el.innerHTML=h;
   }
   build();
   el.addEventListener('click',function(e){var b=e.target.closest?e.target.closest('.cxw-cpro-hbtn'):null;if(!b)return;var ci=parseInt(b.getAttribute('data-col'),10);if(sortCol===ci){sortDir=-sortDir;}else{sortCol=ci;sortDir=1;}hiCol=ci;build();});
  };

  /* ---- decision-tree: 분기 진단(질문→선택→경로→결론 카드, 뒤로가기, 전 경로 결론 보장) ---- */
  W2['decision-tree']=function(el){
   var tree=J(el,'data-tree');if(!tree||!tree.start||!tree.nodes)return;
   var results=tree.results||{}, stack=[], cur=tree.start;
   function isResult(id){return !!results[id];}
   function go(id){stack.push(cur);cur=id;render();}
   function back(){if(stack.length){cur=stack.pop();render();}}
   function restart(){stack=[];cur=tree.start;render();}
   function render(){
    var steps=stack.length+1;
    var bar='<div class="cxw-dt-top"><span class="cxw-dt-step">'+(isResult(cur)?'결과':('질문 '+steps))+'</span>'+(stack.length?'<button type="button" class="cxw-dt-back" data-dt="back">← 뒤로</button>':'')+'</div>';
    if(isResult(cur)){
     var R=results[cur];
     var ctaHtml=R.cta&&R.href?'<a class="cxw-dt-cta" href="'+esc(R.href)+'">'+esc(R.cta)+' →</a>':'';
     el.innerHTML=bar+'<div class="cxw-dt-result" data-cx-export data-export-title="'+esc(R.title||'진단 결과')+'"><div class="cxw-dt-badge">'+esc(R.badge||'이런 경우엔')+'</div><h4 class="cxw-dt-rt">'+esc(R.title||'')+'</h4><p class="cxw-dt-rd">'+(R.desc||'')+'</p>'+ctaHtml+'</div><div class="cxw-dt-again"><button type="button" class="cxw-dt-restart" data-dt="restart">처음부터 다시</button></div>';
     try{CXW.enhanceExports&&CXW.enhanceExports(el);}catch(_e){}
    } else {
     var N=tree.nodes[cur];if(!N){el.innerHTML=bar+'<div class="cxw-dt-q">경로가 끊겼어요. 다시 시작해 주세요.</div><div class="cxw-dt-again"><button type="button" class="cxw-dt-restart" data-dt="restart">처음부터 다시</button></div>';return;}
     var opts=(N.opts||[]).map(function(o){return '<button type="button" class="cxw-dt-opt" data-to="'+esc(o.to)+'">'+esc(o.label)+'</button>';}).join('');
     el.innerHTML=bar+'<div class="cxw-dt-q">'+esc(N.q||'')+'</div><div class="cxw-dt-opts">'+opts+'</div>';
    }
   }
   el.addEventListener('click',function(e){var t=e.target.closest?e.target.closest('[data-to],[data-dt]'):null;if(!t)return;
    if(t.getAttribute('data-dt')==='back')return back();
    if(t.getAttribute('data-dt')==='restart')return restart();
    var to=t.getAttribute('data-to');if(to)go(to);});
   render();
  };
 })();

 /* ---- step-guide / term-chip / timeline-h / summary-card / related-rail ---- */
 (function(){
  if(typeof CXW==='undefined'||!CXW||!CXW.w)return;
  var W2=CXW.w, doc=d;
  function J(el,a){var r=el.getAttribute(a);if(!r)return null;try{return JSON.parse(r);}catch(e){return null;}}
  function lazyImg(src,alt,cls){return '<img loading="lazy" decoding="async" class="'+(cls||'')+'" src="'+esc(src)+'" alt="'+esc(alt||'')+'">';}

  /* step-guide: 캡처 스텝(이미지+클릭 위치 배지+캡션, 번호 진행, 이미지 lazy·aspect 예약) */
  W2['step-guide']=function(el){
   var steps=J(el,'data-steps')||[];if(!steps.length)return;
   var ar=el.getAttribute('data-aspect')||'16/10';
   var idx=0;
   function badges(s){return (s.badges||[]).map(function(b,i){return '<span class="cxw-sg-badge" style="left:'+(b.x||0)+'%;top:'+(b.y||0)+'%">'+(b.label!=null?esc(b.label):(i+1))+'</span>';}).join('');}
   function render(){
    var s=steps[idx]||{};
    var dots=steps.map(function(_,i){return '<span class="cxw-sg-dot'+(i===idx?' on':'')+'"></span>';}).join('');
    el.innerHTML='<div class="cxw-sg-head"><span class="cxw-sg-n">STEP '+(idx+1)+' / '+steps.length+'</span><span class="cxw-sg-dots">'+dots+'</span></div>'
     +'<div class="cxw-sg-stage" style="aspect-ratio:'+ar+'">'+(s.img?lazyImg(s.img,s.cap,'cxw-sg-img'):'<div class="cxw-sg-noimg">이미지 준비 중</div>')+badges(s)+'</div>'
     +'<div class="cxw-sg-cap">'+(s.cap?esc(s.cap):'')+'</div>'
     +'<div class="cxw-sg-nav"><button type="button" class="cxw-sg-prev" data-sg="prev"'+(idx===0?' disabled':'')+'>← 이전</button><button type="button" class="cxw-sg-next" data-sg="next"'+(idx>=steps.length-1?' disabled':'')+'>다음 →</button></div>';
   }
   el.addEventListener('click',function(e){var b=e.target.closest?e.target.closest('[data-sg]'):null;if(!b)return;var k=b.getAttribute('data-sg');if(k==='next'&&idx<steps.length-1)idx++;else if(k==='prev'&&idx>0)idx--;render();});
   render();
  };

  /* term-chip: 용어 칩(탭/클릭 시 풀이 팝오버) */
  W2['term-chip']=function(el){
   var term=el.getAttribute('data-term')||el.textContent||'', def=el.getAttribute('data-def')||'';
   if(!def)return;
   el.classList.add('cxw-term');el.setAttribute('role','button');if(!el.getAttribute('tabindex'))el.setAttribute('tabindex','0');
   if(!el.querySelector('.cxw-term-pop')){var pop=doc.createElement('span');pop.className='cxw-term-pop';pop.innerHTML='<b>'+esc(term)+'</b>'+esc(def);el.appendChild(pop);}
   function toggle(e){e.stopPropagation();var was=el.classList.contains('on');[].slice.call(doc.querySelectorAll('.cxw-term.on')).forEach(function(x){x.classList.remove('on');});if(!was)el.classList.add('on');}
   el.addEventListener('click',toggle);
   el.addEventListener('keydown',function(e){var k=e.keyCode||e.which;if(k===13||k===32){e.preventDefault();toggle(e);}});
   if(!W.__cxwtermdoc){W.__cxwtermdoc=1;doc.addEventListener('click',function(){[].slice.call(doc.querySelectorAll('.cxw-term.on')).forEach(function(x){x.classList.remove('on');});});}
  };

  /* timeline-h: 가로 타임라인 */
  W2['timeline-h']=function(el){
   var ev=J(el,'data-events')||[];if(!ev.length)return;
   var items=ev.map(function(e){return '<li class="cxw-tlh-item"><span class="cxw-tlh-dot" aria-hidden="true"></span><div class="cxw-tlh-date">'+esc(e.date||'')+'</div><div class="cxw-tlh-t">'+esc(e.title||'')+'</div>'+(e.desc?'<div class="cxw-tlh-d">'+esc(e.desc)+'</div>':'')+'</li>';}).join('');
   el.innerHTML='<div class="cxw-tlh-scroll"><ol class="cxw-tlh-track">'+items+'</ol></div>';
  };

  /* summary-card: 요약·체크리스트 카드 */
  W2['summary-card']=function(el){
   var title=el.getAttribute('data-title')||'요약', pts=J(el,'data-points')||[], key=el.getAttribute('data-key');
   var check=el.getAttribute('data-check')==='1';
   var KEY=key?('bbl_cxw_sum_'+key):null, saved={};
   if(KEY){try{saved=JSON.parse(localStorage.getItem(KEY)||'{}')||{};}catch(e){saved={};}}
   var rows=pts.map(function(p,i){var txt=(typeof p==='string')?p:(p.t||''); var on=saved[i]?' on':'';
    if(check)return '<li class="cxw-sum-li'+on+'" data-i="'+i+'"><button type="button" class="cxw-sum-chk" aria-pressed="'+(saved[i]?'true':'false')+'"><span class="cxw-sum-box" aria-hidden="true"></span><span class="cxw-sum-tx">'+esc(txt)+'</span></button></li>';
    return '<li class="cxw-sum-li"><span class="cxw-sum-bul" aria-hidden="true">•</span><span class="cxw-sum-tx">'+esc(txt)+'</span></li>';}).join('');
   el.innerHTML='<div class="cxw-sum" data-cx-export data-export-title="'+esc(title)+'"><div class="cxw-sum-h"><span class="cxw-sum-ic" aria-hidden="true">📌</span><h4>'+esc(title)+'</h4></div><ul class="cxw-sum-list">'+rows+'</ul></div>';
   if(check){el.addEventListener('click',function(e){var b=e.target.closest?e.target.closest('.cxw-sum-chk'):null;if(!b)return;var li=b.closest('.cxw-sum-li');var i=li.getAttribute('data-i');var on=!li.classList.contains('on');li.classList.toggle('on',on);b.setAttribute('aria-pressed',on?'true':'false');saved[i]=on?1:0;if(KEY){try{localStorage.setItem(KEY,JSON.stringify(saved));}catch(_e){}}});}
   try{CXW.enhanceExports&&CXW.enhanceExports(el);}catch(_e){}
  };

  /* related-rail: 관련 콘텐츠 레일(인덱스 pair/related/connect 자동) */
  W2['related-rail']=function(el){
   var slug=el.getAttribute('data-slug')|| (location.hash||'').replace(/^#/,'').trim();
   var it=(typeof findItem==='function')?findItem(slug):null;
   var seen={}, slugs=[];
   function add(s){if(s&&!seen[s]&&s!==slug){seen[s]=1;slugs.push(s);}}
   var manual=J(el,'data-related');if(manual&&manual.length)manual.forEach(add);
   if(it){if(it.pair)add(it.pair);(it.related||[]).forEach(add);var cn=it.connect||{};(cn.columns||[]).forEach(add);(cn.tools||[]).forEach(add);(cn.kits||[]).forEach(add);}
   var cards=slugs.slice(0,8).map(function(s){var r=(typeof findItem==='function')?findItem(s):null;if(!r)return '';
    var href=(typeof itemHref==='function')?itemHref(r):('#'+s);
    var free=(r.free===true||r.premium===false)?'<span class="cxw-rr-b cxw-rr-free">🆓 무료</span>':(r.premium===true?'<span class="cxw-rr-b cxw-rr-prem">🔒 프리미엄</span>':'');
    return '<a class="cxw-rr-card" href="'+href+'"><span class="cxw-rr-th" aria-hidden="true">'+esc(r.thumb||'🔗')+'</span><span class="cxw-rr-t">'+esc(r.title||s)+'</span><span class="cxw-rr-hook">'+esc(r.hook||'')+'</span><span class="cxw-rr-badges">'+free+'</span></a>';}).join('');
   if(!cards){el.style.display='none';return;}
   el.innerHTML='<div class="cxw-rr-head">'+esc(el.getAttribute('data-title')||'함께 보면 좋아요')+'</div><div class="cxw-rr-scroll">'+cards+'</div>';
  };
 })();

 /* ---- exportCard: 도구·결과 카드 [이미지로 저장][PDF로 저장] (html2canvas+jsPDF, cdnjs 지연 로드, 브랜드 프레임 합성) ---- */
 (function(){
  if(typeof CXW==='undefined'||!CXW)return;
  var doc=d;
  var CDN_H2C='https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
  var CDN_PDF='https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
  var _cache={};
  function loadScript(src){if(_cache[src])return _cache[src];_cache[src]=new Promise(function(res,rej){var s=doc.createElement('script');s.src=src;s.async=true;s.onload=res;s.onerror=function(){_cache[src]=null;rej(new Error('load fail'));};(doc.head||doc.body).appendChild(s);});return _cache[src];}
  function needH2C(){return window.html2canvas?Promise.resolve():loadScript(CDN_H2C);}
  function needPDF(){return (window.jspdf&&window.jspdf.jsPDF)?Promise.resolve():loadScript(CDN_PDF);}
  function today(){var t=new Date();function p(n){return (n<10?'0':'')+n;}return t.getFullYear()+'.'+p(t.getMonth()+1)+'.'+p(t.getDate());}
  function safeName(s){return String(s||'부부연구소').replace(/[\\/:*?"<>|\s]+/g,'_').slice(0,40);}
  /* 브랜드 프레임: 캡처 캔버스 아래 로고(하트)+워터마크+날짜 스트립 합성 */
  function brandWrap(src){
   var pad=Math.round(src.width*0.028), strip=Math.round(src.width*0.072);
   var c=doc.createElement('canvas');c.width=src.width;c.height=src.height+strip;
   var g=c.getContext('2d');
   g.fillStyle='#FFFDF9';g.fillRect(0,0,c.width,c.height);
   g.drawImage(src,0,0);
   var y=src.height, h=strip;
   g.fillStyle='#F3ECDF';g.fillRect(0,y,c.width,h);
   g.fillStyle='#EAD7D3';g.fillRect(0,y,c.width,Math.max(1,Math.round(h*0.02)));
   var cy=y+h/2, fs=Math.round(h*0.34);
   /* 하트 로고 */
   var hx=pad, hs=Math.round(h*0.42);
   g.fillStyle='#B33A4C';
   g.beginPath();
   var hox=hx+hs/2, hoy=cy-hs*0.05, r=hs*0.28;
   g.moveTo(hox,hoy+hs*0.32);
   g.bezierCurveTo(hox-r*1.7,hoy-r*0.9,hox-r*0.2,hoy-r*1.6,hox,hoy-r*0.2);
   g.bezierCurveTo(hox+r*0.2,hoy-r*1.6,hox+r*1.7,hoy-r*0.9,hox,hoy+hs*0.32);
   g.closePath();g.fill();
   g.fillStyle='#3E2F29';g.font='700 '+fs+'px Pretendard, -apple-system, sans-serif';g.textBaseline='middle';
   g.fillText('부부연구소',hx+hs*1.25,cy);
   g.textAlign='right';g.fillStyle='#8A7B72';g.font='600 '+Math.round(fs*0.82)+'px Pretendard, -apple-system, sans-serif';
   g.fillText('bubulab.co.kr · '+today(),c.width-pad,cy);
   return c;
  }
  function capture(el){return needH2C().then(function(){return window.html2canvas(el,{backgroundColor:'#ffffff',scale:Math.min(2,(window.devicePixelRatio||1)+0.5)||2,useCORS:true,logging:false,ignoreElements:function(n){return n.classList&&n.classList.contains('cxw-exp-bar');}});});}
  function triggerDownload(dataURL,name){try{var a=doc.createElement('a');a.href=dataURL;a.download=name;doc.body.appendChild(a);a.click();doc.body.removeChild(a);}catch(e){try{window.open(dataURL,'_blank');}catch(_e){}}}
  function savePNG(el,title){return capture(el).then(function(cv){var out=brandWrap(cv);var url=out.toDataURL('image/png');triggerDownload(url,safeName(title)+'_'+today()+'.png');});}
  function savePDF(el,title){return capture(el).then(function(cv){var out=brandWrap(cv);return needPDF().then(function(){var JP=window.jspdf.jsPDF;var w=out.width,h=out.height;var pdf=new JP({orientation:w>h?'l':'p',unit:'pt',format:[w*0.75,h*0.75]});pdf.addImage(out.toDataURL('image/png'),'PNG',0,0,w*0.75,h*0.75);pdf.save(safeName(title)+'_'+today()+'.pdf');});});}
  CXW.exportCard=function(el,opt){opt=opt||{};var t=opt.title||el.getAttribute('data-export-title')||'부부연구소';return (opt.pdf?savePDF:savePNG)(el,t);};

  function busy(btn,on){if(!btn)return;btn.disabled=on;btn.classList.toggle('cxw-exp-busy',on);}
  function enhance(scope){
   if(!scope||!scope.querySelectorAll)return;
   [].slice.call(scope.querySelectorAll('[data-cx-export]')).forEach(function(card){
    var nx=card.nextSibling;while(nx&&nx.nodeType!==1)nx=nx.nextSibling;
    if(nx&&nx.className&&(' '+nx.className+' ').indexOf(' cxw-exp-bar ')>=0)return;
    if(!card.parentNode)return;
    var title=card.getAttribute('data-export-title')||'부부연구소';
    var bar=doc.createElement('div');bar.className='cxw-exp-bar';
    bar.innerHTML='<span class="cxw-exp-lbl">저장하기</span><button type="button" class="cxw-exp-btn" data-exp="png"><span aria-hidden="true">🖼️</span> 이미지로 저장</button><button type="button" class="cxw-exp-btn" data-exp="pdf"><span aria-hidden="true">📄</span> PDF로 저장</button>';
    card.parentNode.insertBefore(bar,card.nextSibling);
    bar.addEventListener('click',function(e){var b=e.target.closest?e.target.closest('[data-exp]'):null;if(!b)return;var kind=b.getAttribute('data-exp');busy(b,true);
     var p=(kind==='pdf')?savePDF(card,title):savePNG(card,title);
     p.then(function(){busy(b,false);},function(){busy(b,false);b.textContent='다시 시도';});});
   });
  }
  CXW.enhanceExports=enhance;

  /* 훅: CXW.mount 래핑 → 마운트된 콘텐츠의 export 카드 자동 활성 */
  var _mount=CXW.mount;
  CXW.mount=function(root){var r=_mount.apply(this,arguments);try{enhance(root);}catch(e){}return r;};

  /* 훅: 기존 도구(wire* 엔진) 결과 카드 공통 적용 — wireTool 래핑 */
  if(typeof wireTool==='function'){
   var _wt=wireTool;
   wireTool=function(slug,el){var r=_wt(slug,el);try{if(el&&el.querySelector){var out=el.querySelector('[id$="Out"]')||el.querySelector('[id$="Prev"]');if(out&&!out.getAttribute('data-cx-export')){out.setAttribute('data-cx-export','');out.setAttribute('data-export-title',(doc.title||'부부연구소 도구').replace(/\s*[|·-].*$/,''));}}enhance(el);}catch(e){}return r;};
  }
 })();

 /* ---- Reader v2: 챕터 시스템(스티키 목차·진행바 틱·위치기억·이어읽기·딥링크 @chN·챕터 지연렌더·모바일 경량) ---- */
 (function(){
  if(typeof CXW==='undefined'||!CXW)return;
  var doc=d, MEM='bbl_rd_pos_';
  var state={slug:'',chs:[],onScroll:null,body:null};
  function litemq(){return (window.matchMedia&&(matchMedia('(max-width:640px)').matches||matchMedia('(pointer:coarse)').matches));}
  function slugify(t){return String(t||'').trim().toLowerCase().replace(/\s+/g,'-').replace(/[^0-9a-z가-힣_-]/g,'').slice(0,32);}
  function anchorFromHash(){var h=(location.hash||'').replace(/^#/,'');var i=h.indexOf('@');return i>=0?h.slice(i+1):'';}
  function wrapChapters(body){
   var heads=[].slice.call(body.querySelectorAll('h2,[data-ch]'));
   if(heads.length<2)return [];
   var chs=[],n=0;
   heads.forEach(function(hd){
    n++;
    var custom=hd.getAttribute&&hd.getAttribute('data-ch');
    var id='cx-ch-'+n, alias=custom?slugify(custom):slugify(hd.textContent);
    var sec=doc.createElement('section');sec.className='cx-ch';sec.id=id;if(alias)sec.setAttribute('data-ch-alias',alias);
    hd.parentNode.insertBefore(sec,hd);
    var node=hd;
    while(node){var nextIsHead=(node!==hd)&&(node.nodeType===1&&(node.tagName==='H2'||node.getAttribute&&node.getAttribute('data-ch')!=null));if(nextIsHead)break;var mv=node;node=node.nextSibling;sec.appendChild(mv);}
    chs.push({id:id,alias:alias,n:n,title:(hd.textContent||('챕터 '+n)).trim(),el:sec});
   });
   chs.forEach(function(c,i){if(i>1)c.el.classList.add('cx-ch-lazy');});
   return chs;
  }
  function buildTOC(reader,chs){
   var old=reader.querySelector('.cx-toc');if(old)old.parentNode.removeChild(old);
   if(chs.length<2)return null;
   var links=chs.map(function(c){return '<li><a class="cx-toc-a" href="#'+state.slug+'@ch'+c.n+'" data-ch="'+c.id+'"><span class="cx-toc-n">'+(c.n<10?'0':'')+c.n+'</span><span class="cx-toc-t">'+esc(c.title)+'</span></a></li>';}).join('');
   var nav=doc.createElement('nav');nav.className='cx-toc';nav.setAttribute('aria-label','챕터 목차');
   nav.innerHTML='<div class="cx-toc-h">목차</div><ol class="cx-toc-list">'+links+'</ol>';
   reader.appendChild(nav);
   nav.addEventListener('click',function(e){var a=e.target.closest?e.target.closest('.cx-toc-a'):null;if(!a)return;e.preventDefault();var id=a.getAttribute('data-ch');scrollToCh(id);try{history.replaceState(null,'',a.getAttribute('href'));}catch(_e){}});
   return nav;
  }
  function progTicks(chs){
   var pg=doc.getElementById('cxProg');if(!pg)return;
   [].slice.call(pg.querySelectorAll('.cx-prog-tick')).forEach(function(x){x.parentNode.removeChild(x);});
   var doc0=doc.documentElement,H=(doc0.scrollHeight-doc0.clientHeight)||1;
   chs.forEach(function(c){var top=c.el.getBoundingClientRect().top+ (doc0.scrollTop||doc.body.scrollTop||0);var p=Math.min(100,Math.max(0,top/H*100));var t=doc.createElement('i');t.className='cx-prog-tick';t.style.left=p.toFixed(2)+'%';pg.appendChild(t);});
  }
  function scrollToCh(id){var sec=doc.getElementById(id);if(!sec)return;var y=sec.getBoundingClientRect().top+(doc.documentElement.scrollTop||doc.body.scrollTop||0)-72;try{scrollTo({top:y,behavior:'smooth'});}catch(e){scrollTo(0,y);}}
  function savePos(){if(!state.slug||!state.chs.length)return;var sy=doc.documentElement.scrollTop||doc.body.scrollTop||0;var cur=state.chs[0],off=0;for(var i=0;i<state.chs.length;i++){var top=state.chs[i].el.getBoundingClientRect().top+sy;if(top-80<=sy){cur=state.chs[i];off=sy-top;}else break;}try{localStorage.setItem(MEM+state.slug,JSON.stringify({id:cur.id,off:Math.round(off),n:cur.n}));}catch(e){}}
  function activeUpd(){
   var sy=doc.documentElement.scrollTop||doc.body.scrollTop||0, cur=null;
   for(var i=0;i<state.chs.length;i++){var top=state.chs[i].el.getBoundingClientRect().top+sy;if(top-90<=sy)cur=state.chs[i];else break;}
   var nav=state.reader&&state.reader.querySelector('.cx-toc');if(nav){[].slice.call(nav.querySelectorAll('.cx-toc-a')).forEach(function(a){a.classList.toggle('on',cur&&a.getAttribute('data-ch')===cur.id);});}
  }
  function resumeBanner(reader,saved){
   var old=reader.querySelector('.cx-resume');if(old)old.parentNode.removeChild(old);
   var b=doc.createElement('div');b.className='cx-resume';
   b.innerHTML='<span class="cx-resume-tx">읽던 곳이 있어요 · '+(saved.n||1)+'장부터</span><span class="cx-resume-act"><button type="button" class="cx-resume-go">이어읽기</button><button type="button" class="cx-resume-x" aria-label="닫기">처음부터</button></span>';
   var host=reader.querySelector('.cx-rd-body')||reader;host.parentNode.insertBefore(b,host);
   function close(){if(b.parentNode)b.parentNode.removeChild(b);}
   b.querySelector('.cx-resume-go').addEventListener('click',function(){var sec=doc.getElementById(saved.id);if(sec){var y=sec.getBoundingClientRect().top+(doc.documentElement.scrollTop||doc.body.scrollTop||0)+ (saved.off||0)-72;try{scrollTo({top:y,behavior:'smooth'});}catch(e){scrollTo(0,y);}}close();});
   b.querySelector('.cx-resume-x').addEventListener('click',close);
   setTimeout(close,9000);
  }
  CXW.reader={
   init:function(body,slug,it){
    state.slug=slug;state.body=body;
    var reader=body.closest?body.closest('.cx-reader'):(doc.getElementById('cxReader'));
    state.reader=reader||doc.getElementById('cxReader');
    if(litemq()&&state.reader)state.reader.classList.add('cx-lite');else if(state.reader)state.reader.classList.remove('cx-lite');
    var chs=wrapChapters(body);state.chs=chs;
    if(chs.length>=2){buildTOC(state.reader,chs);if(state.reader)state.reader.classList.add('cx-has-toc');}
    else if(state.reader)state.reader.classList.remove('cx-has-toc');
    /* 기준일 표기(있으면) */
    if(it&&it.basis_date){var top=state.reader&&state.reader.querySelector('.cx-rd-time');if(top&&top.textContent.indexOf('기준')<0)top.innerHTML+=' · 기준 '+esc(String(it.basis_date));}
    /* 딥링크 우선, 없으면 이어읽기 배너 */
    var anchor=anchorFromHash(), saved=null;try{saved=JSON.parse(localStorage.getItem(MEM+slug)||'null');}catch(e){saved=null;}
    setTimeout(function(){progTicks(chs);activeUpd();
     if(anchor){var m=/^ch(\d+)$/.exec(anchor);var target=m?('cx-ch-'+m[1]):null;if(!target){for(var i=0;i<chs.length;i++)if(chs[i].alias===anchor){target=chs[i].id;break;}}if(target)scrollToCh(target);}
     else if(saved&&saved.n>1&&chs.length>=2){resumeBanner(state.reader,saved);}
    },220);
    /* 스크롤 훅(중복 방지) */
    if(state.onScroll)try{removeEventListener('scroll',state.onScroll);}catch(e){}
    var tick=false;
    state.onScroll=function(){if(tick)return;tick=true;requestAnimationFrame(function(){tick=false;activeUpd();savePos();});};
    addEventListener('scroll',state.onScroll,{passive:true});
    addEventListener('resize',function(){progTicks(chs);},{passive:true});
   }
  };
 })();

 /* ---- sim-frame: 계산 시뮬레이터 프레임(입력 폼+결과 카드+공식 토글, CXW.sim 레지스트리 구동) ---- */
 (function(){
  if(typeof CXW==='undefined'||!CXW||!CXW.w)return;
  var W2=CXW.w;
  W2['sim-frame']=function(el){
   var name=el.getAttribute('data-calc'), reg=CXW.sim&&CXW.sim[name];
   if(!reg)return;
   var vals={};reg.fields.forEach(function(f){vals[f.k]=f.def;});
   function fieldHTML(f){return '<label class="cxw-sim-f"><span class="cxw-sim-fl">'+esc(f.label)+'</span><span class="cxw-sim-fin"><input type="number" inputmode="decimal" class="cxw-sim-in" data-k="'+f.k+'" value="'+f.def+'" min="'+f.min+'" max="'+f.max+'" step="'+f.step+'"><span class="cxw-sim-u">'+esc(f.unit||'')+'</span></span></label>';}
   function resultHTML(){var r=reg.run(vals);var lines=(r.lines||[]).map(function(l){return '<div class="cxw-sim-line"><span>'+esc(l.label)+'</span><b>'+esc(l.value)+'</b></div>';}).join('');return '<div class="cxw-sim-primary"><span class="cxw-sim-pl">'+esc(r.primary.label)+'</span><b class="cxw-sim-pv">'+esc(r.primary.value)+'</b></div>'+lines;}
   function paint(){var out=el.querySelector('.cxw-sim-out');if(out)out.innerHTML=resultHTML();}
   el.innerHTML='<div class="cxw-sim" data-cx-export data-export-title="'+esc(reg.title||'시뮬레이터')+'"><div class="cxw-sim-h">'+esc(reg.title||'')+'</div><div class="cxw-sim-form">'+reg.fields.map(fieldHTML).join('')+'</div><div class="cxw-sim-out">'+resultHTML()+'</div>'+(reg.formula?'<details class="cxw-sim-formula"><summary>계산식 보기</summary><code>'+esc(reg.formula)+'</code></details>':'')+'</div>';
   el.addEventListener('input',function(e){var i=e.target.closest?e.target.closest('.cxw-sim-in'):null;if(!i)return;var k=i.getAttribute('data-k'),f=null;reg.fields.forEach(function(x){if(x.k===k)f=x;});var v=parseFloat(i.value);if(isNaN(v))return;if(f){if(v<f.min)v=f.min;if(v>f.max)v=f.max;}vals[k]=v;paint();});
   try{CXW.enhanceExports&&CXW.enhanceExports(el);}catch(_e){}
  };
 })();
