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
# 11-23: 플레이어가 한글로 지은 이름(나 · 배우자 · 아이 · 형제)이 든 문장은 틀에 끼운 이름이 한글로 남는다는 이유로 틀 전체를 버려
# 일본어 · 영어 화면에서 그 문장이 통째로 한국어로 나왔다. 직접 지은 이름은 그대로 두고 나머지를 옮긴다
rp("const q=/^(은|는|이|가|을|를|과|와|으로|로|이나|나|이라|라|이라는|라는|이다|다|의|에|에게|도|만)$/.test(v)?'':tr(v); if(HANGUL.test(q)) continue;",
   "const q=/^(은|는|이|가|을|를|과|와|으로|로|이나|나|이라|라|이라는|라는|이다|다|의|에|에게|도|만)$/.test(v)?'':tr(v); if(HANGUL.test(q)&&!_userNm(v)) continue;")
rp("let _tplDepth=0, _tplCut=0;",
   "// 플레이어가 직접 지은 이름(1초마다 다시 모음, 11-23)\n"
   "let _UN=null, _UNt=0; function _userNm(v){ const now=Date.now(); if(!_UN||now-_UNt>1000){ _UN=new Set(); _UNt=now; try{ const S=Sim.S, f=S&&S.fam, a=x=>{ if(x&&typeof x==='string'&&/[가-힣]/.test(x)) _UN.add(x.trim()); };\n"
   "  if(S){ a(S.name); if(f){ a(f.sibName); if(f.spouse) a(f.spouse.name); for(const k of f.kids||[]) a(k&&k.name); } } }catch(e){} } return _UN.has(String(v).trim()); }\n"
   "let _tplDepth=0, _tplCut=0;")
# 11-23: 문장 틀 되맞춤에 걸음 수 상한 — 맨 바깥 tr() 한 번(그 안의 조각 · 문장 나눔 포함)에 TPL_STEPS까지.
# 넘으면 남은 틀 맞춤을 건너뛰고(문장 · 조각 단위 번역은 계속) 그 결과를 그대로 기억한다.
# (서번트 대사가 든 긴 한 줄이 PC에서도 2~68초, 폰에서는 몇 분씩 화면을 멈추게 했다: 인연 사건 · 꿈 · 소환 첫 대사 등)
rp("const _trc=new Map();\nfunction tr(s){\n  if(LANG==='ko'||!s||!HANGUL.test(s)) return s;\n  const hit=_trc.get(s); if(hit!==undefined) return hit;\n  const c0=_tplCut, d0=_tplDepth;\n  let r=_tr1(s);",
   "const _trc=new Map();\nconst TPL_STEPS=window.__TPL_STEPS||300000; let _tplSteps=0, _tplOver=false, _trNest=0; const _trcD=new Map();\nfunction tr(s){\n  if(LANG==='ko'||!s||!HANGUL.test(s)) return s;\n  const hit=_trc.get(s); if(hit!==undefined) return hit;\n  const c0=_tplCut, d0=_tplDepth, top=_trNest===0; if(top){ _tplSteps=0; _tplOver=false; }\n  let r; _trNest++; try{ r=_tr1(s); } finally{ _trNest--; }")
rp("if(s.length<240&&(!HANGUL.test(r)||(d0===0&&_tplCut===c0))) _trc.set(s,r); return r;",
   "if(s.length<240&&(!HANGUL.test(r)||_tplCut===c0||(top&&_tplOver))) _trc.set(s,r); else if(s.length<240&&!_tplOver){ const o=_trcD.get(s); if(!o||d0<o[0]){ if(_trcD.size>40000) _trcD.clear(); _trcD.set(s,[d0,r]); } } return r;")
# 깊이 제한에 걸린 결과는 「그 깊이에서」의 결과로 기억한다: 같은 깊이이거나 더 깊은 곳에서 다시 부르면 그대로 쓴다
# (긴 대사 한 줄에서 같은 조각 400개를 43만 번 다시 옮기던 것, 11-23)
rp("  const hit=_trc.get(s); if(hit!==undefined) return hit;\n  const c0=_tplCut, d0=_tplDepth, top=_trNest===0;",
   "  const hit=_trc.get(s); if(hit!==undefined) return hit;\n  { const dc=_trcD.get(s); if(dc&&dc[0]<=_tplDepth) return dc[1]; }\n  const c0=_tplCut, d0=_tplDepth, top=_trNest===0;")   # 깊이 제한에 걸리지 않았으면 안쪽(끼워 넣을 말 후보)에서 실패한 결과도 기억한다 — 같은 후보를 틀마다 다시 옮기던 것
rp("function _trTpl(t){ if(_tplDepth>=4||t.length>600){ if(_tplDepth>=4) _tplCut++; return null; } _tplDepth++;",
   "const _tplMemo=new Map();   // 같은 조각을 틀 6천여 개에 거듭 맞춰 보지 않게: 조각 → 결과(깊이 제한에 걸리지 않은 것만, 11-23)\n"
   "function _trTpl(t){ if(_tplDepth>=4||t.length>600){ if(_tplDepth>=4) _tplCut++; return null; } if(_tplOver) return null; if(_tplMemo.has(t)) return _tplMemo.get(t); const m0=_tplCut; _tplDepth++; let mr; try{ mr=_trTpl0(t); } finally{ _tplDepth--; } if(_tplCut===m0){ if(_tplMemo.size>40000) _tplMemo.clear(); _tplMemo.set(t,mr); } return mr; }\n"
   "function _trTpl_old(t){ if(_tplDepth>=4||t.length>600){ if(_tplDepth>=4) _tplCut++; return null; } if(_tplOver) return null; _tplDepth++;")
rp("  const go=(i,pos)=>{ if(i===toks.length) return pos===s.length;",
   "  const go=(i,pos)=>{ if(++_tplSteps>TPL_STEPS){ if(!_tplOver){ _tplOver=true; _tplCut++; } return false; } if(i===toks.length) return pos===s.length;")
# 11-23: 틀 후보 색인 — 틀마다 닻(가장 긴 고정 글자)에서 가장 드문 두 글자를 열쇠로 둔다. 닻이 글 안에 있으면 그 두 글자도 있으므로
# 글의 두 글자 조각으로 후보만 모아 본다. (끼워 넣을 말 후보마다 틀 6천여 개를 다 훑느라 긴 대사 한 줄에 2~68초가 걸렸다)
rp("    return {toks,v,an,x,nl:k.includes('\\n'),w:lits.join('').length,nc:toks.filter(x=>x.c!=null).length}; }).sort((a,b)=>b.w-a.w||b.nc-a.nc); })();",
   "    return {toks,v,an,x,nl:k.includes('\\n'),w:lits.join('').length,nc:toks.filter(x=>x.c!=null).length}; }).sort((a,b)=>b.w-a.w||b.nc-a.nc); })();\n"
   "const _TPL_IX=(()=>{ const bg=a=>{ const o=new Set(); for(let i=0;i<a.length-1;i++) o.add(a.substr(i,2)); return o; }, f=new Map(), any=[], m=new Map();\n"
   "  const B=I18N_TPLS.map(T=>T.an&&T.an.length>=2?bg(T.an):null); for(const o of B) if(o) for(const k of o) f.set(k,(f.get(k)||0)+1);\n"
   "  B.forEach((o,i)=>{ if(!o){ any.push(i); return; } let best=null; for(const k of o) if(best===null||f.get(k)<f.get(best)) best=k; let l=m.get(best); if(!l) m.set(best,l=[]); l.push(i); });\n"
   "  return {m,any}; })();\n"
   "function _tplCands(t){ const S=new Set(_TPL_IX.any); for(let i=0;i<t.length-1;i++){ const l=_TPL_IX.m.get(t.substr(i,2)); if(l) for(const x of l) S.add(x); } return [...S].sort((a,b)=>a-b); }")
rp("  for(const T of I18N_TPLS){ if(nl&&!T.nl) continue; if(T.an&&!t.includes(T.an)) continue;",
   "  for(const ci of _tplCands(t)){ const T=I18N_TPLS[ci]; if(nl&&!T.nl) continue; if(T.an&&!t.includes(T.an)) continue;")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
print('lang 적용')
