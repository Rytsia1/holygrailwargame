"""11-22: 연출 막(#fxCur) — 연출이 뜨기 직전 · 연출이 줄 서 있는 사이에 뒤의 화면이 먼저 보여 스포일러가 되는 문제.
- 소환: 서번트가 정해지는 순간(sndHook 'summon') 막을 친다 → 소환 연출이 화면을 덮으면 걷는다.
  (그 사이 기록 · 서번트 이름 · 첫 만남 창이 뒤에서 먼저 그려진다)
- 검귀 결투(kgduel): 연출이 앞 연출(잔이 가득 차는 순간 등) 뒤에 줄 서 있는 동안 결투 창이 먼저 뜬다 → 연출을 부를 때 막을 치고, 결투 연출이 닫힐 때 걷는다.
- 덤: sndHook 한 줄의 주석이 뒤 case(reveal · ghost)까지 삼키던 것을 줄을 나눠 바로잡는다(진명 · 유령 짧은 곡이 다시 울린다).
사용: python3 fxcur_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read(); miss = []
def rp(o, n):
    global s
    if s.count(o) != 1: miss.append((o[:70], s.count(o))); return
    s = s.replace(o, n)
rp("case 'summon': break; // 소환 소리는 첫 만남 화면이 뜰 때 소환 연출과 함께 울린다(summonGo) case 'reveal':",
   "case 'summon': { const h=Sim.hero(), w=Sim.S&&Sim.S.war; if(xfxOK()&&h&&(!w||w._sfx!==h.id)) fxCurOn(); } break; // 소환 소리는 첫 만남 화면이 뜰 때 소환 연출과 함께 울린다(summonGo). 그때까지 막을 친다\n  case 'reveal':")
rp("function summonGo(){", """// 11-22: 연출이 뜨기 전 · 연출 사이에 뒤의 화면(서번트 이름 · 결투 창)이 먼저 보이지 않게 덮는 막. 12초 넘게 남지 않는다
function fxCurOn(){ let c=$('#fxCur'); if(!c){ c=document.createElement('div'); c.id='fxCur'; c.setAttribute('aria-hidden','true'); document.body.appendChild(c); } c.classList.remove('off'); clearTimeout(c._t); c._t=setTimeout(fxCurOff,12000); }
function fxCurOff(){ const c=$('#fxCur'); if(!c||c.classList.contains('off')) return; clearTimeout(c._t); c.classList.add('off'); setTimeout(()=>{ if(c.isConnected&&c.classList.contains('off')) c.remove(); },520); }
function summonGo(){""")
rp("if(!Sim.hero()){ try{ Snd.jingle('j_summon'); }catch(e){} return; } xfxGo(sumSndK(),()=>summonFx()); }",
   "if(!Sim.hero()){ fxCurOff(); try{ Snd.jingle('j_summon'); }catch(e){} return; } if(!xfxOK()) fxCurOff(); xfxGo(sumSndK(),()=>summonFx()); }")
rp("document.body.appendChild(o); document.body.appendChild(fly); sh.classList.remove('sfx-show');",
   "document.body.appendChild(o); document.body.appendChild(fly); fxCurOff(); sh.classList.remove('sfx-show');")
rp("function kgDuelFx(fx){ xfxGo(", "function kgDuelFx(fx){ if(xfxOK()) fxCurOn(); xfxGo(")
rp(".sfx{position:fixed;inset:0;z-index:60;", "#fxCur{position:fixed;inset:0;z-index:59;background:#08070c;pointer-events:none;transition:opacity .45s ease}#fxCur.off{opacity:0}\n.sfx{position:fixed;inset:0;z-index:60;")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
print('fxcur 적용')
