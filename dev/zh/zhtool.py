"""중국어(간체 zhs · 번체 zht) 번역 작업 도구 — 사용법은 dev/zh/README.md
  python3 dev/zh/zhtool.py extract [game.html]   원문 목록(src.jsonl)을 지금 빌드에서 다시 뽑는다 (이미 번역한 것은 그대로)
  python3 dev/zh/zhtool.py next [글자수]          아직 번역하지 않은 다음 묶음을 보여 준다 (한국어 K · 일본어 J)
  python3 dev/zh/zhtool.py ingest <파일>          번역 묶음(#id / S: / T:)을 검사해 done.json에 넣는다
  python3 dev/zh/zhtool.py stats                  진행 현황
"""
import sys, os, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(HERE, 'src.jsonl'); DONE = os.path.join(HERE, 'done.json')
HANGUL = re.compile('[가-힣]')

def blk(s, name):
    m = re.search(r"(?:const|var|let)\s+" + name + r"\s*=\s*(\{.*?\});\n", s, re.S); return json.loads(m.group(1))
def load_src(): return [json.loads(l) for l in open(SRC, encoding='utf-8')] if os.path.exists(SRC) else []
def load_done(): return json.load(open(DONE, encoding='utf-8')) if os.path.exists(DONE) else {}
def save_done(d):
    tmp = DONE + '.tmp'; json.dump(d, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0); os.replace(tmp, DONE)

def extract(path):
    s = open(path, encoding='utf-8').read(); D = blk(s, 'I18N_DICT'); T = blk(s, 'I18N_TPL')
    old = {x['ko']: x['id'] for x in load_src()}; nid = max(old.values(), default=0) + 1
    rows = []; seen = set()
    def add(kind, ko, en, ja):
        nonlocal nid
        if ko in seen: return
        seen.add(ko); i = old.get(ko)
        if i is None: i = nid; nid += 1
        rows.append({'id': i, 'k': kind, 'ko': ko, 'en': en, 'ja': ja})
    for ko, en in D['en'].items(): add('d', ko, en, D['ja'].get(ko, ''))
    ja_t = {x[0]: x[1] for x in T['ja']}
    for x in T['en']: add('t', x[0], x[1], ja_t.get(x[0], ''))
    rows.sort(key=lambda r: r['id'])
    with open(SRC, 'w', encoding='utf-8') as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print('원문', len(rows), '(새로', sum(1 for r in rows if r['ko'] not in old), ')')

def esc(t): return t.replace('\\', '\\\\').replace('\n', '\\n')
def unesc(t): return re.sub(r'\\(.)', lambda m: '\n' if m.group(1) == 'n' else m.group(1), t)

_OFF = None
def off_hints(ja):
    global _OFF
    if _OFF is None:
        o = json.load(open(os.path.join(HERE, 'official/names.json'), encoding='utf-8'))
        _OFF = sorted(((k, v) for k, v in o.items() if len(k) >= 3 and v[0]), key=lambda x: -len(x[0]))
    hs = []; seen = ja
    for k, v in _OFF:
        if k in seen: hs.append(f"{k}={v[0]}/{v[1] or v[0]}"); seen = seen.replace(k, '')
        if len(hs) >= 4: break
    return hs

def nxt(budget):
    done = load_done(); n = 0; out = []
    for r in load_src():
        if r['ko'] in done: continue
        h = off_hints(r['ja'] or '')
        out.append(f"#{r['id']}{' tpl' if r['k']=='t' else ''}\nK: {esc(r['ko'])}\nJ: {esc(r['ja'] or r['en'])}" + (f"\n= {' · '.join(h)}" if h else ''))
        n += len(r['ko'])
        if n >= budget: break
    print('\n'.join(out))

PH = re.compile(r'\{\d\}')
TAG = re.compile(r'</?[a-zA-Z][^>]*>')
def check(r, zs, zt):
    errs = []
    ref = r['en'] or r['ja']
    for nm, z in (('S', zs), ('T', zt)):
        if not z.strip(): errs.append(nm + ' 비었음'); continue
        if HANGUL.search(z): errs.append(nm + ' 한글 남음')
        if sorted(PH.findall(z)) != sorted(PH.findall(ref)): errs.append(f"{nm} 자리표시자 {PH.findall(z)} ≠ {PH.findall(ref)}")
        if sorted(TAG.findall(z)) != sorted(TAG.findall(ref)): errs.append(f"{nm} 태그 다름")
        if z.count('\n') != r['ko'].count('\n'): errs.append(nm + ' 줄 수 다름')
    return errs

def ingest(path):
    src = {str(r['id']): r for r in load_src()}; done = load_done()
    txt = open(path, encoding='utf-8').read(); bad = []; ok = 0
    for blkt in re.split(r'\n(?=#\d)', txt.strip()):
        m = re.match(r'#(\d+)[^\n]*\nS: (.*)\nT: (.*)$', blkt.strip(), re.S)
        if not m: bad.append(('형식', blkt[:60])); continue
        i, zs, zt = m.group(1), unesc(m.group(2).strip()), unesc(m.group(3).strip())
        r = src.get(i)
        if not r: bad.append((i, '원문 없음')); continue
        e = check(r, zs, zt)
        if e: bad.append((i, e)); continue
        done[r['ko']] = [zs, zt]; ok += 1
    save_done(done)
    print('넣음', ok, '문제', len(bad))
    for b in bad: print('  ', b)

def prefill():
    """공식 이름과 일본어가 정확히 같은 문장은 공식 간체 · 번체로 채운다(번체가 비면 건너뜀)"""
    o = json.load(open(os.path.join(HERE, 'official/names.json'), encoding='utf-8')); done = load_done(); n = 0
    for r in load_src():
        v = o.get(r['ja'])
        if r['ko'] in done or not v or not v[0] or not v[1]: continue
        done[r['ko']] = [v[0], v[1]]; n += 1
    save_done(done); print('공식 이름으로 채움', n)

def stats():
    src = load_src(); done = load_done()
    n = sum(1 for r in src if r['ko'] in done); c = sum(len(r['ko']) for r in src); cd = sum(len(r['ko']) for r in src if r['ko'] in done)
    print(f"문장 {n}/{len(src)} · 한국어 글자 {cd}/{c} ({100*cd/max(1,c):.1f}%)")

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__)
    elif a[0] == 'extract': extract(a[1] if len(a) > 1 else os.path.join(ROOT, 'public/index.html'))
    elif a[0] == 'next': nxt(int(a[1]) if len(a) > 1 else 5000)
    elif a[0] == 'ingest': ingest(a[1])
    elif a[0] == 'stats': stats()
    elif a[0] == 'prefill': prefill()
