"""11-22: 새로고침 · 새 창에서 소리가 겹쳐 나오던 것 (커뮤니티 제보 11-21, 디시)
- 소리는 숨긴 탭에서만 멈췄다. 창 두 개가 모두 보이거나, 새로고침 직후 옛 페이지가 내려가기 전에는 두 페이지가 같이 울렸다
- 이제 게임 페이지끼리 BroadcastChannel로 알려, 가장 최근에 열리거나 누르거나 포커스를 받은 페이지만 소리를 낸다(다른 페이지는 멈춤, 다시 누르면 되찾음)
- 페이지를 떠날 때(pagehide) 소리를 바로 멈춘다
사용: python3 sndtab_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if "BroadcastChannel('cupnight.snd')" in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n):
    global s
    if s.count(o) != 1: miss.append((o[:80], s.count(o))); return
    s = s.replace(o, n)
rp("  function wake(){ const c=ac(); if(c&&c.state==='suspended'&&!document.hidden) c.resume().catch(()=>{}); return c; }",
   "  function wake(){ const c=ac(); if(c&&c.state==='suspended'&&!document.hidden&&!yielded) c.resume().catch(()=>{}); return c; }")
rp("  document.addEventListener('visibilitychange',()=>{ if(!ctx) return; if(document.hidden) ctx.suspend().catch(()=>{}); else if(on()) ctx.resume().catch(()=>{}); });",
   "  // 11-22: 소리는 가장 최근에 쓴 게임 페이지 하나에서만 (새 창 · 새로고침에서 겹치던 것)\n"
   "  let yielded=false; const tabId=Math.random().toString(36).slice(2); let bc=null;\n"
   "  try{ bc=new BroadcastChannel('cupnight.snd'); bc.onmessage=e=>{ if(e.data&&e.data.id!==tabId){ yielded=true; if(ctx) ctx.suspend().catch(()=>{}); } }; }catch(e){}\n"
   "  const claim=()=>{ if(document.hidden) return; yielded=false; try{ bc&&bc.postMessage({id:tabId}); }catch(e){} if(ctx&&on()) ctx.resume().catch(()=>{}); };\n"
   "  claim(); window.addEventListener('focus',claim); document.addEventListener('pointerdown',claim,true); document.addEventListener('keydown',claim,true);\n"
   "  window.addEventListener('pagehide',()=>{ try{ if(ctx) ctx.suspend(); }catch(e){} });\n"
   "  document.addEventListener('visibilitychange',()=>{ if(!ctx) return; if(document.hidden) ctx.suspend().catch(()=>{}); else claim(); });")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
print('sndtab 적용')
