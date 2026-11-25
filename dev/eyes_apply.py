"""6 New Mystic Eyes & Rainbow Grade patch script (eyes1125).
Usage: python3 eyes_apply.py <game.html>
"""
import sys, os, json, re, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'eyes1125' in s:
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

# 1. Custom Master Grade 5 (무지개) = 10 pt & dynamic UI grade button
rp(
"  const CUST_GIFT_COST = [0, 2, 4, 6, 9];",
"  const CUST_GIFT_COST = [0, 2, 4, 6, 9, 10]; /* eyes1125 */"
)
rp(
"  $('#custGiftGrSeg').innerHTML=[1,2,3,4].map(g=>`<button type=\"button\" data-g=\"${g}\">${esc(T(Sim.GRADE_N[g]))}</button>`).join('');",
"  $('#custGiftGrSeg').innerHTML=[1,2,3,4,5].map(g=>`<button type=\"button\" data-g=\"${g}\">${esc(T(Sim.GRADE_N[g]))}</button>`).join('');"
)
rp(
"    gs.querySelectorAll('button').forEach(b=>{\n      const g=+b.dataset.g, ok=g>=G.g[0]&&g<=G.g[1];\n      b.disabled=!ok; b.style.opacity=ok?'':'0.35';\n      b.setAttribute('aria-pressed',String(g===d.giftGr));\n    });",
"    gs.querySelectorAll('button').forEach(b=>{\n      const g=+b.dataset.g, ok=g>=G.g[0]&&g<=G.g[1];\n      b.classList.toggle('hidden', g>4 && G.g[1]<5);\n      b.disabled=!ok; b.style.opacity=ok?'':'0.35';\n      b.setAttribute('aria-pressed',String(g===d.giftGr));\n    });"
)

# 2. Register 6 new Mystic Eyes, GRADE_N[5], GIFT_AWAKE, ACH, giftRoll rarity, GIFT_F, giftCost, giftEvent, giftView, EYE_D
OLD_GIFTS = """  const GIFTS={
    charm:{n:'매료의 마안',w:25,g:[1,3],slot:{trkM:4,trick:4}}, bind:{n:'속박의 마안',w:20,g:[1,3],all:3},
    flame:{n:'염소의 마안',w:14,g:[2,3],slot:{atkM:5,rush:5}}, stone:{n:'석화의 마안',w:6,g:[3,4]},
    future:{n:'미래시의 마안',w:10,g:[2,4],all:2}, past:{n:'과거시의 마안',w:10,g:[2,3]},
    jinx:{n:'흉운의 마안',w:6,g:[3,3],slot:{atkM:4,rush:4}}, compel:{n:'강제의 마안',w:1.5,g:[4,4],slot:{trkM:5,trick:5}},
    telek:{n:'염동',w:8,g:[1,3],slot:{defM:3,hide:3}}, blood:{n:'마의 피',w:0,g:[2,3],slot:{rush:8,hide:8,trick:8}},
  };
  const GRADE_N=['','하','중','상','보석'];
  const GIFT_AWAKE={
    charm:'친구와 말다툼을 하다 눈이 마주쳤다. 친구가 갑자기 말을 멈추고 웃었다. 당신이 바란 대로였다. 그 뒤로 사람들의 눈을 오래 보지 않게 되었다.',
    bind:'쫓아오던 개와 눈이 마주친 순간, 개가 그 자리에 얼어붙었다. 당신이 눈을 돌리고 나서야 개는 낑낑거리며 달아났다.',
    flame:'화가 치민 순간, 바라보던 종이가 끝에서부터 타들어 갔다. 불씨는 어디에도 없었다.',
    stone:'눈이 따끔거리던 날, 창가의 화분이 회색으로 굳어 있었다. 손끝으로 두드리자 돌 소리가 났다.',
    future:'횡단보도 앞에서 발이 멈췄다. 1초 뒤 트럭이 신호를 무시하고 지나갔다. 당신은 그 장면을 이미 보았다.',
    past:'오래된 의자에 손을 얹자 그 의자에 앉았던 사람들이 차례로 보였다. 오래전에 죽은 사람도 있었다.',
    jinx:'당신을 괴롭히던 아이를 오래 노려본 다음 날, 그 아이가 계단에서 굴렀다. 그다음 날에도 무슨 일이 생겼다.',
    compel:'“멈춰.” 그 한마디에 교실 전체가 숨을 멈췄다. 당신의 눈을 본 사람은 아무도 움직이지 못했다.',
    telek:'떨어지는 컵이 바닥에 닿기 직전 멈춰 섰다. 손을 대지 않았는데도.',
    blood:'열이 사흘 동안 내리지 않았다. 열이 내린 날, 손에 쥔 쇠파이프가 엿가락처럼 휘었다. 집안 어른들은 말없이 서로를 보았다.',
  };"""

NEW_GIFTS = """  const GIFTS={
    charm:{n:'매료의 마안',w:25,g:[1,3],slot:{trkM:4,trick:4}}, bind:{n:'속박의 마안',w:20,g:[1,3],all:3},
    flame:{n:'염소의 마안',w:14,g:[2,3],slot:{atkM:5,rush:5}}, stone:{n:'석화의 마안',w:6,g:[3,4]},
    future:{n:'미래시의 마안',w:10,g:[2,4],all:2}, past:{n:'과거시의 마안',w:10,g:[2,3]},
    jinx:{n:'흉운의 마안',w:6,g:[3,3],slot:{atkM:4,rush:4}}, compel:{n:'강제의 마안',w:1.5,g:[4,4],slot:{trkM:5,trick:5}},
    telek:{n:'염동',w:8,g:[1,3],slot:{defM:3,hide:3}}, blood:{n:'마의 피',w:0,g:[2,3],slot:{rush:8,hide:8,trick:8}},
    illusion:{n:'환각의 마안',w:12,g:[1,3],slot:{defM:4,hide:4}},
    clairvoyance:{n:'천리안의 마안',w:10,g:[2,3],slot:{atkM:3,trkM:3}},
    immob:{n:'정지의 마안',w:12,g:[1,3],slot:{rush:4,atkM:3}},
    vtheft:{n:'탈시의 마안',w:8,g:[2,3],slot:{trkM:4,trick:4}},
    prolong:{n:'연장의 마안',w:1.5,g:[4,4],all:3},
    death:{n:'직사의 마안',w:0.2,g:[4,5],slot:{atkM:5,rush:5}},
  };
  const GRADE_N=['','하','중','상','보석','무지개'];
  const GIFT_AWAKE={
    charm:'친구와 말다툼을 하다 눈이 마주쳤다. 친구가 갑자기 말을 멈추고 웃었다. 당신이 바란 대로였다. 그 뒤로 사람들의 눈을 오래 보지 않게 되었다.',
    bind:'쫓아오던 개와 눈이 마주친 순간, 개가 그 자리에 얼어붙었다. 당신이 눈을 돌리고 나서야 개는 낑낑거리며 달아났다.',
    flame:'화가 치민 순간, 바라보던 종이가 끝에서부터 타들어 갔다. 불씨는 어디에도 없었다.',
    stone:'눈이 따끔거리던 날, 창가의 화분이 회색으로 굳어 있었다. 손끝으로 두드리자 돌 소리가 났다.',
    future:'횡단보도 앞에서 발이 멈췄다. 1초 뒤 트럭이 신호를 무시하고 지나갔다. 당신은 그 장면을 이미 보았다.',
    past:'오래된 의자에 손을 얹자 그 의자에 앉았던 사람들이 차례로 보였다. 오래전에 죽은 사람도 있었다.',
    jinx:'당신을 괴롭히던 아이를 오래 노려본 다음 날, 그 아이가 계단에서 굴렀다. 그다음 날에도 무슨 일이 생겼다.',
    compel:'“멈춰.” 그 한마디에 교실 전체가 숨을 멈췄다. 당신의 눈을 본 사람은 아무도 움직이지 못했다.',
    telek:'떨어지는 컵이 바닥에 닿기 직전 멈춰 섰다. 손을 대지 않았는데도.',
    blood:'열이 사흘 동안 내리지 않았다. 열이 내린 날, 손에 쥔 쇠파이프가 엿가락처럼 휘었다. 집안 어른들은 말없이 서로를 보았다.',
    illusion:'복도 끝에 서 있던 그림자에게 말을 걸었다. 돌아보니 아무도 없었다. 그날부터 당신이 눈으로 짚은 허상은 남의 눈에도 그대로 겹쳐 보였다.',
    clairvoyance:'창밖 몇 킬로미터 너머, 닫힌 문 뒤의 불빛과 사람의 움직임이 손에 잡힐 듯 선명하게 비쳤다. 눈을 감아도 거리의 윤곽이 지워지지 않았다.',
    immob:'뛰어내리던 길고양이와 눈이 마주친 찰나, 고양이의 도약이 늪에 빠진 듯 느려졌다. 사슬도 감옥도 없이 공간 자체가 움직임을 끌어내리고 있었다.',
    vtheft:'스쳐 지나간 행인의 시선이 겹친 순간, 그 사람이 방금 보았던 골목의 풍경과 기억이 통째로 눈 안으로 흘러들었다. 상대는 잠시 앞을 보지 못했다.',
    prolong:'다 꺼져 가던 모닥불의 불꽃을 오래 바라보았다. 바람이 불어도 불씨는 좀처럼 사그라지지 않고, 평소보다 배는 더 오래 타올랐다.',
    death:'열병이 멎고 눈을 떴을 때, 세상 모든 사물과 살아 숨 쉬는 것 위에 검은 금이 가 있었다. 손가락 하나로 그어 내리면 두 번 다시 붙지 않을 죽음의 선이었다.',
  };"""
rp(OLD_GIFTS, NEW_GIFTS)

rp(
"  for(const id of Object.keys(GIFTS)){ const G=GIFTS[id], h=(id==='compel'||id==='blood')?1:0;",
"  for(const id of Object.keys(GIFTS)){ const G=GIFTS[id], h=(id==='compel'||id==='blood'||id==='prolong'||id==='death')?1:0;"
)
rp(
"    {id:'h_jewel',cat:'숨겨진 업적',h:1,n:'보석의 눈',d:'보석 등급의 마안이 깨어났다',t:()=>!!S.gift&&!!S.gift.awake&&S.gift.gr>=4},",
"    {id:'h_jewel',cat:'숨겨진 업적',h:1,n:'보석의 눈',d:'보석 등급의 마안이 깨어났다',t:()=>!!S.gift&&!!S.gift.awake&&S.gift.gr>=4},\n    {id:'h_rainbow',cat:'숨겨진 업적',h:1,n:'무지개의 눈',d:'무지개 등급의 마안이 깨어났다',t:()=>!!S.gift&&!!S.gift.awake&&S.gift.gr>=5},"
)

rp(
"    const [g0,g1]=GIFTS[id].g; S.gift={id,gr:g0+Math.floor(hrand('giftG')*(g1-g0+1)),awake:false,ctl:0}; }",
"    const [g0,g1]=GIFTS[id].g; const gr=id==='death'?(hrand('giftG')<.12?5:4):g0+Math.floor(hrand('giftG')*(g1-g0+1)); S.gift={id,gr,awake:false,ctl:0}; }"
)
rp(
"  // 등급 보정: 하 1 · 중 2.5 · 상 4 · 보석 6, 제어에 따라 ×0.7 / ×1 / ×1.3\n  const GIFT_F=[0,1,2.5,4,6];\n  const giftF=()=>{ const g=giftOn(); return g?GIFT_F[g.gr]*[.7,1,1.3][g.ctl||0]:0; };\n  function giftDuel(k){ const g=giftOn(); if(!g) return 0; const G=GIFTS[g.id]; return (((G.slot&&G.slot[k])||0)+(G.all||0))*giftF(); }\n  const giftCost=()=>{ const g=giftOn(); return g?[4,2,0][g.ctl||0]+(g.id==='compel'?8:0):0; };",
"""  // 등급 보정: 하 1 · 중 2.5 · 상 4 · 보석 6 · 무지개 8.5, 제어에 따라 ×0.7 / ×1 / ×1.3
  const GIFT_F=[0,1,2.5,4,6,8.5];
  const giftF=()=>{ const g=giftOn(); return g?GIFT_F[g.gr]*[.7,1,1.3][g.ctl||0]:0; };
  function giftDuel(k){ const g=giftOn(); if(!g) return 0; const G=GIFTS[g.id]; return (((G.slot&&G.slot[k])||0)+(G.all||0))*giftF(); }
  const giftCost=()=>{ const g=giftOn(); if(!g) return 0; const b0=[4,2,0][g.ctl||0]; if(g.id==='compel') return b0+8; if(g.id==='prolong') return b0+4; if(g.id==='death'){ const w=W(), bt=w&&w.battle; return 12+[6,3,1][g.ctl||0]+(bt&&bt.deathUses?bt.deathUses*6:0); } return b0; };
  function deathGrasp(e, b){
    const g=giftOn(), eh=e&&H_BY[e.hero]; if(!g||!eh) return {ok:false,mode:'blur',p:0};
    const res = divR(eh)*0.05 + (eh.sp==='revive'?0.18:0) + (e.aid==='apostle'||e.cx==='boss'||e.cx==='shadow'||e.bxNun?0.2:0) + (npRV(eh)>=5?0.08:0) + (SV(eh,'mr')>=4?0.06:0);
    const p = Math.max(0.15, Math.min(0.92, 0.42 + (g.gr>=5?0.22:0) + (g.ctl||0)*0.1 + Math.max(0,(S.st.will||50)-35)*0.004 - res));
    if(!ch(p)) return {ok:false,mode:'blur',p};
    const pointP = Math.max(0.12, Math.min(0.85, (g.gr>=5?0.55:0.28) + (g.ctl||0)*0.1 - res*0.6));
    return {ok:true,mode:ch(pointP)?'point':'line',p};
  }"""
)
rp(
"    const up=r=>{ g.ctl=Math.min(2,(g.ctl||0)+1); if(g.ctl===2&&g.gr<4&&hrand('gUp')<.3){ g.gr++; log(`${G.n}${J(G.n,이)} 한 단계 깊어졌다. 등급 · ${GRADE_N[g.gr]}`,'ev'); } return r||'제어가 한 단계 나아졌다.'; };",
"    const up=r=>{ g.ctl=Math.min(2,(g.ctl||0)+1); const mx=GIFTS[g.id]?GIFTS[g.id].g[1]:4; if(g.ctl===2&&g.gr<mx&&hrand('gUp')<(g.id==='death'?.15:.3)){ g.gr++; log(`${G.n}${J(G.n,이)} 한 단계 깊어졌다. 등급 · ${GRADE_N[g.gr]}`,'ev'); } return r||'제어가 한 단계 나아졌다.'; };"
)
rp(
"  function giftView(){ const g=S&&S.gift; if(!g||!g.awake) return null; return {n:GIFTS[g.id].n,gr:GRADE_N[g.gr],ctl:['제어 못 함','제어 보통','제어 능숙'][g.ctl||0],fx:{blood:'마스터끼리 맞붙을 때 「정면으로 덤빈다」 · 「몸을 숨긴다」 · 「허를 찌른다」가 강해진다',past:'전투에 들어서면 상대 조가 걸어온 길을 읽는다'}[g.id]||''}; }",
"  function giftView(){ const g=S&&S.gift; if(!g||!g.awake) return null; return {n:GIFTS[g.id].n,gr:GRADE_N[g.gr],ctl:['제어 못 함','제어 보통','제어 능숙'][g.ctl||0],fx:{blood:'마스터끼리 맞붙을 때 「정면으로 덤빈다」 · 「몸을 숨긴다」 · 「허를 찌른다」가 강해진다',past:'전투에 들어서면 상대 조가 걸어온 길을 읽는다',illusion:'적의 추적을 흐리고 밤 습격을 다른 표적으로 돌린다',clairvoyance:'멀리서 적의 거처를 포착하고 정찰 범위와 정보 획득을 넓힌다',immob:'상대의 민첩과 회피·도주를 묶고 다음 공격을 강화한다',vtheft:'전투 중 상대의 시야와 정보를 빼앗아 숨겨진 능력을 드러낸다',prolong:'전투 중 아군 버프와 보구의 지속 시간을 늘리고 위력을 증폭한다',death:'막대한 부담을 안고 적의 방어와 재생을 끊으며 사점을 노린다'}[g.id]||''}; }"
)
rp(
"  const EYE_D={charm:'이번 합 상대 마스터가 머뭇거린다 · 상대 전투력이 떨어진다',bind:'이번 합 상대 마스터를 묶는다 · 상대 전투력이 떨어진다',flame:'이번 합 상대 전투력이 크게 떨어진다',stone:'세 합 동안 상대 서번트가 굳는다 · 대마력이 높을수록 덜 듣는다',future:'세 합 동안 받는 피해를 크게 줄인다',jinx:'상대 조에 흉 표식을 새긴다 · 표식 하나마다 상대 전투력 −5',compel:'세 합 동안 상대 마스터를 조종한다',telek:'이번 합 받는 피해를 줄인다'};",
"""  const EYE_D={charm:'이번 합 상대 마스터가 머뭇거린다 · 상대 전투력이 떨어진다',bind:'이번 합 상대 마스터를 묶는다 · 상대 전투력이 떨어진다',flame:'이번 합 상대 전투력이 크게 떨어진다',stone:'세 합 동안 상대 서번트가 굳는다 · 대마력이 높을수록 덜 듣는다',future:'세 합 동안 받는 피해를 크게 줄인다',jinx:'상대 조에 흉 표식을 새긴다 · 표식 하나마다 상대 전투력 −5',compel:'세 합 동안 상대 마스터를 조종한다',telek:'이번 합 받는 피해를 줄인다',
    illusion:'두 합 동안 적의 시야와 인식을 비틀어 거짓 표적을 세운다 · 회피와 반격 억제',
    clairvoyance:'적의 움직임을 멀리서 꿰뚫어 보고 정보를 얻는다 · 회피를 꺾고 전투력을 높인다',
    immob:'두 합 동안 상대의 움직임을 묶어 민첩과 회피, 도주를 꺾고 다음 공격을 강화한다',
    vtheft:'상대의 시야와 정보를 빼앗고 숨겨진 스킬을 드러낸다 · 노출을 줄이고 적의 관찰을 막는다',
    prolong:'현재 걸린 버프·디버프와 보구 효과를 연장하고 위력을 끌어올린다',
    death:'큰 대가를 치르고 죽음의 선과 점을 읽는다 · 방어·배율 무시 및 재생 차단 · 사점 관통 시 즉사'};"""
)

# 3. Passive War Hooks: Illusion (expUp & threat misdirection), Clairvoyance (addIntel, dayStart, scout, rideScout, npcInitB)
rp(
"  const expUp=v=>(S.hero==='lancelot'&&v>0)?Math.round(v*.75):v;",
"  const expUp=v=>{ let x=v; if(S.hero==='lancelot'&&x>0) x=Math.round(x*.75); if(x>0&&giftIs('illusion')) x=Math.max(1,Math.round(x*Math.max(.55,1-.08*giftF()))); return x; };"
)
rp(
"  function addIntel(t,g,why){\n    if(g>0&&t.hero==='lancelot') g=Math.round(g*.6);",
"  function addIntel(t,g,why){\n    if(g>0&&t.hero==='lancelot') g=Math.round(g*.6);\n    if(g>0&&giftIs('clairvoyance')) g=Math.round(g*(1+.1*giftF()));"
)
rp(
"    if(w.day===14) log('마지막 날. 오늘 밤 끝나지 않으면 성배는 남은 이들을 한자리로 불러 모은다.','war');",
"    if(w.day===14) log('마지막 날. 오늘 밤 끝나지 않으면 성배는 남은 이들을 한자리로 불러 모은다.','war');\n    if(giftIs('clairvoyance')&&w.heroAlive){ const hids=alivePairs().filter(p=>!p.known&&!p.cx); if(hids.length&&ch(Math.min(.65,.2+.08*giftF()))){ const ct=pick(hids); addIntel(ct,15,'trace'); ct.known=true; log(`거리 너머를 훑던 시선이 ${cn(ct)} 조의 은신처를 포착했다. 천리안의 마안이다.`,'war'); } }"
)
rp(
"    if(ch(.15)){ const t2=wpick(pool.filter(p=>p!==t&&p.alive),p=>100-p.intel); if(t2){ addIntel(t2,ri(15,25),'trace'); log(`돌아오는 길에 ${cn(t2)} 조의 흔적도 스쳐 보았다.`,'war'); } }",
"    if(ch(giftIs('clairvoyance')?.85:.15)){ const t2=wpick(alivePairs().filter(p=>p!==t&&p.alive&&p.intel<95),p=>100-p.intel); if(t2){ addIntel(t2,giftIs('clairvoyance')?Math.round(14+giftF()*2.5):ri(15,25),'trace'); log(giftIs('clairvoyance')?`멀리서 시야를 넓힌 덕분에 ${cn(t2)} 조의 기척까지 함께 읽어 냈다.`:`돌아오는 길에 ${cn(t2)} 조의 흔적도 스쳐 보았다.`,'war'); } }"
)
rp(
"    if(!t.ally&&ch(.16+(t.tac==='hunter'?.1:0))&&!t.truce&&npcWillRaid(t)){ log(`돌아오는 길, ${pName(t)} 조에게 들켰다.`,'war'); woundNote(t); battle(t,{ambushed:true}); return; }\n    if(ch(.5)) scoutEvent(t);",
"    if(giftIs('clairvoyance')){ const t2=wpick(alivePairs().filter(p=>p!==t&&p.alive&&p.intel<95),p=>100-p.intel); if(t2){ addIntel(t2,Math.round(10+giftF()*2.5),'trace'); if(!t2.known&&t2.intel>=25) t2.known=true; log(`멀리서 시야를 넓힌 덕분에 ${cn(t2)} 조의 기척까지 함께 읽어 냈다.`,'war'); } }\n    const _ambP=(.16+(t.tac==='hunter'?.1:0))*(giftIs('clairvoyance')?Math.max(.2,1-.18*giftF()):1)*(giftIs('illusion')?.75:1);\n    if(!t.ally&&ch(_ambP)&&!t.truce&&npcWillRaid(t)){ log(`돌아오는 길, ${pName(t)} 조에게 들켰다.`,'war'); woundNote(t); battle(t,{ambushed:true}); return; }\n    if(ch(.5)) scoutEvent(t);"
)
rp(
"  function npcInitB(b){ const c=b.ctx; return c.betrayed? (b.round===1?14:b.round===2?7:0) : (c.defend||c.ambushed)&&!c.final&&!c.claim&&!c.hunted? (b.round===1?10:b.round===2?5:0) : 0; }",
"  function npcInitB(b){ const c=b.ctx; let v=c.betrayed? (b.round===1?14:b.round===2?7:0) : (c.defend||c.ambushed)&&!c.final&&!c.claim&&!c.hunted? (b.round===1?10:b.round===2?5:0) : 0; if(v>0&&c.ambushed&&!c.betrayed&&giftIs('clairvoyance')) v=Math.round(v*Math.max(.25,1-.18*giftF())); return v; }"
)
rp(
"        if(tid === 'me' && w.heroAlive){ p.knowMe = Math.min(100, (p.knowMe || 0) + 25); w.exposure = clamp(w.exposure + expUp(4)); }",
"        if(tid === 'me' && w.heroAlive){ const _km=giftIs('illusion')?12:25; p.knowMe = Math.min(100, (p.knowMe || 0) + _km); w.exposure = clamp(w.exposure + expUp(4)); }"
)
rp(
"    if(H_BY[e.hero].cls==='shadow'&&ch(.5)){ shadowVisit(e); return; }",
"""    if(giftIs('illusion')&&!e.cx&&ch(Math.min(.42,.12+giftF()*.05))){
      const dec=foes.find(x=>x!==e&&x.alive&&!x.ally&&!x.cx);
      if(dec&&ch(.55)){ log(`환각에 속은 ${pName(e)} 조가 엉뚱하게도 ${pName(dec)} 조의 거처를 향해 칼을 돌렸다.`,'war'); npcFight(e,dec,false,true); return; }
      log(`환각이 ${pName(e)} 조의 눈길을 비틀었다. 적은 텅 빈 거짓 표적에 칼을 내리찍고 물러났다.`,'war'); return;
    }
    if(H_BY[e.hero].cls==='shadow'&&ch(.5)){ shadowVisit(e); return; }"""
)

# 4. MACT.eye, actChips, and battleMods updates
rp(
"    eye:{free:1,get n(){ return GIFTS[S.gift.id].n; },get once(){ return ['stone','future','compel'].includes(S.gift.id)?'eyeUsed':null; },get d(){ return EYE_D[S.gift.id]+(this.once?' · 전투에서 한 번':''); },\n      req:()=>!(S.gift.id==='stone'&&S.gift.gr<3)&&S.st.health>giftCost()+5,rq:'건강이 모자라다',cost:()=>giftCost(),\n      f:(b,e)=>{ const g=S.gift, F=giftF(), eh=H_BY[e.hero]; add({health:-giftCost()}); if(g.id==='compel'){ add({will:-2}); lean('cruel',1); }\n        if(g.id==='charm'){ b.eHes=b.round; b.mDeb={r:b.round,v:Math.round(5+F*1.5)}; }\n        else if(g.id==='bind'){ b.eHes=b.round; b.mDeb={r:b.round,v:Math.round(6+F*1.5)}; }\n        else if(g.id==='flame'){ b.mDeb={r:b.round,v:Math.round(8+F*2)}; }\n        else if(g.id==='stone'){ b.eyeDeb={until:b.round+2,set:b.round,v:Math.round((14+F*3)*Math.max(0,1-.15*SV(eh,'mr')))}; } // 대마력 랭크마다 15%씩 덜 듣는다(E 15% … A 75%, EX 90%)\n        else if(g.id==='future'){ b.eyeGuard={until:b.round+2,set:b.round,v:Math.min(.5,.25+F*.04)}; }\n        else if(g.id==='jinx'){ e.jinx=Math.min(3,(e.jinx||0)+1); }\n        else if(g.id==='compel'){ b.eHes=b.round; b.eHesTo=b.round+2; b.eyeDeb={until:b.round+2,set:b.round,v:[6,10,16][g.ctl||0]}; }\n        else if(g.id==='telek'){ b.mGuard={r:b.round,v:Math.min(.5,.2+F*.03)}; } },\n      l:(h,e)=>{ const id=S.gift.id, mn=e.mname||pName(e); return id==='charm'?`당신의 눈을 마주친 ${mn}${J(mn,이)} 한순간 멍하니 서 있었다.`:id==='bind'?`${mn}의 몸이 당신의 시선에 묶였다.`:id==='flame'?'당신이 바라본 자리에서 불길이 치솟았다.':id==='stone'?`${pName(e)}의 다리가 회색으로 굳어 갔다.`:id==='future'?`당신은 다음 일격이 어디로 올지 이미 보았다. ${h.name}에게 짧게 외쳤다.`:id==='jinx'?`당신은 오래 노려보았다. ${pName(e)} 조에 흉 표식이 하나 더 새겨졌다.`:id==='compel'?`“멈춰라.” ${mn}의 몸이 당신의 말대로 굳었다.`:`떨어지던 잔해가 허공에서 멈췄다. ${h.name}${J(h.name,이)} 그 틈으로 몸을 뺐다.`; }},",
"""    eye:{free:1,get n(){ return GIFTS[S.gift.id].n; },get once(){ return ['stone','future','compel','prolong'].includes(S.gift.id)?'eyeUsed':null; },get d(){ return EYE_D[S.gift.id]+(this.once?' · 전투에서 한 번':''); },
      req:()=>{ const id=S.gift.id, b=W()&&W().battle; if(id==='stone') return S.gift.gr>=3&&S.st.health>giftCost()+5; if(id==='death') return S.st.will>=35&&!(b&&b.ctx&&b.ctx.remote)&&S.st.health>giftCost()+15; return S.st.health>giftCost()+5; },
      get rq(){ return S.gift&&S.gift.id==='death'?'정신 35·체력·직접 시야 필요':'건강이 모자라다'; },cost:()=>giftCost(),
      f:(b,e)=>{ const g=S.gift, F=giftF(), eh=H_BY[e.hero]; add({health:-giftCost()}); if(g.id==='compel'){ add({will:-2}); lean('cruel',1); }
        if(g.id==='charm'){ b.eHes=b.round; b.mDeb={r:b.round,v:Math.round(5+F*1.5)}; }
        else if(g.id==='bind'){ b.eHes=b.round; b.mDeb={r:b.round,v:Math.round(6+F*1.5)}; }
        else if(g.id==='flame'){ b.mDeb={r:b.round,v:Math.round(8+F*2)}; }
        else if(g.id==='stone'){ b.eyeDeb={until:b.round+2,set:b.round,v:Math.round((14+F*3)*Math.max(0,1-.15*SV(eh,'mr')))}; }
        else if(g.id==='future'){ b.eyeGuard={until:b.round+2,set:b.round,v:Math.min(.5,.25+F*.04)}; }
        else if(g.id==='jinx'){ e.jinx=Math.min(3,(e.jinx||0)+1); }
        else if(g.id==='compel'){ b.eHes=b.round; b.eHesTo=b.round+2; b.eyeDeb={until:b.round+2,set:b.round,v:[6,10,16][g.ctl||0]}; }
        else if(g.id==='telek'){ b.mGuard={r:b.round,v:Math.min(.5,.2+F*.03)}; }
        else if(g.id==='illusion'){ b.eyeIll={until:b.round+1,set:b.round,v:Math.min(.45,.14+F*.05)}; b.mDeb={r:b.round,v:Math.round(4+F)}; }
        else if(g.id==='clairvoyance'){ b.eyeClair={until:b.round+1,set:b.round,v:Math.round(4+F*1.5)}; b.mPow={r:b.round,v:Math.round(4+F*1.5)}; addIntel(e,Math.round(8+F*2),'sight'); e.kitSeen=true; if(g.gr>=3&&!e.revealed) revealSkills(e,'천리안이 상대의 기술을 간파했다. ',1); }
        else if(g.id==='immob'){ b.eyeImmob={until:b.round+1,set:b.round,agiPen:Math.min(3,1+Math.floor(F/2)),fleePen:Math.min(.55,.2+F*.06),nextPow:Math.round(6+F*2),nextMul:1.15+F*.03}; b.immobNext=1; }
        else if(g.id==='vtheft'){
          b.eyeVTheft={until:b.round+1,set:b.round,v:Math.round(4+F*1.5)};
          addIntel(e,Math.round(14+F*3),'trace'); e.kitSeen=true; e.scoutEdge=0;
          W().exposure=clamp(W().exposure-Math.round(4+F));
          if(!e.revealed) revealSkills(e,'탈시의 마안으로 상대의 숨겨진 수를 훔쳐보았다. ',2);
          if(!e.artKnown&&!e.artHint){ const ea=artOf(eh); e.artHint={k:ea.k,r:RANK_BAND(ea.r)}; }
          if(e.know){ for(const [ki,kv] of Object.entries(e.know)){ if(kv>=20){ const tp=pairBy(Number(ki)); if(tp&&tp!==e&&tp.alive) addIntel(tp,Math.round(kv*.4),'trace'); } } }
          if((b.vtLore||0)<3){ add({lore:1}); b.vtLore=(b.vtLore||0)+1; }
        }
        else if(g.id==='prolong'){
          const ext=(g.ctl||0)>=2?2:1, mul=g.ctl>=2?1.35:1.25;
          b.eyeProlong={until:b.round+ext,ext,mul};
          for(const k of ['eyeGuard','eyeDeb','eWeak','eyeIll','eyeImmob','eyeClair','eyeVTheft']){ if(b[k]&&b[k].until>=b.round){ b[k].until+=ext; if(b[k].v!=null) b[k].v=(b[k].v<1?Math.min(.75,b[k].v*mul):Math.round(b[k].v*mul)); } }
          if(b.mPow&&b.mPow.r>=b.round){ b.mPow.until=Math.max(b.mPow.until||b.mPow.r,b.round+ext); b.mPow.v=Math.round(b.mPow.v*mul); }
          if(b.mDeb&&b.mDeb.r>=b.round){ b.mDeb.until=Math.max(b.mDeb.until||b.mDeb.r,b.round+ext); b.mDeb.v=Math.round(b.mDeb.v*mul); }
          if(b.mGuard&&b.mGuard.r>=b.round){ b.mGuard.until=Math.max(b.mGuard.until||b.mGuard.r,b.round+ext); b.mGuard.v=Math.min(.75,b.mGuard.v*mul); }
          if(b.mad>=b.round) b.mad+=ext;
          for(const f of fxL(b)){ if(f.side==='me'&&f.left<90) f.left+=ext; }
          if(e.mHurt) e.mHurt+=1; if(e.provoked) e.provoked+=1;
        }
        else if(g.id==='death'){
          add({will:-3}); b.deathUses=(b.deathUses||0)+1;
          const gr=deathGrasp(e,b);
          b.eyeDeath={until:b.round+(g.gr>=5?2:1),set:b.round,mode:gr.mode,pointDone:false};
          e.noRegen=Math.max(e.noRegen||0,3);
          if(gr.mode!=='blur') e.survUsed=true;
        }
      },
      l:(h,e)=>{ const id=S.gift.id, mn=e.mname||pName(e);
        if(id==='illusion') return `공기가 일렁이며 허상이 겹쳐졌다. ${pName(e)}의 시야가 엇갈리기 시작했다.`;
        if(id==='clairvoyance') return `먼 거리까지 꿰뚫는 시선이 ${pName(e)}의 빈틈을 정확히 짚어 냈다.`;
        if(id==='immob') return `${pName(e)}의 발걸음이 보이지 않는 무게에 눌린 듯 느려졌다.`;
        if(id==='vtheft') return `${pName(e)}의 시야가 한순간 검게 꺼지며 정보가 이쪽으로 흘러들었다.`;
        if(id==='prolong') return `지속되던 술식과 효과의 윤곽이 선명하게 고정되며 한층 강해졌다.`;
        if(id==='death'){ const b=W().battle, md=b&&b.eyeDeath?b.eyeDeath.mode:'blur'; return md==='point'?`정신을 극한까지 벼려 냈다. ${pName(e)}의 심장부에서 일렁이는 죽음의 점이 또렷하게 잡혔다.`:md==='line'?`눈앞에 검은 금이 그어졌다. ${pName(e)}의 방어를 가를 죽음의 선이 보였다.`:`격렬한 두통 속에 죽음의 선이 희미하게 스쳐 지나갔다.`; }
        return id==='charm'?`당신의 눈을 마주친 ${mn}${J(mn,이)} 한순간 멍하니 서 있었다.`:id==='bind'?`${mn}의 몸이 당신의 시선에 묶였다.`:id==='flame'?'당신이 바라본 자리에서 불길이 치솟았다.':id==='stone'?`${pName(e)}의 다리가 회색으로 굳어 갔다.`:id==='future'?`당신은 다음 일격이 어디로 올지 이미 보았다. ${h.name}에게 짧게 외쳤다.`:id==='jinx'?`당신은 오래 노려보았다. ${pName(e)} 조에 흉 표식이 하나 더 새겨졌다.`:id==='compel'?`“멈춰라.” ${mn}의 몸이 당신의 말대로 굳었다.`:`떨어지던 잔해가 허공에서 멈췄다. ${h.name}${J(h.name,이)} 그 틈으로 몸을 뺐다.`; }},"""
)

rp(
"    if(k==='eye'){ const g=S.gift, F=giftF(), V={charm:f=>5+1.5*f,bind:f=>6+1.5*f,flame:f=>8+2*f,stone:f=>14+3*f,future:f=>Math.min(.5,.25+.04*f),telek:f=>Math.min(.5,.2+.03*f)}[g.id];",
"    if(k==='eye'){ const g=S.gift, F=giftF(), V={charm:f=>5+1.5*f,bind:f=>6+1.5*f,flame:f=>8+2*f,stone:f=>14+3*f,future:f=>Math.min(.5,.25+.04*f),telek:f=>Math.min(.5,.2+.03*f),illusion:f=>4+f,clairvoyance:f=>4+1.5*f,immob:f=>6+2*f,vtheft:f=>4+1.5*f,prolong:()=>g.ctl>=2?2:1,death:f=>14+f*2}[g.id];"
)

# Remote battle halving for new eye debuffs/pow
rp(
"    A.f(b,e); if(b.ctx.remote){ if(b.mPow&&b.mPow.r===b.round) b.mPow.v=Math.round(b.mPow.v/2); if(b.mDeb&&b.mDeb.r===b.round) b.mDeb.v=Math.round(b.mDeb.v/2); if(b.mGuard&&b.mGuard.r===b.round) b.mGuard.v/=2; if(b.eyeDeb&&b.eyeDeb.set===b.round) b.eyeDeb.v=Math.round(b.eyeDeb.v/2); if(b.eyeGuard&&b.eyeGuard.set===b.round) b.eyeGuard.v/=2; }",
"    A.f(b,e); if(b.ctx.remote){ if(b.mPow&&b.mPow.r===b.round) b.mPow.v=Math.round(b.mPow.v/2); if(b.mDeb&&b.mDeb.r===b.round) b.mDeb.v=Math.round(b.mDeb.v/2); if(b.mGuard&&b.mGuard.r===b.round) b.mGuard.v/=2; if(b.eyeDeb&&b.eyeDeb.set===b.round) b.eyeDeb.v=Math.round(b.eyeDeb.v/2); if(b.eyeGuard&&b.eyeGuard.set===b.round) b.eyeGuard.v/=2; if(b.eyeIll&&b.eyeIll.set===b.round) b.eyeIll.v/=2; if(b.eyeClair&&b.eyeClair.set===b.round) b.eyeClair.v=Math.round(b.eyeClair.v/2); if(b.eyeImmob&&b.eyeImmob.set===b.round) b.eyeImmob.nextPow=Math.round(b.eyeImmob.nextPow/2); if(b.eyeVTheft&&b.eyeVTheft.set===b.round) b.eyeVTheft.v=Math.round(b.eyeVTheft.v/2); }"
)

# Extend mBon & eMal & battleMods for Prolongation extended buffs + new eyes
rp(
"  const mBon=b=>(b.mPow&&b.mPow.r===b.round?b.mPow.v:0)-(b.shield===b.round?6:0);\n  const eMal=b=>(b.mDeb&&b.mDeb.r===b.round?b.mDeb.v:0)+(b.eWeak&&b.eWeak.until>=b.round?b.eWeak.v:0)+(b.eyeDeb&&b.eyeDeb.until>=b.round?b.eyeDeb.v:0)+((b.e&&b.e.jinx)||0)*5;",
"  const mBon=b=>((b.mPow&&(b.mPow.r===b.round||(b.mPow.until&&b.mPow.until>=b.round)))?b.mPow.v:0)+((b.eyeClair&&b.eyeClair.until>=b.round&&b.eyeClair.set!==b.round)?b.eyeClair.v:0)-(b.shield===b.round?6:0);\n  const eMal=b=>((b.mDeb&&(b.mDeb.r===b.round||(b.mDeb.until&&b.mDeb.until>=b.round)))?b.mDeb.v:0)+(b.eWeak&&b.eWeak.until>=b.round?b.eWeak.v:0)+(b.eyeDeb&&b.eyeDeb.until>=b.round?b.eyeDeb.v:0)+(b.eyeVTheft&&b.eyeVTheft.until>=b.round?b.eyeVTheft.v:0)+((b.e&&b.e.jinx)||0)*5;"
)
rp(
"    if(b.eyeDeb&&b.eyeDeb.until>=rd&&b.eyeDeb.v) add(E,S.gift?GIFTS[S.gift.id].n:'마안',-b.eyeDeb.v,'상대가 약해져 있다',`${b.eyeDeb.until-rd+1}합 남음`);",
"""    if(b.eyeDeb&&b.eyeDeb.until>=rd&&b.eyeDeb.v) add(E,S.gift?GIFTS[S.gift.id].n:'마안',-b.eyeDeb.v,'상대가 약해져 있다',`${b.eyeDeb.until-rd+1}합 남음`);
    if(b.eyeIll&&b.eyeIll.until>=rd) add(M,'환각 · 잔상',b.eyeIll.v*20,'거짓 표적으로 적의 공격과 반격이 빗나간다',`${b.eyeIll.until-rd+1}합 남음`);
    if(b.eyeClair&&b.eyeClair.until>=rd) add(M,'천리안 · 간파',b.eyeClair.v,'멀리서 움직임을 읽어 전투력과 정밀도가 올랐다',`${b.eyeClair.until-rd+1}합 남음`);
    if(b.eyeImmob&&b.eyeImmob.until>=rd) add(E,'정지 · 감속',-b.eyeImmob.agiPen*4,'동작이 묶여 민첩·회피·도주 확률이 떨어지고 다음 일격이 강해진다',`${b.eyeImmob.until-rd+1}합 남음`);
    if(b.eyeVTheft&&b.eyeVTheft.until>=rd) add(E,'탈시 · 실명',-b.eyeVTheft.v,'시야를 빼앗겨 간파와 공격 예리함이 무뎌졌다',`${b.eyeVTheft.until-rd+1}합 남음`);
    if(b.eyeDeath&&b.eyeDeath.until>=rd) add(M,b.eyeDeath.mode==='point'?'직사 · 사점':'직사 · 선',b.eyeDeath.mode==='point'?18:10,'적의 방어와 재생을 끊고 죽음의 선과 점을 겨눈다',`${b.eyeDeath.until-rd+1}합 남음`);"""
)

# 5. Prolongation passive NP duration +1 & mPow/mGuard +1
rp(
"  function npFieldDur(b,side){ const s=npSide(b,side); let d=npDur((PV(s.P[3])+npRV(s.h))/2,NPK.fDur,NPK.fMin,NPK.fMax);\n    if(s.me?S.st.mana>=NPK.fMana:s.e.pw>=74) d=Math.min(NPK.fMax,d+1); return d; }",
"  function npFieldDur(b,side){ const s=npSide(b,side); let d=npDur((PV(s.P[3])+npRV(s.h))/2,NPK.fDur,NPK.fMin,NPK.fMax);\n    if(s.me?S.st.mana>=NPK.fMana:s.e.pw>=74) d=Math.min(NPK.fMax,d+1); if(s.me&&giftIs('prolong')) d+=1; return d; }"
)
rp(
"  function npWallDur(b,side){ const s=npSide(b,side); return npDur(PV(s.P[2])+npRV(s.h),NPK.wDur,NPK.wMin,NPK.wMax); }",
"  function npWallDur(b,side){ const s=npSide(b,side); return npDur(PV(s.P[2])+npRV(s.h),NPK.wDur,NPK.wMin,NPK.wMax)+(s.me&&giftIs('prolong')?1:0); }"
)
rp(
"  function npSupDur(b,side){ return npDur((PV(npSide(b,side).P[3])+npRV(npSide(b,side).h))/2,NPK.sDur,NPK.sMin,NPK.sMax); }",
"  function npSupDur(b,side){ return npDur((PV(npSide(b,side).P[3])+npRV(npSide(b,side).h))/2,NPK.sDur,NPK.sMin,NPK.sMax)+(side==='me'&&giftIs('prolong')?1:0); }"
)

# 6. Combat resolution (clash, npBase, npTick, npcRetreat) & Final Duel (DUEL_EYE, duelEye, duelClash)
rp(
"    if(s.me) return Math.round(npDmg(s.h,s.o,!!FORESEE[e.hero],e.aid==='elder',s.P)*(b.ctx.raid?.6:1)*(b.sealNow?1.3:1)*kavF(s.o.id,e)*(s.h.id==='enkidu'&&w.morph==='atk'?1.15:1)*npDmgSp(b,s)*imm*take);",
"""    if(s.me){
      const dOn=b.eyeDeath&&b.eyeDeath.until>=b.round, dFull=dOn&&b.eyeDeath.mode!=='blur';
      const takeD=dFull?(1-(1-take)*.2):dOn?(1-(1-take)*.55):take;
      const kf=dFull?1:kavF(s.o.id,e);
      return Math.round(npDmg(s.h,s.o,!!FORESEE[e.hero],!dFull&&e.aid==='elder',s.P)*(b.ctx.raid?.6:1)*(b.sealNow?1.3:1)*kf*(s.h.id==='enkidu'&&w.morph==='atk'?1.15:1)*npDmgSp(b,s)*imm*takeD);
    }"""
)

rp(
"      if(f.type==='sup'&&(SUP_SP[f.id]||{}).heal){ const v=SUP_SP[f.id].heal; if(f.side==='me'&&w.hp>0) w.hp=clamp(w.hp+v); else if(f.side==='en'&&b.e.hp>0) b.e.hp=clamp(b.e.hp+v); }",
"      if(f.type==='sup'&&(SUP_SP[f.id]||{}).heal){ const v=SUP_SP[f.id].heal; if(f.side==='me'&&w.hp>0) w.hp=clamp(w.hp+v); else if(f.side==='en'&&b.e.hp>0&&!(b.eyeDeath&&b.eyeDeath.until>=b.round)) b.e.hp=clamp(b.e.hp+v); }"
)

OLD_CLASH_MATH = """    b.dodged=null; b.judgedNow=b.judged; b.sealNow=b.sealBuff===b.round; const P=myPower({e,defend:b.ctx.defend,judged:b.judged,attack:b.ctx.attack,trap:b.ctx.trap,breach:b.ctx.breach})+bonus+mBon(b)+(b.ctx.final&&w.altar==='me'?6:0)+(b.ctx.final&&w.riteDone?6:0)+(b.ctx.raid?12:0)+initB(b)+(b.mad>=b.round?12:0)+(b.aron?8:0)+(rnd()*36-18)-eSab-(w.sm<=0?30:w.sm<15?10:0)+npFxP(b,'me'); b.judged=false;
    let E=npcPower(e,true)-eMal(b)+(rnd()*36-18)+(b.ctx.hunted?(w.hid?HUNT_E/2:HUNT_E):0)+(b.ctx.final&&e.altar?6:0)+(b.ctx.claim&&b.ctx.attack&&e.altarPre?10:0)+(e.tac==='reckless'?6:0)+npcAct(b,e)+npcInitB(b)+(b.ctx.hostage&&b.round<=2?10:0)-sab+(b.ctx.attack?eWsB(e):0)-(b.compChk&&b.compChk.r===b.round?b.compChk.v:0);
    E+=npFxP(b,'en'); { const _c=Math.round(((3+ri(0,3))*(H_BY[e.hero].cls==='berserk'?1.4:1)+(SV(H_BY[e.hero],'mad')?1:0))*(b.eMad>=b.round?2:1)); e.sm=Math.max(0,npcSmOf(e)-_c); if(e.master&&e.seals>1&&e.sm<15){ e.seals--; e.sm=clamp(e.sm+40); log(`${pName(e)}의 마스터가 령주를 긁었다. 흐려지던 윤곽이 다시 짙어졌다.`,'seal'); } E-=e.sm<=0?30:e.sm<15?10:0; }
    if(S.dead) return;
    if(b.endNow){ b.endNow=false; return endBattle(); }
    if(e.tac==='hunter'&&b.round===1) E+=5;
    const d=P-E, fin=b.ctx.final;
    const eN=pName(e), mN=h.name;
    const extra = d>0 ? (kind==='weak'?6:0) : 0;
    let myNP = kind==='art', enNP = eArtHit>0;
    const MP=myParams().p, EP=npcParams(e).p, cl=(x,a,b)=>Math.max(a,Math.min(b,x));
    const night=w.tod==='밤', atkK=kind==='magic'||kind==='burst'?kind:'round';
    let eK='round'; if(MG.npc&&!enNP){ let bv=-9; for(const k of atkKinds(eh2)){ const v=atkVal(k,eh2,EP,h,MP,night); if(v>bv+.02){bv=v;eK=k;} } } b.eK=eK;
    const agi=(PV(MP[1])-PV(EP[1]))*.02, outM=atkM(atkK,h,MP,eh2,EP,night)*udM(h,eh2)*sjDayM(h)*(b.ctx.raid?.6:1)*(h.sp==='gate'?1.06:1)*(h.id==='enkidu'&&w.morph==='atk'?1.15:1)*npTakeM(b,'en')*npDealM(b,'me'), inM=atkM(eK,eh2,EP,h,MP,night)*udM(eh2,h)*sjDayM(eh2)*(b.ctx.raid?.8:1)*(h.id==='enkidu'&&w.morph==='def'?.85:1)*(eh2.sp==='gate'?1.06:1)*npTakeM(b,'me')*npDealM(b,'en')*(e.bx?BXK.logos:1);"""

NEW_CLASH_MATH = """    b.dodged=null; b.judgedNow=b.judged; b.sealNow=b.sealBuff===b.round;
    const _immOn=b.eyeImmob&&b.eyeImmob.until>=b.round, _immNext=_immOn&&b.immobNext;
    const _illOn=b.eyeIll&&b.eyeIll.until>=b.round, _clrOn=b.eyeClair&&b.eyeClair.until>=b.round, _vtOn=b.eyeVTheft&&b.eyeVTheft.until>=b.round, _dthOn=b.eyeDeath&&b.eyeDeath.until>=b.round, _dthFull=_dthOn&&b.eyeDeath.mode!=='blur';
    if(_immNext){ b.immobNext=0; bonus+=(b.eyeImmob.nextPow||6); }
    const P=myPower({e,defend:b.ctx.defend,judged:b.judged,attack:b.ctx.attack,trap:b.ctx.trap,breach:b.ctx.breach})+bonus+mBon(b)+(b.ctx.final&&w.altar==='me'?6:0)+(b.ctx.final&&w.riteDone?6:0)+(b.ctx.raid?12:0)+initB(b)+(b.mad>=b.round?12:0)+(b.aron?8:0)+(rnd()*36-18)-eSab-(w.sm<=0?30:w.sm<15?10:0)+npFxP(b,'me'); b.judged=false;
    let E=npcPower(e,true)-eMal(b)+(rnd()*36-18)+(b.ctx.hunted?(w.hid?HUNT_E/2:HUNT_E):0)+(b.ctx.final&&e.altar?6:0)+(b.ctx.claim&&b.ctx.attack&&e.altarPre?10:0)+(e.tac==='reckless'?6:0)+npcAct(b,e)+npcInitB(b)+(b.ctx.hostage&&b.round<=2?10:0)-sab+(b.ctx.attack?eWsB(e):0)-(b.compChk&&b.compChk.r===b.round?b.compChk.v:0);
    if(_vtOn) E-=Math.min(6,SV(eh2,'insight')*1.5);
    E+=npFxP(b,'en'); { const _c=Math.round(((3+ri(0,3))*(H_BY[e.hero].cls==='berserk'?1.4:1)+(SV(H_BY[e.hero],'mad')?1:0))*(b.eMad>=b.round?2:1)); e.sm=Math.max(0,npcSmOf(e)-_c); if(e.master&&e.seals>1&&e.sm<15){ e.seals--; e.sm=clamp(e.sm+40); log(`${pName(e)}의 마스터가 령주를 긁었다. 흐려지던 윤곽이 다시 짙어졌다.`,'seal'); } E-=e.sm<=0?30:e.sm<15?10:0; }
    if(S.dead) return;
    if(b.endNow){ b.endNow=false; return endBattle(); }
    if(e.tac==='hunter'&&b.round===1) E+=5;
    const d=P-E, fin=b.ctx.final;
    const eN=pName(e), mN=h.name;
    const extra = d>0 ? (kind==='weak'?6:0) : 0;
    let myNP = kind==='art', enNP = eArtHit>0;
    const MP=myParams().p, EP0=npcParams(e).p, EP=_immOn?EP0.map((x,i)=>i===1?Math.max(1,PV(x)-b.eyeImmob.agiPen):x):EP0, cl=(x,a,b)=>Math.max(a,Math.min(b,x));
    const night=w.tod==='밤', atkK=kind==='magic'||kind==='burst'?kind:'round';
    let eK='round'; if(MG.npc&&!enNP){ let bv=-9; for(const k of atkKinds(eh2)){ const v=atkVal(k,eh2,EP,h,MP,night); if(v>bv+.02){bv=v;eK=k;} } } b.eK=eK;
    const _tmRaw=npTakeM(b,'en'), _tmD=_dthFull?(1-(1-_tmRaw)*.15):_dthOn?(1-(1-_tmRaw)*.5):_tmRaw;
    const _enRed=_dthFull?1:(1-Math.min(.35,SV(eh2,'evade')*.035*(_immOn?.3:1)))*sgfM(eh2)*kavF(eh2.id,e)*(e.aid==='elder'?.8:1);
    const _enGrd=_dthFull?0:_dthOn?Math.round(grdD(eh2)*.5):grdD(eh2);
    const _eDodgeMul=(_immOn?Math.max(.15,1-(.35+giftF()*.08)):1)*(_clrOn?.55:1);
    const _mDodgeAdd=(_illOn?b.eyeIll.v*.45:0);
    const agi=(PV(MP[1])-PV(EP[1]))*.02, outM=atkM(atkK,h,MP,eh2,EP,night)*udM(h,eh2)*sjDayM(h)*(b.ctx.raid?.6:1)*(h.sp==='gate'?1.06:1)*(h.id==='enkidu'&&w.morph==='atk'?1.15:1)*(_immNext?(b.eyeImmob.nextMul||1.15):1)*_tmD*npDealM(b,'me'), inM=atkM(eK,eh2,EP,h,MP,night)*udM(eh2,h)*sjDayM(eh2)*(b.ctx.raid?.8:1)*(h.id==='enkidu'&&w.morph==='def'?.85:1)*(eh2.sp==='gate'?1.06:1)*npTakeM(b,'me')*npDealM(b,'en')*(e.bx?BXK.logos:1);"""
rp(OLD_CLASH_MATH, NEW_CLASH_MATH)

# Apply _enRed / _enGrd / _eDodgeMul / _mDodgeAdd / Illusion false-target & Death Perception Point-of-Death in clash()
rp(
"      else if(d>=8){ const dmg=Math.max(1,Math.round((Math.round((6+d*.3+extra)*outM*(e.aid==='elder'?.8:1))-grdD(eh2))*(1-Math.min(.35,SV(eh2,'evade')*.035))*sgfM(eh2)*kavF(eh2.id,e))); e.hp=clamp(e.hp-dmg);",
"      else if(d>=8){ const dmg=Math.max(1,Math.round((Math.round((6+d*.3+extra)*outM)-_enGrd)*_enRed)); e.hp=clamp(e.hp-dmg);"
)
rp(
"      const rvS=Math.abs(d)>=8&&ch(revP(d>0?EP:MP))?(d>0?'e':'m'):null; b.rev=null;",
"      const rvS=Math.abs(d)>=8&&ch(revP(d>0?EP:MP)*(d>0&&_illOn?Math.max(.25,1-b.eyeIll.v):1))?(d>0?'e':'m'):null; b.rev=null;"
)
rp(
"      } else if(rvS==='m'){ b.rev='m';\n        const dmg=Math.max(1,Math.round((Math.round((6+8*.3)*outM*(e.aid==='elder'?.8:1))-grdD(eh2))*(1-Math.min(.35,SV(eh2,'evade')*.035))*sgfM(eh2)*kavF(eh2.id,e))); e.hp=clamp(e.hp-dmg); w.hp=clamp(w.hp-ri(1,5));",
"      } else if(rvS==='m'){ b.rev='m';\n        const dmg=Math.max(1,Math.round((Math.round((6+8*.3)*outM)-_enGrd)*_enRed)); e.hp=clamp(e.hp-dmg); w.hp=clamp(w.hp-ri(1,5));"
)
rp(
"      } else if(d>0&&ch(dodgeP(EP[1],MP[1])*(atkK==='magic'?MG.dodge:1)*(fxGet(b,'me','holmes')?0:1))){ b.dodged='e'; w.hp=clamp(w.hp-ri(1,3));",
"      } else if(d>0&&ch(dodgeP(EP[1],MP[1])*(atkK==='magic'?MG.dodge:1)*_eDodgeMul*(fxGet(b,'me','holmes')?0:1))){ b.dodged='e'; w.hp=clamp(w.hp-ri(1,3));"
)
rp(
"        const dmg=Math.max(1,Math.round((Math.round((6+d*.3+extra)*outM*(e.aid==='elder'?.8:1))-grdD(eh2))*(1-Math.min(.35,SV(eh2,'evade')*.035))*sgfM(eh2)*kavF(eh2.id,e))); e.hp=clamp(e.hp-dmg); w.hp=clamp(w.hp-ri(1,5));",
"        const dmg=Math.max(1,Math.round((Math.round((6+d*.3+extra)*outM)-_enGrd)*_enRed)); e.hp=clamp(e.hp-dmg); w.hp=clamp(w.hp-ri(1,5));"
)
rp(
"      } else if(ch(dodgeP(MP[1],EP[1])*(eK==='magic'?MG.dodge:1)*(fxGet(b,'en','holmes')?0:1))){ b.dodged='m'; e.hp=clamp(e.hp-ri(1,3));",
"      } else if(ch((dodgeP(MP[1],EP[1])+_mDodgeAdd)*(eK==='magic'?MG.dodge:1)*(fxGet(b,'en','holmes')?0:1))||(_illOn&&ch(b.eyeIll.v))){ b.dodged='m'; e.hp=clamp(e.hp-ri(1,3));"
)
rp(
"        if(h.sp==='tough') w.hp=clamp(w.hp+3);\n      } else if(ch",
"        if(h.sp==='tough') w.hp=clamp(w.hp+3);\n      } else if(ch"
)
rp(
"if(eh2.sp==='tough') e.hp=clamp(e.hp+3);",
"if(eh2.sp==='tough'&&!_dthOn) e.hp=clamp(e.hp+3);"
)

# Death Perception Point-of-Death trigger & Illusion/Prolongation end-of-round hooks
rp(
"    { const gv=Math.max(b.mGuard&&b.mGuard.r===b.round?b.mGuard.v:0,b.eyeGuard&&b.eyeGuard.until>=b.round?b.eyeGuard.v:0); if(!(myNP||enNP)&&gv&&w.hp<hp0) w.hp=clamp(w.hp+Math.round((hp0-w.hp)*gv)); }",
"""    { const gv=Math.max((b.mGuard&&(b.mGuard.r===b.round||(b.mGuard.until&&b.mGuard.until>=b.round)))?b.mGuard.v:0,b.eyeGuard&&b.eyeGuard.until>=b.round?b.eyeGuard.v:0); if(!(myNP||enNP)&&gv&&w.hp<hp0) w.hp=clamp(w.hp+Math.round((hp0-w.hp)*gv)); }
    if(_dthOn&&b.eyeDeath.mode==='point'&&!b.eyeDeath.pointDone&&e.hp>0&&(myNP||b.rev==='m'||(d>0&&b.dodged!=='e'))){
      b.eyeDeath.pointDone=true; const _g=S.gift;
      if(!e.cx&&!e.bxNun&&ch(.55+(_g&&_g.gr>=5?.25:0))){
        e.hp=0; e.usedRevive=true; e.survUsed=true;
        log(`시선으로 죽음의 점을 꿰뚫었다. ${eN}의 존재가 한순간에 흩어졌다!`,'war');
      } else {
        const _td=ri(18,28); e.hp=clamp(e.hp-_td);
        log(`죽음의 선이 ${eN}의 불멸을 베어 냈다. 재생도 버팀도 허락되지 않는다.`,'war');
      }
    }"""
)

# Immobilization flee penalty in retreat/npcRetreat
rp(
"    if(e.hp<RET&&ch(Math.min(.9,st.rp*fleeP(H_BY[e.hero],npcParams(e).p)/.6)-npFleeMinus(b,'en'))) return 'run';",
"    const _immF=(b.eyeImmob&&b.eyeImmob.until>=b.round)?b.eyeImmob.fleePen:0;\n    if(e.hp<RET&&ch(Math.min(.9,st.rp*fleeP(H_BY[e.hero],npcParams(e).p)/.6)-npFleeMinus(b,'en')-_immF)) return 'run';"
)

# Final Duel: DUEL_EYE, duelEye, duelClash
rp(
"  const DUEL_EYE={charm:'이번 합 서번트가 한 번 더 머뭇거린다 · 서번트 전투력이 떨어진다',bind:'이번 합 서번트가 한 번 더 머뭇거린다 · 서번트 전투력이 떨어진다',flame:'이번 합 서번트 전투력이 크게 떨어진다',stone:'세 합 동안 서번트가 굳는다 · 대마력이 높을수록 덜 듣는다',future:'세 합 동안 받는 피해를 크게 줄인다',jinx:'흉 표식을 새긴다 · 표식 하나마다 서번트 전투력 −5',compel:'세 합 동안 서번트의 공격 방식을 정한다 · 대마력이면 두 합',telek:'이번 합 받는 피해를 줄인다'};",
"""  const DUEL_EYE={charm:'이번 합 서번트가 한 번 더 머뭇거린다 · 서번트 전투력이 떨어진다',bind:'이번 합 서번트가 한 번 더 머뭇거린다 · 서번트 전투력이 떨어진다',flame:'이번 합 서번트 전투력이 크게 떨어진다',stone:'세 합 동안 서번트가 굳는다 · 대마력이 높을수록 덜 듣는다',future:'세 합 동안 받는 피해를 크게 줄인다',jinx:'흉 표식을 새긴다 · 표식 하나마다 서번트 전투력 −5',compel:'세 합 동안 서번트의 공격 방식을 정한다 · 대마력이면 두 합',telek:'이번 합 받는 피해를 줄인다',
    illusion:'두 합 동안 서번트의 인식을 흐려 공격을 빗나가게 하고 거짓 표적을 세운다',
    clairvoyance:'서번트의 동작을 멀리서 읽어 낸다 · 이번 합 공격력과 정밀도가 오른다',
    immob:'두 합 동안 서번트의 민첩과 회피를 꺾고 다음 일격의 위력을 높인다',
    vtheft:'서번트의 시야를 빼앗아 간파와 회피를 꺾는다',
    prolong:'걸려 있는 저주·약화·결계 효과를 연장하고 한층 강하게 만든다',
    death:'체력과 정신을 크게 소모해 결계와 방어를 꿰뚫는 일격을 넣는다'};"""
)
rp(
"      if(eyeOn&&DUEL_EYE[S.gift.id]){ const g=S.gift, once=['stone','future','compel'].includes(g.id), used=once&&D.used.eye, gc=giftCost();",
"      if(eyeOn&&DUEL_EYE[S.gift.id]){ const g=S.gift, once=['stone','future','compel','prolong'].includes(g.id), used=once&&D.used.eye, gc=giftCost(), reqOk=g.id!=='death'||(S.st.will>=35&&D.mhp>gc+15);"
)
rp(
"        cs.push({grp:'eye',t:GIFTS[g.id].n,d:`${DUEL_EYE[g.id]}${once?' · 결투에서 한 번':''} ${used?'[이미 썼다]':gc?`[건강 −${gc}]`:'[대가 없음]'}`,off:used||D.mhp<=gc+5,f:()=>{ if(once) D.used.eye=1; D.mhp-=gc; duelEye(g.id); return duelPre(GIFTS[g.id].n); }}); }",
"        cs.push({grp:'eye',t:GIFTS[g.id].n,d:`${DUEL_EYE[g.id]}${once?' · 결투에서 한 번':''} ${used?'[이미 썼다]':!reqOk?'[정신·건강 부족]':gc?`[건강 −${gc}]`:'[대가 없음]'}`,off:used||!reqOk||D.mhp<=gc+5,f:()=>{ if(once) D.used.eye=1; D.mhp-=gc; duelEye(g.id); return duelPre(GIFTS[g.id].n); }}); }"
)
rp(
"    else if(id==='telek') P.guard=Math.max(P.guard||0,Math.min(.5,.2+F*.03));",
"""    else if(id==='telek') P.guard=Math.max(P.guard||0,Math.min(.5,.2+F*.03));
    else if(id==='illusion'){ D.eyeIll={until:D.r+1,v:Math.min(.45,.14+F*.05)}; P.reroll=true; P.deb=(P.deb||0)+Math.round(4+F); }
    else if(id==='clairvoyance'){ D.eyeClair={until:D.r+1,v:Math.round(4+F*1.5)}; P.pow=(P.pow||0)+Math.round(4+F*1.5); }
    else if(id==='immob'){ D.eyeImmob={until:D.r+1,agiPen:Math.min(3,1+Math.floor(F/2)),nextPow:Math.round(6+F*2)}; P.pow=(P.pow||0)+Math.round(6+F*2); }
    else if(id==='vtheft'){ D.eyeVTheft={until:D.r+1,v:Math.round(5+F*1.5)}; P.deb=(P.deb||0)+Math.round(5+F*1.5); }
    else if(id==='prolong'){ const ext=(S.gift.ctl||0)>=2?2:1, mul=1.3; if(D.curse&&D.curse.until>=D.r){ D.curse.until+=ext; D.curse.v=Math.round(D.curse.v*mul); } if(D.eyeDeb&&D.eyeDeb.until>=D.r){ D.eyeDeb.until+=ext; D.eyeDeb.v=Math.round(D.eyeDeb.v*mul); } if(D.eyeGuard&&D.eyeGuard.until>=D.r){ D.eyeGuard.until+=ext; D.eyeGuard.v=Math.min(.75,D.eyeGuard.v*mul); } if(D.compel>=D.r) D.compel+=ext; if(D.hesUp>=D.r) D.hesUp+=ext; if(P.pow) P.pow=Math.round(P.pow*mul); if(P.deb) P.deb=Math.round(P.deb*mul); D.sWall=D.sWall>=D.r?D.sWall:0; D.wallM=D.wallM>=D.r?D.wallM+ext:0; }
    else if(id==='death'){ add({will:-3}); D.eyeDeath={until:D.r+1,gr:S.gift.gr}; P.pow=(P.pow||0)+Math.round(8+F*1.5); }"""
)
rp(
"    const sTake=x=>Math.max(1,Math.round((x-grdD(h))*(1-Math.min(.35,SV(h,'evade')*.035))*sgfM(h)*(D.sWall>=D.r?.5:1)));",
"    const _dDeath=D.eyeDeath&&D.eyeDeath.until>=D.r; const sTake=x=>_dDeath?Math.max(1,Math.round(x*(D.sWall>=D.r?.85:1))):Math.max(1,Math.round((x-grdD(h))*(1-Math.min(.35,SV(h,'evade')*.035))*sgfM(h)*(D.sWall>=D.r?.5:1)));"
)
rp(
"      else if(d>0){ if(ch(dodgeP(h.s[1],M.P[1])*(kind==='magic'?MG.dodge:1))){ hitMe(ri(1,3)); log(`${n}${J(n,이)} 당신의 공격을 흘려 냈다.`,'war'); }",
"      else if(d>0){ const _dIm=D.eyeImmob&&D.eyeImmob.until>=D.r, _dCl=D.eyeClair&&D.eyeClair.until>=D.r, _eAg=_dIm?Math.max(1,PV(h.s[1])-D.eyeImmob.agiPen):h.s[1]; if(ch(dodgeP(_eAg,M.P[1])*(kind==='magic'?MG.dodge:1)*(_dIm?.35:1)*(_dCl?.55:1))){ hitMe(ri(1,3)); log(`${n}${J(n,이)} 당신의 공격을 흘려 냈다.`,'war'); }"
)
rp(
"      else { if(ch(dodgeP(M.P[1],h.s[1])*(sk==='magic'?MG.dodge:1))){ D.shp-=ri(1,3); log(`${n}의 일격을 간신히 피했다.`,'war'); }",
"      else { const _dIl=D.eyeIll&&D.eyeIll.until>=D.r; if(ch((dodgeP(M.P[1],h.s[1])+(_dIl?D.eyeIll.v*.45:0))*(sk==='magic'?MG.dodge:1))||(_dIl&&ch(D.eyeIll.v))){ D.shp-=ri(1,3); log(`${n}의 일격을 간신히 피했다.`,'war'); }"
)

if miss:
    for x in miss:
        print('못 찾음', x)
    sys.exit(1)

open(P, 'w', encoding='utf-8').write(s)
print('eyes1125 적용 끝')

# Update i18n
from eyes_lines import D, T
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
