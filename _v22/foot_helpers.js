  /* __SMK_H0__ v2.2 시각화 애니메이션 공용 헬퍼 (cx- 접두, prefers-reduced-motion 존중) */
  var LTPAL=['#B33A4C','#5E8C7F','#C9A84C','#9C6BA8'];
  function commaInt(n){return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g,',');}
  function cxOnce(el,cb){
   if(rm||!('IntersectionObserver'in window)){cb(true);return;}
   var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){io.unobserve(el);cb(false);}});},{threshold:.32,rootMargin:'0px 0px -7% 0px'});
   io.observe(el);
  }
  function tween(dur,delay,onframe,onend){
   if(rm||!('requestAnimationFrame'in window)){onframe(1);if(onend)onend();return;}
   var t0=null;dur=Math.max(1,dur);delay=delay||0;
   function step(ts){if(t0===null)t0=ts;var e=ts-t0-delay;if(e<0){requestAnimationFrame(step);return;}var p=e/dur;if(p>1)p=1;onframe(easeOut(p));if(p<1)requestAnimationFrame(step);else if(onend)onend();}
   requestAnimationFrame(step);
  }
  function cxReveal(el){
   if(rm||!('IntersectionObserver'in window)){el.classList.add('cx-in');return;}
   el.classList.add('cxw-anim');
   var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('cx-in');io.unobserve(en.target);}});},{threshold:.15,rootMargin:'0px 0px -6% 0px'});
   io.observe(el);
  }
  function shSpark(a){
   var W=240,H=48,px=3,py=7,n=a.length,i;
   var mn=Math.min.apply(null,a),mx=Math.max.apply(null,a);if(mx===mn)mx=mn+1;
   function X(i){return n<2?W/2:px+i*(W-2*px)/(n-1);}
   function Y(v){return py+(1-(v-mn)/(mx-mn))*(H-2*py);}
   var d='',pts=[];
   for(i=0;i<n;i++){var x=X(i),y=Y(a[i]);pts.push([x,y]);d+=(i?' L':'M')+x.toFixed(2)+' '+y.toFixed(2);}
   var area=d+' L'+X(n-1).toFixed(2)+' '+(H-py).toFixed(2)+' L'+X(0).toFixed(2)+' '+(H-py).toFixed(2)+' Z';
   var len=0;for(i=1;i<n;i++){var dx=pts[i][0]-pts[i-1][0],dy=pts[i][1]-pts[i-1][1];len+=Math.sqrt(dx*dx+dy*dy);}
   return {line:d,area:area,len:len||W,W:W,H:H};
  }
  function pathLen(pts){var l=0;for(var i=1;i<pts.length;i++){var dx=pts[i][0]-pts[i-1][0],dy=pts[i][1]-pts[i-1][1];l+=Math.sqrt(dx*dx+dy*dy);}return l;}
  /* __SMK_H1__ */
