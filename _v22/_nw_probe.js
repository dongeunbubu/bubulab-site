(function(){var W2={},rm=false,window={},document={},esc=function(s){return s},fmtNum=function(n){return String(n)},attr=function(e,a,d){return d},J=function(){return null},MCPAL=[],LTPAL=[],cxOnce=function(_,cb){cb(true)},tween=function(){},commaInt=function(){},shSpark=function(){return{W:1,H:1,area:"",line:"",len:1}},pathLen=function(){return 1},cxReveal=function(){};
  /* ---- ② evidence-card: 뉴스·발표 헤드라인(신문 스크랩 결, 홈 팔레트) + 등장 애니(살짝 슬라이드+페이드, IO 1회) ---- */
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
   cxReveal(el);
  };
  /* __SMK_SH0__ ④ stat-hero: 큰 숫자 1개 + 맥락 한 줄 + 옵션 미니 스파크라인(홈 팔레트 · 숫자 count-up · 선 그리기, 챕터 사이 삽입용) */
  W2['stat-hero']=function(el){
   if(el.getAttribute('data-cx-shx')==='1')return; el.setAttribute('data-cx-shx','1');
   var vraw=attr(el,'data-value',null);
   if(vraw==null||vraw===''){el.style.display='none';return;}
   var val=parseFloat(String(vraw).replace(/,/g,''))||0;
   var pre=attr(el,'data-prefix',''), suf=attr(el,'data-suffix',attr(el,'data-unit',''));
   var ctx=attr(el,'data-label',attr(el,'data-context','')), cap=attr(el,'data-caption',''), note=attr(el,'data-note','');
   var delta=attr(el,'data-delta',''), trend=String(attr(el,'data-trend','')||'').toLowerCase();
   var dur=parseFloat(attr(el,'data-dur','820'))||820; if(dur<600)dur=600; if(dur>900)dur=900;
   var series=J(el,'data-series'); if(!(series&&series.length>1))series=null;
   var anim=!rm&&('IntersectionObserver'in window);
   var tcls=trend==='up'?'cxw-sh-up':(trend==='down'?'cxw-sh-down':(trend==='flat'?'cxw-sh-flat':''));
   var sd=series?shSpark(series):null;
   var sparkHTML=sd?('<div class="cxw-sh-spark"><svg class="cxw-sh-ssvg" viewBox="0 0 '+sd.W+' '+sd.H+'" preserveAspectRatio="none" aria-hidden="true"><path class="cxw-sh-area" d="'+sd.area+'"></path><path class="cxw-sh-line" d="'+sd.line+'"></path></svg></div>'):'';
   if(el.className.indexOf('cxw-sh')<0)el.className=('cxw-sh '+el.className).replace(/\s+$/,'');
   el.innerHTML=(cap?'<div class="cxw-sh-cap">'+esc(cap)+'</div>':'')
    +'<div class="cxw-sh-main"><span class="cxw-sh-num">'+(pre?'<span class="cxw-sh-pre">'+esc(pre)+'</span>':'')+'<b class="cxw-sh-v" data-mcto="'+val+'">'+esc(anim?'0':fmtNum(val))+'</b>'+(suf?'<span class="cxw-sh-suf">'+esc(suf)+'</span>':'')+'</span>'+(delta?'<span class="cxw-sh-delta '+tcls+'">'+esc(delta)+'</span>':'')+'</div>'
    +(ctx?'<div class="cxw-sh-ctx">'+esc(ctx)+'</div>':'')
    +sparkHTML
    +(note?'<div class="cxw-sh-note">'+esc(note)+'</div>':'');
   var vEl=el.querySelector('.cxw-sh-v'), lineEl=el.querySelector('.cxw-sh-line');
   if(anim&&lineEl&&sd){lineEl.style.strokeDasharray=sd.len.toFixed(2)+' '+sd.len.toFixed(2);lineEl.style.strokeDashoffset=sd.len.toFixed(2);}
   cxOnce(el,function(imm){
    if(vEl){if(imm)vEl.textContent=fmtNum(val);else tween(dur,0,function(k){vEl.textContent=commaInt(val*k);},function(){vEl.textContent=fmtNum(val);});}
    if(lineEl&&sd){if(imm){lineEl.style.strokeDashoffset='0';}else{tween(780,140,function(k){lineEl.style.strokeDashoffset=(sd.len*(1-k)).toFixed(2);},function(){lineEl.style.strokeDashoffset='0';});}}
   });
  };
  /* __SMK_SH1__ */

  /* __SMK_LT0__ ⑤ line-trend: 시계열 꺾은선(연도 라벨 · 점 호버 툴팁 · 선 그리기 애니 · 2계열 비교 예: 기준금리 vs 적금금리), 외부 라이브러리 없이 SVG */
  W2['line-trend']=function(el){
   if(el.getAttribute('data-cx-lt')==='1')return; el.setAttribute('data-cx-lt','1');
   var xs=J(el,'data-x')||[];
   var rawS=J(el,'data-series');
   var series=[];
   if(rawS&&rawS.length&&typeof rawS[0]==='object'&&!(rawS[0] instanceof Array)){
    series=rawS.map(function(s,i){return {name:String(s.name==null?('계열'+(i+1)):s.name),color:(s.color||LTPAL[i%LTPAL.length]),values:(s.values||s.data||[]).map(function(v){return parseFloat(v)||0;})};});
   } else if(rawS&&rawS.length){
    series=[{name:attr(el,'data-name','계열'),color:LTPAL[0],values:rawS.map(function(v){return parseFloat(v)||0;})}];
   }
   if(!series.length||!xs.length){el.style.display='none';return;}
   var unit=attr(el,'data-unit',''), cap=attr(el,'data-caption',''), note=attr(el,'data-note','');
   var nx=xs.length, allv=[];
   series.forEach(function(s){s.values.forEach(function(v){allv.push(v);});});
   var dmin=attr(el,'data-min',null), dmax=attr(el,'data-max',null);
   var ymin=(dmin!=null&&dmin!=='')?parseFloat(dmin):Math.min.apply(null,allv);
   var ymax=(dmax!=null&&dmax!=='')?parseFloat(dmax):Math.max.apply(null,allv);
   if(ymax===ymin){ymax=ymin+1;}
   var vpad=(ymax-ymin)*0.12;ymin-=vpad;ymax+=vpad;
   var W=520,H=250,ml=38,mr=12,mt=14,mb=28;
   function X(i){return nx<2?ml+(W-ml-mr)/2:ml+i*(W-ml-mr)/(nx-1);}
   function Y(v){return mt+(1-(v-ymin)/(ymax-ymin))*(H-mt-mb);}
   var anim=!rm&&('IntersectionObserver'in window);
   var grid='',GN=4,gi;
   for(gi=0;gi<=GN;gi++){var gv=ymin+(ymax-ymin)*gi/GN,gy=Y(gv);
    grid+='<line class="cxw-lt-grid" x1="'+ml+'" y1="'+gy.toFixed(1)+'" x2="'+(W-mr)+'" y2="'+gy.toFixed(1)+'"></line>';
    grid+='<text class="cxw-lt-yl" x="'+(ml-5)+'" y="'+(gy+3).toFixed(1)+'" text-anchor="end">'+esc(fmtNum(Math.round(gv*10)/10)+unit)+'</text>';}
   var xlab='';xs.forEach(function(xl,i){xlab+='<text class="cxw-lt-xl" x="'+X(i).toFixed(1)+'" y="'+(H-8)+'" text-anchor="middle">'+esc(String(xl))+'</text>';});
   var lines='',dots='',lens=[];
   series.forEach(function(s,si){var d='',pts=[],i;
    for(i=0;i<nx;i++){var v=(s.values[i]==null?0:s.values[i]),x=X(i),y=Y(v);pts.push([x,y]);d+=(i?' L':'M')+x.toFixed(2)+' '+y.toFixed(2);}
    lens.push(pathLen(pts));
    lines+='<path class="cxw-lt-line" data-si="'+si+'" d="'+d+'" stroke="'+s.color+'"></path>';
    for(i=0;i<nx;i++){var vv=(s.values[i]==null?0:s.values[i]);
     dots+='<circle class="cxw-lt-dot" tabindex="0" role="img" cx="'+X(i).toFixed(2)+'" cy="'+Y(vv).toFixed(2)+'" r="3.4" fill="'+s.color+'" data-name="'+esc(s.name)+'" data-xl="'+esc(String(xs[i]))+'" data-vl="'+esc(fmtNum(vv)+unit)+'" aria-label="'+esc(s.name+' '+xs[i]+' '+fmtNum(vv)+unit)+'"></circle>';}
   });
   var legend=series.length>1?('<div class="cxw-lt-legend">'+series.map(function(s){return '<span class="cxw-lt-lg"><span class="cxw-lt-sw" style="background:'+s.color+'"></span>'+esc(s.name)+'</span>';}).join('')+'</div>'):'';
   var aria='꺾은선 그래프: '+series.map(function(s){return s.name;}).join(' 대 ')+', '+xs[0]+'~'+xs[nx-1];
   if(el.className.indexOf('cxw-lt')<0)el.className=('cxw-lt '+(anim?'cxw-anim ':'')+el.className).replace(/\s+$/,'');
   el.innerHTML=(cap?'<div class="cxw-lt-cap">'+esc(cap)+'</div>':'')+legend
    +'<div class="cxw-lt-plot"><svg class="cxw-lt-svg" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="'+esc(aria)+'">'+grid+xlab+lines+dots+'</svg><div class="cxw-lt-tip" role="status" aria-live="polite" hidden></div></div>'
    +(note?'<div class="cxw-lt-note">'+esc(note)+'</div>':'');
   var plot=el.querySelector('.cxw-lt-plot'), tip=el.querySelector('.cxw-lt-tip'), lineEls=el.querySelectorAll('.cxw-lt-line');
   if(anim){[].forEach.call(lineEls,function(p,si){var L=lens[si]||W;p.style.strokeDasharray=L.toFixed(2)+' '+L.toFixed(2);p.style.strokeDashoffset=L.toFixed(2);});}
   function showTip(dot){if(!tip||!plot)return;tip.innerHTML='<b>'+dot.getAttribute('data-name')+'</b> '+dot.getAttribute('data-xl')+' · '+dot.getAttribute('data-vl');tip.hidden=false;
    try{var pr=plot.getBoundingClientRect(),dr=dot.getBoundingClientRect();tip.style.left=(dr.left-pr.left+dr.width/2)+'px';tip.style.top=(dr.top-pr.top)+'px';}catch(e){}}
   function hideTip(){if(tip)tip.hidden=true;}
   if(plot){
    plot.addEventListener('mouseover',function(e){var t=e.target;if(t&&t.classList&&t.classList.contains('cxw-lt-dot'))showTip(t);});
    plot.addEventListener('mouseout',function(e){var t=e.target;if(t&&t.classList&&t.classList.contains('cxw-lt-dot'))hideTip();});
    plot.addEventListener('focusin',function(e){var t=e.target;if(t&&t.classList&&t.classList.contains('cxw-lt-dot'))showTip(t);});
    plot.addEventListener('focusout',hideTip);
   }
   cxOnce(el,function(imm){
    el.classList.add('cx-in');
    [].forEach.call(lineEls,function(p,si){var L=lens[si]||W;if(imm){p.style.strokeDashoffset='0';}else{tween(860,si*240,function(k){p.style.strokeDashoffset=(L*(1-k)).toFixed(2);},function(){p.style.strokeDashoffset='0';});}});
   });
  };
  /* __SMK_LT1__ */

})();
