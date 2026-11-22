"""11-22: 검귀 루트와 공용 에필로그가 어긋나지 않게
- 「끝까지 남은 사람」(survivor)의 「성배는 다른 이에게 갔다」 · 「마지막 밤을 며칠 앞두고 쓰러졌다」는 검귀 결말과 맞지 않는다
  (⑤ 둘이 잔을 부숨 · 금이 감, ⑥ 마지막 밤 동맹 결전에서 쓰러짐, ③ 잔이 소원을 들어줌) → 검귀 결말이면 빼고, 결말마다의 검귀 사건이 그 자리를 맡는다
- 본성 속 진심이 이루어진 결말(③ 묶인 잔 · ① 서번트를 벰 · ② 둘이 이긴 세계)에서 공용 에필로그로 넘어가면,
  이루어진 소원과 부딪치는 성향 사건을 뺀다(KG_WISH_NO)
사용: python3 kgepi_apply.py <game.html>"""
import sys, json
P = sys.argv[1]
s = open(P, encoding='utf-8').read(); miss = []
def rp(o, n):
    global s
    if s.count(o) != 1: miss.append((o[:70], s.count(o))); return
    s = s.replace(o, n)
# 이루어진 진심과 부딪치는 사건 (진심 글귀: 복수 「나를 짓밟은 모든 것에 갚는다」 · 정의 「누구도 거역할 수 없는 정의」 · 잔혹 「약한 것이 없는 세상」 · 금기 「문 너머를 이쪽으로 연다」 · 근원 집착 「이 도시 전부를 근원에 닿는 디딤돌로 쓴다」)
NO = {
 'avenger': ['af_av09', 'af_av10'],                                   # 아직 남은 장부 · 마지막 원수
 'judge': ['af_jd01', 'af_jd02', 'af_jd05', 'af_jd06', 'af_jd08', 'af_jd09', 'judge_eye'],   # 비리 · 부당 해고 · 비리 후보 · 잘못된 판결 · 누명 — 거역할 수 없는 정의의 세계
 'cruel': ['af_cr01', 'af_cr03', 'af_cr07'],                                     # 무너진 사람 · 돌봐 달라는 늙은 어른 — 약한 것이 없는 세상
 'taboo': [],
 'zeal': ['af_zl01', 'af_zl02', 'af_zl04', 'af_zl05', 'af_zl06', 'af_zl08', 'af_zl09', 'root_step'],    # 근원 앞에서 멈춘 연구 · 비웃음 · 몰래 측량 · 앞선 집안 · 모자란 시간 · 근원의 문턱
}
rp("const epiBlock=id=>(/^cx_/.test(id)&&",
   "const KG_WISH_NO=" + json.dumps(NO) + ";   // 11-22: 진심이 이루어진 검귀 결말에서 빼는 공용 사건 (kgepi_apply)\n"
   "  const kgWishDone=()=>['b','t','m'].includes(S.flags.kgEnd);\n"
   "  const epiBlock=id=>(id==='survivor'&&!!S.flags.kgEnd)||(kgWishDone()&&(KG_WISH_NO[S.flags.kg]||[]).includes(id))||(/^cx_/.test(id)&&")
# 11-22: 진심이 이루어진 세계(①·②·③)에서 그 세계의 규칙과 부딪치는 공용 사건 빼기(kgWorldNo, kg.js) ·
#        무거운 사건 다음 차례는 가볍거나 보통인 사건 ×2 · ⑥은 사건 13~15개를 1~3년 간격으로 · 근원 집착 세계에는 「다시 차오르는 성배」 뉴스가 없다(도시가 잠듦)
rp("(kgWishDone()&&(KG_WISH_NO[S.flags.kg]||[]).includes(id))||", "(kgWishDone()&&(KG_WISH_NO[S.flags.kg]||[]).includes(id))||kgWorldNo(id)||")
rp("const E=S.epi; E.used=E.used||[]; E.n=E.n||ri(8,10);", "const E=S.epi; E.used=E.used||[]; E.n=E.n||(S.flags.kg6?ri(13,15):ri(8,10));")
rp("if(c.length){ sc=wpick(c,x=>x.w||1); E.used.push(sc.id); if(sc.arc) E.arcN=(E.arcN||0)+1; sc={yrs:()=>ri(1,4),f:sc.f,rid:'@pool'+sc.id}; }",
   "if(c.length){ sc=wpick(c,x=>(x.w||1)*kgPace(x)); kgPaced(sc); E.used.push(sc.id); if(sc.arc) E.arcN=(E.arcN||0)+1; sc={yrs:()=>ri(1,S.flags.kg6||E.kw?3:4),f:sc.f,rid:'@pool'+sc.id}; }")
rp("const EPI_END={yrs:()=>Math.max(1,S.warYear+58-S.year),c:()=>{const d=S.warYear+58-S.year;return d>0&&d<45&&S.age+d<100},",
   "const EPI_END={yrs:()=>Math.max(1,S.warYear+58-S.year),c:()=>{const d=S.warYear+58-S.year;return d>0&&d<45&&S.age+d<100&&!(kgCtx()&&S.flags.kg==='zeal')},")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
print('kgepi 적용')
