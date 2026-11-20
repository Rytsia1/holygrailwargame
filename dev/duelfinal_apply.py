"""11-20: 약속된 결판은 결전 날에 끼어들지 않는다
- 결전 날(14일째, 또는 위기의 마지막 날)에는 싸우러 가는 갈림길(fight:true, 지금은 결투장)이 나오지 않는다
- 서번트의 고집(결판을 내고 싶어 한다) 사건도 결전 날에는 나오지 않는다
- 그 밖에 결판을 약속하는 선택(NPC 마스터 사연 등)은 결전 날이면 약속이 잡히지 않고 한 줄로 알린다
- 혹시 약속이 남아 있으면 결전의 밤 시작에 한 줄로 거둔다
- (그 밖의 밤에는 지금처럼 약속된 결판 하나만 고를 수 있다)
사용: python3 duelfinal_apply.py <game.html>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'const finalToday=' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

rp("  const CROSS=[",
   """  // 11-20: 결전 날(14일째 · 위기의 마지막 날)에는 결판을 약속하지 않는다. 그날 밤은 결전이다
  const finalToday=()=>{ const w=W(); return !!w&&(w.day>=14||!!(w.crisis&&w.crisis.finalDay&&!w.crisis.done&&w.day>=w.crisis.finalDay)); };
  function duelSet(p){ if(finalToday()){ log('결전의 밤이라, 약속한 결판은 열리지 않는다.','war'); return; } W().duel = p; }
  const CROSS=[""")
rp("    {id:'duel',c:()=>contracted().some(p=>!p.ally&&p.known),f:",
   "    {id:'duel',fight:true,c:()=>contracted().some(p=>!p.ally&&p.known),f:")
rp("const el=CROSS.filter(x=>!(w.crossSeen||[]).includes(x.id)&&(!x.c||x.c()));",
   "const el=CROSS.filter(x=>!(w.crossSeen||[]).includes(x.id)&&!(x.fight&&finalToday())&&(!x.c||x.c()));")
rp("{w:2,c:()=>alivePairs().some(p=>p.known&&!p.ally)&&W().hp>60,f:",
   "{w:2,c:()=>alivePairs().some(p=>p.known&&!p.ally)&&W().hp>60&&!finalToday(),f:")
n_ = s.count("W().duel=p;")
if n_ < 4: miss.append(("W().duel=p;", n_))
s = s.replace("W().duel=p;", "duelSet(p);")
rp("w.duel=p;", "duelSet(p);")
rp("const w=W(); relGain(20); relEve(); if(cxFinalNight()) return; w.final=true;",
   "const w=W(); if(w.duel){ if(w.duel.alive) log(`${pName(w.duel)} 조와 약속한 결판은 결전의 밤에 묻혔다.`,'war'); w.duel=null; } relGain(20); relEve(); if(cxFinalNight()) return; w.final=true;")

if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

D = [("결전의 밤이라, 약속한 결판은 열리지 않는다.", "It is the night of the final battle. The promised showdown will not happen.",
      "決戦の夜だ。約束した決着はつけられない。", "今夜是决战之夜，约好的决斗不会举行。", "今夜是決戰之夜，約好的決鬥不會舉行。")]
T = [("{0} 조와 약속한 결판은 결전의 밤에 묻혔다.", "The showdown promised with the {0} team was buried under the night of the final battle.",
      "{0}陣営と約束した決着は、決戦の夜に埋もれた。", "与{0}组约好的决斗，被决战之夜掩埋了。", "與{0}組約好的決鬥，被決戰之夜掩埋了。")]
s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, *_ in D], [(a, b, c) for a, b, c, *_ in T])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _b, _c, d, e in D + T:
    if a not in Z: Z[a] = [d, e]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 사전', nd, '· 틀', nt, '· 중국어', n)
