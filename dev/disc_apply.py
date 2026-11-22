"""11-22: 비공식 표기 — 팬이 만든 비공식 2차 창작 게임이며 TYPE-MOON · 공식 권리자와 관계없다는 한 줄
- A: 「이 밤의 이야기와 규칙」 창 맨 아래, 스포일러 주의 줄 밑
- B: 로비 화면 맨 아래 흐린 한 줄(로비에 있을 때만 · 소개 창을 열거나 화면 숨기기 중에는 감춤)
  넓은 화면과 첫 화면은 화면 바닥에 고정(왼쪽 메뉴 칸 오른쪽 가운데), 폰의 메뉴 화면은 메뉴 맨 끝(링크 단추 밑)에 흐름대로
- (C: 후원 창 아래는 support 브랜치의 support_apply)
사용: python3 disc_apply.py <game.html>"""
import sys, json
P = sys.argv[1]
s = open(P, encoding='utf-8').read(); miss = []
def rp(o, n):
    global s
    if s.count(o) != 1: miss.append((o[:70], s.count(o))); return
    s = s.replace(o, n)
DISC = {
 'ko': '「성배가 차는 밤」은 팬이 만든 비공식 2차 창작 게임이며, TYPE-MOON 및 공식 권리자와는 관계가 없습니다.',
 'en': '“The Night the Grail Fills” is an unofficial fan-made game and is not affiliated with TYPE-MOON or any official rights holders.',
 'ja': '『聖杯が満ちる夜』はファンが制作した非公式の二次創作ゲームであり、TYPE-MOONおよび公式の権利者とは関係ありません。',
 'zhs': '《圣杯盈满之夜》是粉丝制作的非官方同人游戏，与TYPE-MOON及官方权利方无关。',
 'zht': '《聖杯盈滿之夜》是粉絲製作的非官方同人遊戲，與TYPE-MOON及官方權利方無關。',
}
rp("  intro.classList.add('lb');\n",
   "  const DISC=" + json.dumps(DISC, ensure_ascii=False) + "[typeof LANG==='string'&&['en','ja','zhs','zht'].includes(LANG)?LANG:'ko']; window.__DISC=DISC;   // 11-22 비공식 표기 (disc_apply)\n"
   "  intro.classList.add('lb');\n")
# A
rp("el('p','ab-spoil',TX.spoil),go);", "el('p','ab-spoil',TX.spoil),el('p','ab-spoil','※ '+DISC),go);")
# B — 폰 메뉴 화면용 자리는 lb2 틀에 넣고 로비에 들어올 때 글을 채운다
rp('<div class="l2-foot"><div class="l2-links"></div>', '<p class="l2-disc">${window.__DISC||\'\'}</p><div class="l2-foot"><div class="l2-links"></div>')
rp("sndSt(); LOBBY.enter(s); requestAnimationFrame(()=>LOBBY.fit());", "sndSt(); LOBBY.enter(s); document.querySelectorAll('#lb2 .l2-disc').forEach(e=>{ if(!e.textContent) e.textContent=DISC; }); requestAnimationFrame(()=>LOBBY.fit());")
rp("  intro.insertBefore(scr,intro.firstChild);\n",
   "  intro.insertBefore(scr,intro.firstChild);\n"
   "  { const d=el('p','lb-disc'); d.textContent=DISC; document.body.appendChild(d); }\n")
CSS = ("\n/* 11-22 비공식 표기 (disc_apply) */\n"
       ".lb-disc{display:none}\n"
       "body.lb-on .lb-disc{display:block;position:fixed;left:0;right:0;bottom:max(8px,env(safe-area-inset-bottom,0px));margin:0;"
       "padding:0 max(16px,env(safe-area-inset-right,0px)) 0 max(16px,env(safe-area-inset-left,0px));text-align:center;font-size:11px;line-height:1.5;"
       "color:rgba(235,229,216,.42);z-index:5;pointer-events:none;text-wrap:balance}\n"
       "body.lb-wide.lb-on .lb-disc{left:380px}\n"
       "@media (max-height:519px){body.lb-wide.lb-on .lb-disc{left:300px}}\n"
       "body.lb-on.lb-s2:not(.lb-wide) .lb-disc{display:none}\n"
       "#lb2 .l2-disc{display:none}\n"
       "body.lb-s2:not(.lb-wide) #lb2 .l2-disc{display:block;order:9;margin:14px 0 0;text-align:center;font-size:11px;line-height:1.5;color:rgba(235,229,216,.42);text-wrap:balance}\n"
       "body.lb-reading .lb-disc,body.lb-hideui .lb-disc,body.lb-rec .lb-disc,body.lb-hideui #lb2 .l2-disc{display:none!important}\n")
i = s.find('</style>')
if i < 0: miss.append(('</style>', 0))
else: s = s[:i] + CSS + s[i:]
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
print('disc 적용')
