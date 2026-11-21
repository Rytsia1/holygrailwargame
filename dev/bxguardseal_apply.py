"""11-21: 키아라 결전에서 호위 센티넬을 쓰러뜨릴 때마다 「다음 날 감독관의 사자가 찾아와 … 령주 한 획」이 끼어들던 문제 (커뮤니티 제보 11-21)
- 령주 보상은 도시를 헤매는 센티넬을 사냥할 때의 보상이다. 결전에서 키아라 곁을 지키는 호위(u.guard)는 싸움 한가운데라
  감독관의 사자가 올 자리가 없다 → 호위를 쓰러뜨려도 령주를 주지 않고 그 줄도 쓰지 않는다(플레이어 · NPC 조 모두)
- KP 회수 · 처치 수(shadowKills) · 업적 판정은 그대로
사용: python3 bxguardseal_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if "if(!u.guard){ w.seals++" in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

rp("      if(by==='me'){ w.seals++; c.shadowKills++; log('다음 날 감독관의 사자가 찾아와 당신 손등에 령주 한 획을 그려 주었다.','seal'); if(k) log(",
   "      if(by==='me'){ c.shadowKills++; if(!u.guard){ w.seals++; log('다음 날 감독관의 사자가 찾아와 당신 손등에 령주 한 획을 그려 주었다.','seal'); } if(k) log(")   # 호위는 령주 보상 없음 (11-21)
rp("      else if(by&&by.i){ by.seals=(by.seals||0)+1; if(c.stage===2)",
   "      else if(by&&by.i){ if(!u.guard) by.seals=(by.seals||0)+1; if(c.stage===2)")

if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
