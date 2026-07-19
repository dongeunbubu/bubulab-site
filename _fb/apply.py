import sys,os,importlib.util
FN=sys.argv[1]; ORIG=sys.argv[2]; REPMOD=sys.argv[3]
spec=importlib.util.spec_from_file_location("rep",REPMOD); rep=importlib.util.module_from_spec(spec); spec.loader.exec_module(rep)
text=open(ORIG,encoding="utf-8").read()
n=0
for i,(old,new) in enumerate(rep.REP):
    c=text.count(old)
    if c!=1:
        raise SystemExit(f"[REP #{i}] old occurs {c}x (need 1): {old[:70]!r}")
    text=text.replace(old,new); n+=1
tmp=FN+".tmp"
open(tmp,"w",encoding="utf-8").write(text)
os.replace(tmp,FN)
print(f"applied {n} replacements -> {FN}")
