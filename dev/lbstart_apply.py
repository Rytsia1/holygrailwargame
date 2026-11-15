"""로비 시작 화면 소리 (11-15)
- Enter·Space로 「press to start」를 넘겨도 소리를 깨운다(전에는 마우스·터치로 누를 때만 깨워서, 키보드로 넘기면 배경음악이 나오지 않았다)
- 「press to start」를 넘길 때(누름 · Enter · Space) 시작음 u_start(B안 「잔이 울림」: 유리잔 같은 맑은 음 + 낮게 부푸는 5도 화음, 3.8초). 소리를 켰을 때만 울린다
  u_ 효과음 맨 앞에 두어 소리를 켜면 가장 먼저 미리 받는다
사용: python3 lbstart_apply.py <game.html>"""
import sys
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("document.addEventListener('pointerdown',()=>{ if(on()) wake(); },{passive:true});",
       "document.addEventListener('pointerdown',()=>{ if(on()) wake(); },{passive:true});\n"
       "  document.addEventListener('keydown',e=>{ if(on()&&!e.repeat) wake(); },true); // 키보드로 시작해도 소리를 깨운다")
    rp('"u_choice":{"d":0.306}', '"u_start":{"d":3.776},"u_choice":{"d":0.306}')
    rp(".snd-ask')) return;\n    setStage(2); });",
       ".snd-ask')) return;\n    lbGo(); });")
    rp("    e.preventDefault(); setStage(2); });",
       "    e.preventDefault(); lbGo(); });")
    rp("  const busy=()=>",
       "  const lbGo=()=>{ try{ Snd.sfx('u_start',{gap:0}); }catch(e){} setStage(2); }; // 시작음\n  const busy=()=>")
    if miss: print('못 찾음:', miss); sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s); print('ok', P)
