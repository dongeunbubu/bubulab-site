# -*- coding: utf-8 -*-
import io, os, sys, time

BASE = "/tmp/bbfb2/imweb_cdn"
V22  = "/tmp/bbfb2/_v22"
FOOT = os.path.join(BASE, "contents__FOOTER.html")
BODY = os.path.join(BASE, "contents__BODY.html")

def rd(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()

def rdsnip(p):
    # snippet files were written by heredoc; strip a single trailing newline only
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        t = f.read()
    if t.endswith("\n"):
        t = t[:-1]
    return t

def atomic_write(p, text):
    stamp = time.strftime("%Y%m%d_%H%M%S")
    bak = p + ".bak_v22_" + stamp
    # backup current
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        cur = f.read()
    with io.open(bak, "w", encoding="utf-8", newline="") as f:
        f.write(cur)
    tmp = p + ".tmp_v22"
    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, p)
    return bak

def must_replace(text, old, new, label):
    n = text.count(old)
    if n != 1:
        print("FATAL: anchor '%s' found %d times (expected 1)" % (label, n))
        sys.exit(2)
    return text.replace(old, new, 1)

# ---------------- FOOTER ----------------
foot = rd(FOOT)

helpers = rdsnip(os.path.join(V22, "foot_helpers.js"))
mc      = rdsnip(os.path.join(V22, "foot_minichart.js"))
ev      = rdsnip(os.path.join(V22, "foot_evidence.js"))
nw      = rdsnip(os.path.join(V22, "foot_newwidgets.js"))

A_MCPAL = "  var MCPAL=['#B33A4C','#5E8C7F','#C9A84C','#9C6BA8','#D67A89','#7C243B','#7FB08A','#E08696'];"
A_MC    = "  /* ---- ① mini-chart: bar(가로 비교)·stack(구성 분해)·donut — 외부 라이브러리 없이 SVG ---- */"
A_EV    = "  /* ---- ② evidence-card: 뉴스·발표 헤드라인(신문 스크랩 결, 홈 팔레트) ---- */"
A_SLC   = "  /* ---- ③ slider-calc: 슬라이더 즉시 계산 — CXW.calc 레지스트리 재사용 ---- */"
A_RAIL  = "  /* ---- 우측 스티키 레일(.cx-rrail) — 기존 목차 상태 재사용, ≥1400px는 CSS가 표시 게이트 ---- */"

# sanity: anchors present
for lbl, a in [("MCPAL",A_MCPAL),("MC",A_MC),("EV",A_EV),("SLC",A_SLC),("RAIL",A_RAIL)]:
    if foot.count(a) != 1:
        print("FATAL: FOOTER anchor %s count=%d" % (lbl, foot.count(a))); sys.exit(2)

# 1) insert helpers after MCPAL line
foot = must_replace(foot, A_MCPAL, A_MCPAL + "\n" + helpers, "MCPAL")

# 2) replace mini-chart region [A_MC, A_EV)
i0 = foot.index(A_MC); i1 = foot.index(A_EV)
foot = foot[:i0] + mc + "\n\n" + foot[i1:]

# 3) replace evidence region [A_EV, A_SLC)
i0 = foot.index(A_EV); i1 = foot.index(A_SLC)
foot = foot[:i0] + ev + "\n\n" + foot[i1:]

# 4) insert new widgets before rail comment
foot = must_replace(foot, A_RAIL, nw + "\n\n" + A_RAIL, "RAIL")

# ---------------- BODY ----------------
body = rd(BODY)
css  = rdsnip(os.path.join(V22, "body_css.css"))

A_MICRO = "/* =================== 마이크로 피드백(피드백 2) — transform만 =================== */"
if body.count(A_MICRO) != 1:
    print("FATAL: BODY micro-feedback anchor count=%d" % body.count(A_MICRO)); sys.exit(2)
body = body.replace(A_MICRO, css + "\n\n" + A_MICRO, 1)

# augment reduced-motion block
RM_OLD = (" .cxw-ev-card,.cxw-mc,.cx-viz,.cx-rrail-cta,.cx-rrail-term,.cx-ch,.cxw-slc-ov{transition:none!important}\n"
          " .cxw-sum-box.cx-pop,.cxw-slc-pop,.cx-dtprog i,.cx-rrail-pin.on,.cx-term-flash{animation:none!important}")
RM_NEW = (" .cxw-ev-card,.cxw-mc,.cx-viz,.cx-rrail-cta,.cx-rrail-term,.cx-ch,.cxw-slc-ov,.cxw-sh-line,.cxw-lt-line,.cxw-lt-dot{transition:none!important}\n"
          " .cxw-sum-box.cx-pop,.cxw-slc-pop,.cx-dtprog i,.cx-rrail-pin.on,.cx-term-flash{animation:none!important}\n"
          " .cxw-ev.cxw-anim{opacity:1!important;transform:none!important}\n"
          " .cxw-lt.cxw-anim .cxw-lt-dot{opacity:1!important}")
if body.count(RM_OLD) != 1:
    print("FATAL: BODY reduced-motion block count=%d" % body.count(RM_OLD)); sys.exit(2)
body = body.replace(RM_OLD, RM_NEW, 1)

# ---------------- SCHEMA ----------------
sch = os.path.join(BASE, "_CXW_v2_스키마.md")
schema = rd(sch)
add = rdsnip(os.path.join(V22, "schema_add.md"))
if "data-cx-w=\"stat-hero\"" not in schema and "stat-hero" not in schema:
    schema = schema.rstrip("\n") + "\n" + add + "\n"
else:
    print("NOTE: schema already mentions stat-hero; appending anyway guarded")
    schema = schema.rstrip("\n") + "\n" + add + "\n"

# ---------------- write all atomically ----------------
b1 = atomic_write(FOOT, foot)
b2 = atomic_write(BODY, body)
b3 = atomic_write(sch, schema)
print("OK FOOTER bak:", os.path.basename(b1))
print("OK BODY   bak:", os.path.basename(b2))
print("OK SCHEMA bak:", os.path.basename(b3))
print("FOOTER len:", len(foot), "BODY len:", len(body), "SCHEMA len:", len(schema))
