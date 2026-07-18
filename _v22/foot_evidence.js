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
