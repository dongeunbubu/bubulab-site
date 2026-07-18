# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled","--no-sandbox"])
    ctx = b.new_context(viewport={"width":1440,"height":900}, device_scale_factor=1.5,
        locale="ko-KR", timezone_id="Asia/Seoul", ignore_https_errors=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36")
    pg = ctx.new_page()
    pg.goto("https://fill4young.kinfa.or.kr", wait_until="domcontentloaded", timeout=25000)
    pg.wait_for_timeout(5000)
    print("TITLE:", pg.title())
    print("URL:", pg.url)
    pg.screenshot(path="/tmp/yc_caps/_probe_viewport.png")
    dlg = pg.evaluate("()=>{const d=document.querySelector('[role=dialog], .modal, [class*=popup], [class*=Popup]'); return d? (d.tagName+' '+String(d.className).slice(0,100)):null}")
    print("DIALOG:", dlg)
    txt = pg.evaluate("()=>document.body.innerText.slice(0,400)")
    print("BODYTEXT:", txt.replace(chr(10),' | ')[:400])
    b.close()
