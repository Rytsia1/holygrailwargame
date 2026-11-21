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

rp("  ];\n  const FOCUS_PICK=", G + "  ];\n  // 11-22: 성향 사건의 나이 폭을 정의 사건과 비슷하게(평균 약 16년) 넓힌다 — 복수 · 잔혹 · 금기 · 근원 집착\n  { const AGE_FIX={'c_bully':[6,14],'betrayed':[16,45],'l2_07':[12,22],'l2_08':[13,28],'l2_09':[12,35],'l2_10':[18,50],'l2_11':[22,55],'l2_13':[13,30],'l2_14':[18,55],'l2_15':[10,30],'l2_04':[5,12],'l2_05':[7,15],'l2_06':[6,15],'l2_12':[6,15],'d_ant':[4,10],'d_vase':[5,12],'d_bully':[8,15],'d_bird':[5,13],'d_secret':[11,15],'l2_18':[12,19],'l2_19':[11,18],'l2_20':[16,45],'l2_21':[25,55],'l2_22':[9,25],'l2_23':[10,18],'l2_24':[16,60],'l2_25':[20,60],'l2_26':[10,25],'l2_16':[6,15],'l2_17':[8,15],'c_book':[7,15],'l2_39':[12,22],'l2_40':[13,35],'l2_41':[15,55],'l2_43':[20,55],'l2_44':[16,55],'l2_45':[10,30],'l2_46':[16,45],'t_door':[4,12],'t_grave':[8,15],'t_mirror':[8,15],'t_blood':[10,15],'t_museum':[8,15],'l2_38':[6,14],'l2_42':[8,15],'l2_29':[12,25],'l2_30':[14,40],'l2_31':[18,50],'l2_32':[24,55],'l2_33':[12,24],'l2_34':[14,35],'l2_36':[18,55],'l2_37':[12,30],'z_party':[7,15],'z_plant':[8,15],'z_sick':[7,15],'z_root':[10,15],'z_memory':[9,15],'l2_27':[5,13],'l2_28':[8,15],'l2_35':[7,15]}; [...EV,...GROW].forEach(e=>{ const f=AGE_FIX[e.id]; if(f) e.a=f; }); }\n  const FOCUS_PICK=")
# 11-22: 이미 기운 성향의 사건이 더 자주 — 선택지에서 그 성향을 올리는 사건은 성향 점수에 따라 ×1.4~×2.4
rp("  function wpick(arr,wf){", """  function evLk(e){ if(e._lk) return e._lk; const k={}; (e.ch||[]).forEach(c=>{ const m=String(c.f).match(/lean\\('(\\w+)',\\s*\\d/g)||[]; m.forEach(x=>{ k[x.slice(6,x.indexOf("'",6))]=1; }); }); return e._lk=Object.keys(k); }
  function evW(e){ const A=S.aff||{}; let v=0; evLk(e).forEach(k=>{ v=Math.max(v,A[k]||0); }); return e.w*(v<=0?1:v<3?1.4:v<6?1.9:2.4); }
  function wpick(arr,wf){""")
rp("wpick(elig,x=>x.w); if(!e) return;\n    S.once[e.id]=1; (S.onceAt", "wpick(elig,evW); if(!e) return;\n    S.once[e.id]=1; (S.onceAt")
rp("const e=wpick(elig,x=>x.w); S.once[e.id]=1; mark('event');\n    showGrow(e);", "const e=wpick(elig,evW); S.once[e.id]=1; mark('event');\n    showGrow(e);")
rp("\n  ];\n  function relicRoom(){", "\n" + E.rstrip('\n') + "\n  ];\n  function relicRoom(){")
# 한 해 최대 2개
rp("    if(!S.pending&&!S.dead) artEvent();\n    if(!S.pending&&!S.dead) rollEvent();\n    if(!S.pending&&!S.dead&&S.age>=3&&S.age<=15&&ch(.8)) growthEvent();",
   """    if(!S.pending&&!S.dead) artEvent();
    const artY=!!S.pending;   // 11-20: 마안·기술 사건이 뜬 해는 그것 하나만
    if(!S.pending&&!S.dead) rollEvent();
    // 11-20: 삶 사건과 성장 사건은 따로 굴린다(한 해 최대 2개). 삶 사건이 떠 있으면 그 창을 닫은 뒤 같은 나이에 성장 사건
    if(!artY&&!S.dead&&S.age>=3&&S.age<=15&&ch(.8)){ if(!S.pending) growthEvent(); else { S.growNext=S.age; S.growWait=1.3; } }""")
rp("    if(S._resume){ const r=S._resume; S._resume=null; resumeAt(r); if(S.pending) return; }",
   "    if(S._resume){ const r=S._resume; S._resume=null; resumeAt(r); if(S.pending) return; }\n    if(S.phase==='life'&&S.growNext!=null){ if((S.growWait||0)>0){ S.growWait-=dt; return; }   // 11-22: 두 번째 사건은 잠깐 쉬었다가\n      const a=S.growNext; S.growNext=null; if(a===S.age&&!S.dead){ growthEvent(); H.change(); if(S.pending) return; } }")

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
