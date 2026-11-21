"""11-21: 검귀 루트 「검을 거두지 않은 자」 — 진짜 소원 · 나흘 · 결말 ①~⑥ · 에필로그 사건 220 · 후일담 150 · 서번트별 대사 945
- 엔진: kg.js (Sim 안, battleRound 앞)
- 글의 원본: kg/epi.json(「검귀 에필로그 안」) · kg/sv.json(「검귀 서번트별 대사」) · kg/ov.py(비고 칸을 조건으로)
- 번역: kg/tr_e.txt · tr_a.txt · tr_s.txt (번호|영어|일본어|간체) · kg/tre.txt (한국어|영어|일본어|간체, 틀은 앞에 T) · kg/lines.txt
- 번체는 간체를 OpenCC(s2tw)로
사용: python3 kg_apply.py <game.html> [--dump 파일] [--loose]"""
import sys, os, re, json
D0 = os.path.dirname(os.path.abspath(__file__)); KD = os.path.join(D0, 'kg')
sys.path.insert(0, D0); sys.path.insert(0, KD)
import i18n
from ov import OV
try:
    from opencc import OpenCC; CC = OpenCC('s2tw')
except ImportError: CC = None
args = sys.argv[1:]; P = args[0]
DUMP = args[args.index('--dump') + 1] if '--dump' in args else None
LOOSE = '--loose' in args
s = open(P, encoding='utf-8').read()
if 'function kgStart(' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:100], k)); return
    s = s.replace(o, n)
def js(t): return "'" + t.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n') + "'"
def zht(z): return None if CC is None else CC.convert(z).replace('“', '「').replace('”', '」').replace('‘', '『').replace('’', '』')

# ---------- 글 모음: (번호, 한국어) ----------
KO = {}        # 번호 → 한국어
def K(i, t):
    t = t.strip()
    if not t: return None
    KO[i] = t; return t

# ---------- 효과 ----------
EFF = {'정신': 'will', '건강': 'health', '재산': 'wealth', '지식': 'lore', '관계': 'bond'}
AFF = {'복수': 'avenger', '정의': 'judge', '잔혹': 'cruel', '금기': 'taboo', '근원집착': 'zeal'}
ARW = {'↑': 3, '↑↑': 6, '↓': -3, '↓↓': -6}
AR_RE = re.compile(r'^(정신|건강|재산|지식|관계|인연)(↑↑|↓↓|↑|↓)$')
def efx(res, where):
    """결과 칸 → (글, JS)"""
    a = res.replace('−', '-')
    b = a.replace('근원 집착', '근원집착').replace('소원 성향', '소원성향')
    segA = [x.strip() for x in a.split(' · ')]; segB = [x.strip() for x in b.split(' · ')]
    assert len(segA) == len(segB), where
    txt, st, js_ = [], {}, []
    for sa, sb in zip(segA, segB):
        if sb in ('', '변화 없음'): continue
        if sb == '인연의 흔적': js_.append('S.flags.kgTrace=1;'); continue
        toks = sb.split(); ok = True; tmp_st = {}; tmp_js = []; i = 0
        while i < len(toks):
            t = toks[i]; m = AR_RE.match(t)
            if m:
                k, v = m.group(1), ARW[m.group(2)]
                if k == '인연': tmp_js.append('kgRel(%d);' % (v * 4 // 3))
                else: tmp_st[EFF[k]] = tmp_st.get(EFF[k], 0) + v
                i += 1; continue
            if (t in AFF or t == '소원성향') and i + 1 < len(toks) and re.match(r'^[+-]\d$', toks[i + 1]):
                n = int(toks[i + 1])
                tmp_js.append("lean('%s',%d);" % (AFF[t], n) if t in AFF else 'if(S.flags.kg) lean(S.flags.kg,%d);' % n)
                i += 2; continue
            ok = False; break
        if ok:
            for k, v in tmp_st.items(): st[k] = st.get(k, 0) + v
            js_ += tmp_js
        else: txt.append(sa)
    t = '. '.join(x.rstrip('.') for x in txt)
    if t and not re.search(r'[.!?…」”)]$', t): t += '.'
    code = ('add({%s});' % ','.join('%s:%d' % kv for kv in st.items()) if st else '') + ''.join(js_)
    return t, code

# ---------- 조건 ----------
TR = {'복수': 'avenger', '정의': 'judge', '잔혹': 'cruel', '금기': 'taboo', '근원 집착': 'zeal'}
PH = {'첫 열나흘': 'A', '첫 해': 'B', '첫 해 끝': 'B12', '둘째 해 이후': 'C', '마지막 해': 'Z'}
CN = {
 '마술사': 'lkM()', '인연 2단계 이상': 'kgS()>=2', '인연 0~1단계': 'kgS()<=1', '인연 2단계': 'kgS()===2', '인연 3단계': 'kgS()>=3',
 '둘째 날 지킴': 'S.flags.kgSaved===1', '둘째 날 내버려 둠': 'S.flags.kgSaved===0',
 '가족': "S.flags.kgWho==='fam'", '친구': "S.flags.kgWho==='friend'", '제자': "S.flags.kgWho==='pupil'", '이웃': "S.flags.kgWho==='nbr'",
 '령주 남음': 'kgSeals()>0',
 '출신 교회': "S.origin==='church'", '출신 마술 가문': "['noble','noble2'].includes(S.origin)", '출신 몰락 가문': "S.origin==='fallen'",
 '출신 퇴마': "S.origin==='exorcist'", '출신 보육원': "S.origin==='orphan'", '출신 평범한 가정': "S.origin==='common'", '가족 있음': 'lkFam()',
 '친구 있음': 'kgFriend()', '제자 있음': '!!S.flags.student', '배우자 있음': '!!(S.fam.spouse&&S.fam.spouse.alive)', '아이 있음': 'lkKid()',
 '동맹 결전 이김': '!!S.flags.kgAllyWin', '동맹 마스터 생존': 'kgAllyAlive()', '동맹 결전 없음': '!S.flags.kgAllyFight',
 '동맹 서번트 남음': 'kgAllySv()', '동맹 마스터 쓰러짐': 'kgAllyFell()', '관계 낮음': 'S.st.bond<35',
 '서번트 곁에 남음': 'stayHome()', '서번트 떠남': '!stayHome()',
 '넷째 날 걷기': "S.flags.kgWalk==='walk'", '넷째 날 밥': "S.flags.kgWalk==='eat'",
 '함께 소원을 빌던 동맹': '!!S.flags.kgShared', '의심 2 이상': '(S.flags.kgSus||0)>=2', '의심 2 미만': '(S.flags.kgSus||0)<2',
 '연인': '!!S.flags.kgLover', '지기': None, '지기 아님': '!S.flags.kgLover', '다른 조건 없음': None,
}
def cond(src, where, cw=False):
    toks = [x.strip() for x in src.split(' · ') if x.strip()]
    if '지기 아님' in toks and '연인' in toks: toks.remove('연인')
    ph, cs, n = None, [], 0
    for t in toks:
        if t in PH: ph = PH[t]; continue
        if t.startswith('진짜 소원 '): cs.append("S.flags.kg==='%s'" % TR[t[6:]]); n += 1; continue
        if cw and t in ('넷째 날 걷기', '넷째 날 밥'): cs.append('!!S.flags.kgWalk'); n += 1; continue
        if t not in CN: raise SystemExit('모르는 조건 (%s): %s' % (where, t))
        if CN[t]: cs.append(CN[t]); n += 1
    return ph, cs, n

GRP = {'③': 'b', '⑤': 'p', '⑥': 'x'}
AFG = {'① 서번트 승 · 후일담': 's', '① 마스터 승 · 후일담': 'm', '② 함께 간다 · 마지막 두 줄': 't',
       '④ 함께 가는 척한다 · 서번트 시점': 'f', '④ 함께 가는 척한다 · 가까운 사람 시점': 'fn'}
ROWS = json.load(open(os.path.join(KD, 'epi.json'), encoding='utf-8'))[2:]
assert len(ROWS) == 370

def fieldexpr(n, pre, f, base, ov):
    """칸의 JS 식: 원문 + 조건별 갈래"""
    for fld, a, b in ov.get('rep', []):
        if fld == f: assert a in base, (n, f, a); base = base.replace(a, b).strip()
    bid = K('%s%d%s' % (pre, n, f), base) if base else None
    groups = {}
    for c, fld, a, b in ov.get('var', []):
        if fld == f: groups.setdefault(c, []).append((a, b))
    e = js(base)
    for j, (c, reps) in enumerate(reversed(list(groups.items()))):
        v = base
        for a, b in reps:
            if a is None: v = b
            else: assert a in v, (n, f, a); v = v.replace(a, b)
        K('%s%d%s@%d' % (pre, n, f, j), v)
        e = '(%s)?%s:%s' % (c, js(v), e)
    return e, base

EV, POOLX, AFX = [], [], []
for r in ROWS:
    n = int(r[0]); grp, cnd = r[1], r[2]; ov = OV.get(n, {})
    if n <= 220:
        e = GRP[grp[0]]
        ph, cs, _ = cond(cnd, n)
        ph = ov.get('ph', ph); mon = None
        if ph == 'B12': ph, mon = 'B', 12
        if ov.get('c'): cs.append(ov['c'])
        tE, _ = fieldexpr(n, 'k', 't', r[3], ov); bE, _ = fieldexpr(n, 'k', 'b', r[4], ov)
        chs = []
        for i in (1, 2, 3):
            ct, rt = r[2 + 3 * i].strip(), r[3 + 3 * i].strip()
            if not ct: continue
            rtext, code = efx(rt, '%d-%d' % (n, i))
            for fld, a, b in ov.get('rep', []):
                if fld == 'r%d' % i: assert a in rt, (n, a); rtext, _c = efx(rt.replace(a, b), n)
            if i in ov.get('fx', {}): code = ov['fx'][i]
            if i in ov.get('fxa', {}): code += ov['fxa'][i]
            if i in ov.get('fxv', {}): vc, vj = ov['fxv'][i]; code = 'if(%s){%s}else{%s}' % (vc, vj, code)
            cE, _ = fieldexpr(n, 'k', 'c%d' % i, ct, ov)
            ov2 = {'var': ov.get('var', [])}
            rE, _ = fieldexpr(n, 'k', 'r%d' % i, rtext, ov2) if (rtext or any(v[1] == 'r%d' % i for v in ov.get('var', []))) else ("''", '')
            res = ov.get('res', {}).get(i, '')
            off = ov.get('off', {}).get(i); only = ov.get('only', {}).get(i)
            if ph == 'Z': body = '%s{ const r_=%s; if(r_) log(r_,\'n\'); }%sif(then) then(); return \'\';' % (code, rE, res)
            else: body = '%s%sreturn %s;' % (code, res, rE)
            o = '{t:%s%s%s,f:()=>{%s}}' % (cE, ',auto:true' if not chs else '', ',off:(%s)' % off if off else '', body)
            if only: o = '...((%s)?[%s]:[])' % (only, o)
            chs.append(o)
        assert len(chs) >= 2, n
        dec = 'decide({title:%s,body:%s,choices:[%s]})' % (tE, bE, ','.join(chs))
        cj = '&&'.join('(%s)' % x for x in cs) or 'true'
        if e == 'p' and ph == 'C':
            POOLX.append("    {id:'kg%d',w:3,c:()=>(!!S.flags.kg5&&%s),f:()=>{ %s%s; }},\n" % (n, cj, ov.get('pre', ''), dec)); continue
        EV.append("    {id:'k%d',e:'%s',ph:'%s'%s,c:()=>(%s),f:(then)=>{ %s%s; }}" % (n, e, ph, ',mon:%d' % mon if mon else '', cj, ov.get('pre', ''), dec))
    else:
        k = AFG[grp]
        _ph, cs, sp = cond(cnd, n, ov.get('cw'))
        if k == 't' and '동맹 결전 이김' in cnd: sp += 10
        if ov.get('c'): cs.append(ov['c']); sp += 1
        tE, _ = fieldexpr(n, 'a', 't', r[3], ov)
        ls = [x.strip() for x in r[4].split('\n') if x.strip()]
        assert 1 <= len(ls) <= 3, n
        bs = [fieldexpr(n, 'a', 'b%d' % (j + 1), l, ov)[0] for j, l in enumerate(ls)]
        cj = '&&'.join('(%s)' % x for x in cs) or 'true'
        AFX.append("    {k:'%s',sp:%d,c:()=>(%s),t:()=>%s,b:()=>[%s]}" % (k, sp, cj, tE, ','.join(bs)))
assert len(EV) + len(POOLX) == 220 and len(AFX) == 150, (len(EV), len(POOLX), len(AFX))

# ---------- 서번트별 대사 ----------
SVR = json.load(open(os.path.join(KD, 'sv.json'), encoding='utf-8'))
SV = {}
for r in SVR[1:]:
    if not r[0] or r[0] == '공통': continue
    SV[r[0]] = [K('s:%s:%d' % (r[0], i), r[3 + i]) or '' for i in range(7)]
assert len(SV) == 135, len(SV)
COM = {r[1][:6]: r for r in SVR if r and r[0] == '공통'}
cw = next(r for r in SVR if r and r[0] == '공통' and r[1].startswith('④'))
ca = next(r for r in SVR if r and r[0] == '공통' and r[1].startswith('⑥-186'))
WHEN = [K('w%d' % i, cw[3 + i]) for i in range(4)]
ALLYV = [K('y%d' % i, ca[3 + i]) for i in range(3)]

# ---------- 날 · 달 · 해의 문장 · 복선 (4개 언어를 한 줄에) ----------
TRL = {}   # 한국어 → (영, 일, 간)
def L4(x, where):
    p = [y.strip() for y in x.split('|')]
    if len(p) != 4 or not all(p): raise SystemExit('칸이 4개가 아님 (%s): %s' % (where, x[:60]))
    TRL[p[0]] = tuple(p[1:]); return p[0]
DAY, DAYL, MON, YR, OMEN, OMENW = [], None, {}, [], {}, {}
for ln in open(os.path.join(KD, 'lines.txt'), encoding='utf-8'):
    ln = ln.rstrip('\n')
    if not ln.strip() or ln.startswith('#'): continue
    tag, rest = ln.split(' ', 1)
    if tag == 'DAY': DAY.append(L4(rest, tag))
    elif tag == 'DAYL': DAYL = L4(rest, tag)
    elif tag == 'MON': m, t = rest.split(' ', 1); MON[m] = L4(t, tag)
    elif tag == 'YR': YR.append(L4(rest, tag))
    elif tag == 'OMEN': k, t = rest.split(' ', 1); OMEN.setdefault(k, []).append(L4(t, tag))
    elif tag == 'OMENW':
        st, a, rg, t = rest.split(' ', 3)
        OMENW.setdefault(st, {}).setdefault(a, {})[rg] = L4(t, tag)
assert len(DAY) >= 13 and DAYL and sorted(MON, key=int) == [str(i) for i in range(2, 13)] and len(YR) >= 9
OW = [[[v[g] for g in 'porm'] for v in OMENW[st].values()] for st in '123']
J = lambda o: json.dumps(o, ensure_ascii=False)
data = ('  const KG_SV=%s;\n  const KG_WHEN=%s, KG_ALLYV=%s;\n' % (J(SV), J(WHEN), J(ALLYV))
        + '  const KG_DAY=%s, KG_DAYL=%s, KG_MON=%s, KG_YR=%s, KG_OMEN=%s, KG_OMENW=%s;\n' % (J(DAY), J(DAYL), J(MON), J(YR), J(OMEN), J(OW))
        + '  const KG_EV=[\n' + ',\n'.join(EV) + '\n  ];\n  const KG_AF=[\n' + ',\n'.join(AFX) + '\n  ];\n'
        + "  const kgTag=t=>((HLK[S.hero]||{})[t]||0)>0;\n")
eng = open(os.path.join(D0, 'kg.js'), encoding='utf-8').read().replace('  /*KG_DATA*/\n', data)
eng = eng.replace('for(const l of x.b) log(l', 'for(const l of x.b()) log(l').replace('${head} · ${x.t}`', '${head} · ${x.t()}`')

if DUMP:
    with open(DUMP, 'w', encoding='utf-8') as f:
        for i, t in KO.items(): f.write('%s|%s\n' % (i, t))
    print('글', len(KO), '→', DUMP)

# ---------- 붙이기 ----------
rp("  function battleRound(){", eng + "  function battleRound(){")
rp("    decide({title:'성배',body:`${shared?", "    kgOffer(ch_,shared);   // 11-21: 진짜 소원\n    decide({title:'성배',body:`${shared?")
rp("if(!b.talked&&!e.cx) choices.push({grp:'special',t:'말을 건다'", "if(!b.talked&&!e.cx&&!b.ctx.kgAlly) choices.push({grp:'special',t:'말을 건다'")
rp("    if(ctx.defend) p+=5*wsF()*fortRead(ctx.e)*(ctx.breach?.5:1); if(ctx.trap) p-=8;\n",
   "    if(ctx.defend) p+=5*wsF()*fortRead(ctx.e)*(ctx.breach?.5:1); if(ctx.trap) p-=8;\n    if(w.battle&&w.battle.ctx&&w.battle.ctx.kgAlly) p+=kgAllyMod();   // 11-21: 잔을 쥔 쪽 · 령주에 묶인 몸\n")
# 결투: 첫마디 · 첫 줄
rp("    log(`잔이 가득 찼다. ${n}${J(n,이)} 당신과 마주 섰다.`,'war');\n    log(`${n}: “그 소원만큼은 내가 막겠다.”`,'voice');\n",
   "    if(ctx.intro!=='') log(ctx.intro||`잔이 가득 찼다. ${n}${J(n,이)} 당신과 마주 섰다.`,'war');\n    if(ctx.first!==null) log(ctx.first?voiceLine(h,ctx.first):`${n}: “그 소원만큼은 내가 막겠다.”`,'voice');\n")
# 에필로그
rp("    if(!E.ph){ const lk=E.i===1&&loneKind(); if(E.i===1&&stayHome()&&relOf()) ep2Start(); else if(lk) ep3Start(lk); else return false; }\n    if(E.ph==='D') return false;\n",
   "    if(!E.ph){ const lk=E.i===1&&loneKind(); if(E.i===1&&S.flags.kgB&&!S.flags.kgGone) kgEpStart(); else if(E.i===1&&stayHome()&&relOf()) ep2Start(); else if(lk) ep3Start(lk); else return false; }\n    if(E.ph==='D') return false;\n    if(E.kg) return kgEpStep();   // 11-21: 묶인 잔\n")
rp("  function ep2Pick(){ const E=S.epi, r=relOf(), ph=E.ph; if(S.pending) return true;\n",
   "  function ep2Pick(){ const E=S.epi, r=relOf(), ph=E.ph; if(S.pending) return true;\n    if(kgMix()) return true;   // 11-21: 돌아선 삶\n")
rp("  function ep3Pick(){ if(S.pending||S.dead) return; const E=S.epi;\n",
   "  function ep3Pick(){ if(S.pending||S.dead) return; const E=S.epi;\n    if(kgMix()) return;   // 11-21: 돌아선 삶 · 손을 놓친 잔\n")
rp("    if(id.startsWith('@lone')){", "    if(id.startsWith('@kg')){ kgResume(id.slice(3)); return; }\n    if(id.startsWith('@lone')){")
rp("const EPI_POOL=[\n", "const EPI_POOL=[\n" + ''.join(POOLX))
# 세상을 떠나는 자리: 묶인 잔 · 돌아선 삶의 마지막 해
rp("    if(ch(Math.min(.6,q)) || S.st.health<=0 || S.age>=104){ if(stayHome()) lastNight(); else relMeet(); die(causeFor()); }",
   "    if(ch(Math.min(.6,q)) || S.st.health<=0 || S.age>=104){ if(kgDeath(()=>{ if(stayHome()) lastNight(); else relMeet(); die(causeFor()); })) return; if(stayHome()) lastNight(); else relMeet(); die(causeFor()); }")
rp("    if(dead){ if(stayHome()) lastNight(); else relMeet(); die(causeFor()); return; }",
   "    if(dead){ if(kgDeath(()=>{ if(stayHome()) lastNight(); else relMeet(); die(causeFor()); })) return; if(stayHome()) lastNight(); else relMeet(); die(causeFor()); return; }")
rp("      if(ch(Math.min(.6,q))||S.age>=104){\n        if(stayHome()) lastNight();",
   "      if(ch(Math.min(.6,q))||S.age>=104){\n        if(kgDeath(()=>decide({title:'다시 산다면',body:QUESTIONS[70].replace('일흔. ',''),input:'note',silent:true,choices:[{t:'남기고 보내 주기',auto:true,f:()=>die(causeFor())}]}))) return;\n        if(stayHome()) lastNight();")
rp("    if(!S.dead){ if(stayHome()) lastNight(); else relMeet(); die(causeFor()); }\n  }",
   "    if(!S.dead){ if(kgDeath(()=>{ if(stayHome()) lastNight(); else relMeet(); die(causeFor()); })) return; if(stayHome()) lastNight(); else relMeet(); die(causeFor()); }\n  }")
# 복선: 삶 파트(해마다) · 전쟁(밤)
rp("  function advanceYear(){\n    S.age++; S.year++;\n", "  function advanceYear(){\n    S.age++; S.year++;\n    kgOmenLife();   // 11-21: 검귀 루트 복선\n")
rp("    log(`제${w.day}일 · 밤`,'night');\n", "    log(`제${w.day}일 · 밤`,'night'); kgOmenWar();\n")
# 결말 연출
rp("const END_N={wish:'wish',", "const END_N={kgM:'kgM',kgT:'kgT',kgB:'kgB',kgP:'kgP',kgP2:'kgP2',kgX:'kgX',kgS:'kgS',kgF:'kgF',wish:'wish',")
rp("({lost:'c',dead:'c',survived:'b',withdrew:'b',refused:'e'})[k]", "({lost:'c',dead:'c',kgS:'c',kgF:'c',kgX:'c',survived:'b',withdrew:'b',refused:'e'})[k]")
SCN = r"""  // 11-21: 검귀 루트 결말 — 있는 장면을 빌려 문구만 바꾼다
  const scnAs=(base,hold,txt)=>({HOLD:hold,get low(){ return SCN[base].low; },init(){ SCN[base].init.call(this); txt.call(this); },frame(t,dt){ return SCN[base].frame.call(this,t,dt); }});
  SCN.kgM=scnAs('wish',7.0,function(){ setText('검을 거두지 않은 자','잔이 당신의 소원을 받아 들었다.','막아선 서번트는 새벽이 오기 전에 흩어졌다.'); });
  SCN.kgT=scnAs('wish',7.0,function(){ setText('둘이 이긴 세계','둘이 이긴 세계의 첫 아침이 왔다.','그 세계는 아주 조용했다.'); });
  SCN.kgB=scnAs('heroWish',7.0,function(){ setWish(opt.wish); setText('묶인 잔','소원은 이루어졌다.',`${opt.hero}${jo(opt.hero,'은','는')} 곁에 남았다. 그 뒤로 입을 열지 않았다.`); });
  SCN.kgP=scnAs('break',7.4,function(){ setText('잔을 내려놓은 손','본성 속 진심을 잔에 맡기지 않았다.','잔은 둘의 손으로 부서졌다.'); });
  SCN.kgP2=scnAs('stay',7.6,function(){ setText('잔을 내려놓은 손','본성 속 진심을 잔에 맡기지 않았다.',`${opt.hero}${jo(opt.hero,'이','가')} 이 세계에 남았다.`); });
  SCN.kgX=scnAs('lost',6.4,function(){ setText('손을 놓친 잔','동맹이 잔을 부쉈다.',`${opt.hero}${jo(opt.hero,'을','를')} 잃었다. 당신은 살아남았다.`); });
  SCN.kgS=scnAs('dead',7.0,function(){ setText('막아선 칼','서번트가 당신을 멈췄다.','잔은 새벽 속에서 부서졌다.'); });
  SCN.kgF=scnAs('dead',7.0,function(){ setText('등 뒤의 칼','함께 가는 척했던 서번트가 잔을 부쉈다.','당신의 시점은 거기서 끊겼다.'); });
"""
rp("  SCN.dead={HOLD:", SCN + "  SCN.dead={HOLD:")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

# ---------- 번역 ----------
def rd(fn, keyed):
    out = {}
    pth = os.path.join(KD, fn)
    if not os.path.exists(pth): return out
    for ln in open(pth, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if not ln.strip() or ln.startswith('#'): continue
        tpl = ln.startswith('T ')
        if tpl: ln = ln[2:]
        p = [y.strip() for y in ln.split('|')]
        if len(p) != 4 or not all(p): raise SystemExit('칸이 4개가 아님 (%s): %s' % (fn, ln[:70]))
        out[p[0]] = (tuple(p[1:]), tpl)
    return out
TID = {}
import glob
for fp in sorted(glob.glob(os.path.join(KD, 'tr_*.txt'))): TID.update(rd(os.path.basename(fp), False))
TRE = rd('tre.txt', True)
dict_items, tpl_items, zh = [], [], []
lost = []
for i, ko in KO.items():
    if i in TID: (en, ja, zs), _ = TID[i]; dict_items.append((ko, en, ja)); zh.append((ko, zs))
    else: lost.append(i)
for ko, (en, ja, zs) in TRL.items(): dict_items.append((ko, en, ja)); zh.append((ko, zs))
for ko, ((en, ja, zs), tpl) in TRE.items():
    (tpl_items if tpl else dict_items).append((ko, en, ja)); zh.append((ko, zs))
if lost:
    print('번역 없음', len(lost), '· 예', lost[:5])
    if not LOOSE: raise SystemExit(1)
s, nd, nt = i18n.add(s, dict_items, tpl_items)
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(D0, 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, d in zh:
    if a not in Z:
        e = zht(d)
        if e is None: raise SystemExit('OpenCC 없음')
        Z[a] = [d, e]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 사건', len(EV), '+', len(POOLX), '· 후일담', len(AFX), '· 서번트', len(SV), '· 글', len(KO), '· 사전', nd, '틀', nt, '· 중국어', n)
