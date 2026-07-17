# contents/images/ — 콘텐츠 이미지 규약 (P1)
슬러그별 폴더: `contents/images/<slug>/`
- `_src/*.png` 원본(로컬), `<name>.ann.json` 주석(마스킹·배지), `<name>.webp` 산출물(CDN 발행).
- 변환: `python _gen/img_pipeline.py <slug>` (webp·최대폭 1600·품질 82).
- 리더 참조: `<img src="../images/<slug>/<name>.webp" loading="lazy">`
