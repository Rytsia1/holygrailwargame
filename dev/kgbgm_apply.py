"""11-21: 검귀 루트 배경음악. 지금은 K7 동맹 결전(kgally)만: 검귀 루트에서 잔을 막으러 온 동맹과의 결전(battle ctx.kgAlly) 동안 최후의 결전 곡(final) 대신 튼다.
곡은 오리지널 작곡(dev/kgbgm/k7_ally.py, 공통 엔진 eng.py · FluidR3 GM 렌더 + 합성 층). 참고곡의 템포 · 구성 · 짜임만 재서 맞췄고 소리는 쓰지 않았다.
사용: python3 kgbgm_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read(); miss = []
def rp(o, n):
    global s
    if s.count(o) != 1: miss.append((o[:60], s.count(o))); return
    s = s.replace(o, n)
rp('"final":{"d":73.93,"ls":10.07,"le":73.43}', '"final":{"d":73.93,"ls":10.07,"le":73.43},"kgally":{"d":81.668,"ls":4.272,"le":81.168}')
rp("if(b.ctx&&b.ctx.final) return 'final';", "if(b.ctx&&b.ctx.kgAlly) return 'kgally'; if(b.ctx&&b.ctx.final) return 'final';")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
