import re
FOOT='/tmp/bbfb2/imweb_cdn/contents__FOOTER.html'
CSS=open('/tmp/bbfb2/_gen/v21_body.css',encoding='utf-8').read()
src=open(FOOT,encoding='utf-8').read()

def extract_fn(name):
    key="W2['%s']=function(el){"%name
    i=src.index(key); j=i+len(key); depth=1
    while depth>0:
        c=src[j]
        if c=='{':depth+=1
        elif c=='}':depth-=1
        j+=1
    # include trailing ';'
    if src[j]==';': j+=1
    return src[i:j]

fns='\n'.join(extract_fn(n) for n in ['mini-chart','evidence-card','slider-calc'])

# minimal tokens (home palette subset) + shim
tokens=""":root{--cx-bg:#FDFBF7;--cx-bg2:#FBF3EE;--cx-card:#fff;--cx-ink:#3E2F29;--cx-ink2:#5C4B43;--cx-mut:#8A7B72;--cx-border:#EAD7D3;--cx-rose:#B33A4C;--cx-rose2:#B85060;--cx-deep:#7C243B;--cx-pink:#D67A89;--cx-pinkSoft:#F8E8EA;--cx-pinkSoft2:#FCEEF1;--cx-sage:#5E8C7F;--cx-gold:#C9A84C;--cx-lav:#9C6BA8;--cx-r:22px;--cx-r-sm:14px;--cx-sh:0 1px 2px rgba(62,47,41,.04),0 6px 16px rgba(179,58,76,.06),0 18px 40px rgba(179,58,76,.07);--cx-shi:0 2px 6px rgba(62,47,41,.06),0 14px 30px rgba(179,58,76,.12);--cx-ease:cubic-bezier(.16,1,.3,1)}
body{background:var(--cx-bg);font-family:Pretendard,-apple-system,system-ui,sans-serif;color:var(--cx-ink);max-width:720px;margin:0 auto;padding:30px 22px;line-height:1.7}
h1{font-size:22px}h2{font-size:16px;margin:30px 0 6px;color:var(--cx-deep)}"""

demo_markup="""
<h1>CX v2.1 신규 위젯 데모(스모크)</h1>
<h2>① mini-chart · bar</h2>
<div data-cx-w="mini-chart" data-type="bar" data-caption="가구 월 지출 비교(만원)" data-unit="만원"
  data-items='[{"label":"고정비","value":120},{"label":"변동비","value":78},{"label":"저축","value":52}]'></div>
<h2>① mini-chart · stack</h2>
<div data-cx-w="mini-chart" data-type="stack" data-caption="수입 구성" data-unit="만원"
  data-items='[{"label":"근로","value":300},{"label":"부수입","value":80},{"label":"배당","value":20}]'></div>
<h2>① mini-chart · donut</h2>
<div data-cx-w="mini-chart" data-type="donut" data-center="자산" data-caption="자산 배분" data-unit="%"
  data-items='[{"label":"예금","value":40},{"label":"주식","value":35},{"label":"연금","value":25}]'></div>
<h2>② evidence-card</h2>
<div data-cx-w="evidence-card" data-kind="보도" data-title="가계 저축률 3년 만에 반등" data-source="한국은행" data-date="2026.06" data-note="실질소득 개선이 배경으로 분석됩니다." data-href="https://example.com"></div>
<h2>③ slider-calc(계산 레지스트리 재사용)</h2>
<div data-cx-w="slider-calc" data-calc="futureValue" data-args='[0,"$",5,10]' data-label="매달 저축" data-min="0" data-max="200" data-step="5" data-def="30" data-unit="만원" data-out-label="10년 뒤 예상 잔고(연 5%)" data-format="won" data-out-unit="원" data-caption="슬라이더를 움직이면 즉시 갱신"></div>
"""

shim="""
var d=document, rm=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;
function esc(s){return String(s==null?'':s).replace(/[&<>\\"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','\\"':'&quot;'}[c];});}
function fmtWon(n){return String(Math.round(n)).replace(/\\B(?=(\\d{3})+(?!\\d))/g,',');}
var CXW={w:{},calc:{futureValue:function(p0,m,r,y){r=r/100/12;var n=Math.round(y*12);return p0*Math.pow(1+r,n)+(r>0?m*((Math.pow(1+r,n)-1)/r):m*n);}},enhanceExports:function(){}};
var W2=CXW.w;
__FNS__
[].slice.call(d.querySelectorAll('[data-cx-w]')).forEach(function(el){var fn=W2[el.getAttribute('data-cx-w')];if(fn)try{fn(el);}catch(e){console.error(e);}});
"""
shim=shim.replace('__FNS__',fns)

html='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CX v2.1 위젯 데모</title><style>'+tokens+'\n'+CSS+'</style></head><body>'+demo_markup+'<script>'+shim+'</'+'script></body></html>'
open('/tmp/bbfb2/_gen/_v21_widget_demo.html','w',encoding='utf-8').write(html)
# count instances
n=html.count('data-cx-w="mini-chart"')+html.count('data-cx-w="evidence-card"')+html.count('data-cx-w="slider-calc"')
print('[OK] demo written, new-widget instances=%d, bytes=%d'%(n,len(html.encode('utf-8'))))
