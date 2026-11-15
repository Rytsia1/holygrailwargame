"""언어 선택: 로비 위쪽의 언어 단추 하나 + 언어 창 (11-16 시안 → 적용)
- 한국어 · English · 日本語가 나란히 있던 자리를 단추 하나(지구본 · 지금 언어 · ▾)로 바꾼다. 높이 · 테두리는 소리 · 설정 단추와 같다.
- 누르면 설정 창과 같은 틀의 작은 창이 열린다(휴대폰은 아래에서, PC는 가운데).
  줄마다 큰 글씨는 그 언어로 쓴 이름, 작은 글씨는 지금 화면 언어로 쓴 이름. 지금 언어에는 '사용 중'과 ✓.
- 고르면 지금처럼 그 언어로 바로 바뀐다(다시 불러옴). 창 문구는 언어마다 직접 들고 있어 번역표를 거치지 않는다.
- 언어를 늘릴 때는 LANG_LIST에 한 줄, LANG_SUB에 이름을 더하면 된다.
사용: python3 langui_apply.py <game.html>"""
import sys

GLOBE = ('<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="7.2" fill="none" stroke="currentColor" stroke-width="1.3"/>'
         '<ellipse cx="10" cy="10" rx="3.1" ry="7.2" fill="none" stroke="currentColor" stroke-width="1.1"/>'
         '<path d="M3 10h14M4.2 6.3h11.6M4.2 13.7h11.6" fill="none" stroke="currentColor" stroke-width="1"/></svg>')
CV = '<svg class="cv" viewBox="0 0 10 10" aria-hidden="true"><path d="M1.5 3.5 5 7l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'

CSS = r"""
/* 언어 단추 · 언어 창 (11-16) */
.lang-pick.lg-one{padding:0!important}
.lg-one .lg-btn{display:inline-flex;align-items:center;gap:7px;height:100%;padding:0 12px 0 10px!important;color:#f3e8cb!important;font-size:13.5px}
.lg-one .lg-btn::after{display:none!important}
.lg-one .lg-btn svg{width:15px;height:15px;color:#d8bd7c;flex:none}
.lg-one .lg-btn .cv{width:9px;height:9px;color:#a39c8a;margin-left:1px}
.lg-one .lg-btn:hover .cv{color:#d8bd7c}
#langDlg .lg-sheet{max-width:360px}
#langDlg .set-head h2 small{display:block;font-size:11px;letter-spacing:.18em;color:#a39c8a;font-weight:400;margin-top:2px;font-family:var(--f-ui)}
#langDlg .lg-list{display:grid;gap:10px;padding:14px 0 6px}
#langDlg .lg-list .pn-btn{width:100%;display:flex!important;align-items:center;justify-content:space-between;gap:10px;padding:11px 16px!important;text-align:left;min-height:52px;box-sizing:border-box}
#langDlg .lg-list .pn-btn::before{display:none!important;content:none!important}
#langDlg .lg-list .pn-btn>span{text-align:left;line-height:1.35;flex:1;min-width:0}
#langDlg .lg-list .pn-btn b{display:block;font-weight:500;font-size:15.5px;color:#e9e1cf}
#langDlg .lg-list .pn-btn i{display:block;font-style:normal;font-size:11.5px;letter-spacing:.04em;color:#8f887a;font-family:var(--f-ui)}
#langDlg .lg-list .pn-btn .ck{width:16px;height:16px;color:#e6cd8f;opacity:0;flex:none}
#langDlg .lg-list .pn-btn.on b{color:#f3dfa6;text-shadow:0 0 10px rgba(230,200,140,.45)}
#langDlg .lg-list .pn-btn.on .ck{opacity:1}
#langDlg .lg-list .pn-btn.on{filter:drop-shadow(0 0 6px rgba(230,200,140,.35))}
"""

JS = r"""
// ---- 언어 단추 · 언어 창 (11-16) ----
const LANG_LIST=[['ko','한국어'],['en','English'],['ja','日本語']];
const LANG_SUB={ko:{ko:'한국어',en:'영어',ja:'일본어',zh:'중국어 (간체)',cur:'사용 중',t:'언어',x:'닫기'},
  en:{ko:'Korean',en:'English',ja:'Japanese',zh:'Chinese (Simplified)',cur:'In use',t:'Language',x:'Close'},
  ja:{ko:'韓国語',en:'英語',ja:'日本語',zh:'中国語（簡体字）',cur:'使用中',t:'言語',x:'閉じる'}};
(function(){ const btn=document.getElementById('langBtn'); if(!btn) return;
  const T=LANG_SUB[LANG]||LANG_SUB.en, me=LANG_LIST.find(x=>x[0]===LANG);
  btn.querySelector('.lg-cur').textContent=me?me[1]:LANG;
  const CK='<svg class="ck" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5 6.5 12 13 4.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  const d=document.createElement('div'); d.className='dlg hidden'; d.id='langDlg'; d.setAttribute('role','dialog'); d.setAttribute('aria-modal','true'); d.setAttribute('aria-label',T.t); d.dataset.notr=''; d.style.zIndex='56';
  d.innerHTML='<div class="sheet info set-sheet lg-sheet"><div class="set-head"><h2>'+T.t+(LANG==='en'?'':'<small>LANGUAGE</small>')+'</h2><button class="set-x" type="button" aria-label="'+T.x+'">×</button></div>'
    +'<div class="lg-list">'+LANG_LIST.map(([l,n])=>'<button type="button" class="pn-btn'+(l===LANG?' on':'')+'" data-l="'+l+'"'+(l===LANG?' aria-current="true"':'')+'><span><b lang="'+l+'">'+n+'</b><i>'+(l===LANG?T.cur:(T[l]||n))+'</i></span>'+CK+'</button>').join('')+'</div></div>';
  document.body.appendChild(d);
  const open=()=>{ d.classList.remove('hidden'); const f=d.querySelector('.pn-btn.on')||d.querySelector('.pn-btn'); if(f) f.focus({preventScroll:true}); btn.setAttribute('aria-expanded','true'); };
  const close=()=>{ d.classList.add('hidden'); btn.setAttribute('aria-expanded','false'); };
  btn.onclick=open;
  d.addEventListener('click',e=>{ const b=e.target.closest('.lg-list .pn-btn'); if(b){ if(b.dataset.l!==LANG) setLang(b.dataset.l); else close(); return; } if(e.target===d||e.target.closest('.set-x')) close(); });
  document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&!d.classList.contains('hidden')) close(); });
})();
"""

for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp('<div class="lang-pick lp-pc" id="langPick" data-notr role="group" aria-label="Language"><button type="button" data-l="ko" lang="ko">한국어</button><button type="button" data-l="en" lang="en">English</button><button type="button" data-l="ja" lang="ja">日本語</button></div>',
       '<div class="lang-pick lp-pc lg-one" id="langPick" data-notr><button type="button" class="lg-btn on" id="langBtn" aria-haspopup="dialog" aria-expanded="false" aria-label="Language">'
       + GLOBE + '<span class="lg-cur"></span>' + CV + '</button></div>')
    # 단추 하나짜리 언어 단추는 예전 고르기(data-l)를 타지 않는다
    rp("pick.querySelectorAll('button').forEach(b=>{ b.classList.toggle('on',b.dataset.l===LANG);",
       "pick.querySelectorAll('button[data-l]').forEach(b=>{ b.classList.toggle('on',b.dataset.l===LANG);")
    # 스타일은 마지막 스타일 블록 끝에, 스크립트는 설정 창 연결 뒤에
    i = s.rfind('</style>')
    if i < 0: miss.append(('</style>', 0))
    else: s = s[:i] + CSS + s[i:]
    rp("$('#setBtn').onclick=setOpen;", "$('#setBtn').onclick=setOpen;" + JS)
    print('langui miss', miss)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
