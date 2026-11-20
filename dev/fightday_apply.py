"""11-20: 싸움을 약속하는 일은 하루에 하나만
- 오늘 이미 결판을 약속했거나(그 상대가 살아 있음), 오늘 싸움 사건이 있었거나, 인질을 구하러 가기로 했으면
  싸우러 가는 갈림길(fight:true) · 서번트의 고집 · 명문 후계자의 결투장 사연은 그날 나오지 않는다(다음 날로 미뤄짐)
- 그 밖에 결판을 약속하는 선택이 겹치면 먼저 한 약속을 지키고 한 줄로 알린다
사용: python3 fightday_apply.py <game.html>  (duelfinal_apply.py 다음)"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'const fightToday=' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

rp("  function duelSet(p){ if(finalToday()){ log('결전의 밤이라, 약속한 결판은 열리지 않는다.','war'); return; } W().duel = p; }",
   """  // 싸움을 약속하는 일은 하루에 하나: 이미 약속한 결판(상대 생존) · 오늘 있었던 싸움 사건 · 인질 구출
  const fightToday=()=>{ const w=W(); return !!w&&(!!(w.duel&&w.duel.alive)||w.fightD===w.day||!!(w.host&&w.host.go)); };
  function duelSet(p){ if(finalToday()){ log('결전의 밤이라, 약속한 결판은 열리지 않는다.','war'); return; } const w=W();
    if(w.duel&&w.duel.alive&&w.duel!==p){ log(`오늘 밤은 이미 ${pName(w.duel)} 조와 약속한 결판이 있다.`,'war'); return; }
    w.duel = p; w.fightD=w.day; }""")
rp("!(x.fight&&finalToday())", "!(x.fight&&(finalToday()||fightToday()))")
rp("&&W().hp>60&&!finalToday(),f:", "&&W().hp>60&&!finalToday()&&!fightToday(),f:")
rp("""      {c:p=>true,f:p=>decide({title:'결투장',body:""", """      {c:p=>!finalToday()&&!fightToday(),f:p=>decide({title:'결투장',body:""")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

T = [("오늘 밤은 이미 {0} 조와 약속한 결판이 있다.", "Tonight you already have a promised showdown with the {0} team.",
      "今夜はすでに{0}陣営と約束した決着がある。", "今晚已经和{0}组约好了决斗。", "今晚已經和{0}組約好了決鬥。")]
s, nd, nt = i18n.add(s, [], [(a, b, c) for a, b, c, *_ in T])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _b, _c, d, e in T:
    if a not in Z: Z[a] = [d, e]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 틀', nt, '· 중국어', n)
