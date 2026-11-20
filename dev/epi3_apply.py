"""11-21: 에필로그 성향 사건 50개 · 서번트가 떠난 삶의 봄(열나흘)과 첫 해
- 성향 사건: epi3_aff.txt → EPI_POOL 맨 앞 (짙음 무게 4 · 깊음 5)
- 떠난 삶: epi3_a.txt · epi3_b.txt · epi3_lines.txt → EP3_EV · 날과 달의 문장. 엔진은 epi3.js
- 글은 한국어|영어|일본어|간체. 번체는 간체를 OpenCC(s2tw)로 바꾸고 따옴표를 「」로
사용: python3 epi3_apply.py <game.html>"""
import sys, os, re, json
D0 = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D0)
import i18n
try:
    from opencc import OpenCC; CC = OpenCC('s2tw')   # pip install opencc-python-reimplemented
except ImportError: CC = None                        # 없으면 done.json에 이미 있는 번체를 쓴다
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'function ep3Step(' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

TR = {}
def zht(z): return None if CC is None else CC.convert(z).replace('“', '「').replace('”', '」').replace('‘', '『').replace('’', '』')
def kq(t): return re.sub(r"'([^']+)'", r'‘\1’', t)   # 한국어 안의 '…' → ‘…’
def T4(x, where):
    p = [y.strip() for y in x.split('|')]
    if len(p) != 4 or not all(p): raise ValueError('칸이 4개가 아님 (%s): %s' % (where, x[:60]))
    ko = kq(p[0]); TR[ko] = (ko, p[1], p[2], p[3], zht(p[3])); return ko
def js(t): return "'" + t.replace('\\', '\\\\').replace("'", "\\'") + "'"
STAT = {'will', 'lore', 'bond', 'mana', 'health', 'wealth'}; AFF = {'avenger', 'judge', 'cruel', 'taboo', 'zeal'}
def fx(src, where):
    src = src.strip()
    if src in ('', '-'): return ''
    if src.startswith('js:'): return src[3:].strip() + ';'
    st, af = [], []
    for tok in src.split():
        m = re.match(r'^([a-z]+)([+-]\d+)$', tok)
        if not m: raise ValueError('효과를 읽지 못함 (%s): %s' % (where, tok))
        k, n = m.group(1), int(m.group(2))
        if k in STAT: st.append('%s:%d' % (k, n))
        elif k in AFF: af.append("lean('%s',%d);" % (k, n))
        else: raise ValueError('모르는 효과 (%s): %s' % (where, k))
    return ('add({%s});' % ','.join(st) if st else '') + ''.join(af)

def parse(path):
    out, cur = [], None
    for ln in open(os.path.join(D0, path), encoding='utf-8'):
        ln = ln.rstrip('\n')
        if not ln.strip() or ln.startswith('#'): continue
        if ln.startswith('@'):
            hd = ln[1:].split(); cur = {'id': hd[0], 'ph': hd[1], 'w': 1, 'B': [], 'C': []}
            for o in hd[2:]:
                if o == 'must': cur['must'] = 1
                elif '=' in o:
                    k, v = o.split('=', 1)
                    cur[k] = float(v) if k == 'w' else v.split(',')
                else: raise ValueError('머리줄 ' + ln)
            out.append(cur); continue
        tag, rest = ln.split(' ', 1)
        if tag == '?': cur['c'] = rest.strip()
        elif tag == 'T': cur['T'] = T4(rest, cur['id'])
        elif tag == 'B': cur['B'].append((None, T4(rest, cur['id'])))
        elif tag.startswith('B?'): cur['B'].append((tag[2:], T4(rest, cur['id'])))
        elif tag in ('C', 'C*'):
            a, f, r = rest.split(' :: ')
            cur['C'].append((T4(a, cur['id']), fx(f, cur['id']), T4(r, cur['id']), tag == 'C*'))
        else: raise ValueError('모르는 줄 ' + ln)
    for e in out:
        if not e.get('T') or not e['B'] or len(e['C']) < 2: raise ValueError('빠진 칸 ' + e['id'])
        if e['B'][-1][0] is not None: raise ValueError('본문 갈래의 마지막이 조건 없음이 아님 ' + e['id'])
        if sum(1 for c in e['C'] if c[3]) != 1: raise ValueError('자동 선택이 하나가 아님 ' + e['id'])
    return out

def body(e):
    b = js(e['B'][-1][1])
    for cnd, t in reversed(e['B'][:-1]): b = '(%s)?%s:%s' % (cnd, js(t), b)
    return b
def dec(e):
    ch = ','.join('{t:%s%s,f:()=>{%sreturn %s;}}' % (js(t), ',auto:true' if au else '', f, js(r)) for t, f, r, au in e['C'])
    return 'decide({title:%s,body:%s,choices:[%s]})' % (js(e['T']), body(e), ch)

AF = parse('epi3_aff.txt')
LA, LB = parse('epi3_a.txt'), parse('epi3_b.txt')
assert len(AF) == 50 and len(LA) == 50 and len(LB) == 50, (len(AF), len(LA), len(LB))
for e in AF: assert e['ph'] == 'P' and e.get('c'), e['id']
for e in LA: assert e['ph'] == 'A'
for e in LB: assert e['ph'] == 'B'
ids = [e['id'] for e in AF + LA + LB]; assert len(ids) == len(set(ids))

pool = ''.join("    {id:'%s',w:%s,c:()=>(%s),f:()=>{ %s%s; }},\n" % (e['id'], ('%g' % e['w']), e['c'],
       ''.join("S.epi.used.includes('%s')||S.epi.used.push('%s'); " % (b, b) for b in e.get('blk', [])), dec(e)) for e in AF)

def lone(e):
    o = ["id:'%s'" % e['id'], "ph:'%s'" % e['ph']]
    if e.get('must'): o.append('must:1')
    if e.get('day'): o.append('day:[%s]' % ','.join(e['day']))
    if e.get('mon'): o.append('mon:[%s]' % ','.join(e['mon']))
    if e.get('k'): o.append('k:%s' % json.dumps(e['k']))
    if e['w'] != 1: o.append('w:%g' % e['w'])
    if e.get('blk'): o.append('blk:%s' % json.dumps(e['blk']))
    if e.get('c'): o.append('c:()=>(%s)' % e['c'])
    o.append('f:()=>%s' % dec(e))
    return '    {' + ','.join(o) + '}'
evjs = '  const EP3_EV=[\n' + ',\n'.join(lone(e) for e in LA + LB) + '\n  ];\n'

# 날과 달의 문장
DAY, DAYK, DAYL, MON, MONK, END = [], {}, {}, {}, {}, None
for ln in open(os.path.join(D0, 'epi3_lines.txt'), encoding='utf-8'):
    ln = ln.rstrip('\n')
    if not ln.strip() or ln.startswith('#'): continue
    tag, rest = ln.split(' ', 1)
    if tag == 'DAY': DAY.append(T4(rest, tag))
    elif tag == 'DAYK': k, t = rest.split(' ', 1); DAYK.setdefault(k, []).append(T4(t, tag))
    elif tag == 'DAYL': k, t = rest.split(' ', 1); DAYL[k] = T4(t, tag)
    elif tag == 'MON': n, t = rest.split(' ', 1); MON[n] = T4(t, tag)
    elif tag == 'MONK': k, n, t = rest.split(' ', 2); MONK.setdefault(k, {})[n] = T4(t, tag)
    elif tag == 'END': END = T4(rest, tag)
assert len(DAY) >= 13 and sorted(MON, key=int) == [str(i) for i in range(2, 13)] and END
J = lambda o: json.dumps(o, ensure_ascii=False)
lines = ('  const EP3_DAY=%s, EP3_DAYK=%s, EP3_DAYL=%s, EP3_MON=%s, EP3_MONK=%s, EP3_END=%s;\n'
         % (J(DAY), J(DAYK), J(DAYL), J(MON), J(MONK), J(END)))

eng = open(os.path.join(D0, 'epi3.js'), encoding='utf-8').read().replace('  /*EP3_DATA*/\n', lines + evjs)
rp("const EPI_POOL=[\n", "const EPI_POOL=[\n" + pool)
rp("  function ep2When(){", eng + "  function ep2When(){")
rp("    if(!E.ph){ if(E.i===1&&stayHome()&&relOf()) ep2Start(); else return false; }\n    if(E.ph==='D') return false;\n",
   "    if(!E.ph){ const lk=E.i===1&&loneKind(); if(E.i===1&&stayHome()&&relOf()) ep2Start(); else if(lk) ep3Start(lk); else return false; }\n    if(E.ph==='D') return false;\n    if(E.lone) return ep3Step();   // 11-21: 서번트가 떠난 삶\n")
rp("    if(id.startsWith('@pool')){", "    if(id.startsWith('@lone')){ const x=EP3_EV.find(x=>x.id===id.slice(5)); if(x){ S.resumeEv={src:'EP2',id}; x.f(); } return; }\n    if(id.startsWith('@pool')){")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

U = list(TR.values())
s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, *_ in U], [])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(D0, 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _b, _c, d, e in U:
    if a not in Z:
        if e is None: raise SystemExit('번체를 만들 OpenCC가 없고 done.json에도 없음: ' + a[:40])
        Z[a] = [d, e]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 성향', len(AF), '· 떠난 삶', len(LA) + len(LB), '· 문장', len(U), '· 사전', nd, '· 중국어', n)
