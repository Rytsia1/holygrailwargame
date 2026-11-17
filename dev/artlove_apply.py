"""11-18: 알트리아 연애 가능 — 연인 불가 목록(REL_NOLOVE)에서 빼고 애정 대사 30줄(artlove_lines.py, 새로 씀)을 넣는다
- 영어 · 일본어: {M} · {K}가 든 줄은 문장 틀({1}), 지문 '(…)'은 따로 사전에. 중국어는 zh/done.json에
- 어린이 서번트(REL_CHILD)는 그대로 우정만
사용: python3 artlove_apply.py <game.html>"""
import sys, re, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n
from artlove_lines import L
H = 'artoria'
SLOTS = ['s1', 's2', 's3', 'morn', 'bye1', 'bye2', 'bye3', 'eve', 'epi', 'cry']
def parts(t):
    m = re.match(r'^\(([^()]*)\)\s*(.*)$', t)
    return (m.group(1), m.group(2)) if m else (None, t)
f1 = lambda x: x.replace('{M}', '{1}').replace('{K}', '{1}')
P = sys.argv[1]
s = open(P, encoding='utf-8').read(); miss = []
m = re.search(r"REL_NOLOVE=\[([^\]]*)\]", s)
ids = [x.strip().strip("'") for x in m.group(1).split(',')]
if H not in ids: print('이미 적용됨'); sys.exit(0)
s = s[:m.start(1)] + ",".join("'" + x + "'" for x in ids if x != H) + s[m.end(1):]
i = s.index('const RLU='); k = s.index('{', i)
R, end = json.JSONDecoder().raw_decode(s[k:])
if 'love' in R[H]: miss.append(('love exists', 1))
for sl in SLOTS:
    if len(L[sl]) != 3: miss.append((sl, len(L[sl])))
R[H] = {'love': {sl: [x[0] for x in L[sl]] for sl in SLOTS}, **R[H]}
s = s[:k] + json.dumps(R, ensure_ascii=False, separators=(',', ':')) + s[k + end:]
D, T, Zn = [], [], {}
for sl in SLOTS:
    for ko, en, ja, zs, zt in L[sl]:
        pk, pe, pj, ps, pt = map(parts, (ko, en, ja, zs, zt))
        if len({x[0] is None for x in (pk, pe, pj, ps, pt)}) != 1: miss.append(('지문 어긋남', ko[:30])); continue
        if pk[0]: D.append((pk[0], pe[0], pj[0])); Zn[pk[0]] = [ps[0], pt[0]]
        rk, re_, rj, rs, rt = pk[1], pe[1], pj[1], ps[1], pt[1]
        if '{M}' in rk or '{K}' in rk: T.append((f1(rk), f1(re_), f1(rj))); Zn[f1(rk)] = [f1(rs), f1(rt)]
        else: D.append((rk, re_, rj)); Zn[rk] = [rs, rt]
if miss: print('못 찾음', miss); sys.exit(1)
s, nd, nt = i18n.add(s, D, T)
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, v in Zn.items():
    if a not in Z: Z[a] = v; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 사전', nd, '· 틀', nt, '· 중국어', n)
