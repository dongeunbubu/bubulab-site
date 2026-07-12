# -*- coding: utf-8 -*-
import json,re,os
BODY='/tmp/bbfb/imweb_cdn/contents-hub__BODY.html'
idx=json.load(open('/tmp/bbfb/contents/contents_index.json',encoding='utf-8'))['items']
by_slug={i['slug']:i for i in idx}
STAGE={'gather':'seed','keep':'bud','grow':'bloom'}

def slug_from_href(h):
    frag=h.split('#',1)[1] if '#' in h else ''
    return ('kit-'+frag) if h.startswith('/contents-kits') else frag

def flower(stage,tk,prem):
    shape='cxBud' if prem else {'seed':'cxSeed','bud':'cxBud','bloom':'cxBloom'}[stage]
    acc={'column':'cxAcCol','tool':'cxAcTool','kit':'cxAcKit'}[tk]
    dew='<circle class="cx-dew" cx="16.5" cy="14" r="3"></circle>' if prem else ''
    return ('<svg class="cx-flower" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<use class="cx-shape" href="#'+shape+'"></use>'
            '<use class="cx-acc" href="#'+acc+'"></use>'+dew+'</svg>')

s=open(BODY,encoding='utf-8').read()
orig_bytes=len(s.encode())
hrefs_before=re.findall(r'<a class="jm-node[^>]*href="([^"]+)"',s)

# ---------- A. cx token rule (jm-* aliased -> cx-*) inserted before ".jm-scope *{" ----------
TOKEN_RULE=(
".jm-scope{"
"--cx-bg:#FDFBF7;--cx-bg2:#FBF3EE;--cx-card:#FFFFFF;"
"--cx-ink:#3E2F29;--cx-ink2:#5C4B43;--cx-mut:#8A7B72;--cx-border:#EAD7D3;"
"--cx-rose:#B33A4C;--cx-rose2:#B85060;--cx-deep:#7C243B;"
"--cx-pink:#D67A89;--cx-pinkSoft:#F8E8EA;--cx-pinkSoft2:#FCEEF1;"
"--cx-sage:#5E8C7F;--cx-gold:#C9A84C;--cx-lav:#9C6BA8;--cx-sand:#F0DED8;"
"--cx-up:#D8584E;--cx-down:#4A7DE8;"
"--cx-seed:#7FB08A;--cx-bud:#E08696;--cx-bloom:#B33A4C;--cx-pollen:#C9A84C;"
"--cx-zone-gather:rgba(94,140,127,.10);--cx-zone-keep:rgba(179,58,76,.08);--cx-zone-grow:rgba(201,168,76,.13);"
"--cx-fs-cap:clamp(12px,1.4vw,13px);--cx-fs-body:clamp(15px,1.6vw,17px);--cx-fs-lead:clamp(17px,2vw,19.5px);"
"--cx-fs-h3:clamp(18px,2.3vw,23px);--cx-fs-h2:clamp(23px,3.4vw,34px);--cx-fs-h1:clamp(27px,4vw,42px);--cx-fs-hero:clamp(34px,5.4vw,68px);"
"--cx-lh-body:1.75;--cx-lh-head:1.3;--cx-tr-head:-.02em;"
"--cx-r:22px;--cx-r-sm:14px;--cx-maxw:1180px;--cx-read:720px;"
"--cx-pad-sec:clamp(120px,13vw,192px);--cx-pad-hero:clamp(44px,6vw,84px);--cx-pad-x:clamp(22px,4.5vw,40px);"
"--cx-sh:0 1px 2px rgba(62,47,41,.04),0 4px 10px rgba(190,80,96,.05),0 14px 30px rgba(190,80,96,.07);"
"--cx-shi:0 2px 4px rgba(62,47,41,.05),0 12px 24px rgba(190,80,96,.10),0 28px 56px rgba(190,80,96,.15);"
"--cx-ease:cubic-bezier(.16,1,.3,1);--cx-dur:.6s;"
"--jm-bg:var(--cx-bg);--jm-bg2:var(--cx-bg2);--jm-card:var(--cx-card);"
"--jm-ink:var(--cx-ink);--jm-ink2:var(--cx-ink2);--jm-mut:var(--cx-mut);"
"--jm-rose:var(--cx-rose);--jm-rose2:var(--cx-rose2);--jm-deep:var(--cx-deep);"
"--jm-sage:var(--cx-sage);--jm-gold:var(--cx-gold);"
"--jm-pinkSoft:var(--cx-pinkSoft);--jm-pinkSoft2:var(--cx-pinkSoft2);--jm-sand:var(--cx-sand);--jm-border:var(--cx-border);"
"--jm-ease:var(--cx-ease);--jm-maxw:var(--cx-maxw);"
"--jm-sh:var(--cx-sh);--jm-shi:var(--cx-shi)}\n")
assert s.count(".jm-scope *{box-sizing:border-box")==1
s=s.replace(".jm-scope *{box-sizing:border-box", TOKEN_RULE+".jm-scope *{box-sizing:border-box",1)

# ---------- B. bloom / season / particle / hero-cta CSS before </style> ----------
BLOOM_CSS=r"""
/* ===== 개화(開花) 시스템 · cx 토큰 승계(색·타이포·모션 값 토큰화) ===== */
.cx-sprite{position:absolute;width:0;height:0;overflow:hidden}
.jm-node .jm-emo{position:relative;overflow:visible}
.jm-emo .cx-flower{width:62%;height:62%;display:block;overflow:visible;fill:currentColor;color:var(--cx-stage,var(--cx-bloom));transform:scale(.34) rotate(-14deg);opacity:0;transition:transform .72s var(--cx-ease),opacity .5s var(--cx-ease);transition-delay:calc(var(--jm-i,0)*.05s)}
.jm-n-kit .jm-emo .cx-flower{width:72%;height:72%}
.jm-node.jm-in .jm-emo .cx-flower{transform:none;opacity:1}
.jm-s-seed{--cx-stage:var(--cx-seed)}.jm-s-bud{--cx-stage:var(--cx-bud)}.jm-s-bloom{--cx-stage:var(--cx-bloom)}
.cx-dew{fill:#fff;stroke:var(--cx-down);stroke-width:.5;opacity:.85}
.jm-node.jm-live:hover .jm-emo .cx-flower,.jm-node.jm-live:focus-visible .jm-emo .cx-flower{transform:scale(1.14) rotate(7deg)}
.jm-emo::before,.jm-emo::after{content:"";position:absolute;top:15%;width:5px;height:5px;border-radius:50%;background:var(--cx-pollen);opacity:0;pointer-events:none;z-index:2}
.jm-emo::before{left:44%}.jm-emo::after{left:58%}
.jm-node.jm-live:hover .jm-emo::before,.jm-node.jm-live:focus-visible .jm-emo::before{animation:cxPollen 1.25s var(--cx-ease)}
.jm-node.jm-live:hover .jm-emo::after,.jm-node.jm-live:focus-visible .jm-emo::after{animation:cxPollen 1.5s .18s var(--cx-ease)}
@keyframes cxPollen{0%{opacity:0;transform:translate(-50%,0) scale(.5)}25%{opacity:.95}100%{opacity:0;transform:translate(-40%,-30px) scale(1.05)}}
.jm-prem .jm-emo{border-color:var(--cx-bud)}
.jm-prem .cx-flower{filter:saturate(.92)}
.jm-prem .cx-dew{animation:cxDew 3.4s var(--cx-ease) infinite}
@keyframes cxDew{0%,100%{opacity:.5}50%{opacity:1}}
.jm-node.jm-prem.jm-live:hover .cx-dew,.jm-node.jm-prem.jm-live:focus-visible .cx-dew{opacity:1}
.jm-node.jm-visited .jm-emo{border-color:var(--cx-bloom);box-shadow:0 0 0 3px var(--cx-pinkSoft2),var(--cx-sh)}
.jm-node.jm-visited .cx-flower{filter:drop-shadow(0 0 5px rgba(201,168,76,.55))}
.jm-b-stage{background:var(--cx-pinkSoft2);color:var(--cx-rose)}
/* 히어로 시작 CTA */
.jm-herocta{display:inline-flex;align-items:center;gap:8px;margin:22px auto 0;background:var(--cx-rose);color:#fff;padding:13px 24px;border-radius:100px;font-weight:800;font-size:15px;box-shadow:var(--cx-sh);transition:transform .2s,box-shadow .25s,background .2s}
.jm-herocta:hover{background:var(--cx-deep);transform:translateY(-2px);box-shadow:var(--cx-shi)}
.jm-herocta .jm-ar{transition:transform .25s}.jm-herocta:hover .jm-ar{transform:translateX(4px)}
.jm-legend .jm-lgd{color:var(--cx-border)}
/* 계절 환경 파티클(절제) */
.cx-part,.cx-fly{position:absolute;pointer-events:none;z-index:1}
.cx-spring{width:9px;height:9px;border-radius:50%;background:radial-gradient(circle at 40% 40%,#fff,rgba(126,176,138,.5));opacity:.7;animation:cxFloat 9s var(--cx-ease) infinite}
.cx-seed2{width:6px;height:9px;border-radius:50% 50% 50% 50%/62% 62% 40% 40%;background:var(--cx-pollen);opacity:.72;animation:cxFall 8.5s linear infinite}
.cx-fly{animation:cxDrift 12s var(--cx-ease) infinite}
@keyframes cxFloat{0%,100%{transform:translate(0,0)}50%{transform:translate(14px,-16px)}}
@keyframes cxFall{0%{transform:translate(0,-10px) rotate(0);opacity:0}15%{opacity:.72}100%{transform:translate(-16px,64px) rotate(120deg);opacity:0}}
@keyframes cxDrift{0%,100%{transform:translate(0,0) rotate(-4deg)}50%{transform:translate(22px,-12px) rotate(5deg)}}
@media(max-width:640px){.jm-emo .cx-flower{width:66%;height:66%}.cx-fly{display:none}}
@media(prefers-reduced-motion:reduce){
.jm-emo .cx-flower{transition:none!important;transform:none!important;opacity:1!important}
.jm-emo::before,.jm-emo::after,.jm-prem .cx-dew,.cx-part,.cx-fly{animation:none!important}
}
"""
assert s.count("</style>")==1
s=s.replace("</style>", BLOOM_CSS+"</style>",1)

# ---------- C. hero (copy A) ----------
NEW_HERO=(
'<section class="jm-hero jm-wrap">'
'<span class="jm-eyebrow jm-reveal">\U0001F331 우리 돈이 피어나는 지도</span>'
'<h1 class="jm-h1 jm-reveal">심은 대로 피어나요,<br>두 분의 <span class="jm-grad">돈나무</span></h1>'
'<p class="jm-lead jm-reveal">반지하에서 심은 작은 씨앗이, 돈을 <b>모으고·지키고·불리는</b> 세 계절을 지나 이만큼 자랐어요.</p>'
'<p class="jm-lead jm-reveal">맨 위 새싹에서 아래 만개까지, 두 분의 속도로 천천히 피워가면 돼요,,ㅎㅎ</p>'
'<a class="jm-herocta jm-reveal" href="#jmSeedStart">첫 새싹부터 보기 <span class="jm-ar">→</span></a>'
'<div class="jm-legend jm-reveal">'
'<span><b>\U0001F331 새싹</b> 모으기</span>'
'<span><b>\U0001F338 봉오리</b> 지키기</span>'
'<span><b>\U0001F33A 만개</b> 불리기</span>'
'<span class="jm-lgd">·</span>'
'<span><b>잎맥</b> 칼럼</span><span><b>톱니</b> 도구</span><span><b>큰 꽃</b> 키트</span>'
'<span>· 잠긴 봉오리엔 이슬이 맺혔 있어요</span>'
'</div></section>')
s2=re.sub(r'<section class="jm-hero jm-wrap">.*?</section>', lambda m:NEW_HERO, s, count=1, flags=re.S)
assert s2!=s and s2.count('첫 새싹부터 보기')==1 and s2.count('class="jm-herocta')==1
s=s2

# ---------- D. seed-start id on gather zone label ----------
GZ='<div class="jm-zlabel jm-zl-gather jm-reveal" style="top:3.18%" data-zone="gather">'
assert s.count(GZ)==1
s=s.replace(GZ,'<div class="jm-zlabel jm-zl-gather jm-reveal" id="jmSeedStart" style="top:3.18%" data-zone="gather">',1)

# ---------- E. SVG sprite + season particles after <div class="jm-map" id="jmMap"> ----------
SPRITE=(
'<svg class="cx-sprite" width="0" height="0" aria-hidden="true" focusable="false"><defs>'
'<symbol id="cxPetal" viewBox="0 0 48 48"><path d="M24 24C18.6 20 18.6 9.6 24 4C29.4 9.6 29.4 20 24 24Z"></path></symbol>'
'<symbol id="cxSeed" viewBox="0 0 48 48"><path d="M24 40V23" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linecap="round"></path><path d="M24 25C19 25.4 13 22 11 15.4C18 14.4 23 17.6 24 24Z"></path><path d="M24 25C29 25.4 35 22 37 15.4C30 14.4 25 17.6 24 24Z"></path></symbol>'
'<symbol id="cxBud" viewBox="0 0 48 48"><path d="M24 42V29" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"></path><path d="M24 6C31 13 31 24.5 24 30C17 24.5 17 13 24 6Z"></path><path d="M24 30C21 27.5 15.5 27.5 13.5 31.5C18 34 23 33 24 30Z"></path><path d="M24 30C27 27.5 32.5 27.5 34.5 31.5C30 34 25 33 24 30Z"></path></symbol>'
'<symbol id="cxBloom" viewBox="0 0 48 48"><use href="#cxPetal" transform="rotate(0 24 24)"></use><use href="#cxPetal" transform="rotate(72 24 24)"></use><use href="#cxPetal" transform="rotate(144 24 24)"></use><use href="#cxPetal" transform="rotate(216 24 24)"></use><use href="#cxPetal" transform="rotate(288 24 24)"></use><circle cx="24" cy="24" r="4.6" fill="var(--cx-pollen)"></circle></symbol>'
'<symbol id="cxAcCol" viewBox="0 0 48 48"><path d="M24 34V20M24 25.5L20 22M24 25.5L28 22" fill="none" stroke="var(--cx-sage)" stroke-width="1.5" stroke-linecap="round" opacity=".85"></path></symbol>'
'<symbol id="cxAcTool" viewBox="0 0 48 48"><g fill="none" stroke="var(--cx-mut)" stroke-width="1.5"><circle cx="24" cy="36" r="3.6"></circle><path d="M24 31.4V29M24 42.6V40.2M18.4 36H16M32 36H29.6" stroke-linecap="round"></path></g></symbol>'
'<symbol id="cxAcKit" viewBox="0 0 48 48"><path d="M20.5 22.5h7v10l-3.5-2.6-3.5 2.6z" fill="var(--cx-rose)" opacity=".9"></path></symbol>'
'</defs></svg>')
PARTS=(
'<span class="cx-part cx-spring" style="left:16%;top:8.5%"></span>'
'<span class="cx-part cx-spring" style="left:82%;top:22%"></span>'
'<span class="cx-fly" style="left:31%;top:47%"><svg width="20" height="16" viewBox="0 0 20 16" aria-hidden="true"><path d="M10 8C7 2 1 2 2 8C1 14 7 14 10 8ZM10 8C13 2 19 2 18 8C19 14 13 14 10 8Z" fill="var(--cx-bud)" opacity=".7"></path></svg></span>'
'<span class="cx-part cx-seed2" style="left:70%;top:84%"></span>'
'<span class="cx-part cx-seed2" style="left:40%;top:93%"></span>')
MAPOPEN='<div class="jm-map" id="jmMap">'
assert s.count(MAPOPEN)==1
s=s.replace(MAPOPEN, MAPOPEN+SPRITE+PARTS,1)

# ---------- F. season gradient defs + band fills ----------
assert s.count("</linearGradient></defs>")==1
SEASON=('<linearGradient id="jmSeasonGather" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(94,140,127,.05)"></stop><stop offset="1" stop-color="rgba(94,140,127,.15)"></stop></linearGradient>'
'<linearGradient id="jmSeasonKeep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(179,58,76,.05)"></stop><stop offset="1" stop-color="rgba(179,58,76,.12)"></stop></linearGradient>'
'<linearGradient id="jmSeasonGrow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(201,168,76,.07)"></stop><stop offset="1" stop-color="rgba(201,168,76,.2)"></stop></linearGradient>')
s=s.replace("</linearGradient></defs>", "</linearGradient>"+SEASON+"</defs>",1)
for a,b in [('rx="48" fill="rgba(94,140,127,.10)"','rx="48" fill="url(#jmSeasonGather)"'),
            ('rx="48" fill="rgba(179,58,76,.08)"','rx="48" fill="url(#jmSeasonKeep)"'),
            ('rx="48" fill="rgba(201,168,76,.13)"','rx="48" fill="url(#jmSeasonGrow)"')]:
    assert s.count(a)==1, a
    s=s.replace(a,b,1)

# ---------- G. nodes -> bloom flowers + stage/slug meta ----------
node_re=re.compile(r'<a class="jm-node jm-n-(column|tool|kit) jm-live"([^>]*)>(<span class="jm-emo">)(.*?)(</span>)',re.S)
counts={'seed':0,'bud':0,'bloom':0,'prem':0}
def repl(m):
    tk,attrs,emoopen,emoji,emoclose=m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)
    href=re.search(r'href="([^"]+)"',attrs).group(1)
    slug=slug_from_href(href)
    assert slug in by_slug, "unknown slug "+slug
    zone=by_slug[slug]['zone']; stage=STAGE[zone]
    prem='data-prem="1"' in attrs
    counts[stage]+=1
    if prem: counts['prem']+=1
    prem_cls=' jm-prem' if prem else ''
    attrs2=attrs.replace('data-live="1"', 'data-live="1" data-stage="'+stage+'" data-slug="'+slug+'"',1)
    return ('<a class="jm-node jm-n-'+tk+' jm-live jm-s-'+stage+prem_cls+'"'+attrs2+'>'
            +emoopen+flower(stage,tk,prem)+emoclose)
s,n=node_re.subn(repl,s)
assert n==29, "node subn=%d"%n

# ---------- verify + atomic write ----------
hrefs_after=re.findall(r'<a class="jm-node[^>]*href="([^"]+)"',s)
assert hrefs_before==hrefs_after, "HREF CHANGED"
assert s.count('data-live="1"')==29
assert s.count('class="cx-flower"')==29
new_bytes=len(s.encode())
tmp=BODY+'.tmp'
open(tmp,'w',encoding='utf-8').write(s)
os.replace(tmp,BODY)
print("OK nodes=%d stages=%s"%(n,counts))
print("bytes %d -> %d (%.1fKB)"%(orig_bytes,new_bytes,new_bytes/1024))
print("hrefs unchanged:",hrefs_before==hrefs_after)
