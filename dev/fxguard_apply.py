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
# ③ 화면 전체 연출 · 결말 장면 · 작별 장면의 시간을 실제 시간으로 센다 (11-23)
#    예전엔 한 프레임에 더하는 시간을 0.05초로 막아, 초당 20프레임이 안 나오는 폰에서는 연출이 느린 화면처럼 길어졌다
#    (초당 5프레임이면 9.6초짜리 키아라 강림이 38초). 0.7초보다 긴 틈(탭을 내렸다 돌아옴 등)만 0.05초로 친다
import re
n0 = s.count("const dt=Math.min(.05,(now-last)/1000);")
if n0 != 5: miss.append(('loop dt', n0))
else:
    s = s.replace("const dt=Math.min(.05,(now-last)/1000);", "const rd=(now-last)/1000, dt=rd>.7?.05:rd; globalThis.XDT_=dt;")
    # 짧은 번쩍임(가우스 폭 0.05~0.12초)은 프레임 간격이 넓으면 프레임 사이에 끼어 안 보인다 → 폭을 프레임 간격의 0.6배 아래로 줄이지 않는다
    pat = re.compile(r"exp\(-Math\.pow\(\(t-([^()]*)\)/(\.\d+|w),2\)\)")
    s, k = pat.subn(lambda m: f"exp(-Math.pow((t-{m.group(1)})/Math.max({m.group(2)},(globalThis.XDT_||.016)*.6),2))", s)
    if k != 26: miss.append(('flash', k))
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
print('fxguard 적용')
