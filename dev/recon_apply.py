"""11-18: 서번트를 잃은 NPC 마스터의 재계약이 같은 밤에 몰려 '쓰러뜨리자마자 연속 재전투'처럼 보이던 문제 (커뮤니티 문의 11-18)
- 예전: 버서커를 쓰러뜨린 밤 → 같은 밤 NPC 행동에서 그 마스터가 주인 잃은 서번트와 재계약(40%) → 같은 밤 습격으로 바로 쳐들어올 수 있었다
- 이제 ① 서번트를 잃은 그 날에는 재계약하지 않는다(다음 밤부터) ② 재계약한 조는 계약한 그 밤에는 습격하러 오지 않는다
사용: python3 recon_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'loneD' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)
rp("    if(npcStayAlone(e)){ e.lone=true; log(",
   "    if(npcStayAlone(e)){ e.lone=true; e.loneD=W().day; log(")
rp("        if(npcStayAlone(lose)){ lose.lone=true; if(",
   "        if(npcStayAlone(lose)){ lose.lone=true; lose.loneD=w.day; if(")
rp("""    for(const m of w.pairs.filter(p=>p.lone)){
      if(ch(.1)){ m.lone=false; continue; }""",
   """    for(const m of w.pairs.filter(p=>p.lone)){
      if(m.loneD===w.day) continue;   // 서번트를 잃은 그 밤에는 다시 계약하지 않는다 (11-18)
      if(ch(.1)){ m.lone=false; continue; }""")
rp("s.wishKnown=false; s.recon=1; m.lone=false;", "s.wishKnown=false; s.recon=1; s.reconD=w.day; m.lone=false;")
rp("const foes=contracted().filter(p=>!p.ally&&!p.truce&&!(p.halt>0)&&!p.rest&&raidOk(p)&&",
   "const foes=contracted().filter(p=>!p.ally&&!p.truce&&!(p.halt>0)&&!p.rest&&p.reconD!==w.day&&raidOk(p)&&")   # 재계약한 그 밤에는 습격하지 않는다
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
print('적용 끝')
