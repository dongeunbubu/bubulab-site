import re,os,subprocess,sys,glob
ROOT='/tmp/bbfb2/imweb_cdn'
BODY=os.path.join(ROOT,'contents__BODY.html'); FOOT=os.path.join(ROOT,'contents__FOOTER.html')
def rd(p): return open(p,encoding='utf-8').read()
body=rd(BODY); foot=rd(FOOT)
def bak(p):
    xs=sorted(glob.glob(p+'.bak_v21_*'));
    return rd(xs[-1]) if xs else None
body0=bak(BODY); foot0=bak(FOOT)
res=[]; fails=[]
def check(name,cond,extra=''):
    res.append((bool(cond),name,extra));
    if not cond: fails.append(name)

# 1) node --check on every <script> in FOOTER
scripts=re.findall(r'<script>(.*?)</script>',foot,re.S)
ok_all=True; errs=[]
for i,s in enumerate(scripts):
    tf='/tmp/bbfb2/_gen/_chk_%d.js'%i; open(tf,'w',encoding='utf-8').write(s)
    p=subprocess.run(['node','--check',tf],capture_output=True,text=True)
    if p.returncode!=0: ok_all=False; errs.append('script#%d: %s'%(i,p.stderr.strip().split(chr(10))[0] if p.stderr else '?'))
check('node --check (FOOTER %d scripts)'%len(scripts), ok_all, '; '.join(errs))

# 2) regression markers preserved
existing=["W.slider=function","W.tabs=function","W.quiz=function","W.compare=function","W.checklist=function",
 "W2['compare-pro']=function","W2['decision-tree']=function","W2['step-guide']=function","W2['term-chip']=function",
 "W2['timeline-h']=function","W2['summary-card']=function","W2['related-rail']=function","W2['sim-frame']=function"]
miss=[m for m in existing if m not in foot]
check('기존 위젯 13종 등록 유지', not miss, 'missing: '+','.join(miss))
readers=["CXW.reader=","function wrapChapters(","function buildTOC(","function activeUpd(","function renderReader(","function fetchBody(","CXW.mount=function"]
rmiss=[m for m in readers if m not in foot]
check('리더 회귀 마커 유지', not rmiss, 'missing: '+','.join(rmiss))

# 3) new registrations
newreg=["W2['mini-chart']=function","W2['evidence-card']=function","W2['slider-calc']=function","CXW.rrail="]
nmiss=[m for m in newreg if m not in foot]
check('신규 위젯 3종 + 레일 등록', not nmiss, 'missing: '+','.join(nmiss))

# 4) delta-based tag balance vs backup (insertion internally balanced)
tags=['div','span','section','svg','script','style','button','a','ul','ol','li','text','title','rect','circle','aside','nav','details','summary','label','b','i','em','h2','h3','h4','table','tr','td','th','figure']
def counts(t,tag):
    o=len(re.findall(r'<'+tag+r'(?=[\s>/])',t)); c=len(re.findall(r'</'+tag+r'>',t)); return o,c
def delta_balanced(new,old):
    if old is None: return None
    bad=[]
    for tag in tags:
        no,nc=counts(new,tag); oo,oc=counts(old,tag)
        if (no-oo)!=(nc-oc): bad.append('%s(+o%d,+c%d)'%(tag,no-oo,nc-oc))
    return bad
bb=delta_balanced(body,body0); fb=delta_balanced(foot,foot0)
check('BODY 태그 균형(삽입 델타)', bb==[], 'imbalance: '+','.join(bb or []) if bb else '')
check('FOOTER 태그 균형(삽입 델타)', fb==[], 'imbalance: '+','.join(fb or []) if fb else '')
# absolute structural balance
for label,t in [('BODY',body),('FOOTER',foot)]:
    for tag in ['script','style','section','svg','div']:
        o,c=counts(t,tag); check('%s <%s> 균형(%d/%d)'%(label,tag,o,c), o==c)

# 5) zero HTML comment openers
check("BODY '<!--' == 0", body.count('<!--')==0, str(body.count('<!--')))
check("FOOTER '<!--' == 0", foot.count('<!--')==0, str(foot.count('<!--')))

# 6) cx-/cxw- prefix for NEW content (css selectors + js literal classes)
css=rd('/tmp/bbfb2/_gen/v21_body.css'); js=rd('/tmp/bbfb2/_gen/v21_footer.js')
sel=set(re.findall(r'(?<![\w-])\.([A-Za-z][\w-]*)',css))
badsel=[s for s in sel if not (s.startswith('cx-') or s.startswith('cxw-') or s=='on')]
check('CSS 신규 셀렉터 cx-/cxw- 접두', not badsel, 'non-prefixed: '+','.join(sorted(badsel)))
jsclasses=set()
for m in re.findall(r'class="([^"<]*)"',js):
    for tok in m.split():
        if any(ch in tok for ch in "'+<>{}"): continue
        if tok: jsclasses.add(tok)
badjs=[c for c in jsclasses if not (c.startswith('cx-') or c.startswith('cxw-') or c=='on')]
check('JS 리터럴 클래스 cx-/cxw- 접두', not badjs, 'non-prefixed: '+','.join(sorted(badjs)))

# 7) node smoke (real mount of 3 new widgets)
p=subprocess.run(['node','/tmp/bbfb2/_gen/v21_smoke.js'],capture_output=True,text=True)
check('신규 위젯 데모 스모크(node 실행)', p.returncode==0, p.stdout.strip().split(chr(10))[-1] if p.stdout else p.stderr[:80])

# 8) demo artifact
dm='/tmp/bbfb2/_gen/_v21_widget_demo.html'
demo_ok=os.path.exists(dm) and all(('data-cx-w="%s"'%t) in rd(dm) for t in ['mini-chart','evidence-card','slider-calc'])
check('데모 파일 3위젯 인스턴스', demo_ok)

# 9) schema doc updated
sc='/tmp/bbfb2/imweb_cdn/_CXW_v2_스키마.md'
schema_ok=os.path.exists(sc) and all(t in rd(sc) for t in ['mini-chart','evidence-card','slider-calc','.cx-rrail'])
check('스키마 문서 신규 계약 반영', schema_ok)

print('='*60)
for good,name,extra in res:
    print(('  PASS  ' if good else '  FAIL  ')+name+(('   ['+extra+']') if (extra and not good) else ''))
print('='*60)
print('RESULT:', 'ALL PASS ✅  (%d checks)'%len(res) if not fails else ('FAIL ❌  → '+', '.join(fails)))
sys.exit(1 if fails else 0)
