"""보스가 강림한 뒤 NPC 조가 보스로 향할 확률 올림 (11-16)
- 갈 날을 정하는 확률(검은 성배 · 비스트 공통, cxGoP):
  부수려는 조 50% → 70% / 쥐려는 조 2단계 전 0% → 20%, 2단계 뒤 35% → 55%
  마지막 날이 다가오면 더: 마지막 날 이틀 전 +10%p, 하루 전 +20%p (최대 95%)
- 건강 조건 55 → 45 (갈 날 정하기 · 내가 빠진 뒤 그날그날 정하기 모두)
- 그대로: 소문이 돈 밤에 실제로 갈 때의 건강 40 이상, 함께 가자는 권유 50%, 혼자 남은 조 70%
사용: python3 bossnpc_apply.py <game.html>"""
import sys
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("  function cxPlan(){",
       "  // 보스로 갈 날을 정할 확률: 부수려는 조 70% · 쥐려는 조 2단계 전 20% / 뒤 55% · 마지막 날 이틀 전 +10%p, 하루 전 +20%p\n"
       "  function cxGoP(p,b){ const w=W(), c=CXW(), fin=(c&&c.finalDay)||14, near=Math.max(0,3-(fin-w.day))*.1;\n"
       "    const base=p.cxStance==='break'?.7:p.cxStance==='claim'?(b&&b.phase2?.55:.2):0; return base?Math.min(.95,base+near):0; }\n"
       "  function cxPlan(){")
    rp("if(!(p.hp>=55&&(p.cxStance==='break'&&ch(.5)||p.cxStance==='claim'&&b.phase2&&ch(.35)))) continue;",
       "if(!(p.hp>=45&&ch(cxGoP(p,b)))) continue;")
    rp("(last&&ch(.7)||p.hp>=55&&(p.cxStance==='break'&&ch(.5)||p.cxStance==='claim'&&b.phase2&&ch(.35)))",
       "(last&&ch(.7)||p.hp>=45&&ch(cxGoP(p,b)))")
    rp("(last&&ch(.7)||p.hp>=55&&ch(.5))", "(last&&ch(.7)||p.hp>=45&&ch(cxGoP(p,k)))")
    print('bossnpc miss', miss)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
