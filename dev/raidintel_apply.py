"""습격받아 얻은 단서로는 소원을 알 수 없다 (11-15)
- 아처의 저격(저격 사건 · 나를 노린 저격)과 어새신의 암습을 막아 내며 얻는 단서를 'raid'로 따로 표시한다.
  거처는 지금처럼 알아낼 수 있지만(쏜 방향 · 남은 흔적), 상대 마스터의 소원은 이것만으로는 드러나지 않는다.
  소원은 정찰 · 뒤밟기 · 대화처럼 그 사람을 알아 가는 단서가 쌓였을 때만.
- 단서 문장(이름 · 진명이 드러날 때의 말투)은 지금처럼 '흔적' 쪽을 쓴다.
사용: python3 raidintel_apply.py <game.html>"""
import sys
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("if(loc&&(!t.wishKnown||t.bxNun&&!t.bxWishTrue)&&t.intel>=50)",
       "if(loc&&why!=='raid'&&(!t.wishKnown||t.bxNun&&!t.bxWishTrue)&&t.intel>=50)")   # 습격받아 얻은 단서로는 소원까지 알 수 없다
    rp("const T=INTEL_SRC[why==='btalk'?'talk':why==='watch'?'trail':why]",
       "const T=INTEL_SRC[why==='btalk'?'talk':why==='watch'||why==='raid'?'trail':why]")
    # 저격 사건
    rp("addIntel(p,15);return '세 발을 더 피했다.", "addIntel(p,15,'raid');return '세 발을 더 피했다.")
    rp("addIntel(p,40);w.queue.unshift(()=>battle(p,{attack:true}));return '서번트가 빗발치는",
       "addIntel(p,40,'raid');w.queue.unshift(()=>battle(p,{attack:true}));return '서번트가 빗발치는")
    # 암습 · 나를 노린 저격: 그 구간의 'trail'만 'raid'로
    a = s.find("{w:0,title:'ambush'"); b0 = s.find("function snipeAtMe(p){"); b = s.find("\n  WAR_EV.push(", b0)
    if a < 0 or b0 < a or b < b0: miss.append(('ambush..snipeAtMe span', a, b0, b))
    else:
        seg = s[a:b]; n = seg.count("'trail')")
        if n != 7: miss.append(('trail count in span', n))
        else: s = s[:a] + seg.replace("'trail')", "'raid')") + s[b:]
    print('raidintel miss', miss)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
