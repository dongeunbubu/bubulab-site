
 /* ================= CX v2.1 · 신규 위젯 3종 + 우측 스티키 레일 + 마이크로 피드백 (선언형 data-cx-w, cx- 접두) ================= */
 /* 계약: CXW.w[name] 자동 마운트 유지. mini-chart/evidence-card/slider-calc 신설. 레일은 CXW.reader.init 래핑으로 부착, 현재 챕터는 기존 목차(.cx-toc) 상태 재사용. */
 (function(){
  if(typeof CXW==='undefined'||!CXW||!CXW.w)return;
  var W2=CXW.w, doc=d;
  function J(el,a){var r=el.getAttribute(a);if(!r)return null;try{return JSON.parse(r);}catch(e){return null;}}
  function attr(el,a,dv){var v=el.getAttribute(a);return v==null?dv:v;}
  function fmtNum(n){n=Math.round((parseFloat(n)||0)*100)/100;return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,',');}
  var MCPAL=['#B33A4C','#5E8C7F','#C9A84C','#9C6BA8','#D67A89','#7C243B','#7FB08A','#E08696'];

  /* ---- ① mini-chart: bar(가로 비교)·stack(구성 분해)·donut — 외부 라이브러리 없이 SVG ---- */
  W2['mini-chart']=function(el){
   if(el.getAttribute('data-cx-mc')==='1')return; el.setAttribute('data-cx-mc','1');
   var type=String(attr(el,'data-type','bar')||'bar').toLowerCase();
   var items=J(el,'data-items')||[];
   var cap=attr(el,'data-caption',''), note=attr(el,'data-note',''), unit=attr(el,'data-unit','');
   if(!items.length){el.style.display='none';return;}
   items=items.map(function(it,i){return {label:String(it.label==null?'':it.label),value:(parseFloat(it.value)||0),color:(it.color||MCPAL[i%MCPAL.length])};});
   var total=items.reduce(function(s,it){return s+Math.max(0,it.value);},0)||1;
   var max=items.reduce(function(m,it){return Math.max(m,it.value);},0)||1;
   var aria=type+' 차트: '+items.map(function(it){return it.label+' '+fmtNum(it.value)+unit;}).join(', ');
   var body='';
   if(type==='donut'){
    var C=2*Math.PI*15.9155, off=0, arcs='';
    items.forEach(function(it){var len=Math.max(0,it.value)/total*C;
     arcs+='<circle cx="21" cy="21" r="15.9155" fill="transparent" stroke="'+it.color+'" stroke-width="6" stroke-dasharray="'+len.toFixed(3)+' '+(C-len).toFixed(3)+'" stroke-dashoffset="'+(-off).toFixed(3)+'" transform="rotate(-90 21 21)"><title>'+esc(it.label+' '+fmtNum(it.value)+unit)+'</title></circle>';
     off+=len;});
    var legend=items.map(function(it){var pct=Math.round(Math.max(0,it.value)/total*100);return '<span class="cxw-mc-lg"><span class="cxw-mc-sw" style="background:'+it.color+'"></span>'+esc(it.label)+' · '+pct+'%</span>';}).join('');
    body='<div class="cxw-mc-donut"><svg class="cxw-mc-dsvg" viewBox="0 0 42 42" role="img" aria-label="'+esc(aria)+'"><circle cx="21" cy="21" r="15.9155" fill="transparent" stroke="var(--cx-border)" stroke-width="6"></circle>'+arcs+'<text class="cxw-mc-dc" x="21" y="21" text-anchor="middle" dominant-baseline="central">'+esc(fmtNum(total)+unit)+'</text><text class="cxw-mc-dl" x="21" y="27" text-anchor="middle">'+esc(attr(el,'data-center','합계'))+'</text></svg><div class="cxw-mc-legend">'+legend+'</div></div>';
   } else if(type==='stack'){
    var x=0, segs='';
    items.forEach(function(it){var w=Math.max(0,it.value)/total*100;segs+='<rect x="'+x.toFixed(3)+'" y="0" width="'+w.toFixed(3)+'" height="26" fill="'+it.color+'"><title>'+esc(it.label+' '+fmtNum(it.value)+unit)+'</title></rect>';x+=w;});
    var legend2=items.map(function(it){var pct=Math.round(Math.max(0,it.value)/total*100);return '<span class="cxw-mc-lg"><span class="cxw-mc-sw" style="background:'+it.color+'"></span>'+esc(it.label)+' · '+pct+'%</span>';}).join('');
    body='<div class="cxw-mc-stack"><svg class="cxw-mc-stackbar" viewBox="0 0 100 26" preserveAspectRatio="none" role="img" aria-label="'+esc(aria)+'">'+segs+'</svg></div><div class="cxw-mc-legend">'+legend2+'</div>';
   } else {
    var rows=items.map(function(it){var w=Math.max(1,it.value/max*100);
     return '<div class="cxw-mc-row"><span class="cxw-mc-lab">'+esc(it.label)+'</span><span class="cxw-mc-tr"><svg class="cxw-mc-svg" viewBox="0 0 100 15" preserveAspectRatio="none" aria-hidden="true"><rect x="0" y="0" width="'+w.toFixed(2)+'" height="15" fill="'+it.color+'"></rect></svg></span><span class="cxw-mc-val">'+esc(fmtNum(it.value)+unit)+'</span></div>';}).join('');
    body='<div class="cxw-mc-rows" role="img" aria-label="'+esc(aria)+'">'+rows+'</div>';
   }
   if(el.className.indexOf('cxw-mc')<0)el.className=('cxw-mc '+el.className).replace(/\s+$/,'');
   el.innerHTML=(cap?'<div class="cxw-mc-cap">'+esc(cap)+'</div>':'')+body+(note?'<div class="cxw-mc-note">'+esc(note)+'</div>':'');
  };

  /* ---- ② evidence-card: 뉴스·발표 헤드라인(신문 스크랩 결, 홈 팔레트) ---- */
  W2['evidence-card']=function(el){
   if(el.getAttribute('data-cx-ev')==='1')return; el.setAttribute('data-cx-ev','1');
   var kind=attr(el,'data-kind','발표'), title=attr(el,'data-title',''), src=attr(el,'data-source','');
   var date=attr(el,'data-date',''), note=attr(el,'data-note',''), img=attr(el,'data-img',''), href=attr(el,'data-href','');
   if(!title){el.style.display='none';return;}
   var kmap={'발표':['cxw-ev-k-announce','📢'],'보도':['cxw-ev-k-press','📰'],'화면':['cxw-ev-k-screen','🖥️']};
   var km=kmap[kind]||kmap['발표'];
   var inner='<div class="cxw-ev-in"><div class="cxw-ev-top"><span class="cxw-ev-kind '+km[0]+'">'+km[1]+' '+esc(kind)+'</span>'+(src?'<span class="cxw-ev-src">'+esc(src)+'</span>':'')+(date?'<span class="cxw-ev-date">'+esc(date)+'</span>':'')+'</div><div class="cxw-ev-title">'+esc(title)+(href?'<i class="cxw-ev-arr" aria-hidden="true">↗</i>':'')+'</div>'+(note?'<div class="cxw-ev-note">'+esc(note)+'</div>':'')+(img?'<img class="cxw-ev-img" loading="lazy" decoding="async" src="'+esc(img)+'" alt="'+esc(title)+'">':'')+'</div>';
   if(el.className.indexOf('cxw-ev')<0)el.className=('cxw-ev '+el.className).replace(/\s+$/,'');
   if(href){el.innerHTML='<a class="cxw-ev-card" href="'+esc(href)+'" target="_blank" rel="noopener">'+inner+'</a>';}
   else{el.innerHTML='<div class="cxw-ev-card">'+inner+'</div>';}
  };

  /* ---- ③ slider-calc: 슬라이더 즉시 계산 — CXW.calc 레지스트리 재사용 ---- */
  W2['slider-calc']=function(el){
   if(el.getAttribute('data-cx-slc')==='1')return; el.setAttribute('data-cx-slc','1');
   var fnName=attr(el,'data-calc',''), fn=CXW.calc&&CXW.calc[fnName];
   var argsT=J(el,'data-args'); if(!argsT||!argsT.length)argsT=['$'];
   var lab=attr(el,'data-label','값'), unit=attr(el,'data-unit','');
   var mn=parseFloat(attr(el,'data-min','0')), mx=parseFloat(attr(el,'data-max','100')), st=parseFloat(attr(el,'data-step','1')), dv=parseFloat(attr(el,'data-def',''));
   if(isNaN(dv))dv=mn;
   var outLab=attr(el,'data-out-label','결과'), outUnit=attr(el,'data-out-unit',''), fmt=attr(el,'data-format','num'), outKey=attr(el,'data-out-key','');
   var note=attr(el,'data-note',''), cap=attr(el,'data-caption','');
   function fmtOut(v){if(v==null||isNaN(v))return '—';if(fmt==='won')return fmtWon(Math.round(v));if(fmt==='pct')return String(Math.round(v*10)/10);return fmtNum(v);}
   function calc(val){
    if(typeof fn!=='function')return val;
    var args=argsT.map(function(a){return a==='$'?val:a;});
    var r; try{r=fn.apply(null,args);}catch(e){r=null;}
    if(r&&typeof r==='object'){var keys=Object.keys(r);r=(outKey&&r[outKey]!=null)?r[outKey]:(r.value!=null?r.value:(keys.length?r[keys[0]]:null));}
    return r;
   }
   function ovHTML(v){return esc(String(fmtOut(calc(v))))+(outUnit?'<em>'+esc(outUnit)+'</em>':'');}
   function tpl(v){
    return '<div class="cxw-slc-out" data-cx-export data-export-title="'+esc(outLab)+'"><span class="cxw-slc-ol">'+esc(outLab)+'</span><b class="cxw-slc-ov" data-slc-ov>'+ovHTML(v)+'</b></div>'
     +'<div class="cxw-slc-lab"><span>'+esc(lab)+'</span><span class="cxw-slc-lv" data-slc-lv>'+esc(fmtNum(v)+unit)+'</span></div>'
     +'<input type="range" class="cxw-slc-range" min="'+mn+'" max="'+mx+'" step="'+st+'" value="'+v+'" aria-label="'+esc(lab)+'">'
     +'<div class="cxw-slc-scale"><span>'+esc(fmtNum(mn)+unit)+'</span><span>'+esc(fmtNum(mx)+unit)+'</span></div>';
   }
   if(el.className.indexOf('cxw-slc')<0)el.className=('cxw-slc '+el.className).replace(/\s+$/,'');
   el.innerHTML=(cap?'<div class="cxw-slc-cap">'+esc(cap)+'</div>':'')+tpl(dv)+(note?'<div class="cxw-slc-note">'+esc(note)+'</div>':'');
   var ov=el.querySelector('[data-slc-ov]'), lv=el.querySelector('[data-slc-lv]'), rg=el.querySelector('.cxw-slc-range');
   function paint(v){
    if(lv)lv.textContent=fmtNum(v)+unit;
    if(ov){ov.innerHTML=ovHTML(v); if(!rm){ov.classList.remove('cxw-slc-pop');void ov.offsetWidth;ov.classList.add('cxw-slc-pop');}}
    try{el.dispatchEvent(new CustomEvent('cx:calc',{bubbles:true,detail:{label:outLab,value:(fmtOut(calc(v))+(outUnit||''))}}));}catch(e){}
   }
   if(rg)rg.addEventListener('input',function(){var v=parseFloat(rg.value);if(isNaN(v))return;paint(v);});
   try{CXW.enhanceExports&&CXW.enhanceExports(el);}catch(e){}
  };

  /* ---- 우측 스티키 레일(.cx-rrail) — 기존 목차 상태 재사용, ≥1400px는 CSS가 표시 게이트 ---- */
  var RS={obs:null,onScroll:null,terms:[]};
  function railCleanup(){if(RS.obs){try{RS.obs.disconnect();}catch(e){}RS.obs=null;}if(RS.onScroll){try{removeEventListener('scroll',RS.onScroll);}catch(e){}RS.onScroll=null;}RS.terms=[];}
  function clip(t,n){t=String(t||'').replace(/\s+/g,' ').trim();return t.length>n?t.slice(0,n-1)+'…':t;}
  function firstEmph(sec){var e=sec.querySelector('.cx-hl,.cx-pull,strong,b');if(e){var t=clip(e.textContent,90);if(t)return t;}var p=sec.querySelector('.cx-rd-p,p');return p?clip(p.textContent,90):'';}
  function chapterKey(sec){
   var h2=sec.querySelector('.cx-rd-h2,h2,[data-ch]');
   var dk=sec.getAttribute('data-key')||(h2&&h2.getAttribute?h2.getAttribute('data-key'):'');
   var num='',line='';
   if(dk){var parts=String(dk).split('|');if(parts.length>1){num=parts[0].trim();line=parts.slice(1).join('|').trim();}else{line=String(dk).trim();}}
   var title=h2?clip(h2.textContent,60):'';
   if(!line)line=firstEmph(sec);
   return {num:num,title:title,line:line};
  }
  function collectTerms(sec){
   var out=[],seen={};
   [].slice.call(sec.querySelectorAll('[data-cx-w="term-chip"],.cxw-term,.cx-term')).forEach(function(n){
    var term=String(n.getAttribute('data-term')||n.textContent||'').replace(/[▸▾•?]+/g,'').replace(/\s+/g,' ').trim();
    var def=n.getAttribute('data-def')||n.getAttribute('data-tip')||'';
    if(!term||seen[term])return;seen[term]=1;out.push({term:clip(term,26),def:clip(def,72),node:n});
   });
   return out;
  }
  function currentSec(host){
   var toc=host.querySelector('.cx-toc');
   if(toc){var on=toc.querySelector('.cx-toc-a.on')||toc.querySelector('.cx-toc-a');if(on){var id=on.getAttribute('data-ch');var s=id&&doc.getElementById(id);if(s)return s;}}
   var chs=[].slice.call(host.querySelectorAll('.cx-ch'));
   if(!chs.length)return host.querySelector('.cx-rd-body')||host;
   var sy=doc.documentElement.scrollTop||doc.body.scrollTop||0,cur=chs[0];
   for(var i=0;i<chs.length;i++){var top=chs[i].getBoundingClientRect().top+sy;if(top-100<=sy)cur=chs[i];else break;}
   return cur;
  }
  function refreshRail(host){
   var sec=currentSec(host);if(!sec)return;
   var key=host.querySelector('.cx-rrail-key'),list=host.querySelector('.cx-rrail-tlist');if(!key)return;
   var k=chapterKey(sec);
   key.innerHTML='<div class="cx-rrail-h">지금 챕터</div>'+(k.num?'<div class="cx-rrail-kn">'+esc(k.num)+'</div>':'')+(k.title?'<div class="cx-rrail-kt">'+esc(k.title)+'</div>':'')+(k.line?'<div class="cx-rrail-kd">'+esc(k.line)+'</div>':'');
   RS.terms=collectTerms(sec);
   if(list){
    if(RS.terms.length)list.innerHTML=RS.terms.map(function(t,i){return '<li><button type="button" class="cx-rrail-term" data-ti="'+i+'"><b>'+esc(t.term)+'</b>'+(t.def?'<span>'+esc(t.def)+'</span>':'')+'</button></li>';}).join('');
    else list.innerHTML='<li class="cx-rrail-empty">이 챕터에는 용어 칩이 없어요.</li>';
   }
  }
  function pinCalc(host,label,value){var pin=host.querySelector('.cx-rrail-pin');if(!pin||value==null)return;pin.innerHTML='<div class="cx-rrail-pl">내 계산 결과</div><div class="cx-rrail-pv">'+esc(String(value))+'</div>'+(label?'<div class="cx-rrail-ps">'+esc(String(label))+'</div>':'');pin.classList.add('on');}
  function ctaHTML(it){
   var target=null,klabel='다음 콘텐츠';
   if(it&&it.pair){var p=findItem(it.pair);if(p){target=p;klabel=(p.type==='tool'?'페어 도구':(p.type==='kit'?'실행 키트':'이어 읽기'));}}
   if(!target){var cols=liveColumns(),idx=-1,i;for(i=0;i<cols.length;i++)if(cols[i].slug===(it&&it.slug)){idx=i;break;}var nx=(idx>=0&&idx<cols.length-1)?cols[idx+1]:(cols[0]||null);if(nx&&nx.slug!==(it&&it.slug)){target=nx;klabel='다음 칼럼';}}
   if(!target)return '';
   var href=(typeof itemHref==='function')?itemHref(target):('#'+target.slug);
   return '<a class="cx-rrail-cta" href="'+href+'"><span class="cx-rrail-ck">'+esc(klabel)+'</span><span class="cx-rrail-ct">'+esc(target.title||target.slug)+' <i class="cx-rrail-cx" aria-hidden="true">→</i></span></a>';
  }
  function buildRail(body,slug,it){
   var host=doc.getElementById('cxReader');if(!host)return;
   railCleanup();
   var old=host.querySelector('.cx-rrail');if(old&&old.parentNode)old.parentNode.removeChild(old);
   var rail=doc.createElement('aside');rail.className='cx-rrail';rail.setAttribute('aria-label','읽기 도우미');
   rail.innerHTML='<div class="cx-rrail-card cx-rrail-key"></div>'
    +'<div class="cx-rrail-card cx-rrail-terms"><div class="cx-rrail-h">용어 미니 사전</div><ul class="cx-rrail-tlist"></ul></div>'
    +'<div class="cx-rrail-pin" aria-live="polite"></div>'
    +ctaHTML(it);
   host.appendChild(rail);host.classList.add('cx-has-rrail');
   rail.addEventListener('click',function(e){var b=e.target.closest?e.target.closest('.cx-rrail-term'):null;if(!b)return;var t=RS.terms[parseInt(b.getAttribute('data-ti'),10)];if(!t||!t.node)return;try{t.node.scrollIntoView({behavior:rm?'auto':'smooth',block:'center'});}catch(_e){scrollTo(0,t.node.getBoundingClientRect().top+(doc.documentElement.scrollTop||0)-96);}t.node.classList.add('cx-term-flash');setTimeout(function(){t.node.classList.remove('cx-term-flash');},1100);});
   function simRead(e){var sim=e.target&&e.target.closest?e.target.closest('.cxw-sim'):null;if(!sim)return;requestAnimationFrame(function(){var pl=sim.querySelector('.cxw-sim-pl'),pv=sim.querySelector('.cxw-sim-pv');if(pv)pinCalc(host,pl?pl.textContent:'',pv.textContent);});}
   body.addEventListener('cx:calc',function(ev){if(ev&&ev.detail&&ev.detail.value!=null)pinCalc(host,ev.detail.label,ev.detail.value);});
   body.addEventListener('input',simRead);body.addEventListener('change',simRead);
   var toc=host.querySelector('.cx-toc');
   if(toc&&'MutationObserver'in window){RS.obs=new MutationObserver(function(){refreshRail(host);});RS.obs.observe(toc,{subtree:true,attributes:true,attributeFilter:['class']});}
   var tick=false;RS.onScroll=function(){if(tick)return;tick=true;requestAnimationFrame(function(){tick=false;refreshRail(host);});};addEventListener('scroll',RS.onScroll,{passive:true});
   setTimeout(function(){refreshRail(host);},260);
  }
  if(CXW.reader&&typeof CXW.reader.init==='function'){var _rinit=CXW.reader.init;CXW.reader.init=function(body,slug,it){var r=_rinit.apply(this,arguments);try{buildRail(body,slug,it);}catch(e){}return r;};}
  CXW.rrail={build:buildRail,refresh:function(){var h=doc.getElementById('cxReader');if(h)refreshRail(h);}};

  /* ---- 마이크로 피드백(피드백 2): 결정트리 진행 점 + 체크 팝 — transform만, reduced-motion 존중 ---- */
  if(!window.__cxMicro){window.__cxMicro=1;
   var DTC=(typeof WeakMap!=='undefined')?new WeakMap():null;
   function dtGet(dt){return DTC?(DTC.get(dt)||0):(parseInt(dt.getAttribute('data-cx-dtc')||'0',10));}
   function dtSet(dt,n){if(DTC)DTC.set(dt,n);else dt.setAttribute('data-cx-dtc',n);}
   function dtDots(dt){var n=dtGet(dt),top=dt.querySelector('.cxw-dt-top');if(!top)return;var strip=top.querySelector('.cx-dtprog');if(!strip){strip=doc.createElement('span');strip.className='cx-dtprog';top.appendChild(strip);}var cap=Math.min(Math.max(n,1),8),h='';for(var i=0;i<cap;i++)h+='<i class="'+(i<n?'on':'')+'"></i>';strip.innerHTML=h;}
   doc.addEventListener('click',function(e){
    var t=e.target;if(!t||!t.closest)return;
    var opt=t.closest('.cxw-dt-opt');if(opt){var dt=opt.closest('.cxw-dt');if(dt){dtSet(dt,dtGet(dt)+1);setTimeout(function(){dtDots(dt);},0);}return;}
    var bk=t.closest('[data-dt="back"]');if(bk){var dt2=bk.closest('.cxw-dt');if(dt2){dtSet(dt2,Math.max(0,dtGet(dt2)-1));setTimeout(function(){dtDots(dt2);},0);}return;}
    var rsb=t.closest('[data-dt="restart"]');if(rsb){var dt3=rsb.closest('.cxw-dt');if(dt3){dtSet(dt3,0);setTimeout(function(){dtDots(dt3);},0);}return;}
    var chk=t.closest('.cxw-sum-chk');if(chk){var box=chk.querySelector('.cxw-sum-box');if(box&&!rm){box.classList.remove('cx-pop');void box.offsetWidth;box.classList.add('cx-pop');}return;}
   },true);
  }
 })();
