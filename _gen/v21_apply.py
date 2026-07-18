import os,sys,time,io
ROOT='/tmp/bbfb2/imweb_cdn'
BODY=os.path.join(ROOT,'contents__BODY.html')
FOOT=os.path.join(ROOT,'contents__FOOTER.html')
css=open('/tmp/bbfb2/_gen/v21_body.css',encoding='utf-8').read()
js =open('/tmp/bbfb2/_gen/v21_footer.js',encoding='utf-8').read()

def atomic_write(path,data):
    d=os.path.dirname(path); tmp=os.path.join(d,'.tmp_%d_%s'%(os.getpid(),os.path.basename(path)))
    with io.open(tmp,'w',encoding='utf-8',newline='') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    os.replace(tmp,path)

def guard_marker(text,label):
    # v2.1 재실행 방지
    if 'CX v2.1 · 신규 위젯 3종' in text or 'CX v2.1 · 홈(home) 디자인 DNA' in text:
        print('[SKIP] %s already contains v2.1 block — abort to avoid double-insert'%label); sys.exit(3)

ts=time.strftime('%Y%m%d_%H%M%S')
# ---- BODY ----
b=open(BODY,encoding='utf-8').read()
guard_marker(b,'BODY')
anchor_b='</style>\n<section class="cx-reader" id="cxReader"'
n=b.count(anchor_b)
assert n==1, 'BODY anchor count=%d (expected 1)'%n
b2=b.replace(anchor_b, css.rstrip('\n')+'\n</style>\n<section class="cx-reader" id="cxReader"',1)
assert len(b2)>len(b) and b2!=b
open(BODY+'.bak_v21_'+ts,'w',encoding='utf-8').write(b)
atomic_write(BODY,b2)

# ---- FOOTER ----
f=open(FOOT,encoding='utf-8').read()
guard_marker(f,'FOOTER')
anchor_f=' function fetchBody(slug,routeId,it){'
n=f.count(anchor_f)
assert n==1, 'FOOTER anchor count=%d (expected 1)'%n
f2=f.replace(anchor_f, js.rstrip('\n')+'\n\n'+anchor_f,1)
assert len(f2)>len(f) and f2!=f
open(FOOT+'.bak_v21_'+ts,'w',encoding='utf-8').write(f)
atomic_write(FOOT,f2)

print('[OK] BODY  %d -> %d (+%d)'%(len(b),len(b2),len(b2)-len(b)))
print('[OK] FOOTER %d -> %d (+%d)'%(len(f),len(f2),len(f2)-len(f)))
print('[OK] backups: .bak_v21_%s'%ts)
