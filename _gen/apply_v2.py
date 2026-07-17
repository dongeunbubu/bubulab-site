#!/usr/bin/env python3
import os, sys, shutil, io, time
CDN='/tmp/bbfb2/imweb_cdn'
FOOT=os.path.join(CDN,'contents__FOOTER.html')
BODY=os.path.join(CDN,'contents__BODY.html')
INJ_JS=open('/tmp/bbfb2/_gen/_v2_footer_inject.js',encoding='utf-8').read()
INJ_CSS=open('/tmp/bbfb2/_gen/_v2_body_inject.css',encoding='utf-8').read()

def atomic_write(path, text):
    tmp=path+'.tmp_%d'%os.getpid()
    with io.open(tmp,'w',encoding='utf-8',newline='') as f:
        f.write(text); f.flush(); os.fsync(f.fileno())
    os.replace(tmp,path)

def repl_once(s, old, new, tag):
    n=s.count(old)
    assert n==1, "ANCHOR '%s' count=%d (expected 1)"%(tag,n)
    return s.replace(old,new,1)

ts=time.strftime('%Y%m%d_%H%M%S')
# --- backups (file copy; no git) ---
for p in (FOOT,BODY):
    shutil.copy2(p, p+'.bak_v2_'+ts)

# ================= FOOTER =================
f=open(FOOT,encoding='utf-8').read()
orig_f=f
# 1) big JS block after CXW IIFE close
f=repl_once(f,
  "  return {mount:mount,calc:calc,w:W};\n })();",
  "  return {mount:mount,calc:calc,w:W};\n })();\n"+INJ_JS,
  "CXW-close")
# 2) reader v2 init hook in fetchBody
f=repl_once(f,
  "    CXW.mount(el);\n    reveal(el,'.cx-sc');",
  "    CXW.mount(el);\n    try{CXW.reader&&CXW.reader.init(el,slug,it);}catch(_e){}\n    reveal(el,'.cx-sc');",
  "mount-call")
# 3) parseHash deep-link (@chN) tolerant
f=repl_once(f,
  "function parseHash(){var h=(location.hash||'').replace(/^#/,'').trim();return h?{mode:'reader',slug:h}:{mode:'explore'};}",
  "function parseHash(){var h=(location.hash||'').replace(/^#/,'').trim();var at=h.indexOf('@');var s=at>=0?h.slice(0,at):h;return h?{mode:'reader',slug:s,anchor:(at>=0?h.slice(at+1):'')}:{mode:'explore'};}",
  "parseHash")
# 4) index v2: card() free badge honors it.free
f=repl_once(f,
  ":it.premium===false?'<span class=\"cx-b cx-b-free\">🆓 무료</span>':''",
  ":(it.premium===false||it.free===true)?'<span class=\"cx-b cx-b-free\">🆓 무료</span>':''",
  "card-free")
# 5) index v2: mwRow() free honors it.free
f=repl_once(f,
  "pm===false?'<span class=\"cx-mw-free\">🆓</span>':''",
  "(pm===false||it.free===true)?'<span class=\"cx-mw-free\">🆓</span>':''",
  "mwRow-free")
# 6) index v2: readTime derives from pages when read absent
f=repl_once(f,
  "function readTime(it){if(it&&it.read)return it.read;return 3;}",
  "function readTime(it){if(it&&it.read)return it.read;if(it&&it.pages)return Math.max(3,Math.round(it.pages*1.1));return 3;}",
  "readTime")
assert f!=orig_f
atomic_write(FOOT,f)

# ================= BODY =================
b=open(BODY,encoding='utf-8').read()
b=repl_once(b,
  '<section class="cx-reader" id="cxReader" hidden aria-label="칼럼 리더"></section>',
  INJ_CSS.rstrip('\n')+'\n<section class="cx-reader" id="cxReader" hidden aria-label="칼럼 리더"></section>',
  "cxReader-sec")
atomic_write(BODY,b)

print("APPLIED OK")
print("FOOTER lines:", f.count(chr(10))+1, " BODY lines:", b.count(chr(10))+1)
print("backup ts:", ts)
