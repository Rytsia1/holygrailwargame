"""11-17: 이름 고정 — 태어나는 장면의 이름 칸 아래 「다음에도 이 이름으로」
- 체크하고 이름을 정하면 그 성 · 이름을 기억해 두고, 다음 생부터 이름 칸에 미리 채워 둔다(체크도 켜진 채).
- 체크를 끄고 정하면 기억을 지우고 예전처럼 도시에 맞는 이름을 추천한다.
- 「다른 이름」 주사위 · 직접 고치기는 그대로 된다. 성별 · 도시가 바뀌어도 고정한 이름을 그대로 쓴다.
사용: python3 namefix_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if "K_NAMEFIX" in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

rp('<label class="b-opt"><input type="checkbox" id="bNoFx"><span id="bLNoFx"></span></label>',
   '<div class="b-opts"><label class="b-opt"><input type="checkbox" id="bFix"><span id="bLFix"></span></label>'
   '<label class="b-opt"><input type="checkbox" id="bNoFx"><span id="bLNoFx"></span></label></div>')
rp(".b-opt{display:flex;gap:6px;align-items:center;font-size:12px;color:var(--faint);cursor:pointer}",
   ".b-opt{display:flex;gap:6px;align-items:center;font-size:12px;color:var(--faint);cursor:pointer}"
   ".b-opts{display:flex;flex-wrap:wrap;gap:4px 16px}")
for a, b in [("nofx:'다음부터 시작 연출 건너뛰기',aria:'태어나기',lead:sx", "fix:'다음에도 이 이름으로',"),
             ("nofx:'Skip the opening next time',", "fix:'Keep this name next time',"),
             ("nofx:'次回から演出を省略する',", "fix:'次回もこの名前にする',"),
             ]:
    rp(a, b + a)
# 중국어 BT(zhs · zht)는 zh/zh_apply.py가 넣는다 — 거기에도 fix를 넣어 두었다
rp("$('#bLNoFx').textContent=BT0.nofx;", "$('#bLNoFx').textContent=BT0.nofx; $('#bLFix').textContent=BT0.fix||'다음에도 이 이름으로';")
# 이름 칸 채우기: 고정한 이름이 있으면 그것으로
rp("    sug={sur:S.sur,given:givenOf(S.name,S.sur,L)}; fill(); $('#bNoFx').checked=noFx();",
   "    const fx=store.get(K_NAMEFIX); sug=fx&&(fx.sur||fx.given)?{sur:fx.sur||'',given:fx.given||''}:{sur:S.sur,given:givenOf(S.name,S.sur,L)}; fill(); $('#bFix').checked=!!(fx&&(fx.sur||fx.given)); $('#bNoFx').checked=noFx();")
rp("    Sim.setName(a,b); const nf=$('#bNoFx').checked;",
   "    Sim.setName(a,b); if($('#bFix').checked) store.set(K_NAMEFIX,{sur:a,given:b}); else store.del(K_NAMEFIX); const nf=$('#bNoFx').checked;")
rp("const Birth=(()=>{\n", "const K_NAMEFIX='cupnight.nameFix.v1';   // 이름 고정: 다음 생에도 이름 칸에 미리 채워 둘 성 · 이름 (11-17)\nconst Birth=(()=>{\n")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
print('적용 끝')
