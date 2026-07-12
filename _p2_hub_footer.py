# -*- coding: utf-8 -*-
import os
F='/tmp/bbfb/imweb_cdn/contents-hub__FOOTER.html'
s=open(F,encoding='utf-8').read()
orig=len(s.encode())

# 1) popover: growth-stage badge
old1=("""  function badges(node){
   var tk=node.getAttribute('data-tk'), t=node.getAttribute('data-t');
   var s='<span class="jm-lt jm-pt-'+tk+'">'+t+'</span>';
   s+= node.getAttribute('data-prem')==='1'""")
new1=("""  function badges(node){
   var tk=node.getAttribute('data-tk'), t=node.getAttribute('data-t');
   var s='<span class="jm-lt jm-pt-'+tk+'">'+t+'</span>';
   var st=node.getAttribute('data-stage'), sm={seed:'\U0001F331 새싹',bud:'\U0001F338 봉오리',bloom:'\U0001F33A 만개'};
   if(st&&sm[st]) s+='<span class="jm-b jm-b-stage">'+sm[st]+'</span>';
   s+= node.getAttribute('data-prem')==='1'""")
assert s.count(old1)==1, "anchor1"
s=s.replace(old1,new1,1)

# 2) localStorage bloom persistence (visited/complete -> stay bloomed+glow)
old2="\n var draw=scope.querySelector('.jm-draw');"
new2=("""
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

 var draw=scope.querySelector('.jm-draw');""")
assert s.count(old2)==1, "anchor2"
s=s.replace(old2,new2,1)

tmp=F+'.tmp'; open(tmp,'w',encoding='utf-8').write(s); os.replace(tmp,F)
print("FOOTER %d -> %d bytes"%(orig,len(s.encode())))
