"""11-21: 마스터 대 서번트 결투 엔진 (상세안 6판 · 「claude/마스터 대 서번트 결투 상세안.md」)
- 엔진(duel.js)은 Sim 안, battleRound 앞에 넣는다. Sim.duelStart(ctx) · Sim.duelView()로 연다
- 화면(duel_ui.js)은 vsHtml 앞에 넣고, showDecision · renderChoices에 결투 갈래를 더한다
- 글은 duel_lines.txt (한국어|영어|일본어|간체). 번체는 간체를 OpenCC(s2tw)로 바꾸고 따옴표를 「」로
사용: python3 duel_apply.py <game.html>"""
import sys, os, re, json
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
import i18n
try:
    from opencc import OpenCC; CC = OpenCC('s2tw')   # pip install opencc-python-reimplemented
except ImportError: CC = None
P = sys.argv[1]; s = open(P, encoding='utf-8').read()
if 'function duelStart(' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

eng = open(os.path.join(D0, 'duel.js'), encoding='utf-8').read()
ui = open(os.path.join(D0, 'duel_ui.js'), encoding='utf-8').read()
rp("  function battleRound(){", eng + "  function battleRound(){")
rp("    _: {advanceYear, die} };", "    duelStart:c=>duelStart(c||{}), duelView:()=>S?duelView():null,\n    _: {advanceYear, die} };")
rp("function vsHtml(endE){", ui + "function vsHtml(endE){")
rp("  if(d.battle&&Sim.S.war&&(Sim.S.war.battle||d.endE)){ vs.innerHTML=vsHtml(d.endE); vs.classList.remove('hidden'); }",
   "  if(d.duel&&Sim.S.war&&Sim.S.war.duel){ vs.innerHTML=duelVsHtml(); vs.classList.remove('hidden'); }\n  else if(d.battle&&Sim.S.war&&(Sim.S.war.battle||d.endE)){ vs.innerHTML=vsHtml(d.endE); vs.classList.remove('hidden'); }")
rp("hd.textContent=d.battle?'이번 전투':'지금까지'", "hd.textContent=d.duel?'이번 결투':d.battle?'이번 전투':'지금까지'")
rp("const GRP={master:{n:'마스터'},seal:{n:'령주',strip:/^령주: /},special:{n:'특수 행동'}};",
   "const GRP={master:{n:'마스터'},eye:{n:'마안'},arcana:{n:'고위 기술'},seal:{n:'령주',strip:/^령주: /},talk:{n:'말을 건다'},special:{n:'특수 행동'}};")
rp("for(const g of ['master','seal','special'])", "for(const g of ['master','eye','arcana','seal','talk','special'])")
rp("const B=Sim.S.war&&Sim.S.war.battle, left=", "const B=Sim.S.war&&(Sim.S.war.battle||Sim.S.war.duel), left=")
CSS = (".comp{margin-top:5px;display:flex;flex-wrap:wrap;gap:3px 8px;font-size:11.5px;color:var(--text)}"
       "\n.side.me .phd .mst{flex:0 0 auto;width:52px;height:52px;margin:10px;display:grid;place-items:center;transform:rotate(45deg);border:1px solid var(--gold);background:rgba(20,18,36,.85);box-shadow:0 0 12px rgba(201,164,92,.25)}"
       "\n.side.me .phd .mst span{transform:rotate(-45deg);font-size:12px;color:var(--gold);text-align:center;line-height:1.25}"
       "\n.side .hes{display:flex;gap:6px;align-items:center;margin-top:6px;font-size:12px;color:var(--dim)}"
       "\n.side .hes .lv{display:flex;gap:3px}.side .hes .lv i{width:16px;height:6px;border-radius:2px;background:rgba(156,148,169,.3)}.side .hes .lv i.on{background:var(--gold)}"
       "\n.side .hes b{color:var(--gold);font-weight:600}")
rp(".comp{margin-top:5px;display:flex;flex-wrap:wrap;gap:3px 8px;font-size:11.5px;color:var(--text)}", CSS)
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

# 글: 한국어|영어|일본어|간체. 'T ' 로 시작하면 문장 틀({0} · {0~이} …)
def zht(z): return None if CC is None else CC.convert(z).replace('“', '「').replace('”', '」').replace('‘', '『').replace('’', '』')
DI, TP, ZH = [], [], {}
for ln in open(os.path.join(D0, 'duel_lines.txt'), encoding='utf-8'):
    ln = ln.rstrip('\n')
    if not ln.strip() or ln.startswith('#'): continue
    tpl = ln.startswith('T ')
    p = [x.strip() for x in (ln[2:] if tpl else ln).split('|')]
    if len(p) != 4 or not all(p): raise SystemExit('칸이 4개가 아님: ' + ln[:70])
    (TP if tpl else DI).append((p[0], p[1], p[2])); ZH[p[0]] = p[3]
s, nd, nt = i18n.add(s, DI, TP)
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(D0, 'zh', 'done.json'); Z = json.load(open(zp, encoding='utf-8')); n = 0
for k, z in ZH.items():
    if k in Z: continue
    t = zht(z)
    if t is None: raise SystemExit('번체를 만들 OpenCC가 없고 done.json에도 없음: ' + k[:40])
    Z[k] = [z, t]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 사전', nd, '· 틀', nt, '· 중국어', n)
