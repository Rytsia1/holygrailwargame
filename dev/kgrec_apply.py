"""11-22: 검귀 루트 결과 화면 글 — 맨 위 기록 카드의 전쟁 한 줄 · 「성배전쟁 기록」의 판정 · 나의 조 결과 · 날짜별 기록 끝 줄 · 지난 생 목록 이름표 · 기록 복사
- 결말마다(record r.kg + r.kgv = 결말 연출 키) 이름표(결말 이름) · 한 줄 · 덧붙임을 둔다. 본성 속 진심 글귀는 「본성 속 진심 「…」」로 붙인다(r.kgw)
- ④ 등 뒤의 칼 · ① 막아선 칼에서 서번트의 결과가 「끝까지 함께했다」로 나오던 것 → 엔진(kgDie)이 w.myOut을 남긴다
사용: python3 kgrec_apply.py <game.html>"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import i18n
P = sys.argv[1]
s = open(P, encoding='utf-8').read(); miss = []
def rp(o, n):
    global s
    if s.count(o) != 1: miss.append((o[:70], s.count(o))); return
    s = s.replace(o, n)
# 결말 → [이름표, 한 줄, 덧붙임]
KGR = {
 'kgM': ('검을 거두지 않은 자', '막아선 서번트를 베고 본성 속 진심을 이뤘다', '잔이 당신의 소원을 받아 들었다'),
 'kgT': ('둘이 이긴 세계', '서번트와 함께 본성 속 진심을 이뤘다', '둘이 이긴 세계의 첫 아침 · 그 세계는 아주 조용했다'),
 'kgB': ('묶인 잔', '령주로 묶은 서번트와 함께 본성 속 진심을 이뤘다', '서번트는 곁에 남았다 · 그 뒤로 입을 열지 않았다'),
 'kgS': ('막아선 칼', '본성 속 진심을 막아선 서번트의 칼 앞에 쓰러졌다', '잔은 새벽 속에서 부서졌다'),
 'kgF': ('등 뒤의 칼', '함께 가던 서번트에게 등을 베였다', '서번트가 남은 마력으로 잔을 부수고 사라졌다'),
 'kgP': ('잔을 내려놓은 손', '본성 속 진심을 잔에 맡기지 않고 서번트와 함께 잔을 부쉈다', '잔은 둘의 손으로 부서졌다'),
 'kgP2': ('잔을 내려놓은 손', '본성 속 진심을 잔에 맡기지 않고 서번트를 이 세계에 남겼다', '바닥에 고였던 빛이 서번트에게 스며들었다'),
 'kgX': ('손을 놓친 잔', '잔을 막으러 온 동맹에게 서번트를 잃었다', '동맹이 잔을 부쉈다 · 당신은 살아남았다'),
}
JS = "const KGR=" + json.dumps(KGR, ensure_ascii=False) + ";\n" + \
     "const kgR_=r=>{ if(!r||!r.kg) return null; const k=r.kgv&&KGR[r.kgv]?r.kgv:({m:'kgM',t:'kgT',b:'kgB',s:'kgS',f:'kgF',p:'kgP',x:'kgX'})[r.kg]; return KGR[k]?{k,tag:KGR[k][0],war:KGR[k][1],sub:KGR[k][2]}:null; };\n" + \
     "const kgWishT=r=>r&&r.kg&&r.kgw?`본성 속 진심 「${r.kgw}」`:(r&&r.kg?'':r&&r.wish||'');\n"
rp("const warTxt=r=>bxEndOf(r)==='me'&&wkey(r)==='victor'?'셋쇼인 키아라를 쓰러뜨렸다':r.war;",
   JS + "const warTxt=r=>kgR_(r)?kgR_(r).war:bxEndOf(r)==='me'&&wkey(r)==='victor'?'셋쇼인 키아라를 쓰러뜨렸다':r.war;")
rp("const rlab=(r,k)=>bxEndOf(r)==='me'&&k==='victor'?'키아라 처치':(RLAB[k]||'');",
   "const rlab=(r,k)=>kgR_(r)?kgR_(r).tag:bxEndOf(r)==='me'&&k==='victor'?'키아라 처치':(RLAB[k]||'');")
# 기록 카드
rp("${warTxt(r)}${r.wish?` · ${esc(r.wish)}`:''}</span></dd>", "${warTxt(r)}${kgWishT(r)?` · ${esc(kgWishT(r))}`:''}</span></dd>")
# 성배전쟁 기록: 판정 · 덧붙임
rp("<div class=\"verdict\">${esc(RLAB[k]==='전사'?'전쟁 중에 숨을 거두었다':warTxt(r))}",
   "<div class=\"verdict\">${esc(kgR_(r)?kgR_(r).war:RLAB[k]==='전사'?'전쟁 중에 숨을 거두었다':warTxt(r))}")
rp("  const my=wd.my;\n  const myState= my.out?",
   "  { const G=kgR_(r); if(G) verdictSub=[G.sub,r.kgw?`본성 속 진심 「${esc(r.kgw)}」`:''].filter(Boolean).join(' · '); }\n  const my=wd.my;\n  const myState= my.out?")
rp("if(endTxt&&k!=='dead') tl.push({d:wd.day,tod:'밤',k:'end',t:endTxt});",
   "if(kgR_(r)) tl.push({d:wd.day,tod:'밤',k:'end',t:kgR_(r).sub.split(' · ')[0]}); else if(endTxt&&k!=='dead') tl.push({d:wd.day,tod:'밤',k:'end',t:endTxt});")
rp("<td>${my.alive&&RGRP(k)==='grail'?",
   "<td>${my.alive&&['t','b'].includes(r.kg)?'<span class=\"st win\">본성 속 진심을 이뤘다</span>':my.alive&&RGRP(k)==='grail'?")
# 기록 복사
rp("${warTxt(r)}${r.wish?' · '+r.wish:''}${bt?", "${warTxt(r)}${kgWishT(r)?' · '+kgWishT(r):''}${bt?")
rp("${wt}${r.wish?' · '+T(r.wish):''}${bt?", "${wt}${kgWishT(r)?' · '+T(kgWishT(r)):''}${bt?")
# 기록에 결말 연출 키와 진심 글귀
rp("kg:S.flags.kgEnd||'', ach:", "kg:S.flags.kgEnd||'', kgv:S.flags.kgEnd?S.flags.endFx||'':'', kgw:S.flags.kgEnd&&S.flags.kg&&KG_W[S.flags.kg]?KG_W[S.flags.kg].wish:'', ach:")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
# 번역
D = [
 ('검을 거두지 않은 자', 'The One Who Did Not Sheathe the Sword', '剣を収めなかった者', '未曾收剑之人', '未曾收劍之人'),
 ('둘이 이긴 세계', 'The World the Two of You Won', 'ふたりが勝ち取った世界', '两人赢下的世界', '兩人贏下的世界'),
 ('묶인 잔', 'The Bound Cup', '縛られた杯', '被束缚的杯', '被束縛的杯'),
 ('막아선 칼', 'The Blade That Stood in the Way', '立ちはだかった刃', '挡在面前的剑', '擋在面前的劍'),
 ('잔을 내려놓은 손', 'The Hand That Set Down the Cup', '杯を置いた手', '放下杯子的手', '放下杯子的手'),
 ('손을 놓친 잔', 'The Cup That Slipped Away', '手から零れた杯', '脱手的杯', '脫手的杯'),
 ('막아선 서번트를 베고 본성 속 진심을 이뤘다', 'You cut down the Servant who stood in your way and fulfilled the truth beneath your nature', '立ちはだかったサーヴァントを斬り、本性に潜む本心を叶えた', '斩倒挡路的从者，实现了本性深处的真心', '斬倒擋路的從者，實現了本性深處的真心'),
 ('서번트와 함께 본성 속 진심을 이뤘다', 'You fulfilled the truth beneath your nature together with your Servant', 'サーヴァントと共に、本性に潜む本心を叶えた', '与从者一同实现了本性深处的真心', '與從者一同實現了本性深處的真心'),
 ('령주로 묶은 서번트와 함께 본성 속 진심을 이뤘다', 'You fulfilled the truth beneath your nature with a Servant bound by a Command Spell', '令呪で縛ったサーヴァントと共に、本性に潜む本心を叶えた', '与被令咒束缚的从者一同实现了本性深处的真心', '與被令咒束縛的從者一同實現了本性深處的真心'),
 ('본성 속 진심을 막아선 서번트의 칼 앞에 쓰러졌다', 'You fell before the blade of the Servant who stood against the truth beneath your nature', '本性に潜む本心に立ちはだかったサーヴァントの刃の前に倒れた', '倒在了阻挡本性深处真心的从者剑下', '倒在了阻擋本性深處真心的從者劍下'),
 ('함께 가던 서번트에게 등을 베였다', 'The Servant walking beside you cut you down from behind', '共に歩んでいたサーヴァントに、背を斬られた', '被同行的从者从背后斩倒', '被同行的從者從背後斬倒'),
 ('본성 속 진심을 잔에 맡기지 않고 서번트와 함께 잔을 부쉈다', 'You did not entrust the truth beneath your nature to the cup, and broke it together with your Servant', '本性に潜む本心を杯に委ねず、サーヴァントと共に杯を砕いた', '没有把本性深处的真心托付给杯，与从者一同打碎了杯', '沒有把本性深處的真心託付給杯，與從者一同打碎了杯'),
 ('본성 속 진심을 잔에 맡기지 않고 서번트를 이 세계에 남겼다', 'You did not entrust the truth beneath your nature to the cup, and kept your Servant in this world', '本性に潜む本心を杯に委ねず、サーヴァントをこの世界に残した', '没有把本性深处的真心托付给杯，而是让从者留在了这个世界', '沒有把本性深處的真心託付給杯，而是讓從者留在了這個世界'),
 ('잔을 막으러 온 동맹에게 서번트를 잃었다', 'You lost your Servant to the ally who came to stop the cup', '杯を止めに来た同盟にサーヴァントを奪われた', '在前来阻止杯的同盟手中失去了从者', '在前來阻止杯的同盟手中失去了從者'),
 ('잔이 당신의 소원을 받아 들었다', 'The cup accepted your wish', '杯はあなたの願いを受け入れた', '杯接受了你的愿望', '杯接受了你的願望'),
 ('둘이 이긴 세계의 첫 아침', 'The first morning of the world the two of you won', 'ふたりが勝ち取った世界の最初の朝', '两人赢下的世界的第一个早晨', '兩人贏下的世界的第一個早晨'),
 ('그 세계는 아주 조용했다', 'That world was very quiet', 'その世界はとても静かだった', '那个世界非常安静', '那個世界非常安靜'),
 ('서번트는 곁에 남았다', 'The Servant stayed by your side', 'サーヴァントは傍に残った', '从者留在了你身边', '從者留在了你身邊'),
 ('그 뒤로 입을 열지 않았다', 'and never spoke again', 'それきり口を開かなかった', '此后再也没有开口', '此後再也沒有開口'),
 ('잔은 새벽 속에서 부서졌다', 'The cup shattered in the dawn', '杯は夜明けの中で砕けた', '杯在黎明中碎裂', '杯在黎明中碎裂'),
 ('서번트가 남은 마력으로 잔을 부수고 사라졌다', 'The Servant broke the cup with the last of its mana and vanished', 'サーヴァントは残った魔力で杯を砕き、消えた', '从者用残余的魔力打碎了杯，随后消失', '從者用殘餘的魔力打碎了杯，隨後消失'),
 ('잔은 둘의 손으로 부서졌다', 'The cup broke in both your hands', '杯はふたりの手で砕かれた', '杯在两人手中碎裂', '杯在兩人手中碎裂'),
 ('바닥에 고였던 빛이 서번트에게 스며들었다', 'The light pooled at the bottom seeped into your Servant', '底に溜まっていた光が、サーヴァントに染み込んだ', '积在杯底的光渗入了从者体内', '積在杯底的光滲入了從者體內'),
 ('동맹이 잔을 부쉈다', 'Your ally broke the cup', '同盟が杯を砕いた', '同盟打碎了杯', '同盟打碎了杯'),
 ('당신은 살아남았다', 'You survived', 'あなたは生き残った', '你活了下来', '你活了下來'),
 ('본성 속 진심을 이뤘다', 'Fulfilled the truth beneath their nature', '本性に潜む本心を叶えた', '实现了本性深处的真心', '實現了本性深處的真心'),
 ('당신을 베고 잔을 부순 뒤 사라졌다', 'Cut you down, broke the cup, and vanished', 'あなたを斬り、杯を砕いて消えた', '斩倒你、打碎杯后消失了', '斬倒你、打碎杯後消失了'),
 ('결투 끝에 잔을 부수고 새벽 속으로 흩어졌다', 'After the duel, broke the cup and scattered into the dawn', '決闘の末、杯を砕いて夜明けに散った', '决斗之后打碎了杯，消散在黎明中', '決鬥之後打碎了杯，消散在黎明中'),
]
TPL = [('본성 속 진심 「{0}」', 'True heart: “{0}”', '本性に潜む本心「{0}」', '本性深处的真心「{0}」', '本性深處的真心「{0}」')]
s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, *_ in D], [(a, b, c) for a, b, c, *_ in TPL])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(HERE, 'zh', 'done.json'); Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _b, _c, d, e in D + TPL:
    if a not in Z: Z[a] = [d, e]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('kgrec 적용 · 사전', nd, nt, '· 중국어', n)
