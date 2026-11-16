"""11-16: 이미 이루어진 소원 — 연애 · 반려를 바라는 서번트와 「연인」이 된 채 성배 앞에서 그 서번트의 소원을 빌면
성배는 아무것도 바꾸지 못한다(소원이 이미 이루어져 있다). 서번트가 그렇게 말하고, 남은 빛으로 이 세계에 남는다(수육).
- 대상: 스즈카 고젠 · 프랑켄슈타인 · 타마모노마에 · 패션립 · 정밀의 하산 · 멜뤼진
- 조건: 관계 사랑 3단계 「연인」(멜뤼진은 우정 3단계 「지기」도), 맑은 성배. 신뢰는 따로 보지 않는다(연인이면 신뢰 60 아래여도 남는다)
- 검은 성배는 지금과 같다. 결과는 수육과 같다(유대 +10 · 수육 에필로그). 기록의 소원: ‘○○의 소원 — 이미 이루어져 있었다’
- 결말 연출 「이미 이루어진 소원」: 「남는다」 장면에 문구만 다르게
사용: python3 lovewish_apply.py <game.html>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'LOVE_WISH' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:80], k)); return
    s = s.replace(o, n)

# (서번트, 한국어 대사, 영어, 일본어, 간체, 번체) — 괄호 안은 지문
LINES = [
 ('suzuka', '…어라? 아무 일도 안 일어나네. 아, 그렇구나. 제대로 된 연애, 이미 하고 있었잖아. 그럼 이 빛은 남는 데 쓸래. 이번 생, 끝까지 해 보고 싶으니까.',
  "…Huh? Nothing's happening. Oh, I get it. A real romance—I was already in one, wasn't I. Then I'll use this light to stay. I wanna see this life through to the end.",
  '…あれ？ 何も起きないじゃん。あ、そっか。ちゃんとした恋愛、もうしてたんだ。じゃあこの光は残るのに使うね。今度の人生、最後までやってみたいし。',
  '……咦？什么都没发生嘛。啊，原来如此。真正的恋爱，我早就在谈了嘛。那这道光就用来留下来吧。这辈子，我想好好走到最后。',
  '……咦？什麼都沒發生嘛。啊，原來如此。真正的戀愛，我早就在談了嘛。那這道光就用來留下來吧。這輩子，我想好好走到最後。'),
 ('frankenstein', '……우. 아무것도, 안 바뀌어. ……반려. 이미, 있어. 여기. ……같이, 남을래.',
  '……Uu. Nothing, changes. ……Companion. Already, have. Here. ……Together, stay.',
  '……ウ。なにも、かわらない。……はんりょ。もう、いる。ここに。……いっしょに、のこる。',
  '……呜。什么，都没变。……伴侣。已经，有了。这里。……一起，留下。',
  '……嗚。什麼，都沒變。……伴侶。已經，有了。這裡。……一起，留下。'),
 ('tamamo', '어머, 성배가 조용하네요. 그럴 수밖에요. 좋은 아내가 되는 소원이라면, 타마모는 매일 아침 이미 이루고 있었는걸요. 그러니 이 빛은 곁에 남는 데 쓸게요, 주인님.',
  "Oh my, the Grail's so quiet. Well, of course it is. If the wish is to be a good wife, Tamamo was already granting it every morning. So I'll use this light to stay by your side, Master.",
  'あら、聖杯が静かですね。それもそのはず。良妻になるという願いなら、タマモは毎朝もう叶えていたんですもの。ですからこの光は、お傍に残るために使いますね、ご主人様。',
  '哎呀，圣杯好安静呢。那也是当然的。若是成为贤妻的愿望，玉藻每天早上都已经在实现了呀。所以这道光，就用来留在您身边吧，主人。',
  '哎呀，聖杯好安靜呢。那也是當然的。若是成為賢妻的願望，玉藻每天早上都已經在實現了呀。所以這道光，就用來留在您身邊吧，主人。'),
 ('passionlip', '…아무 일도 안 일어났어요. 그야… 벌써 안아 봤으니까요. 다치게 하지 않고. …그러니까, 남은 건 곁에 있는 데 쓰고 싶어요.',
  "…Nothing happened. Well… I've already held you, after all. Without hurting you. …So I want to use what's left to stay by your side.",
  '…何も起きませんでした。だって…もう抱きしめましたから。傷つけずに。…だから、残りはそばにいるために使いたいです。',
  '……什么都没有发生。毕竟……我已经抱过了嘛。没有弄伤你。……所以，剩下的，我想用来待在你身边。',
  '……什麼都沒有發生。畢竟……我已經抱過了嘛。沒有弄傷你。……所以，剩下的，我想用來待在你身邊。'),
 ('serenity', '…성배가 아무것도 하지 않네요. 당연해요. 저는 이미 닿아 있으니까요. 이 손으로, 당신에게. …남게 해 주세요. 그 온기를 조금 더 오래 느끼고 싶어요.',
  "…The Grail isn't doing anything. Of course not. I'm already touching someone. With this hand—you. …Let me stay. I want to feel that warmth a little longer.",
  '…聖杯は何もしませんね。当然です。私はもう触れているのですから。この手で、あなたに。…残らせてください。そのぬくもりを、もう少し長く感じていたいんです。',
  '……圣杯什么也没做呢。这是当然的。因为我已经触碰到了。用这双手，触碰到了你。……请让我留下。我想再久一点感受那份温暖。',
  '……聖杯什麼也沒做呢。這是當然的。因為我已經觸碰到了。用這雙手，觸碰到了你。……請讓我留下。我想再久一點感受那份溫暖。'),
 ('melusine', '아무것도 바뀌지 않았네. 응, 알아. 내가 지켜보고 싶은 빛은 이미 여기 있으니까. 그러니 이 빛은 남는 데 쓸게. 끝까지 보려면 곁에 있어야 하잖아.',
  "Nothing changed. Yeah, I know. The light I want to watch over is already right here. So I'll use this light to stay. To see it through to the end, I have to be beside it.",
  '何も変わらなかったね。うん、わかってる。私が見守りたい光は、もうここにあるから。だからこの光は残るために使う。最後まで見るには、そばにいなきゃでしょ。',
  '什么都没变呢。嗯，我知道。我想守望的光，已经在这里了。所以这道光，我就用来留下。想看到最后，就得待在身边才行吧。',
  '什麼都沒變呢。嗯，我知道。我想守望的光，已經在這裡了。所以這道光，我就用來留下。想看到最後，就得待在身邊才行吧。'),
]
PRE = {'frankenstein': '(그녀는 성배와 당신을 번갈아 보았다.) '}
# 문장 (한국어, 영어, 일본어, 간체, 번체)
D = [
 ('그녀는 성배와 당신을 번갈아 보았다.', 'She looked from the Grail to you and back.', '彼女は聖杯とあなたを交互に見た。', '她来回看着圣杯和你。', '她來回看著聖杯和你。'),
 ('이미 이루어져 있었다', 'It had already come true', 'すでに叶っていた', '早已实现', '早已實現'),
 ('소원은 이미 이루어져 있었다.', 'The wish had already come true.', '願いはすでに叶っていた。', '愿望早已实现。', '願望早已實現。'),
 ('남은 빛은 곁에 남는 데 쓰였다.', 'The remaining light was spent on staying by your side.', '残った光は、そばに残るために使われた。', '剩下的光芒，化作了留在身边的力量。', '剩下的光芒，化作了留在身邊的力量。'),
]
T = [
 ('성배가 빛났다. 빛은 {0}에게 모여들었다가, 아무것도 바꾸지 못하고 그 둘레를 맴돌았다.',
  'The Grail shone. The light gathered around {0}, then only circled there, unable to change anything.',
  '聖杯が輝いた。光は{0}のもとへ集まり、何も変えられないまま、そのまわりを巡った。',
  '圣杯亮了起来。光芒聚向{0}，却什么也没能改变，只在其周围盘旋。',
  '聖杯亮了起來。光芒聚向{0}，卻什麼也沒能改變，只在其周圍盤旋。'),
 ('소원은 이미 이루어져 있었다. 남은 빛이 {0}에게 스며들었다. 다음 날 아침, {1}는 처음으로 배가 고프다고 했다.',
  'The wish had already come true. The remaining light seeped into {0}. The next morning, {1:he} said for the first time that {1:he} was hungry.',
  '願いはすでに叶っていた。残った光が{0}に染み込んだ。翌朝、{1}は初めてお腹が空いたと言った。',
  '愿望早已实现。剩下的光芒渗入了{0}体内。第二天早上，{1:he}第一次说肚子饿了。',
  '願望早已實現。剩下的光芒滲入了{0}體內。第二天早上，{1:he}第一次說肚子餓了。'),
]

# ---- 엔진 ----
LW = '{' + ','.join(f'{i}:{json.dumps(PRE.get(i, "") + ko, ensure_ascii=False)}' for i, ko, *_ in LINES) + '}'
rp("  function grantHero(shared){\n    const w=W(),h=hero(), pure=w.cupPure;\n",
   "  // 이미 이루어진 소원: 연애 · 반려를 바라는 서번트와 「연인」(멜뤼진은 「지기」도)이면, 맑은 성배는 아무것도 바꾸지 못하고 서번트가 남는다\n"
   "  const LOVE_WISH=" + LW + ";\n"
   "  function loveWishOK(h){ if(!h||!LOVE_WISH[h.id]) return false; const r=relOf(); return !!r&&r.stage>=3&&(r.track==='love'||h.id==='melusine'); }\n"
   "  function grantHero(shared){\n    const w=W(),h=hero(), pure=w.cupPure;\n"
   "    if(pure&&loveWishOK(h)){\n"
   "      log(`성배가 빛났다. 빛은 ${h.name}에게 모여들었다가, 아무것도 바꾸지 못하고 그 둘레를 맴돌았다.`,'voice');\n"
   "      log(voiceLine(h,LOVE_WISH[h.id]),'voice');\n"
   "      log(`소원은 이미 이루어져 있었다. 남은 빛이 ${h.name}에게 스며들었다. 다음 날 아침, ${he(h)}는 처음으로 배가 고프다고 했다.`,'joy');\n"
   "      add({bond:10}); S.flags.stay=h.id; S.flags.loveWish=1; S.flags.wishText=`${h.name}의 소원 — 이미 이루어져 있었다`;\n"
   "      S.flags.endFx='loveWish'; S.flags.endWish=h.wish;\n"
   "      sharedOut(shared); warOver(); return;\n"
   "    }\n")
rp("const END_N={wish:'wish',heroWish:'heroWish',stay:'stay',", "const END_N={wish:'wish',heroWish:'heroWish',stay:'stay',loveWish:'loveWish',")
rp("  SCN.stay={HOLD:7.6,init(){",
   "  // 이미 이루어진 소원: 「남는다」 장면을 그대로 쓰고 문구만 바꾼다\n"
   "  SCN.loveWish={HOLD:7.6,init(){ setWish(''); setText(`${opt.hero}의 소원`,'소원은 이미 이루어져 있었다.','남은 빛은 곁에 남는 데 쓰였다.'); OUT=99; const R=rng(19); this.M=[...Array(70)].map(()=>({a:R()*Math.PI*2,d:.3+R()*.9,v:.4+R()*.8,r:.8+R()*1.8,vy:0,y:null,x:null})); },\n"
   "   frame(t,dt){ return SCN.stay.frame.call(this,t,dt); }};\n"
   "  SCN.stay={HOLD:7.6,init(){")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

# ---- 번역: 영어 · 일본어는 게임 사전, 중국어는 dev/zh/done.json ----
s, nd, nt = i18n.add(s, dict_items=[(ko, en, ja) for _, ko, en, ja, *_ in LINES] + [(a, b, c) for a, b, c, *_ in D],
                     tpl_items=[(a, b, c) for a, b, c, *_ in T])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
if os.path.exists(zp):
    Z = json.load(open(zp, encoding='utf-8')); n = 0
    for row in [(ko, zs, zt) for _, ko, _e, _j, zs, zt in LINES] + [(a, d, e) for a, _b, _c, d, e in D] + [(a, d, e) for a, _b, _c, d, e in T]:
        if row[0] not in Z: Z[row[0]] = [row[1], row[2]]; n += 1
    json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('중국어 사전', n)
print('적용 끝 · 사전', nd, '틀', nt)
