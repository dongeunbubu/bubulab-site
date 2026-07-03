# 📦 아임웹 이식 패키지 v3 — 자동 생성 (`야간_진행로그/_gen_imweb_v3.py`)

> 총 **147개 페이지** · 내부링크 **2202건** 슬러그 치환 · 생성일 2026-06-11.
> 원본이 바뀌면 생성기를 다시 실행하세요 — 조각을 수동 편집하면 다음 재생성 때 사라져요.

> 페이지마다 **BODY**(HTML+CSS)는 코드위젯에, **FOOTER**(JS)는 페이지별 푸터에 붙여넣기.
> 슬러그는 파일명 기반(`/스템`). 내부링크가 이 슬러그로 치환돼 있어 그대로 쓰면 링크가 자동으로 맞아요.
> 이미지 `../사진/…`는 아임웹 업로드 후 URL 교체(절차: `아임웹_이식_가이드_v1.md`).

## 0. 사이트 공통(head)에 1회 — 폰트
```html
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
```

## 1. 페이지 매핑 — 홈 1 · 핵심 14 · 머니레터 3 · 도구 47 · 부동산도구 11 · 콘텐츠 33 · 부동산 14 · 레포트 15 · 조각(위젯) 9

| 분류 | 슬러그 | BODY | FOOTER(JS) | 링크치환 |
|---|---|---|---|---|
| 홈 | `/home` | `home__BODY.html` | `home__FOOTER.html` | 74 |
| 핵심 | `/class-7389` | `class-7389__BODY.html` | `class-7389__FOOTER.html` | 15 |
| 핵심 | `/class-b779` | `class-b779__BODY.html` | `class-b779__FOOTER.html` | 21 |
| 핵심 | `/faq-v1` | `faq-v1__BODY.html` | `faq-v1__FOOTER.html` | 15 |
| 핵심 | `/goods-9972` | `goods-9972__BODY.html` | `goods-9972__FOOTER.html` | 20 |
| 핵심 | `/goods-fd41` | `goods-fd41__BODY.html` | `goods-fd41__FOOTER.html` | 17 |
| 핵심 | `/kit-842c` | `kit-842c__BODY.html` | `kit-842c__FOOTER.html` | 17 |
| 핵심 | `/kit-bcaf` | `kit-bcaf__BODY.html` | `kit-bcaf__FOOTER.html` | 20 |
| 핵심 | `/library` | `library__BODY.html` | `library__FOOTER.html` | 68 |
| 핵심 | `/moneyletter-landing` | `moneyletter-landing__BODY.html` | `moneyletter-landing__FOOTER.html` | 67 |
| 핵심 | `/privacy-v1` | `privacy-v1__BODY.html` | `privacy-v1__FOOTER.html` | 13 |
| 핵심 | `/refund-v1` | `refund-v1__BODY.html` | `refund-v1__FOOTER.html` | 13 |
| 핵심 | `/report-hub` | `report-hub__BODY.html` | `report-hub__FOOTER.html` | 25 |
| 핵심 | `/story` | `story__BODY.html` | `story__FOOTER.html` | 11 |
| 핵심 | `/terms-v1` | `terms-v1__BODY.html` | `terms-v1__FOOTER.html` | 13 |
| 머니레터 | `/letter-evening` | `letter-evening__BODY.html` | `letter-evening__FOOTER.html` | 8 |
| 머니레터 | `/letter-morning` | `letter-morning__BODY.html` | `letter-morning__FOOTER.html` | 8 |
| 머니레터 | `/viz-library` | `viz-library__BODY.html` | `viz-library__FOOTER.html` | 0 |
| 도구 | `/tool-1d83` | `tool-1d83__BODY.html` | `tool-1d83__FOOTER.html` | 10 |
| 도구 | `/tool-2f6a` | `tool-2f6a__BODY.html` | `tool-2f6a__FOOTER.html` | 14 |
| 도구 | `/tool-3dad` | `tool-3dad__BODY.html` | `tool-3dad__FOOTER.html` | 15 |
| 도구 | `/tool-4a49` | `tool-4a49__BODY.html` | `tool-4a49__FOOTER.html` | 10 |
| 도구 | `/tool-4a72` | `tool-4a72__BODY.html` | `tool-4a72__FOOTER.html` | 13 |
| 도구 | `/tool-4d2e` | `tool-4d2e__BODY.html` | `tool-4d2e__FOOTER.html` | 17 |
| 도구 | `/tool-52-f1dd` | `tool-52-f1dd__BODY.html` | `tool-52-f1dd__FOOTER.html` | 11 |
| 도구 | `/tool-568e` | `tool-568e__BODY.html` | `tool-568e__FOOTER.html` | 16 |
| 도구 | `/tool-64bb` | `tool-64bb__BODY.html` | `tool-64bb__FOOTER.html` | 16 |
| 도구 | `/tool-65dc` | `tool-65dc__BODY.html` | `tool-65dc__FOOTER.html` | 11 |
| 도구 | `/tool-853a` | `tool-853a__BODY.html` | `tool-853a__FOOTER.html` | 10 |
| 도구 | `/tool-93f4` | `tool-93f4__BODY.html` | `tool-93f4__FOOTER.html` | 12 |
| 도구 | `/tool-a34d` | `tool-a34d__BODY.html` | `tool-a34d__FOOTER.html` | 13 |
| 도구 | `/tool-a6be` | `tool-a6be__BODY.html` | `tool-a6be__FOOTER.html` | 16 |
| 도구 | `/tool-ac1c` | `tool-ac1c__BODY.html` | `tool-ac1c__FOOTER.html` | 16 |
| 도구 | `/tool-af26` | `tool-af26__BODY.html` | `tool-af26__FOOTER.html` | 12 |
| 도구 | `/tool-b7ab` | `tool-b7ab__BODY.html` | `tool-b7ab__FOOTER.html` | 15 |
| 도구 | `/tool-bc45` | `tool-bc45__BODY.html` | `tool-bc45__FOOTER.html` | 14 |
| 도구 | `/tool-cbeb` | `tool-cbeb__BODY.html` | `tool-cbeb__FOOTER.html` | 12 |
| 도구 | `/tool-cea3` | `tool-cea3__BODY.html` | `tool-cea3__FOOTER.html` | 10 |
| 도구 | `/tool-dfe4` | `tool-dfe4__BODY.html` | `tool-dfe4__FOOTER.html` | 13 |
| 도구 | `/tool-dsr-6e40` | `tool-dsr-6e40__BODY.html` | `tool-dsr-6e40__FOOTER.html` | 10 |
| 도구 | `/tool-ea90` | `tool-ea90__BODY.html` | `tool-ea90__FOOTER.html` | 10 |
| 도구 | `/tool-irp-pro-f6f3` | `tool-irp-pro-f6f3__BODY.html` | `tool-irp-pro-f6f3__FOOTER.html` | 18 |
| 도구 | `/tool-isa-5c34` | `tool-isa-5c34__BODY.html` | `tool-isa-5c34__FOOTER.html` | 11 |
| 도구 | `/tool-pro-1780` | `tool-pro-1780__BODY.html` | `tool-pro-1780__FOOTER.html` | 12 |
| 도구 | `/tool-pro-1d9e` | `tool-pro-1d9e__BODY.html` | `tool-pro-1d9e__FOOTER.html` | 11 |
| 도구 | `/tool-pro-240b` | `tool-pro-240b__BODY.html` | `tool-pro-240b__FOOTER.html` | 14 |
| 도구 | `/tool-pro-39d5` | `tool-pro-39d5__BODY.html` | `tool-pro-39d5__FOOTER.html` | 11 |
| 도구 | `/tool-pro-3a11` | `tool-pro-3a11__BODY.html` | `tool-pro-3a11__FOOTER.html` | 10 |
| 도구 | `/tool-pro-438b` | `tool-pro-438b__BODY.html` | `tool-pro-438b__FOOTER.html` | 12 |
| 도구 | `/tool-pro-6aa3` | `tool-pro-6aa3__BODY.html` | `tool-pro-6aa3__FOOTER.html` | 11 |
| 도구 | `/tool-pro-6b5d` | `tool-pro-6b5d__BODY.html` | `tool-pro-6b5d__FOOTER.html` | 17 |
| 도구 | `/tool-pro-8138` | `tool-pro-8138__BODY.html` | `tool-pro-8138__FOOTER.html` | 14 |
| 도구 | `/tool-pro-8362` | `tool-pro-8362__BODY.html` | `tool-pro-8362__FOOTER.html` | 10 |
| 도구 | `/tool-pro-9b41` | `tool-pro-9b41__BODY.html` | `tool-pro-9b41__FOOTER.html` | 16 |
| 도구 | `/tool-pro-c231` | `tool-pro-c231__BODY.html` | `tool-pro-c231__FOOTER.html` | 12 |
| 도구 | `/tool-pro-c48a` | `tool-pro-c48a__BODY.html` | `tool-pro-c48a__FOOTER.html` | 10 |
| 도구 | `/tool-pro-cc61` | `tool-pro-cc61__BODY.html` | `tool-pro-cc61__FOOTER.html` | 12 |
| 도구 | `/tool-pro-d05a` | `tool-pro-d05a__BODY.html` | `tool-pro-d05a__FOOTER.html` | 15 |
| 도구 | `/tool-pro-ec50` | `tool-pro-ec50__BODY.html` | `tool-pro-ec50__FOOTER.html` | 14 |
| 도구 | `/tool-pro-fbcd` | `tool-pro-fbcd__BODY.html` | `tool-pro-fbcd__FOOTER.html` | 12 |
| 도구 | `/tool-pro-fdd1` | `tool-pro-fdd1__BODY.html` | `tool-pro-fdd1__FOOTER.html` | 17 |
| 도구 | `/tool-pro-fe0e` | `tool-pro-fe0e__BODY.html` | `tool-pro-fe0e__FOOTER.html` | 19 |
| 도구 | `/tool-vs-24fc` | `tool-vs-24fc__BODY.html` | `tool-vs-24fc__FOOTER.html` | 16 |
| 도구 | `/tool-vs-3ef9` | `tool-vs-3ef9__BODY.html` | `tool-vs-3ef9__FOOTER.html` | 14 |
| 도구 | `/tool-vs-489f` | `tool-vs-489f__BODY.html` | `tool-vs-489f__FOOTER.html` | 11 |
| 부동산도구 | `/tool-re-158a` | `tool-re-158a__BODY.html` | `tool-re-158a__FOOTER.html` | 15 |
| 부동산도구 | `/tool-re-3253` | `tool-re-3253__BODY.html` | `tool-re-3253__FOOTER.html` | 20 |
| 부동산도구 | `/tool-re-4254` | `tool-re-4254__BODY.html` | `tool-re-4254__FOOTER.html` | 14 |
| 부동산도구 | `/tool-re-57f2` | `tool-re-57f2__BODY.html` | `tool-re-57f2__FOOTER.html` | 7 |
| 부동산도구 | `/tool-re-6e94` | `tool-re-6e94__BODY.html` | `tool-re-6e94__FOOTER.html` | 11 |
| 부동산도구 | `/tool-re-8cfa` | `tool-re-8cfa__BODY.html` | `tool-re-8cfa__FOOTER.html` | 17 |
| 부동산도구 | `/tool-re-ac3c` | `tool-re-ac3c__BODY.html` | `tool-re-ac3c__FOOTER.html` | 16 |
| 부동산도구 | `/tool-re-c0bd` | `tool-re-c0bd__BODY.html` | `tool-re-c0bd__FOOTER.html` | 15 |
| 부동산도구 | `/tool-re-c181` | `tool-re-c181__BODY.html` | `tool-re-c181__FOOTER.html` | 14 |
| 부동산도구 | `/tool-re-f1e8` | `tool-re-f1e8__BODY.html` | `tool-re-f1e8__FOOTER.html` | 7 |
| 부동산도구 | `/tool-re-fefa` | `tool-re-fefa__BODY.html` | `tool-re-fefa__FOOTER.html` | 11 |
| 콘텐츠 | `/col-1d8c` | `col-1d8c__BODY.html` | `col-1d8c__FOOTER.html` | 19 |
| 콘텐츠 | `/col-33ee` | `col-33ee__BODY.html` | `col-33ee__FOOTER.html` | 13 |
| 콘텐츠 | `/col-5392` | `col-5392__BODY.html` | `col-5392__FOOTER.html` | 14 |
| 콘텐츠 | `/col-561d` | `col-561d__BODY.html` | `col-561d__FOOTER.html` | 15 |
| 콘텐츠 | `/col-5fa2` | `col-5fa2__BODY.html` | `col-5fa2__FOOTER.html` | 19 |
| 콘텐츠 | `/col-6a03` | `col-6a03__BODY.html` | `col-6a03__FOOTER.html` | 14 |
| 콘텐츠 | `/col-6b79` | `col-6b79__BODY.html` | `col-6b79__FOOTER.html` | 18 |
| 콘텐츠 | `/col-873e` | `col-873e__BODY.html` | `col-873e__FOOTER.html` | 17 |
| 콘텐츠 | `/col-a331` | `col-a331__BODY.html` | `col-a331__FOOTER.html` | 14 |
| 콘텐츠 | `/col-bca7` | `col-bca7__BODY.html` | `col-bca7__FOOTER.html` | 19 |
| 콘텐츠 | `/col-cae7` | `col-cae7__BODY.html` | `col-cae7__FOOTER.html` | 14 |
| 콘텐츠 | `/col-d16b` | `col-d16b__BODY.html` | `col-d16b__FOOTER.html` | 18 |
| 콘텐츠 | `/col-e2bc` | `col-e2bc__BODY.html` | `col-e2bc__FOOTER.html` | 15 |
| 콘텐츠 | `/col-vs-a208` | `col-vs-a208__BODY.html` | `col-vs-a208__FOOTER.html` | 20 |
| 콘텐츠 | `/contents-hub` | `contents-hub__BODY.html` | `contents-hub__FOOTER.html` | 60 |
| 콘텐츠 | `/eco-2031` | `eco-2031__BODY.html` | `eco-2031__FOOTER.html` | 17 |
| 콘텐츠 | `/eco-2af1` | `eco-2af1__BODY.html` | `eco-2af1__FOOTER.html` | 18 |
| 콘텐츠 | `/eco-38cf` | `eco-38cf__BODY.html` | `eco-38cf__FOOTER.html` | 19 |
| 콘텐츠 | `/eco-5396` | `eco-5396__BODY.html` | `eco-5396__FOOTER.html` | 12 |
| 콘텐츠 | `/eco-630d` | `eco-630d__BODY.html` | `eco-630d__FOOTER.html` | 14 |
| 콘텐츠 | `/eco-676e` | `eco-676e__BODY.html` | `eco-676e__FOOTER.html` | 18 |
| 콘텐츠 | `/eco-7ee1` | `eco-7ee1__BODY.html` | `eco-7ee1__FOOTER.html` | 17 |
| 콘텐츠 | `/eco-9e63` | `eco-9e63__BODY.html` | `eco-9e63__FOOTER.html` | 17 |
| 콘텐츠 | `/eco-abc-c50f` | `eco-abc-c50f__BODY.html` | `eco-abc-c50f__FOOTER.html` | 17 |
| 콘텐츠 | `/eco-cf33` | `eco-cf33__BODY.html` | `eco-cf33__FOOTER.html` | 17 |
| 콘텐츠 | `/eco-etf-364f` | `eco-etf-364f__BODY.html` | `eco-etf-364f__FOOTER.html` | 13 |
| 콘텐츠 | `/eco-ev-f752` | `eco-ev-f752__BODY.html` | `eco-ev-f752__FOOTER.html` | 19 |
| 콘텐츠 | `/eco-fcf-3b13` | `eco-fcf-3b13__BODY.html` | `eco-fcf-3b13__FOOTER.html` | 17 |
| 콘텐츠 | `/eco-fcfvs-19e4` | `eco-fcfvs-19e4__BODY.html` | `eco-fcfvs-19e4__FOOTER.html` | 18 |
| 콘텐츠 | `/eco-fomc-958f` | `eco-fomc-958f__BODY.html` | `eco-fomc-958f__FOOTER.html` | 19 |
| 콘텐츠 | `/eco-perpbrroe-18bd` | `eco-perpbrroe-18bd__BODY.html` | `eco-perpbrroe-18bd__FOOTER.html` | 13 |
| 콘텐츠 | `/eco-rpo-6696` | `eco-rpo-6696__BODY.html` | `eco-rpo-6696__FOOTER.html` | 17 |
| 콘텐츠 | `/eco-vs-3479` | `eco-vs-3479__BODY.html` | `eco-vs-3479__FOOTER.html` | 18 |
| 부동산 | `/re-1a87` | `re-1a87__BODY.html` | `re-1a87__FOOTER.html` | 15 |
| 부동산 | `/re-440a` | `re-440a__BODY.html` | `re-440a__FOOTER.html` | 12 |
| 부동산 | `/re-4870` | `re-4870__BODY.html` | `re-4870__FOOTER.html` | 13 |
| 부동산 | `/re-50db` | `re-50db__BODY.html` | `re-50db__FOOTER.html` | 14 |
| 부동산 | `/re-5d69` | `re-5d69__BODY.html` | `re-5d69__FOOTER.html` | 15 |
| 부동산 | `/re-68e6` | `re-68e6__BODY.html` | `re-68e6__FOOTER.html` | 15 |
| 부동산 | `/re-6bcb` | `re-6bcb__BODY.html` | `re-6bcb__FOOTER.html` | 15 |
| 부동산 | `/re-91aa` | `re-91aa__BODY.html` | `re-91aa__FOOTER.html` | 15 |
| 부동산 | `/re-a0a2` | `re-a0a2__BODY.html` | `re-a0a2__FOOTER.html` | 11 |
| 부동산 | `/re-c89d` | `re-c89d__BODY.html` | `re-c89d__FOOTER.html` | 12 |
| 부동산 | `/re-e0f1` | `re-e0f1__BODY.html` | `re-e0f1__FOOTER.html` | 11 |
| 부동산 | `/re-e6d2` | `re-e6d2__BODY.html` | `re-e6d2__FOOTER.html` | 15 |
| 부동산 | `/re-vs-2921` | `re-vs-2921__BODY.html` | `re-vs-2921__FOOTER.html` | 12 |
| 부동산 | `/re-vs-7b73` | `re-vs-7b73__BODY.html` | `re-vs-7b73__FOOTER.html` | 12 |
| 레포트 | `/report-14a4` | `report-14a4__BODY.html` | `report-14a4__FOOTER.html` | 21 |
| 레포트 | `/report-3efe` | `report-3efe__BODY.html` | `report-3efe__FOOTER.html` | 14 |
| 레포트 | `/report-87f1` | `report-87f1__BODY.html` | `report-87f1__FOOTER.html` | 14 |
| 레포트 | `/report-942b` | `report-942b__BODY.html` | `report-942b__FOOTER.html` | 19 |
| 레포트 | `/report-9493` | `report-9493__BODY.html` | `report-9493__FOOTER.html` | 18 |
| 레포트 | `/report-9c5b` | `report-9c5b__BODY.html` | `report-9c5b__FOOTER.html` | 13 |
| 레포트 | `/report-ai-9970` | `report-ai-9970__BODY.html` | `report-ai-9970__FOOTER.html` | 14 |
| 레포트 | `/report-ba95` | `report-ba95__BODY.html` | `report-ba95__FOOTER.html` | 16 |
| 레포트 | `/report-bb4d` | `report-bb4d__BODY.html` | `report-bb4d__FOOTER.html` | 17 |
| 레포트 | `/report-ccb2` | `report-ccb2__BODY.html` | `report-ccb2__FOOTER.html` | 19 |
| 레포트 | `/report-d576` | `report-d576__BODY.html` | `report-d576__FOOTER.html` | 14 |
| 레포트 | `/report-de46` | `report-de46__BODY.html` | `report-de46__FOOTER.html` | 14 |
| 레포트 | `/report-e29c` | `report-e29c__BODY.html` | `report-e29c__FOOTER.html` | 13 |
| 레포트 | `/report-ffe1` | `report-ffe1__BODY.html` | `report-ffe1__FOOTER.html` | 14 |
| 레포트 | `/report-smr3-ef74` | `report-smr3-ef74__BODY.html` | `report-smr3-ef74__FOOTER.html` | 19 |
| 조각(위젯) | `/letter-8221` | `letter-8221__BODY.html` | `letter-8221__FOOTER.html` | 0 |
| 조각(위젯) | `/letter-ba2f` | `letter-ba2f__BODY.html` | `letter-ba2f__FOOTER.html` | 0 |
| 조각(위젯) | `/pay-809e` | `pay-809e__BODY.html` | `pay-809e__FOOTER.html` | 0 |
| 조각(위젯) | `/pay-dunning-fa4c` | `pay-dunning-fa4c__BODY.html` | `pay-dunning-fa4c__FOOTER.html` | 0 |
| 조각(위젯) | `/sub-2645` | `sub-2645__BODY.html` | `sub-2645__FOOTER.html` | 0 |
| 조각(위젯) | `/sub-3a8b` | `sub-3a8b__BODY.html` | `sub-3a8b__FOOTER.html` | 0 |
| 조각(위젯) | `/sub-5a7f` | `sub-5a7f__BODY.html` | `sub-5a7f__FOOTER.html` | 0 |
| 조각(위젯) | `/sub-8645` | `sub-8645__BODY.html` | `sub-8645__FOOTER.html` | 0 |
| 조각(위젯) | `/sub-vs-fd47` | `sub-vs-fd47__BODY.html` | `sub-vs-fd47__FOOTER.html` | 0 |

## 2. 검증 요약
- FOOTER 스크립트 총 512개 · BODY 조각 내 실제 script 태그 0 (주석 안 문구는 제외)
- 조각(위젯) 분류는 독립 페이지가 아니라 마이페이지/결제 화면 등에 붙이는 카드 위젯이에요.