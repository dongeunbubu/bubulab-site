# -*- coding: utf-8 -*-
import os, re, glob, json, tempfile

CDN = "/tmp/bbfb/imweb_cdn"
CK  = os.path.join(CDN, "contents-kits__BODY.html")

def atomic_write(path, text):
    d = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)

# ---------- new kx- CSS (merge bands) ----------
CSS = r"""
/* ===== [merge] kit 흡수 밴드 · kx- 접두 · cx 토큰 승계 ===== */
.kx-mband{position:relative;padding:clamp(30px,4.5vw,52px) 0;border-top:1px solid var(--border)}
.kx-mbandin{max-width:var(--maxw);margin:0 auto;padding:0 clamp(22px,4.5vw,40px)}
.kx-mhead{max-width:640px;margin:0 auto 22px;text-align:center}
.kx-meyebrow{display:inline-flex;align-items:center;gap:7px;font-size:11.5px;font-weight:800;letter-spacing:.05em;color:var(--rose);background:var(--pinkSoft);border:1px solid var(--border);border-radius:999px;padding:6px 13px}
.kx-mh2{font-size:clamp(20px,3vw,27px);font-weight:900;letter-spacing:-.02em;color:var(--ink);line-height:1.32;margin-top:12px}
.kx-mh2 small{font-size:12px;color:var(--mut);font-weight:700}
.kx-mdesc{font-size:14.5px;color:var(--ink2);font-weight:600;line-height:1.66;margin-top:10px}
.kx-pick{display:grid;grid-template-columns:.85fr 1.4fr;gap:clamp(16px,3vw,30px);align-items:stretch;max-width:960px;margin:0 auto;background:linear-gradient(150deg,#fff,var(--pinkSoft2));border:1px solid var(--border);border-radius:var(--cx-r);box-shadow:var(--sh1);overflow:hidden}
.kx-pickfig{position:relative;display:flex;align-items:center;justify-content:center;background:linear-gradient(150deg,var(--pink),var(--rose));color:#fff;min-height:180px;padding:24px}
.kx-pickfig svg{width:74px;height:74px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;opacity:.95}
.kx-pickrib{position:absolute;top:14px;left:14px;font-size:11px;font-weight:800;color:var(--deep);background:#fff;border-radius:999px;padding:5px 11px;box-shadow:var(--sh1)}
.kx-pickbody{padding:clamp(20px,3vw,28px)}
.kx-picktag{display:inline-block;font-size:11.5px;font-weight:800;color:var(--rose);background:var(--pinkSoft);border-radius:999px;padding:5px 12px}
.kx-pickh3{font-size:clamp(18px,2.3vw,22px);font-weight:900;letter-spacing:-.02em;color:var(--ink);line-height:1.3;margin-top:12px}
.kx-picklead{font-size:14.5px;color:var(--ink2);font-weight:600;line-height:1.68;margin-top:10px}
.kx-picklead b{color:var(--rose);font-weight:800}
.kx-pickfeat{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:8px}
.kx-pickfeat li{position:relative;padding-left:24px;font-size:13.5px;color:var(--ink);font-weight:600;line-height:1.5}
.kx-pickfeat li::before{content:"";position:absolute;left:2px;top:6px;width:13px;height:13px;border-radius:50%;background:var(--sage);box-shadow:inset 0 0 0 2px #fff}
.kx-pickcta{display:inline-flex;align-items:center;gap:7px;margin-top:18px;min-height:48px;padding:13px 24px;border-radius:14px;background:linear-gradient(135deg,var(--rose),var(--deep));color:#fff;font-size:15px;font-weight:800;box-shadow:0 14px 30px -12px rgba(179,58,76,.55);transition:transform .3s var(--ease2)}
.kx-pickcta:hover{transform:translateY(-2px)}
.kx-pickcta i{font-style:normal;transition:transform .25s}
.kx-pickcta:hover i{transform:translateX(4px)}
.kx-pickuse{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:960px;margin:18px auto 0}
.kx-ustep{background:#fff;border:1px solid var(--border);border-radius:14px;padding:16px}
.kx-ustep b{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;background:var(--pinkSoft);color:var(--rose);font-size:13px;font-weight:900}
.kx-ustep h4{font-size:14px;font-weight:800;color:var(--ink);margin-top:9px}
.kx-ustep p{font-size:12.5px;color:var(--ink2);font-weight:600;line-height:1.55;margin-top:5px}
.kx-vgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;max-width:var(--maxw);margin:0 auto}
.kx-vcard{background:#fff;border:1px solid var(--border);border-radius:18px;padding:20px;box-shadow:var(--sh1);display:flex;flex-direction:column}
.kx-vstars{color:var(--gold);font-size:14px;letter-spacing:2px}
.kx-vtxt{font-size:13.5px;color:var(--ink2);font-weight:600;line-height:1.66;margin-top:10px;flex:1}
.kx-vwho{display:flex;align-items:center;gap:10px;margin-top:15px}
.kx-vav{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;color:#fff;font-size:14px;font-weight:800;flex:none}
.kx-vnm{font-size:13px;font-weight:800;color:var(--ink);display:flex;flex-direction:column}
.kx-vnm small{font-size:11.5px;color:var(--mut);font-weight:600;margin-top:1px}
.kx-mgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;max-width:var(--maxw);margin:0 auto}
.kx-mcard{display:block;background:#fff;border:1px solid var(--border);border-radius:18px;padding:22px;box-shadow:var(--sh1);transition:transform .3s var(--ease2),box-shadow .3s}
.kx-mcard:hover{transform:translateY(-3px);box-shadow:var(--sh2)}
.kx-mico{display:flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:13px;color:#fff}
.kx-mico svg{width:24px;height:24px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.kx-mcard h4{font-size:15.5px;font-weight:900;color:var(--ink);margin-top:14px}
.kx-mcard p{font-size:13px;color:var(--ink2);font-weight:600;line-height:1.6;margin-top:8px}
.kx-mkicker{display:inline-flex;align-items:center;gap:5px;margin-top:12px;font-size:13px;font-weight:800;color:var(--rose)}
.kx-mkicker i{font-style:normal;transition:transform .25s}
.kx-mcard:hover .kx-mkicker i{transform:translateX(4px)}
.kx-msub{text-align:center;margin-top:22px}
.kx-msub a{display:inline-flex;align-items:center;gap:7px;font-size:14.5px;font-weight:800;color:var(--rose);border-bottom:2px solid var(--pinkSoft);padding-bottom:3px}
@media(max-width:760px){.kx-pick{grid-template-columns:1fr}.kx-pickfig{min-height:130px}.kx-pickuse{grid-template-columns:1fr}.kx-vgrid,.kx-mgrid{grid-template-columns:1fr}}
"""

# ---------- band A: 대표 키트 spotlight (+ 이용안내 3-step) ----------
PICK = r"""<section class="kx-mband" aria-label="대표 키트">
 <div class="kx-mbandin">
  <div class="kx-mhead">
   <span class="kx-meyebrow">✦ 먼저 만나는 키트</span>
   <h2 class="kx-mh2">처음이라면, 이 키트부터</h2>
   <p class="kx-mdesc">동은부부가 실제로 쓰는 통장 구조를 그대로 옮겼어요.</p>
  </div>
  <div class="kx-pick">
   <div class="kx-pickfig"><span class="kx-pickrib">동은부부 픽</span><svg viewBox="0 0 24 24"><rect x="3" y="6" width="18" height="13" rx="2.2"/><path d="M3 10.5h18"/><circle cx="16.5" cy="14.6" r="1.25"/></svg></div>
   <div class="kx-pickbody">
    <span class="kx-picktag">전자책 · 엑셀 시트</span>
    <h3 class="kx-pickh3">신혼부부 통장 쪼개기 가계부 키트</h3>
    <p class="kx-picklead">'이번 달 우리 얼마 썼지?'가 <b>한 파일에서</b> 끝나요.</p>
    <p class="kx-picklead">월급이 들어오면 자동으로 나뉘는 시트에 공동 예산·고정비·비상금까지 담았어요.</p>
    <ul class="kx-pickfeat">
     <li>공동 예산·고정비·비상금을 한 번에 합산하는 시트</li>
     <li>통장 쪼개기 구조를 그대로 옮긴 분배 템플릿</li>
     <li>처음 쓰는 부부를 위한 작성 가이드 포함</li>
     <li>구글시트·엑셀 함께 제공 — 모바일·PC 어디서나</li>
    </ul>
    <a class="kx-pickcta" href="/kit-842c">자세히 보기 <i aria-hidden="true">→</i></a>
   </div>
  </div>
  <div class="kx-pickuse">
   <div class="kx-ustep"><b>1</b><h4>받기</h4><p>결제하면 파일을 바로 받아요. 회원가입 없이도 가능해요.</p></div>
   <div class="kx-ustep"><b>2</b><h4>함께 펴기</h4><p>구글시트·엑셀을 열어 부부가 같이 채워요.</p></div>
   <div class="kx-ustep"><b>3</b><h4>오늘부터</h4><p>가이드대로 숫자만 넣으면 이번 달 가계부가 완성돼요.</p></div>
  </div>
 </div>
</section>
 """

# ---------- band B: 후기 ----------
REV = r"""<section class="kx-mband" aria-label="후기">
 <div class="kx-mbandin">
  <div class="kx-mhead">
   <span class="kx-meyebrow">★ 먼저 써본 부부들</span>
   <h2 class="kx-mh2">먼저 써본 부부들의 한마디 <small>(예시)</small></h2>
   <p class="kx-mdesc">실제 후기가 쌓이면 이 자리에 그대로 보여드릴게요.</p>
  </div>
  <div class="kx-vgrid">
   <div class="kx-vcard"><div class="kx-vstars">★★★★★</div><p class="kx-vtxt">결제하자마자 받아서 그날 저녁에 가계부를 채웠어요. 숫자만 넣으면 끝이라 편했어요.</p><div class="kx-vwho"><span class="kx-vav" style="background:var(--rose)">김</span><span class="kx-vnm">김OO<small>결혼 1년차</small></span></div></div>
   <div class="kx-vcard"><div class="kx-vstars">★★★★★</div><p class="kx-vtxt">통장 쪼개기를 시트로 보니 확 이해됐어요. 둘이 같이 채우니 돈 얘기가 자연스러워졌고요.</p><div class="kx-vwho"><span class="kx-vav" style="background:var(--sage)">이</span><span class="kx-vnm">이OO<small>예비부부</small></span></div></div>
   <div class="kx-vcard"><div class="kx-vstars">★★★★☆</div><p class="kx-vtxt">엑셀이랑 구글시트 둘 다 줘서 폰으로도 편했어요. 가이드도 친절했고요.</p><div class="kx-vwho"><span class="kx-vav" style="background:var(--lav)">박</span><span class="kx-vnm">박OO<small>결혼 2년차</small></span></div></div>
  </div>
 </div>
</section>
 """

# ---------- band C: 함께 보면 좋아요 (cross-sell + 구독 CTA) ----------
CROSS = r"""<section class="kx-mband" aria-label="함께 보면 좋아요">
 <div class="kx-mbandin">
  <div class="kx-mhead">
   <span class="kx-meyebrow">✦ 함께 보면 좋아요</span>
   <h2 class="kx-mh2">함께 두면 더 잘 굴러가요</h2>
   <p class="kx-mdesc">키트는 거들 뿐, 시작은 오늘 한 줄이에요. 머니레터를 중심으로 도구와 강의가 서로를 거들어요.</p>
  </div>
  <div class="kx-mgrid">
   <a class="kx-mcard" href="/letter-evening"><div class="kx-mico" style="background:linear-gradient(150deg,#E8899A,#C75E70)"><svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.6 6.6 12 13l8.4-6.4"/></svg></div><h4>매일 머니레터</h4><p>아침·저녁으로 시장과 인사이트를 부부의 언어로 정리해 드려요.</p><span class="kx-mkicker">오늘의 머니레터 <i aria-hidden="true">→</i></span></a>
   <a class="kx-mcard" href="/goods-9972"><div class="kx-mico" style="background:linear-gradient(150deg,#D98AA0,#B85060)"><svg viewBox="0 0 24 24"><rect x="4" y="3" width="14.5" height="18" rx="2"/><path d="M4 8h14.5"/><path d="M8 13h7M8 16.5h5"/></svg></div><h4>머니 굿즈</h4><p>눈에 보이는 곳에 두면 습관이 되는 다이어리·플래너예요.</p><span class="kx-mkicker">굿즈 보기 <i aria-hidden="true">→</i></span></a>
   <a class="kx-mcard" href="/class-b779"><div class="kx-mico" style="background:linear-gradient(150deg,#A982B5,#7E5790)"><svg viewBox="0 0 24 24"><path d="M12 4l9.5 5L12 14 2.5 9 12 4z"/><path d="M6 11v4.2c0 1.6 2.7 3 6 3s6-1.4 6-3V11"/></svg></div><h4>재테크 클래스</h4><p>둘이 같이 들어 끝까지 가는 입문 과정이에요.</p><span class="kx-mkicker">강의 보기 <i aria-hidden="true">→</i></span></a>
  </div>
  <div class="kx-msub"><a href="/home#subscribe">함께 시작하기 <i aria-hidden="true">→</i></a></div>
 </div>
</section>
 """

# ================= transform contents-kits =================
with open(CK, encoding="utf-8") as f:
    s = f.read()
orig = s

# 1) remove ALL html comments (gate ⑤: '<!--' 0)
s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
s = s.lstrip("\n")

# 2) CSS insert before first </style>
assert s.count("</style>") >= 1
s = s.replace("</style>", CSS + "</style>", 1)

# 3) header: move active 콘텐츠->키트 + kit href -> /contents-kits
HDR_OLD = '<a href="/moneyletter-landing">머니레터</a><a href="/contents" class="cur">콘텐츠</a><a href="/kit-bcaf">키트</a><a href="/goods-9972">굿즈</a><a href="/class-b779">강의</a>'
HDR_NEW = '<a href="/moneyletter-landing">머니레터</a><a href="/contents">콘텐츠</a><a href="/contents-kits" class="cur">키트</a><a href="/goods-9972">굿즈</a><a href="/class-b779">강의</a>'
assert s.count(HDR_OLD) == 1, "header anchor not unique/found"
s = s.replace(HDR_OLD, HDR_NEW, 1)

# 4) insert PICK band before kx-controls (after introwrap)
A1 = '<div class="kx-controls">'
assert s.count(A1) == 1
s = s.replace(A1, PICK + A1, 1)

# 5) insert REVIEWS + CROSS before premium band (after </main>)
A2 = '<section class="kx-band" aria-label="프리미엄 안내">'
assert s.count(A2) == 1
s = s.replace(A2, REV + CROSS + A2, 1)

# 6) sweep remaining /kit-bcaf in this file (footer nav) -> /contents-kits
nk = s.count('href="/kit-bcaf"')
s = s.replace('href="/kit-bcaf"', 'href="/contents-kits"')

assert s.count('<!--') == 0, "comments remain"
assert s.count('href="/kit-bcaf"') == 0, "kit-bcaf remains in contents-kits"
atomic_write(CK, s)
print("contents-kits: comments->0, header active=키트, footer sweep(%d), bands inserted (pick/rev/cross)" % nk)

# ================= batch nav sweep (all other BODY) =================
changed = ["contents-kits__BODY.html"]
skip = {"kit-bcaf__BODY.html", "contents-kits__BODY.html"}
sweep_total = 0
for p in sorted(glob.glob(os.path.join(CDN, "*__BODY.html"))):
    name = os.path.basename(p)
    if name in skip:
        continue
    with open(p, encoding="utf-8") as f:
        t = f.read()
    c = t.count('href="/kit-bcaf"')
    if c:
        t2 = t.replace('href="/kit-bcaf"', 'href="/contents-kits"')
        atomic_write(p, t2)
        changed.append(name)
        sweep_total += c

print("batch sweep: files=%d, total href replaced=%d" % (len(changed)-1, sweep_total))

# ================= result json =================
slugs = [c[:-len("__BODY.html")] for c in changed]
result = {
  "merged_sections": [
    "대표키트 spotlight(통장쪼개기 가계부 키트 → /kit-842c)",
    "이용안내 3-step(받기·함께 펴기·오늘부터) — pick 밴드 내 통합",
    "후기(먼저 써본 부부들, 예시 3건)",
    "함께 보면 좋아요(머니레터·굿즈·클래스 + 구독 CTA)"
  ],
  "folded_dedup": [
    "히어로 카피: ② kx-hero 유지, ① 히어로는 중복이라 미도입",
    "전체상품 4카드: 전원 /kit-842c 동일링크 → 탐색기+spotlight로 흡수(중복 제거)",
    "종료 CTA(도구는 거들 뿐/→home#subscribe): cross 밴드에 통합, 프리미엄 밴드 1개 유지"
  ],
  "changed": sorted(changed),
  "slugs_to_inject": sorted(slugs)
}
with open("/tmp/bbfb/kit_merge_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print("changed files:", len(changed))
print("result json written")
