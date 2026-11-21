"""11-20: 성향을 화면에 보여 준다
- 나의 서번트 칸: 서번트 성향 · 속성 칩, 지금 궁합과 소환할 때의 궁합
- 서번트 정보 창(나의 서번트를 눌렀을 때): 성향 · 속성 · 궁합 줄
- 상태 칸: 나의 성향(복수 · 정의 · 잔혹 · 금기 · 근원 집착). 숫자는 숨기고 옅음 · 짙음 · 깊음.
  칩을 누르면(마우스를 올리면) 어떤 서번트와 멀어지고 가까워지는지 보여 준다
사용: python3 affview_apply.py <game.html>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'function heroAffRows(' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

# 상태 칸 자리
rp('<div class="prof" id="prof"></div><div id="stats"></div></div>',
   '<div class="prof" id="prof"></div><div id="stats"></div><div id="affs"></div></div>')
# 나의 성향 그리기
rp("""  $('#stats').innerHTML=Object.entries(ST_LABEL).map(([k,l])=>bar(l,S.st[k],k)).join('')+bar('재산',S.wealth||0,'wealth');""",
   """  $('#stats').innerHTML=Object.entries(ST_LABEL).map(([k,l])=>bar(l,S.st[k],k)).join('')+bar('재산',S.wealth||0,'wealth');
  affRender(S);""")
# 나의 서번트 칸
rp("""<div class="htitle">${h.title} · ${h.from}</div></div></div>
      ${paramGrid(h.s,Sim.myParams().p)}""",
   """<div class="htitle">${h.title} · ${h.from}</div></div></div>
      ${heroAffRows(h,w)}
      ${paramGrid(h.s,Sim.myParams().p)}""")
# 서번트 정보 창
rp("""<dl class="row"><dt>소원</dt><dd>${esc(h.wish)}</dd><dt>신뢰</dt><dd>${Math.round(w.trust)}</dd></dl>""",
   """<dl class="row"><dt>소원</dt><dd>${esc(h.wish)}</dd><dt>신뢰</dt><dd>${Math.round(w.trust)}</dd><dt>성향</dt><dd>${h.traits.map(t=>'「'+esc(t)+'」').join(' ')}</dd>${Sim.alName(h.id)?`<dt>속성</dt><dd>${esc(Sim.alName(h.id))}</dd>`:''}<dt>궁합</dt><dd>${fitWord(w.fit)}</dd></dl>""")
# 함수들: showInfo 앞에 둔다
rp("function showInfo(key){\n",
   r"""// 11-20: 성향 보기 — 서번트의 성향 · 속성 · 궁합, 나의 성향(숫자는 숨기고 옅음 · 짙음 · 깊음)
const fitWord=f=>(f??60)>=70?'잘 맞음':(f??60)<50?'어긋남':'보통';
function heroAffRows(h,w){ const al=Sim.alName(h.id);
  return `<div class="af-box"><div class="af-row"><span class="af-lb">성향</span>${h.traits.map(t=>`<span class="af-c">${esc(t)}</span>`).join('')}${al?`<span class="af-lb af-lb2">속성</span><span class="af-c">${esc(al)}</span>`:''}</div>
    <div class="af-row"><span class="af-lb">궁합</span><b class="af-ft">${fitWord(w.fit)}</b><span class="af-sub">·</span><span class="af-sub">소환할 때</span><span class="af-sub">${fitWord(w.fit0??w.fit)}</span></div></div>`; }
const AF_K=['avenger','judge','cruel','taboo','zeal'], AF_N={avenger:'복수',judge:'정의',cruel:'잔혹',taboo:'금기',zeal:'근원 집착'}, AF_TH={avenger:4,judge:4,cruel:4,taboo:4,zeal:4};   // 11-22: 칩의 옅음 · 짙음 글은 다섯 성향 모두 4부터(궁합 계산 기준 FIT_TH · fitScore는 그대로 정의 · 복수 3)
const AF_TIP={
  avenger:['복수 · 아직 옅습니다. 짙어지면 「연민」을 중시하는 서번트와 멀어지고, 「자유」·「야망」을 따르는 서번트와 가까워집니다. 쌓일수록 어벤저가 응답하기 쉬워집니다.','복수 · 「연민」을 중시하는 서번트와 멀어지고, 「자유」·「야망」을 따르는 서번트와 가까워집니다. 어벤저가 응답하기 쉬워집니다.'],
  judge:['정의 · 아직 옅습니다. 짙어지면 「명예」·「연민」을 중시하는 서번트와 가까워집니다. 쌓일수록 룰러가 응답하기 쉬워집니다.','정의 · 「명예」·「연민」을 중시하는 서번트와 가까워집니다. 룰러가 응답하기 쉬워집니다.'],
  cruel:['잔혹 · 아직 옅습니다. 짙어지면 「연민」·「명예」를 중시하는 서번트와 멀어지고, 「야망」을 따르는 서번트와 가까워집니다.','잔혹 · 「연민」·「명예」를 중시하는 서번트와 멀어지고, 「야망」을 따르는 서번트와 가까워집니다.'],
  taboo:['금기 · 아직 옅습니다. 짙어지면 「명예」·「충성」을 중시하는 서번트와 멀어지고, 「자유」·「야망」을 따르는 서번트와 가까워집니다.','금기 · 「명예」·「충성」을 중시하는 서번트와 멀어지고, 「자유」·「야망」을 따르는 서번트와 가까워집니다.'],
  zeal:['근원 집착 · 아직 옅습니다. 짙어지면 「연민」을 중시하는 서번트와 멀어지고, 「야망」을 따르는 서번트와 가까워집니다.','근원 집착 · 「연민」을 중시하는 서번트와 멀어지고, 「야망」을 따르는 서번트와 가까워집니다.']};
const AF_HINT='짙은 성향은 소환되는 서번트와 궁합, 갈림길의 선택지를 바꿉니다. 칩을 누르면 자세히 볼 수 있습니다.';
let afSel=null;
function affRender(S){ const el=$('#affs'); if(!el) return; const A=S.aff||{}, ks=AF_K.filter(k=>(A[k]||0)>0);
  if(!ks.length){ el.innerHTML=''; afSel=null; return; } if(afSel&&!ks.includes(afSel)) afSel=null;
  const tip=k=>AF_TIP[k][(A[k]||0)>=AF_TH[k]?1:0];
  el.innerHTML=`<div class="af-box"><div class="af-row"><span class="af-lb">성향</span>${ks.map(k=>{ const v=A[k], on=v>=AF_TH[k], lv=v>=8?'깊음':on?'짙음':'옅음';
      return `<button type="button" class="af-c af-b${on?' on':''}${afSel===k?' sel':''}" data-k="${k}" title="${esc(tr(tip(k)))}"><span>${AF_N[k]}</span><i>${lv}</i></button>`; }).join('')}</div>
    <p class="af-h">${esc(afSel?tip(afSel):AF_HINT)}</p></div>`;
  el.querySelectorAll('.af-b').forEach(b=>b.onclick=()=>{ afSel=afSel===b.dataset.k?null:b.dataset.k; affRender(Sim.S); }); }
function showInfo(key){
""")
# 모양
rp("</style>",
   """.af-box{margin:10px 0 12px}.af-row{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;margin:0 0 7px;font-size:12.5px}
.af-lb{color:var(--dim);min-width:34px}.af-lb2{margin-left:6px;min-width:0}
.af-c{display:inline-flex;gap:5px;align-items:center;padding:2px 9px;border:1px solid rgba(196,164,104,.35);border-radius:4px;font-size:12px;color:#cfc6b0;background:none;font-family:inherit;line-height:1.5}
.af-c i{font-style:normal;font-size:11px;color:#a39c8a}.af-b{cursor:pointer}.af-b:hover{border-color:rgba(226,196,138,.6)}
.af-c.on{border-color:rgba(226,196,138,.7);color:#f0dcae}.af-c.on i{color:#e2c48a}.af-c.sel{background:rgba(226,196,138,.12)}
.af-ft{color:var(--gold2,#e2c48a);font-weight:500}.af-sub{color:#8f8878;font-size:11.5px}
.af-h{font-size:11.5px;color:#8f8878;margin:2px 0 0;line-height:1.55}
</style>""")

if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

from affview_lines import D
s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, *_ in D], [])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _b, _c, d, e in D:
    if a not in Z: Z[a] = [d, e]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 사전', nd, '· 중국어', n)
