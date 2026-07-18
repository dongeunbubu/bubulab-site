# -*- coding: utf-8 -*-
"""KB국민은행 청년미래적금 상품 페이지 캡처: step08"""
from playwright.sync_api import sync_playwright
OUT="/tmp/yc_caps/"
CANDS=[
 ("prod","https://obank.kbstar.com/quics?page=C016613&cc=b061496%3Ab061645&isNew=Y&prcode=DP01001656"),
 ("news","https://obank.kbstar.com/quics?page=C020722&boardId=669&compId=b058336&articleId=145082&bbsMode=view&viewPage=1&articleClass=2&searchCondition=title&searchStr="),
]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--disable-blink-features=AutomationControlled","--no-sandbox"])
    ctx=b.new_context(viewport={"width":1440,"height":900},device_scale_factor=1.5,locale="ko-KR",
        timezone_id="Asia/Seoul",ignore_https_errors=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36")
    for tag,url in CANDS:
        pg=ctx.new_page()
        try:
            pg.goto(url,wait_until="domcontentloaded",timeout=30000)
            pg.wait_for_timeout(4000)
            t=pg.title(); txt=pg.evaluate("()=>document.body.innerText.slice(0,900)")
            hit="청년미래적금" in txt or "청년미래적금" in t
            btn=pg.evaluate("""()=>{const els=[...document.querySelectorAll('a,button,input[type=button],input[type=submit],img')];
                const b=els.find(e=>/가입/.test((e.innerText||e.value||e.alt||'').trim())&&(e.innerText||e.value||e.alt||'').trim().length<12);
                if(!b)return null;const r=b.getBoundingClientRect();return {t:(b.innerText||b.value||b.alt||'').trim(),y:Math.round(r.top+scrollY),vis:r.width>0}}""")
            print(tag,"| TITLE:",t[:60],"| hit:",hit,"| btn:",btn)
            print(tag,"| TEXT:",txt.replace(chr(10),' | ')[:500])
            if hit:
                pg.evaluate("()=>window.scrollTo(0,0)");pg.wait_for_timeout(400)
                pg.screenshot(path=OUT+f"raw_step08_bank_{tag}.png")
                pg.screenshot(path=OUT+f"ref_bank_{tag}_fullpage.png",full_page=True)
                print(tag,"captured")
        except Exception as ex:
            print(tag,"ERROR",str(ex)[:150])
        pg.close()
    b.close()
