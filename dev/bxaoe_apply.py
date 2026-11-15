"""키아라 곁의 호위 센티넬과 범위 보구 (11-16)
A. 범위 보구는 플레이어 결전에서도 호위를 휩쓴다(NPC 결전과 같은 규칙).
   - 호위 하나하나를 보구 범위에 따라 정해진 확률로 맞힌다(키아라의 체력과 무관):
     대계 · 대국 100% / 대성 95% / 대군 · 고유결계 85% / 대진 75%. 여러 종별이 붙은 보구는 가장 넓은 것.
     자신에게 거는 보구('(자신)')와 한 대상을 노리는 보구(대인 · 대마 · 대신 등)는 호위에 닿지 않는다.
   - 피해는 그 센티넬의 능력치로만 계산한다(그 서번트가 이 보구를 맞았을 때의 피해, 키아라의 체력 · 배율과 무관).
     함께 간 조의 보구는 평소처럼 CXB.np만큼.
C. 호위가 된 센티넬의 밤 회복 +10 → +4.
보정: 호위가 쉽게 쓰러지면 KP가 풀려 키아라가 약해지므로, 키아라의 배율에 BXK.mB를 곱해 승률을 맞춘다.
사용: python3 bxaoe_apply.py <game.html>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n

N5 = ['하나가', '둘이', '셋이', '넷이', '다섯이']
EN5 = ['one Sentinel', 'two Sentinels', 'three Sentinels', 'four Sentinels', 'five Sentinels']
JA5 = ['ひとり', 'ふたり', '三人', '四人', '五人']
TR_D = [(f'보구의 여파가 키아라 곁을 지키던 센티넬 {k} 휩쓸었다.',
         f'The aftershock of the Noble Phantasm swept over {e} guarding Kiara.',
         f'宝具の余波が、キアラの傍らを守るセンチネル{j}を呑み込んだ。') for k, e, j in zip(N5, EN5, JA5)]

for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("gCover:.6, gChip:.2,", "gCover:.6, gChip:.2, mB:1.25,")
    rp("if(c.karma) m*=BXK.wdM; if(vsNpc) m*=BXK.npM; return m; }", "if(c.karma) m*=BXK.wdM; if(vsNpc) m*=BXK.npM; return m*BXK.mB; }")
    rp("const BX_AOE=/대군|대성|대계|대국|대왕|대마/;",
       "const BX_AOE=/대군|대성|대계|대국|대왕|대마/;\n"
       "  // 범위 보구가 호위를 맞힐 확률(보구 범위로만): 대계 · 대국 100% / 대성 95% / 대군 · 고유결계 85% / 대진 75%. 자신에게 거는 보구는 닿지 않는다\n"
       "  const BX_AOEP=k=>{ k=k||''; return /자신/.test(k)?0:/대계|대국/.test(k)?1:/대성/.test(k)?.95:/대군|고유결계/.test(k)?.85:/대진/.test(k)?.75:0; };\n"
       "  // 호위 하나하나를 그 확률로 맞히고, 피해는 그 센티넬이 이 보구를 맞았을 때의 값(키아라의 체력 · 배율과 무관)\n"
       "  function bxAoeG(ah,aP,mul,hitG){ const p=BX_AOEP(artOf(ah).k); if(!p) return 0; let n=0;\n"
       "    for(const g of bxGuards()){ if(!ch(p)) continue; n++; hitG(g,Math.max(3,Math.round(npDmg(ah,H_BY[g.hero],false,false,aP)*(mul||1)))); } return n; }")
    # NPC 결전: 대표 조 · 함께 간 조
    rp("if(fire.get(X)&&BX_AOE.test(artOf(X.h).k||'')) for(const g of bxGuards()) gHit(g,kLost()*m*.5);",
       "if(fire.get(X)) bxAoeG(X.h,X.P,1,(g,d)=>gHit(g,d));")
    rp("if(BX_AOE.test(artOf(qh).k||'')) for(const g of bxGuards()) gHit(g,(k0-k.hp)*m*.5,q); continue; }",
       "bxAoeG(qh,npcParams(q).p,CXB.np,(g,d)=>gHit(g,d,q)); continue; }")
    # 플레이어 결전: 보구를 쏜 합에 표시해 두고, 그 합의 호위 처리에서 휩쓴다
    rp("const NX=npPre(sel); myNP=NX.myNP; enNP=NX.enNP;", "const NX=npPre(sel); myNP=NX.myNP; enNP=NX.enNP; if(myNP&&e.bx) b.bxAoe=1;")
    rp("let cov=false; bxAllyRound(b); const mN=hero().name;",
       "let cov=false; bxAllyRound(b); const mN=hero().name;\n"
       "    if(b.bxAoe){ b.bxAoe=0; const n=bxAoeG(hero(),myParams().p,1,(g,d)=>{ g.hp=clamp(g.hp-d); if(g.hp<=0) bxUnitDown(g,'me'); });\n"
       f"      if(n) log(`보구의 여파가 키아라 곁을 지키던 센티넬 ${{{N5!r}[n-1]||'{N5[-1]}'}} 휩쓸었다.`,'war'); }}")
    # C. 호위의 밤 회복
    rp("u.hp=clamp(u.hp+(u.guard?10:8)+(u.kp==='Organ'?12:0));", "u.hp=clamp(u.hp+(u.guard?4:8)+(u.kp==='Organ'?12:0));")
    s, nd, nt = i18n.add(s, TR_D)
    print('bxaoe miss', miss, 'tr', nd, nt)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
