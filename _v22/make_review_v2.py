# -*- coding: utf-8 -*-
# 검수판 v2 생성기 — 라이브 BODY+FOOTER 원문 임베드 + 조각/인덱스 b64 자급자족 셔틀
import base64, datetime, sys, re
ROOT='/tmp/bbfb2'
OUT='/sessions/gifted-charming-carson/mnt/홈페이지 찐/재테크_구독서비스_설계/콘텐츠_대개편_기획/_파일럿/검수용_청년적금_칼럼.html'
rd=lambda p: open(p,encoding='utf-8').read()
rb=lambda p: open(p,'rb').read()
body=rd(f'{ROOT}/imweb_cdn/contents__BODY.html')
foot=rd(f'{ROOT}/imweb_cdn/contents__FOOTER.html')
frag_b=rb(f'{ROOT}/contents/columns/bookcol-youthchoice.html')
idx_b=rb(f'{ROOT}/contents/contents_index.json')
leg_b=rb(f'{ROOT}/contents/legacy_index.json')
tool_b=rb(f'{ROOT}/contents/tools/booktool-youthchoice.html')
b64=lambda b: base64.b64encode(b).decode()
KST=datetime.timezone(datetime.timedelta(hours=9))
now=datetime.datetime.now(KST).strftime('%Y-%m-%d %H:%M KST')
REPO='1e8e991'

head='''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>검수용 v2 · 청년도약계좌 vs 청년미래적금 (bookcol-youthchoice)</title>
<style>
/* ===== 검수판 베이스 (라이브 imweb 전역 리셋 대체) ===== */
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:#FDFBF7}
button,input,select{font-family:inherit}
/* ===== 검수 안내 바 (v2: 흐름 배치 — 라이브 고정 헤더와 충돌 방지) ===== */
.rv-bar{position:relative;z-index:1300;display:flex;gap:8px 14px;align-items:center;min-height:42px;padding:8px 16px;background:#3E2F29;color:#F3ECDF;font:700 12.5px/1.45 'Pretendard Variable',Pretendard,sans-serif;overflow-x:auto;white-space:nowrap}
.rv-bar b{color:#FFD9DF;font-weight:800}
.rv-bar .rv-chip{flex:none;display:inline-block;background:#B33A4C;color:#fff;font-weight:800;border-radius:999px;padding:2.5px 10px;font-size:11.5px}
.rv-bar .rv-dim{color:#C9B8AE;font-weight:600}
/* ===== 하단 검수 포인트 ===== */
.rv-points{max-width:var(--cx-read,720px);margin:34px auto 0;padding:22px clamp(22px,4.5vw,40px) 8px;border-top:2px dashed #E4C8C2}
.rv-points h2{font-size:15px;font-weight:900;color:#7C243B;margin:0 0 12px;letter-spacing:-.01em}
.rv-points ol{margin:0;padding:0 0 0 2px;list-style:none;counter-reset:rvp;display:flex;flex-direction:column;gap:9px}
.rv-points li{position:relative;padding:11px 14px 11px 44px;background:#fff;border:1px solid #EAD7D3;border-radius:12px;font-size:13.5px;font-weight:600;color:#5C4B43;line-height:1.62}
.rv-points li::before{counter-increment:rvp;content:counter(rvp);position:absolute;left:12px;top:11px;width:22px;height:22px;border-radius:50%;background:#F8E8EA;color:#B33A4C;font-size:12px;font-weight:900;display:grid;place-items:center}
.rv-points li b{color:#B33A4C;font-weight:800}
.rv-foot{max-width:var(--cx-read,720px);margin:0 auto;padding:14px clamp(22px,4.5vw,40px) 46px;font-size:12px;font-weight:600;color:#8A7B72;line-height:1.6}
/* ===== 토스트 ===== */
.rv-toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(8px);z-index:1500;background:#3E2F29;color:#fff;font:700 13px/1.5 'Pretendard Variable',Pretendard,sans-serif;padding:11px 17px;border-radius:999px;box-shadow:0 12px 30px rgba(62,47,41,.25);opacity:0;visibility:hidden;transition:all .22s ease;max-width:88vw;text-align:center}
.rv-toast.on{opacity:1;visibility:visible;transform:translateX(-50%) translateY(0)}
</style>
</head>
<body>
'''

rvbar=f'''<div class="rv-bar"><span class="rv-chip">파일럿 검수용 v2</span><b>청년적금 칼럼 · bookcol-youthchoice</b><span>라이브 플랫폼(BODY+FOOTER 원문) 그대로 담은 단일 파일 — 라이브 아님</span><span class="rv-dim">작성 {now} · repo {REPO} · 새 스킨·레일·시각화 반영판</span></div>
'''

points='''<section class="rv-points"><h2>🔍 검수 포인트 6 (v2)</h2><ol>
<li><b>새 시각화 실동작</b> — 큰 숫자 카드(자산 증감 −0.3% 카운트업), 꺾은선 3종(기준금리·2인가구 기준중위소득·도약계좌 중도해지율), 막대·구성 차트 5개, 근거 카드 5장(신문 스크랩 결), 슬라이더 계산기를 직접 조작해봐 주세요. <b>(발견 사항)</b> 슬라이더의 '결과' 칸이 지금은 납입액 숫자를 그대로 되비추는 상태예요 — mirae_maturity 계산식이 시뮬레이터(SIM) 쪽에만 등록되고 슬라이더용 calc 레지스트리엔 미배선이라, 유형별 예상액 배선 보강이 필요해요. 정확한 예상액은 바로 아래 시뮬레이터 카드(우대 2,255·일반 2,138·비과세 2,021만원)가 정답 기준이에요.</li>
<li><b>리더 스킨 v2</b> — 챕터 배지 그라디언트·카드 스타일·타이포 사다리가 홈과 같은 결(라이브 토큰 원문 내장)로 느껴지는지 봐주세요.</li>
<li><b>우측 스티키 레일</b> — 브라우저 창을 1400px 이상으로 넓히면 오른쪽에 '지금 챕터·용어 칩·내 계산 결과' 레일이 떠요. 스크롤 따라 챕터가 갱신되는지 확인해 주세요.</li>
<li><b>본문 문단 재편집</b> — 짧은 문단을 맥락으로 병합(568→156문단)했어요. 읽는 호흡이 자연스러운지, 뚝뚝 끊기는 곳이 남았는지 봐주세요.</li>
<li><b>숫자·기준일 검수</b> — 기준일 2026-07 표기, 중도해지율 확정치, 금리(기본 5%+우대)·기여율(일반 6%·우대 12%)·한도(월 50/70만원)·일정(2026.12 잠정 모집)이 본문·차트·계산기에서 서로 어긋나지 않는지 봐주세요.</li>
<li><b>기존 위젯 유지</b> — 진단 트리(12경로)·시뮬레이터·비교표·캡처 스텝 8장·용어칩 11개·체크리스트는 그대로 실동작해요. 저장하기(이미지·PDF)는 인터넷 연결 시에만, 다른 콘텐츠로 이동은 라이브에서만 동작해요(안내 토스트).</li>
</ol></section>
<div class="rv-foot">이 파일은 bubulab-site@REPOHASH 기준 검수용 단일 HTML 사본이에요. 라이브 /contents 위젯의 BODY·FOOTER 원문을 그대로 담고, 칼럼 조각·인덱스를 내장해 오프라인에서도 글과 위젯 동작을 확인할 수 있어요. 외부 로드는 Pretendard 폰트·캡처 이미지(raw.githubusercontent.com)·저장하기 라이브러리(cdnjs)뿐이에요.</div>
'''.replace('REPOHASH','1e8e991')

shim='''<script>
/* ===== 검수판 v2 셔틀 — 라이브 fetch 가로채기(조각·인덱스 내장, 자급자족) ===== */
(function(){
 var B64={frag:'__FRAG__',idx:'__IDX__',leg:'__LEG__',tool:'__TOOL__'};
 function dec(b){var bin=atob(b),u=new Uint8Array(bin.length);for(var i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);return new TextDecoder('utf-8').decode(u);}
 var MAP=[
  ['contents/columns/bookcol-youthchoice.html',function(){return [dec(B64.frag),'text/html;charset=utf-8'];}],
  ['contents/tools/booktool-youthchoice.html',function(){return [dec(B64.tool),'text/html;charset=utf-8'];}],
  ['contents/contents_index.json',function(){return [dec(B64.idx),'application/json'];}],
  ['contents/legacy_index.json',function(){return [dec(B64.leg),'application/json'];}]
 ];
 var STUB='<div class="cx-tx"><p>검수용 사본이에요 — 이 콘텐츠는 라이브(bubulab.co.kr/contents)에서 열려요.</p></div>';
 var orig=window.fetch?window.fetch.bind(window):null;
 window.fetch=function(url,opt){
  var u=String(url&&url.url?url.url:url);
  for(var i=0;i<MAP.length;i++){if(u.indexOf(MAP[i][0])>=0){var r=MAP[i][1]();return Promise.resolve(new Response(r[0],{status:200,headers:{'Content-Type':r[1]}}));}}
  if(u.indexOf('/contents/columns/')>=0||u.indexOf('/contents/tools/')>=0){return Promise.resolve(new Response(STUB,{status:200,headers:{'Content-Type':'text/html;charset=utf-8'}}));}
  if(orig)return orig(url,opt);
  return Promise.reject(new Error('rv-offline'));
 };
 try{if(!location.hash)location.hash='#bookcol-youthchoice';}catch(e){}
})();
</script>
'''

tail='''<script>
/* ===== 검수판 v2 — 사이트 내부 링크 안내 토스트 ===== */
(function(){
 var t=document.createElement('div');t.className='rv-toast';document.body.appendChild(t);var tm=null;
 function toast(m){t.textContent=m;t.classList.add('on');clearTimeout(tm);tm=setTimeout(function(){t.classList.remove('on');},2600);}
 document.addEventListener('click',function(e){
  var a=e.target&&e.target.closest?e.target.closest('a[href]'):null;if(!a)return;
  var h=a.getAttribute('href')||'';
  if(h.charAt(0)==='/'||/^https?:\\/\\/(www\\.)?bubulab\\.co\\.kr/.test(h)){e.preventDefault();e.stopPropagation();toast('검수용 사본이에요 — 사이트 이동은 라이브(bubulab.co.kr)에서 동작해요');}
 },true);
})();
</script>
</body>
</html>
'''

shim=shim.replace('__FRAG__',b64(frag_b)).replace('__IDX__',b64(idx_b)).replace('__LEG__',b64(leg_b)).replace('__TOOL__',b64(tool_b))
html=head+rvbar+body+'\n'+points+shim+foot+tail
open(OUT,'w',encoding='utf-8').write(html)

# ===== 게이트 =====
out=rd(OUT)
g={}
g['size']=len(out.encode('utf-8'))
g['sh']=out.count('stat-hero');g['rr']=out.count('cx-rrail')
g['scriptOpen']=len(re.findall(r'<script[ >]',out));g['scriptClose']=out.count('</script>')
g['shimBeforeFoot']=out.find('rv-offline')<out.find("__cxhub")
g['b64ok']=base64.b64encode(frag_b).decode() in out
import json;print(json.dumps(g,ensure_ascii=False))
