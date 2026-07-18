# -*- coding: utf-8 -*-
import json, asyncio
from playwright.async_api import async_playwright
F='/sessions/gifted-charming-carson/mnt/홈페이지 찐/재테크_구독서비스_설계/콘텐츠_대개편_기획/_파일럿/검수용_청년적금_칼럼.html'
async def main():
  out={}; errs=[]
  async with async_playwright() as p:
    b=await p.chromium.launch()
    pg=await b.new_page(viewport={'width':1500,'height':900})
    pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto('file://'+F, wait_until='load')
    await pg.wait_for_timeout(2200)
    out['toc']=await pg.evaluate("document.querySelectorAll('.cx-toc-a').length")
    out['rvbar']=await pg.evaluate("!!document.querySelector('.rv-bar') && document.querySelector('.rv-bar').textContent.includes('KST')")
    await pg.evaluate("var e=document.querySelector('[data-cx-w\\x3d\"stat-hero\"]'); e&&e.scrollIntoView({block:'center'})")
    await pg.wait_for_timeout(1500)
    out['statHero']=await pg.evaluate("(document.querySelector('.cxw-sh-v')||{}).textContent||null")
    out['ltPaths']=await pg.evaluate("[...document.querySelectorAll('[data-cx-w\\x3d\"line-trend\"]')].reduce((n,e)=>n+e.querySelectorAll('svg path').length,0)")
    out['mcRects']=await pg.evaluate("[...document.querySelectorAll('[data-cx-w\\x3d\"mini-chart\"]')].reduce((n,e)=>n+e.querySelectorAll('svg rect').length,0)")
    out['evCards']=await pg.evaluate("[...document.querySelectorAll('[data-cx-w\\x3d\"evidence-card\"]')].filter(e=>e.children.length>0).length")
    out['rail']=await pg.evaluate("(function(){var r=document.querySelector('.cx-rrail');return r?getComputedStyle(r).display:'none'})()")
    tb=await pg.evaluate("(function(){var t=document.querySelector('[data-cx-w\\x3d\"decision-tree\"]');if(!t)return null;var n=t.textContent.length;var b=t.querySelector('button');if(b)b.click();return n;})()")
    await pg.wait_for_timeout(600)
    ta=await pg.evaluate("(function(){var t=document.querySelector('[data-cx-w\\x3d\"decision-tree\"]');return t?t.textContent.length:null})()")
    out['tree']={'before':tb,'after':ta,'changed':(tb is not None and ta is not None and tb!=ta)}
    out['sim']=await pg.evaluate("(function(){var s=document.querySelector('[data-cx-w\\x3d\"sim-frame\"]');if(!s)return null;return {kids:s.children.length,inputs:s.querySelectorAll('select,input').length,txt:s.textContent.replace(/\\s+/g,' ').slice(0,50)};})()")
    out['slider']=await pg.evaluate("""(async function(){var sc=document.querySelector('[data-cx-w\\x3d"slider-calc"]');if(!sc)return null;var rng=sc.querySelector('input[type=range]');var ov=sc.querySelector('[data-slc-ov]');var b=ov?ov.textContent:'';var st=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;st.call(rng,rng.min);rng.dispatchEvent(new Event('input',{bubbles:true}));await new Promise(r=>setTimeout(r,400));return {before:b,after:ov?ov.textContent:'',changed:b!==(ov?ov.textContent:'')};})()""")
    out['errCount']=len(errs); out['errs']=errs[:4]
    await b.close()
  print(json.dumps(out,ensure_ascii=False))
asyncio.run(main())
