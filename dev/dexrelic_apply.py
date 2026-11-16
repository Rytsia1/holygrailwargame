"""11-16: 서번트 도감의 성유물
① 계약한 서번트의 도감 상세에 「성유물」 줄 — 성유물 이름 · ‘전승’에 얽힌 물건
③ 아직 만나지 못한 서번트라도 그 성유물을 손에 넣은 적이 있으면, 도감의 ??? 칸에 ‘성유물’의 주인이라고 보인다.
   마주치기만 한 서번트의 상세에도 성유물 줄(손에 넣은 적이 있다)이 보인다.
- 기록: 한 생에서 손에 넣은 성유물을 지난 생 기록(rel)에 남기고, 도감(heroes[id].rh)에 모은다. 이 판부터 쌓인다(예전 생에는 없음)
사용: python3 dexrelic_apply.py <game.html>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'S.relSeen' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:80], k)); return
    s = s.replace(o, n)

# 한 생에서 손에 넣은 성유물(내놓거나 쓴 것도 포함)
rp("  function addRelic(id){ S.relics=S.relics||[]; if(id&&!S.relics.includes(id)) S.relics.push(id); }",
   "  function addRelic(id){ S.relics=S.relics||[]; if(id&&!S.relics.includes(id)) S.relics.push(id); S.relSeen=S.relSeen||[]; if(id&&!S.relSeen.includes(id)) S.relSeen.push(id); }")
rp("bx:S.flags.bxEnd?'moon':S.flags.bxDream?'dream':'', ach:(S.ach||[]).slice()};",
   "bx:S.flags.bxEnd?'moon':S.flags.bxDream?'dream':'', ach:(S.ach||[]).slice(), rel:[...new Set([...(S.relSeen||[]),...(S.relics||[]),...(S.relic?[S.relic]:[])])]};")
# 도감에 모으기 · 지난 생 기록에서 다시 채우기
rp("  for(const id of new Set([...(r.ach||[]),...retroAch(r)])) if(!c.ach[id]){",
   "  for(const id of r.rel||[]) if(Sim.H_BY[id]) dexHero(c,id).rh=1;   // 손에 넣은 적이 있는 성유물\n"
   "  for(const id of new Set([...(r.ach||[]),...retroAch(r)])) if(!c.ach[id]){")
rp("  for(const [a,b] of Object.entries(HERO_ALIAS)) if(c.heroes[a]){",
   "  // 성유물 기록 되살리기: 동기화로 빠져도 남아 있는 지난 생 기록에서 다시 채운다\n"
   "  { let up=false; for(const r of store.get(K_HIST)||[]) for(const id of r.rel||[]) if(Sim.H_BY[id]&&!(c.heroes[id]&&c.heroes[id].rh)){ dexHero(c,id).rh=1; up=true; } if(up) store.set(K_CODEX,c); }\n"
   "  for(const [a,b] of Object.entries(HERO_ALIAS)) if(c.heroes[a]){")
rp("t.first=t.first||e.first; delete c.heroes[a]; }", "t.first=t.first||e.first; if(e.rh) t.rh=1; delete c.heroes[a]; }")
# 성유물 이름: 언어별 따옴표
rp("function showDexInfo(", "function relQ(n){ const t=tr(n); return LANG==='ja'?`「${t}」`:LANG==='ko'?`‘${t}’`:`“${t}”`; }\nfunction showDexInfo(")
# 마주친 기록: 쓰러뜨린 횟수가 옮겨지지 않던 것
rp("${e.met}번${e.beat?` · 그중 ${e.beat}번 쓰러뜨렸다`:''}", "${e.met}번${e.beat?` · ${tr(`그중 ${e.beat}번 쓰러뜨렸다`)}`:''}")
# ③ ??? 칸: 성유물의 주인
rp("""  const unk=x=>all?`<div class="dx-card u nm">${faceHtml(null,48,{unk:true})}<div><span class="n">${esc(x.name)}</span><span class="t">아직 만나지 못했다</span></div></div>`:`<div class="dx-card u">${faceHtml(null,48,{unk:true})}<div><span class="n">???</span><span class="t">아직 만나지 못했다</span></div></div>`;""",
   """  const unk=x=>{ const rh=!!(c.heroes[x.id]&&c.heroes[x.id].rh), t=rh?esc(tr(`‘${x.relic}’의 주인`)):'아직 만나지 못했다';
    return all?`<div class="dx-card u nm${rh?' rh':''}">${faceHtml(null,48,{unk:true})}<div><span class="n">${esc(x.name)}</span><span class="t">${t}</span></div></div>`:`<div class="dx-card u${rh?' rh':''}"${rh?` title="${t}"`:''}>${faceHtml(null,48,{unk:true})}<div><span class="n">???</span><span class="t">${t}</span></div>${rh?`<span class="mk">${esc(tr('성유물'))}</span>`:''}</div>`; };""")
# ① 상세: 성유물 줄
rp("<dl class=\"row\"><dt>보구</dt><dd>${esc(x.art.n)} <span class=\"unk\">· ${esc(x.art.d)}</span></dd>",
   "<dl class=\"row\"><dt>보구</dt><dd>${esc(x.art.n)} <span class=\"unk\">· ${esc(x.art.d)}</span></dd><dt>성유물</dt><dd>${esc(relQ(x.relic))} <span class=\"unk\">· ${esc(tr(`‘${x.from}’에 얽힌 물건`))}</span></dd>")
rp("""  else html+=`<p class="unk" style="margin-top:12px">계약하면 능력치와 보구, 사연이 공개됩니다.</p>${met}`;""",
   """  else html+=`${e.rh?`<dl class="row" style="margin-top:12px"><dt>성유물</dt><dd>${esc(relQ(x.relic))} <span class="unk">· 손에 넣은 적이 있다</span></dd></dl>`:''}<p class="unk" style="margin-top:12px">계약하면 능력치와 보구, 사연이 공개됩니다.</p>${met}`;""")
# 모양: 성유물을 쥔 적 있는 ??? 칸은 점선 금테
rp(".dx-card.m{cursor:pointer}.dx-card.m .n{color:#cfc8ba}",
   ".dx-card.m{cursor:pointer}.dx-card.m .n{color:#cfc8ba}\n.dx-card.u.rh,body.lb-on #lbRec .dx-card.u.rh{border:1px dashed rgba(216,189,124,.55)!important}.dx-card.u.rh .t{color:var(--gold2);opacity:.9;white-space:normal;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;word-break:keep-all}.dx-card.u.rh .mk{color:var(--gold2);opacity:.8}")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

T = [('‘{0}’의 주인', 'Owner of “{0}”', '「{0}」の持ち主', '“{0}”的主人', '「{0}」的主人'),
     ('그중 {0}번 쓰러뜨렸다', 'defeated {0}', 'うち{0}回撃破', '其中{0}次击败', '其中{0}次擊敗')]
D = [('성유물', 'Relic', '聖遺物', '圣遗物', '聖遺物'),
     ('손에 넣은 적이 있다', 'You once held it', 'かつて手にしたことがある', '曾经拿到过', '曾經拿到過')]
s, nd, nt = i18n.add(s, dict_items=[(a, b, c) for a, b, c, *_ in D], tpl_items=[(a, b, c) for a, b, c, *_ in T])
open(P, 'w', encoding='utf-8').write(s)
import json
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
if os.path.exists(zp):
    Z = json.load(open(zp, encoding='utf-8')); n = 0
    for a, _b, _c, d, e in D + T:
        if a not in Z: Z[a] = [d, e]; n += 1
    json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0); print('중국어 사전', n)
print('적용 끝 · 사전', nd, '틀', nt)
