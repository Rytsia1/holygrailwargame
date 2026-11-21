"""11-21: 결과 화면 「기록 복사」 문구가 언어 설정을 따르지 않고 늘 한국어로 복사되던 문제 (커뮤니티 제보 11-20, X 일본어)
- 예전: 복사 문구를 한국어 틀에 값을 그대로 끼워 만들어, 화면은 일본어여도 클립보드에는 한국어가 들어갔다
- 이제 shareText(r): 한국어는 예전 문구 그대로, 다른 언어는 언어별 틀에 값을 하나씩 tr()로 옮겨 넣는다
사용: python3 share_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'function shareText(' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

OLD = "$('#copyBtn').onclick=()=>{ const t=`성배가 차는 밤 — ${r.name} (${r.born}–${r.died}, ${r.age}세)\\n${r.origin}\\n${r.warYear}년 겨울: ${r.hero?r.hero.cls+' '+wa(r.hero.name)+' 함께, ':''}${warTxt(r)}${r.wish?' · '+r.wish:''}${r.wd&&r.wd.bt?`\\n전적: 교전 ${r.wd.bt.n} · 격파 ${r.wd.kills} · 령주 ${r.wd.seals.length}획`:''}\\n떠난 이유: ${r.cause}${r.last?'\\n'+(r.lastTo?r.lastTo+'에게: ':'')+'“'+r.last+'”':''}`;"
rp(OLD, "$('#copyBtn').onclick=()=>{ const t=shareText(r);")

rp("function showEnding(r,fromHistory){\n",
r"""// 「기록 복사」 문구: 화면 언어를 따른다 (11-21)
function shareText(r){
  const bt=r.wd&&r.wd.bt;
  if(LANG==='ko') return `성배가 차는 밤 — ${r.name} (${r.born}–${r.died}, ${r.age}세)\n${r.origin}\n${r.warYear}년 겨울: ${r.hero?r.hero.cls+' '+wa(r.hero.name)+' 함께, ':''}${warTxt(r)}${r.wish?' · '+r.wish:''}${bt?`\n전적: 교전 ${bt.n} · 격파 ${r.wd.kills} · 령주 ${r.wd.seals.length}획`:''}\n떠난 이유: ${r.cause}${r.last?'\n'+(r.lastTo?r.lastTo+'에게: ':'')+'“'+r.last+'”':''}`;
  const T=x=>x==null?'':tr(String(x)), cj=LANG!=='en', C=cj?'：':': ';
  const wt0=T(warTxt(r)), wt=LANG==='en'&&r.hero&&/^[A-Z][a-z]/.test(wt0)?wt0[0].toLowerCase()+wt0.slice(1):wt0;
  const nm=T(r.name), hn=r.hero?T(r.hero.name):'', hc=r.hero?T(r.hero.cls):'';
  const head=LANG==='en'?`${nm} (${r.born}–${r.died}, age ${r.age})`:LANG==='ja'?`${nm}（${r.born}–${r.died}、${r.age}歳）`:`${nm}（${r.born}–${r.died}，${r.age}${LANG==='zhs'?'岁':'歲'}）`;
  const withH=!r.hero?'':LANG==='en'?`with ${hc} ${hn}, `:LANG==='ja'?`${hc} ${hn}と共に、`:`${LANG==='zhs'?'与':'與'}${hc}${hn}一起，`;
  const q=x=>LANG==='ja'||LANG==='zht'?'「'+x.replace(/。$/,LANG==='ja'?'':'。')+'」':'“'+x+'”';
  const to=!r.lastTo?'':LANG==='en'?`To ${T(r.lastTo)}: `:LANG==='ja'?`${T(r.lastTo)}へ：`:`致${T(r.lastTo)}：`;
  return `${T('성배가 차는 밤')} — ${head}\n${T(r.origin)}\n${T(r.warYear+'년 겨울')}${C}${withH}${wt}${r.wish?' · '+T(r.wish):''}${bt?`\n${T('전적')}${C}${T('교전')} ${bt.n} · ${T('격파')} ${r.wd.kills} · ${T('령주 '+r.wd.seals.length+'획')}`:''}\n${T('떠난 이유')}${C}${T(r.cause)}${r.last?'\n'+to+q(T(r.last)):''}`;
}
function showEnding(r,fromHistory){
""")

if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
