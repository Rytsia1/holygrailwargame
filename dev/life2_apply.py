"""11-20: 삶 파트 성향 사건 46개 추가 · 성향 사건 1.5배 · 마술과 만나는 사건 2.2배 · 한 해 최대 2개
- 사건: life2_a.py · life2_b.py (⟦한국어¦영어¦일본어¦간체¦번체⟧). 15세 이하는 성장 사건(GROW), 그 위는 삶 사건(EV, 전쟁 전만)
- 기존 성향 사건 38개와 새 사건의 가중치 1.5배(새 사건은 4.5로 적어 둠), 마술과 만나는 사건(mc_/mt_/ma_/mw_) 2.2배
- 한 해의 순서: 마안 → 기술 → 삶 → 성장. 마안·기술 사건이 뜬 해는 그것 하나만.
  그 밖의 해에는 삶 사건과 성장 사건을 따로 굴려 둘 다 뜰 수 있다(성장 사건은 삶 사건을 닫은 뒤 같은 나이에)
사용: python3 life2_apply.py <game.html>"""
import sys, os, json, re
D0 = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D0)
import i18n
from cross2_lib import compile_js
import life2_a, life2_b
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if "{id:'l2_01'" in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

TR = []
G = compile_js(life2_a.GROW + life2_b.GROW, TR)
E = compile_js(life2_a.EV + life2_b.EV, TR)

# 가중치: 기존 성향 사건 ×1.5, 마술과 만나는 사건 ×2.2 (새 사건 넣기 전에)
OLD = 'friend_saw sibling c_bully c_window c_book c_fail c_money first_love rival tell_spouse betrayed injustice testimony grudge relic_archive relic_museum relic_dig relic_rival relic_parcel relic g_ache g_lie g_rep d_ant d_vase d_bully d_bird d_secret t_door t_grave t_mirror t_blood t_museum z_party z_plant z_sick z_root z_memory'.split()
def mul(ids_re, k, expect):
    global s
    n = 0
    def f(m):
        nonlocal n; n += 1
        return "{id:'%s',a:[%s],w:%s" % (m.group(1), m.group(2), round(float(m.group(3)) * k, 3))
    s = re.sub(r"\{id:'(%s)',a:\[([0-9]+,[0-9]+)\],w:([0-9.]+)" % ids_re, f, s)
    if n != expect: miss.append(('가중치 ' + ids_re[:30], n))
mul('|'.join(re.escape(x) for x in OLD), 1.5, len(OLD))
mul(r"m[ctaw]_[a-z_0-9]+", 2.2, 39)

rp("  ];\n  const FOCUS_PICK=", G + "  ];\n  const FOCUS_PICK=")
rp("\n  ];\n  function relicRoom(){", "\n" + E.rstrip('\n') + "\n  ];\n  function relicRoom(){")
# 한 해 최대 2개
rp("    if(!S.pending&&!S.dead) artEvent();\n    if(!S.pending&&!S.dead) rollEvent();\n    if(!S.pending&&!S.dead&&S.age>=3&&S.age<=15&&ch(.8)) growthEvent();",
   """    if(!S.pending&&!S.dead) artEvent();
    const artY=!!S.pending;   // 11-20: 마안·기술 사건이 뜬 해는 그것 하나만
    if(!S.pending&&!S.dead) rollEvent();
    // 11-20: 삶 사건과 성장 사건은 따로 굴린다(한 해 최대 2개). 삶 사건이 떠 있으면 그 창을 닫은 뒤 같은 나이에 성장 사건
    if(!artY&&!S.dead&&S.age>=3&&S.age<=15&&ch(.8)){ if(!S.pending) growthEvent(); else S.growNext=S.age; }""")
rp("    if(S._resume){ const r=S._resume; S._resume=null; resumeAt(r); if(S.pending) return; }",
   "    if(S._resume){ const r=S._resume; S._resume=null; resumeAt(r); if(S.pending) return; }\n    if(S.phase==='life'&&S.growNext!=null){ const a=S.growNext; S.growNext=null; if(a===S.age&&!S.dead){ growthEvent(); H.change(); if(S.pending) return; } }")

if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

# 능력치 변화(d) 번역: 낱말 ↑/↓를 이어 붙인다
ST = {'정신': ('Spirit', '精神', '心灵', '心靈'), '지식': ('Knowledge', '知識', '学识', '學識'), '관계': ('Bonds', '人間関係', '人际', '人際'),
      '마력': ('Mana', '魔力', '魔力', '魔力'), '건강': ('Health', '健康', '健康', '健康'), '재산': ('Wealth', '財産', '财产', '財產')}
ds = sorted(set(re.findall(r",d:'([^']+)'", life2_a.GROW + life2_a.EV + life2_b.GROW + life2_b.EV)))
for d in ds:
    out = [[], [], [], []]
    for tok in d.split(' '):
        m = re.match(r'^(정신|지식|관계|마력|건강|재산)([↑↓]+)$', tok)
        if not m: raise ValueError('d 번역 불가: ' + d)
        for i in range(4): out[i].append(ST[m.group(1)][i] + m.group(2))
    TR.append((d, ' '.join(out[0]), ' '.join(out[1]), ' '.join(out[2]), ' '.join(out[3])))

seen = set(); U = []
for t in TR:
    if t[0] in seen: continue
    seen.add(t[0]); U.append(t)
s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, *_ in U], [])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(D0, 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _b, _c, d, e in U:
    if a not in Z: Z[a] = [d, e]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 사건', (G + E).count("{id:'l2_"), '· 문장', len(U), '· 사전', nd, '· 중국어', n)
