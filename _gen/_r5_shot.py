import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import visual_qa as VQ
from playwright.sync_api import sync_playwright
url=VQ.to_url('qa_out/_youth_local.html'); name=sys.argv[1]
W,H=(1920,1080) if name=='desktop' else (390,844)
MUA=('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox','--disable-dev-shm-usage'])
    kw=dict(viewport={'width':W,'height':H},ignore_https_errors=True,device_scale_factor=(2 if name=='mobile' else 1))
    if name=='mobile': kw.update(user_agent=MUA,is_mobile=True,has_touch=True)
    ctx=b.new_context(**kw); pg=ctx.new_page()
    pg.goto(url,wait_until='load',timeout=45000)
    pg.wait_for_timeout(1800)
    pg.add_style_tag(content='*{content-visibility:visible !important}')
    pg.wait_for_timeout(350); pg.evaluate(VQ.AUTOSCROLL); pg.wait_for_timeout(500)
    m=pg.evaluate('''() => {
      const q=s=>document.querySelector(s);
      const scs=[].slice.call(document.querySelectorAll('.cx-rd-body .cx-sc'));
      const r=el=>el.getBoundingClientRect();
      const hero=q('.cx-rd-hero'), body=q('.cx-rd-body'), em=q('.cx-em');
      const gaps=[]; for(let i=1;i<Math.min(scs.length,5);i++) gaps.push(+(r(scs[i]).top-r(scs[i-1]).bottom).toFixed(1));
      const w=q('.cx-rd-body [data-cx-w].cxw, .cx-rd-body div[data-cx-w]');
      let wgap=null; if(w&&w.previousElementSibling) wgap=+(r(w).top-r(w.previousElementSibling).bottom).toFixed(1);
      const fig=q('.cx-fig'); let fgap=null; if(fig&&fig.previousElementSibling) fgap=+(r(fig).top-r(fig.previousElementSibling).bottom).toFixed(1);
      const qk=q('.cx-rd-quick'); let qgap=null,qpad=null; if(qk){ if(qk.previousElementSibling) qgap=+(r(qk).top-r(qk.previousElementSibling).bottom).toFixed(1); const cs=getComputedStyle(qk); qpad=cs.padding; }
      return {lite:q('.cx-reader').className.indexOf('cx-lite')>=0,
        heroToFirst:+(r(scs[0]).top-r(hero).bottom).toFixed(1),
        chapterGaps:gaps,
        bodyToEnd: em?+(r(em).top-r(body).bottom).toFixed(1):null,
        widgetGap:wgap, figGap:fgap, quickGap:qgap, quickPad:qpad};
    }''')
    print(name, json.dumps(m, ensure_ascii=False))
    pg.screenshot(path='qa_out/youth-r5__%s.png'%name, full_page=True)
    print('shot saved')
    ctx.close(); b.close()
