import re,os,sys
os.chdir("/tmp/bbfb/imweb_cdn")
DRY = ("--apply" not in sys.argv)
applied=[]; warns=[]

def bal_ok(a,b):
    for tag in ("a","span","p","div","section","button"):
        if (len(re.findall('<'+tag+r'\b',a))-len(re.findall('</'+tag+'>',a))) != \
           (len(re.findall('<'+tag+r'\b',b))-len(re.findall('</'+tag+'>',b))):
            return tag
    return None

def do(fn, edits, rule):
    t=open(fn,encoding="utf-8").read(); orig=t; n=0; detail=[]
    for kind,a,b in edits:
        if kind=="re":
            new,c=re.subn(a,b,t,flags=re.S); 
            if c: t=new; n+=c; detail.append(f"[re x{c}] {b[:30] if b else '(removed)'}")
            else: warns.append(f"{fn}: RE no-match {a[:40]}")
        else:
            c=t.count(a)
            if c: t=t.replace(a,b); n+=c; detail.append(f"[x{c}] {a[:26]} -> {b[:26]}")
            else: warns.append(f"{fn}: STR no-match <{a[:46]}>")
    if t!=orig:
        bt=bal_ok(orig,t)
        if bt: warns.append(f"{fn}: TAG IMBALANCE {bt}")
        # gates
        if '9,900' in t: warns.append(f"{fn}: GATE 9,900 present!")
        if re.search(r'저녁 ?5시',t): warns.append(f"{fn}: GATE 저녁5시!")
        applied.append({"file":fn,"rule":rule,"n":n})
        print(f"\n### {fn} [{rule}] {n} edits"); [print("   ",d) for d in detail]
        if not DRY:
            tmp=fn+".tmp"; open(tmp,"w",encoding="utf-8").write(t); os.replace(tmp,fn)
    else:
        print(f"\n### {fn} [{rule}] NO CHANGE")

# ---- C3 premium ----
do("premium__BODY.html",[
 ("re", r'\n        <span class="tc"><svg viewBox="0 0 24 24"><path d="M7 11V8a5 5 0 0 1 10 0v3"/><rect x="5" y="11" width="14" height="9" rx="2"/></svg>약정 없이 언제든 해지</span>', ""),
 ("re", r'\n        <p class="prsr">약정 없이 · 언제든 한 번에 해지</p>', ""),
 ("str","0원으로 받아보세요.","무료로 받아보세요."),
 ("str","0원으로 먼저 받아보세요.","무료로 먼저 받아보세요."),
 ("str","무료로 충분히 써보고 결정하셔도 돼요. 약정이 없어서, 프리미엄도 언제든 한 번에 해지할 수 있어요.","무료로 충분히 써보고 결정하셔도 돼요."),
 ("str","잠금은 구독하면 풀려요.","잠금은 프리미엄으로 풀려요."),
],"C3")

# ---- C3 sub-5a7f ----
do("sub-5a7f__BODY.html",[
 ("str","언제든 해지할 수 있어요 — 해지해도 다음 결제일 전까지 그대로 보실 수 있어요.","해지하시면 다음 결제일 전까지 그대로 보실 수 있어요."),
],"C3")

# ---- C3 letter-archive ----
do("letter-archive__BODY.html",[
 ("str","머니레터는 늘 0원으로 열려 있어요.","머니레터는 늘 무료로 열려 있어요."),
 ("str","약정 없이 언제든 해지 · 하루 두 번, 아침·저녁","하루 두 번, 아침·저녁"),
],"C3")

# ---- C4 English persuasion eyebrows -> T8 product nouns ----
do("class-7389__BODY.html",[("str",">JOIN THE 3RD COHORT<",">MONEY CLASS<")],"C4")
do("goods-fd41__BODY.html",[("str",">START TODAY<",">MONEY GOODS<")],"C4")
do("kit-842c__BODY.html",[("str",">START TODAY<",">MONEY KIT<")],"C4")

# ---- C6 remove 오픈 예정 soon-cards (F1) ----
for fn in ["class-b779__BODY.html","goods-9972__BODY.html","kit-bcaf__BODY.html"]:
    do(fn,[("re", r'<a href="/home#subscribe" class="pcard soon ringed">.*?</a>', "")],"C6")

# ---- C10 home facts (exception-allowed) ----
do("home__BODY.html",[
 ("str","3년 만에 자산 10배 상승","3년 만에 자산 10배 이상 성장"),
 ("str","월 수입 10배 이상 증가","연봉 이상의 월급"),
],"C10")

print("\n===== WARNINGS ====="); [print("  !!",w) for w in warns]
print(f"\nDRY={DRY}  files={len(applied)}  edits={sum(a['n'] for a in applied)}")
