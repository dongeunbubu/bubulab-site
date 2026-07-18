# -*- coding: utf-8 -*-
"""fill4young /yfs/main 캡처: step01,02,03,04,05,06 + 전체페이지 ref"""
from playwright.sync_api import sync_playwright
import json
OUT="/tmp/yc_caps/"
YMAP_JS="""(labels)=>{const out={};const els=[...document.querySelectorAll('body *')];
for(const L of labels){const pref=L.endsWith('*');const key=pref?L.slice(0,-1):L;let best=null;
for(const e of els){const t=(e.innerText||'').trim();const ok=pref? t.startsWith(key) && t.length<key.length+25 : t===key;
if(ok){const r=e.getBoundingClientRect();if(r.height>0&&(!best||r.height<best.h)){best={y:Math.round(r.top+window.scrollY),h:r.height}}}}
if(best)out[L]=best.y}
out.__H=Math.round(document.documentElement.scrollHeight);return out}"""
CLICK_JS="""(labels)=>{const res=[];for(const L of labels){const pref=L.endsWith('*');const key=pref?L.slice(0,-1):L;
const els=[...document.querySelectorAll('body *')].filter(e=>{const t=(e.innerText||'').trim();
return (pref? t.startsWith(key)&&t.length<key.length+25 : t===key) && e.getElementsByTagName('*').length<6});
if(!els.length){res.push([L,'NOTFOUND']);continue}
const e=els[0];const c=e.closest('button,[role=button],[class*=accord],[class*=Accord],[class*=toggle],[class*=Toggle],[class*=collaps],[class*=Collaps]')||e.parentElement||e;
c.click();res.push([L,'ok'])}return res}"""
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--disable-blink-features=AutomationControlled","--no-sandbox"])
    ctx=b.new_context(viewport={"width":1440,"height":900},device_scale_factor=1.5,locale="ko-KR",
        timezone_id="Asia/Seoul",ignore_https_errors=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36")
    pg=ctx.new_page()
    pg.goto("https://fill4young.kinfa.or.kr",wait_until="domcontentloaded",timeout=25000)
    pg.wait_for_timeout(4500)
    # step06: 일정 팝업 (로드시 자동 오픈)
    popup_open="schedule-popup-open" in (pg.evaluate("()=>document.body.className") or "")
    if popup_open:
        pg.screenshot(path=OUT+"raw_step06_popup.png")
        print("step06 popup: captured")
    r=pg.evaluate("""()=>{let btn=[...document.querySelectorAll('button')].find(b=>/닫기|close/i.test((b.getAttribute('aria-label')||''))||/닫기/.test(b.innerText||''));
        if(btn){btn.click();return 'btn'}return 'none'}""")
    pg.wait_for_timeout(700)
    if "schedule-popup-open" in (pg.evaluate("()=>document.body.className") or ""):
        pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    print("popup close:",r,"| body class:",pg.evaluate("()=>document.body.className"))
    # step01: 메인 상단
    pg.evaluate("()=>window.scrollTo(0,0)"); pg.wait_for_timeout(600)
    pg.screenshot(path=OUT+"raw_step01_main.png")
    print("step01 main: captured")
    # 접힘 상태 Y맵 (step02 상품 클립용)
    labels=["가입 심사 절차 안내","청년미래적금 요건","적금방식","적금한도","적금기간","적금금리","혜택","해지 시 확인사항","문의 및 도움","가입 대상"]
    ym=pg.evaluate(YMAP_JS,labels); print("YMAP collapsed:",json.dumps(ym,ensure_ascii=False))
    def clip(y0,y1):
        y0=max(0,y0); h=min(y1,ym0["__H"] if False else y1)-y0
        return {"x":0,"y":y0,"width":1440,"height":h}
    if "적금방식" in ym and "혜택" in ym:
        pg.screenshot(path=OUT+"raw_step02_product.png",clip={"x":0,"y":ym["적금방식"]-70,"width":1440,"height":(ym["혜택"]-20)-(ym["적금방식"]-70)},full_page=True)
        print("step02 product: captured")
    # 아코디언 펼침
    acc=["가입 신청","가입요건 심사","심사 결과 안내","계좌 개설",
         "[공통] 나이 요건","[공통] 개인소득*","[공통] 가구 요건","[공통] 금융소득종합과세","[해당자] 중소기업 요건","[해당자] 소상공인 요건",
         "특별중도해지","일반중도해지","해지 후 재가입"]
    res=pg.evaluate(CLICK_JS,acc); print("CLICKS:",json.dumps(res,ensure_ascii=False))
    pg.wait_for_timeout(1200)
    ym2=pg.evaluate(YMAP_JS,labels); print("YMAP expanded:",json.dumps(ym2,ensure_ascii=False))
    def shot(name,y0,y1):
        pg.screenshot(path=OUT+name,clip={"x":0,"y":max(0,y0),"width":1440,"height":y1-max(0,y0)},full_page=True)
        print(name,"captured h=",y1-max(0,y0))
    if "가입 심사 절차 안내" in ym2 and "청년미래적금 요건" in ym2:
        shot("raw_step04_procedure.png",ym2["가입 심사 절차 안내"]-20,ym2["청년미래적금 요건"]-40)
    if "청년미래적금 요건" in ym2 and "적금방식" in ym2:
        shot("raw_step03_eligibility.png",ym2["청년미래적금 요건"]-20,ym2["적금방식"]-70)
    if "해지 시 확인사항" in ym2 and "문의 및 도움" in ym2:
        shot("raw_step05_termination.png",ym2["해지 시 확인사항"]-20,ym2["문의 및 도움"]-40)
    pg.screenshot(path=OUT+"ref_yfs_fullpage_expanded.png",full_page=True)
    print("fullpage ref captured, total H:",ym2.get("__H"))
    b.close()
