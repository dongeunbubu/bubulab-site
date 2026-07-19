import re,sys,collections
FN=sys.argv[1]; ORIG=sys.argv[2]
cur=open(FN,encoding="utf-8").read(); orig=open(ORIG,encoding="utf-8").read()

def chips(s): return sorted(re.findall(r'<button type="button" data-cx-w="term-chip"[^>]*>.*?</button>', s, re.S))
def hrefs(s): return collections.Counter(re.findall(r'href="([^"]*)"', s)) + collections.Counter(re.findall(r'data-href="([^"]*)"', s))
def nums(s):
    # strip tags first so we compare numbers in both prose and markup identically
    return collections.Counter(re.findall(r'\d[\d,\.]*', s))
def cxw(s): return sorted(re.findall(r'<div class="cxw"[^>]*></div>', s, re.S))
def svg(s): return sorted(re.findall(r'<svg.*?</svg>', s, re.S))
def figcap(s): return sorted(re.findall(r'<p class="cx-figcap"[^>]*>.*?</p>', s, re.S))

ok=True
def chk(name,a,b):
    global ok
    same = a==b
    ok = ok and same
    print(("  OK  " if same else " FAIL ")+name)
    if not same and isinstance(a,list):
        sa,sb=set(a),set(b)
        for x in list(sb-sa)[:6]: print("     - removed:",x[:90])
        for x in list(sa-sb)[:6]: print("     + added  :",x[:90])
    if not same and isinstance(a,collections.Counter):
        d=(a-b)+(b-a)
        print("     delta:",dict(list(d.items())[:20]))

print("### IMMUTABILITY (cur vs orig) — must all OK ###")
chk("chips inventory", chips(orig), chips(cur))
chk("href multiset", hrefs(orig), hrefs(cur))
chk("number multiset", nums(orig), nums(cur))
chk("cxw widget blocks", cxw(orig), cxw(cur))
chk("svg blocks", svg(orig), svg(cur))
chk("figcap blocks", figcap(orig), figcap(cur))

print("\n### TAG BALANCE / hygiene ###")
for t in ["p","button","div","section","svg","h2","text","a","table"]:
    o=len(re.findall(f'<{t}[ >]',cur)); c=len(re.findall(f'</{t}>',cur))
    flag="" if o==c else "  <-- MISMATCH"
    print(f"  <{t}>={o}  </{t}>={c}{flag}")
print("  '<!--' comments:", cur.count("<!--"))

# gate metrics on prose zones
body=re.findall(r'<p class="cx-rd-p">(.*?)</p>',cur,re.S)
lead=re.findall(r'<p class="cx-rd-lead">(.*?)</p>',cur,re.S)
h2=re.findall(r'<h2 class="cx-rd-h2">(.*?)</h2>',cur,re.S)
prose=" ".join(re.sub(r'<[^>]+>','',x) for x in body+lead+h2)
print("\n### GATE METRICS (prose scope) ###")
print("  그릇 prose:",prose.count("그릇"),"| doc total:",cur.count("그릇"))
print("  흐름이에요:",prose.count("흐름이에요"),"| 흐름 any(prose):",prose.count("흐름"))
print("  셈이 prose:",prose.count("셈이"),"| doc:",cur.count("셈이"))
print("  자리예요:",prose.count("자리예요"),"| 자리라:",prose.count("자리라"))
for w in ["계보","불가피","감수","소급","잠정","임박"]:
    print(f"  {w}: prose={prose.count(w)} doc={cur.count(w)}")
print("  -- signatures (prose) --")
for m in [",,",":)","ㅎㅎ","ㅠㅠ"]:
    print(f"    '{m}': {prose.count(m)}")
print("  -- voice (prose) --")
for m in ["거든요","네요","여러분","고요","죠"]:
    print(f"    '{m}': {prose.count(m)}")
# sentence length stdev (prose, split on . ? ! and 다./요. boundaries roughly)
sents=[s for s in re.split(r'(?<=[.!?])\s+', prose) if len(s.strip())>1]
import statistics
lens=[len(s) for s in sents]
print(f"  sentences:{len(lens)} mean_len={statistics.mean(lens):.1f} stdev={statistics.pstdev(lens):.1f}")
print("\nRESULT:", "ALL IMMUTABLE-CHECKS PASS" if ok else "*** IMMUTABILITY FAIL ***")
