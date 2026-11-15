"""11-16 피드백
① 센티넬의 엄호(키아라전): 키아라가 그 합에 잃은 체력이 작으면(약 2 미만) 되돌릴 양이 반올림으로 0이 되어,
   '대신 받았다'는 문장만 나오고 센티넬 체력도 키아라 회복도 없던 것. 비율을 반올림하지 않고 계산하고,
   센티넬이 받을 피해가 1 이상일 때만 엄호한다(플레이어 결전 · NPC 결전 모두).
③ 물러선다: 퇴각 소리(F5)는 울리지만, 전투가 그 자리에서 끝나며 마지막 합이 '막음'으로 집계되어 칼 부딪치는 소리가
   함께 울리던 것 → 퇴각한 합은 맞음 · 막음 소리를 내지 않는다.
④ 마스터의 오드: 전투마다 가득 차던 것을 하루 단위로. 그날 쓴 만큼은 같은 날 다음 전투에도 이어지고, 날이 바뀌면 가득 찬다.
⑤ 결말 연출: 탭이 숨겨져 있던 순간에 결말이 나면 연출을 건너뛰던 것 → 탭으로 돌아왔을 때 보여 준다.
사용: python3 fb1116_apply.py <game.html>"""
import sys
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # ① 엄호
    rp("if(lost>0&&lost>=BXK.gMinMe&&!cov){ cov=true; const a=Math.round(lost*(.4+rnd()*.2)); e.hp=Math.min(100,e.hp+a); g.hp=clamp(g.hp-Math.round(a*Math.min(m,BXK.gCap)));",
       "const sh=.4+rnd()*.2, gd=Math.round(lost*sh*Math.min(m,BXK.gCap)); if(lost>0&&lost>=BXK.gMinMe&&!cov&&gd>=1){ cov=true; e.hp=Math.min(100,e.hp+lost*sh); g.hp=clamp(g.hp-gd);")
    rp("if(l>0&&l>=BXK.gMin&&!cov){ cov=true; const a=Math.round(l*(.4+rnd()*.2)); k.hp=Math.min(k.phase2?BXK.hp2:100,k.hp+a); gHit(g,a*m); }",
       "const sh=.4+rnd()*.2, gd=Math.round(l*sh*m); if(l>0&&l>=BXK.gMin&&!cov&&gd>=1){ cov=true; k.hp=Math.min(k.phase2?BXK.hp2:100,k.hp+l*sh); gHit(g,gd); }")
    # ③ 퇴각한 합은 맞음 · 막음 소리 없이
    rp("case 'retreat': Snd.sfx('f_retreat'); break;", "case 'retreat': Snd.sfx('f_retreat'); if(SB) SB.clash=true; break;")
    # ④ 오드는 하루 단위
    rp("w.battle.od=w.battle.odMax=oddMax();",
       "w.battle.odMax=oddMax(); if(w.odD!==w.day){ w.odD=w.day; w.odLeft=w.battle.odMax; } w.battle.od=Math.min(w.odLeft!=null?w.odLeft:w.battle.odMax,w.battle.odMax);")
    rp("if(b.od>=cost){ b.od-=cost; return; }", "if(b.od>=cost){ b.od-=cost; W().odLeft=b.od; return; }")
    # ⑤ 숨긴 탭에서 난 결말은 돌아왔을 때 보여 준다
    rp("function endFx(fx){ if(!xfxOK()||!fx) return;",
       "function endFx(fx){ if(fx&&document.hidden){ const go=()=>{ if(document.hidden) return; document.removeEventListener('visibilitychange',go); endFx(fx); }; document.addEventListener('visibilitychange',go); return; } if(!xfxOK()||!fx) return;")
    print('fb1116 miss', miss)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
