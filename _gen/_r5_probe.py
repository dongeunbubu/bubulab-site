#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""visual_qa.py의 동일 파이프라인(대기·content-visibility 강제·오토스크롤·PROBE)을
스크린샷 없이 실행 — 45초 샌드박스 호출 한도 안에서 카운트 산출. 검사 코드는 visual_qa에서 그대로 import."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import visual_qa as VQ

url = VQ.to_url(sys.argv[1]); label = sys.argv[2]; want = sys.argv[3].split(',')
out = sys.argv[4] if len(sys.argv) > 4 else 'qa_out'
VPS = {'desktop': (1920, 1080), 'mobile': (390, 844)}
MOBILE_UA = ('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) '
             'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
from playwright.sync_api import sync_playwright
report = {'url': url, 'label': label, 'ts': int(time.time()), 'viewports': {}}
with sync_playwright() as pw:
    browser = pw.chromium.launch(args=['--no-sandbox', '--disable-dev-shm-usage'])
    for name in want:
        w, h = VPS[name]; mobile = (name == 'mobile')
        kw = dict(viewport={'width': w, 'height': h}, ignore_https_errors=True,
                  device_scale_factor=(2 if mobile else 1))
        if mobile: kw.update(user_agent=MOBILE_UA, is_mobile=True, has_touch=True)
        ctx = browser.new_context(**kw); page = ctx.new_page()
        page.goto(url, wait_until='load', timeout=45000)
        try: page.wait_for_load_state('networkidle', timeout=8000)
        except Exception: pass
        page.wait_for_timeout(1800)
        try: page.add_style_tag(content='*{content-visibility:visible !important}')
        except Exception: pass
        page.wait_for_timeout(350)
        try: page.evaluate(VQ.AUTOSCROLL)
        except Exception: pass
        page.wait_for_timeout(500)
        d = page.evaluate(VQ.PROBE)
        d['viewport_name'] = name
        report['viewports'][name] = d
        ctx.close()
    browser.close()
tot = {}
for name, d in report['viewports'].items():
    c = d.get('counts', {})
    print('[%s] counts=%s pageOverflow=%s docH=%s' % (
        name, json.dumps(c, ensure_ascii=False), d.get('overflow', {}).get('page'), d.get('page', {}).get('docHeight')))
    for k, v in c.items(): tot[k] = tot.get(k, 0) + v
report['total'] = tot
p = os.path.join(out, label + '__report.json')
json.dump(report, open(p, 'w'), ensure_ascii=False, indent=1)
print('TOTAL', json.dumps(tot), '->', p)
