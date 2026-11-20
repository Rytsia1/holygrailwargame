"""11-20: 일본어 화면에 한국어가 남던 곳 (커뮤니티 제보 11-20)
① 이름 칸에서 한쪽(예: 이름)만 바꾸면 안 바꾼 쪽은 엔진 속 한국어 표기로 저장돼 '하 ユキ'처럼 섞였다
   → 이름이 들어간 문장(출생 기록 · 마스터 정보 · 에필로그 마지막 말)이 통째로 한국어로 남았다
   - 이제: 한쪽이라도 바꾸면 화면에 보이던 그대로(번역된 표기)를 저장한다(한국어 화면은 예전대로)
   - 이미 섞여 저장된 이름(기록 · 이어하기)도 옮길 수 있게, 한글 조각과 다른 글자 조각이 섞인 이름을 조각별로 옮긴다
② 「마스터가 지쳐 마력 공급이 흔들립니다」 번역 없음
③ 여러 문장이 붙은 기록을 문장 단위로 나눌 때, 따옴표 안이 두 문장이면(“이름. 대사.”) 앞 조각이 여는 따옴표만 삼켜 뒤 대사가 한국어로 남았다
   → 따옴표(“” 「」)가 짝이 맞지 않는 묶음은 한 덩이로 쓰지 않는다
④ 「밤사이 ○○에서 센티넬 ○○가 쓰러졌다고 한다」 문장 틀 없음
⑤ 선택지 설명에서 판정 부분을 떼어 낸 나머지(예: 「성공하면 넘칠 때를 안다」)가 사전에 따로 없으면 한국어로 남았다
   → 설명 전체의 번역이 있으면 그 번역을 같은 자리에서 잘라 쓴다
사용: python3 i18nfix20_apply.py <game.html>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n
from i18nfix20_lines import D as D2
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if '이름 칸 한쪽만 바꾸면' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)
# ①
rp("    if(a===disp(sug.sur)) a=sug.sur; if(b===disp(sug.given)) b=sug.given;",
   "    { const ka=a===disp(sug.sur), kb=b===disp(sug.given);   // 이름 칸 한쪽만 바꾸면 다른 쪽도 화면 표기 그대로 (한국어 표기와 섞이면 번역이 깨진다 · 11-20)\n"
   "      if((ka&&kb)||LANG==='ko'){ if(ka) a=sug.sur; if(kb) b=sug.given; } }")
rp("function _trName(t){\n  if(!/^[가-힣]+( [가-힣]+){0,3}$/.test(t)) return null;",
   "function _trName(t){\n  if(t.length<=40&&/[가-힣]/.test(t)&&/[^가-힣\\s]/.test(t)&&/^[가-힣\\u3040-\\u30ff\\u3400-\\u9fff\\uf900-\\ufaffA-Za-zÀ-ÿ'・·\\- ]+$/.test(t)){   // 한글 조각과 다른 글자 조각이 섞인 이름 (11-20)\n"
   "    const L=LANG==='ja'?1:LANG==='zhs'?3:LANG==='zht'?4:0, out=[];\n"
   "    for(const p of t.match(/[가-힣]+|[^가-힣\\s]+/g)){ if(!/[가-힣]/.test(p)){ out.push(p); continue; } if(!_NM[p]) return null; out.push(_NM[p][L]); }\n"
   "    const cjk=/^[\\u3040-\\u30ff\\u3400-\\u9fff\\uf900-\\ufaff]+$/; return out.join(L&&out.every(x=>cjk.test(x))?'':' '); }\n"
   "  if(!/^[가-힣]+( [가-힣]+){0,3}$/.test(t)) return null;")
# 아이 · 형제 이름: 성과 이름을 fullName으로 잇는다 (성이 한글이 아니면 띄어 쓴다)
rp("  function kidName(sex){ const L=NAMES[S.city.loc], F=S.fam||{}; const mk=g=>L.order==='sg'? S.sur+L.sp+g : g+L.sp+S.sur;",
   "  function kidName(sex){ const L=NAMES[S.city.loc], F=S.fam||{}; const mk=g=>fullName(S.sur,g);   // 성이 한글이 아니면(이름 칸에서 바꾼 경우) 띄어 써야 번역이 된다 (11-20)")
# ③
rp("      let seg=P[i]; for(let k=i;k<j;k++) seg+=S[k]+P[k+1];\n",
   "      let seg=P[i]; for(let k=i;k<j;k++) seg+=S[k]+P[k+1];\n"
   "      if(seg.split('“').length!==seg.split('”').length||seg.split('「').length!==seg.split('」').length) continue;   // 따옴표 짝이 안 맞는 묶음은 쓰지 않는다 (11-20)\n")
# ⑤
rp("  const segs=[]; d0.split(' · ').forEach(sg=>{ const P=sg.split(', '); if(P.length>1&&P.every(x=>STX.test(x.trim()))) segs.push(...P); else segs.push(sg); });",
   "  const segs=[], segW=[]; let splitOk=true; d0.split(' · ').forEach(sg=>{ const P=sg.split(', '); if(P.length>1&&P.every(x=>STX.test(x.trim()))){ segs.push(...P); splitOk=false; } else segs.push(sg); });\n"
   "  // 떼어 낸 나머지가 사전에 따로 없으면, 설명 전체의 번역을 같은 자리에서 잘라 쓴다 (11-20)\n"
   "  if(LANG!=='ko'&&splitOk&&segs.length>1){ const w=tr(d0), ws=w.split(' · '); if(!HANGUL.test(w)&&ws.length===segs.length) ws.forEach((x,i)=>segW[i]=x); }")
rp("  for(let sg of segs){ sg=sg.trim(); if(!sg) continue;\n    if(ck&&/^[가-힣]+(\\+[가-힣]+)* 판정$/.test(sg)){ ch=true; continue; }",
   "  for(let si=0;si<segs.length;si++){ let sg=segs[si].trim(); if(!sg) continue;\n    if(ck&&/^[가-힣]+(\\+[가-힣]+)* 판정$/.test(sg)){ ch=true; continue; }\n"
   "    if(segW[si]!=null&&HANGUL.test(tr(sg))&&!/[↑↓]/.test(sg)){ keep.push(segW[si].trim()); continue; }")
# ⑥ 령주로 끌어올린 능력치 표시 「근력 A+ ▲3」: ▲ 뒤를 떼고 옮긴다
rp("  for(const [re,m] of I18N_PAT){ const x=t.match(re);",
   "  { const am=t.match(/^(.+) ▲(\\d+)$/); if(am){ const q=_tr1(am[1]); if(!HANGUL.test(q)) return lead+q+' ▲'+am[2]+trail; } }   // 령주로 끌어올린 능력치 「근력 A+ ▲3」 (11-20)\n"
   "  for(const [re,m] of I18N_PAT){ const x=t.match(re);")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
D = [('마스터가 지쳐 마력 공급이 흔들립니다', 'Your Master is exhausted, and the mana supply wavers', 'マスターが疲れ、魔力供給が揺らいでいます',
      '御主疲惫，魔力供给不稳', '御主疲憊，魔力供給不穩')]
T = [('밤사이 {0}에서 {1~이} 쓰러졌다고 한다.', 'Word is that {1} fell at {0} during the night.', '夜のうちに{0}で{1}が倒れたらしい。',
      '据说夜里，{1}在{0}倒下了。', '據說夜裡，{1}在{0}倒下了。')]
D = D + D2   # ⑦ 선택지 · 기술 설명 조각 (i18nfix20_lines.py)
s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, *_ in D], [(a, b, c) for a, b, c, *_ in T])
# ⑧ 타마모 캣 대사 일본어 번역 속 한글 「ご주인」 → 「ご主人」
CK = '이 잔, 냄새가 고약하다. 상한 우유 같다. 캣은 이런 건 안 마신다. 주인도 마시지 마라.'
s, _n1, _n2 = i18n.add(s, [(CK, "This cup smells foul. Like spoiled milk. Cat won't drink this. Neither should you, Master.",
                            'この杯、くさい。腐った牛乳みたいだ。キャットはこんなの飲まない。ご主人も飲むな。')], overwrite=True)
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _b, _c, d, e in D + T:
    if a not in Z: Z[a] = [d, e]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 사전', nd, '· 틀', nt, '· 중국어', n)
