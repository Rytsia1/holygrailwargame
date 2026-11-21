"""11-21: 번역 캐시가 순서에 따라 한국어를 기억하던 문제 (커뮤니티 제보 11-21: 「그 겨울 함께 싸운 형가에게…」가 일본어판에서 한국어로)
- tr()은 옮긴 결과를 _trc에 기억한다. 그런데 문장 틀(_trTpl) 속에서 다시 부른 tr()은 깊이 제한(4단)에 걸리거나,
  중국어의 문장 나눔처럼 깊이 0에서만 하는 길을 못 타서 실패할 수 있다. 그 실패(한국어 그대로)가 캐시에 남으면
  나중에 그 문장 하나만 화면에 나와도 한국어로 나왔다.
  예: 「이름, 2000–2032.\\n그 겨울 함께 싸운 형가에게 …」를 먼저 옮기면 뒤의 한 줄짜리도 계속 한국어
- 이제: 한글이 남은 결과는 깊이 0에서, 깊이 제한에 걸리지 않고 얻은 것만 기억한다(번역이 된 결과는 예전처럼 기억)
사용: python3 i18nfix21_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if '_tplCut' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

rp("let _tplDepth=0;\nfunction _trTpl(t){ if(_tplDepth>=4||t.length>600) return null;",
   "let _tplDepth=0, _tplCut=0;   // _tplCut: 깊이 제한에 걸린 횟수 (그 사이 얻은 실패는 캐시에 남기지 않는다 · 11-21)\nfunction _trTpl(t){ if(_tplDepth>=4||t.length>600){ if(_tplDepth>=4) _tplCut++; return null; }")
# tr() 본문: 중국어 단계(zh_apply)가 「let r=_tr1(s); if(LANG==='ja') …;」 뒤에 끼워 넣으므로 그 앞뒤만 건드린다
rp("  const hit=_trc.get(s); if(hit!==undefined) return hit;\n  let r=_tr1(s);",
   "  const hit=_trc.get(s); if(hit!==undefined) return hit;\n  const c0=_tplCut, d0=_tplDepth;\n  let r=_tr1(s);")
rp(" if(s.length<240) _trc.set(s,r); return r;\n}",
   " if(s.length<240&&(!HANGUL.test(r)||(d0===0&&_tplCut===c0))) _trc.set(s,r); return r;\n}")

if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
