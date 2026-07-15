#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""부부연구소 layout+nav sweep. bash+python, atomic, no git.
Owner-excluded: contents__BODY/FOOTER, contents-kits__BODY/FOOTER."""
import re, os, glob, json, tempfile

CDN = "imweb_cdn"
OWNED = {"contents__BODY.html","contents-kits__BODY.html",
         "contents__FOOTER.html","contents-kits__FOOTER.html"}
LETTER_SHELLS = {"letter-evening__BODY.html","letter-morning__BODY.html","letter-archive__BODY.html"}
LETTER_INJECT = {"letter-evening__BODY.html","letter-morning__BODY.html"}  # runtime #bblLetter host

def atomic_write(path, text):
    d=os.path.dirname(path)
    fd,tmp=tempfile.mkstemp(dir=d, suffix=".tmp")
    try:
        with os.fdopen(fd,"w",encoding="utf-8",newline="") as f:
            f.write(text)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.remove(tmp)

def maxw_var(s):
    m=re.search(r'--maxw:\s*([^;}\s]+)', s); return m.group(1) if m else None
def content_wrap_px(s):
    m=re.search(r'(?<!#hdr )\.wrap\{max-width:\s*([0-9]+)px', s)
    return int(m.group(1)) if m else None
def eff_width(s):
    v=maxw_var(s)
    if v and v.endswith("px"):
        try: return int(v[:-2])
        except: return None
    if v is None: return content_wrap_px(s)
    return None  # non-px var (already a clamp etc.)

# ---- header center + brand-link CSS (all hdr files) ----
HDR_CSS = ("#hdr .nav{align-items:center}"
           "#hdr .logo{line-height:1;text-decoration:none;color:inherit}")

WIDTH_CSS = (
 ".wrap{max-width:clamp(960px,90vw,1240px);"
 "padding-left:clamp(24px,4vw,56px);padding-right:clamp(24px,4vw,56px)}"
 "#hdr .wrap{max-width:1080px;padding-left:clamp(22px,4.5vw,40px);padding-right:clamp(22px,4.5vw,40px)}"
 ".art{max-width:100%}"
 ".art>p,.art .sec>p,.art>h2,.art>h3,.art .sec>h2,.art .sec>h3,"
 ".art>ul,.art>ol,.art .sec>ul,.art .sec>ol,.art .lead{max-width:76ch}"
 ".art .tblwrap,.art table,.art .gaugewrap,.art figure,.art img,.art .grid,.art .chks,.art .datalabel{max-width:100%}"
)

LETTER_CSS = (
 "#bblLetter{--maxw:1240px;--col:clamp(640px,58vw,860px);--rail:332px;--gap:44px}"
 "#bblLetter .reading{max-width:1240px}"
 "#bblLetter .rail{position:sticky;top:calc(var(--bbhdrH,64px) + 24px);align-self:flex-start}"
 "#bblLetter,#bblLetter .reading,#bblLetter .flow{overflow:visible}"
 "#bblLetter .band .bin{padding-left:clamp(24px,4vw,56px);padding-right:clamp(24px,4vw,56px)}"
)

def brand_link(s):
    """Normalize #hdr brand block to <a href='/' aria-label='홈으로' class='logo'>. Returns (s, changed)."""
    changed=False
    # variant A: <div class="logo"> ... 부부연구소</div>  (header-unique)
    def repA(m):
        return '<a class="logo" href="/" aria-label="홈으로">'+m.group(1)+'</a>'
    s2,nA=re.subn(r'<div class="logo">(.*?부부연구소)</div>', repA, s, count=1, flags=re.S)
    if nA: s=s2; changed=True
    # variant B: <a class="logo" href="/home">  ->  href="/" + aria-label
    if '<a class="logo" href="/home">' in s:
        s=s.replace('<a class="logo" href="/home">',
                    '<a class="logo" href="/" aria-label="홈으로">',1)
        changed=True
    return s, changed

def process_body(path):
    fn=os.path.basename(path)
    s=open(path,encoding="utf-8").read()
    orig=s
    has_hdr='<header id="hdr">' in s or 'id="hdr"' in s
    info={"file":fn,"brand":False,"hdr":has_hdr,"widen":False,"letter":False}
    if not has_hdr:
        return None  # chrome-less fragment: skip
    if 'data-bblayout="1"' in s:
        return None  # already processed
    # 1) brand link
    s,bchg=brand_link(s)
    info["brand"]=bchg
    # build override style
    css=HDR_CSS
    eff=eff_width(orig)
    has_art='class="art' in orig
    if eff is not None and eff<1080 and has_art and fn not in LETTER_SHELLS:
        css+=WIDTH_CSS; info["widen"]=True
    if fn in LETTER_INJECT:
        css+=LETTER_CSS; info["letter"]=True
    block='\n<style data-bblayout="1">'+css+'</style>\n'
    if s.endswith("\n"): s=s+block
    else: s=s+"\n"+block
    if s!=orig:
        atomic_write(path,s)
        return info
    return None

def process_footer(path):
    fn=os.path.basename(path)
    s=open(path,encoding="utf-8").read()
    if 'class="dlogo"' not in s: return None
    # convert JS innerHTML div.dlogo -> a.dlogo home link (both escaped & literal variants)
    new,n=re.subn(r'<div class="dlogo">(.*?)</div>',
                  r'<a class="dlogo" href="/" aria-label="홈으로">\1</a>', s, count=1, flags=re.S)
    if n and new!=s:
        atomic_write(path,new)
        return fn
    return None

def main():
    bodies=sorted(glob.glob(os.path.join(CDN,"*__BODY.html")))
    footers=sorted(glob.glob(os.path.join(CDN,"*__FOOTER.html")))
    res={"brand":[], "widen":[], "letter":[], "footer_drawer":[], "slugs":set()}
    for p in bodies:
        if os.path.basename(p) in OWNED: continue
        info=process_body(p)
        if info:
            if info["brand"]: res["brand"].append(info["file"])
            if info["widen"]: res["widen"].append(info["file"])
            if info["letter"]: res["letter"].append(info["file"])
            res["slugs"].add(info["file"].replace("__BODY.html",""))
    for p in footers:
        if os.path.basename(p) in OWNED: continue
        fn=process_footer(p)
        if fn:
            res["footer_drawer"].append(fn)
            res["slugs"].add(fn.replace("__FOOTER.html",""))
    res["slugs"]=sorted(res["slugs"])
    print("brand_link_applied:", len(res["brand"]))
    print("widen_applied:", len(res["widen"]), res["widen"])
    print("letter_overrides:", res["letter"])
    print("footer_drawer_applied:", len(res["footer_drawer"]))
    print("slugs_modified:", len(res["slugs"]))
    json.dump(res, open("_layout_sweep_run.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__=="__main__":
    main()
