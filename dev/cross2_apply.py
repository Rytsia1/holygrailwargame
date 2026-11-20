"""11-20: 갈림길 61장면 추가 · 한 전쟁 최대 5번(하루 한 번, 65%)
- 장면: cross2_a~d.py (⟦한국어¦영어¦일본어¦간체¦번체⟧)
- 마스터 유형 조건(마술사 · 교회 집안 · 고아 · 가족 · 직업 · 셋집 · 촉매), 나의 성향 변화, 싸움 계열(fight:true)
- 우리를 습격한 조(raidMe) · 우리 서번트를 크게 다치게 한 조(hurtMe) 기록
- 갈림길에서 얻은 기세(오늘)와 원한(그 조 상대, 전쟁 내내)은 결전에는 적용되지 않는다
- 원한을 품은 조가 쓰러지면 한 줄(우리 손 · 다른 손), 빚 갚기 · 마지막 싸움 결과 한 줄
사용: python3 cross2_apply.py <game.html>"""
import sys, os, json
D0 = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D0)
import i18n
from cross2_lib import compile_js
import cross2_a, cross2_b, cross2_c, cross2_d
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if "{id:'x01'" in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

TR = []
EV = compile_js(cross2_a.JS + cross2_b.JS + cross2_c.JS + cross2_d.JS, TR)

rp("  const CROSS=[",
   """  // 11-20: 갈림길 추가 장면용 도구
  const xMage=()=>isMage()&&!S.flags.mundane;
  const xFoes=()=>contracted().filter(p=>!p.ally&&!p.truce);
  const xExp=n=>{ const w=W(); w.exposure=clamp(w.exposure+(n>0?expUp(n):n)); };
  const xBoost=n=>{ const w=W(); if(w.cbstD!==w.day){ w.cbst=0; w.cbstD=w.day; } w.cbst+=n; };
  const xFight=()=>{ const w=W(); w.fightD=w.day; };
  const xPar=()=>!!(S.fam&&((S.fam.father&&S.fam.father.alive)||(S.fam.mother&&S.fam.mother.alive)));
  const xHome=()=>!!(S.fam&&((S.fam.spouse&&S.fam.spouse.alive!==false)||(S.fam.kids&&S.fam.kids.length)));
  const CROSS=[""")
rp("  ];\n  function crossTry(){", EV + "  ];\n  function crossTry(){")
rp("    decide({title:'갈림길',body:d.txt,war:true,choices:chs}); return true; }",
   "    decide({title:'갈림길',body:d.txt,war:true,choices:chs}); return true; }\n  if(typeof globalThis!=='undefined'&&globalThis.__XTEST) globalThis.__XC={CROSS,crossReact};")
rp("(w.crossN||0)>=3||w.day<2||(w.crossD&&w.day-w.crossD<2)||!ch(.45)", "(w.crossN||0)>=5||w.day<2||(w.crossD&&w.day-w.crossD<1)||!ch(.65)")
# 전투 기록: 습격해 온 조 · 서번트를 크게 다치게 한 조
rp("e.fought=true; if(!e.cx) e.met=true; relBattleOpen(ctx);",
   "e.fought=true; if(!e.cx) e.met=true; relBattleOpen(ctx); w.bHp0=w.hp; if(ctx.defend||ctx.ambushed) e.raidMe=w.day;")
rp("function endBattle(){ const w=W(); const b=w.battle; if(b) b.fx=[];",
   """function endBattle(){ const w=W(); const b=w.battle; if(b) b.fx=[];
    if(b&&b.e&&!b.xDone){ b.xDone=1; const e=b.e, won=b.res==='win'||b.res==='fled';
      if(w.heroAlive&&w.hp<(w.bHp0??w.hp)-8) e.hurtMe=w.day;
      if(w.xDebt===e.i){ w.xDebt=null; if(won){ if(e.alive) log('빚은 갚았다. 그 조는 등을 보이고 달아났다.','war'); } else if(w.heroAlive){ lean('avenger',1); log('빚은 갚지 못했다. 그만큼 더 무거워졌다.','war'); } }
      if(w.xLast===e.i){ w.xLast=null; if(won&&w.heroAlive){ w.sm=clamp(w.sm+20); w.hp=clamp(w.hp+8); log('마지막 싸움을 받아 준 서번트가 웃으며 흩어졌다. 그 빛 한 줌이 우리 서번트에게 스며들었다.','war'); } } }""")
# 원한을 품은 조가 쓰러졌을 때
rp("function pairOut(p,why,by,quiet){ const w=S.war; if(!w||p.out) return;",
   """function pairOut(p,why,by,quiet){ const w=S.war; if(!w||p.out) return;
    if(p.xGrudge){ const mine=/^우리 손에/.test(why)||why==='당신과 다시 계약했다', k=p.xGrudge; p.xGrudge=null;
      if(k==='debt'&&w.xDebt===p.i) w.xDebt=null;
      if(mine) log({oath:'가문의 원수가 쓰러졌다. 오래 쥐고 있던 무언가가 손에서 빠져나갔다.',family:'가족을 건드린 조가 끝났다. 경고장을 태웠다.',promise:'유족에게 짧은 소식을 전했다. 전화는 오래 끊기지 않았다.',debt:'빚은 갚았다.'}[k]||'','war');
      else { log({oath:'가문의 원수는 다른 손에 쓰러졌다. 복수는 끝내 내 것이 되지 못했다.',family:'가족을 건드린 조는 다른 손에 끝났다. 쥐었던 주먹을 펼 곳이 없다.',promise:'약속한 복수는 다른 손에 넘어갔다. 유족에게 할 말을 찾지 못했다.',debt:'갚으러 가기 전에, 그 조는 다른 손에 끝났다.'}[k]||'','war'); add({will:k==='oath'?-4:k==='debt'?0:-2}); } }""")
# 갈림길에서 얻은 기세 · 원한: 결전에는 적용하지 않는다
rp("    if(w.boost) p+=w.boost;",
   "    if(w.boost) p+=w.boost;\n    if(!ctx.final){ if(w.cbst&&w.cbstD===w.day) p+=w.cbst; if(ctx.e&&ctx.e.grudge) p+=ctx.e.grudge; }")
rp("if(w.boost) add(M,'기세',w.boost,'오늘 낮의 일로 기세가 올라 있다','오늘');",
   "if(w.boost) add(M,'기세',w.boost,'오늘 낮의 일로 기세가 올라 있다','오늘');\n    if(!c.final){ if(w.cbst&&w.cbstD===w.day) add(M,'다짐',w.cbst,'갈림길에서 내린 결정으로 마음이 단단하다','오늘'); if(e.grudge) add(M,'원한',e.grudge,'이 조에게는 갚을 것이 있다'); }")

if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

TR += [
 ('빚은 갚았다. 그 조는 등을 보이고 달아났다.', 'The debt is paid. That team turned tail and fled.', '借りは返した。その陣営は背を向けて逃げていった。', '这笔账讨回来了。那组转身逃走了。', '這筆帳討回來了。那組轉身逃走了。'),
 ('빚은 갚지 못했다. 그만큼 더 무거워졌다.', 'The debt went unpaid. It weighs all the heavier for it.', '借りは返せなかった。そのぶん重くなった。', '这笔账没能讨回来，反而更沉重了。', '這筆帳沒能討回來，反而更沉重了。'),
 ('마지막 싸움을 받아 준 서번트가 웃으며 흩어졌다. 그 빛 한 줌이 우리 서번트에게 스며들었다.', 'The Servant you gave its last fight faded away smiling. A handful of its light seeped into your own Servant.', '最後の戦いを受けてもらったサーヴァントは、笑って消えていった。その光のひとかけらがこちらのサーヴァントに染み込んだ。', '你成全了最后一战的那位从者笑着消散了。它的一捧光芒渗进了你的从者体内。', '你成全了最後一戰的那位從者笑著消散了。它的一捧光芒滲進了你的從者體內。'),
 ('가문의 원수가 쓰러졌다. 오래 쥐고 있던 무언가가 손에서 빠져나갔다.', "Your family's enemy has fallen. Something you'd been clutching for a long time slipped from your hand.", '家の仇が倒れた。長く握りしめていた何かが手から抜け落ちた。', '家族的仇人倒下了。紧握了许久的某样东西从手中滑落。', '家族的仇人倒下了。緊握了許久的某樣東西從手中滑落。'),
 ('가족을 건드린 조가 끝났다. 경고장을 태웠다.', 'The team that touched your family is finished. You burned the warning note.', '家族に手を出した陣営は終わった。警告状を燃やした。', '伤害你家人的那组完了。你烧掉了那张警告信。', '傷害你家人的那組完了。你燒掉了那張警告信。'),
 ('유족에게 짧은 소식을 전했다. 전화는 오래 끊기지 않았다.', "You sent the bereaved family a short message. The call didn't end for a long time.", '遺族に短い知らせを伝えた。電話はなかなか切れなかった。', '你给家属捎去了简短的消息。电话很久都没有挂断。', '你給家屬捎去了簡短的消息。電話很久都沒有掛斷。'),
 ('빚은 갚았다.', 'The debt is paid.', '借りは返した。', '这笔账讨回来了。', '這筆帳討回來了。'),
 ('가문의 원수는 다른 손에 쓰러졌다. 복수는 끝내 내 것이 되지 못했다.', "Your family's enemy fell by another's hand. The revenge was never yours in the end.", '家の仇は別の手で倒れた。復讐はついに自分のものにならなかった。', '家族的仇人倒在了别人手里。复仇终究没能由自己完成。', '家族的仇人倒在了別人手裡。復仇終究沒能由自己完成。'),
 ('가족을 건드린 조는 다른 손에 끝났다. 쥐었던 주먹을 펼 곳이 없다.', 'The team that touched your family was finished by another hand. Your clenched fist has nowhere to go.', '家族に手を出した陣営は別の手で終わった。握った拳のやり場がない。', '伤害你家人的那组被别人解决了。握紧的拳头无处可落。', '傷害你家人的那組被別人解決了。握緊的拳頭無處可落。'),
 ('약속한 복수는 다른 손에 넘어갔다. 유족에게 할 말을 찾지 못했다.', 'The revenge you promised passed to another hand. You could find nothing to say to the family.', '約束した復讐は別の手に渡った。遺族にかける言葉が見つからなかった。', '答应的复仇落到了别人手中。你找不到话对家属说。', '答應的復仇落到了別人手中。你找不到話對家屬說。'),
 ('갚으러 가기 전에, 그 조는 다른 손에 끝났다.', 'Before you could go pay them back, that team was finished by another hand.', '借りを返しに行く前に、その陣営は別の手で終わった。', '还没等你去讨回来，那组就被别人解决了。', '還沒等你去討回來，那組就被別人解決了。'),
 ('다짐', 'Resolve', '決意', '决心', '決心'),
 ('갈림길에서 내린 결정으로 마음이 단단하다', 'A decision made at a crossroads has steeled your resolve', '岐路での決断で心が固まっている', '在岔路口做出的决定让决心更加坚定', '在岔路口做出的決定讓決心更加堅定'),
 ('원한', 'Grudge', '怨恨', '怨恨', '怨恨'),
 ('이 조에게는 갚을 것이 있다', 'You have a score to settle with this team', 'この陣営には返すべき借りがある', '和这一组还有账要算', '和這一組還有帳要算'),
]
# 같은 한국어가 두 번 나오면 첫 번역을 쓴다
seen = set(); U = []
for t in TR:
    if t[0] in seen: continue
    seen.add(t[0]); U.append(t)
s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, *_ in U], [])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(D0, 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _b, _c, d, e in U:
    if a not in Z: Z[a] = [d, e]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 장면', EV.count("{id:'x"), '· 문장', len(U), '· 사전', nd, '· 중국어', n)
