"""연애 가능으로 바꾼 서번트 (11-15): 멀린 · 솔로몬 · 시바의 여왕
- 연인 불가 목록(REL_NOLOVE)에서 뺀다.
- 애정 대사 30줄씩(RLU[id].love)을 넣는다. 멀린 · 시바의 여왕은 시트 「서번트 관계 대사」의 '애정 (제외)' 줄 그대로,
  솔로몬은 '마스터와 함께 세상을 알아가는' 방향으로 새로 썼다(relopen_lines.py).
- 영어 · 일본어: {M} · {K}가 든 줄은 문장 틀({1}), 지문 '(…)'은 따로 사전에.
사용: python3 relopen_apply.py <game.html>"""
import sys, re, json, os, i18n
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from relopen_lines import L
IDS = ['merlin', 'solomon', 'sheba']
SLOTS = ['s1', 's2', 's3', 'morn', 'bye1', 'bye2', 'bye3', 'eve', 'epi', 'cry']
def parts(t):
    m = re.match(r'^\(([^()]*)\)\s*(.*)$', t)
    return (m.group(1), m.group(2)) if m else (None, t)
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    # 연인 불가 목록에서 빼기
    m = re.search(r"REL_NOLOVE=\[([^\]]*)\]", s)
    ids = [x.strip().strip("'") for x in m.group(1).split(',')]
    for h in IDS:
        if h not in ids: miss.append(('nolove ' + h, 0))
    ids = [x for x in ids if x not in IDS]
    s = s[:m.start(1)] + ",".join("'" + x + "'" for x in ids) + s[m.end(1):]
    # 애정 대사
    i = s.index('const RLU='); k = s.index('{', i)
    R, end = json.JSONDecoder().raw_decode(s[k:])
    for h in IDS:
        if 'love' in R[h]: miss.append(('love exists ' + h, 1))
        R[h] = {'love': {sl: [x[0] for x in L[h][sl]] for sl in SLOTS}, **R[h]}
        for sl in SLOTS:
            if len(L[h][sl]) != 3: miss.append((h + ' ' + sl, len(L[h][sl])))
    s = s[:k] + json.dumps(R, ensure_ascii=False, separators=(',', ':')) + s[k + end:]
    # 번역
    D, T = [], []
    for h in IDS:
        for sl in SLOTS:
            for ko, en, ja in L[h][sl]:
                (dk, rk), (de, re_), (dj, rj) = parts(ko), parts(en), parts(ja)
                if (dk is None) != (de is None) or (dk is None) != (dj is None): miss.append(('dir mismatch', ko[:30])); continue
                if dk: D.append((dk, de, dj))
                if '{M}' in rk or '{K}' in rk:
                    f = lambda x: x.replace('{M}', '{1}').replace('{K}', '{1}')
                    T.append((f(rk), f(re_), f(rj)))
                else: D.append((rk, re_, rj))
    s, nd, nt = i18n.add(s, D, T)
    print('relopen miss', miss, 'tr', nd, nt)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
