"""11-23: 보구 · 령주 같은 화면 연출에서 오류가 나도 게임이 멈추지 않게
- 연출 함수는 기록(log) 훅 안에서 바로 불린다. 여기서 오류가 나면 Sim.tick을 지나 화면 갱신 고리(requestAnimationFrame)까지 끊겨
  진행이 통째로 멈춘다. 연출이 대기열에서 꺼내질 때(cfxEnd → fxNext) 오류가 나면 '연출 중 멈춤'(setHold)이 풀리지 않는다.
- 연출 호출을 감싸 오류가 나면 그 연출만 건너뛰고 멈춤을 푼다. 화면 갱신 고리는 오류가 나도 다음 프레임을 이어 간다.
사용: python3 fxguard_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read(); miss = []
def rp(o, n):
    global s
    if s.count(o) != 1: miss.append((o[:70], s.count(o))); return
    s = s.replace(o, n)
if 'fxSafe(' in s: print('이미 적용됨'); sys.exit(0)
# ① 연출 호출: 오류가 나면 그 연출을 걷어 내고 멈춤을 푼다
rp("function cfxEnd(all){",
   "function fxSafe(f,fx){ try{ f(fx); }catch(err){ try{ console.error('fx',fx&&fx.t,err); }catch(_){} const o=$('#cfx'); if(o) o.remove(); if(!$('#cfx')){ try{ Sim.setHold(false); }catch(_){} if(FXQ.length) cfxEnd(); } } }   // 11-23\n"
   "function cfxEnd(all){")
rp("if(FXQ.length){ fxNext(); return; } try{ Sim.setHold(false); }catch(e){} }",
   "if(FXQ.length){ try{ fxNext(); return; }catch(err){ try{ console.error('fxq',err); }catch(_){} const o2=$('#cfx'); if(o2) o2.remove(); return cfxEnd(); } } try{ Sim.setHold(false); }catch(e){} }")
rp("if(e.k==='fx'){ if(e.fx&&F[e.fx.t]) F[e.fx.t](e.fx); return; }",
   "if(e.k==='fx'){ if(e.fx&&F[e.fx.t]) fxSafe(F[e.fx.t],e.fx); return; }")
rp("if(e.fx) (F[e.fx.t]||clashFx)(e.fx);",
   "if(e.fx) fxSafe(F[e.fx.t]||clashFx,e.fx);")
# ② 화면 갱신 고리: 한 프레임에서 오류가 나도 다음 프레임은 돈다
rp("const f=t=>{ const dt=Math.min(.25,(t-last)/1000); last=t; Sim.tick(dt); prog(); raf=requestAnimationFrame(f); };",
   "const f=t=>{ const dt=Math.min(.25,(t-last)/1000); last=t; try{ Sim.tick(dt); prog(); }catch(err){ try{ console.error('tick',err); }catch(_){} } raf=requestAnimationFrame(f); };")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
print('fxguard 적용')
