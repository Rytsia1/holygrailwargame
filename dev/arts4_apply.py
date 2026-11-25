"""4 New Magic Learned Arts patch script (arts41125).
Usage: python3 arts4_apply.py <game.html>
"""
import sys, os, json, re, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'arts41125' in s:
    print('이미 적용됨')
    sys.exit(0)

miss = []
def rp(o, n):
    global s
    k = s.count(o)
    if k != 1:
        miss.append((o[:90], k))
        return
    s = s.replace(o, n)

# 1. ARTS, KIT_SIGN, ART_CHAIN, ART_UP, ART_AFF, ART_INFO, ART_ACT
rp(
"    alchemy:{n:'연금술',br:'magic'}, familiar:{n:'사역마 마술',br:'magic'}, necro:{n:'강령술',br:'magic'}, puppet:{n:'인형술',br:'magic'}, astro:{n:'점성술',br:'magic'},",
"    alchemy:{n:'연금술',br:'magic'}, familiar:{n:'사역마 마술',br:'magic'}, necro:{n:'강령술',br:'magic'}, puppet:{n:'인형술',br:'magic'}, astro:{n:'점성술',br:'magic'},\n    projection:{n:'투영 마술',br:'magic'}, evocation:{n:'영매 마술',br:'magic'}, illusion_art:{n:'환술',br:'magic'}, displacement:{n:'치환 마술',br:'magic'}, /* arts41125 */"
)
rp(
"    enhance:n=>`${n}의 몸놀림이 사람의 것이 아니었다. 강화 마술이다.`,\n  };",
"""    enhance:n=>`${n}의 몸놀림이 사람의 것이 아니었다. 강화 마술이다.`,
    projection:n=>`${n}의 손안에서 마력으로 빚은 칼날이 형체를 갖추었다. 투영 마술이다.`,
    evocation:n=>`${n}의 주위로 낯선 영기가 겹쳐졌다. 영매 마술이다.`,
    illusion_art:n=>`${n}의 그림자가 둘, 셋으로 갈라졌다. 환술이다.`,
    displacement:n=>`발밑의 돌과 칼날이 눈 깜짝할 새 자리를 바꿨다. 치환 마술이다.`,
  };"""
)
rp(
"      3:['한 사람의 별을 끝까지 읽어 냈다. 그 사람의 운명이 언제 꺾이는지 보였다.']}},\n  };",
"""      3:['한 사람의 별을 끝까지 읽어 냈다. 그 사람의 운명이 언제 꺾이는지 보였다.']}},
    projection:{st:'mana',max:3,ev:{
      1:['빈 손바닥 위에 낡은 나이프의 구조를 떠올렸다. 마력이 뭉치며 차가운 칼자루가 손에 쥐어졌다. 몇 분 뒤 연기로 흩어졌다.','투영은 헛수고라고 스승은 말했다. 그래도 구조를 이해한 물건이라면 마력으로 잠시 불러낼 수 있었다.'],
      2:['금속의 결을 속속들이 읽어 내는 감각이 붙었다. 투영한 무구가 웬만한 충격에도 쉽게 부서지지 않게 되었다.','전투에 쓸 도구와 칼날을 머릿속 서고에 정리해 두었다. 필요한 순간 바로 손에 쥘 수 있다.'],
      3:['눈으로 본 무구의 역사와 성질까지 함께 엮어 냈다. 잠시뿐이지만 진짜에 가까운 일격을 담을 수 있다.','손끝에서 빚어낸 무구가 푸른 불꽃을 머금었다. 허상이 현실을 잠시 덮어쓸 만큼 단단했다.']}},
    evocation:{st:'will',max:3,ev:{
      1:['오래된 사당 뒤편에서 바람 소리 사이에 섞인 목소리를 들었다. 쫓아내는 대신 귀를 기울이자 영체가 응답했다.','빈 방에 향을 피우고 의식을 가라앉혔다. 보이지 않던 기척 하나가 촛불을 흔들며 인사를 건넸다.'],
      2:['불러낸 영체를 잠시 몸에 겹쳐 두는 법을 익혔다. 숨결이 차가워졌지만 감각과 몸놀림이 한층 예리해졌다.','주변에 머무는 영들과 짧은 계약을 맺었다. 밤마다 낯선 기척이 다가오면 가장 먼저 알려 준다.'],
      3:['깊은 빙의로 영체의 힘을 온전히 끌어다 쓸 수 있게 되었다. 영령의 곁에 서도 밀리지 않을 만큼 영기가 짙어졌다.','어둠 속에서 수많은 영들이 부름에 답했다. 그 힘을 흘려 보내 서번트의 윤곽까지 떠받칠 수 있었다.']}},
    illusion_art:{st:'lore',max:3,ev:{
      1:['거울 앞에서 빛의 굴절과 시선의 빈틈을 맞추어 보았다. 손에 든 동전이 보는 사람의 눈에서만 감쪽같이 사라졌다.','환술은 물건을 바꾸는 것이 아니라 보는 쪽의 인식을 비트는 술식이었다. 골목 끝 그림자를 사람처럼 세워 보았다.'],
      2:['소리와 기척까지 엮은 입체 환영을 만들었다. 지나가던 개조차 빈 공터를 향해 한참이나 짖었다.','거처 근처에 가짜 기척을 흘려 두는 법을 익혔다. 진짜 위치는 한 겹 더 깊은 어둠 속에 감출 수 있다.'],
      3:['전장의 거리감과 시야를 통째로 비틀어 놓을 수 있게 되었다. 상대는 늘 반 박자 늦게 허공을 베게 된다.','거짓 표적과 진짜 공격이 한꺼번에 겹쳐진다. 눈에 보이는 것을 믿는 한 빠져나올 길이 없다.']}},
    displacement:{st:'lore',max:3,ev:{
      1:['책상 위의 동전과 창가의 지우개를 마력으로 이었다. 손가락을 튕기자 둘의 자리가 소리 없이 바뀌었다.','치환은 공간을 접어 두 대상의 좌표를 맞바꾸는 술식이었다. 무게가 비슷할수록 마력이 덜 들었다.'],
      2:['움직이는 표적과 미리 표식을 새긴 물체의 자리를 맞바꿀 수 있게 되었다. 함정을 피하고 되돌려 주는 데 이보다 좋은 수는 없었다.','밤길에 날아온 돌멩이를 발밑의 낙엽과 맞바꾸었다. 찰나의 타이밍이 몸에 익기 시작했다.'],
      3:['적의 공격이 닿는 순간 궤도째 위치를 뒤바꾸는 치환 반격을 완성했다. 적의 힘은 고스란히 준비된 함정으로 향한다.','전장의 모든 사물이 좌표로 읽히기 시작했다. 어디에 서 있든 한 걸음 앞서 자리를 바꿀 수 있다.']}},
  };"""
)

rp(
"astro:{lore:1}};",
"astro:{lore:1},projection:{mana:1,lore:1},evocation:{will:2},illusion_art:{lore:1,will:1},displacement:{lore:2}};"
)
rp(
"  const ART_AFF={judge:{barrier:1.5,heal:1.5,curse:.5,baptism:1.5,necro:.5},avenger:{curse:1.5,element:1.5,heal:.5},cruel:{curse:1.5,heal:.5,necro:1.5},taboo:{necro:2,puppet:2,mind:1.5,baptism:.5},zeal:{elementHi:1.5,alchemy:1.5,astro:1.5}};",
"  const ART_AFF={judge:{barrier:1.5,heal:1.5,curse:.5,baptism:1.5,necro:.5,projection:1.3},avenger:{curse:1.5,element:1.5,heal:.5,illusion_art:1.3},cruel:{curse:1.5,heal:.5,necro:1.5,illusion_art:1.3},taboo:{necro:2,puppet:2,mind:1.5,baptism:.5,evocation:1.5},zeal:{elementHi:1.5,alchemy:1.5,astro:1.5,projection:1.4,displacement:1.4}};"
)
rp(
"    exorcism:{1:[...BODY_G,'맞대결에서 ‘퇴마의 칼’로 맞설 수 있다 · 사도와 사령에게 더 강하다'],2:BODY_UP},\n  };",
"""    exorcism:{1:[...BODY_G,'맞대결에서 ‘퇴마의 칼’로 맞설 수 있다 · 사도와 사령에게 더 강하다'],2:BODY_UP},
    projection:{1:['전투 지원 ‘무구 투영’과 ‘강화 마술’을 쓸 수 있다','맞대결에서 임시 무구를 투영해 힘을 보탠다'],2:['‘무구 투영’의 위력과 피해가 늘어난다','맞대결에서 임시 무구를 투영해 힘을 보탠다'],3:['‘무구 투영’이 두 합 동안 유지되고 크게 강해진다']},
    evocation:{1:['전투 지원 ‘영령 빙의’와 ‘강화·방해 마술’을 쓸 수 있다','전투에 들어서며 주변 영체에게서 상대 정보를 듣는다'],2:['영체가 거처를 지켜 기습과 암습을 먼저 알린다','‘영령 빙의’의 방어와 전투력이 더 강해진다'],3:['‘영령 빙의’가 서번트의 마력까지 채워 주고 크게 강해진다']},
    illusion_art:{1:['전투 지원 ‘환영 미끼’와 ‘방해 마술’을 쓸 수 있다','노출이 덜 쌓이고 선제 기습과 잠입이 유리해진다'],2:['거처에 환영 미끼를 깔아 밤 습격을 흘려보낼 수 있다','‘환영 미끼’가 더 강해지고 맞대결 교란에 힘이 실린다'],3:['‘환영 미끼’가 두 합 동안 유지되고 기습 보정이 크게 오른다']},
    displacement:{1:['전투 지원 ‘치환 반격’과 ‘엄호 결계’를 쓸 수 있다','적의 함정으로 받는 불이익을 줄인다'],2:['암습을 받으면 ‘치환으로 자리를 바꾼다’로 반격할 수 있다 · 전쟁에서 한 번','함정의 불이익을 완전히 벗어 던지고 ‘치환 반격’이 강해진다'],3:['‘치환 반격’의 피해 경감과 반격 위력이 크게 강해진다']},
  };"""
)
rp(
"  const ART_ACT={mind:['hex'],element:['buff'],enhance:['buff'],jewel:['buff'],curse:['hex'],necro:['hex'],astro:['hex'],familiar:['hex'],barrier:['ward'],puppet:['ward'],rune:['ward','heal'],heal:['heal'],alchemy:['heal']};",
"  const ART_ACT={mind:['hex'],element:['buff'],enhance:['buff'],jewel:['buff'],curse:['hex'],necro:['hex'],astro:['hex'],familiar:['hex'],barrier:['ward'],puppet:['ward'],rune:['ward','heal'],heal:['heal'],alchemy:['heal'],projection:['buff'],evocation:['buff','hex'],illusion_art:['hex'],displacement:['ward','hex']};"
)

# 2. Final Duel tables (DUEL_STR/AGI/MAG/BK/BKN, duelMaster, duelRound, duelClash)
rp(
"  const DUEL_STR={bajiquan:1,sword:1,agent:1,exorcism:1,anshou:.5,gunfight:.5}, DUEL_AGI={anshou:1,gunfight:1,agent:1,bajiquan:.5,exorcism:.5,sword:.5}, DUEL_MAG={element:1,curse:1,jewel:1,rune:1,necro:1};",
"  const DUEL_STR={bajiquan:1,sword:1,agent:1,exorcism:1,anshou:.5,gunfight:.5,projection:.5}, DUEL_AGI={anshou:1,gunfight:1,agent:1,bajiquan:.5,exorcism:.5,sword:.5,illusion_art:.5,displacement:.5}, DUEL_MAG={element:1,curse:1,jewel:1,rune:1,necro:1,projection:.5,evocation:.8,displacement:.5};"
)
rp(
"  const DUEL_BK={element:{g:'atk',d:18,mr:1},jewel:{g:'atk',d:22,mr:1,w:10},body:{g:'atk',d:18,mr:0,ev:1},holy:{g:'atk',d:14,mr:1,av:1},rune:{g:'atk',d:18,mr:1},\n    curse:{g:'hex'},mind:{g:'hex'},necro:{g:'hex'},astro:{g:'hex'},familiar:{g:'hex'},barrier:{g:'wall'},puppet:{g:'wall'},heal:{g:'heal'},alchemy:{g:'heal'}};",
"  const DUEL_BK={element:{g:'atk',d:18,mr:1},jewel:{g:'atk',d:22,mr:1,w:10},body:{g:'atk',d:18,mr:0,ev:1},holy:{g:'atk',d:14,mr:1,av:1},rune:{g:'atk',d:18,mr:1},\n    curse:{g:'hex'},mind:{g:'hex'},necro:{g:'hex'},astro:{g:'hex'},familiar:{g:'hex'},barrier:{g:'wall'},puppet:{g:'wall'},heal:{g:'heal'},alchemy:{g:'heal'},\n    projection:{g:'atk',d:20,mr:0,ev:1},evocation:{g:'atk',d:19,mr:1,av:1},illusion_art:{g:'hex'},displacement:{g:'wall'}};"
)
rp(
"  const DUEL_BKN={element:'원소 마술 비기',jewel:'보석 마술 비기',body:'몸의 비기',holy:'성언의 비기',rune:'룬 마술 비기',curse:'저주의 비기',mind:'정신 간섭 비기',necro:'강령술 비기',astro:'점성술 비기',familiar:'사역마 비기',barrier:'결계 마술 비기',puppet:'인형술 비기',heal:'치유 마술 비기',alchemy:'연금술 비기'};",
"  const DUEL_BKN={element:'원소 마술 비기',jewel:'보석 마술 비기',body:'몸의 비기',holy:'성언의 비기',rune:'룬 마술 비기',curse:'저주의 비기',mind:'정신 간섭 비기',necro:'강령술 비기',astro:'점성술 비기',familiar:'사역마 비기',barrier:'결계 마술 비기',puppet:'인형술 비기',heal:'치유 마술 비기',alchemy:'연금술 비기',projection:'투영 마술 비기',evocation:'영매 마술 비기',illusion_art:'환술 비기',displacement:'치환 마술 비기'};"
)
rp(
"    const ml=Math.max(0,...MARTIAL.map(lv)), dur=1+ml*.5+(lv('enhance')+lv('barrier'))/2+(A.regen?1:0);",
"    const ml=Math.max(0,...MARTIAL.map(lv)), dur=1+ml*.5+(lv('enhance')+lv('barrier'))/2+lv('evocation')*.35+(A.regen?1:0);"
)
rp(
"        if(artLv('baptism')) one('bapt','세례영창','이번 합 서번트 전투력이 떨어진다 · 어벤저에게는 두 배 · 대마력이면 절반 · 결투에서 한 번',25,!D.used.bapt,()=>{ D.used.bapt=1; const lv=artLv('baptism'); let v=[0,4,6,8][Math.min(3,lv)]*(lv>=2?artQ('baptism'):1); if(h.cls==='avenger') v*=2; if(mr) v/=2; D.pre={...(D.pre||{}),deb:Math.round(v)}; }); }",
"""        if(artLv('baptism')) one('bapt','세례영창','이번 합 서번트 전투력이 떨어진다 · 어벤저에게는 두 배 · 대마력이면 절반 · 결투에서 한 번',25,!D.used.bapt,()=>{ D.used.bapt=1; const lv=artLv('baptism'); let v=[0,4,6,8][Math.min(3,lv)]*(lv>=2?artQ('baptism'):1); if(h.cls==='avenger') v*=2; if(mr) v/=2; D.pre={...(D.pre||{}),deb:Math.round(v)}; });
        if(artLv('projection')) one('proj','무구 투영','마력으로 임시 무구와 도구를 투영한다',20,true,()=>{ const lv=artLv('projection'); D.pre={...(D.pre||{}),pow:(D.pre&&D.pre.pow||0)+Math.round((5+lv*3)*(lv>=2?artQ('projection'):1))}; });
        if(artLv('evocation')) one('evoke','영령 빙의','영체를 불러내 빙의하여 전투력과 수비를 끌어올린다 · 결투에서 한 번',25,!D.used.evoke,()=>{ D.used.evoke=1; const lv=artLv('evocation'); D.pre={...(D.pre||{}),pow:(D.pre&&D.pre.pow||0)+Math.round((5+lv*3)*(lv>=2?artQ('evocation'):1)),guard:Math.max(D.pre&&D.pre.guard||0,lv>=2?.2:.12)}; });
        if(artLv('illusion_art')) one('mirage','환영 미끼','환영 미끼를 세워 적의 시야를 어지럽히고 회피를 높인다',20,true,()=>{ const lv=artLv('illusion_art'); D.artIll={until:D.r+(lv>=3?1:0),v:Math.min(.32,.1+lv*.06*(lv>=2?artQ('illusion_art'):1))}; D.pre={...(D.pre||{}),reroll:true,deb:(D.pre&&D.pre.deb||0)+Math.round((4+lv*2)*(lv>=2?artQ('illusion_art'):1))}; });
        if(artLv('displacement')) one('swap','치환 반격','대상과 물체의 위치를 치환해 피해를 줄이고 반격한다',25,true,()=>{ const lv=artLv('displacement'); D.pre={...(D.pre||{}),guard:Math.max(D.pre&&D.pre.guard||0,Math.min(.42,.14+lv*.08)),dispSwap:Math.round((6+lv*3)*(lv>=2?artQ('displacement'):1))}; }); }"""
)
rp(
"      else { const _dIl=D.eyeIll&&D.eyeIll.until>=D.r; if(ch((dodgeP(M.P[1],h.s[1])+(_dIl?D.eyeIll.v*.45:0))*(sk==='magic'?MG.dodge:1))||(_dIl&&ch(D.eyeIll.v))){ D.shp-=ri(1,3); log(`${n}의 일격을 간신히 피했다.`,'war'); }",
"      else { const _dIl=D.eyeIll&&D.eyeIll.until>=D.r, _dAI=D.artIll&&D.artIll.until>=D.r, _iv=Math.max(_dIl?D.eyeIll.v:0,_dAI?D.artIll.v:0); if(ch((dodgeP(M.P[1],h.s[1])+_iv*.45)*(sk==='magic'?MG.dodge:1))||(_iv>0&&ch(_iv))){ D.shp-=ri(1,3); log(`${n}의 일격을 간신히 피했다.`,'war'); }"
)
rp(
"    if(wallOn&&!np&&!talk&&!isBk) log('✓ 결계 — 서번트의 칼이 닿지 않았다','check');",
"    if(wallOn&&!np&&!talk&&!isBk) log('✓ 결계 — 서번트의 칼이 닿지 않았다','check');\n    if(P0.dispSwap&&!talk&&!isBk&&(d<=-8||D.mhp<b0.mhp)){ D.shp-=P0.dispSwap; log(`치환 마술이 발동했다! ${n}의 공격 궤도가 뒤틀리며 되려 준비된 함정에 꽂혔다.`,'war'); }"
)

# 3. Strategic War Passives (expUp, myPower trap, infilD, initB, scout, threat, pastSee, famGuard, WAR_EV ambush)
rp(
"  const expUp=v=>{ let x=v; if(S.hero==='lancelot'&&x>0) x=Math.round(x*.75); if(x>0&&giftIs('illusion')) x=Math.max(1,Math.round(x*Math.max(.55,1-.08*giftF()))); return x; };",
"  const expUp=v=>{ let x=v; if(S.hero==='lancelot'&&x>0) x=Math.round(x*.75); if(x>0&&giftIs('illusion')) x=Math.max(1,Math.round(x*Math.max(.55,1-.08*giftF()))); if(x>0&&artLv('illusion_art')>=1) x=Math.max(1,Math.round(x*Math.max(.65,1-artLv('illusion_art')*.08))); return x; };"
)
rp(
"    if(ctx.defend) p+=5*wsF()*fortRead(ctx.e)*(ctx.breach?.5:1); if(ctx.trap) p-=8;",
"    if(ctx.defend) p+=5*wsF()*fortRead(ctx.e)*(ctx.breach?.5:1); if(ctx.trap){ const _dl=artLv('displacement'); p-=_dl>=2?0:_dl===1?4:8; }"
)
rp(
"  function infilD(e,est){ const h=hero(),P=myP();\n    return (P[1]*2+SV(h,'stealth')*1.5+P[4]*1.5+(e.intel||0)*.12+8)-(10+(est?6:asnFoe(e,'night'))+(e.cls==='caster'?8:0)+(e.workshop?6:0)+((e.plan&&e.plan.fort)?Math.round(e.plan.fort*.1):0)-(e.hp<40?4:0)+asnAlert(e)*5); }",
"  function infilD(e,est){ const h=hero(),P=myP();\n    return (P[1]*2+SV(h,'stealth')*1.5+P[4]*1.5+(e.intel||0)*.12+8+artLv('illusion_art')*4)-(10+(est?6:asnFoe(e,'night'))+(e.cls==='caster'?8:0)+(e.workshop?6:0)+((e.plan&&e.plan.fort)?Math.round(e.plan.fort*.1):0)-(e.hp<40?4:0)+asnAlert(e)*5); }"
)
rp(
"  function initB(b){ const c=b.ctx; return c.attack&&!c.final&&!c.claim&&!c.raid? (b.round===1?10:b.round===2?5:0) : 0; }",
"  function initB(b){ const c=b.ctx; if(!(c.attack&&!c.final&&!c.claim&&!c.raid)) return 0; const il=artLv('illusion_art'); return (b.round===1?10+il*3:b.round===2?5+il*2:0); }"
)
rp(
"    const _ambP=(.16+(t.tac==='hunter'?.1:0))*(giftIs('clairvoyance')?Math.max(.2,1-.18*giftF()):1)*(giftIs('illusion')?.75:1);",
"    const _ambP=(.16+(t.tac==='hunter'?.1:0))*(giftIs('clairvoyance')?Math.max(.2,1-.18*giftF()):1)*(giftIs('illusion')?.75:1)*Math.max(.5,1-artLv('illusion_art')*.15);"
)
rp(
"  function pastSee(e){ if(!e||e.pastSeen||e.cx) return; const g=giftIs('past')?giftF():0, n=artLv('necro'); if(!g&&!n) return; e.pastSeen=true; addIntel(e,Math.round(6+g*4+n*4),'sight'); log(g?`${pName(e)} 조가 걸어온 길이 눈앞에 겹쳐 보였다. 과거시의 마안이다.`:`떠도는 영들이 ${pName(e)} 조에 대해 수군거렸다.`,'war'); }",
"  function pastSee(e){ if(!e||e.pastSeen||e.cx) return; const g=giftIs('past')?giftF():0, n=artLv('necro'), ev=artLv('evocation'); if(!g&&!n&&!ev) return; e.pastSeen=true; addIntel(e,Math.round(6+g*4+n*4+ev*3),'sight'); log(g?`${pName(e)} 조가 걸어온 길이 눈앞에 겹쳐 보였다. 과거시의 마안이다.`:ev&&!n?`부름에 응한 영체가 ${pName(e)} 조의 기척을 속삭여 주었다.`:`떠도는 영들이 ${pName(e)} 조에 대해 수군거렸다.`,'war'); }"
)
rp(
"    if(artLv('necro')>=2||artLv('astro')>=2){ w.famWarn=w.day; e.scoutEdge=0; log(artLv('necro')>=2?'거처를 떠돌던 사령이 먼저 기척을 알렸다. 기습은 헛돌았다.':'별이 오늘 밤의 습격을 일러 주었다. 기습은 헛돌았다.','war'); } }",
"    if(artLv('necro')>=2||artLv('astro')>=2||artLv('evocation')>=2){ w.famWarn=w.day; e.scoutEdge=0; log(artLv('evocation')>=2?'부름에 답한 수호 영체가 먼저 기척을 알렸다. 기습은 헛돌았다.':artLv('necro')>=2?'거처를 떠돌던 사령이 먼저 기척을 알렸다. 기습은 헛돌았다.':'별이 오늘 밤의 습격을 일러 주었다. 기습은 헛돌았다.','war'); } }"
)
rp(
"    const P=.13+w.exposure*.003+w.day*.011-(w.hid?.12:0)-Math.min(w.fort,SIEGE_FORT)*.0015+(w.seals===0?.08:0)-SV(hero(),'stealth')*.012+(foes.some(p=>p.provoked>0)?.12:0)+(w.hunted?.08:0)+(w.altarPre&&!w.altarDone?.06:0);",
"    const P=.13+w.exposure*.003+w.day*.011-(w.hid?.12:0)-Math.min(w.fort,SIEGE_FORT)*.0015+(w.seals===0?.08:0)-SV(hero(),'stealth')*.012-artLv('illusion_art')*.03+(foes.some(p=>p.provoked>0)?.12:0)+(w.hunted?.08:0)+(w.altarPre&&!w.altarDone?.06:0);"
)
rp(
"    if(giftIs('illusion')&&!e.cx&&ch(Math.min(.42,.12+giftF()*.05))){",
"    if(artLv('illusion_art')>=2&&!e.cx&&ch(artLv('illusion_art')*.1)){ log(`환술로 꾸며 둔 가짜 거처가 ${pName(e)} 조의 눈길을 끌었다. 적은 빈 건물만 부수고 돌아갔다.`,'war'); return; }\n    if(giftIs('illusion')&&!e.cx&&ch(Math.min(.42,.12+giftF()*.05))){"
)
rp(
"      const E=npcParams(p).p.map(PV), off=Math.max(-10,Math.min(12,asnAtk(th,E)-22))*1.5, det=asnSk(h,'battle',true)*1.5+(famWatch()?6:0)+(giftIs('future')?8:0)+(artLv('astro')>=2||artLv('necro')>=2?4:0), cut=(lo,hi)=>Math.max(6,ri(lo,hi)+Math.round(asnStrike(E)-9.5));",
"      const E=npcParams(p).p.map(PV), off=Math.max(-10,Math.min(12,asnAtk(th,E)-22))*1.5, det=asnSk(h,'battle',true)*1.5+(famWatch()?6:0)+(giftIs('future')?8:0)+(artLv('astro')>=2||artLv('necro')>=2||artLv('evocation')>=2?5:0), cut=(lo,hi)=>Math.max(6,ri(lo,hi)+Math.round(asnStrike(E)-9.5));"
)
rp(
"        ...(artLv('puppet')>=2&&!w.puppetUsed?[{t:'대역 인형을 내세운다',d:'인형술 · 전쟁에서 한 번',f:()=>{ w.puppetUsed=true; addIntel(p,15,'raid'); return '칼날이 꽂힌 것은 당신을 닮은 인형이었다. 그림자는 속았다는 것을 알고 물러났다.'; }}]:[]),",
"        ...(artLv('puppet')>=2&&!w.puppetUsed?[{t:'대역 인형을 내세운다',d:'인형술 · 전쟁에서 한 번',f:()=>{ w.puppetUsed=true; addIntel(p,15,'raid'); return '칼날이 꽂힌 것은 당신을 닮은 인형이었다. 그림자는 속았다는 것을 알고 물러났다.'; }}]:[]),\n        ...(artLv('displacement')>=2&&!w.dispUsed?[{t:'치환으로 자리를 바꾼다',d:'치환 마술 · 전쟁에서 한 번 · 반격',f:()=>{ w.dispUsed=true; p.hp=clamp(p.hp-12); addIntel(p,20,'raid'); return '찰나의 치환으로 침대 위 장식과 자리를 맞바꾸었다. 칼날이 부서지며 어새신이 반동으로 상처를 입고 물러났다.'; }}]:[]),"
)

# 4. Master Duel (myMDScore), Battle Support (MACT, MACT_UI, ACT_SRC, artRatio, masterChoices, mAct, mBon/eMal, battleMods, clash)
rp(
"    if(m.mg) return masterScore()*.8+(st[m.st]-50)*.2+(k==='atkM'?artDuel('element'):k==='defM'?artDuel('barrier'):k==='trkM'?Math.max(artDuel('curse'),artDuel('mind'),artDuel('astro')):0)+giftDuel(k);\n    return 30+(st[m.a]-50)*.3+(st[m.b]-50)*.15+mdMartial(k)+giftDuel(k); }",
"    if(m.mg) return masterScore()*.8+(st[m.st]-50)*.2+(k==='atkM'?Math.max(artDuel('element'),artDuel('projection'),artDuel('evocation')):k==='defM'?Math.max(artDuel('barrier'),artDuel('displacement'),artDuel('evocation')):k==='trkM'?Math.max(artDuel('curse'),artDuel('mind'),artDuel('astro'),artDuel('illusion_art'),artDuel('displacement')):0)+giftDuel(k);\n    return 30+(st[m.a]-50)*.3+(st[m.b]-50)*.15+mdMartial(k)+(k==='rush'||k==='hide'?artLv('projection')*3*artQ('projection'):0)+(k==='hide'?artLv('illusion_art')*3:0)+giftDuel(k); }"
)
rp(
"    bapt:{n:'세례영창',art:'baptism',c:25,mg:1,once:'bapted',d:'이번 합 상대 서번트 전투력이 떨어진다 · 어벤저와 그림자, 사도에게는 두 배 · 대마력이면 절반 · 전투에서 한 번',f:(b,e)=>{ const lv=artLv('baptism'), eh=H_BY[e.hero]; let v=[0,4,6,8][lv]*(lv>=2?artQ('baptism'):1); if(eh.cls==='avenger'||e.cx||e.aid==='apostle') v*=2; if(SV(eh,'mr')) v/=2; b.mDeb={r:b.round,v:Math.round(v)}; },l:(h,e)=>`당신의 세례영창이 ${pName(e)}의 영기를 흔들었다.`},",
"""    bapt:{n:'세례영창',art:'baptism',c:25,mg:1,once:'bapted',d:'이번 합 상대 서번트 전투력이 떨어진다 · 어벤저와 그림자, 사도에게는 두 배 · 대마력이면 절반 · 전투에서 한 번',f:(b,e)=>{ const lv=artLv('baptism'), eh=H_BY[e.hero]; let v=[0,4,6,8][lv]*(lv>=2?artQ('baptism'):1); if(eh.cls==='avenger'||e.cx||e.aid==='apostle') v*=2; if(SV(eh,'mr')) v/=2; b.mDeb={r:b.round,v:Math.round(v)}; },l:(h,e)=>`당신의 세례영창이 ${pName(e)}의 영기를 흔들었다.`},
    proj:{n:'무구 투영',art:'projection',c:20,mg:1,d:'마력으로 임시 무구와 도구를 투영한다',f:b=>{ const lv=artLv('projection'); b.proj={until:b.round+(lv>=3?1:0),set:b.round,v:Math.round((5+lv*3)*(lv>=2?artQ('projection'):1)),dmgM:lv>=2?1.12:1.05}; },l:h=>`당신이 마력으로 빚은 임시 무구가 ${h.name}의 손끝에서 푸르게 빛났다.`},
    evoke:{n:'영령 빙의',art:'evocation',c:25,mg:1,once:'evoked',d:'영체를 불러내 빙의하여 전투력과 수비를 끌어올린다',f:b=>{ const lv=artLv('evocation'); b.evoke={until:b.round+1,set:b.round,pow:Math.round((5+lv*3)*(lv>=2?artQ('evocation'):1)),guard:lv>=2?.16:.08}; if(lv>=3) W().sm=clamp(W().sm+8); },l:h=>`부름에 응한 영체가 전장에 겹쳐지며 ${h.name}의 기세를 떠받쳤다.`},
    mirage:{n:'환영 미끼',art:'illusion_art',c:20,mg:1,d:'환영 미끼를 세워 적의 시야를 어지럽히고 회피를 높인다',f:(b,e)=>{ const lv=artLv('illusion_art'), q=lv>=2?artQ('illusion_art'):1; b.artIll={until:b.round+(lv>=3?1:0),set:b.round,v:Math.min(.32,.1+lv*.06*q)}; b.mDeb={r:b.round,v:Math.round((4+lv*2)*q)}; },l:(h,e)=>`허상이 겹겹이 피어나며 ${pName(e)}의 시야를 흔들었다.`},
    swap:{n:'치환 반격',art:'displacement',c:25,mg:1,d:'대상과 물체의 위치를 치환해 피해를 줄이고 반격한다',f:(b,e)=>{ const lv=artLv('displacement'), q=lv>=2?artQ('displacement'):1; b.dispTrap={r:b.round,v:Math.round((6+lv*3)*q),red:Math.min(.42,.14+lv*.08)}; b.mDeb={r:b.round,v:Math.round((3+lv*2)*q)}; },l:(h,e)=>`주변 사물의 좌표를 묶어 ${pName(e)}의 발밑에 치환 함정을 깔았다.`},"""
)
rp(
"          for(const k of ['eyeGuard','eyeDeb','eWeak','eyeIll','eyeImmob','eyeClair','eyeVTheft']){ if(b[k]&&b[k].until>=b.round){ b[k].until+=ext; if(b[k].v!=null) b[k].v=(b[k].v<1?Math.min(.75,b[k].v*mul):Math.round(b[k].v*mul)); } }",
"          for(const k of ['eyeGuard','eyeDeb','eWeak','eyeIll','eyeImmob','eyeClair','eyeVTheft','proj','evoke','artIll']){ if(b[k]&&b[k].until>=b.round){ b[k].until+=ext; if(b[k].v!=null) b[k].v=(b[k].v<1?Math.min(.75,b[k].v*mul):Math.round(b[k].v*mul)); if(b[k].pow!=null) b[k].pow=Math.round(b[k].pow*mul); } }"
)
rp(
"  const ACT_SRC=k=>k==='bapt'?['baptism']:k==='key'?['blackkey']:k==='gem'?['jewel']:k==='gap'||k==='back'?MARTIAL.slice():Object.keys(ART_ACT).filter(id=>ART_ACT[id].includes(k));",
"  const ACT_SRC=k=>k==='bapt'?['baptism']:k==='proj'?['projection']:k==='evoke'?['evocation']:k==='mirage'?['illusion_art']:k==='swap'?['displacement']:k==='key'?['blackkey']:k==='gem'?['jewel']:k==='gap'||k==='back'?MARTIAL.slice():Object.keys(ART_ACT).filter(id=>ART_ACT[id].includes(k));"
)
rp(
"    if(k==='gem') return (6+lv*3)*(lv>=2?q:1)/9;",
"    if(k==='gem') return (6+lv*3)*(lv>=2?q:1)/9;\n    if(k==='proj'||k==='evoke') return (5+lv*3)*(lv>=2?q:1)/8;\n    if(k==='mirage') return (4+lv*2)*(lv>=2?q:1)/6;\n    if(k==='swap') return (6+lv*3)*(lv>=2?q:1)/9;"
)
rp(
"    bapt:{dd:'세례영창으로 상대 서번트의 영기를 흔든다',fx:()=>[['이번 합 상대 전투력 ↓','up'],['어벤저·그림자·사도에게 두 배','up'],['대마력이면 절반',''],['전투에서 한 번','']]},",
"""    bapt:{dd:'세례영창으로 상대 서번트의 영기를 흔든다',fx:()=>[['이번 합 상대 전투력 ↓','up'],['어벤저·그림자·사도에게 두 배','up'],['대마력이면 절반',''],['전투에서 한 번','']]},
    proj:{dd:'마력으로 임시 무구와 도구를 투영한다',fx:()=>[['이번 합 우리 전투력 ↑','up'],['공격 피해 ↑','up']]},
    evoke:{dd:'영체를 불러내 빙의하여 전투력과 수비를 끌어올린다',fx:()=>[['두 합 지속 · 받는 피해 ↓','up'],['고위 시 서번트 마력 +8','up'],['전투에서 한 번','']]},
    mirage:{dd:'환영 미끼를 세워 적의 시야를 어지럽히고 회피를 높인다',fx:()=>[['이번 합 상대 전투력 ↓','up'],['회피 ↑ · 미끼','up']]},
    swap:{dd:'대상과 물체의 위치를 치환해 피해를 줄이고 반격한다',fx:()=>[['이번 합 상대 전투력 ↓','up'],['피격 시 자동 반격','up']]},"""
)
rp(
"    const mk=mg?['buff','hex','ward','heal'].filter(k=>actLv(k)>=1).concat(artLv('baptism')>=1?['bapt']:[]):[];",
"    const mk=mg?['buff','hex','ward','heal'].filter(k=>actLv(k)>=1).concat(artLv('baptism')>=1?['bapt']:[],artLv('projection')>=1?['proj']:[],artLv('evocation')>=1?['evoke']:[],artLv('illusion_art')>=1?['mirage']:[],artLv('displacement')>=1?['swap']:[]):[];"
)
rp(
"    A.f(b,e); if(b.ctx.remote){ if(b.mPow&&b.mPow.r===b.round) b.mPow.v=Math.round(b.mPow.v/2); if(b.mDeb&&b.mDeb.r===b.round) b.mDeb.v=Math.round(b.mDeb.v/2); if(b.mGuard&&b.mGuard.r===b.round) b.mGuard.v/=2; if(b.eyeDeb&&b.eyeDeb.set===b.round) b.eyeDeb.v=Math.round(b.eyeDeb.v/2); if(b.eyeGuard&&b.eyeGuard.set===b.round) b.eyeGuard.v/=2; if(b.eyeIll&&b.eyeIll.set===b.round) b.eyeIll.v/=2; if(b.eyeClair&&b.eyeClair.set===b.round) b.eyeClair.v=Math.round(b.eyeClair.v/2); if(b.eyeImmob&&b.eyeImmob.set===b.round) b.eyeImmob.nextPow=Math.round(b.eyeImmob.nextPow/2); if(b.eyeVTheft&&b.eyeVTheft.set===b.round) b.eyeVTheft.v=Math.round(b.eyeVTheft.v/2); }",
"    A.f(b,e); if(b.ctx.remote){ if(b.mPow&&b.mPow.r===b.round) b.mPow.v=Math.round(b.mPow.v/2); if(b.mDeb&&b.mDeb.r===b.round) b.mDeb.v=Math.round(b.mDeb.v/2); if(b.mGuard&&b.mGuard.r===b.round) b.mGuard.v/=2; if(b.eyeDeb&&b.eyeDeb.set===b.round) b.eyeDeb.v=Math.round(b.eyeDeb.v/2); if(b.eyeGuard&&b.eyeGuard.set===b.round) b.eyeGuard.v/=2; if(b.eyeIll&&b.eyeIll.set===b.round) b.eyeIll.v/=2; if(b.eyeClair&&b.eyeClair.set===b.round) b.eyeClair.v=Math.round(b.eyeClair.v/2); if(b.eyeImmob&&b.eyeImmob.set===b.round) b.eyeImmob.nextPow=Math.round(b.eyeImmob.nextPow/2); if(b.eyeVTheft&&b.eyeVTheft.set===b.round) b.eyeVTheft.v=Math.round(b.eyeVTheft.v/2); if(b.proj&&b.proj.set===b.round) b.proj.v=Math.round(b.proj.v/2); if(b.evoke&&b.evoke.set===b.round) b.evoke.pow=Math.round(b.evoke.pow/2); if(b.artIll&&b.artIll.set===b.round) b.artIll.v/=2; if(b.dispTrap&&b.dispTrap.r===b.round) b.dispTrap.v=Math.round(b.dispTrap.v/2); }"
)
rp(
"    log(A.l(h,e),'war'); H.sfx('m_'+({bapt:'ward',gap:'hex',back:'ward',key:'hex',eye:'hex',gem:'hex',decoy:'hex'}[k]||k));",
"    log(A.l(h,e),'war'); H.sfx('m_'+({bapt:'ward',proj:'buff',evoke:'buff',mirage:'hex',swap:'ward',gap:'hex',back:'ward',key:'hex',eye:'hex',gem:'hex',decoy:'hex'}[k]||k));"
)
rp(
"  const mBon=b=>((b.mPow&&(b.mPow.r===b.round||(b.mPow.until&&b.mPow.until>=b.round)))?b.mPow.v:0)+((b.eyeClair&&b.eyeClair.until>=b.round&&b.eyeClair.set!==b.round)?b.eyeClair.v:0)-(b.shield===b.round?6:0);",
"  const mBon=b=>((b.mPow&&(b.mPow.r===b.round||(b.mPow.until&&b.mPow.until>=b.round)))?b.mPow.v:0)+((b.proj&&b.proj.until>=b.round)?b.proj.v:0)+((b.evoke&&b.evoke.until>=b.round)?b.evoke.pow:0)+((b.eyeClair&&b.eyeClair.until>=b.round&&b.eyeClair.set!==b.round)?b.eyeClair.v:0)-(b.shield===b.round?6:0);"
)
rp(
"    if(b.eyeDeath&&b.eyeDeath.until>=rd) add(M,b.eyeDeath.mode==='point'?'직사 · 사점':'직사 · 선',b.eyeDeath.mode==='point'?18:10,'적의 방어와 재생을 끊고 죽음의 선과 점을 겨눈다',`${b.eyeDeath.until-rd+1}합 남음`);",
"""    if(b.eyeDeath&&b.eyeDeath.until>=rd) add(M,b.eyeDeath.mode==='point'?'직사 · 사점':'직사 · 선',b.eyeDeath.mode==='point'?18:10,'적의 방어와 재생을 끊고 죽음의 선과 점을 겨눈다',`${b.eyeDeath.until-rd+1}합 남음`);
    if(b.proj&&b.proj.until>=rd) add(M,'투영 무구',b.proj.v,'마력으로 투영한 무구가 공격력을 끌어올린다',`${b.proj.until-rd+1}합 남음`);
    if(b.evoke&&b.evoke.until>=rd) add(M,'영매 · 빙의',b.evoke.pow,'불러낸 영체가 전투력과 방어를 떠받치고 있다',`${b.evoke.until-rd+1}합 남음`);
    if(b.artIll&&b.artIll.until>=rd) add(M,'환술 · 미끼',b.artIll.v*18,'환영이 적의 조준을 흔들고 거짓 표적을 세웠다',`${b.artIll.until-rd+1}합 남음`);
    if(b.dispTrap&&b.dispTrap.r===rd) add(M,'치환 · 함정',b.dispTrap.v,'위치 치환으로 공격을 흘리고 반격 함정으로 끌어들인다','이번 합');"""
)

# Clash math: projection dmgM, illusion_art dodge & decoy, evocation & displacement guard + auto-counter
rp(
"    const _mDodgeAdd=(_illOn?b.eyeIll.v*.45:0);\n    const agi=(PV(MP[1])-PV(EP[1]))*.02, outM=atkM(atkK,h,MP,eh2,EP,night)*udM(h,eh2)*sjDayM(h)*(b.ctx.raid?.6:1)*(h.sp==='gate'?1.06:1)*(h.id==='enkidu'&&w.morph==='atk'?1.15:1)*(_immNext?(b.eyeImmob.nextMul||1.15):1)*_tmD*npDealM(b,'me'),",
"    const _artIllOn=b.artIll&&b.artIll.until>=b.round, _projOn=b.proj&&b.proj.until>=b.round;\n    const _mDodgeAdd=(_illOn?b.eyeIll.v*.45:0)+(_artIllOn?b.artIll.v*.4:0);\n    const agi=(PV(MP[1])-PV(EP[1]))*.02, outM=atkM(atkK,h,MP,eh2,EP,night)*udM(h,eh2)*sjDayM(h)*(b.ctx.raid?.6:1)*(h.sp==='gate'?1.06:1)*(h.id==='enkidu'&&w.morph==='atk'?1.15:1)*(_immNext?(b.eyeImmob.nextMul||1.15):1)*(_projOn?(b.proj.dmgM||1.05):1)*_tmD*npDealM(b,'me'),"
)
rp(
"      } else if(ch((dodgeP(MP[1],EP[1])+_mDodgeAdd)*(eK==='magic'?MG.dodge:1)*(fxGet(b,'en','holmes')?0:1))||(_illOn&&ch(b.eyeIll.v))){ b.dodged='m'; e.hp=clamp(e.hp-ri(1,3));",
"      } else if(ch((dodgeP(MP[1],EP[1])+_mDodgeAdd)*(eK==='magic'?MG.dodge:1)*(fxGet(b,'en','holmes')?0:1))||(_illOn&&ch(b.eyeIll.v))||(_artIllOn&&ch(b.artIll.v))){ b.dodged='m'; e.hp=clamp(e.hp-ri(1,3));"
)
rp(
"    { const gv=Math.max((b.mGuard&&(b.mGuard.r===b.round||(b.mGuard.until&&b.mGuard.until>=b.round)))?b.mGuard.v:0,b.eyeGuard&&b.eyeGuard.until>=b.round?b.eyeGuard.v:0); if(!(myNP||enNP)&&gv&&w.hp<hp0) w.hp=clamp(w.hp+Math.round((hp0-w.hp)*gv)); }",
"""    { const gv=Math.max((b.mGuard&&(b.mGuard.r===b.round||(b.mGuard.until&&b.mGuard.until>=b.round)))?b.mGuard.v:0,b.eyeGuard&&b.eyeGuard.until>=b.round?b.eyeGuard.v:0,b.evoke&&b.evoke.until>=b.round?b.evoke.guard:0,b.dispTrap&&b.dispTrap.r===b.round?b.dispTrap.red:0); if(!(myNP||enNP)&&gv&&w.hp<hp0) w.hp=clamp(w.hp+Math.round((hp0-w.hp)*gv)); }
    if(!(myNP||enNP)&&b.dispTrap&&b.dispTrap.r===b.round&&e.hp>0&&(d<=-8||b.rev==='e'||w.hp<hp0)){
      e.hp=clamp(e.hp-b.dispTrap.v);
      log(`치환 마술이 발동했다! ${eN}의 공격 궤도가 뒤틀리며 되려 준비된 함정에 꽂혔다.`,'war');
    }"""
)

if miss:
    for x in miss:
        print('못 찾음', x)
    sys.exit(1)

open(P, 'w', encoding='utf-8').write(s)
print('arts41125 적용 끝')

# Update i18n
from arts4_lines import D, T
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
if os.path.exists(zp):
    Z = json.load(open(zp, encoding='utf-8'))
    nz = 0
    for a, _b, _c, d, e in D + T:
        if a not in Z:
            Z[a] = [d, e]
            nz += 1
    if nz:
        json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('zh/done.json 추가', nz)

if re.search(r'const I18N_DICT=\{en:\{', s):
    import i18n
    s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, *_ in D], [(a, b, c) for a, b, c, *_ in T])
    open(P, 'w', encoding='utf-8').write(s)
    print('인라인 사전 추가', nd, nt)
else:
    base_dir = os.path.dirname(os.path.abspath(P))
    i18n_dir = os.path.join(base_dir, 'assets', 'i18n')
    if os.path.isdir(i18n_dir):
        for lg, var, idx in (('en', 'I18N_EN', 1), ('ja', 'I18N_JA', 2)):
            fp = os.path.join(i18n_dir, lg + '.js')
            if not os.path.exists(fp): continue
            txt = open(fp, encoding='utf-8').read()
            m1 = re.search(r'window\.' + var + r'=(\{.*?\});\nwindow\.' + var + r'_T=(\[.*?\]);', txt, re.S)
            if not m1: continue
            dic = json.loads(m1.group(1))
            tpl = json.loads(m1.group(2))
            nd = nt = 0
            for row in D:
                if row[0] not in dic:
                    dic[row[0]] = row[idx]
                    nd += 1
            have_t = {x[0] for x in tpl}
            for row in T:
                if row[0] not in have_t:
                    tpl.append([row[0], row[idx]])
                    nt += 1
            body = txt[:m1.start(1)] + json.dumps(dic, ensure_ascii=False, separators=(',', ':')) + ';\nwindow.' + var + '_T=' + json.dumps(tpl, ensure_ascii=False, separators=(',', ':')) + ';' + txt[m1.end(2)+1:]
            open(fp, 'w', encoding='utf-8').write(body)
            h = hashlib.md5(body.encode('utf-8')).hexdigest()[:8]
            s = re.sub(r'assets/i18n/' + lg + r'\.js\?v=[0-9a-f]+', f'assets/i18n/{lg}.js?v={h}', s)
            print(f'{lg}.js 추가 d:{nd} t:{nt}, hash {h}')
        for lg, idx in (('zhs', 3), ('zht', 4)):
            fp = os.path.join(i18n_dir, lg + '.js')
            if not os.path.exists(fp): continue
            txt = open(fp, encoding='utf-8').read()
            m = re.search(r'window\.I18N_ZH=(\{.*\});?\s*$', txt, re.S)
            if not m: continue
            obj = json.loads(m.group(1))
            dic = obj.get('d', {})
            tpl = obj.get('t', [])
            nd = nt = 0
            for row in D:
                if row[0] not in dic:
                    dic[row[0]] = row[idx]
                    nd += 1
            have_t = {x[0] for x in tpl}
            for row in T:
                if row[0] not in have_t:
                    tpl.append([row[0], row[idx]])
                    nt += 1
            obj['d'] = dic
            obj['t'] = tpl
            body = txt[:m.start(1)] + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + ';\n'
            open(fp, 'w', encoding='utf-8').write(body)
            h = hashlib.md5(body.encode('utf-8')).hexdigest()[:8]
            s = re.sub(r"\{zhs:'([0-9a-f]+)',zht:'([0-9a-f]+)'\}", lambda m2: f"{{zhs:'{h if lg=='zhs' else m2.group(1)}',zht:'{h if lg=='zht' else m2.group(2)}'}}", s)
            print(f'{lg}.js 추가 d:{nd} t:{nt}, hash {h}')
        open(P, 'w', encoding='utf-8').write(s)
