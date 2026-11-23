"""11-22: 언어팩을 따로 받기 위한 준비 — 로딩 화면 스크립트가 정한 언어를 게임도 그대로 쓴다
- 예전: 로딩 스크립트는 저장소(localStorage)를 못 읽으면 기기 언어를 보지 않고 한국어로 두고, 게임은 기기 언어를 봐서 둘이 어긋날 수 있었다.
  사전을 따로 받게 되면(dev/release.py) 어긋난 언어는 사전 없이 한국어로 나오므로, 로딩 스크립트가 고른 언어(window.__LANG)를 게임이 그대로 쓴다.
- 주소 ?lang= 도 저장소가 막혀 있어도 그 페이지에서는 따른다
사용: python3 lang_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read(); miss = []
def rp(o, n):
    global s
    if s.count(o) != 1: miss.append((o[:70], s.count(o))); return
    s = s.replace(o, n)
rp("try{const q=new URLSearchParams(location.search).get('lang');if(LS.includes(q))localStorage.setItem('cupnight.lang',JSON.stringify(q));const v=JSON.parse(localStorage.getItem('cupnight.lang')||'null');if(LS.includes(v))L=v;else{const n=((navigator.languages&&navigator.languages[0])||navigator.language||'ko').toLowerCase();L=n.startsWith('ko')?'ko':n.startsWith('ja')?'ja':(ZO&&n.startsWith('zh'))?(/hant|tw|hk|mo/.test(n)?'zht':'zhs'):'en'}}catch(e){}",
   "let q=null,v=null;try{q=new URLSearchParams(location.search).get('lang');}catch(e){}try{if(LS.includes(q))localStorage.setItem('cupnight.lang',JSON.stringify(q));v=JSON.parse(localStorage.getItem('cupnight.lang')||'null');}catch(e){}"
   "if(LS.includes(q))L=q;else if(LS.includes(v))L=v;else{try{const n=((navigator.languages&&navigator.languages[0])||navigator.language||'ko').toLowerCase();L=n.startsWith('ko')?'ko':n.startsWith('ja')?'ja':(ZO&&n.startsWith('zh'))?(/hant|tw|hk|mo/.test(n)?'zht':'zhs'):'en'}catch(e){}}window.__LANG=L;")
rp("const LANG=(()=>{ try{ const v=JSON.parse(localStorage.getItem(K_LANG)||'null'); if(LANGS.includes(v)) return v; }catch(e){}",
   "const LANG=(()=>{ if(typeof window!=='undefined'&&LANGS.includes(window.__LANG)) return window.__LANG;   // 로딩 화면이 고른 언어(사전도 그 언어로 받았다)\n  try{ const v=JSON.parse(localStorage.getItem(K_LANG)||'null'); if(LANGS.includes(v)) return v; }catch(e){}")
# 11-22: 화면 글자를 옮길 때 <script> 본문 글자는 건너뛴다.
# HTML을 읽는 도중 뒤쪽 <script>의 본문 글자가 따로 붙으며 감시(MutationObserver)에 걸려, 코드 332자를 문장 틀 수천 개에 맞춰 보느라
# 영어 · 중국어 첫 화면이 PC에서도 1분, 느린 폰에서는 4분 넘게 멈췄다
rp("  if(root.nodeType===3){ const v=root.nodeValue, r=tr(v); if(r!==v) root.nodeValue=r; return; }",
   "  if(root.nodeType===3){ const pa=root.parentNode; if(pa&&(pa.nodeName==='SCRIPT'||pa.nodeName==='STYLE'||pa.nodeName==='TEXTAREA'||(pa.closest&&pa.closest('[data-notr]')))) return;   // 스크립트 본문은 옮기지 않는다 (11-22)\n    const v=root.nodeValue, r=tr(v); if(r!==v) root.nodeValue=r; return; }")
# 11-23: 여러 줄 글(소환 직후 안내 등)을 문장 틀 수천 개에 통째로 맞춰 보느라 영어 · 일본어 · 중국어에서
# 서번트를 부른 직후 화면이 PC에서도 16~20초, 폰에서는 몇 분 멈췄다(검은 막이 걷히지 않음).
# 줄바꿈이 든 글에는 줄바꿈이 든 틀(10개)만 맞춰 보고, 나머지는 아래의 줄 단위 번역으로 넘긴다
rp("    return {toks,v,an,x,w:lits.join('').length,nc:toks.filter(x=>x.c!=null).length}; }).sort(",
   "    return {toks,v,an,x,nl:k.includes('\\n'),w:lits.join('').length,nc:toks.filter(x=>x.c!=null).length}; }).sort(")
rp("function _trTpl0(t){\n  for(const T of I18N_TPLS){ if(T.an&&!t.includes(T.an)) continue;",
   "function _trTpl0(t){ const nl=t.includes('\\n');\n  for(const T of I18N_TPLS){ if(nl&&!T.nl) continue; if(T.an&&!t.includes(T.an)) continue;")
# 11-23: 능력치 「정신」은 영어로 Spirit인데, 「정신 +n」 틀만 Will로 남아 있었다
rp('["정신 +{0}","Will +{0}"]', '["정신 +{0}","Spirit +{0}"]')
rp('"정신 +1":"Will +1"', '"정신 +1":"Spirit +1"')
rp('"정신 +2":"Will +2"', '"정신 +2":"Spirit +2"')
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
print('lang 적용')
