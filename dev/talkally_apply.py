"""11-21: 전투 중 대화로 상대가 무기를 거두었을 때 동맹이 저절로 맺어지지 않게 한다.
상대가 손을 내밀면(관계 70 이상 · 35%) 전투를 닫은 뒤 「동맹 제안」 창을 띄워 받아들일지 고른다.
자동 진행일 때는 거절한다. 사용: python3 talkally_apply.py <game.html>"""
import sys, os, re, json
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
import i18n
P = sys.argv[1]; s = open(P, encoding='utf-8').read()
if 'function talkAllyAsk(' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

OFFER = '…당신이라면 믿어 볼 수 있겠어요. 마지막 둘이 남을 때까지, 손을 잡지 않을래요?'
BODY = '무기를 거둔 상대가 손을 내밀었다. 동맹을 맺을 것인가.'
NO = '상대는 고개를 끄덕이고 물러났다. 다음에 만나면 다시 적이다.'
rp("      if(bd>=70&&!allyBlock()&&e.master&&ch(.35)){ e.ally=true;e.allyDay=W().day; e.known=true; S.flags.allyName=e.mname;allyConfide(e);wrec('ally',`${cn(e)} 조 ${e.mname}${J(e.mname,과)} 동맹`,{p:e.i}); log(`${e.mname}: “…당신이라면 믿어 볼 수 있겠어요. 마지막 둘이 남을 때까지만.”`,'enemy'); log(`${pName(e)} 조와 동맹을 맺었다.`,'war'); }\n      b.res='talk'; return endBattle(); }",
   "      const ask=bd>=70&&!allyBlock()&&e.master&&ch(.35);   // 11-21: 저절로 맺지 않고, 전투를 닫은 뒤 받아들일지 묻는다\n"
   "      if(ask) log(`${e.mname}: “" + OFFER + "”`,'enemy');\n"
   "      b.res='talk'; endBattle(); if(ask&&!w.ended&&!S.dead) w.queue.splice(w.queue.length?1:0,0,()=>talkAllyAsk(e)); return; }")
rp("  const WEAK = {",
   "  function talkAllyAsk(e){ const w=W(); if(!w||w.ended||S.dead||!w.heroAlive||!e.alive||!e.master||e.ally||allyBlock()) return;\n"
   "    decide({title:'동맹 제안',body:'" + BODY + "',war:true,choices:[\n"
   "      {t:'손을 잡는다',f:()=>{ e.ally=true;e.allyDay=w.day; e.known=true; S.flags.allyName=e.mname;allyConfide(e);wrec('ally',`${cn(e)} 조 ${e.mname}${J(e.mname,과)} 동맹`,{p:e.i}); return `${pName(e)} 조와 동맹을 맺었다.`; }},\n"
   "      {t:'거절한다',auto:true,f:()=>'" + NO + "'}]}); }\n"
   "  const WEAK = {")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
D = [(BODY, 'Your opponent, weapon lowered, holds out a hand. Will you form an alliance?', '武器を収めた相手が手を差し出した。同盟を結ぶか。'),
     (OFFER, '…I think I can trust you. Until the last two remain — will you join hands with me?', '…あなたなら信じてみてもいいかも。最後の二組になるまで、手を組みませんか'),
     (NO, 'Your opponent nodded and withdrew. The next time you meet, you will be enemies again.', '相手はうなずいて退いた。次に会えば、また敵同士だ。')]
TP = [('{0}: “' + OFFER + '”', '{0}: “…I think I can trust you. Until the last two remain — will you join hands with me?”', '{0}：「…あなたなら信じてみてもいいかも。最後の二組になるまで、手を組みませんか」')]
s, nd, nt = i18n.add(s, D, TP)
open(P, 'w', encoding='utf-8').write(s)
ZH = {BODY: ['放下武器的对手向你伸出了手。要结成同盟吗？', '放下武器的對手向你伸出了手。要結成同盟嗎？'],
      OFFER: ['……如果是您，我可以试着相信。到最后剩下两组为止，要不要联手？', '……如果是您，我可以試著相信。到最後剩下兩組為止，要不要聯手？'],
      NO: ['对方点了点头，退了下去。下次再见，你们又是敌人了。', '對方點了點頭，退了下去。下次再見，你們又是敵人了。'],
      '{0}: “' + OFFER + '”': ['{0}：“……如果是您，我可以试着相信。到最后剩下两组为止，要不要联手？”', '{0}：「……如果是您，我可以試著相信。到最後剩下兩組為止，要不要聯手？」']}
zp = os.path.join(D0, 'zh', 'done.json'); Z = json.load(open(zp, encoding='utf-8')); n = 0
for k, v in ZH.items():
    if k not in Z: Z[k] = v; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 사전', nd, '· 틀', nt, '· 중국어', n)
