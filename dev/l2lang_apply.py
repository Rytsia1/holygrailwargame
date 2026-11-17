"""11-18: 로비 2단계 왼쪽 위 언어 버튼을 1단계처럼 — 지구본 + 지금 언어 이름 + ▾, 누르면 같은 언어 창
- 예전: 「한 · EN · 日」 세 버튼(중국어 없음)
- 이제: 1단계의 #langBtn과 같은 모양의 버튼 하나. 누르면 1단계와 같은 언어 창(#langDlg, 중국어 포함)을 연다
사용: python3 l2lang_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'l2-lgb' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)
GLOBE = ('<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="7.2" fill="none" stroke="currentColor" stroke-width="1.3"/>'
         '<ellipse cx="10" cy="10" rx="3.1" ry="7.2" fill="none" stroke="currentColor" stroke-width="1.1"/>'
         '<path d="M3 10h14M4.2 6.3h11.6M4.2 13.7h11.6" fill="none" stroke="currentColor" stroke-width="1"/></svg>')
CV = '<svg class="cv" viewBox="0 0 10 10" aria-hidden="true"><path d="M1.5 3.5 5 7l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'
rp("""<div class="l2-lang" role="group" aria-label="Language" data-notr>${['ko','en','ja'].map(l=>`<button type="button" data-l="${l}" lang="${l}"${l===LG?' class="on" aria-pressed="true"':' aria-pressed="false"'}>${{ko:'한',en:'EN',ja:'日'}[l]}</button>`).join('')}</div>""",
   """<div class="l2-lang lg-one" data-notr><button type="button" class="lg-btn l2-lgb" aria-haspopup="dialog" aria-label="Language">""" + GLOBE +
   """<span class="lg-cur">${((typeof LANG_LIST!=='undefined'?LANG_LIST:[]).find(x=>x[0]===LG)||[0,LG])[1]}</span>""" + CV + """</button></div>""")
rp("""  lb2.querySelectorAll('.l2-lang button').forEach(b=>b.onclick=()=>{ if(b.dataset.l!==LG&&typeof setLang==='function') setLang(b.dataset.l); });""",
   """  lb2.querySelectorAll('.l2-lgb').forEach(b=>b.onclick=()=>{ const o=document.getElementById('langBtn'); if(o) o.click(); });   // 1단계와 같은 언어 창 (11-18)""")
rp("#lb2 .l2-lang button.on::after{", "#lb2 .l2-lang .lg-btn{height:100%!important;font-size:12.5px;white-space:nowrap}#lb2 .l2-top .l2-back{white-space:nowrap}"
   "@media (max-width:379px){#lb2 .l2-lang .lg-cur{display:none}#lb2 .l2-lang .lg-btn{padding:0 8px!important;gap:4px}}@media (max-width:340px){#lb2 .l2-lang .cv{display:none}}#lb2 .l2-lang button.on::after{")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
print('적용 끝')
