#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
부부연구소 콘텐츠 이미지 파이프라인 (P1 · 1회 확립)
=====================================================
디렉토리 규약 (콘텐츠 슬러그별):
  contents/images/<slug>/_src/*.png        # 원본 캡처(로컬 보관 권장)
  contents/images/<slug>/<name>.ann.json   # (선택) 마스킹·클릭배지 주석
  contents/images/<slug>/<name>.webp        # 변환 산출물(CDN 발행 · repo push→라이브)
리더 조각에서는 <img src="../images/<slug>/<name>.webp"> 형태로 참조.

변환 규격: PNG→WEBP · 최대 폭 1600px · 품질 82 (마스터플랜 §5 예산: 콘텐츠당 15장, 캡처 스텝 25장).

주석(ann.json) 스키마 — 좌표는 0~1 비율(권장) 또는 px 정수 혼용 허용:
  {
    "mask":   [ {"x":0.62,"y":0.18,"w":0.30,"h":0.06}, ... ],   # 개인정보 블러(이름·계좌·잔액)
    "badges": [ {"x":0.50,"y":0.40,"label":"1"}, ... ]           # 캡처 스텝 클릭 위치 배지
  }

사용:
  python img_pipeline.py <slug>            # 해당 슬러그 _src/*.png 전량 변환(+주석 합성)
  python img_pipeline.py --all             # contents/images/* 전체
  python img_pipeline.py --self-test       # 파이프라인 동작 자체 검증(임시 이미지)
  python img_pipeline.py --file a.png b.webp [--maxw 1600 --q 82]
"""
import os, sys, json, argparse
from PIL import Image, ImageFilter, ImageDraw, ImageFont

MAXW_DEFAULT = 1600
Q_DEFAULT    = 82
ROOT         = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_ROOT     = os.path.join(ROOT, 'contents', 'images')
BRAND_ROSE   = (179, 58, 76)

def _px(v, total):
    """0~1 비율이면 px로 환산, 그 외엔 정수 px로 간주."""
    v = float(v)
    return int(round(v * total)) if 0.0 <= v <= 1.0 else int(round(v))

def mask_blur(img, boxes, radius=None):
    """지정 사각 영역을 가우시안 블러로 마스킹(개인정보 보호)."""
    if not boxes:
        return img
    W, H = img.size
    if radius is None:
        radius = max(6, int(min(W, H) * 0.03))
    base = img.convert('RGB')
    for b in boxes:
        x = _px(b.get('x', 0), W); y = _px(b.get('y', 0), H)
        w = _px(b.get('w', 0), W); h = _px(b.get('h', 0), H)
        x2 = max(0, min(W, x + w)); y2 = max(0, min(H, y + h))
        x = max(0, min(W, x));      y = max(0, min(H, y))
        if x2 <= x or y2 <= y:
            continue
        region = base.crop((x, y, x2, y2)).filter(ImageFilter.GaussianBlur(radius))
        base.paste(region, (x, y))
    return base

def add_click_badge(img, points, r=None):
    """클릭 위치에 번호 배지(흰 테두리 + 로즈 원 + 숫자) 합성 — 캡처 스텝 가이드용."""
    if not points:
        return img
    im = img.convert('RGBA')
    W, H = im.size
    if r is None:
        r = max(14, int(min(W, H) * 0.028))
    draw = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', int(r*1.1))
    except Exception:
        font = ImageFont.load_default()
    for i, p in enumerate(points):
        cx = _px(p.get('x', 0), W); cy = _px(p.get('y', 0), H)
        label = str(p.get('label', i + 1))
        draw.ellipse([cx-r-3, cy-r-3, cx+r+3, cy+r+3], fill=(255, 255, 255, 235))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=BRAND_ROSE + (255,))
        try:
            bbox = draw.textbbox((0, 0), label, font=font); tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
            draw.text((cx-tw/2, cy-th/2-bbox[1]), label, fill=(255, 255, 255, 255), font=font)
        except Exception:
            draw.text((cx-4, cy-6), label, fill=(255, 255, 255, 255))
    return im

def convert_to_webp(src, dst, maxw=MAXW_DEFAULT, quality=Q_DEFAULT, ann=None):
    """PNG→WEBP: 최대 폭 리사이즈 → (마스킹) → (배지) → webp 저장."""
    img = Image.open(src)
    if img.mode in ('P', 'LA'):
        img = img.convert('RGBA')
    W, H = img.size
    if W > maxw:
        img = img.resize((maxw, int(round(H * maxw / W))), Image.LANCZOS)
    if ann:
        img = mask_blur(img, ann.get('mask'))
        img = add_click_badge(img, ann.get('badges'))
    save = img.convert('RGB') if img.mode == 'RGBA' and not (ann and ann.get('badges')) else img
    os.makedirs(os.path.dirname(dst) or '.', exist_ok=True)
    save.save(dst, 'WEBP', quality=quality, method=6)
    return dst, save.size

def _ann_for(src):
    cand = os.path.splitext(src)[0] + '.ann.json'
    if os.path.exists(cand):
        try:
            return json.load(open(cand, encoding='utf-8'))
        except Exception:
            return None
    return None

def process_slug(slug, maxw=MAXW_DEFAULT, quality=Q_DEFAULT):
    d = os.path.join(IMG_ROOT, slug)
    src_dir = os.path.join(d, '_src')
    if not os.path.isdir(src_dir):
        print('  (skip) no _src for', slug); return 0
    n = 0
    for fn in sorted(os.listdir(src_dir)):
        if not fn.lower().endswith('.png'):
            continue
        src = os.path.join(src_dir, fn)
        dst = os.path.join(d, os.path.splitext(fn)[0] + '.webp')
        _, size = convert_to_webp(src, dst, maxw, quality, _ann_for(src))
        print('  %s -> %s %s' % (fn, os.path.basename(dst), size)); n += 1
    return n

def self_test():
    import tempfile
    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, 't.png')
    im = Image.new('RGB', (2200, 1400), (245, 238, 223))
    d = ImageDraw.Draw(im); d.rectangle([1300, 250, 1900, 360], fill=(255, 255, 255)); d.text((1320, 285), 'ACCOUNT 110-234-567890  BAL 12,345,678', fill=(30, 30, 30))
    im.save(src)
    ann = {'mask': [{'x': 0.59, 'y': 0.17, 'w': 0.28, 'h': 0.09}], 'badges': [{'x': 0.5, 'y': 0.55, 'label': '1'}, {'x': 0.3, 'y': 0.7, 'label': '2'}]}
    dst = os.path.join(tmp, 't.webp')
    _, size = convert_to_webp(src, dst, ann=ann)
    ok = os.path.exists(dst) and size[0] == MAXW_DEFAULT and os.path.getsize(dst) > 0
    # verify it is a real WEBP
    with Image.open(dst) as v:
        fmt_ok = (v.format == 'WEBP')
    print('SELF-TEST webp=%s size=%s bytes=%d format_ok=%s -> %s' % (dst, size, os.path.getsize(dst), fmt_ok, 'PASS' if (ok and fmt_ok) else 'FAIL'))
    return 0 if (ok and fmt_ok) else 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slug', nargs='?')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    ap.add_argument('--file', nargs=2, metavar=('SRC', 'DST'))
    ap.add_argument('--maxw', type=int, default=MAXW_DEFAULT)
    ap.add_argument('--q', type=int, default=Q_DEFAULT)
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if a.file:
        dst, size = convert_to_webp(a.file[0], a.file[1], a.maxw, a.q, _ann_for(a.file[0]))
        print('converted', dst, size); return
    if a.all:
        if not os.path.isdir(IMG_ROOT):
            print('no images root:', IMG_ROOT); return
        tot = sum(process_slug(s, a.maxw, a.q) for s in sorted(os.listdir(IMG_ROOT)) if os.path.isdir(os.path.join(IMG_ROOT, s)))
        print('TOTAL converted', tot); return
    if a.slug:
        print(process_slug(a.slug, a.maxw, a.q), 'converted for', a.slug); return
    ap.print_help()

if __name__ == '__main__':
    main()
