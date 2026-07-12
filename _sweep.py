#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, os, sys, json, glob, tempfile

ROOT="/tmp/bbfb/imweb_cdn"
DRY = ("--apply" not in sys.argv)
ONLY = None
for a in sys.argv[1:]:
    if a.startswith("--only="):
        ONLY = a.split("=",1)[1].split(",")

WIDGETS = {"letter-8221","letter-ba2f","pay-809e","pay-dunning-fa4c",
           "sub-2645","sub-3a8b","sub-5a7f","sub-8645","sub-vs-fd47","viz-library"}
ALREADY_FW = {"contents-hub","contents","library","moneyletter-landing","story"}
TOPBAR = {"class-7389","class-b779","contents-columns","contents-kits","contents",
          "goods-9972","goods-fd41","home","kit-842c","kit-bcaf",
          "letter-archive","letter-evening","letter-morning","premium"}

BEIGE="#F3ECDF"; INK="#3E2F29"; ROSE="#B33A4C"
B1='<svg viewBox="0 0 24 24" width="20" height="20" fill="none" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><path d="M11.05 3.5 4.2 9.1A2.4 2.4 0 0 0 3.3 11v8.1A1.9 1.9 0 0 0 5.2 21h13.6a1.9 1.9 0 0 0 1.9-1.9V11a2.4 2.4 0 0 0-.9-1.9L12.95 3.5a1.5 1.5 0 0 0-1.9 0Z" fill="#B33A4C"/><path d="M11.45 4.05 5.2 9.2" fill="none" stroke="#FFFFFF" stroke-opacity=".55" stroke-width=".85" stroke-linecap="round"/><path d="M9.9 21v-4.7a2.1 2.1 0 0 1 2.1-2.1 2.1 2.1 0 0 1 2.1 2.1V21Z" fill="#F7E6E2"/><path d="M 16.4 7.243 l -0.189 -0.172 C 15.542 6.464 15.1 6.064 15.1 5.572 15.1 5.172 15.415 4.857 15.815 4.857 c 0.226 0.0 0.443 0.105 0.585 0.272 C 16.542 4.963 16.759 4.857 16.985 4.857 17.385 4.857 17.7 5.172 17.7 5.572 c 0.0 0.491 -0.442 0.892 -1.112 1.5 L 16.4 7.243 z" fill="#C9A84C"/></svg>'
NOTE='부부연구소는 누군가에게 의지하지 않는 안정적이며 효과적인 돈관리/재테크 구조와 환경을 만드는 도움이 될 수 있기를 지향해요. 재테크는 평생 해야하는 것이기 때문에 단 편의 정보가 아닌 평생 할 수 있는 재테크 지식과 습관을 만들어드리고 싶어요. 모든 콘텐츠에는 특정 종목에 대한 추천이나 권유내용을 포함하지 않는다는 점을 말씀드려요. 머니레터를 포함한 부부연구소에서 전해드리는 모든 정보에 대한 판단과 책임은 독자분들에게 있으며, 건강한 판단으로부터 현명한 가계운영에 도움이 될 수 있기를 진심으로 바래요:) · © 부부연구소'

FOOTER_HTML = (
'<footer class="bbft"><div class="bbft-in">'
'<div class="bbft-logo">'+B1+'부부연구소</div>'
'<nav class="bbft-nav"><a href="/moneyletter-landing">머니레터</a><a href="/contents">콘텐츠</a>'
'<a href="/kit-bcaf">키트</a><a href="/goods-9972">굿즈</a><a href="/class-b779">강의</a>'
'<a href="/story">스토리</a><a href="/privacy-v1">개인정보처리방침</a><a href="/terms-v1">이용약관</a></nav>'
'<div class="bbft-info"><span>상호명 <b>부부연구소</b></span><span>대표 <b>김동엽</b></span>'
'<span>사업자등록번호 <b>387-52-00871</b></span><span>통신판매업 <b>2026-별내-1152</b></span>'
'<span>이메일 <b>dongeunbubu@gmail.com</b></span></div>'
'<div class="bbft-note">'+NOTE+'</div>'
'</div></footer>')

BBFT_CSS = (
".bbft{background:#F3ECDF;color:#3E2F29;font-size:13px;padding:40px 0 46px;margin-top:0;"
"border-top:1px solid rgba(62,47,41,.08);position:relative;z-index:2}"
".bbft .bbft-in{max-width:1120px;margin:0 auto;padding:0 clamp(20px,4vw,40px)}"
".bbft .bbft-logo{font-weight:800;color:#3E2F29;font-size:16px;margin-bottom:14px;display:flex;align-items:center;gap:8px}"
".bbft .bbft-logo svg{width:20px;height:20px;display:block;flex:none}"
".bbft .bbft-nav{display:flex;flex-wrap:wrap;gap:10px 22px;margin-bottom:16px}"
".bbft .bbft-nav a{color:#3E2F29;font-weight:700;font-size:13.5px;text-decoration:none;transition:color .15s}"
".bbft .bbft-nav a:hover{color:#B33A4C}"
".bbft .bbft-info{display:flex;flex-wrap:wrap;gap:6px 20px;color:#6b5b52}"
".bbft .bbft-info b{color:#3E2F29;font-weight:700}"
".bbft .bbft-note{margin-top:14px;font-size:12px;color:#8a7b72;line-height:1.62;max-width:920px}")

FOOTER_ELEM_BEIGE = "footer{background:#F3ECDF;color:#3E2F29;border-top:1px solid rgba(62,47,41,.08)}"

SYNC_JS = ('<script>/*bb-hdrsync*/(function(){var r=document.documentElement,'
'tb=document.querySelector(".topbar"),hd=document.getElementById("hdr")||document.getElementById("jmhdr");'
'if(!hd)return;function s(){var th=tb?tb.offsetHeight:0,hh=hd.offsetHeight||0;'
'if(tb){hd.style.top=th+"px";}r.style.setProperty("--bbhdrH",(th+hh)+"px");}'
's();addEventListener("resize",s);addEventListener("load",s);'
'if(document.readyState!=="loading")s();else document.addEventListener("DOMContentLoaded",s);})();</script>')

def fix_hdr_rule(m):
    sel=m.group(1); body=m.group(2)
    body=body.replace('position:sticky','position:fixed')
    if 'left:0' not in body:
        body=re.sub(r'top:0', 'top:0;left:0;right:0', body, count=1)
    if 'z-index' in body:
        body=re.sub(r'z-index:\d+','z-index:9990',body)
    else:
        body+=';z-index:9990'
    body=re.sub(r'(rgba\(253,251,247,)[.\d]+\)', r'\g<1>.94)', body)
    if 'box-shadow:' not in body:
        body=body+';box-shadow:0 2px 14px rgba(62,47,41,.06)'
    return sel+'{'+body+'}'

HDR_RE = re.compile(r'(?<![\w.#\-])(header|#hdr|#jmhdr)\{([^{}]*position:sticky[^{}]*)\}')

def process(slug, s):
    info={"slug":slug,"hdr_fixed":False,"footer":False,"bbfw":False,"topbar":slug in TOPBAR}
    if 'data-bbsweep' in s:
        info["skipped"]="already"; return s, info
    topbar = slug in TOPBAR
    bbfw   = (slug not in ALREADY_FW)
    hid = '#hdr' if 'id="hdr"' in s else ('#jmhdr' if 'id="jmhdr"' in s else '#hdr')
    # 1) header base rule sticky->fixed
    s2, n = HDR_RE.subn(fix_hdr_rule, s)
    s=s2; info["hdr_rules_fixed"]=n; info["hdr_fixed"]=(n>0)
    # 2) navDrawer z-index above header
    s=re.sub(r'(\.navDrawer\{[^{}]*?z-index:)\d+', r'\g<1>10000', s)
    # 3) footer element + special class backgrounds -> beige
    s=re.sub(r'(?<![\w.#\-])footer\{[^{}]*\}', FOOTER_ELEM_BEIGE, s, count=1)
    s=re.sub(r'(\.(?:jm-foot|afoot|cx-foot|kx-foot)\{[^{}]*?)background:[^;}]*',
             r'\g<1>background:#F3ECDF', s)
    # 4) remove old footer, build new
    new_ft = FOOTER_HTML + ('\n</div>' if bbfw else '')
    if re.search(r'<footer\b', s):
        s=re.sub(r'<footer\b[^>]*>.*?</footer>', lambda m: new_ft, s, count=1, flags=re.S)
    else:
        s=s + '\n' + new_ft
    info["footer"]=True
    # 5) bbfw open wrapper
    if bbfw:
        anchor = '<div class="topbar"' if topbar else '<header id="hdr"'
        if anchor not in s:
            anchor = '<header id="hdr"' if '<header id="hdr"' in s else '<header'
        s=s.replace(anchor, '<div class="bbfw">\n'+anchor, 1)
        info["bbfw"]=True
    # 6) spacer after first </header>
    if '</header>' in s:
        s=s.replace('</header>','</header>\n<div class="bbhdr-spacer" aria-hidden="true"></div>',1)
        info["spacer"]=True
    else:
        info["spacer"]=False
    # 7) sweep style
    parts=["html{scroll-padding-top:calc(var(--bbhdrH,64px) + 16px);overflow-x:hidden}",
           ".bbhdr-spacer{height:var(--bbhdrH,64px)}"]
    if topbar:
        parts.append(hid+"{position:fixed;top:44px;left:0;right:0;z-index:9990}")
        parts.append(".topbar{position:fixed;top:0;left:0;right:0;z-index:9991}")
    else:
        parts.append(hid+"{position:fixed;top:0;left:0;right:0;z-index:9990}")
    if bbfw:
        parts.append(".bbfw{width:100vw;margin-left:calc(50% - 50vw);overflow-x:clip}")
    parts.append(BBFT_CSS)
    s=s + '\n<style data-bbsweep="1">' + "".join(parts) + '</style>'
    return s, info

def checks(slug, s):
    c={}
    c["tag_open_footer"]=s.count('<footer')
    c["tag_close_footer"]=s.count('</footer>')
    c["comment_open"]=s.count('<!--'); c["comment_close"]=s.count('-->')
    c["has_tongsin"]='통신판매' in s
    c["has_beige"]=BEIGE in s
    c["has_fixed"]=('position:fixed' in s)
    c["scroll_pad"]=('scroll-padding-top' in s)
    c["spacer"]=('bbhdr-spacer' in s)
    c["bbfw_count"]=s.count('class="bbfw"')
    c["bbfw_clip"]=('overflow-x:clip' in s)
    c["b1"]=('d="M11.05 3.5 4.2 9.1' in s)
    mh=re.search(r'<header id="(?:hdr|jmhdr)">.*?</header>', s, re.S)
    navreg=(mh.group(0) if mh else "")
    c["nav_jaryosil"]=navreg.count('자료실')
    c["nav_contents"]=('>콘텐츠<' in s)
    # tag balance quick (div)
    c["div_open"]=len(re.findall(r'<div\b',s)); c["div_close"]=s.count('</div>')
    return c

def atomic_write(path, data):
    d=os.path.dirname(path)
    fd,tmp=tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd,'w',encoding='utf-8') as f:
        f.write(data)
    os.replace(tmp, path)

def main():
    bodies=sorted(glob.glob(os.path.join(ROOT,"*__BODY.html")))
    result={"fixed_nav":0,"footer_unified":0,
            "fullwidth":{"already":0,"applied":0,"special":[]},
            "slugs_to_inject":[]}
    rows=[]
    targets = ONLY if ONLY else None
    for path in bodies:
        slug=os.path.basename(path).replace("__BODY.html","")
        if targets and slug not in targets: continue
        s=open(path,encoding='utf-8').read()
        if slug in WIDGETS:
            result["fullwidth"]["special"].append(slug)
            rows.append((slug,"WIDGET-skip",{}))
            continue
        ns, info = process(slug, s)
        if info.get("skipped"):
            rows.append((slug,"already-swept",{})); continue
        c=checks(slug, ns)
        cls = "already" if slug in ALREADY_FW else "applied"
        if cls=="already": result["fullwidth"]["already"]+=1
        else: result["fullwidth"]["applied"]+=1
        if info["hdr_fixed"] or slug=="contents-hub": result["fixed_nav"]+=1
        if info["footer"]: result["footer_unified"]+=1
        result["slugs_to_inject"].append(slug)
        rows.append((slug,cls,c))
        if not DRY:
            atomic_write(path, ns)
            # FOOTER.html sync JS append
            fp=path.replace("__BODY.html","__FOOTER.html")
            if os.path.exists(fp):
                fs=open(fp,encoding='utf-8').read()
                if '/*bb-hdrsync*/' not in fs:
                    atomic_write(fp, fs.rstrip()+'\n'+SYNC_JS+'\n')
    # summary
    print("MODE:", "DRY" if DRY else "APPLY")
    print(json.dumps(result, ensure_ascii=False))
    # print check anomalies
    print("\n--- CHECK ANOMALIES ---")
    bad=0
    for slug,cls,c in rows:
        if not c: continue
        probs=[]
        if c["tag_open_footer"]!=1 or c["tag_close_footer"]!=1: probs.append(f"footer={c['tag_open_footer']}/{c['tag_close_footer']}")
        if c["comment_open"]!=c["comment_close"]: probs.append(f"cmt={c['comment_open']}/{c['comment_close']}")
        if not c["has_tongsin"]: probs.append("no-tongsin")
        if not c["has_beige"]: probs.append("no-beige")
        if not c["has_fixed"]: probs.append("no-fixed")
        if not c["scroll_pad"]: probs.append("no-scrollpad")
        if not c["spacer"]: probs.append("no-spacer")
        if not c["b1"]: probs.append("no-B1")
        if c["nav_jaryosil"]: probs.append(f"nav-jaryosil={c['nav_jaryosil']}")
        if not c["nav_contents"]: probs.append("no-nav-contents")
        if cls=="applied" and (c["bbfw_count"]!=1 or not c["bbfw_clip"]): probs.append(f"bbfw={c['bbfw_count']}/{c['bbfw_clip']}")
        if cls=="already" and c["bbfw_count"]!=0: probs.append(f"bbfw-on-fw={c['bbfw_count']}")
        if c["div_open"]!=c["div_close"]: probs.append(f"div={c['div_open']}/{c['div_close']}")
        if probs:
            bad+=1; print(f"  {slug} [{cls}]: {', '.join(probs)}")
    print(f"anomalies: {bad}/{len([r for r in rows if r[2]])}")
    if not DRY:
        json.dump(result, open("/tmp/bbfb/final_sweep_result.json","w",encoding='utf-8'), ensure_ascii=False, indent=2)
        print("wrote /tmp/bbfb/final_sweep_result.json")

main()
