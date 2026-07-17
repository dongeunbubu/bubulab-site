#!/usr/bin/env python3
import json, os, io
CI='/tmp/bbfb2/contents/contents_index.json'
LI='/tmp/bbfb2/contents/legacy_index.json'
def atomic(path,obj):
    tmp=path+'.tmp'
    with io.open(tmp,'w',encoding='utf-8',newline='') as f:
        json.dump(obj,f,ensure_ascii=False,indent=1); f.write('\n'); f.flush(); os.fsync(f.fileno())
    os.replace(tmp,path)

ci=json.load(open(CI,encoding='utf-8'))
ci['updated']='2026-07-18T09:00:00'
ci['schema']='v2'
by={it['slug']:it for it in ci['items']}
# demonstrate every new field, backward-compatible (only enrich a few; others untouched)
patch={
 'bookcol-01':{'free':True,'pages':52,'chapters':6,'basis_date':'2026-07','next_review':'2026-10','pair':'booktool-portfolio','related':['bookcol-04','bookcol-13']},
 'bookcol-04':{'free':True,'pages':50,'chapters':5,'pair':'bookcol-05','related':['bookcol-01']},
 'bookcol-08':{'pages':54,'chapters':7,'basis_date':'2026-07','next_review':'2026-10','related':['bookcol-09']},
 'bookcol-13':{'free':True,'pair':'booktool-couplecheck','related':['bookcol-02']},
 'booktool-portfolio':{'pair':'bookcol-11','related':['bookcol-05','bookcol-06']},
}
n=0
for slug,fields in patch.items():
    if slug in by:
        by[slug].update(fields); n+=1
atomic(CI,ci)

li=json.load(open(LI,encoding='utf-8'))
li['schema']='v2'
lby={it['slug']:it for it in li['items']}
for slug in ('tool-4a49','tool-853a'):
    if slug in lby:
        lby[slug]['free']=True
        lby[slug]['basis_date']='2026-07'
atomic(LI,li)

# validate
json.load(open(CI,encoding='utf-8')); json.load(open(LI,encoding='utf-8'))
print('INDEX v2 OK · contents patched=%d · schema=v2'%n)
print('new fields present:', sorted(set().union(*[set(v) for v in patch.values()])))
# backward-compat: count items WITHOUT any new field (must still be majority, untouched)
newf={'free','pages','chapters','pair','related','basis_date','next_review'}
untouched=sum(1 for it in ci['items'] if not (newf & set(it)))
print('contents items untouched (no new field) =',untouched,'/',len(ci['items']))
