"""11-21: 검귀 루트 연출 ① 본성 속 진심(진입) ② 등 뒤의 칼 (갈래 a 눈치채지 못함 · b 령주로 멈춰라 · c 알면서 둔다 · h 동맹 앞에서 먼저 닿음)
- 화면: dev/kgfx.js (결말 연출의 맑은 성배 · 밤 · 빛의 수면 · 파동과 같은 그림, 공통 틀 xfxOpen · 누르면 넘어감)
- 소리: dev/sumsnd_kg.py가 만든 j_kg_in · j_kg_back_a/b/c/h (public/assets/sound)
- 엔진(kg.js)이 기록 줄에 fx {t:'kgin'} · {t:'kgback',v}를 붙인다. 령주로 멈춰라는 useSeal에 이 연출을 넘겨 공통 령주 연출과 겹치지 않는다
사용: python3 kgfx_apply.py <game.html>"""
import sys, os, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import i18n
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'function kgInFx(' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)
SND = os.path.join(HERE, '..', 'public', 'assets', 'sound')
def dur(n):
    try: return round(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(SND, n + '.mp3')], capture_output=True, text=True).stdout.strip()), 2)
    except Exception: return 6.0
SNDS = ['j_end_kgN', 'j_end_kgF', 'j_end_kgS', 'j_end_kgT', 'j_kg_in', 'j_kg_back_a', 'j_kg_back_b', 'j_kg_back_c', 'j_kg_back_h', 'j_kg_day1', 'j_kg_day2', 'j_kg_day3', 'j_kg_day4', 'j_kg_full_r', 'j_kg_full_g', 'j_kg_duel', 'j_kg_mr', 'j_kg_ally']
CSS = (".kgx .kgx-w{position:absolute;left:0;right:0;top:12%;text-align:center;padding:0 22px;font-family:var(--f-story);font-size:clamp(16px,3.6vw,22px);line-height:1.7;color:#fff4dc;opacity:0;pointer-events:none;word-break:keep-all}"
       ".kgx .kgx-w.red{color:#ffe9ec}.kgx .kgx-w span.c{display:inline-block;opacity:0}.kgx .kgx-w .ww{display:inline-block;white-space:nowrap}"
       ".kgx .xd-txt{bottom:12%}.kgx .xd-d.long{letter-spacing:.12em;font-size:clamp(24px,5.6vw,38px)}"
       ".kgx .kgx-hint{position:absolute;left:0;right:0;bottom:4.5%;text-align:center;font-family:var(--f-mono);font-size:12px;letter-spacing:.2em;color:#d9c9d0;opacity:0;pointer-events:none}"
       ".kgx .xd-s{color:#efe2cf;line-height:1.65;word-break:keep-all;max-width:26em;margin:0 auto;text-shadow:0 0 4px #000,0 0 12px #000}.kgx .kgx-s2{margin-top:6px;opacity:0}"
       # 가로로 눕힌 휴대폰처럼 낮은 화면: 아래 글을 작고 낮게 두어 잔 · 초상과 겹치지 않게 (검귀 연출 · 검귀 결말 전용 장면만)
       "@media (max-height:520px) and (min-aspect-ratio:1/1){.kgx .xd-txt,.kge .txt{bottom:4%!important}.kgx .xd-d,.kgx .xd-d.long,.kge .txt .d,.kge .txt .d.long{font-size:clamp(20px,6.5vh,30px)!important}"
       ".kgx .xd-rule,.kge .txt .rule{margin:5px auto!important}.kgx .xd-s,.kge .txt .s,.kge .txt .s2{font-size:12.5px!important;line-height:1.45!important}.kgx .kgx-s2,.kge .txt .s2{margin-top:2px!important}.kgx .kgx-w,.kge .wish{top:5%!important;font-size:15px!important}}")

js = open(os.path.join(HERE, 'kgfx.js'), encoding='utf-8').read()
rp("function bxOrderFx(fx){", js + "\nfunction bxOrderFx(fx){")
rp("bxconf:bxConfFx,bxorder:bxOrderFx};", "bxconf:bxConfFx,bxorder:bxOrderFx,kgin:kgInFx,kgback:kgBackFx,kgday:kgDayFx,kgfull:kgFullFx,kgduel:kgDuelFx,kgmr:kgMrFx,kgally:kgAllyFx};")
rp('"j_bx_order":{"d":4.63}', '"j_bx_order":{"d":4.63},' + ','.join(f'"{n}":{{"d":{dur(n)}}}' for n in SNDS))
rp(".xd-rule.bx{", CSS + ".xd-rule.bx{")
# 결말 전용 장면(시안 8~10): kg_apply가 빌려 쓰던 장면을 바꿔 끼운다 · 소리는 효과 + 결말 곡을 붙인 판
import re
_n = len(re.findall(r"  SCN\.kg[FST]=scnAs\([^\n]*\n", s))
if _n != 3: miss.append(('SCN.kgF/S/T', _n))
s = re.sub(r"  SCN\.kgT=scnAs\([^\n]*\n", '', s); s = re.sub(r"  SCN\.kgS=scnAs\([^\n]*\n", '', s)
s = re.sub(r"  SCN\.kgF=scnAs\([^\n]*\n", lambda m: open(os.path.join(HERE, 'kgend.js'), encoding='utf-8').read(), s)
rp(" items=items.slice(-24);\n    // 결과 팝업", " items=items.slice(-24); if(d.recap) items=d.recap.slice(-24);   // 11-22: 창이 넘겨준 기록(후일담 창의 마지막 순간)\n    // 결과 팝업")
rp("const END_SK={", "const END_SK={kgF:'j_end_kgF',kgS:'j_end_kgS',kgT:'j_end_kgT',")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
# 새 글 (한국어 · 영어 · 일본어 · 간체 · 번체)
D = [
 ('마지막 순간', 'Final moments', '最期の瞬間', '最后的瞬间', '最後的瞬間'),
 ('서번트 결심 ↑', 'Servant resolve ↑', 'サーヴァントの決意 ↑', '从者决心 ↑', '從者決心 ↑'),
 ('서번트 결심 ↑↑', 'Servant resolve ↑↑', 'サーヴァントの決意 ↑↑', '从者决心 ↑↑', '從者決心 ↑↑'),
 ('서번트 결심 ↓', 'Servant resolve ↓', 'サーヴァントの決意 ↓', '从者决心 ↓', '從者決心 ↓'),
 ('서번트 결심 ↓↓', 'Servant resolve ↓↓', 'サーヴァントの決意 ↓↓', '从者决心 ↓↓', '從者決心 ↓↓'),
 ('신뢰 ↓↓', 'Trust ↓↓', '信頼 ↓↓', '信赖 ↓↓', '信賴 ↓↓'),
 ('서번트 건강 ↓', 'Servant health ↓', 'サーヴァントの健康 ↓', '从者健康 ↓', '從者健康 ↓'),
 ('본성 속 진심', 'The Truth Beneath Your Nature', '本性に潜む本心', '本性深处的真心', '本性深處的真心'),
 ('잔은 바닥만 젖었다.', 'Only the bottom of the cup is wet.', '杯は底だけが濡れている。', '杯子只有底部湿了。', '杯子只有底部濕了。'),
 ('가득 차기까지 나흘.', 'Four days until it is full.', '満ちるまで、四日。', '距离盛满，还有四天。', '距離盛滿，還有四天。'),
 ('등 뒤의 온기가 한 걸음 가까워졌다.', 'The warmth at your back came one step closer.', '背中の温もりが、一歩近づいた。', '背后的温度靠近了一步。', '背後的溫度靠近了一步。'),
 ('알고 있었다. 그래도 돌아보지 않았다.', 'You knew. Even so, you did not look back.', 'わかっていた。それでも振り返らなかった。', '你早就知道。即便如此，你也没有回头。', '你早就知道。即便如此，你也沒有回頭。'),
 ('끝까지, 당신이 고른 대로.', 'To the very end, as you chose.', '最後まで、あなたが選んだとおりに。', '直到最后，都如你所选。', '直到最後，都如你所選。'),
 ('당신의 시점은 거기서 끊겼다.', 'Your point of view ended there.', 'あなたの視点はそこで途切れた。', '你的视角就此中断。', '你的視角就此中斷。'),
 ('칼끝이 목 한 뼘 앞에서 멈췄다.', 'The blade stopped a hand’s breadth from your throat.', '刃先が喉の一寸手前で止まった。', '刀尖停在了离喉咙一拃远的地方。', '刀尖停在了離喉嚨一拃遠的地方。'),
 ('등 뒤에서 칼이 먼저 닿았다.', 'The blade at your back reached you first.', '背後から、刃が先に届いた。', '背后的刀先一步碰到了你。', '背後的刀先一步碰到了你。'),
 ('등 뒤의 칼', 'The Blade at Your Back', '背後の刃', '背后的刀', '背後的刀'),
 ('진심', 'True Heart', '本心', '真心', '真心'),
 ('넷째 날 밤', 'Fourth Night', '四日目の夜', '第四天夜', '第四天夜'),
 ('본성에 삼켜진다.', 'You are swallowed by your nature.', '本性に呑まれていく。', '被本性吞噬。', '被本性吞噬。'),
 ('흘러넘치던 본성이 고요해졌다.', 'The nature that had been spilling over fell still.', '溢れ出していた本性が、静まった。', '满溢而出的本性归于平静。', '滿溢而出的本性歸於平靜。'),
 ('나의 서번트였던 자', 'The one who was your Servant', 'かつて我がサーヴァントだった者', '曾是我的从者之人', '曾是我的從者之人'),
 ('서번트가 당신의 앞을 막아섰다.', 'Your Servant stands in your way.', 'サーヴァントが、あなたの前に立ちはだかった。', '从者挡在了你的面前。', '從者擋在了你的面前。'),
 ('대마력', 'Magic Resistance', '対魔力', '对魔力', '對魔力'),
 ('령주가 닿지 못했다.', 'The Command Spell could not reach.', '令呪は届かなかった。', '令咒没能触及。', '令咒沒能觸及。'),
 ('서번트가 강렬한 의지로 저항했다.', 'Your Servant resisted with fierce will.', 'サーヴァントが、強烈な意志で抗った。', '从者以强烈的意志抵抗了。', '從者以強烈的意志抵抗了。'),
 ('동맹', 'Ally', '同盟', '同盟', '同盟'),
 ('동맹이 등을 돌렸다.', 'Your ally turned against you.', '同盟が背を向けた。', '同盟背弃了你。', '同盟背棄了你。'),
 ('셋째 날 물러났던 동맹이 잔을 막으러 돌아왔다.', 'The ally who withdrew on the third day came back to stop the cup.', '三日目に退いた同盟が、杯を止めに戻ってきた。', '第三天退走的同盟回来阻止杯子了。', '第三天退走的同盟回來阻止杯子了。'),
 ('나', 'Me', '私', '我', '我'),
 ('당신이 이겼다', 'You won', 'あなたが勝った', '你赢了', '你贏了'),
 ('당신이 졌다', 'You lost', 'あなたが負けた', '你输了', '你輸了'),
 ('찰나의 순간, 잔과 함께 등을 베였다.', 'In an instant, your back was cut, and the cup with it.', '刹那のうちに、杯もろとも背を斬られた。', '刹那之间，你连同杯子一起被从背后斩开。', '剎那之間，你連同杯子一起被從背後斬開。'),
 ('당신의 사고는 이어지지 않았다.', 'Your thoughts went no further.', 'あなたの思考は、その先へ続かなかった。', '你的思绪没能再延续下去。', '你的思緒沒能再延續下去。'),
 ('무자비한 본성은 저지되었고,', 'Your merciless nature was stopped,', '無慈悲な本性は阻まれ、', '无情的本性被阻止了，', '無情的本性被阻止了，'),
 ('서번트의 표정에는 연민만이 가득했다.', 'and your Servant’s face held nothing but pity.', 'サーヴァントの表情には、憐れみだけが満ちていた。', '从者的脸上只剩下满满的怜悯。', '從者的臉上只剩下滿滿的憐憫。'),
]
TPL = [('「{0}」 성향 ↑', '{0} tendency ↑', '「{0}」の性向 ↑', '「{0}」倾向 ↑', '「{0}」傾向 ↑'),
       ('「{0}」 성향 ↓', '{0} tendency ↓', '「{0}」の性向 ↓', '「{0}」倾向 ↓', '「{0}」傾向 ↓'),
       ('{0} · 결투 종료', '{0} · Duel over', '{0} · 決闘終了', '{0} · 决斗结束', '{0} · 決鬥結束'),
       ('당신 {0}', 'You {0}', 'あなた {0}', '你 {0}', '你 {0}'),
       ('그 뒤 · {0}', 'Afterward · {0}', 'その後 · {0}', '之后 · {0}', '之後 · {0}'),
       ('그 뒤 · 서번트 · {0}', 'Afterward · Servant · {0}', 'その後 · サーヴァント · {0}', '之后 · 从者 · {0}', '之後 · 從者 · {0}'),
       ('그 뒤 · 가까운 사람 · {0}', 'Afterward · Someone close · {0}', 'その後 · 近しい人 · {0}', '之后 · 亲近之人 · {0}', '之後 · 親近之人 · {0}')]
s, nd, _ = i18n.add(s, [(a, b, c) for a, b, c, *_ in D], [(a, b, c) for a, b, c, *_ in TPL])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(HERE, 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _b, _c, d, e in D + TPL:
    if a not in Z: Z[a] = [d, e]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 사전', nd, '· 중국어', n)
