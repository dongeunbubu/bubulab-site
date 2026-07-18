# CXW v2 위젯 스키마 (contents 리더·키트 공용)

선언형 위젯은 `data-cx-w="<name>"` 속성으로 표기하고, 로더가 `CXW.mount(root)`에서 자동 마운트한다.
모든 클래스·상태는 `cx-` / `cxw-` 접두를 쓰며 색은 홈 팔레트 토큰(`--cx-*`)만 사용한다.
계약: `CXW.w[name]=function(el){}` 등록, `CXW.calc`(순수식)·`CXW.sim`(시뮬레이터) 레지스트리 재사용, `data-cx-export`가 붙은 결과 카드는 이미지/PDF 저장 훅이 자동 부착된다.

## 기존 위젯(회귀 마커) — 유지 대상
slider, tabs, quiz, compare, checklist, compare-pro, decision-tree, step-guide,
term-chip, timeline-h, summary-card, related-rail, sim-frame

---

## v2.1 신규 위젯 3종

### ① mini-chart — 외부 라이브러리 없이 SVG 미니 차트
`<div data-cx-w="mini-chart" ...></div>`

| 속성 | 필수 | 값 | 설명 |
|---|---|---|---|
| `data-type` | | `bar`\|`stack`\|`donut` (기본 bar) | bar=가로 비교, stack=구성 분해(100%), donut=도넛 |
| `data-items` | ✔ | JSON `[{label,value,color?}]` | color 생략 시 홈 팔레트 순환 |
| `data-unit` | | 문자열 | 값 접미(예: `만원`,`%`) |
| `data-caption` | | 문자열 | 상단 로즈 캡션 |
| `data-note` | | 문자열 | 하단 회색 주석 |
| `data-center` | | 문자열 | donut 중앙 라벨(기본 `합계`) |

- 색 기본값 팔레트: `#B33A4C,#5E8C7F,#C9A84C,#9C6BA8,#D67A89,#7C243B,#7FB08A,#E08696`
- 접근성: 차트 컨테이너 `role="img"` + 요약 `aria-label`, 각 세그먼트 `<title>`.
- 반응형: bar/stack SVG는 `preserveAspectRatio="none"`으로 가로 신축, 라벨/값은 HTML(비신축).

예)
```
<div data-cx-w="mini-chart" data-type="donut" data-center="자산" data-unit="%"
  data-items='[{"label":"예금","value":40},{"label":"주식","value":35},{"label":"연금","value":25}]'></div>
```

### ② evidence-card — 근거(뉴스·발표) 헤드라인 카드
`<div data-cx-w="evidence-card" ...></div>` — 신문 스크랩 결(홈 팔레트, 좌측 로즈 러버 + 괘선 텍스처)

| 속성 | 필수 | 값 | 설명 |
|---|---|---|---|
| `data-kind` | | `발표`\|`보도`\|`화면` (기본 발표) | 색·아이콘 매핑(rose/sage/lav) |
| `data-title` | ✔ | 문자열 | 헤드라인 |
| `data-source` | | 문자열 | 출처 소형 표기 |
| `data-date` | | 문자열 | 우측 날짜 |
| `data-note` | | 문자열 | 부연 |
| `data-img` | | URL | 지연 로드 이미지 |
| `data-href` | | URL | 있으면 카드가 링크(새 탭), 없으면 정적 카드 |

### ③ slider-calc — 슬라이더 즉시 계산(계산 레지스트리 재사용)
`<div data-cx-w="slider-calc" ...></div>` — 슬라이더를 움직이면 결과 숫자 즉시 갱신 + 살짝 튀는 팝

| 속성 | 필수 | 값 | 설명 |
|---|---|---|---|
| `data-calc` | ✔ | `CXW.calc`의 함수명 | 예: `futureValue`,`erode`,`monthlyForGoal` |
| `data-args` | | JSON 배열, `"$"`가 슬라이더 슬롯 | 예: `[0,"$",5,10]` → fn(0, 값, 5, 10) |
| `data-out-key` | | 문자열 | fn이 객체 반환 시 뽑을 키(예: `worth`) |
| `data-label` `data-unit` | | 문자열 | 슬라이더 라벨·단위 |
| `data-min` `data-max` `data-step` `data-def` | | 숫자 | 슬라이더 범위·초기값 |
| `data-out-label` `data-out-unit` | | 문자열 | 결과 라벨·단위 |
| `data-format` | | `won`\|`num`\|`pct` (기본 num) | 결과 숫자 포맷 |
| `data-caption` `data-note` | | 문자열 | 캡션·주석 |

- 결과 카드에 `data-cx-export`가 붙어 이미지/PDF 저장 지원.
- 값 변경 시 `cx:calc`(bubbles) 커스텀 이벤트 디스패치 → 우측 레일이 결과를 pin.

---

## 우측 스티키 레일(.cx-rrail) — data 계약
`CXW.reader.init(body,slug,it)` 래핑으로 자동 부착. `#cxReader`에 `.cx-has-rrail` 부여, **CSS가 `@media(min-width:1400px)`에서만 표시**(미만은 기존 그대로 숨김).

구성(4블록):
1. **지금 챕터 핵심 카드** `.cx-rrail-key`
   - 우선순위: 챕터 섹션(`.cx-ch`) 또는 그 `h2`의 `data-key` 속성.
   - `data-key` 포맷: `"핵심숫자|한 줄"` 또는 `"한 줄"`.
   - 속성 없으면 자동 추출: `h2` 제목 + 첫 강조(`.cx-hl`/`.cx-pull`/`strong`/`b`)의 텍스트.
2. **용어 미니 사전** `.cx-rrail-terms`
   - 현재 챕터 내 `[data-cx-w="term-chip"]`·`.cxw-term`·`.cx-term` 자동 수집(term/def, 중복 제거).
   - 항목 클릭 → 해당 위치로 스크롤 + 대상 플래시(`.cx-term-flash`).
3. **내 계산 결과 pin** `.cx-rrail-pin`
   - `slider-calc`의 `cx:calc` 이벤트 또는 `sim-frame`의 결과(`.cxw-sim-pv`)를 요약해 고정.
   - 레일이 `position:fixed`라 스크롤해도 유지.
4. **하단 고정 CTA** `.cx-rrail-cta`
   - 인덱스 `it.pair`(페어 도구/키트/칼럼) 우선, 없으면 `liveColumns()` 다음 칼럼.

현재 챕터 추적: 기존 목차(`.cx-toc`)의 `.cx-toc-a.on` 상태를 `MutationObserver`로 미러(+목차 없을 때 스크롤 폴백).

## 마이크로 피드백(피드백 2)
- 결정트리(`.cxw-dt`) 선택 시 `.cx-dtprog` 진행 점 증가/감소(back/restart 반영).
- 요약 카드 체크(`.cxw-sum-chk`) 시 `.cxw-sum-box`에 `cx-pop`(scale 팝).
- 모두 transform만 사용, `prefers-reduced-motion` 존중.

---

## v2.2 시각화 애니메이션 레이어 + 신규 위젯 2종

파일럿 피드백 반영: 시각화에도 애니메이션. 모든 진입 애니는 `IntersectionObserver`로 **1회만** 재생(재진입 시 미재생), `prefers-reduced-motion:reduce`면 **즉시 최종 상태**. 외부 라이브러리 없이 SVG + rAF.

### 기존 위젯 애니(회귀 안전 — 마크업/계약 유지)
- **mini-chart**: 진입 시 — `bar` 좌→우 성장(폭, stagger), `stack` 세그먼트 순차 채움, `donut` `stroke-dashoffset` 스윕. 수치 라벨은 count-up(0→값, 콤마 유지). `data-w`(막대·세그 목표폭)·`data-len`(도넛 호 길이)·`data-mcto`(count-up 목표) 훅 추가.
- **evidence-card**: 등장 시 살짝 슬라이드+페이드(`.cxw-ev.cxw-anim`→`.cx-in`), IO 1회.

### ④ stat-hero — 통계 히어로 카드
`<div data-cx-w="stat-hero" ...></div>` — 큰 숫자 1개 + 맥락 한 줄, 챕터 사이 삽입용(홈 팔레트).

| 속성 | 필수 | 값 | 설명 |
|---|---|---|---|
| `data-value` | ✔ | 숫자(콤마 허용) | 큰 숫자. 진입 시 0→값 count-up |
| `data-prefix` | | 문자열 | 숫자 앞 기호(예: `₩`) |
| `data-suffix` / `data-unit` | | 문자열 | 숫자 뒤 단위(예: `%`,`만원`,`명`) |
| `data-label` / `data-context` | | 문자열 | 숫자 아래 맥락 한 줄 |
| `data-delta` | | 문자열 | 변화량 필(예: `전년 대비 +1.2%p`) |
| `data-trend` | | `up`\|`down`\|`flat` | delta 필 색(sage/rose/lav) |
| `data-series` | | JSON 숫자 배열 | 있으면 하단 미니 스파크라인(선 그리기 애니) |
| `data-dur` | | 숫자(600~900) | count-up 지속(ms, 기본 820·범위 클램프) |
| `data-caption` `data-note` | | 문자열 | 상단 로즈 캡션·하단 회색 주석 |

예)
```
<div data-cx-w="stat-hero" data-value="7" data-unit="%" data-caption="7% 적금의 힘"
  data-label="월 30만원, 3년이면 세전 이자만 이만큼" data-delta="시중 대비 +4%p" data-trend="up"
  data-series="[1200,2450,3720,5010,6330,7680]" data-note="* 단리 가정 · 예시"></div>
```

### ⑤ line-trend — 시계열 꺾은선(2계열 비교)
`<div data-cx-w="line-trend" ...></div>` — 연도 라벨 · 점 호버 툴팁 · 선 그리기 애니 · 2계열 비교(예: 기준금리 vs 적금금리). 외부 라이브러리 없이 SVG.

| 속성 | 필수 | 값 | 설명 |
|---|---|---|---|
| `data-x` | ✔ | JSON 배열 | x축 라벨(연도 등). 계열 값과 길이 정렬 |
| `data-series` | ✔ | JSON | 2형식: ① 숫자 배열(단일 계열) ② `[{name,color?,values:[...]}]`(다계열) |
| `data-unit` | | 문자열 | y값 단위(예: `%`) |
| `data-min` `data-max` | | 숫자 | y축 경계(생략 시 자동 + 12% 여유) |
| `data-name` | | 문자열 | 단일 계열일 때 이름 |
| `data-caption` `data-note` | | 문자열 | 캡션·주석 |

- 색 기본값: `#B33A4C`(rose), `#5E8C7F`(sage), `#C9A84C`, `#9C6BA8` 순환. 계열별 `color`로 개별 지정 가능.
- 접근성: SVG `role="img"`+요약 `aria-label`, 각 점 `tabindex=0`+`aria-label`(포커스 시 툴팁). 점 호버/포커스 → 값 툴팁.
- 애니: 계열별 선 그리기(`stroke-dashoffset`, stagger), 점 페이드(`.cxw-lt.cxw-anim`→`.cx-in`). reduced-motion 즉시 최종.

예)
```
<div data-cx-w="line-trend" data-unit="%" data-caption="기준금리 vs 대표 적금금리"
  data-x='["2019","2020","2021","2022","2023","2024"]'
  data-series='[{"name":"기준금리","values":[1.75,0.5,1.0,3.25,3.5,3.5]},{"name":"적금금리","color":"#5E8C7F","values":[2.1,1.3,1.8,4.2,4.4,3.9]}]'></div>
```

### 공용 헬퍼(cx- 접두, FOOTER)
`commaInt`(콤마 정수), `cxOnce`(IO 1회+reduced-motion 즉시), `tween`(rAF+easeOut), `cxReveal`(슬라이드·페이드), `shSpark`(스파크라인 경로), `pathLen`(경로 길이). 모두 `rm`(prefers-reduced-motion) 분기 내장.
