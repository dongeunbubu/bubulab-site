import re,os,sys,json
os.chdir("/tmp/bbfb/imweb_cdn")
DRY = ("--apply" not in sys.argv)

C1=["class-b779","col-5392","col-561d","col-6a03","col-a331","col-cae7","col-e2bc","eco-5396","eco-630d","eco-etf-364f","eco-perpbrroe-18bd","goods-9972","kit-bcaf","report-3efe","report-87f1","report-ai-9970","report-d576","report-de46","report-ffe1","tool-1d83","tool-2f6a","tool-4a49","tool-4a72","tool-4d2e","tool-853a","tool-93f4","tool-a34d","tool-b7ab","tool-cbeb","tool-dfe4","tool-ea90","tool-isa-5c34","tool-pro-240b","tool-pro-39d5","tool-pro-438b","tool-pro-6aa3","tool-pro-8138","tool-pro-cc61","tool-pro-ec50","tool-pro-fdd1","tool-re-57f2","tool-re-ac3c","tool-re-f1e8","tool-vs-3ef9","tool-vs-489f"]
COMMERCE={"class-b779","goods-9972","kit-bcaf"}

PREM="프리미엄으로 모두 열기 →"
# normalized inner -> (new_inner, new_href or None)
PREMIUM_CTAS={
 "구독하고 시작하기 →","구독하고 칼럼 받기 →","구독하고 리포트 받기 →","구독하고 시리즈 받기 →",
 "구독하고 처방 받기 →","구독하고 먼저 받기 →","구독하고 함께 그리기 →","구독하고 추적 시작 →",
 "구독하고 추적 시작하기 →","구독하고 열어보기 →","구독하고 노후 추적 열기","구독하고 함께 추적하기 →",
 "구독하고 Pro 열기 →","구독하고 카 머니 보드 받기 →","부부연구소 구독하고 시작하기",
 "구독으로 육아 Pro 열기 →","구독으로 협상 Pro 열기 →","구독으로 공동 추적 열기 →","부부연구소 구독하기 →",
}
FREE_MAP={"머니레터 구독하기 →":"오늘의 머니레터 열어보기 →","머니레터 구독하고 먼저 받기 →":"오늘의 머니레터 받아보기 →"}
KEEP={"구독하기","머니레터 구독"}

def norm(s): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',s)).strip()

logs=[]; applied=[]; warns=[]
for f in C1:
    fn=f+"__BODY.html"; t=open(fn,encoding="utf-8").read(); orig=t
    edits=[]
    def repl_el(m):
        open_t,tag,inner,close=m.group(1),m.group(2),m.group(3),m.group(4)
        if '구독' not in inner: return m.group(0)
        n=norm(inner)
        new_inner=None; new_href=None
        if n in KEEP: return m.group(0)
        if f in COMMERCE and n=="구독하고 함께 시작하기 →":
            new_inner="함께 시작하기 →"  # keep href (commerce brand-start)
        elif n in FREE_MAP:
            new_inner=FREE_MAP[n]        # keep href (free letter)
        elif n in PREMIUM_CTAS:
            new_inner=PREM; new_href="/premium"
        else:
            if '구독하고' in n or '구독으로' in n:
                warns.append(f"{f}: UNMAPPED element inner=<{n}>")
            return m.group(0)
        ot=open_t
        if new_href: ot=re.sub(r'href="[^"]*"','href="%s"'%new_href,ot)
        edits.append((n,new_inner,new_href))
        return ot+new_inner+close
    t=re.sub(r'(<(a|button)\b[^>]*>)(.*?)(</\2>)', repl_el, t, flags=re.S)
    # body-text sentences
    def sub_count(t,old,new):
        c=t.count(old)
        return (t.replace(old,new),c)
    if f in COMMERCE:
        for old,new in [("부부연구소 구독으로 함께 시작해요","부부연구소와 함께 시작해요"),
                        ("부부연구소 구독이면 둘 다 함께예요","부부연구소와 함께라면 둘 다 함께예요"),
                        ("구독자 <b>추가 할인</b>","프리미엄 회원 <b>추가 할인</b>")]:
            t,c=sub_count(t,old,new)
            if c: edits.append((old,new,"body"))
    else:
        # non-commerce premium body sentences
        c=len(re.findall(r'부부연구소 구독으로 ',t))
        if c: t=t.replace("부부연구소 구독으로 ","부부연구소 프리미엄으로 "); edits.append(("부부연구소 구독으로 …","부부연구소 프리미엄으로 …","body"))
        c=t.count("구독으로 열려요")
        if c: t=t.replace("구독으로 열려요","프리미엄으로 열려요"); edits.append(("…구독으로 열려요","…프리미엄으로 열려요","body"))
    if t!=orig:
        # balance check
        for tag in ("a","button","div","section","span","p"):
            o=len(re.findall(r'<'+tag+r'\b',orig)); c=len(re.findall(r'</'+tag+r'>',orig))
            no=len(re.findall(r'<'+tag+r'\b',t)); nc=len(re.findall(r'</'+tag+r'>',t))
            if (o-c)!=(no-nc): warns.append(f"{f}: TAG IMBALANCE {tag} {o-c}->{no-nc}")
        rule="C2" if f in COMMERCE else "C1"
        applied.append({"file":fn,"rule":rule,"n":len(edits)})
        logs.append((f,edits))
        if not DRY:
            tmp=fn+".tmp"; open(tmp,"w",encoding="utf-8").write(t); os.replace(tmp,fn)

# report
for f,edits in logs:
    print(f"\n### {f}  ({len(edits)} edits)")
    for a,b,c in edits: print(f"    [{c}] {a[:34]:<34} -> {b[:34]}")
print("\n===== WARNINGS =====")
for w in warns: print("  !!",w)
print(f"\nDRY={DRY}  files_touched={len(applied)}  total_edits={sum(a['n'] for a in applied)}")
# residual 구독하고 in touched files (premium/persuasion pattern only)
print("\n===== residual '구독하고' after (in-memory) =====")
for f,_ in logs: pass
