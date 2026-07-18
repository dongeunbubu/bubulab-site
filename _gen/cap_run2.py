# -*- coding: utf-8 -*-
"""/yla/main 청년도약계좌 안내 캡처: step07"""
from playwright.sync_api import sync_playwright
OUT="/tmp/yc_caps/"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--disable-blink-features=AutomationControlled","--no-sandbox"])
    ctx=b.new_context(viewport={"width":1440,"height":900},device_scale_factor=1.5,locale="ko-KR",
        timezone_id="Asia/Seoul",ignore_https_errors=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36")
    pg=ctx.new_page()
    pg.goto("https://fill4young.kinfa.or.kr/yla/main",wait_until="domcontentloaded",timeout=25000)
    pg.wait_for_timeout(4500)
    cls=pg.evaluate("()=>document.body.className"); print("body:",cls)
    if "popup-open" in (cls or ""):
        pg.evaluate("""()=>{let btn=[...document.querySelectorAll('button')].find(b=>/닫기|close/i.test((b.getAttribute('aria-label')||''))||/닫기/.test(b.innerText||''));if(btn)btn.click()}""")
        pg.wait_for_timeout(700)
        if "popup-open" in (pg.evaluate("()=>document.body.className") or ""):
            pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    print("body after:",pg.evaluate("()=>document.body.className"))
    pg.evaluate("()=>window.scrollTo(0,0)"); pg.wait_for_timeout(600)
    pg.screenshot(path=OUT+"raw_step07_yla.png")
    pg.screenshot(path=OUT+"ref_yla_fullpage.png",full_page=True)
    print("TITLE:",pg.title())
    txt=pg.evaluate("()=>document.body.innerText.slice(0,700)")
    print("TEXT:",txt.replace(chr(10),' | ')[:700])
    b.close()
