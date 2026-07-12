# -*- coding: utf-8 -*-
import json, os, tempfile, hashlib, datetime

MD_PATH  = "/sessions/gifted-charming-carson/mnt/홈페이지 찐/재테크_구독서비스_설계/책연계_콘텐츠_기획/_퀄리티500_기획_v1.md"
JSON_PATH= "/tmp/bbfb/quality500_plan.json"

def atomic_write(path, data):
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp_", suffix=".part")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp): os.remove(tmp)

# ---------------- COLUMN PRESCRIPTIONS (D) ----------------
COLS = [
 ("bookcol-01","가만히 있으면 녹아내리는 내 돈","keep",False,8,
   "구매력 슬라이더+비교탭 이미 탑재(모범 기준). 카운트업 절제 양호.",
   "슬라이더 값→내 월급 대입 입력칸 1개 추가(개인화 후킹). 마무리 '사랑의 실천' 문장은 본문 유지하되 리더 추가 맺음말 금지.",
   "이미 data-cx-sc 신형. 위젯 라이브러리 표준 레퍼런스로 승격."),
 ("bookcol-02","7% 적금과 월 30만원의 비밀","gather",True,7,
   "'7%'+'비밀' 숫자·호기심 훅 강함. 도입 티저 문장 리듬 좋음.",
   "티저에 reveal-steps(구조 3단계) 1개 미리보기. 게이트 위 '무료 계산 맛보기'로 savingrule 도구 임베드.",
   "PREMIUM_GATE 위 도입만 노출. 게이트 직전 counter-bar로 '월30→태산' 시각 훅 1개."),
 ("bookcol-03","나는 멋진 할머니가 되고 싶어, 당신은?","gather",True,8,
   "정체성·부부 지향 훅 매우 차별적. 감정 진입점 우수.",
   "checklist 위젯으로 '우리가 되고 싶은 노년' 3문 셀프체크(공유형). 만다라트 도구 딥링크.",
   "리드+첫섹션 무료. 티저에 quiz 1문(가벼운 자기발견)로 스크롤 유인."),
 ("bookcol-04","5년만 미뤄도, 이만큼 벌어져요","keep",False,8,
   "손실회피 훅 강력. 은퇴자산 막대 비교 시각화 보유.",
   "정적 cx-bar→slider 위젯(미룬 햇수 0~10년→격차 실시간). counter-bar로 격차액 카운트업(성장지표 허용).",
   "구형 cx-doc→신형 data-cx-sc 마이그레이션(통일 1순위)."),
 ("bookcol-05","몰빵의 반대말을 아세요?","keep",True,7,
   "질문형 훅+반대말 호기심 좋음. 분산 개념 명확.",
   "compare 위젯(몰빵 vs 분산 최악의 해). reveal-steps로 분산 3원칙 단계 공개.",
   "리드+첫섹션 무료. 도넛형 배분 미니 시각화 1개(포트폴리오 도구 티저)."),
 ("bookcol-06","안전한 투자는 없다던데,,","keep",True,6,
   "',,' 보이스 살아있음. 위기 생존 프레임 매력.",
   "금리↔자산 seesaw 인터랙션(slider: 금리↑→무엇이 춤추나). 초심자 3문 '왜 나에게' 콜드오픈 리드 보강.",
   "헷지·금리 난도 높음→비유(시소·우산) 먼저, 용어는 뒤. tabs로 상승기/하락기 분리."),
 ("bookcol-07","인구 줄면 집값 떨어지는 거 아니야?","keep",False,8,
   "통념반박 훅 클릭률 높음. 내집마련 보편성. 표 데이터 보유.",
   "정적 table→compare/tabs 위젯(지역·연령 시나리오 전환). 지도형 미니 인포그래픽 1개.",
   "전문 공개 무료의 강점 살려 상단에 '3줄 결론' 요약 박스 추가."),
 ("bookcol-08","절세계좌, 언제 써야 진짜 이득일까","keep",True,6,
   "'타이밍이 절반' 실용 훅. 실생활 밀착.",
   "세 계좌 compare 탭(연금/ISA/IRP 빛나는 순간). reveal-steps로 소득구간별 우선순위.",
   "'절세계좌'가 낯선 독자용 한 줄 정의 리드 선행. taxaccount 도구 임베드."),
 ("bookcol-09","2천만 원의 벽 앞에서","grow",True,6,
   "'2천만 원의 벽' 서사 장치 흥미. 배당 수익화 매력.",
   "counter-bar 게이지(내 이자·배당→2천만 벽 근접도). quiz 1문 '나는 벽에 얼마나?'.",
   "금융소득종합과세 맥락 3줄 선설명 필요. finincome 도구 딥링크 강화."),
 ("bookcol-10","'싸다'는 감정의 실체","keep",True,6,
   "철학적·차별적 훅. '감정의 실체' 카피 좋음.",
   "quiz 위젯(두 종목 지표 제시→'싸다/비싸다' 맞히기). compare로 PER/PBR/ROE 나란히.",
   "가치평가 난도 완화: 저울 비유 시각화 먼저. valuation 도구 연결."),
 ("bookcol-11","우리 부부만의 포트폴리오는 왜 달라야 할까","keep",True,7,
   "부부 개인화·온브랜드 훅. '남의 정답 아님' 공감.",
   "slider 위젯(나이·자녀·소득→배분 실시간 변화). compare(신혼 vs 자녀家 예시).",
   "리드+첫섹션 무료. portfolio 도구를 본문 임베드(체험형)."),
 ("bookcol-12","월급 밖에서 돈이 들어오게 하라","grow",False,8,
   "월급 밖·낮은 문턱(공모주) 훅 강함. 열망 자극.",
   "checklist(파이프라인 5종 셀프체크). reveal-steps로 공모주 첫 청약 절차.",
   "전문 공개 강점. counter-bar로 '파이프라인 개수→현금흐름' 시각 훅."),
]

# ---------------- TOOLS (F) ----------------
TOOLS = [
 ("booktool-mandala","우리 목표 만다라트","present",
  "저장 게이트 유지·양호. 81칸 자동 배치·포커스 모드 UX 유지. 완성 시 공유 이미지에 브랜드 로고·부부 이름 각인 추가."),
 ("booktool-flexcost","새는 돈 진단기","MISSING",
  "HTML 미제작(인덱스만 존재)—신규 빌드 필요. 고정·변동 분리 도넛+'새는 항목 top3' 결과 카드. 무료."),
 ("booktool-savingrule","우리 집 적금·절약 규칙 메이커","present",
  "역산 UX 좋음. 슬라이더-숫자 동기화 유지. 결과에 '월 규칙 카드' 저장/공유 1개 추가. 통일 네임스페이스로 이관."),
 ("booktool-portfolio","부부 포트폴리오 배분기","MISSING",
  "HTML 미제작—신규 빌드. 인원·소득→도넛 배분+'우리집 한 줄 코멘트'. 간이 무료·정밀 게이트."),
 ("booktool-taxaccount","절세계좌 3형제 시뮬레이터","MISSING",
  "HTML 미제작—신규 빌드. 연금/ISA/IRP 배분 슬라이더→절세액 나란히 막대. 미리보기 무료·정밀 게이트."),
 ("booktool-finincome","금융소득종합과세 가늠기","present",
  "게이지 UX 좋음. 2천만 벽 근접도 시각화 유지. 하이드레이션 대상 값 없음 확인(정적 세율 주석 최신화)."),
 ("booktool-valuation","가치평가 첫걸음","MISSING",
  "HTML 미제작—신규 빌드. PER·PBR·ROE 입력→'싸다/보통/비싸다' 신호등+또래 비교. 미리보기 무료·정밀 게이트."),
]

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

# ---------------- MARKDOWN ----------------
def col_table():
    rows=["| # | 제목 | 존 | 유료 | 후킹 | 추가할 인터랙티브/시각화 | 뺄 것·구성 개선 |",
          "|---|------|----|----|----|------------------------|----------------|"]
    for i,(slug,title,zone,prem,score,good,add,rm) in enumerate(COLS,1):
        z={"gather":"모으기","keep":"지키기","grow":"불리기"}[zone]
        p="유료" if prem else "무료"
        rows.append(f"| {i:02d} | {title} | {z} | {p} | **{score}/10** | {add} | {rm} |")
    return "\n".join(rows)

def tool_lines():
    out=[]
    for slug,title,st,fix in TOOLS:
        flag=" ⚠️미제작" if st=="MISSING" else ""
        out.append(f"- **{title}** (`{slug}`){flag} — {fix}")
    return "\n".join(out)

MD = f"""# 퀄리티 500% 실행 기획 v1 — 부부연구소 콘텐츠 시스템

작성: 콘텐츠 총괄 크리에이티브 디렉터 · {now} · 감사대상 29건(칼럼12·도구7·키트10)+콘텐츠 허브
기준선: 홈 디자인 토큰(어우러짐) · 디자인텍스트 컨센서스 v1.2 · 초심자 3문(필요한가·위치·WOW)

> 한 줄 총평: 보이스·정보설계·허브 골격은 이미 상위 10%. 그러나 (1)리더 인터랙티브가 칼럼1편에만 완성 (2)구·신 마크업 2세대 혼재 (3)도구 7종 중 4종 미제작 (4)허브 은유가 '지도'에 멈춰 '성장·개화'의 정서적 폭발이 없음. 500%는 신규 제작이 아니라 **통일·위젯화·개화 리뉴얼**로 달성한다.

---

## A. 전역 진단 (잘된 것 3 / 아쉬운 것 5+)

### A-1. 리더(칼럼) — contents-columns__BODY + bookcol-01~12
**잘된 것**
1. 보이스 최상급: ',,' ':)' 'ㅎㅎ' 회고체, '구조와 환경', 코칭체(명령형+안심)가 원문 순도로 살아있음.
2. bookcol-01이 신형 리더의 완성형 레퍼런스(구매력 슬라이더+비교탭+카운트업+용어 툴팁+체크리스트)를 이미 보유.
3. 필터·정렬 칩, 프리미엄 게이트(PREMIUM_GATE+blur+접근권 프레임)가 컨센서스(무료 먼저)와 정합.

**아쉬운 것 (근거)**
1. **마크업 2세대 혼재**: 01은 신형(`data-cx-sc`/`cx-rd-*`), 04·07·12는 구형(`cx-doc`/`cx-h2`+인라인 style). 리더가 위젯을 배선하는 대상이 01뿐 → 나머지 11편은 정적. (grep: cx-erode 참조 11, 그러나 전부 01 소속)
2. **인터랙티브 편중**: 실제 동작 위젯 보유 칼럼은 01(슬라이더·탭). 04는 막대가 정적(style width 하드코딩), 07은 정적 table. 나머지는 텍스트+툴팁뿐.
3. **선언형 위젯 부재**: 위젯이 `data-cx-erode`/`data-cx-compare`처럼 종류별 하드코딩. 조각이 `data-cx-w="..."`로 선언하면 라우터가 배선하는 범용 계약이 없음 → 확장·재사용 불가.
4. **프리미엄 티저 과소**: 02·03·05·06 조각이 1.5~2.5KB로 게이트 전 '무료 가치'가 얇음. C0(이어서 보기: 무료 관련글4+티저) 패턴 미적용.
5. **콜드오픈 훅 약화 구간**: 06·08·09·10은 헷지/절세계좌/종합과세/가치평가 등 난도 높은 명사로 진입 → 처음 온 독자에 '왜 나에게 필요한가'(초심자 3문) 선설명 부재.
6. **타이포 리듬 잔여**: 구형 조각은 문단 3문장+ 덩어리 존재(L8 위반 소지), 강조 스팬 이음새 공백(L9)·헤드라인 의미단위 줄나눔(L10) 렌더 검수 미완.

### A-2. 키트 — contents-kits__BODY + kits/*/kit.json(82스텝)
**잘된 것**
1. kit.json 스키마 성숙(why/outcome/audience/steps free플래그) → 데이터 주도 렌더 가능.
2. step00 프롤로그가 서사 원전(반지하·버섯·완주 초대)과 정합, 무료 개방으로 진입장벽 낮음.
3. 커머스 단건(P4)·개별 구매 프레임이 허브 카피와 일치, 문제기반 태그(problem) 명확.

**아쉬운 것**
1. **완주 모멘텀 부재**: localStorage 진행저장·완주 축하 메커니즘 없음(grep: localStorage 0). 8~10스텝 완주 동기가 배지 정적 노출뿐.
2. **커리큘럼 시각화 없음**: 스텝이 목록/타일 나열. '어디까지 왔고 몇 걸음 남았나'의 여정감(허브 은유와 연동) 미구현.
3. **kx-soon 다수(12)**: 일부 스텝이 '준비 중' 노출 소지 → F1(미확정/준비중 노출 금지) 저촉 위험.
4. **스텝 뷰 동작 빈약**: 스텝 내 인터랙션(대화 카드 뒤집기·입력·체크)이 리더 위젯과 분리(kx- 독자 네임스페이스) → 위젯 라이브러리 재사용 불가.
5. **허브-키트 시각 불일치**: 키트 카드 배지/톤이 홈 토큰과 부분 이탈(자체 kx- 팔레트). 여백 L7 기본값 미적용 구간.

### A-3. 도구 — tools/*.html (booktool 7종 중 3종만 실재)
**잘된 것**
1. 실재 3종(mandala·savingrule·finincome)의 슬라이더-숫자 동기화·프리셋 UX 견고.
2. 입력값 기기 저장·서버 미전송 원칙(푸터 고지)으로 신뢰·프라이버시 확보.
3. 저장/정밀 게이트가 무료-유료 경계와 정합(간이 무료·정밀 게이트).

**아쉬운 것**
1. **4종 미제작**: flexcost·portfolio·taxaccount·valuation 이 인덱스·허브 노드엔 live=1로 노출되나 tools/에 HTML 없음 → 링크 도달 시 공백/깨짐 위험(치명).
2. **네임스페이스 파편화**: tx·tx2·tx3… 도구마다 독자 접두사 → 공통 계산·렌더 코어 부재, 유지보수 취약.
3. **결과 공유 자산 약함**: 결과를 부부가 저장/공유할 카드(브랜드 각인)가 mandala 외 미흡 → 바이럴 훅 상실.
4. **홈 토큰 이탈**: 도구별 인라인 style이 자체 색·라운드 사용 → 계열 통일 필요.
5. **하이드레이션 점검 미완**: 정적 세율·가정치 주석이 L2/X3(정적 하드코딩 금지) 관점 재검 필요.

### A-4. 허브 — contents-hub__BODY (여정 지도)
**잘된 것**
1. S-곡선 경로+29노드+3존 밴드(모으기·지키기·불리기)+호버 팝업으로 이미 인터랙티브 지도 완성.
2. jmSnap(29) 임베드·데이터 주도, 존별 카운트·필터칩·목록 폴백까지 갖춘 정보설계.
3. 경로 그라디언트(sage→rose→gold)·pulse·reveal가 홈 모션 어휘와 정합, 시작🏠·끝💗 서사 수미상관.

**아쉬운 것**
1. **은유가 '지도'에 정지**: 사용자가 원한 '줄기 위 새싹→꽃봉오리→만개 개화'의 성장 서사가 없음. 노드가 혼합 이모지(🧊⏳🧺…)라 한눈에 종류·성장단계가 안 읽힘.
2. **개화·계절 애니메이션 부재**: 노드 등장이 단순 pulse. SVG 꽃잎 전개·호버 만개·계절 배경 전이 없음(사용자 명시 요구).
3. **성장 지표화 안 됨**: 방문/완주에 따라 길이 '피어나는' 진행 저장 없음(허브·키트 공통 localStorage 부재).
4. **모바일 세로 경로 과장**: viewBox 1000x4150 → 소형 화면 스크롤 부담·라벨 겹침 소지.
5. **레전드 은유 혼선**: 잎=칼럼/연장=도구/이정표=키트인데 노드 이모지는 품목별이라 레전드와 시각 언어 불일치.
6. **히어로 훅 여지**: 카피는 좋으나 '개화·돈나무' 정서로 끌어올릴 여지(첫인상 후킹 강화).

---

## B. 디자인 시스템 통일안 (홈 토큰 → 콘텐츠 계열 적용)

홈 `home__BODY`의 :root를 추출해 콘텐츠 계열 공통 변수 `--cx-*`로 재선언한다. 리더·키트·허브·도구 4계열의 `<style>` 헤드에 동일 블록을 주입(단일 소스).

### B-1. 컬러 토큰 (홈 추출값 그대로)
```
--cx-bg:#FDFBF7; --cx-bg2:#FBF3EE; --cx-card:#FFFFFF;
--cx-ink:#3E2F29; --cx-ink2:#5C4B43; --cx-mut:#8A7B72; --cx-border:#EAD7D3;
--cx-rose:#B33A4C;   /* 키컬러(로고 계열) */  --cx-rose2:#B85060;
--cx-deep:#7C243B; --cx-pink:#D67A89; --cx-pinkSoft:#F8E8EA; --cx-pinkSoft2:#FCEEF1;
--cx-sage:#5E8C7F;  --cx-gold:#C9A84C;  --cx-lav:#9C6BA8;  --cx-sand:#F0DED8;
--cx-up:#D8584E; --cx-down:#4A7DE8;    /* 등락 전용 */
```
금지(컨센서스 X4/V0): 다크 밴드·순검정(#000)·보라 주조·형광. 강조는 rose·pink 계열로.

### B-2. 성장·계절 토큰 (허브·키트 공용, 신설)
```
--cx-seed:#7FB08A;   /* 새싹 연둣빛 (모으기·봄) */
--cx-bud:#E08696;    /* 꽃봉오리 로즈핑크 (지키기·초여름) */
--cx-bloom:#B33A4C;  /* 만개 로즈 (불리기·결실) */
--cx-pollen:#C9A84C; /* 꽃가루·씨앗 골드 */
--cx-zone-gather:rgba(94,140,127,.10);
--cx-zone-keep:rgba(179,58,76,.08);
--cx-zone-grow:rgba(201,168,76,.13);   /* 기존 밴드 틴트 재사용 */
```

### B-3. 타이포 스케일 (홈 clamp 사다리 정규화, Pretendard Variable)
```
--cx-fs-cap:clamp(12px,1.4vw,13px);    /* 캡션·주석 */
--cx-fs-body:clamp(15px,1.6vw,17px);   /* 본문 기본 */
--cx-fs-lead:clamp(17px,2vw,19.5px);   /* 리드 */
--cx-fs-h3:clamp(18px,2.3vw,23px);
--cx-fs-h2:clamp(23px,3.4vw,34px);     /* 섹션 헤드 */
--cx-fs-h1:clamp(27px,4vw,42px);       /* 콘텐츠 타이틀 */
--cx-fs-hero:clamp(34px,5.4vw,68px);   /* 허브 히어로 */
line-height 본문 1.75 · 헤드 1.3 · letter-spacing 헤드 -0.02em
```
규칙: 카드 타이틀 1줄(L11) · 리드 max-width+가운데정렬(L12) · 강조 스팬 앞뒤 공백(L9) · 헤드라인 의미단위 `<br>`(L10) · 문단 1~2문장(L8).

### B-4. 여백·라운드·그림자
```
--cx-r:22px; --cx-r-sm:14px; --cx-maxw:1180px; --cx-read:720px; /* 읽기 폭 */
--cx-pad-sec:clamp(120px,13vw,192px);  --cx-pad-hero:clamp(44px,6vw,84px);  --cx-pad-x:clamp(22px,4.5vw,40px);
--cx-sh:0 1px 2px rgba(62,47,41,.04),0 4px 10px rgba(190,80,96,.05),0 14px 30px rgba(190,80,96,.07);
--cx-shi:0 2px 4px rgba(62,47,41,.05),0 12px 24px rgba(190,80,96,.10),0 28px 56px rgba(190,80,96,.15);
```
섹션 상하 여백 대칭(L1), 등분 그리드(L6).

### B-5. 모션 규칙
```
--cx-ease:cubic-bezier(.16,1,.3,1);
--cx-dur:.6s;  reveal: IntersectionObserver로 .cx-in 토글(홈 .reveal 패턴 이식)
```
- 카운트업(.cnt)은 성장·중립 지표에만(누적 편수·격차액·파이프라인 개수). 서사 스탯 카드엔 금지(V2/B11).
- 개화·꽃잎·드리프트는 홈 keyframes(bob/drift/shimmer/pulse) 어휘 재사용, 절제.
- prefers-reduced-motion: 개화·드리프트 정지, 최종상태 노출.

---

## C. 리더 위젯 라이브러리 스펙 (선언형 `data-cx-w`)

원칙: **조각은 마크업으로 선언만, 배선은 리더 라우터가 담당.** 리더 `<script>`에 단일 라우터 `CXW.mount(root)` 탑재 → `root.querySelectorAll('[data-cx-w]')` 순회하며 `data-cx-w` 값으로 위젯 초기화. 값·계산은 `data-*`로 선언, 입력은 기기 저장(서버 미전송). 접근성: role/aria, 키보드 조작, reduced-motion 폴백 필수. 기존 01의 erode/compare/count/term/pull/check를 이 계약으로 흡수.

공통 계약
- 컨테이너: `<div data-cx-w="TYPE" ...옵션 data->`
- 초기화 표식: 배선 후 `data-cx-ready="1"` 부여(중복 mount 방지)
- 스타일 훅: `.cxw` 베이스 + `.cxw-TYPE`
- 실패 안전: JS 미로드/실패 시 마크업만으로 정적 의미 성립(progressive enhancement)

| data-cx-w | 용도 | 핵심 마크업 계약 | 동작 |
|-----------|------|------------------|------|
| `slider` | 변수 1개→결과 실시간 | `[data-cx-w=slider][data-min][data-max][data-step][data-unit]` 내부 `<input type=range>` + `[data-out]` 표시 노드 + 선택 `[data-formula]`(내장 프리셋: erode/compound/gap) | range 입력→포뮬러 계산→`[data-out]` 갱신, 채움 바 `[data-fill]` width%, 눈금 라벨 |
| `tabs` | 시나리오/기간 전환 | `[data-cx-w=tabs]` > `[role=tablist]` 버튼 `[data-tab=key]` + 패널 `[data-panel=key]` | 버튼 클릭→해당 패널 노출, aria-selected 토글, 좌우 키 이동 |
| `quiz` | 자기발견·정답 맞히기 | `[data-cx-w=quiz]` > `[data-q]` 문항 > 보기 `<button data-opt data-correct?>` + `[data-feedback]` | 선택→정답/해설 노출, 점수 집계, 마지막 결과 카드(공유용), 오답 재시도 |
| `reveal-steps` | 단계 순차 공개 | `[data-cx-w=reveal-steps]` > `<li data-step>` + 다음 버튼 `[data-next]` | 클릭/스크롤로 다음 스텝 페이드인, 진행 점 표시, 완료 시 요약 |
| `counter-bar` | 성장·근접도 게이지 | `[data-cx-w=counter-bar][data-to][data-goal?][data-unit]` + `[data-num]` + `[data-track]` | in-view 시 0→to 카운트업(성장지표 한정), goal 대비 근접% 바, 임계선 마커 |
| `compare` | A/B 나란히 대조 | `[data-cx-w=compare]` > 2×`[data-side]` (kind/num/sub) + 선택 `[data-cmp-tabs]` 연동 | 탭·토글로 두 카드 수치 동시 갱신, 우열 색(rose/sage) |
| `checklist` | 셀프체크·공유 | `[data-cx-w=checklist]` > `<label><input type=checkbox data-chk>` + `[data-count]` | 체크 수 집계·저장(localStorage), 전체완료 시 축하·공유 카드, '내 결과 저장' |

부가 인라인 훅(위젯 아님, 라우터가 함께 처리)
- `.cx-term[data-tip]` 용어 회색 음영 호버 툴팁(컨센서스 시드) — 키보드 focus 대응.
- `.cx-count[data-to][data-suffix]` 성장 카운트업(counter-bar 미니 버전).
- `.cx-pull` 인용 강조 / `.cx-hl` 형광 아닌 밑줄·굵기 강조(rose).

라우터 배치: `contents-columns__BODY`(리더)·`contents-kits__BODY`(스텝 뷰) 양쪽에서 동일 `CXW` 로드 → 칼럼·키트 스텝 공용. 도구는 `CXW.calc` 코어(포뮬러 레지스트리) 공유로 tx/tx2/tx3 네임스페이스 통합.

---

## D. 칼럼 12편 후킹 점수 + 개선 처방

평균 후킹 **7.0/10** — 훅 카피·보이스는 강함, 병목은 '인터랙티브 편중·구신 혼재·난도 콜드오픈'. 처방은 편당 인터랙티브 1~2개 + 통일.

{col_table()}

공통 처방(전편)
- 구형(04·07·12 등)→신형 `data-cx-sc`/`cx-rd-*` 마크업 통일, 위젯은 `data-cx-w`로 선언.
- 난도 높은 4편(06·08·09·10): 리드 첫 문단에 '왜 지금 나에게'(초심자 3문) 콜드오픈 + 비유 시각화 선행.
- 프리미엄 티저(02·03·05·06·11): 게이트 위 '무료 위젯 1개' 체험 + C0(이어서 보기: 무료 관련글4+티저3).
- 각 칼럼 하단 연결 동선(connect.tools/kits) 카드화 — 전환 필수(C0/C3).

---

## E. 키트 허브/스텝 뷰 개선안

### E-1. 커리큘럼 시각화 (여정감)
- 키트 상세 상단에 **줄기형 스텝 미니맵**: 스텝 수만큼 마디, 무료(00~01) 새싹, 유료 잠금은 봉오리, 완주 스텝은 만개. 허브 개화 언어와 동일 SVG 컴포넌트 재사용.
- 각 마디에 title+무료/잠금 배지, 현재 스텝 하이라이트, '남은 N걸음' 표기.

### E-2. 스텝 동작 (위젯 재사용)
- 스텝 본문에 `data-cx-w` 위젯 이식: 대화 카드=tabs/reveal-steps, 자가진단=quiz/checklist, 계산=slider. kx- 독자 위젯 폐기→CXW 공용.
- 스텝 입력은 localStorage 저장(부부가 이어서), 서버 미전송 고지 유지.

### E-3. 완주 모멘텀
- `cxKitProgress[slug]` localStorage로 완료 스텝 집계 → 미니맵 개화율(%)·상단 진행 링.
- 각 스텝 끝 '한 걸음 완료' 마이크로 축하(꽃잎 1장 개화 애니), 마지막 스텝 완주 시 **개화 카드**(부부 이름·키트명 각인, 저장/공유).
- kx-soon(준비 중) 스텝은 F1 준수: 미완이면 노출 제거 또는 명확한 '다음 업데이트' 없이 숨김.
- 완주율은 '누적 편수'류 중립 성장지표로만 카운트업 허용(V2).

---

## F. 도구 7종 개선안

{tool_lines()}

우선순위: **미제작 4종 신규 빌드가 1순위**(허브 노드가 live로 링크 중 → 도달 시 공백은 신뢰 훼손). 이후 공통 `CXW.calc` 코어로 tx 네임스페이스 통합 + 홈 토큰 이식 + 결과 공유 카드 표준화.

---

## G. 허브 개화 리뉴얼 스펙 (줄기 위 새싹→꽃봉오리→만개)

컨셉: 기존 'S-곡선 여정 지도'를 **하나의 줄기(vine/stem)가 아래(반지하 출발)에서 위(두 분의 여정)로 자라며, 구간을 오를수록 더 활짝 피는 돈나무**로 리프레임. 데이터 모델(zone/type/prem/live) 변경 없음 — 시각·모션만 승격.

### G-1. 성장 단계 매핑 (최적안)
**1차 축 = 존(여정 진행) → 개화 단계** (사용자 은유 '줄기 위 …개화'에 직결, 데이터 무변경)
- 🌱 **모으기(gather) = 새싹기** : 줄기 하단, 연둣빛 새싹 노드. '이른 봄'.
- 🌸 **지키기(keep) = 꽃봉오리기** : 줄기 중단, 닫힌 봉오리 노드(지킨다=아직 감싼 형태). '초여름'.
- 🌺 **불리기(grow) = 만개기** : 줄기 상단, 활짝 핀 꽃 + 씨앗 흩날림(불리기=파이프라인 확산). '결실의 계절'.

**2차 축 = 콘텐츠 type → 꽃 모티프/색**(레전드 일치): 칼럼=잎맥 꽃잎, 도구=톱니 꽃받침, 키트=이정표 리본 꽃심. 색은 --cx-seed/bud/bloom 위에 type 악센트.

**상태 축**: premium=닫힘(봉오리+이슬 잠금, 호버 시 티저 개화) · live=배선 · visited/완주(localStorage)=만개 유지+은은한 글로우.

> 대안(type→단계: 도구=새싹/칼럼=봉오리/키트=만개)은 검토 후 기각 — '줄기를 오르며 피어난다'는 여정 서사가 깨지고, type는 이미 레전드·칩으로 구분됨. 존→단계가 정서·데이터 양쪽에서 우월.

### G-2. 개화 애니메이션 (SVG)
- **성장 트랜지션**: 페이지 로드·스크롤 시 줄기 `jm-draw` 경로가 아래→위로 그려지며(stroke-dashoffset), 지나온 마디에서 노드가 순차 개화(새싹 잎 2장→봉오리→꽃잎 5장 전개). IntersectionObserver 스텝.
- **호버 만개**: 노드 hover/focus 시 꽃잎이 활짝 벌어지고(scale+회전 미세), 향기처럼 꽃가루(gold) 파티클 1~2개 떠오름. 팝업(jm-pop) 동시 표시.
- **꽃잎 컴포넌트**: `<g class=cx-flower data-stage="seed|bud|bloom">` 재사용 심볼(`<symbol id=cxPetal>`) — 5꽃잎 path, currentColor로 단계색 상속. 키트 미니맵과 공유.
- 절제(V2)·reduced-motion 시 개화 최종형 정적 노출.

### G-3. 길 위 계절감
- 존 밴드 배경을 계절 그라디언트로: 모으기=연둣빛 새벽(sage tint), 지키기=분홍 초여름(rose tint), 불리기=금빛 가을(gold tint) — 기존 밴드 틴트 값 재사용, 위→아래 부드러운 전이.
- 미세 환경 파티클(절제): 봄=떠다니는 새싹 홀씨, 여름=나비 1마리 드리프트, 가을=씨앗·낙엽 하강. 홈 drift/bob keyframes 재사용, 개수 최소.

### G-4. 후킹 히어로 카피 (3안)
- (A) eyebrow: 🌱 우리 돈이 피어나는 지도 · h1: 심은 대로 피어나요,\\n두 분의 **돈나무**
- (B) eyebrow: 🌸 반지하에서 만개까지 · h1: 우리가 걸어온 길에\\n**꽃이 피기 시작했어요**
- (C, 현행 계승) h1 유지 + 리드에 개화 프레임 1문장 추가: 아래 새싹에서 위 만개까지, 두 분의 속도로 피워가요,,ㅎㅎ
- 권장: (A) — '돈나무' 브랜드 자산화 + 성장 은유 직결. 보이스 톤(',,':)') 유지.

---

## H. 신규 후킹 콘텐츠 제안 (최대 2)

### H-1. 「우리 부부 돈 궁합 테스트」 (신규 1순위)
- 형식: 리더 `data-cx-w="quiz"` 인터랙티브 콘텐츠(무료, 6~8문항, 결과 4~6유형 카드).
- 왜 후킹: 자기발견+부부 관계+공유욕구 3중 훅 → 콜드 유입 최상단 자석. 결과 유형별로 키트·칼럼을 처방(퍼널 진입점). 초심자 3문의 'WOW'를 정면 충족.
- 제작 규격: 문항=소비/저축/투자 성향 축, 결과 카드=유형명+한 줄 코칭(코칭체)+추천 키트2/칼럼2 딥링크+저장·공유 이미지(로고·부부 이름). 허브에서 '새싹' 진입 노드로 배치. 하드코딩 결과 텍스트만, 시세 없음(하이드레이션 불필요).

### H-2. 「빚부터 갚을까, 모으면서 갚을까」 (신규 2순위 — 콘텐츠 공백 메움)
- 형식: 인터랙티브 칼럼 + `data-cx-w="slider"`/`compare`(부채 상환 vs 병행 저축 시뮬).
- 왜 후킹: 12편에 **부채/대출 주제 전무**(genuine gap). 신혼·내집마련 서사와 직결(전세대출·주담대 현실), '갚기 vs 굴리기' 딜레마는 검색·공감 훅 강함. 지키기(keep) 존 보강.
- 제작 규격: 슬라이더=금리·잔액·여윳돈 → 상환 우선 vs 병행의 총이자·순자산 비교(compare 카드). 코칭체 리드(초심자 3문), finincome/savingrule 도구 연결. 무료 전문 공개로 자석화.

---

## I. 실행 순서 (빌더 에이전트 작업 분해)

원칙: 원자저장(.tmp→replace), git 금지, 각 단계 게이트 검증(gate) 후 다음. 파일 경로는 절대경로.

**P0. 토큰·라우터 기반 (선행, 병렬 불가 — 모두의 의존원)**
1. `contents-columns__BODY` `contents-kits__BODY` `contents-hub__BODY` `tools/*.html` `<style>` 헤드에 §B `--cx-*` 토큰 블록 주입(단일 소스 텍스트 동일).
2. 리더 `<script>`에 `CXW` 라우터+7위젯+인라인훅(term/count/pull) 구현(§C). `CXW.calc` 포뮬러 레지스트리 포함.

**P1. 리더·칼럼 통일 (담당: 리더 빌더)**
3. `bookcol-04.html` `bookcol-07.html` `bookcol-12.html` 등 구형→신형 마크업 마이그레이션.
4. 12편에 §D 처방 위젯을 `data-cx-w`로 삽입(편당 1~2), 난도4편 콜드오픈 리드 보강, 프리미엄 티저에 무료 위젯1+이어서보기.
5. `contents-columns__BODY`에 위젯 스타일(.cxw-*) 추가, cxSnap·필터 동기.

**P2. 허브 개화 리뉴얼 (담당: 허브 빌더 — 최대 작업)**
6. `contents-hub__BODY`: 노드 렌더를 §G 개화 시스템으로 교체(존→단계, type→모티프, `<symbol id=cxPetal>`, 줄기 성장·호버 만개·계절 밴드·파티클). jmSnap 데이터는 유지.
7. 히어로 카피 (A)안 적용, 레전드 은유 정합. 방문/완주 localStorage 개화 진행.
8. 모바일 viewBox·라벨 겹침·reduced-motion 폴백 검수.

**P3. 키트 뷰 (담당: 키트 빌더)**
9. `contents-kits__BODY`: 줄기형 스텝 미니맵(cxPetal 공유), 스텝 본문 CXW 위젯 이식, `cxKitProgress` 완주 모멘텀·개화 카드, kx-soon F1 정리.

**P4. 도구 (담당: 도구 빌더)**
10. 신규 빌드 4종: `tools/booktool-flexcost.html` `booktool-portfolio.html` `booktool-taxaccount.html` `booktool-valuation.html`(§F 규격).
11. 기존 3종 `CXW.calc` 통합·토큰 이식·결과 공유 카드 표준화.

**P5. 신규 콘텐츠 (담당: 콘텐츠 빌더)**
12. `contents/quiz/money-match.html`(H-1, quiz) + `contents/columns/bookcol-13.html`(H-2, 부채) 제작, 위젯 배선.

**P6. 인덱스·스냅 동기 (선행 완료 후, 원자)**
13. `contents/contents_index.json`에 신규 2건·존/단계 메타 반영 → `count` 갱신.
14. 허브 `jmSnap`·리더 `cxSnap` 재생성(인덱스 단일 소스에서 파생), 노드 좌표 재배치.
15. 전체 게이트 검증(gate) + 라이브 스모크(노드 링크 도달·위젯 mount·개화 렌더).

의존: P0→(P1,P2,P3,P4,P5 병렬 가능)→P6. 단, P2/P3는 P0-2(CXW·cxPetal) 완료 의존.

---

*본 기획은 라이브 문서. 컨센서스 v1.2 및 홈 토큰 갱신 시 §B·§G 우선 동기.*
"""

# ---------------- JSON (builder-facing) ----------------
plan = {
  "meta": {
    "title": "quality500_plan",
    "version": "v1",
    "generated": now,
    "audit_scope": {"columns": 12, "tools_indexed": 7, "tools_built": 3, "kits": 10, "kit_steps_total": 82, "hub_nodes": 29},
    "baselines": ["home__BODY tokens", "consensus_v1.2", "beginner_3q(need/place/wow)"],
    "constraints": ["atomic_write(.tmp->replace)", "no_git", "bash+python", "warm_pink_palette_only", "no_dark_band/purple/pure_black", "free_first/premium=access_frame", "counting_only_on_growth_metrics"]
  },
  "diagnosis": {
    "reader":  {"good": ["voice top-tier(',,':)'ㅎㅎ, coaching)", "bookcol-01 = complete interactive reference", "filter/sort chips + premium gate matches free-first"],
                "weak": ["two markup generations(new data-cx-sc vs old cx-doc)", "interactivity concentrated in col-01 only", "no declarative data-cx-w widget contract", "premium teasers too thin(1.5-2.5KB), C0 missing", "cold-open hook weak on advanced topics(06/08/09/10)", "paragraph rhythm L8/L9/L10 residue in old fragments"]},
    "kit":     {"good": ["mature kit.json schema(why/outcome/steps.free)", "step00 prologue free + narrative-aligned", "single-purchase(P4) framing consistent"],
                "weak": ["no completion momentum(localStorage=0)", "no curriculum visualization", "kx-soon(12) risks F1 'coming-soon' exposure", "step widgets isolated(kx- namespace) not reusable", "visual drift from home tokens"]},
    "tool":    {"good": ["existing 3 tools slider-number sync + presets solid", "input device-only/no server(trust)", "save/precision gate matches free-paid"],
                "weak": ["4 of 7 tools NOT BUILT(flexcost/portfolio/taxaccount/valuation) but linked live=1", "namespace fragmentation tx/tx2/tx3", "weak shareable result asset", "off home-token styling", "hydration audit incomplete(L2/X3)"]},
    "hub":     {"good": ["S-curve map + 29 nodes + 3 zone bands + hover popup already interactive", "jmSnap data-driven + counts/filter/list fallback", "gradient/pulse/reveal aligned to home motion"],
                "weak": ["metaphor stuck at 'map', no sprout->bud->bloom growth", "no bloom/season animation", "no visited/completion growth persistence", "mobile viewBox 1000x4150 too tall/label overlap", "legend(leaf/tool/flag) mismatched with per-item emojis", "hero copy can rise to bloom framing"]}
  },
  "design_tokens": {
    "color": {"--cx-bg":"#FDFBF7","--cx-bg2":"#FBF3EE","--cx-card":"#FFFFFF","--cx-ink":"#3E2F29","--cx-ink2":"#5C4B43","--cx-mut":"#8A7B72","--cx-border":"#EAD7D3","--cx-rose":"#B33A4C","--cx-rose2":"#B85060","--cx-deep":"#7C243B","--cx-pink":"#D67A89","--cx-pinkSoft":"#F8E8EA","--cx-pinkSoft2":"#FCEEF1","--cx-sage":"#5E8C7F","--cx-gold":"#C9A84C","--cx-lav":"#9C6BA8","--cx-sand":"#F0DED8","--cx-up":"#D8584E","--cx-down":"#4A7DE8"},
    "growth_season": {"--cx-seed":"#7FB08A","--cx-bud":"#E08696","--cx-bloom":"#B33A4C","--cx-pollen":"#C9A84C","--cx-zone-gather":"rgba(94,140,127,.10)","--cx-zone-keep":"rgba(179,58,76,.08)","--cx-zone-grow":"rgba(201,168,76,.13)"},
    "type_scale": {"font":"'Pretendard Variable',Pretendard,-apple-system,sans-serif","--cx-fs-cap":"clamp(12px,1.4vw,13px)","--cx-fs-body":"clamp(15px,1.6vw,17px)","--cx-fs-lead":"clamp(17px,2vw,19.5px)","--cx-fs-h3":"clamp(18px,2.3vw,23px)","--cx-fs-h2":"clamp(23px,3.4vw,34px)","--cx-fs-h1":"clamp(27px,4vw,42px)","--cx-fs-hero":"clamp(34px,5.4vw,68px)","lh_body":1.75,"lh_head":1.3,"tracking_head":"-0.02em"},
    "layout": {"--cx-r":"22px","--cx-r-sm":"14px","--cx-maxw":"1180px","--cx-read":"720px","--cx-pad-sec":"clamp(120px,13vw,192px)","--cx-pad-hero":"clamp(44px,6vw,84px)","--cx-pad-x":"clamp(22px,4.5vw,40px)"},
    "shadow": {"--cx-sh":"0 1px 2px rgba(62,47,41,.04),0 4px 10px rgba(190,80,96,.05),0 14px 30px rgba(190,80,96,.07)","--cx-shi":"0 2px 4px rgba(62,47,41,.05),0 12px 24px rgba(190,80,96,.10),0 28px 56px rgba(190,80,96,.15)"},
    "motion": {"--cx-ease":"cubic-bezier(.16,1,.3,1)","--cx-dur":".6s","reveal":"IntersectionObserver -> .cx-in","countup_scope":"growth/neutral metrics only(V2/B11)","reduced_motion":"freeze bloom/drift, show final state","reuse_keyframes":["bob","drift","shimmer","pulse"]},
    "typography_rules": ["card-title 1 line(L11)","lead max-width+center(L12)","emphasis span pad(L9)","headline break by meaning(L10)","paragraph 1-2 sentences(L8)","section symmetric vspace(L1)","equal grid(L6)"]
  },
  "widget_library": {
    "router": {"api":"CXW.mount(root)","scan":"root.querySelectorAll('[data-cx-w]')","ready_flag":"data-cx-ready=1","base_class":".cxw + .cxw-<type>","progressive_enhancement": True,"shared_by":["contents-columns__BODY","contents-kits__BODY"],"calc_core":"CXW.calc registry(unify tx/tx2/tx3)"},
    "widgets": [
      {"name":"slider","attr":"data-cx-w=slider","markup":"[data-min][data-max][data-step][data-unit] > input[type=range] + [data-out] + optional [data-formula=erode|compound|gap] + [data-fill]","behavior":"range->formula->update [data-out], fill width%, scale labels"},
      {"name":"tabs","attr":"data-cx-w=tabs","markup":"[role=tablist] button[data-tab=key] + [data-panel=key]","behavior":"click->show panel, aria-selected, arrow-key nav"},
      {"name":"quiz","attr":"data-cx-w=quiz","markup":"[data-q] > button[data-opt][data-correct?] + [data-feedback]","behavior":"select->reveal answer/explain, score, final result card(shareable), retry"},
      {"name":"reveal-steps","attr":"data-cx-w=reveal-steps","markup":"li[data-step] + [data-next]","behavior":"click/scroll->fade next, progress dots, summary on complete"},
      {"name":"counter-bar","attr":"data-cx-w=counter-bar","markup":"[data-to][data-goal?][data-unit] + [data-num] + [data-track]","behavior":"in-view countup(growth only), goal proximity%, threshold marker"},
      {"name":"compare","attr":"data-cx-w=compare","markup":"2x[data-side](kind/num/sub) + optional [data-cmp-tabs]","behavior":"tab/toggle updates both, winner color rose/sage"},
      {"name":"checklist","attr":"data-cx-w=checklist","markup":"label>input[type=checkbox][data-chk] + [data-count]","behavior":"tally+localStorage, all-done celebrate+share card"}
    ],
    "inline_hooks": [
      {"name":"cx-term","attr":".cx-term[data-tip]","behavior":"gray hover/focus tooltip(consensus seed)"},
      {"name":"cx-count","attr":".cx-count[data-to][data-suffix]","behavior":"growth countup mini"},
      {"name":"cx-pull/cx-hl","behavior":"quote emphasis / rose underline-bold (no neon)"}
    ]
  },
  "columns": [
    {"slug":s,"title":t,"zone":z,"premium":p,"hook_score":sc,"good":g,"add":a,"structure_fix":r}
    for (s,t,z,p,sc,g,a,r) in COLS
  ],
  "columns_common_rx": ["migrate old->new data-cx-sc markup","1-2 data-cx-w widgets per column","cold-open(beginner 3q)+analogy on advanced 06/08/09/10","premium teaser: 1 free widget + C0 continue-reading","bottom connect.tools/kits cards(C0/C3)"],
  "kit_plan": {
    "curriculum_viz":"stem mini-map(cxPetal shared): free=sprout, locked=bud, done=bloom; current highlight; 'N steps left'",
    "step_widgets":"replace kx- with CXW; dialog=tabs/reveal-steps, self-check=quiz/checklist, calc=slider; localStorage save",
    "completion_momentum":"cxKitProgress[slug] -> bloom% ring; per-step petal micro-bloom; finish=bloom card(couple names+kit, save/share)",
    "compliance":["kx-soon steps: F1 hide if unbuilt","countup only neutral growth(V2)"]
  },
  "tools": [
    {"slug":s,"title":t,"status":st,"fix":f} for (s,t,st,f) in TOOLS
  ],
  "tools_priority":"BUILD 4 missing first(nodes link live=1 -> broken on arrival), then unify CXW.calc + tokens + share card",
  "hub_bloom": {
    "concept":"reframe S-curve map into a growing stem/money-tree: blooms more as journey climbs; data model(zone/type/prem/live) unchanged",
    "stage_mapping": {
      "primary_axis":"zone -> bloom stage",
      "gather":"seed(새싹) lower stem, sage/spring",
      "keep":"bud(꽃봉오리) mid stem, rose/early-summer",
      "grow":"bloom(만개) upper stem, gold/harvest + seeds dispersing",
      "secondary_axis":"type -> flower motif/color (column=leaf-vein petal, tool=gear calyx, kit=ribbon core)",
      "state_axis":"premium=closed bud+dew-lock(hover teaser bloom); live=wired; visited/complete(localStorage)=stay bloomed+glow",
      "rejected_alt":"type->stage(tool=seed/column=bud/kit=bloom): breaks climb-the-stem narrative; type already shown by legend/chips"
    },
    "animation": {
      "growth":"stroke-dashoffset draw bottom->top; nodes bloom sequentially via IntersectionObserver(sprout leaves->bud->5 petals)",
      "hover_bloom":"petals open(scale+micro-rotate) + gold pollen particle; show jm-pop",
      "component":"<symbol id=cxPetal> 5-petal path, currentColor stage tint; shared with kit mini-map",
      "restraint":"V2 + reduced-motion final-state static"
    },
    "season":"zone bands as seasonal gradient(spring sage / summer rose / autumn gold; reuse existing tints); minimal particles(spring seed-fluff, summer 1 butterfly, autumn falling seeds) via drift/bob",
    "hero_copy": {
      "A_recommended":{"eyebrow":"🌱 우리 돈이 피어나는 지도","h1":"심은 대로 피어나요, 두 분의 돈나무"},
      "B":{"eyebrow":"🌸 반지하에서 만개까지","h1":"우리가 걸어온 길에 꽃이 피기 시작했어요"},
      "C":"keep current h1 + add bloom-frame lead sentence"
    }
  },
  "new_content": [
    {"rank":1,"title":"우리 부부 돈 궁합 테스트","format":"reader quiz(data-cx-w=quiz), free, 6-8 Q, 4-6 result types",
     "why_hook":"self-discovery+couple+share triple hook; top-of-funnel magnet; result routes to kits/columns(funnel); hits beginner-3q WOW",
     "spec":"axes=spend/save/invest; result card=type+one-line coaching+2kits/2columns deeplink+share image(logo+couple names); hub 'seed' entry node; hardcoded text no market data",
     "files":["contents/quiz/money-match.html"]},
    {"rank":2,"title":"빚부터 갚을까, 모으면서 갚을까","format":"interactive column + slider/compare",
     "why_hook":"debt topic ABSENT in 12(real gap); newlywed/home-buying reality(jeonse/mortgage); 'payoff vs grow' dilemma high search/empathy; strengthens keep zone",
     "spec":"slider=rate/balance/surplus -> payoff-first vs parallel total-interest/net-worth compare cards; coaching lead(beginner 3q); link finincome/savingrule; free full-open magnet",
     "files":["contents/columns/bookcol-13.html"]}
  ],
  "build_order": [
    {"phase":"P0","name":"tokens+router(prereq, blocks all)","files":["imweb_cdn/contents-columns__BODY.html","imweb_cdn/contents-kits__BODY.html","imweb_cdn/contents-hub__BODY.html","contents/tools/*.html"],"tasks":["inject --cx-* tokens(single source)","implement CXW router+7 widgets+inline hooks+calc registry"]},
    {"phase":"P1","name":"reader/columns unify","depends_on":["P0"],"files":["contents/columns/bookcol-01..12.html","imweb_cdn/contents-columns__BODY.html"],"tasks":["old->new markup migration(04/07/12..)","insert data-cx-w per D-rx","cold-open advanced 4","premium teaser widget+C0","add .cxw-* styles"]},
    {"phase":"P2","name":"hub bloom renewal(largest)","depends_on":["P0"],"files":["imweb_cdn/contents-hub__BODY.html"],"tasks":["node render -> bloom system(zone->stage,type->motif,cxPetal)","stem growth+hover bloom+season bands+particles","hero copy A + legend align","localStorage bloom persistence","mobile viewBox+reduced-motion"]},
    {"phase":"P3","name":"kit view","depends_on":["P0"],"files":["imweb_cdn/contents-kits__BODY.html"],"tasks":["stem step mini-map(cxPetal)","step CXW widgets","cxKitProgress momentum+bloom card","kx-soon F1 cleanup"]},
    {"phase":"P4","name":"tools","depends_on":["P0"],"files":["contents/tools/booktool-flexcost.html","contents/tools/booktool-portfolio.html","contents/tools/booktool-taxaccount.html","contents/tools/booktool-valuation.html","contents/tools/booktool-mandala.html","contents/tools/booktool-savingrule.html","contents/tools/booktool-finincome.html"],"tasks":["build 4 missing(F spec)","unify CXW.calc+tokens+share card"]},
    {"phase":"P5","name":"new content x2","depends_on":["P0"],"files":["contents/quiz/money-match.html","contents/columns/bookcol-13.html"],"tasks":["build quiz + debt column, wire widgets"]},
    {"phase":"P6","name":"index+snapshot sync(atomic, last)","depends_on":["P1","P2","P3","P4","P5"],"files":["contents/contents_index.json","imweb_cdn/contents-hub__BODY.html(jmSnap)","imweb_cdn/contents-columns__BODY.html(cxSnap)"],"tasks":["add 2 new + zone/stage meta, bump count","regen jmSnap/cxSnap from index","gate verify + live smoke(node links/widget mount/bloom render)"]}
  ]
}

atomic_write(MD_PATH, MD)
atomic_write(JSON_PATH, json.dumps(plan, ensure_ascii=False, indent=2))

def h(p):
    return hashlib.md5(open(p,'rb').read()).hexdigest()[:8]
print("WROTE MD  :", MD_PATH)
print("  bytes:", os.path.getsize(MD_PATH), "md5:", h(MD_PATH), "lines:", sum(1 for _ in open(MD_PATH,encoding='utf-8')))
print("WROTE JSON:", JSON_PATH)
print("  bytes:", os.path.getsize(JSON_PATH), "md5:", h(JSON_PATH))
# JSON validity re-parse
json.load(open(JSON_PATH,encoding='utf-8')); print("JSON reparse OK")
print("columns in json:", len(plan["columns"]), "tools:", len(plan["tools"]), "widgets:", len(plan["widget_library"]["widgets"]), "phases:", len(plan["build_order"]))
