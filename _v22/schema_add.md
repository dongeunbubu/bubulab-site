
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
