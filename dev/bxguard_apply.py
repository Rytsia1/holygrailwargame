"""11-17: 비스트 위기 업적 「호위를 걷어 내다」가 강림 전에 센티넬을 다 잡으면 열리지 않던 문제
- 예전: 강림(3단계) 순간 살아 있던 센티넬만 '호위'가 되고, 업적은 '호위가 1명 이상 있었고 모두 쓰러졌을 때'만 열렸다.
  강림 전에 센티넬을 모두 잡으면 호위가 0명이라 절대 열리지 않았다(커뮤니티 제보 11-17).
- 이제: 센티넬이 한 번이라도 나왔고, 키아라를 쓰러뜨릴 때 살아 있는 센티넬이 하나도 없으면 연다(누가 잡았든).
  센티넬이 아예 안 나온 판은 열리지 않고, 키아라는 직접 쓰러뜨려야 한다는 조건은 그대로.
- 업적 설명: '호위 센티넬을 모두…' → '센티넬을 모두…'
사용: python3 bxguard_apply.py <game.html>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if '강림 전에 다 잡아도' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:80], k)); return
    s = s.replace(o, n)

rp("    { const G=(c.units||[]).filter(u=>u.cx==='sent'&&u.guard); c.guardAll=G.length>0&&G.every(u=>!u.alive)?1:0; }",
   "    // 센티넬을 모두 걷어 냈는가: 강림 전에 다 잡아도(호위 0명) 강림 뒤 호위를 다 걷어 내도 같다. 센티넬이 안 나온 판은 아니다\n"
   "    { const G=(c.units||[]).filter(u=>u.cx==='sent'); c.guardAll=G.length>0&&G.every(u=>!u.alive)?1:0; }")
OLD_D, NEW_D = '호위 센티넬을 모두 걷어 내고 키아라를 쓰러뜨렸다', '센티넬을 모두 걷어 내고 키아라를 쓰러뜨렸다'
rp("n:'호위를 걷어 내다',d:'" + OLD_D + "'", "n:'호위를 걷어 내다',d:'" + NEW_D + "'")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

D = [(NEW_D, 'Defeated Kiara after every Sentinel had fallen', 'センチネルをすべて退け、キアラを倒した',
      '剥除了所有哨兵并击倒了祈荒', '剝除了所有哨兵並擊倒了祈荒')]
s, nd, nt = i18n.add(s, dict_items=[(a, b, c) for a, b, c, *_ in D])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
if os.path.exists(zp):
    Z = json.load(open(zp, encoding='utf-8')); n = 0
    for a, _b, _c, d, e in D:
        if a not in Z: Z[a] = [d, e]; n += 1
    json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0); print('중국어 사전', n)
print('적용 끝 · 사전', nd)
