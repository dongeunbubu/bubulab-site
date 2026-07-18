(function(){var W2={},rm=false,window={},esc=function(s){return s},fmtNum=function(n){return n},attr=function(){},J=function(){},MCPAL=[],cxOnce=function(){},tween=function(){},commaInt=function(){};
  /* ---- ① mini-chart: bar(가로 비교)·stack(구성 분해)·donut — 외부 라이브러리 없이 SVG + 진입 애니(IO 1회, reduced-motion 즉시 최종) ---- */
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
   var anim=!rm&&('IntersectionObserver'in window);
   var body='';
   if(type==='donut'){
    var C=2*Math.PI*15.9155, off=0, arcs='';
    items.forEach(function(it){var len=Math.max(0,it.value)/total*C;
     arcs+='<circle class="cxw-mc-arc" cx="21" cy="21" r="15.9155" fill="transparent" stroke="'+it.color+'" stroke-width="6" stroke-dasharray="'+(anim?('0 '+C.toFixed(3)):(len.toFixed(3)+' '+(C-len).toFixed(3)))+'" data-len="'+len.toFixed(3)+'" stroke-dashoffset="'+(-off).toFixed(3)+'" transform="rotate(-90 21 21)"><title>'+esc(it.label+' '+fmtNum(it.value)+unit)+'</title></circle>';
     off+=len;});
    var legend=items.map(function(it){var pct=Math.round(Math.max(0,it.value)/total*100);return '<span class="cxw-mc-lg"><span class="cxw-mc-sw" style="background:'+it.color+'"></span>'+esc(it.label)+' · '+pct+'%</span>';}).join('');
    body='<div class="cxw-mc-donut"><svg class="cxw-mc-dsvg" viewBox="0 0 42 42" role="img" aria-label="'+esc(aria)+'"><circle cx="21" cy="21" r="15.9155" fill="transparent" stroke="var(--cx-border)" stroke-width="6"></circle>'+arcs+'<text class="cxw-mc-dc" data-mcto="'+total+'" x="21" y="21" text-anchor="middle" dominant-baseline="central">'+esc((anim?'0':fmtNum(total))+unit)+'</text><text class="cxw-mc-dl" x="21" y="27" text-anchor="middle">'+esc(attr(el,'data-center','합계'))+'</text></svg><div class="cxw-mc-legend">'+legend+'</div></div>';
   } else if(type==='stack'){
    var x=0, segs='';
    items.forEach(function(it){var w=Math.max(0,it.value)/total*100;segs+='<rect x="'+x.toFixed(3)+'" y="0" width="'+(anim?'0':w.toFixed(3))+'" data-w="'+w.toFixed(3)+'" height="26" fill="'+it.color+'"><title>'+esc(it.label+' '+fmtNum(it.value)+unit)+'</title></rect>';x+=w;});
    var legend2=items.map(function(it){var pct=Math.round(Math.max(0,it.value)/total*100);return '<span class="cxw-mc-lg"><span class="cxw-mc-sw" style="background:'+it.color+'"></span>'+esc(it.label)+' · '+pct+'%</span>';}).join('');
    body='<div class="cxw-mc-stack"><svg class="cxw-mc-stackbar" viewBox="0 0 100 26" preserveAspectRatio="none" role="img" aria-label="'+esc(aria)+'">'+segs+'</svg></div><div class="cxw-mc-legend">'+legend2+'</div>';
   } else {
    var rows=items.map(function(it){var w=Math.max(1,it.value/max*100);
     return '<div class="cxw-mc-row"><span class="cxw-mc-lab">'+esc(it.label)+'</span><span class="cxw-mc-tr"><svg class="cxw-mc-svg" viewBox="0 0 100 15" preserveAspectRatio="none" aria-hidden="true"><rect x="0" y="0" width="'+(anim?'0':w.toFixed(2))+'" data-w="'+w.toFixed(2)+'" height="15" fill="'+it.color+'"></rect></svg></span><span class="cxw-mc-val" data-mcto="'+it.value+'">'+esc((anim?'0':fmtNum(it.value))+unit)+'</span></div>';}).join('');
    body='<div class="cxw-mc-rows" role="img" aria-label="'+esc(aria)+'">'+rows+'</div>';
   }
   if(el.className.indexOf('cxw-mc')<0)el.className=('cxw-mc '+el.className).replace(/\s+$/,'');
   el.innerHTML=(cap?'<div class="cxw-mc-cap">'+esc(cap)+'</div>':'')+body+(note?'<div class="cxw-mc-note">'+esc(note)+'</div>':'');
   if(!anim)return;
   cxOnce(el,function(imm){
    if(imm)return;
    if(type==='bar'){
     var rects=el.querySelectorAll('.cxw-mc-svg rect'),vals=el.querySelectorAll('.cxw-mc-val');
     [].forEach.call(rects,function(r,i){var tw=parseFloat(r.getAttribute('data-w'))||0,v=vals[i],tv=v?(parseFloat(v.getAttribute('data-mcto'))||0):0;
      tween(720,i*90,function(k){r.setAttribute('width',(tw*k).toFixed(2));if(v)v.textContent=commaInt(tv*k)+unit;},function(){r.setAttribute('width',tw.toFixed(2));if(v)v.textContent=fmtNum(tv)+unit;});});
    } else if(type==='stack'){
     [].forEach.call(el.querySelectorAll('.cxw-mc-stackbar rect'),function(r,i){var tw=parseFloat(r.getAttribute('data-w'))||0;tween(430,i*150,function(k){r.setAttribute('width',(tw*k).toFixed(3));},function(){r.setAttribute('width',tw.toFixed(3));});});
    } else {
     var Cc=2*Math.PI*15.9155,dc=el.querySelector('.cxw-mc-dc'),tot=dc?(parseFloat(dc.getAttribute('data-mcto'))||0):0,acc=0;
     [].forEach.call(el.querySelectorAll('.cxw-mc-arc'),function(c){var len=parseFloat(c.getAttribute('data-len'))||0,startFrac=acc/Cc;acc+=len;
      tween(Math.max(260,len/Cc*900),startFrac*760,function(k){var cur=len*k;c.setAttribute('stroke-dasharray',cur.toFixed(3)+' '+(Cc-cur).toFixed(3));},function(){c.setAttribute('stroke-dasharray',len.toFixed(3)+' '+(Cc-len).toFixed(3));});});
     if(dc)tween(760,0,function(k){dc.textContent=commaInt(tot*k)+unit;},function(){dc.textContent=fmtNum(tot)+unit;});
    }
   });
  };

})();
