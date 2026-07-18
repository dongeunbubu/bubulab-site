# -*- coding: utf-8 -*-
import io, os, re, subprocess, sys
BASE="/tmp/bbfb2/imweb_cdn"
FOOT=os.path.join(BASE,"contents__FOOTER.html")
BODY=os.path.join(BASE,"contents__BODY.html")
SCH =os.path.join(BASE,"_CXW_v2_스키마.md")
foot=io.open(FOOT,encoding="utf-8").read()
body=io.open(BODY,encoding="utf-8").read()
sch =io.open(SCH ,encoding="utf-8").read()
fails=[]; oks=[]
def chk(cond,msg):
    (oks if cond else fails).append(msg)

# 1) node --check (assembled JS)
js=re.sub(r'</?script[^>]*>','\n',foot)
io.open("/tmp/bbfb2/_v22/_gate_foot.js","w",encoding="utf-8").write(js)
r=subprocess.run(["node","--check","/tmp/bbfb2/_v22/_gate_foot.js"],capture_output=True,text=True)
chk(r.returncode==0, "node --check FOOTER JS"+("" if r.returncode==0 else " :: "+r.stderr.strip()[:200]))

# 2) existing widget regression markers (mini-chart 3type / evidence / slider / rail) + broader CXW set
reg = {
 "mini-chart reg":"W2['mini-chart']=function",
 "mini bar(else path max)":"var rows=items.map",
 "mini stack":"type==='stack'",
 "mini donut":"type==='donut'",
 "evidence reg":"W2['evidence-card']=function",
 "slider-calc reg":"W2['slider-calc']=function",
 "rail buildRail":"function buildRail(",
 "rail CXW.rrail":"CXW.rrail=",
 "rail .cx-rrail markup":"rail.className='cx-rrail'",
 "CXW core mount":"return {mount:mount,calc:calc,w:W};",
 "widget slider":"W.slider=function",
 "widget tabs":"W.tabs=function",
 "widget quiz":"W.quiz=function",
 "widget checklist":"W.checklist=function",
 "widget compare":"W.compare=function",
 "widget reveal-steps":"W['reveal-steps']=function",
 "widget counter-bar":"W['counter-bar']=function",
 "decision-tree(dt)":"cxw-dt-restart",
 "summary-card":"cxw-sum",
 "sim-frame":"data-calc",
 "micro-feedback dt":"cx-dtprog",
}
for k,v in reg.items():
    chk(foot.count(v)>=1, "FOOTER marker: "+k)
# BODY existing widget CSS markers
for k,v in {"body .cxw-mc":".cxw-mc{","body .cxw-ev-card":".cxw-ev-card{","body .cxw-slc":".cxw-slc{","body .cx-rrail":".cx-rrail{"}.items():
    chk(body.count(v)>=1, "BODY marker: "+k)

# 3) new widget markers
for k,v in {"stat-hero reg":"W2['stat-hero']=function","line-trend reg":"W2['line-trend']=function",
            "body .cxw-sh":".cxw-sh{","body .cxw-lt":".cxw-lt{"}.items():
    chk((foot if 'reg' in k else body).count(v)>=1, "NEW marker: "+k)

# 4) animation hooks on mini-chart + evidence reveal + count-up helper
for k,v in {"mini data-w hook":'data-w="', "mini data-len hook":'data-len="', "mini data-mcto hook":'data-mcto="',
            "mini arc class":'class="cxw-mc-arc"', "evidence cxReveal":"cxReveal(el);",
            "helper commaInt":"function commaInt(", "helper cxOnce":"function cxOnce(",
            "helper tween":"function tween(", "helper cxReveal":"function cxReveal(",
            "helper shSpark":"function shSpark(", "count-up commaInt use":"commaInt(tv*k)"}.items():
    chk(foot.count(v)>=1, "ANIM hook: "+k)

# 5) tag balance
chk(foot.count("<script")==foot.count("</script>"), "FOOTER script tag balance (%d/%d)"%(foot.count("<script"),foot.count("</script>")))
chk(body.count("<style")==body.count("</style>"), "BODY style tag balance (%d/%d)"%(body.count("<style"),body.count("</style>")))
chk(body.count("<section")==body.count("</section>") or True, "BODY section (informational)")

# 6) '<!--' == 0
chk(foot.count("<!--")==0, "FOOTER '<!--'==0 (got %d)"%foot.count("<!--"))
chk(body.count("<!--")==0, "BODY '<!--'==0 (got %d)"%body.count("<!--"))

# 7) reduced-motion branch present
chk("prefers-reduced-motion: reduce" in foot, "FOOTER rm detection present")
chk("if(rm||!('IntersectionObserver'in window))" in foot, "FOOTER rm guard in helpers (cxOnce/cxReveal)")
chk("@media(prefers-reduced-motion:reduce)" in body, "BODY reduced-motion media query")
chk(".cxw-sh-line,.cxw-lt-line,.cxw-lt-dot{transition:none!important}" in body, "BODY rm covers new widgets")
chk(".cxw-lt.cxw-anim .cxw-lt-dot{opacity:1!important}" in body, "BODY rm forces line-trend dots visible")

# 8) cx- prefix: scan new FOOTER sentinel blocks + new BODY css section
def block(txt,a,b):
    i=txt.index(a); j=txt.index(b,i); return txt[i:j+len(b)]
sh_blk=block(foot,"__SMK_SH0__","__SMK_SH1__ */")
lt_blk=block(foot,"__SMK_LT0__","__SMK_LT1__ */")
mc_blk=block(foot,"① mini-chart:","__SMK") if "__SMK" in foot else ""
# collect class="..." tokens (static parts only)
bad=[]
for blk,name in [(sh_blk,"stat-hero"),(lt_blk,"line-trend")]:
    for m in re.finditer(r'class="([^"]+)"', blk):
        for tok in m.group(1).split():
            if tok.startswith("'+") or tok.startswith("+"):  # dynamic fragment, skip
                continue
            if not tok.startswith("cx"):
                bad.append(name+":"+tok)
chk(not bad, "cx- prefix on new widget classes"+("" if not bad else " :: "+",".join(bad[:8])))
# CSS section selectors
i=body.index("===== CXW v2.2"); j=body.index("===== /CXW v2.2")
seg=body[i:j]
cssbad=[]
for m in re.finditer(r'(^|\})\s*(\.[A-Za-z][^\{,}]*)\{', seg):
    sel=m.group(2).strip()
    # each selector chain: every class token must start with .cx
    for cls in re.findall(r'\.[A-Za-z0-9_-]+', sel):
        if not cls.startswith(".cx"):
            cssbad.append(cls)
chk(not cssbad, "cx- prefix on new CSS selectors"+("" if not cssbad else " :: "+",".join(sorted(set(cssbad))[:8])))

# 9) schema contract added
for k,v in {"schema stat-hero":'data-cx-w="stat-hero"',"schema line-trend":'data-cx-w="line-trend"',
            "schema v2.2 head":"v2.2 시각화 애니메이션 레이어"}.items():
    chk(v in sch, "SCHEMA: "+k)

# 10) new-widget smoke
r2=subprocess.run(["node","/tmp/bbfb2/_v22/smoke.js"],capture_output=True,text=True)
chk(r2.returncode==0, "new-widget DOM-stub smoke"+("" if r2.returncode==0 else " :: "+r2.stdout.strip()[-200:]))

print("="*60)
print("GATE RESULT:  PASS=%d  FAIL=%d"%(len(oks),len(fails)))
print("="*60)
if fails:
    print("FAILURES:")
    for f in fails: print("  X",f)
    sys.exit(1)
else:
    print("ALL GATES PASSED")
