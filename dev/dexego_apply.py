"""11-17: 서번트 도감에 문 캔서(BB) · 얼터 에고(멜트릴리스 · 패션립) 칸이 없던 문제
- 도감은 클래스 9개만 그려서, 세 서번트는 「○ / 135」 숫자에는 들어가는데 카드는 어디에도 보이지 않았다.
- 이제 클래스 목록 끝에 문 캔서 · 얼터 에고를 넣는다. 룰러 · 어벤저처럼 한 명이라도 만나기 전에는 「???」로 가린다.
사용: python3 dexego_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
o = "function renderDex(c){ const H=Sim.HEROES, CL=['sword','lance','bow','rider','caster','shadow','berserk','judge','avenger'].filter(k=>Sim.CLS[k]);"
n = "function renderDex(c){ const H=Sim.HEROES, CL=['sword','lance','bow','rider','caster','shadow','berserk','judge','avenger','moon','ego'].filter(k=>Sim.CLS[k]);"
if n in s: print('이미 적용됨'); sys.exit(0)
if s.count(o) != 1: print('못 찾음', s.count(o)); sys.exit(1)
s = s.replace(o, n)
open(P, 'w', encoding='utf-8').write(s)
print('적용 끝')
