import re,os,sys
os.chdir("/tmp/bbfb/imweb_cdn")
DRY = ("--apply" not in sys.argv)
EXTRA=["tool-3dad","tool-52-f1dd","tool-568e","tool-64bb","tool-ac1c","tool-af26","tool-bc45","tool-dsr-6e40","tool-pro-1d9e","tool-pro-3a11","tool-pro-9b41","tool-pro-fbcd","tool-vs-24fc"]
PREM="프리미엄으로 모두 열기 →"
def norm(s): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',s)).strip()
applied=[]; warns=[]
for f in EXTRA:
    fn=f+"__BODY.html"; t=open(fn,encoding="utf-8").read(); orig=t; edits=[]
    def repl(m):
        ot,tag,inner,close=m.group(1),m.group(2),m.group(3),m.group(4)
        if '구독하고' not in inner: return m.group(0)
        n=norm(inner)
        ot2=re.sub(r'href="[^"]*"','href="/premium"',ot)
        edits.append((n,PREM))
        return ot2+PREM+close
    t=re.sub(r'(<(a|button)\b[^>]*>)(.*?)(</\2>)',repl,t,flags=re.S)
    if t!=orig:
        for tag in ("a","span","p","div","button","section"):
            if (len(re.findall('<'+tag+r'\b',orig))-len(re.findall('</'+tag+'>',orig)))!=(len(re.findall('<'+tag+r'\b',t))-len(re.findall('</'+tag+'>',t))): warns.append(f"{fn}: IMBALANCE {tag}")
        if t.count('구독하고'): warns.append(f"{fn}: residual 구독하고={t.count('구독하고')}")
        applied.append({"file":fn,"rule":"C1","n":len(edits)})
        print(f"### {fn}: {edits[0][0][:40]} -> {PREM}  (href=/premium)")
        if not DRY:
            tmp=fn+".tmp"; open(tmp,"w",encoding="utf-8").write(t); os.replace(tmp,fn)
print("\nWARN:",warns if warns else "none")
print(f"DRY={DRY} files={len(applied)}")
