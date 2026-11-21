"""11-21: 검귀 루트 배경음악 K1~K7 (모두 오리지널 작곡, dev/kgbgm/*.py · 공통 엔진 eng.py · FluidR3 GM 렌더 + 합성 층).
참고곡(사무라이 렘넌트 OST)의 템포 · 구성 · 짜임만 재서 맞췄고 소리 · 선율 · 화성은 쓰지 않았다.
- K1 kgduel  마스터 대 서번트 결투(w.duel.ctx가 있는 동안)
- K2 kgday · K3 kgnight  본성 속 진심 나흘의 낮 · 밤(w.kg가 끝나지 않았을 때)
- K6 kglast  마지막 밤: 잔이 가득 찬 뒤(kgFinal이 g.fin을 켬) 결전 · 결투가 시작되기 전까지
- K7 kgally  잔을 막으러 온 동맹과의 결전(battle ctx.kgAlly) · 결전 사이사이(동맹 결전이 시작된 뒤 끝나기 전)에도 이어서
- K4 kgbound  묶인 잔(③) 에필로그
- K5 end_kg  검귀 결말의 결과 화면(기록 r.kg) · j_end_kg은 그 앞부분 14초(결말 연출 소리 j_end_kgF/S/T도 이것을 뒤에 붙임, 나머지 검귀 결말 연출은 j_end_kg)
사용: python3 kgbgm_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read(); miss = []
def rp(o, n):
    global s
    if s.count(o) != 1: miss.append((o[:70], s.count(o))); return
    s = s.replace(o, n)
M = {'kgally': (81.668, 4.272, 81.168), 'kgduel': (99.5, 15.0, 99.0), 'kgday': (94.25, 18.75, 93.75), 'kgnight': (100.5, 12.0, 100.0),
     'kgbound': (71.75, 11.25, 71.25), 'kglast': (56.5, 8.0, 56.0), 'end_kg': (140.02, 30.52, 139.52)}
rp('"final":{"d":73.93,"ls":10.07,"le":73.43}', '"final":{"d":73.93,"ls":10.07,"le":73.43},' + ','.join(f'"{k}":{{"d":{d},"ls":{a},"le":{b}}}' for k, (d, a, b) in M.items()) + ',"j_end_kg":{"d":14.04}')
rp("if(S.phase==='epi') return 'epi';", "if(S.phase==='epi') return S.flags.kgEnd==='b'?'kgbound':'epi';")
rp("  const b=w.battle; if(b&&b.e){", "  if(w.duel&&w.duel.ctx) return 'kgduel';\n  const b=w.battle; if(b&&b.e){")
rp("if(b.ctx&&b.ctx.final) return 'final';", "if(b.ctx&&b.ctx.kgAlly) return 'kgally'; if(b.ctx&&b.ctx.final) return 'final';")
rp("  return w.tod==='밤'?'night':'day';\n}", "  if(w.kg&&!w.kg.done) return S.flags.kgAllyFight&&w.kg.fin?'kgally':w.kg.fin?'kglast':w.tod==='밤'?'kgnight':'kgday';\n  return w.tod==='밤'?'night':'day';\n}")
rp("bx:S.flags.bxEnd?'moon':S.flags.bxDream?'dream':'',", "bx:S.flags.bxEnd?'moon':S.flags.bxDream?'dream':'', kg:S.flags.kgEnd||'',")
rp("function sndEndOf(r){ if(r.bx==='moon') return 'f';", "function sndEndOf(r){ if(r.kg) return 'kg'; if(r.bx==='moon') return 'f';")
rp("const END_SK={", "const END_SK={kgM:'j_end_kg',kgB:'j_end_kg',kgP:'j_end_kg',kgP2:'j_end_kg',kgX:'j_end_kg',")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
