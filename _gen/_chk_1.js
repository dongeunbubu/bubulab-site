

(function(){
 var d=document, w=window;
 var scope=d.querySelector('.jm-scope'); if(!scope) return;
 var mq=function(q){return w.matchMedia?w.matchMedia(q).matches:false;};
 var reduce=mq('(prefers-reduced-motion: reduce)');
 var coarse=mq('(pointer: coarse)');

 var hdr=d.getElementById('jmhdr');
 if(hdr){w.addEventListener('scroll',function(){hdr.classList.toggle('jm-scrolled', w.scrollY>8);},{passive:true});}

 (function(){
  var btn=hdr&&hdr.querySelector('.jm-navbtn'); if(!btn) return;
  var main=hdr.querySelector('.jm-menu-main'), sub=hdr.querySelector('.jm-menu-sub');
  var links=''; [main,sub].forEach(function(nav){ if(!nav) return;
   [].slice.call(nav.querySelectorAll('a')).forEach(function(a){
    links+='<a href="'+a.getAttribute('href')+'">'+(a.textContent||'').trim()+'</a>'; }); });
  var dr=d.createElement('div'); dr.className='jm-drawer';
  dr.innerHTML='<div class="jm-dpnl"><button class="jm-dclose" type="button" aria-label="닫기">×</button>'
   +'<div class="jm-dlogo"><i></i>부부연구소</div><nav class="jm-dnav">'+links+'</nav>'
   +'<a class="jm-dcta" href="/home#subscribe">구독하기</a></div>';
  d.body.appendChild(dr);
  function open(){dr.classList.add('jm-on');btn.classList.add('jm-on');d.body.style.overflow='hidden';}
  function close(){dr.classList.remove('jm-on');btn.classList.remove('jm-on');d.body.style.overflow='';}
  btn.addEventListener('click',function(){dr.classList.contains('jm-on')?close():open();});
  dr.addEventListener('click',function(e){var t=e.target;
   if(t===dr||t.classList.contains('jm-dclose')||t.tagName==='A')close();});
  d.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
 })();

 var revs=[].slice.call(scope.querySelectorAll('.jm-reveal,.jm-zlabel,.jm-mark'));
 var nodes=[].slice.call(scope.querySelectorAll('.jm-node'));
 if(reduce||!('IntersectionObserver' in w)){
  revs.forEach(function(e){e.classList.add('jm-in');}); nodes.forEach(function(e){e.classList.add('jm-in');});
 } else {
  var io=new IntersectionObserver(function(es){es.forEach(function(en){
   if(en.isIntersecting){en.target.classList.add('jm-in');io.unobserve(en.target);}});},
   {threshold:.16,rootMargin:'0px 0px -8% 0px'});
  revs.forEach(function(e){io.observe(e);});
  var nio=new IntersectionObserver(function(es){es.forEach(function(en){
   if(en.isIntersecting){en.target.classList.add('jm-in');nio.unobserve(en.target);}});},
   {threshold:.2,rootMargin:'0px 0px -6% 0px'});
  nodes.forEach(function(e){nio.observe(e);});
 }

 (function(){
  var KEY='bbf_hub_bloom', seen={};
  try{ seen=JSON.parse(w.localStorage.getItem(KEY)||'{}')||{}; }catch(e){ seen={}; }
  nodes.forEach(function(n){
   var slug=n.getAttribute('data-slug');
   if(slug&&seen[slug]) n.classList.add('jm-visited');
   n.addEventListener('click',function(){
    if(!slug) return; seen[slug]=1; n.classList.add('jm-visited');
    try{ w.localStorage.setItem(KEY, JSON.stringify(seen)); }catch(e){}
   });
  });
 })();

 var draw=scope.querySelector('.jm-draw');
 var map=d.getElementById('jmMap');
 if(draw&&map&&!reduce){
  var L=0; try{L=draw.getTotalLength();}catch(e){L=0;}
  if(L){draw.style.strokeDasharray=L; draw.style.strokeDashoffset=L;
   var ticking=false;
   function drawUpd(){ ticking=false;
    var r=map.getBoundingClientRect(), vh=w.innerHeight||d.documentElement.clientHeight;
    var p=(vh*0.82 - r.top)/(r.height*0.78); p=p<0?0:(p>1?1:p);
    draw.style.strokeDashoffset=(L*(1-p)).toFixed(1);
   }
   w.addEventListener('scroll',function(){if(!ticking){ticking=true;w.requestAnimationFrame(drawUpd);}},{passive:true});
   w.addEventListener('resize',drawUpd,{passive:true}); drawUpd();
  }
 } else if(draw){ draw.style.strokeDashoffset=0; }

 var pop=d.getElementById('jmPop');
 if(pop&&map){
  var meta=d.getElementById('jmPopMeta'), pt=d.getElementById('jmPopTitle'),
      ph=d.getElementById('jmPopHook'), pf=d.getElementById('jmPopFoot');
  var hideT=null, curNode=null;
  function badges(node){
   var tk=node.getAttribute('data-tk'), t=node.getAttribute('data-t');
   var s='<span class="jm-lt jm-pt-'+tk+'">'+t+'</span>';
   var st=node.getAttribute('data-stage'), sm={seed:'🌱 새싹',bud:'🌸 봉오리',bloom:'🌺 만개'};
   if(st&&sm[st]) s+='<span class="jm-b jm-b-stage">'+sm[st]+'</span>';
   s+= node.getAttribute('data-prem')==='1'
     ? '<span class="jm-b jm-b-prem">🔒 프리미엄</span>' : '<span class="jm-b jm-b-free">🆓 무료</span>';
   if(node.getAttribute('data-live')!=='1') s+='<span class="jm-b jm-b-soon">곧 만나요</span>';
   return s;
  }
  function fill(node){
   meta.innerHTML=badges(node);
   pt.textContent=node.getAttribute('data-title')||'';
   ph.textContent=node.getAttribute('data-hook')||'';
   if(node.getAttribute('data-live')==='1'){
    var href=node.getAttribute('href')||'#';
    pf.innerHTML='<a class="jm-pgo" href="'+href+'">열어보기 <span class="jm-ar">→</span></a>';
   } else { pf.innerHTML='<div class="jm-psoon">곧 준비해서 만나러 올게요 🌱</div>'; }
  }
  function place(node){
   var top=node.offsetTop, left=node.offsetLeft, below=(top < map.clientHeight*0.16);
   pop.classList.toggle('jm-below', below);
   var pw=pop.offsetWidth, ph2=pop.offsetHeight;
   var x=left, y=below ? (top+46+ph2/2) : (top-46-ph2/2);
   var minX=pw/2+6, maxX=map.clientWidth-pw/2-6;
   if(x<minX)x=minX; if(x>maxX)x=maxX;
   pop.style.left=x+'px'; pop.style.top=y+'px'; pop.style.transform='translate(-50%,-50%)';
  }
  function show(node){ if(hideT){clearTimeout(hideT);hideT=null;} curNode=node; fill(node); pop.classList.add('jm-show'); place(node); }
  function hide(){ pop.classList.remove('jm-show'); curNode=null; }
  function hideSoon(){ hideT=setTimeout(hide,140); }
  nodes.forEach(function(node){
   if(!coarse){
    node.addEventListener('mouseenter',function(){show(node);});
    node.addEventListener('mouseleave',hideSoon);
    node.addEventListener('focus',function(){show(node);});
    node.addEventListener('blur',hideSoon);
   } else {
    node.addEventListener('click',function(e){
     var live=node.getAttribute('data-live')==='1';
     if(curNode===node){ if(live){ return; } hide(); return; }
     e.preventDefault(); show(node);
    });
   }
  });
  pop.addEventListener('mouseenter',function(){if(hideT){clearTimeout(hideT);hideT=null;}});
  pop.addEventListener('mouseleave',hideSoon);
  d.addEventListener('click',function(e){ if(coarse&&curNode&&!map.contains(e.target)) hide(); });
  w.addEventListener('scroll',function(){ if(curNode) place(curNode); },{passive:true});
 }

 var chips=d.getElementById('jmChips');
 if(chips&&map){
  chips.addEventListener('click',function(e){
   var b=e.target.closest('.jm-chip'); if(!b||!chips.contains(b)) return;
   [].slice.call(chips.querySelectorAll('.jm-chip')).forEach(function(x){
    x.classList.remove('jm-on'); x.setAttribute('aria-pressed','false'); });
   b.classList.add('jm-on'); b.setAttribute('aria-pressed','true');
   var f=b.getAttribute('data-f')||'all';
   map.classList.remove('jm-f-column','jm-f-tool','jm-f-kit');
   if(f!=='all') map.classList.add('jm-f-'+f);
  });
 }

/* [T18] 바람 인터랙션(줄기 잎·꽃) + 구간별 낙하 파티클 IO 게이팅 — jm- 접두, 전역 오염 없음 */
 (function(){
  var falls=[].slice.call(scope.querySelectorAll('.jm-fall'));
  if(falls.length && !reduce && ('IntersectionObserver' in w)){
   var fio=new IntersectionObserver(function(es){es.forEach(function(en){
    en.target.classList.toggle('jm-run', en.isIntersecting); });},{threshold:0.02});
   falls.forEach(function(f){ fio.observe(f); });
  }
  if(reduce||coarse) return;
  var wind=[].slice.call(scope.querySelectorAll('.jm-windel'));
  if(!wind.length) return;
  wind.forEach(function(el){ el._jmph=Math.random()*6.283; el._jmst=0.55+Math.random()*0.95; });
  if('IntersectionObserver' in w){
   var gio=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){var el=en.target,k=(parseInt(el.getAttribute('data-i'),10)||0)%7;setTimeout(function(){el.classList.add('jm-grew');},k*95);gio.unobserve(el);}});},{threshold:0.08,rootMargin:'0px 0px -6% 0px'});
   wind.forEach(function(el){gio.observe(el);});
  }else{ wind.forEach(function(el){el.classList.add('jm-grew');}); }
  (function(){var nodes=[].slice.call(scope.querySelectorAll('.jm-node'));if(!nodes.length)return;
   nodes.forEach(function(nd){nd.addEventListener('mouseenter',function(){var ny=(parseFloat(nd.style.top||'0')/100)*4150;for(var i=0;i<wind.length;i++){var el=wind[i];if(!el.classList.contains('jm-grew'))continue;var wy=parseFloat(el.getAttribute('data-y'))||0;if(Math.abs(wy-ny)<300){el.classList.remove('jm-react');void el.offsetWidth;el.classList.add('jm-react');(function(e){setTimeout(function(){e.classList.remove('jm-react');},1000);})(el);}}target=(Math.random()<0.5?-1:1)*0.5;jstart();},{passive:true});});
  })();
  var target=0,cur=0,lastX=null,lastT=0,running=false,vis=true;
  var mapEl=d.getElementById('jmMap');
  function jnow(){ return (w.performance&&w.performance.now)?w.performance.now():Date.now(); }
  function jtick(){
   cur+=(target-cur)*0.06; target*=0.93;
   var tt=jnow()/1000;
   for(var i=0;i<wind.length;i++){ var el=wind[i];
    var ang=cur*12*el._jmst + Math.sin(tt*1.05+el._jmph)*2.6*el._jmst;
    el.style.transform='rotate('+ang.toFixed(2)+'deg)'; }
   if(vis){ w.requestAnimationFrame(jtick); } else { running=false; }
  }
  function jstart(){ if(running||!vis)return; running=true; w.requestAnimationFrame(jtick); }
  if(('IntersectionObserver' in w) && mapEl){
   var mio=new IntersectionObserver(function(es){ vis=es[0].isIntersecting; if(vis) jstart(); },{threshold:0});
   mio.observe(mapEl);
  }
  w.addEventListener('mousemove',function(e){
   var t=jnow();
   if(lastX!=null){ var dt=Math.max(t-lastT,16); var vx=(e.clientX-lastX)/dt; var v=vx*2.2; target=v<-1?-1:(v>1?1:v); }
   lastX=e.clientX; lastT=t; jstart();
  },{passive:true});
  jstart();
 })();

})();

