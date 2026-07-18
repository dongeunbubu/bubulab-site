#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""무료 단독 페이지 생성기 (파일럿: bookcol-youthchoice)
사용법:  python3 build_free_page.py bookcol-youthchoice [--url youth-savings]
산출  :  imweb_cdn/free-<이름>__BODY.html · free-<이름>__FOOTER.html
구성  :  BODY = 홈 정본 헤더(콘텐츠 허브 정본 재사용) + OG 메타 + 리더 CSS 내장
              + 조각 인라인(#cxRdBody) + 엔드 모듈 슬롯(#cxEnd) + 베이지 푸터(.bbft)
        FOOTER = script1 엔진(라우터·탐색기·허브부트 구간 제거 → FREE1 경량 부트 치환)
               + 모바일 드로어 + bb-hdrsync (원문 그대로)
게이트 :  node --check · 태그 균형 · HTML 주석 0 · 위젯 등록 커버리지 · 마운트 스모크(node)
        · 홈 정본 마커(B1/aria-label/row-gap:0/베이지) · OG 메타 · 멱등(2회 빌드 동일)
"""
import json, os, re, subprocess, sys, tempfile

GEN  = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(GEN)
CDN  = os.path.join(ROOT, 'imweb_cdn')
SITE = 'https://bubulab.co.kr'
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def atomic_write(path, data):
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix='.tmp_')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(data)
        os.replace(tmp, path)
        os.chmod(path, 0o644)
    except BaseException:
        try: os.unlink(tmp)
        except OSError: pass
        raise

def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

# ---------- 원자재 추출 ----------

def style_blocks(txt):
    return [m.group(0) for m in re.finditer(r'<style[^>]*>.*?</style>', txt, re.S)]

def pick_style(blocks, needle):
    for b in blocks:
        if needle in b:
            return b
    raise SystemExit('style block not found: ' + needle)

def build(slug, url_slug=None):
    hub  = read(os.path.join(CDN, 'contents__BODY.html'))
    foot = read(os.path.join(CDN, 'contents__FOOTER.html'))
    idx  = json.load(open(os.path.join(ROOT, 'contents', 'contents_index.json'), encoding='utf-8'))
    items = idx['items'] if isinstance(idx, dict) else idx
    item = next((it for it in items if it.get('slug') == slug), None)
    if not item:
        raise SystemExit('index에 슬러그가 없어요: ' + slug)
    page = 'free-' + slug.split('-', 1)[1]
    url = url_slug or page

    frag = read(os.path.join(ROOT, 'contents', 'columns', slug + '.html'))
    frag = re.sub(r'<!--.*?-->', '', frag, flags=re.S)
    for p in ('bookcol-', 'booktool-', 'kit-'):
        frag = frag.replace('href="#' + p, 'href="/contents#' + p)
    frag = frag.strip('\n')

    sb = style_blocks(hub)
    st_base   = pick_style(sb, '#hdr .nav{row-gap:0}')      # 토큰+헤더+리더 기본+카탈로그
    st_navmob = pick_style(sb, '#hdr .navMobBtn')            # 모바일 드로어 CSS
    st_cxx    = pick_style(sb, 'cx-functab')                 # cxX 확장(.cx-thm 등)
    st_cxv2   = pick_style(sb, 'cx-em-card')                 # 리더 v2 + CXW 위젯 CSS
    st_sweep  = pick_style(sb, 'data-bbsweep')               # 고정 헤더 + 베이지 푸터

    font = hub.split('\n', 1)[0]
    if not font.startswith('<link'):
        raise SystemExit('폰트 링크 라인을 못 찾았어요')
    hdr_a = hub.index('<div class="topbar">')
    hdr_b = hub.index('<div class="cx-page" id="cxRoot">')
    header = hub[hdr_a:hdr_b].rstrip('\n')
    m = re.search(r'<footer class="bbft">.*?</footer>', hub, re.S)
    footer_mk = m.group(0)
    m = re.search(r'<button class="cx-top"[^>]*>[^<]*</button>', hub)
    cxtop_mk = m.group(0)

    # ---------- BODY ----------
    og_title = item['title'] + ' | 부부연구소'
    og_desc  = item.get('hook') or item.get('sub') or ''
    og = '\n'.join([
        '<meta property="og:type" content="article">',
        '<meta property="og:title" content="%s">' % esc(og_title),
        '<meta property="og:description" content="%s">' % esc(og_desc),
        '<meta property="og:url" content="%s/%s">' % (SITE, url),
        '<meta property="og:image" content="%s/og/%s.png">' % (SITE, page),
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:site_name" content="부부연구소">',
        '<meta name="description" content="%s">' % esc(og_desc),
        '<link rel="canonical" href="%s/%s">' % (SITE, url),
    ])

    mins = item.get('read') or max(3, round(item.get('pages', 3) * 1.1))
    scope = '도입 무료 공개' if item.get('premium') else '전문 무료 공개'
    badge = ('<span class="cx-b cx-b-prem">🔒 프리미엄</span>' if item.get('premium')
             else '<span class="cx-b cx-b-free">🆓 무료</span>')
    sub = ('<div class="cx-rd-subt">%s</div>' % esc(item['sub'])) if item.get('sub') else ''
    top = ('<div class="cx-rd-top"><a class="cx-rd-back" href="/contents"><i aria-hidden="true">←</i> 칼럼 전체</a>'
           '<span class="cx-rd-time">📖 약 %d분 · %s</span></div>' % (mins, scope))
    hero = ('<div class="cx-rd-hero"><div class="cx-rd-eyebrow"><span class="cx-rd-kno">칼럼 No.%02d</span>'
            '<span class="cx-rd-cat">· %s</span>%s</div><h1 class="cx-rd-h1">%s</h1>%s</div>'
            % (item['no'], esc(item.get('cat', '')), badge, esc(item['title']), sub))
    reader = '\n'.join([
        '<section class="cx-reader" id="cxReader" aria-label="칼럼 리더" data-free-slug="%s">' % slug,
        '<div class="cx-reader">',
        top, hero,
        '<div class="cx-rd-body" id="cxRdBody">',
        frag,
        '</div>',
        '<div id="cxEnd" class="cx-endslot"></div>',
        '</div>',
        '</section>',
    ])
    snap = ('<script type="application/json" id="cxSnap">%s</script>'
            % json.dumps(items, ensure_ascii=False))

    body = '\n'.join([
        font, og, st_base,
        '<div class="bbfw">',
        st_navmob, st_cxx,
        header,
        '<div class="cx-page" id="cxRoot">',
        '<div class="cx-prog" id="cxProg" aria-hidden="true"><span id="cxProgBar"></span></div>',
        st_cxv2,
        reader,
        footer_mk,
        cxtop_mk,
        snap,
        '</div>',
        st_sweep,
        '</div>',
        '',
    ])

    # ---------- FOOTER ----------
    scripts = re.findall(r'<script>.*?</script>', foot, re.S)
    if len(scripts) != 4:
        raise SystemExit('contents__FOOTER script 블록 수가 4가 아니에요: %d' % len(scripts))
    eng, drawer, hdrsync = scripts[0], scripts[2], scripts[3]
    js = eng[len('<script>'):-len('</script>')]
    cutmark = '/* ================= 라우터 ================= */'
    if cutmark not in js:
        raise SystemExit('라우터 마커를 못 찾았어요')
    head = js[:js.index(cutmark)]
    boot = LIGHT_BOOT
    footer_out = '<script>' + head + boot + '\n})();\n</script>\n' + drawer + '\n' + hdrsync + '\n'
    return page, item, body, footer_out

LIGHT_BOOT = """/* ================= FREE1 · 무료 단독 페이지 경량 부트 — 라우터·탐색기 제외, 인라인 조각 즉시 init, 엔드 모듈은 인덱스 fetch 렌더 ================= */
 /* FREE1 진행바: contents updateProg 이식 — 라우터 분기 제거, 리더 상시 on */
 var progTick=false;
 function updateProg(){
  var bar=d.getElementById('cxProgBar'),pg=d.getElementById('cxProg');if(!bar||!pg)return;
  pg.classList.add('on');
  var doc=d.documentElement,st=doc.scrollTop||d.body.scrollTop||0,h=(doc.scrollHeight-doc.clientHeight)||1;
  bar.style.width=Math.min(100,Math.max(0,st/h*100)).toFixed(2)+'%';
 }
 var FREE=(function(){var el=d.getElementById('cxReader');return el?{rd:el,slug:el.getAttribute('data-free-slug')||''}:null;})();
 try{[].slice.call(d.querySelectorAll('meta[property^="og:"],meta[name="description"]')||[]).forEach(function(mt){if(d.head&&mt.parentNode!==d.head)d.head.appendChild(mt);});}catch(e){}
 function freeLinks(root){if(!root||!root.querySelectorAll)return;[].slice.call(root.querySelectorAll('a[href^="#"]')).forEach(function(a){var h=a.getAttribute('href')||'';if(h.length<2||h.indexOf('@')>=0)return;a.setAttribute('href','/contents'+h);});}
 function freeEnd(){if(!FREE||!FREE.slug)return;var host=d.getElementById('cxEnd');if(!host||!ALL.length)return;var it=findItem(FREE.slug);if(!it)return;host.innerHTML=endModuleHTML(it);freeLinks(host);reveal(host,'.cx-rv');}
 function freeBoot(){
  if(!FREE)return;
  var body=d.getElementById('cxRdBody')||FREE.rd;
  try{CXW.mount(body);}catch(e){}
  try{wireTerms(FREE.rd);}catch(e){}
  var it=findItem(FREE.slug);
  try{if(CXW.reader&&CXW.reader.init)CXW.reader.init(body,FREE.slug,it);}catch(e){}
  reveal(body,'.cx-sc');reveal(FREE.rd,'.cx-rv');
  freeLinks(FREE.rd);
  freeEnd();
  updateProg();
 }
 if(snap&&snap.length)useData(snap);
 freeBoot();
 if(window.fetch){
  fetch(RAW+'?cb='+Date.now(),{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json();}).then(function(j){var it=j&&j.items;if(it&&it.length){useData(it);freeEnd();}}).catch(function(){});
  fetch(LEG_RAW+'?cb='+Date.now(),{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json();}).then(function(j){var it=(j&&j.items)||j;if(it&&it.length){useLegacy(it);freeEnd();}}).catch(function(){});
 }
 var tp=d.getElementById('cxtop');
 addEventListener('scroll',function(){
  if(tp)tp.classList.toggle('on',(d.documentElement.scrollTop||d.body.scrollTop||0)>600);
  if(!progTick){progTick=true;var _pr=function(){progTick=false;updateProg();};requestAnimationFrame(_pr);setTimeout(_pr,120);}
 },{passive:true});
 d.addEventListener('visibilitychange',function(){if(!d.hidden)updateProg();});
 if(tp)tp.addEventListener('click',function(){scrollTo({top:0,behavior:rm?'auto':'smooth'});});
"""

# ---------- 게이트 ----------

def gate_comments(name, txt):
    n = txt.count('<!--')
    print('  [%s] HTML 주석: %d %s' % (name, n, 'PASS' if n == 0 else 'FAIL'))
    return n == 0

def gate_balance(name, txt):
    from html.parser import HTMLParser
    class P(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.stack = []; self.bad = []
        def handle_starttag(self, tag, attrs):
            if tag not in VOID: self.stack.append(tag)
        def handle_endtag(self, tag):
            if tag in VOID: return
            if self.stack and self.stack[-1] == tag:
                self.stack.pop()
            elif tag in self.stack:
                while self.stack and self.stack[-1] != tag:
                    self.bad.append('unclosed:' + self.stack.pop())
                if self.stack: self.stack.pop()
            else:
                self.bad.append('stray:' + tag)
    p = P(); p.feed(txt); p.close()
    ok = not p.stack and not p.bad
    print('  [%s] 태그 균형: %s%s' % (name, 'PASS' if ok else 'FAIL',
          '' if ok else ' 잔여=%s 오류=%s' % (p.stack[:6], p.bad[:6])))
    return ok

def gate_markers(body):
    need = {
        'B1 로고(하트 C9A84C)': 'C9A84C',
        'aria-label 홈으로': 'aria-label="홈으로"',
        'row-gap:0': '#hdr .nav{row-gap:0}',
        '베이지 푸터 CSS': 'background:#F3ECDF',
        '베이지 푸터 마크업': '<footer class="bbft">',
        'og:type': 'property="og:type"',
        'og:title': 'property="og:title"',
        'og:description': 'property="og:description"',
        'og:url': 'property="og:url"',
        'og:image': 'property="og:image"',
        '헤더 스페이서': 'bbhdr-spacer',
        '리더 루트': 'id="cxRoot"',
        '리더 섹션': 'id="cxReader"',
        '본문 슬롯': 'id="cxRdBody"',
        '엔드 모듈 슬롯': 'id="cxEnd"',
        '인덱스 스냅샷': 'id="cxSnap"',
    }
    ok = True
    for k, v in need.items():
        hit = v in body
        if not hit: ok = False
        print('  [BODY] 마커 %-14s %s' % (k, 'PASS' if hit else 'FAIL(' + v + ')'))
    return ok

def gate_widget_coverage(body, footer):
    names = sorted(set(re.findall(r'data-cx-w="([^"]+)"', body)))
    miss = [n for n in names if ("'" + n + "'") not in footer]
    print('  [X] 위젯 커버리지: %d종 %s%s' % (len(names), 'PASS' if not miss else 'FAIL', '' if not miss else ' 누락=' + ','.join(miss)))
    return not miss, names

def gate_node(footer_path):
    txt = read(footer_path)
    blocks = re.findall(r'<script>(.*?)</script>', txt, re.S)
    ok = True
    for i, b in enumerate(blocks):
        p = os.path.join(GEN, '_free_chk_%d.js' % i)
        atomic_write(p, b)
        r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
        if r.returncode != 0:
            ok = False
            print('  [FOOTER] node --check 블록%d FAIL\n%s' % (i, r.stderr[:500]))
    print('  [FOOTER] node --check: %d블록 %s' % (len(blocks), 'PASS' if ok else 'FAIL'))
    return ok

def gate_smoke(body_path, footer_path, slug):
    r = subprocess.run(['node', os.path.join(GEN, 'free_smoke.js'), body_path, footer_path, slug],
                       capture_output=True, text=True)
    out = (r.stdout or '').strip()
    print('  [SMOKE] ' + (out if out else '(no output)'))
    if r.returncode != 0:
        print('  [SMOKE] FAIL\n' + (r.stderr or '')[:800])
    return r.returncode == 0

def gate_url(body, url):
    og  = '<meta property="og:url" content="%s/%s">' % (SITE, url)
    can = '<link rel="canonical" href="%s/%s">' % (SITE, url)
    hit = og in body and can in body
    print('  [BODY] og:url+canonical /%s: %s' % (url, 'PASS' if hit else 'FAIL'))
    return hit

def gate_prog(body, footer):
    hits = ('id="cxProg"' in body, 'id="cxProgBar"' in body,
            "getElementById('cxProgBar')" in footer,
            'function updateProg(){}' not in footer)
    ok = all(hits)
    print('  [진행바] 마크업+updateProg 실장: %s' % ('PASS' if ok else 'FAIL ' + repr(hits)))
    return ok

def main():
    args = sys.argv[1:]
    url_slug = None
    if '--url' in args:
        i = args.index('--url')
        if i + 1 >= len(args):
            raise SystemExit('--url 뒤에 슬러그가 필요해요')
        url_slug = args[i + 1]
        del args[i:i + 2]
    slug = args[0] if args else 'bookcol-youthchoice'
    page, item, body, footer = build(slug, url_slug)
    page2, _, body2, footer2 = build(slug, url_slug)
    idem = (body == body2 and footer == footer2)

    bp = os.path.join(CDN, page + '__BODY.html')
    fp = os.path.join(CDN, page + '__FOOTER.html')
    atomic_write(bp, body)
    atomic_write(fp, footer)
    print('빌드: %s (%s · No.%02d · %d분)' % (page, item['title'], item['no'], item.get('read', 0)))
    print('  BODY   %7d bytes → %s' % (len(body.encode('utf-8')), bp))
    print('  FOOTER %7d bytes → %s' % (len(footer.encode('utf-8')), fp))

    ok = True
    ok &= gate_comments('BODY', body)
    ok &= gate_comments('FOOTER', footer)
    ok &= gate_balance('BODY', body)
    ok &= gate_markers(body)
    w_ok, names = gate_widget_coverage(body, footer)
    ok &= w_ok
    ok &= gate_url(body, url_slug or page)
    ok &= gate_prog(body, footer)
    ok &= gate_node(fp)
    ok &= gate_smoke(bp, fp, slug)
    print('  [멱등] 2회 빌드 동일: %s' % ('PASS' if idem else 'FAIL'))
    ok &= idem
    print('게이트 종합: %s' % ('ALL PASS' if ok else 'FAIL 있음'))
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
