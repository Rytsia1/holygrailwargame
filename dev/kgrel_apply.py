"""11-22: 검귀 결말과 인연
- 모순 고침: ②(둘이 이긴 세계) · ③(묶인 잔, 서번트가 곁에 있음)은 「함께 사는 생」 표시가 없어 서번트가 떠난 것으로 쳤다
  → 「꿈에서」 · 「다른 겨울의 소식」 · 「소환의 촉매」(떠난 판) · 「꿈속의 재회」 같은 떠난 뒤 사건이 곁에 서번트가 있는데 나왔다.
  gone()이 ② · ③(곁)에서는 거짓이 되게 한다. ①(벰) · ⑥ · ③(놓아줌)은 그대로.
- ②에서 인연이 자란다: 인연 단계 장면 · 애정/우정 사건 · 애정 전환 · 해마다 인연 · 신뢰가 조금씩 오름.
  사건은 세계마다 맞는 것만(KG_REL_OK). 결혼 · 아이(서류가 필요) · 노환 연작(relLate) · 서번트가 먼저 가는 길은 열지 않는다.
  ③(묶인 잔)은 서번트가 말이 없어 닫아 둔다.
사용: python3 kgrel_apply.py <game.html>"""
import sys, json, re
P = sys.argv[1]
s = open(P, encoding='utf-8').read(); miss = []
def rp(o, n, cnt=1):
    global s
    if s.count(o) != cnt: miss.append((o[:70], s.count(o))); return
    s = s.replace(o, n)
# 세계(성향)마다 ②에서 열어 둘 인연 사건 — 세계 규칙과 부딪치는 문장이 있는 것은 뺀다
#   복수: 아무도 다가오지 않는다(이웃 반찬 · 가족 손님) · 정의 · 금기: 대부분 · 잔혹: 약한 것(앓는 사람 · 병원 · 아기)이 없다 · 근원 집착: 도시가 잠들었다(가게 · 버스 · 병원 · 이웃)
ALL = ['sw_grow', 'sw_spring', 'lv_anniv', 'lv_night', 'fr_drink', 'fr_oath']
OK = {
 'avenger': ALL + ['lv_morning', 'fr_field', 'fr_job', 'fr_crisis', 'st_sick', 'st_ask'],
 'judge':   ALL + ['lv_morning', 'fr_field', 'fr_job', 'fr_family', 'fr_god', 'fr_crisis', 'st_sick', 'st_quarrel', 'st_ask'],
 'cruel':   ALL + ['lv_morning', 'fr_job', 'fr_family', 'st_quarrel', 'st_ask'],
 'taboo':   ALL + ['lv_morning', 'fr_field', 'fr_job', 'fr_family', 'fr_god', 'fr_crisis', 'st_sick', 'st_quarrel', 'st_ask'],
 'zeal':    ALL + ['st_sick'],
}
# 1. gone
rp("const gone=()=>!!S.hero&&!S.flags.stay;",
   "const KG_REL_OK=" + json.dumps(OK) + ";   // 11-22 ②에서 여는 인연 사건 (kgrel_apply)\n"
   "  const kgSide=()=>{ const c=kgCtx(); return c==='t'||c==='b'; };   // 검귀 ② · ③: 서번트가 곁에 있다\n"
   "  const relHome=id=>stayHome()||(kgCtx()==='t'&&(!id||(KG_REL_OK[S.flags.kg]||[]).includes(id)));   // 인연이 자랄 수 있는 「곁」\n"
   "  const gone=()=>!!S.hero&&!S.flags.stay&&!kgSide();")
# 2. 인연이 자라는 때
rp("return S.phase==='war'?!!w.heroAlive:stayHome(); };", "return S.phase==='war'?!!w.heroAlive:relHome(); };")
# 3. 애정 전환
rp("function relSwOk(r,why){ if(!stayHome()||", "function relSwOk(r,why){ if(!relHome(why==='minor'?'sw_grow':'sw_spring')||")
# 4. 인연 사건 조건
a = s.find('  const EP_REL=['); b = s.find('\n  ];', a)
if a < 0 or b < 0: miss.append(('EP_REL', 0))
else:
    blk = s[a:b]; n0 = 0
    def f(m):
        global n0
        n0 += 1; return m.group(1) + "relHome('%s')" % m.group(2)
    blk2 = re.sub(r"(\{id:'((?:lv_morning|lv_anniv|lv_night|fr_[a-z]+|st_[a-z]+))',w:[0-9.]+,c:\(?r?\)?=>)stayHome\(\)", f, blk)
    if n0 != 13: miss.append(('EP_REL 조건 13개', n0))
    s = s[:a] + blk2 + s[b:]
# 5. 해마다
rp("if(stayHome()){ relGain(STAY_YG); stayTrust(); relTick(); if(S.age>=OLDC()[1]&&ch(OLDC()[2])) stayFirstLog(); }",
   "if(stayHome()){ relGain(STAY_YG); stayTrust(); relTick(); if(S.age>=OLDC()[1]&&ch(OLDC()[2])) stayFirstLog(); } else if(kgCtx()==='t'){ relGain(STAY_YG); stayTrust(); relTick(); }", 2)
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
print('kgrel 적용')
