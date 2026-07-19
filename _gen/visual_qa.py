#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""visual_qa.py — 시각 QA 게이트 (#5)
입력 URL(라이브 or 로컬 파일) → Playwright 풀페이지 캡처(데스크톱 1920 · 모바일 390)
자동 검사:
  1) 요소 겹침    — 텍스트 노드 bounding box 교차(비-조상/자손 쌍, 면적비 임계)
  2) 가로 오버플로 — documentElement scrollWidth>clientWidth + 뷰포트 밖 요소
  3) 이미지 깨짐   — <img> naturalWidth===0
  4) 대비 미달 후보 — WCAG 대비비 < 임계(대형 3.0 / 본문 4.5)
  5) sticky 잘림   — position sticky/fixed 요소가 뷰포트 밖 또는 고정 헤더 뒤로 잘림
산출: <out>/<label>__<vp>.png · <label>__<vp>__annotated.png · <label>__report.json
사용: python3 visual_qa.py <url|file> [--label NAME] [--out DIR] [--viewports desktop,mobile]
종료: 리포트 생성 성공=0 (결함은 데이터로 기록 · 실행 실패만 비0)
"""
import sys, os, re, json, time, argparse
# 번들 시스템 라이브러리(_qalibs)를 LD_LIBRARY_PATH에 선주입 — 무권한 샌드박스 chromium 실행 보정
_QALIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_qalibs')
if os.path.isdir(_QALIB):
    os.environ['LD_LIBRARY_PATH'] = _QALIB + os.pathsep + os.environ.get('LD_LIBRARY_PATH', '')
from urllib.parse import urlparse

def to_url(s):
    if re.match(r'^https?://', s) or s.startswith('file://'):
        return s
    p = os.path.abspath(s)
    if not os.path.exists(p):
        raise SystemExit('입력 경로/URL이 없어요: ' + s)
    return 'file://' + p

def label_from(url, given):
    if given: return re.sub(r'[^A-Za-z0-9._-]+', '-', given).strip('-')
    u = urlparse(url)
    base = (u.path or '/').rstrip('/').split('/')[-1] or (u.netloc or 'page')
    return re.sub(r'[^A-Za-z0-9._-]+', '-', base).strip('-') or 'page'

# ---- in-page 검사 스크립트 (모든 좌표는 document 절대좌표) ----
PROBE = r"""
(() => {
  const SX = window.scrollX||document.documentElement.scrollLeft||0;
  const SY = window.scrollY||document.documentElement.scrollTop||0;
  const VW = window.innerWidth, VH = window.innerHeight;
  const abox = (r) => ({x:r.left+SX, y:r.top+SY, w:r.width, h:r.height, right:r.right+SX, bottom:r.bottom+SY, top:r.top, vpBottom:r.bottom});
  const vis = (el) => {
    const cs = getComputedStyle(el);
    if (cs.visibility==='hidden'||cs.display==='none') return false;
    if (parseFloat(cs.opacity||'1') < 0.06) return false;
    const r = el.getBoundingClientRect();
    return r.width>1 && r.height>1;
  };
  const pathOf = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#'+el.id;
    if (el.className && typeof el.className==='string') s += '.'+el.className.trim().split(/\s+/).slice(0,3).join('.');
    return s;
  };
  const parseColor = (c) => {
    const m = (c||'').match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(',').map(x=>parseFloat(x));
    return {r:p[0],g:p[1],b:p[2],a:(p.length>3?p[3]:1)};
  };
  const lum = (c) => {
    const f = (v)=>{v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4);};
    return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b);
  };
  const ratio = (a,b) => { const L1=lum(a),L2=lum(b); const hi=Math.max(L1,L2),lo=Math.min(L1,L2); return (hi+0.05)/(lo+0.05); };
  const effBg = (el) => {
    let n = el;
    while (n && n.nodeType===1) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage && cs.backgroundImage!=='none') return null; // 그라디언트/이미지 → 스킵
      const bc = parseColor(cs.backgroundColor);
      if (bc && bc.a>0.5) return bc;
      n = n.parentElement;
    }
    return {r:255,g:255,b:255,a:1};
  };

  // ---- 텍스트 원자(rect) 수집 (Range 기반) ----
  const atoms = []; // {x,y,w,h,owner,ownerId,tag,text}
  const owners = []; // element list, index = ownerId
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode(node){
      const t = (node.nodeValue||'').trim();
      if (t.length < 2) return NodeFilter.FILTER_REJECT;
      const pe = node.parentElement;
      if (!pe || !vis(pe)) return NodeFilter.FILTER_REJECT;
      const tag = pe.tagName.toLowerCase();
      if (tag==='script'||tag==='style'||tag==='noscript') return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    }
  });
  let tn, count=0;
  while ((tn = walker.nextNode()) && count < 6000) {
    const pe = tn.parentElement;
    let oid = owners.indexOf(pe);
    if (oid<0){ oid = owners.length; owners.push(pe); }
    const rng = document.createRange(); rng.selectNodeContents(tn);
    const rects = rng.getClientRects();
    for (let i=0;i<rects.length;i++){
      const r = rects[i];
      if (r.width<3||r.height<3) continue;
      const b = abox(r);
      atoms.push({x:b.x,y:b.y,w:b.w,h:b.h,owner:oid,tag:pe.tagName.toLowerCase(),text:(tn.nodeValue||'').trim().slice(0,40)});
      count++;
    }
  }
  // 아이콘/이미지 원자(겹침 판정 보강)
  const iconEls = [].slice.call(document.querySelectorAll('img,svg,i,button,[class*="icon"],[class*="ic-"]'));
  iconEls.forEach(el=>{
    if(!vis(el)) return;
    const tag=el.tagName.toLowerCase();
    if(tag==='i'||tag==='button'){ if((el.textContent||'').trim().length>1) return; }
    let oid = owners.indexOf(el); if(oid<0){oid=owners.length;owners.push(el);}
    const b = abox(el.getBoundingClientRect());
    if(b.w<6||b.h<6||b.w>72||b.h>72) return; // 소형 아이콘/배지만(대형 위젯 그래픽=의도적 레이어 → 제외)
    atoms.push({x:b.x,y:b.y,w:b.w,h:b.h,owner:oid,tag:tag,text:'[icon]',icon:true});
  });

  const related = (a,b) => (a===b) || owners[a].contains(owners[b]) || owners[b].contains(owners[a]);
  const inter = (A,B) => {
    const ix = Math.max(0, Math.min(A.x+A.w,B.x+B.w)-Math.max(A.x,B.x));
    const iy = Math.max(0, Math.min(A.y+A.h,B.y+B.h)-Math.max(A.y,B.y));
    return ix*iy;
  };
  // ---- 1) 겹침 ----
  const overlaps = []; const seenPair = {};
  for (let i=0;i<atoms.length;i++){
    for (let j=i+1;j<atoms.length;j++){
      const A=atoms[i],B=atoms[j];
      if (A.owner===B.owner) continue;
      if (Math.abs(A.y-B.y) > Math.max(A.h,B.h)+40) continue; // y 근접만
      if (related(A.owner,B.owner)) continue;
      const ov = inter(A,B);
      if (ov<=0) continue;
      const minA = Math.min(A.w*A.h, B.w*B.h);
      const rr = ov/minA;
      if (rr < 0.35 || ov < 90) continue;
      const key = A.owner<B.owner ? A.owner+'-'+B.owner : B.owner+'-'+A.owner;
      const bx = {x:Math.max(A.x,B.x),y:Math.max(A.y,B.y),
                  w:Math.min(A.x+A.w,B.x+B.w)-Math.max(A.x,B.x),
                  h:Math.min(A.y+A.h,B.y+B.h)-Math.max(A.y,B.y)};
      if (seenPair[key]){ if(ov>seenPair[key].area){seenPair[key]={area:ov,box:bx,a:A,b:B};} continue; }
      seenPair[key] = {area:ov,box:bx,a:A,b:B};
    }
  }
  Object.keys(seenPair).forEach(k=>{
    const s=seenPair[k];
    overlaps.push({box:s.box, ratio:+(s.area/Math.min(s.a.w*s.a.h,s.b.w*s.b.h)).toFixed(2),
      a:{sel:pathOf(owners[s.a.owner]),tag:s.a.tag,text:s.a.text},
      b:{sel:pathOf(owners[s.b.owner]),tag:s.b.tag,text:s.b.text}});
  });
  overlaps.sort((p,q)=>(q.box.w*q.box.h)-(p.box.w*p.box.h));

  // ---- 2) 가로 오버플로 ----
  const de = document.documentElement;
  const pageOverflow = de.scrollWidth - de.clientWidth;
  const overflowEls = [];
  const all = [].slice.call(document.body.querySelectorAll('*'));
  for (const el of all){
    if(!vis(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 4 || r.width > VW+2) continue;
    if (r.right > VW+2 && r.left >= -1){
      overflowEls.push({sel:pathOf(el), over:+(r.right-VW).toFixed(1), box:abox(r)});
    }
    if (overflowEls.length>=40) break;
  }
  overflowEls.sort((a,b)=>b.over-a.over);

  // ---- 3) 이미지 깨짐 ----
  const broken = [];
  [].slice.call(document.images).forEach(im=>{
    const bad = (im.complete && im.naturalWidth===0) || (!im.getAttribute('src') && !im.srcset);
    if (bad){ const b=abox(im.getBoundingClientRect()); broken.push({src:im.currentSrc||im.getAttribute('src')||'(none)', alt:im.alt||'', box:b}); }
  });

  // ---- 4) 대비 미달 후보 ----
  const lowc = []; const seenC={};
  for (let oi=0; oi<owners.length; oi++){
    const el = owners[oi];
    if (!el || el.nodeType!==1) continue;
    const txt = (el.textContent||'').trim();
    if (txt.length<2) continue;
    if (!vis(el)) continue;
    const cs = getComputedStyle(el);
    const fg = parseColor(cs.color); if(!fg||fg.a<0.5) continue;
    const bg = effBg(el); if(!bg) continue;
    const rr = ratio(fg,bg);
    const fsize = parseFloat(cs.fontSize)||16;
    const fw = parseInt(cs.fontWeight)||400;
    const large = fsize>=24 || (fsize>=18.66 && fw>=700);
    const thr = large?3.0:4.5;
    if (rr < thr){
      const key = pathOf(el);
      if (seenC[key]) continue; seenC[key]=1;
      const b = abox(el.getBoundingClientRect());
      lowc.push({sel:key, ratio:+rr.toFixed(2), threshold:thr, fontPx:+fsize.toFixed(1),
        fg:[Math.round(fg.r),Math.round(fg.g),Math.round(fg.b)], bg:[Math.round(bg.r),Math.round(bg.g),Math.round(bg.b)],
        text:txt.slice(0,40), box:b});
    }
    if (lowc.length>=60) break;
  }

  // ---- 5) sticky/fixed 잘림 ----
  // 고정 헤더 하단(맨 위 고정 요소들의 최대 bottom)
  let headerBottom = 0;
  for (const el of all){
    const cs = getComputedStyle(el);
    if (cs.position!=='fixed') continue;
    const r = el.getBoundingClientRect();
    if (r.top>-4 && r.top<130 && r.width>VW*0.4 && r.height<220 && r.bottom<VH*0.45)
      headerBottom = Math.max(headerBottom, r.bottom);
  }
  const stickyCut = [];
  for (const el of all){
    const cs = getComputedStyle(el);
    if (cs.position!=='sticky' && cs.position!=='fixed') continue;
    if (!vis(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width<8||r.height<8) continue;
    if (r.bottom<=2 || r.top>=VH-2) continue; // 현재 뷰포트 밖(아래 미도달) 요소는 잘림 아님 → 제외
    const issues=[];
    if (r.top < -2) issues.push('상단 '+Math.round(-r.top)+'px 뷰포트밖 잘림');
    if (r.height > VH+2 && cs.position==='sticky') issues.push('높이 '+Math.round(r.height)+'px > 뷰포트 '+VH+'px (고정 시 하단 잘림)');
    if (headerBottom>4 && r.top < headerBottom-4 && cs.position!=='fixed')
      issues.push('고정헤더('+Math.round(headerBottom)+'px) 뒤로 '+Math.round(headerBottom-r.top)+'px 가림');
    if (issues.length){
      stickyCut.push({sel:pathOf(el), position:cs.position, top:Math.round(r.top), bottom:Math.round(r.bottom), height:Math.round(r.height), issues:issues, box:abox(r)});
    }
    if (stickyCut.length>=40) break;
  }

  // ---- 6) 내용 있으나 높이 0 붕괴(collapsed) — 모바일 본문 미표시 등 ----
  const collapsed = [];
  [].slice.call(document.querySelectorAll('#cxRdBody,.cx-rd-body,.cx-ch,article,section,main,[class*="cx-rd"]')).forEach(el=>{
    const cs = getComputedStyle(el);
    if (cs.display==='none'||cs.visibility==='hidden'||parseFloat(cs.opacity||'1')<0.06) return;
    const txt = (el.textContent||'').replace(/\s+/g,' ').trim();
    if (txt.length < 150) return;
    const r = el.getBoundingClientRect();
    if (r.height < 3 || r.width < 3){
      collapsed.push({sel:pathOf(el), textLen:txt.length, height:Math.round(r.height), width:Math.round(r.width), text:txt.slice(0,48), box:abox(r)});
    }
  });

  return {
    viewport:{w:VW,h:VH}, scroll:{x:SX,y:SY},
    page:{scrollWidth:de.scrollWidth, clientWidth:de.clientWidth, docHeight:de.scrollHeight},
    headerBottom:Math.round(headerBottom),
    counts:{overlap:overlaps.length, overflow:overflowEls.length, brokenImg:broken.length, lowContrast:lowc.length, stickyCut:stickyCut.length, collapsed:collapsed.length},
    overlaps:overlaps.slice(0,40), overflow:{page:+pageOverflow.toFixed(1), elements:overflowEls.slice(0,20)},
    brokenImg:broken.slice(0,40), lowContrast:lowc.slice(0,40), stickyCut:stickyCut.slice(0,30), collapsed:collapsed.slice(0,25)
  };
})()
"""

ANNOTATE = r"""
(defects) => {
  const wrap = document.createElement('div');
  wrap.id='__qa_overlay__';
  wrap.style.cssText='position:absolute;left:0;top:0;width:0;height:0;z-index:2147483000;pointer-events:none';
  const COL = {overlap:'#e53935', overflow:'#8e24aa', brokenImg:'#00897b', lowContrast:'#fb8c00', stickyCut:'#3949ab', collapsed:'#d81b60'};
  const mk = (b,color,label) => {
    if(!b||!isFinite(b.x)) return;
    const d = document.createElement('div');
    d.style.cssText='position:absolute;left:'+b.x+'px;top:'+b.y+'px;width:'+Math.max(4,b.w)+'px;height:'+Math.max(4,b.h)+'px;'
      +'border:2.5px solid '+color+';box-shadow:0 0 0 1px #fff;box-sizing:border-box;pointer-events:none';
    const t = document.createElement('span');
    t.textContent=label;
    t.style.cssText='position:absolute;left:0;top:-15px;font:700 10px/13px system-ui,sans-serif;color:#fff;background:'+color+';padding:0 5px;white-space:nowrap;border-radius:2px';
    d.appendChild(t); wrap.appendChild(d);
  };
  (defects.overlaps||[]).forEach((o,i)=>mk(o.box,COL.overlap,'겹침#'+(i+1)));
  ((defects.overflow&&defects.overflow.elements)||[]).forEach((o,i)=>mk(o.box,COL.overflow,'오버플로 +'+o.over));
  (defects.brokenImg||[]).forEach((o,i)=>mk(o.box,COL.brokenImg,'이미지깨짐'));
  (defects.lowContrast||[]).forEach((o,i)=>mk(o.box,COL.lowContrast,'대비 '+o.ratio));
  (defects.stickyCut||[]).forEach((o,i)=>mk(o.box,COL.stickyCut,'sticky잘림'));
  (defects.collapsed||[]).forEach((o,i)=>mk(o.box,COL.collapsed,'높이붕괴 '+o.height+'px'));
  document.body.appendChild(wrap);
  return true;
}
"""

AUTOSCROLL = r"""
async () => {
  await new Promise(res => {
    let y=0; const step=()=>{ window.scrollBy(0, 700); y+=700;
      if (y < document.documentElement.scrollHeight) setTimeout(step, 90); else { window.scrollTo(0,0); setTimeout(res, 400); } };
    step();
  });
}
"""

def run_vp(page, name, w, h, url, out, label):
    page.goto(url, wait_until='load', timeout=45000)
    try: page.wait_for_load_state('networkidle', timeout=8000)
    except Exception: pass
    page.wait_for_timeout(1800)          # 리더 JS 마운트 + hdrsync
    # content-visibility:auto(.cx-ch-lazy) 강제 렌더 — 오프스크린 붕괴 측정 아티팩트/모바일 미전개 방지
    try: page.add_style_tag(content='*{content-visibility:visible !important}')
    except Exception: pass
    page.wait_for_timeout(350)
    try: page.evaluate(AUTOSCROLL)       # lazy reveal 유도
    except Exception: pass
    page.wait_for_timeout(500)
    shot = os.path.join(out, '%s__%s.png' % (label, name))
    page.screenshot(path=shot, full_page=True)
    defects = page.evaluate(PROBE)
    try:
        page.evaluate(ANNOTATE, defects)
        page.wait_for_timeout(150)
        ashot = os.path.join(out, '%s__%s__annotated.png' % (label, name))
        page.screenshot(path=ashot, full_page=True)
    except Exception as e:
        ashot = None
        defects['_annotate_error'] = str(e)
    defects['viewport_name'] = name
    defects['screenshot'] = os.path.basename(shot)
    defects['annotated'] = os.path.basename(ashot) if ashot else None
    return defects

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('--label', default=None)
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qa_out'))
    ap.add_argument('--viewports', default='desktop,mobile')
    args = ap.parse_args()

    url = to_url(args.url)
    label = label_from(url, args.label)
    os.makedirs(args.out, exist_ok=True)
    VPS = {'desktop': (1920, 1080), 'mobile': (390, 844)}
    want = [v.strip() for v in args.viewports.split(',') if v.strip() in VPS]

    MOBILE_UA = ('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) '
                 'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
    from playwright.sync_api import sync_playwright
    report = {'url': url, 'label': label, 'ts': int(time.time()), 'viewports': {}}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--no-sandbox', '--disable-dev-shm-usage'])
        for name in want:
            w, h = VPS[name]
            mobile = (name == 'mobile')
            kw = dict(viewport={'width': w, 'height': h}, ignore_https_errors=True,
                      device_scale_factor=(2 if mobile else 1))
            if mobile:
                kw.update(user_agent=MOBILE_UA, is_mobile=True, has_touch=True)
            ctx = browser.new_context(**kw)              # 뷰포트별 신선 컨텍스트(UA/상태 격리)
            page = ctx.new_page()
            try:
                report['viewports'][name] = run_vp(page, name, w, h, url, args.out, label)
            except Exception as e:
                report['viewports'][name] = {'error': str(e)}
            finally:
                ctx.close()
        browser.close()

    # 요약
    tot = {'overlap':0,'overflow':0,'brokenImg':0,'lowContrast':0,'stickyCut':0,'collapsed':0}
    for name, d in report['viewports'].items():
        c = d.get('counts') or {}
        for k in tot: tot[k]+=c.get(k,0)
    report['total'] = tot
    rp = os.path.join(args.out, '%s__report.json' % label)
    with open(rp, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print('QA 리포트:', rp)
    for name, d in report['viewports'].items():
        if 'error' in d: print('  [%s] ERROR %s' % (name, d['error'])); continue
        c = d['counts']
        print('  [%s %dx%d] 겹침%d · 오버플로%d(page %+.0f) · 이미지깨짐%d · 대비후보%d · sticky잘림%d · headerBottom=%dpx'
              % (name, d['viewport']['w'], d['viewport']['h'], c['overlap'], c['overflow'],
                 d['overflow']['page'], c['brokenImg'], c['lowContrast'], c['stickyCut'], d.get('headerBottom',0))
              + ' · 붕괴%d' % c.get('collapsed',0))
    print('  합계:', tot)
    return 0

if __name__ == '__main__':
    sys.exit(main())
