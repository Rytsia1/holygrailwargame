"""센티넬이 된 서번트의 정체 (11-15)
- 비스트 위기에서 수녀의 서번트가 센티넬이 될 때, 그 조에 대해 이미 알던 것(진명 · 보구)을 이어받지 못해
  정체를 아는 서번트가 '정체 모를 센티넬'로 나오던 것. 탈락한 다른 서번트처럼 이어받게 한다.
  단, 거짓 탈락 통지가 기록용으로 그 조를 '드러남'으로 바꾸므로, 통지 전에 알던 것만 이어받는다.
사용: python3 bxsent_apply.py <game.html>"""
import sys
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:60], k)); return
        s = s.replace(o, n)
    # 거짓 탈락 통지는 기록을 남기려고 그 조를 '드러남'으로 바꾼다 → 그 전에 알던 것만 이어받도록 먼저 적어 둔다
    rp("n.alive=false; n.bxFake=1; n.revealed=true;", "n.bxKnew={r:!!n.revealed,a:!!n.artKnown}; n.alive=false; n.bxFake=1; n.revealed=true;", 2)
    rp("bxMkSent(c.nunHero,{nun:true});",
       "{ const n=bxNunP(), k=n&&(n.bxKnew||{r:!!n.revealed,a:!!n.artKnown}); bxMkSent(c.nunHero,{nun:true,src:n?{revealed:k.r,artKnown:k.a}:undefined}); }")
    print('bxsent miss', miss)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
