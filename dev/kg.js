  /* ---------- 11-21: 검귀 루트 「검을 거두지 않은 자」 — 진짜 소원 · 나흘 · 결말 ①~⑥ ----------
     설계: 시트 「검귀 루트 시안」 · 「검귀 에필로그 안」 · 「검귀 서번트별 대사」
     상태는 S.war.kg = {k 성향 · d 날 · R 결심 · sus 의심 · bet 배신 갈래 · lock 령주로 묶음 · prom 약속 · mem 기억 · walk 넷째 날 · who 둘째 날의 사람 · saved · ally 동맹 조 i}
     나흘 동안 w.ended를 켜 두어 평소의 낮 · 밤 진행을 멈추고, 큐로만 흘러간다
     결말: m 마스터 승(①) · s 서번트 승(①) · t 함께 간다(②) · b 묶인 잔(③) · f 함께 가는 척한다(④) · p 돌아선다(⑤) · x 손을 놓친 잔(⑥) */
  const KG_K=['avenger','judge','cruel','taboo','zeal'];
  const KG_W={
    avenger:{wish:'나를 짓밟은 모든 것에 갚는다',omen:'아침 신문의 부고란이 길어졌다. 당신이 오래 품어 온 명단의 이름이 하나씩 지워지고 있다.',ok:['무자비','계략'],ng:['희생','구조']},
    judge:{wish:'누구도 거역할 수 없는 정의',omen:'거리의 사람들이 같은 시각에 같은 말을 한다. 다투는 소리가 사라졌다.',ok:['규율','정면승부'],ng:['계략','구조']},
    cruel:{wish:'약한 것이 없는 세상',omen:'병원의 불이 하나씩 꺼진다. 거리에서 노인과 아이가 보이지 않는다.',ok:['무자비'],ng:['구조','희생']},
    taboo:{wish:'문 너머를 이쪽으로 연다',omen:'밤마다 도시의 문이 열린 채로 있다. 거울에 비치지 않는 사람이 늘었다.',ok:['계략'],ng:['규율','구조']},
    zeal:{wish:'이 도시 전부를 근원에 닿는 디딤돌로 쓴다',omen:'영맥이 한 방향으로 쏠린다. 도시의 시계들이 조금씩 늦어진다.',omenN:'도시의 시계들이 조금씩 늦어진다. 무언가가 한 방향으로 쏠리는 것이 느껴진다.',ok:['계략'],ng:['희생','구조']}};
  // 둘째 날의 대가: 그 사람이 겪는 일 (성향별)
  const KG_COST={avenger:w=>`오래전 다툰 적 있는 ${w}${J(w,이)} 쓰러졌다. 그 이름도 명단에 있었다.`,judge:w=>`${w}${J(w,이)} 작은 거짓말 하나 때문에 굳어 버렸다.`,cruel:w=>`앓고 있던 ${w}의 숨이 가늘어졌다.`,taboo:w=>`${w}의 그림자가 반쯤 지워졌다.`,zeal:w=>`마력 회로가 없는 ${w}${J(w,이)} 잠에서 깨지 않는다.`};
  /*KG_DATA*/
  const kgW=()=>S.war&&S.war.kg;
  const kgDeep=()=>{ let b=null; for(const k of KG_K){ const v=(S.aff&&S.aff[k])||0; if(v>=8&&(!b||v>((S.aff&&S.aff[b])||0))) b=k; } return b; };
  const kgSt=()=>((relOf()||{}).stage)||0;
  const kgLover=()=>{ const r=relOf(); return !!r&&r.stage>=3; };
  const kgMu=st=>[1,1.25,1.5,2][Math.max(0,Math.min(3,st||0))];
  // 에필로그 조건에 쓰는 것들
  const kgS=()=>S.flags.kgSt||0;
  const kgMuteH=()=>!!S.hero&&!!H_BY[S.hero]&&VREG(H_BY[S.hero])==='mute';
  const kgFriend=()=>!!S.flags.friendKnows||S.st.bond>=35;
  const kgSeals=()=>(S.war&&S.war.seals)||0;
  const kgUseSeal=()=>{ if(S.war) S.war.seals=Math.max(0,(S.war.seals||0)-1); };
  const kgRel=n=>{ const r=relOf(); if(r) r.pt=clamp(r.pt+n); };
  const kgAllyP=()=>S.flags.kgAllyI!=null&&S.war?(S.war.pairs||[]).find(p=>p.i===S.flags.kgAllyI):null;
  const kgAllyAlive=()=>!!kgAllyP()&&!S.flags.kgAllyFell;
  const kgAllyFell=()=>!!kgAllyP()&&!!S.flags.kgAllyFell;
  const kgAllySv=()=>{ const p=kgAllyP(); return !!p&&p.alive; };
  // 말씨에 맞춘 한 줄: [반말, 존댓말, 왕의 말, 몸짓(말을 잃은 서번트)]
  function kgSayRaw(h,v){ const r=VREG(h); return r==='mute'?v[3]:r==='polite'?v[1]:r==='royal'?(v[2]||v[0]):v[0]; }
  function kgSay(h,v){ return voiceLine(h,kgSayRaw(h,v)); }
  function kgSV(h,i){ const a=KG_SV[h.id]; return a&&a[i]?voiceLine(h,a[i]):''; }
  // 에필로그에서 서번트별 한마디를 들려준다. who='ally'면 동맹 서번트가 전한다
  function kgSvSay(i,who){ const h=H_BY[S.hero]; if(!h) return; const a=KG_SV[h.id]; const l=a&&a[i]; if(!l) return;
    if(who==='ally'){ const p=kgAllyP(), ah=p&&H_BY[p.hero]; if(ah){ log(voiceLine(ah,l),'voice'); return; } }
    log(voiceLine(h,l),'voice'); }
  const KG_ALLYR=a=>['lord','heir','antique','elder'].includes(a&&a.aid)?2:['mother','lecturer','fortune','detective','exorcist','apostle','burial','executor','exec','veteran'].includes(a&&a.aid)?1:0;
  function kgAllySay(){ const p=kgAllyP(); const n=S.flags.kgAllyN||''; const l=KG_ALLYV[KG_ALLYR(p)]; log(n?`${n}: “${l}”`:`“${l}”`,'enemy'); }
  // 진짜 소원을 고를 수 있는가: 성향이 깊음(8 이상) · 서번트가 곁에 있다 · 검은 성배 위기가 아니다
  function kgCan(){ const w=W(); return !!kgDeep()&&w.heroAlive&&!w.crisis&&!w.arsNova&&!w.selfGone&&!S.flags.kgOff; }
  function kgOffer(ch_,shared){ if(!kgCan()) return; const k=kgDeep(), X=KG_W[k];
    const lab=`본성 속 진심: “${X.wish}”`, L=ch_.map(c=>c.t).concat(lab);   // 진입 연출: 성배 선택 창의 줄들 그대로
    ch_.push({t:lab,d:`마음 가장 깊은 곳의 「${AFFN[k]}」. 잔이 가득 차기까지 나흘이 걸린다`,f:()=>kgStart(k,shared,L)}); }
  // 결심 시작값 (시트 20~26줄)
  function kgRes0(k){ const h=hero(), w=W(), st=kgSt(), t=Math.max(.5,Math.min(1.5,w.trust/60)); let R=40;
    for(const x of h.traits) R+=x==='명예'?10:x==='연민'?15*(1+.25*st):x==='자유'?5:x==='충성'?-5*t:x==='야망'?-10*t:0;
    const al=(HAL[h.id]||'NB')[1]; R+=al==='G'?10:al==='E'?-10:0;
    const L=HLK[h.id]||{}, X=KG_W[k]; for(const g of X.ok) if((L[g]||0)>0) R-=10; for(const g of X.ng) if((L[g]||0)>0) R+=10;
    R+=w.trust>=80?-10:w.trust>=60?-5:w.trust>=40?0:10;
    R+=[0,5,10,15][st];
    return Math.max(0,Math.min(100,Math.round(R))); }
  // 배신 갈래: 결심 60 이상 · 계략이나 무자비를 좋아하거나 혼돈 · 첫째 성향이 명예가 아님 · 아이 서번트는 아님
  function kgBetrayOK(h,R){ const L=HLK[h.id]||{}; return R>=60&&!REL_CHILD.includes(h.id)&&h.traits[0]!=='명예'&&((L['계략']||0)>0||(L['무자비']||0)>0||(HAL[h.id]||'')[0]==='C'); }
  // 둘째 날의 가까운 사람: 가족 → 친구 → 제자 → 이웃. 근원 집착은 회로 없는 사람에게 닿으니 마술 가문이면 가족을 건너뛴다
  function kgWho(k){ const F=S.fam||{}, magicHouse=['noble','noble2','fallen'].includes(S.origin);
    if(!(k==='zeal'&&magicHouse)){
      if(F.spouse&&F.spouse.alive) return {kind:'fam',t:'배우자'};
      const kid=(F.kids||[]).find(x=>x&&x.alive!==false); if(kid) return {kind:'fam',t:kid.sex==='f'?'딸':'아들'};
      if(F.mother&&F.mother.alive) return {kind:'fam',t:'어머니'};
      if(F.father&&F.father.alive) return {kind:'fam',t:'아버지'};
      if(S.origin==='orphan') return {kind:'fam',t:'보육원 원장'};
      if(F.sib) return {kind:'fam',t:'형제'}; }
    if(kgFriend()) return {kind:'friend',t:'오랜 친구'};
    if(S.flags.student) return {kind:'pupil',t:'제자'};
    return {kind:'nbr',t:'옆집 이웃'}; }
  function kgR(d){ const g=kgW(); if(!g||g.lock) return; g.R=Math.max(0,Math.min(100,g.R+d*kgMu(kgSt()))); }
  const KG_DAYN=['첫째 날','둘째 날','셋째 날','넷째 날'];
  function kgStart(k,shared,lines){ const w=W(), X=KG_W[k], h=hero();
    S.flags.wishText=X.wish; S.flags.kg=k; S.flags.kgShared=shared?1:0;
    const R=kgRes0(k);
    w.kg={k,d:0,R,R0:R,sus:0,bet:kgBetrayOK(h,R),lock:false,prom:null,mem:null,walk:null,who:null,saved:null,ally:shared?shared.i:null,done:false};
    if(w.kg.ally==null){ const a=(w.pairs||[]).find(p=>p.alive&&p.ally); if(a) w.kg.ally=a.i; }
    w.ended=true; w.queue=[]; w.final=false;
    log(`성배 앞에서 손을 거두었다. 목록 맨 아래, 아무에게도 말하지 않은 소원이 하나 있었다. “${X.wish}.”`,'war',{fx:{t:'kgin',wish:X.wish,lines:lines||[]}});
    log('잔은 그 소원을 받아 들었다. 다만 바닥만 젖었을 뿐, 아직 차지 않았다. 가득 차기까지 나흘이 걸린다.','war');
    wrec('hint',`본성 속 진심 — ${X.wish}`);
    w.queue.push(()=>kgDay());
    return ''; }
  // 11-22: 선택지에 서번트 결심 · 성향 · 신뢰 변화를 칩으로 보인다 (결심이 령주에 묶였으면 결심 칩은 빼 둔다)
  const kgCh=o=>{ const g=kgW(), A=[], ar=(n,b)=>(n>0?'↑':'↓').repeat(Math.abs(n)>=b?2:1);
    if(o.R&&g&&!g.lock) A.push({l:'서번트 결심 '+ar(o.R,10),c:''});
    if(o.a&&g) A.push({l:`「${AFFN[g.k]}」 성향 ${o.a>0?'↑':'↓'}`,c:''});
    if(o.t) A.push({l:'신뢰 '+ar(o.t,10),c:o.t>0?'up':'dn'});
    if(o.hp) A.push({l:'서번트 건강 ↓',c:'dn'});
    return A.length?A:undefined; };
  const kgPut=()=>({t:'잔을 내려놓는다',chips:kgCh({a:-1}),d:kgW()&&kgW().d>=4?'마지막 기회. 그 진심을 잔에 맡기지 않고, 서번트와 함께 잔을 부순다':'그 진심을 잔에 맡기지 않고, 서번트와 함께 잔을 부순다',f:()=>kgPutDown()});
  // 낮: 그날의 일
  function kgDay(){ const w=W(), g=w.kg; if(!g||g.done||S.dead) return; const h=hero();
    g.d++; w.day++; w.tod='낮'; w.prog=0; mark('war');
    log(`진심 · ${KG_DAYN[g.d-1]}`,'night',{fx:{t:'kgday',d:g.d,ev:['흔적','가까운 사람','다른 손','평범한 하루'][g.d-1]}});
    w.queue.unshift(()=>kgDayEv()); }   // 11-22: 날 카드 연출이 끝난 뒤(연출 동안 진행이 멈춘다) 그날 사건
  function kgDayEv(){ const w=W(), g=w.kg; if(!g||g.done||S.dead) return; const h=hero();
    if(g.d===1){ const om=g.k==='zeal'&&!isMage()?KG_W.zeal.omenN:KG_W[g.k].omen;
      decide({title:'흔적',body:`아침 뉴스가 이상한 일을 짧게 전한다. ${om} 잔은 아직 바닥만 젖어 있다.`,war:true,choices:[
        {t:'보러 간다',d:'징조를 가까이서 본다',chips:kgCh({a:1,R:5}),f:()=>{ lean(g.k,1); kgR(5); w.queue.push(()=>kgNight()); return '징조를 가까이서 보았다. 그것은 당신이 바란 모양을 하고 있었다.'; }},
        {t:'모른 척한다',auto:true,f:()=>{ w.queue.push(()=>kgNight()); return '신문을 접었다. 오늘은 아무 일도 없었던 것으로 했다.'; }},kgPut()]}); return; }
    if(g.d===2){ const who=g.who=kgWho(g.k); S.flags.kgWho=who.kind;
      decide({title:'가까운 사람',body:`${KG_COST[g.k](who.t)} 이번 생에 실제로 있는 사람이다. 잔이 무엇을 대가로 차오르는지, 이제 알았다.`,war:true,choices:[
        {t:'지킨다',d:'잔에 고인 것을 그 사람 쪽에서 거둔다',chips:kgCh({a:-1,R:-10}),f:()=>{ lean(g.k,-1); kgR(-10); g.saved=1; S.flags.kgSaved=1; w.queue.push(()=>kgNight()); return '잔에 고인 것을 그 사람 쪽에서 거두었다. 그 사람은 무사했다. 잔이 조금 얕아졌다.'; }},
        {t:'내버려 둔다',auto:true,chips:kgCh({a:1,R:15}),f:()=>{ lean(g.k,1); kgR(15); g.saved=0; S.flags.kgSaved=0; w.queue.push(()=>kgNight()); return '그대로 두었다. 그 사람은 회복하지 못했다. 잔은 조금 더 차올랐다.'; }},kgPut()]}); return; }
    if(g.d===3){ const a=kgAlly(), who=a?`동맹 ${a.mname}`:'감독관', meet=g.R>=50||g.bet;
      if(!meet){ decide({title:'다른 손',body:`${who}${J(who,이)} 잔을 노리고 움직였다. 해가 지기 전에 거처의 결계가 흔들렸다.`,war:true,choices:[
        {t:'맞선다',auto:true,chips:kgCh({R:-5,hp:1}),f:()=>{ w.hp=Math.max(5,w.hp-ri(8,15)); kgR(-5); if(a) a.kgBack=1; w.queue.push(()=>kgNight()); return `${h.name}${J(h.name,이)} 당신 앞을 막아섰다. 짧은 싸움 끝에 그들은 물러났다.`; }},kgPut()]}); return; }
      const seen=S.st.lore>=60||g.bet;
      decide({title:'다른 손',body:`${who}${J(who,이)} 잔을 노리고 움직이기 시작했다. ${seen?'거처 문턱에 낯선 마력의 흔적이 남아 있었다. 서번트가 그쪽과 닿은 흔적이다.':'서번트가 어디론가 다녀온 기척이 있다.'}`,war:true,choices:[
        {t:'모른 척한다',auto:true,f:()=>{ if(a) a.kgBack=1; w.queue.push(()=>kgNight()); return '모른 척했다. 서번트도 아무 말 하지 않았다.'; }},
        {t:'따진다',d:'어디에 다녀왔는지 묻는다',chips:kgCh({R:5}),f:()=>{ kgR(5); g.sus++; if(a) a.kgBack=1; w.queue.push(()=>kgNight()); return '어디에 다녀왔느냐고 따졌다. 서번트는 대답 대신 당신을 오래 보았다.'; }},
        {t:'령주로 묶는다',seal:true,off:w.seals<1,chips:kgCh({t:-10}),d:`서번트의 마음을 지금 자리에 묶는다 · 신뢰가 크게 떨어진다 [령주 1획 · 남은 ${w.seals}획]`,f:()=>{ useSeal('내 곁을 떠나지 마라'); g.lock=true; w.trust=clamp(w.trust-10); if(a) a.kgBack=1; w.queue.push(()=>kgNight()); return '령주가 타올랐다. 서번트의 마음은 그 자리에 묶였다.'; }},kgPut()]}); return; }
    if(g.d===4){
      decide({title:'평범한 하루',body:kgSay(h,['오늘 하루만, 아무 일 없는 날로 하자.','오늘 하루만, 아무 일 없는 날로 보내시지요.','오늘 하루만은 아무 일 없는 날로 하자꾸나.','(서번트가 외투를 들고 문가에 선다. 오늘은 그냥 나가자는 얼굴이다.)']),war:true,choices:[
        {t:'같이 걷는다',d:'그 겨울에 지나간 길을 걷는다',auto:true,f:()=>{ g.walk='walk'; S.flags.kgWalk='walk'; kgDusk(); return '그 겨울에 지나간 길을 걸었다. 둘 다 그날의 이야기를 하지 않았다.'; }},
        {t:'밥을 먹는다',d:'서번트가 좋아하던 것을 먹는다',f:()=>{ g.walk='eat'; S.flags.kgWalk='eat'; kgDusk(); return '서번트가 좋아하던 것을 먹었다. 맛있었다. 그게 이상했다.'; }},kgPut()]}); return; } }
  function kgDusk(){ const w=W(), g=w.kg, h=hero();
    if(g.bet) w.queue.push(()=>{ log('해 질 녘, 헤어질 때 하는 말 같은 것을 들었다.','n'); log(kgSay(h,['오늘은 고마웠어. 정말로.','오늘은 고마웠습니다. 정말로.','오늘은 고마웠다. 진심으로.','(헤어질 때처럼, 서번트가 당신의 손을 오래 쥐었다.)']),'voice'); });
    w.queue.push(()=>kgNight()); }
  // 밤: 서번트가 말을 건다
  function kgNight(){ const w=W(), g=w.kg; if(!g||g.done||S.dead) return; const h=hero();
    w.tod='밤'; log(`진심 · ${KG_DAYN[g.d-1]} 밤`,'night');
    const next=()=>w.queue.push(()=>kgDawn());
    if(g.d===1){ const q=g.bet?kgSay(h,['좋아. 네가 바라는 거라면 따르지.','좋습니다. 당신이 바라신다면 따르겠습니다.','좋다. 그대가 바란다면 짐도 따르마.','(서번트가 고개를 끄덕인다. 생각보다 빨랐다.)'])+'\n평소답지 않게, 대답이 너무 빨랐다.'
        :kgSay(h,['그 소원, 언제부터였어.','그 소원, 언제부터였습니까.','그 소원, 언제부터였느냐.','(서번트가 낮의 신문을 당신 앞에 내려놓는다. 묻는 눈이다.)']);
      const lean0=h.traits[0]==='명예'||h.traits[0]==='연민'?5:h.traits[0]==='충성'||h.traits[0]==='야망'?-5:0;
      decide({title:'물음',body:`징조를 본 서번트가 처음으로 물었다.\n${q}`,war:true,choices:[
        {t:'정직하게 말한다',auto:true,chips:kgCh({R:-5}),f:()=>{ kgR(-5); next(); return '오래전부터였다고 말했다. 서번트는 오래 말이 없었다.'; }},
        {t:'둘러댄다',chips:kgCh({R:10,t:-5}),f:()=>{ kgR(10); w.trust=clamp(w.trust-5); next(); return '성배가 보여 준 것일 뿐이라고 둘러댔다. 서번트는 더 묻지 않았다.'; }},
        {t:'되묻는다',d:'“너라면 무엇을 빌었겠나”',chips:kgCh({R:lean0}),f:()=>{ kgR(lean0); next(); return `${h.name}${J(h.name,은)} 자신의 소원을 이야기했다. “${h.wish}.”`; }}]}); return; }
    if(g.d===2){ const q=g.bet?kgSay(h,['약속은 네가 지키면 돼.','약속은 당신이 지키시면 됩니다.','약속은 그대가 지키면 될 일이다.','(서번트가 당신의 손을 한 번 두드리고 거둔다.)'])+'\n서번트는 약속을 청하지 않았다.'
        :kgSay(h,['다 이루어진 뒤에도, 지금의 네가 남아 있겠다고 말해 줘.','다 이루어진 뒤에도, 지금의 당신이 남아 있겠다고 말해 주십시오.','다 이루어진 뒤에도, 지금의 그대가 남아 있겠다고 말하라.','(서번트가 손등의 령주 자국을 가리키고, 당신의 가슴을 가리킨다.)']);
      decide({title:'약속',body:`낮의 일을 본 서번트가 약속을 청했다.\n${q}`,war:true,choices:[
        {t:'약속한다',auto:true,chips:kgCh({R:-10}),f:()=>{ kgR(-10); g.prom='kept'; S.flags.kgProm='yes'; next(); return '약속했다. 서번트가 짧게 고개를 끄덕였다.'; }},
        {t:'거절한다',chips:kgCh({R:10}),f:()=>{ kgR(10); S.flags.kgProm='no'; next(); return '약속할 수 없다고 했다.'; }},
        {t:'대답하지 않는다',chips:kgCh({R:5}),f:()=>{ kgR(5); S.flags.kgProm='no'; next(); return '대답하지 않았다. 밤이 길었다.'; }}]}); return; }
    if(g.d===3){ const sc=pick(['처음 만난 밤의 이야기였다.','함께 넘긴 위기의 밤 이야기였다.',...(kgSt()>=1?['인연이 깊어진 밤의 이야기였다.']:[])]);
      const q=kgSay(h,['그날의 너는 지금과 같은 사람이었어?','그날의 당신은 지금과 같은 사람이었습니까.','그날의 그대는 지금과 같은 자였느냐.','(서번트가 그날 밤의 자리를 손끝으로 가리키고, 당신을 본다.)']);
      const odd=g.bet?'\n서번트는 그날 비가 왔다고 했다. 당신이 기억하는 그날은 맑았다.':'';
      decide({title:'기억',body:`서번트가 그 겨울의 장면 하나를 꺼냈다. ${sc}${odd}\n${q}`,war:true,choices:[
        {t:'같은 사람이다',auto:true,chips:kgCh({R:-5}),f:()=>{ kgR(-5); g.mem='same'; next(); return '같은 사람이라고 했다. 서번트의 눈이 아주 조금 흔들렸다.'; }},
        {t:'그때와는 다르다',chips:kgCh({R:10}),f:()=>{ kgR(10); g.mem='diff'; next(); return '그때와는 다르다고 했다. 서번트는 고개를 끄덕였다.'; }},
        {t:'그때도 이랬다',chips:kgCh({R:5,t:5}),f:()=>{ kgR(5); w.trust=clamp(w.trust+5); g.mem='again'; next(); return '그때도 이랬다고 했다. 서번트는 그 정직함을 오래 보았다.'; }},
        ...(g.bet?[{t:'그날은 맑았다',d:'서번트의 말이 기억과 다르다',f:()=>{ g.sus++; g.mem='diff'; next(); return '그날은 맑았다고 말했다. 서번트가 아주 잠깐 입을 다물었다.'; }}]:[])]}); return; }
    // 넷째 날 밤: 잔이 가득 찬다
    kgFinal(); }
  function kgDawn(){ const w=W(), g=w.kg; if(!g||g.done||S.dead) return; w.tod='새벽';
    // 11-22: 성배전쟁 새벽과 같은 회복 — 서번트 건강은 dawn() 공식(마력 · 결계 · 재생/치유 스킬 · 영맥), 마력은 smRegen(6). 마스터 건강은 쉬는 밤처럼 +4(치유 마술 · 재생 능력이 있으면 더)
    { const h=hero(); w.hp=clamp(w.hp+2+S.st.mana*.06+Math.min(w.fort||0,50)*.03+SV(h,'regen')*1+SV(h,'heal')*.6+2*wsF()); } smRegen(6); S.st.health=Math.min(100,S.st.health+4+artLv('heal')*2+(artLv('regen')?5:0));   // 치유 마술 단계마다 +2 · 재생 능력 +5
    w.queue.push(()=>kgDay()); }
  // 잔을 내려놓는다 → ⑤
  function kgPutDown(){ const w=W(), g=w.kg, h=hero(); g.done=true; g.end='p'; S.flags.kgEnd='p'; S.flags.kg5=1;
    log('잔에서 손을 뗐다. 본성 속 진심은 끝내 잔에 맡기지 않았다.','war'); lean(g.k,-3);
    const ok=w.trust>=STAY_NEED;
    w.queue.push(()=>decide({title:'잔을 내려놓은 손',body:`${h.name}${J(h.name,이)} 당신 곁에 섰다. 바닥만 젖은 잔이 제단 위에 놓여 있다.`,war:true,choices:[
      {t:'함께 잔을 부순다',auto:true,f:()=>{ S.flags.brokeCup=1; S.flags.wishText='본성 속 진심을 잔에 맡기지 않고 서번트와 함께 잔을 부쉈다'; add({will:8}); S.flags.endFx='kgP';
        log(`${h.name}${J(h.name,이)} 잔을 내리쳤다. 당신의 손도 그 위에 있었다.`,'war'); kgClose(); farewell(); return '잔은 둘의 손으로 부서졌다.'; }},
      {t:`잔의 빛으로 ${h.name}${J(h.name,을)} 남긴다`,off:!ok,d:ok?'남은 빛을 서번트가 몸을 얻는 데 쓴다':'신뢰가 모자라 서번트를 이 세계에 붙잡아 둘 수 없다',foot:ok?undefined:[['필요',[`신뢰 ${STAY_NEED}`]],['현재',[`신뢰 ${Math.round(w.trust)}`]]],f:()=>{ S.flags.wishText='본성 속 진심을 잔에 맡기지 않고 서번트를 남겼다'; S.flags.stay=h.id; add({bond:6}); S.flags.endFx='kgP2';
        log(`바닥에 고였던 빛이 ${h.name}에게 스며들었다. 잔은 그 자리에서 금이 갔다.`,'war'); kgClose(); warOver(); return '그 진심 대신, 곁에 남는 쪽을 골랐다.'; }}]}));
    return ''; }
  function kgClose(){ const w=W(); if(w.kg) w.kg.done=true; S.flags.kgSt=kgSt(); S.flags.kgSus=w.kg?w.kg.sus:0; S.flags.kgLover=kgLover()?1:0; }
  // 마지막 밤의 갈래 (시트 35줄)
  function kgFinal(){ const w=W(), g=w.kg; g.fin=1; const a=kgAlly(); const gone=((S.aff&&S.aff[g.k])||0)<8;
    fxOnly({t:'kgfull',v:gone?'g':'r'});   // 잔이 가득 차는 순간 (성향이 옅어졌으면 금빛)
    if(gone){ g.done=true; S.flags.kgOff=1; log('잔이 가득 찼지만, 마음 가장 깊은 곳의 그 소원은 이제 거기 없었다. 나흘 사이에 무언가가 바뀌어 있었다.','war'); w.queue=[]; finale(a&&S.flags.kgShared?a:null); return; }
    if(g.bet&&g.R>=60){ log('잔이 가득 찼다.','war'); return kgBetray(); }
    if(g.R>=60) return kgDuel(g.R);
    if(g.R>=35) return kgSealAsk();
    log('잔이 가득 찼다.','war'); kgTogether(false); }
  function kgAlly(){ const w=W(), g=w.kg; if(!g||g.ally==null) return null; const p=w.pairs.find(x=>x.i===g.ally); return p&&p.alive?p:null; }
  const kgMR=h=>(SK[h.id]||[]).some(([n,r])=>/^대마력/.test(n)&&RANKV[r]>=RANKV.A);
  function kgSealAsk(){ const w=W(), g=w.kg, h=hero();
    const self=()=>{ if(g.R>=50) kgDuel(g.R); else kgTogether(false); };
    if(w.seals<1){ log(`손등에 남은 령주가 없다. ${h.name}${J(h.name,이)} 스스로 정했다.`,'war'); return self(); }
    decide({title:'마지막 밤',body:`잔이 가득 찼다. ${h.name}${J(h.name,은)} 아직 정하지 못한 얼굴이다. 손등에 령주가 ${w.seals}획 남아 있다.`,war:true,choices:[
      {t:'령주로 명한다',seal:true,d:`“함께 이 소원을 이뤄라.” 서번트를 묶는다 [령주 1획 · 남은 ${w.seals}획]`,f:()=>{ const mr=kgMR(h); useSeal('함께 이 소원을 이뤄라',mr?{t:'kgmr',id:h.id,rank:((SK[h.id]||[]).find(x=>/^대마력/.test(x[0]))||[])[1]||'A',i:Math.min(2,w.seals-1)}:undefined);
        if(mr){ log(`${h.name}${J(h.name,이)} 령주의 빛을 몸으로 받아 냈다. 대마력이 명령을 버텨 냈다.`,'war'); w.queue.push(()=>kgDuel(g.R)); return '령주는 서번트를 묶지 못했다.'; }
        g.bound=true; const l=kgSV(h,3); if(l) log(l,'voice'); w.queue.push(()=>kgTogether(true)); return `${h.name}${J(h.name,은)} 따랐다. 그 뒤로 입을 열지 않았다.`; }},
      {t:'그대로 둔다',auto:true,d:'서번트가 스스로 정하게 둔다',f:()=>{ w.queue.push(self); return `${h.name}${J(h.name,이)} 오래 잔을 보았다.`; }}]}); }
  // 함께 간다(②) · 묶인 잔(③). 살아 있는 동맹이 있으면 먼저 동맹 결전
  function kgTogether(bound){ const w=W(), g=w.kg, a=kgAlly(); g.bound=bound;
    if(a){ S.flags.kgAllyFight=1; S.flags.kgAllyI=a.i; S.flags.kgAllyN=a.mname||'';
      { const ah=H_BY[a.hero]; fxOnly({t:'kgally',back:!!a.kgBack,mname:a.mname||'',hero:a.revealed&&ah?ah.id:'',hname:a.revealed&&ah?ah.name:'',cls:ah&&CLS[ah.cls]?CLS[ah.cls].n:''}); }
      log(a.kgBack?`셋째 날 물러났던 ${pName(a)} 조가 돌아왔다. 잔을 막으러 온 것이다.`:`${pName(a)} 조가 등을 돌렸다. 이 잔이 무엇을 바라는지 알아 버린 얼굴이다.`,'war');
      log(`${a.mname}: “그 소원만큼은 이루게 둘 수 없어.”`,'enemy');
      a.ally=false; a.truce=false; a.intent='betray';
      w.queue.push(()=>battle(a,{final:true,kgAlly:true}),()=>kgAfterAlly(a,bound)); return; }
    kgEndTB(bound); }
  function kgAfterAlly(a,bound){ const w=W(); if(S.dead) return;
    if(!w.heroAlive) return kgEndX(a);
    if(!a.alive||a.hp<=0){ S.flags.kgAllyWin=1; return kgEndTB(bound); }
    w.queue.push(()=>battle(a,{final:true,kgAlly:true}),()=>kgAfterAlly(a,bound)); }
  // 잔을 쥔 쪽의 작은 보정 · 령주에 묶인 몸이면 그만큼 깎인다
  const kgAllyMod=()=>{ const g=kgW(); return g&&g.bound?-8:8; };
  function kgGrant(){ const k=S.flags.kg; log(`잔이 당신의 소원을 받아 들었다. “${KG_W[k].wish}.”`,'war'); log('본성 속의 진심이 이루어졌다.','loss'); S.flags.endWish=KG_W[k].wish; mark('war'); }
  function kgEndTB(bound){ const w=W(), g=w.kg, h=hero(); kgClose(); g.end=bound?'b':'t'; S.flags.kgEnd=g.end;
    kgGrant();
    if(S.flags.kgAllyWin) log(`그 세계에는 ${S.flags.kgAllyN||'동맹'}의 이름이 없다.`,'n');
    if(bound){ S.flags.kgB=h.id; S.flags.endFx='kgB'; log(`${h.name}${J(h.name,은)} 곁에 남았다. 마지막 령주를 쓰던 순간 뒤로, 입을 열지 않았다.`,'voice'); warOver(); return; }
    S.flags.endFx='kgT'; log('둘이 이긴 세계의 첫 아침이 왔다. 그 세계는 아주 조용했다.','n');
    kgNoEpi(kgAfter('t')); }
  // 막아선다(①): 실제 결투
  function kgDuel(R){ const w=W(), g=w.kg, h=hero(), a=kgAlly(); g.duel=1; if(a){ S.flags.kgAllyI=a.i; S.flags.kgAllyN=a.mname||''; }
    fxOnly({t:'kgduel',id:h.id,name:h.name,cls:CLS[h.cls]&&CLS[h.cls].n||'',line:(KG_SV[h.id]||[])[0]||''});   // 결투 시작
    duelStart({kind:'kg1',resolve:R,stage:kgSt(),promise:g.prom,memory:g.mem,ally:a?a.i:null,first:(KG_SV[h.id]||[])[0]||null}); }
  // 함께 가는 척한다(④)
  function kgBetray(){ const w=W(), g=w.kg, h=hero(), a=kgAlly();
    log(kgSay(h,['마지막은 함께 보자.','마지막은 함께 보시지요.','마지막은 함께 보자꾸나.','(서번트가 당신 곁에 선다. 등 뒤로.)']),'voice');
    const st=()=>({kind:'kg4',resolve:g.R,stage:kgSt(),promise:g.prom,memory:g.mem,ally:a?a.i:null,intro:'',first:kgSayRaw(h,KG_WHEN)});
    if(a){ S.flags.kgAllyFight=1; S.flags.kgAllyI=a.i; S.flags.kgAllyN=a.mname||'';
      log(`${pName(a)} 조가 잔을 막으러 왔다. ${h.name}${J(h.name,이)} 당신 앞에 서서 칼을 뽑았다.`,'war');
      log('세 합째. 서번트의 칼끝이 방향을 바꾸었다.','war');
      if(g.sus>=2) return duelStart(st());
      log('등 뒤에서 칼이 먼저 닿았다.','loss',{fx:{t:'kgback',v:'h'}}); S.st.health=Math.max(5,S.st.health-30);
      return duelStart({...st(),first:null}); }
    if(g.sus>=2&&w.seals>=1){
      decide({title:'등 뒤',body:'등 뒤의 온기가 한 걸음 가까워졌다. 그리고 칼날이 공기를 가르는 소리.',war:true,choices:[
        {t:'령주로 멈춰라',seal:true,d:`칼이 닿기 전에 멈춰 세운다 [령주 1획 · 남은 ${w.seals}획]`,f:()=>{ useSeal('멈춰라',{t:'kgback',v:'b',i:Math.min(2,w.seals-1),line:kgSayRaw(h,KG_WHEN)}); w.queue.push(()=>duelStart(st())); return '칼끝이 목 한 뼘 앞에서 멈췄다.'; }},
        {t:'그대로 둔다',auto:true,d:'알면서 받아들인다',f:()=>{ S.flags.kgKnew2=1; w.queue.push(()=>kgFallBack(true)); return '돌아보지 않았다.'; }}]}); return; }
    kgFallBack(false); }
  // ④ 등 뒤의 칼: 마스터가 쓰러진다
  function kgFallBack(knew){ const w=W(), g=w.kg, h=hero(); kgClose(); g.end='f'; S.flags.kgEnd='f';
    log(knew?'알고 있었다. 그래도 돌아보지 않았다. 등 뒤의 온기, 그리고 칼.':'등 뒤의 온기, 그리고 칼.','loss',{fx:{t:'kgback',v:knew?'c':'a'}});
    log(knew?'당신의 시점은 거기서 끊겼다. 끝까지, 당신이 고른 대로.':'당신의 시점은 거기서 끊겼다.','loss');
    log(`${h.name}${J(h.name,은)} 남은 마력과 단독행동으로 잔을 부수고 사라졌다.`,'war'); S.flags.brokeCup=1;
    kgDie('f'); }
  // 결투가 끝난 뒤
  Object.assign(DUEL_END,{kg1:win=>kgDuelEnd(win,'kg1'),kg4:win=>kgDuelEnd(win,'kg4')});
  function kgDuelEnd(win,kind){ const w=W(), g=w.kg, h=hero(), a=kgAlly(); kgClose();
    if(win){ g.end='m'; S.flags.kgEnd='m'; const l=kgSV(h,2); log('쓰러진 서번트가 손을 뻗다 말고 흩어졌다.','war'); if(l) log(l,'voice');
      w.heroAlive=false; w.hp=0; w.myOut={d:w.day,tod:w.tod,why:'마스터와의 결투 끝에 흩어졌다'};
      if(a) log(`${pName(a)} 조는 더 버티지 못하고 물러났다.`,'war');
      kgGrant(); S.flags.endFx='kgM'; kgNoEpi(kgAfter('m')); return; }
    if(kind==='kg4'){ g.end='f'; S.flags.kgEnd='f'; log(`${h.name}${J(h.name,은)} 칼을 거두지 않았다.`,'loss'); log(`${h.name}${J(h.name,은)} 남은 마력과 단독행동으로 잔을 부수고 사라졌다.`,'war'); S.flags.brokeCup=1; kgDie('f'); return; }
    g.end='s'; S.flags.kgEnd='s'; const l=kgSV(h,1);
    log('서번트가 당신 손등의 령주 자국을 한 번 쓰다듬었다.','war'); if(l) log(l,'voice');
    log('그리고 잔을 부쉈다. 빛이 꺼지기 전에, 서번트도 새벽 속으로 흩어졌다.','war'); S.flags.brokeCup=1;
    kgDie('s'); }
  // 손을 놓친 잔(⑥): 동맹 결전에서 졌다
  function kgEndX(a){ const w=W(), g=w.kg, h=hero(); kgClose(); g.end='x'; S.flags.kgEnd='x'; S.flags.kg6=1;
    log(`쓰러진 ${h.name}${J(h.name,은)} 끝까지 당신 쪽을 보고 있었다.`,'loss');
    log(`${a.mname}${J(a.mname,이)} 잔을 부쉈다. 부서진 조각 앞에서 한마디를 남겼다.`,'war');
    kgAllySay();
    S.flags.wishText=''; S.flags.war='lost'; S.flags.brokeCup=1; S.flags.endFx='kgX'; if(ch(.15)) S.flags.kgAllyFell=1;
    warOver(); }
  // ① 검을 거두지 않은 자 · ② 둘이 이긴 세계: 진심이 이루어진 세계의 에필로그 (11-22, 예전에는 남은 세월을 한 번에 흘려보냈다)
  // 후일담은 결말 연출 뒤에 창으로 먼저 한 번 보여 준다(쓰러지는 결말과 같게). 고른 줄은 봄 열나흘의 한 줄에서 뺀다
  function kgNoEpi(A){ const w=W(); w.ended=true; w.queue=[]; fxOnly(endFxOf()); mark('war'); add({will:4,lore:3});
    S.once.crest=1; S.phase='epi'; S.warState='done'; S.clock=0; S.epi={i:0,used:[],kw:S.flags.kgEnd,afU:(A||[]).map(x=>KG_AF.indexOf(x))}; H.phase('epi'); H.save(); H.change();
    const x=(A||[])[0]; if(x) decide({title:`그 뒤 · ${x.t()}`,body:x.b().join('\n'),war:true,silent:true,choices:[{t:'닫기',auto:true,f:()=>null}]}); }
  // 쓰러지는 결말(① 서번트 승 · ④): 죽음 뒤에 후일담
  function kgDie(k){ const w=W(); w.ended=true; w.queue=[];
    // 11-22: 쓰러지던 순간의 기록 몇 줄을 첫 후일담 창의 '지금까지' 칸에 싣는다 (창이 떠 있는 동안에는 기록을 볼 수 없으므로)
    const LG=(S.log||[]).filter(e=>e&&typeof e.t==='string'&&['war','loss','voice','enemy','n','seal'].includes(e.k)&&!/^진심 · /.test(e.t)).slice(-6).map(e=>({...e}));
    w.myOut={d:w.day,tod:w.tod,why:k==='f'?'당신을 베고 잔을 부순 뒤 사라졌다':'결투 끝에 잔을 부수고 새벽 속으로 흩어졌다'};   // 11-22: 결과 화면의 서번트 결과
    S.flags.war='dead'; S.flags.endFx=k==='f'?'kgF':'kgS'; fxOnly(endFxOf());
    die(k==='f'?'등 뒤의 칼':'서번트와의 결투');
    // 11-22: 후일담이 '마지막으로' 창 뒤에 묻혀 바로 기록으로 넘어가는 것처럼 보이던 것 → 기록 줄에도 남기고, 창으로 먼저 보여 준 뒤 닫으면 마지막 말
    const A=(k==='f'?[['그 뒤 · 서번트',kgAfPick('f')],['그 뒤 · 가까운 사람',kgAfPick('fn')]]:[['그 뒤',kgAfPick(k)]]).filter(a=>a[1]);
    A.forEach(([hd,x])=>kgAfShow(x,hd));
    const P0=S.pending, go=i=>{ if(i>=A.length){ if(P0) decide(P0); return null; } const [hd,x]=A[i]; decide({title:`${hd} · ${x.t()}`,body:x.b().join('\n'),recap:i===0&&LG.length?LG:undefined,war:true,silent:true,choices:[{t:'닫기',auto:true,f:()=>go(i+1)}]}); return null; };
    if(P0&&A.length){ S.pending=null; go(0); } }
  // 후일담: 결말마다 그 뒤의 장면 하나 (조건이 가장 많이 맞는 줄들 가운데 하나)
  function kgAfPick(k){ const c=KG_AF.filter(x=>x.k===k&&(!x.c||x.c())); if(!c.length) return null; const m=Math.max(...c.map(x=>x.sp)); return pick(c.filter(x=>x.sp===m)); }
  function kgAfShow(x,head){ if(!x) return; log(`${head} · ${x.t}`,'night'); for(const l of x.b) log(l,'n'); }
  function kgAfter(k){ if(k==='f'){ const a=kgAfPick('f'), b=kgAfPick('fn'); kgAfShow(a,'그 뒤 · 서번트'); kgAfShow(b,'그 뒤 · 가까운 사람'); return [a,b].filter(Boolean); }
    const x=kgAfPick(k); kgAfShow(x,'그 뒤'); return x?[x]:[]; }
  /* ---------- 에필로그 ---------- */
  // 묶인 잔(③): 날 → 달 → 해. ③ 전용 사건만 나온다
  const KG_N={A:14,B:12,C:9}, KG_RATE={A:.7,B:.75,C:.6};
  function kgEpOk(x){ const E=S.epi; if(x.e!=='b'||x.ph!==E.ph||(E.kgU||[]).includes(x.id)) return false; if(x.mon&&E.m!==x.mon) return false; return !x.c||x.c(); }
  function kgEpGo(x){ const E=S.epi; (E.kgU=E.kgU||[]).push(x.id); S.resumeEv={src:'EP2',id:'@kg'+x.id}; x.f(); if(!S.pending) S.resumeEv=null; }
  function kgEpStart(){ const E=S.epi; E.kg=1; E.ph='A'; E.d=0; E.m=1; E.cy=0; E.k=0; E.dayU=[]; E.kgU=E.kgU||[]; }
  // 끝: 공용 에필로그 흐름으로. ①·② · 열 해를 넘긴 ③은 「그 뒤의 길」 없이 사건 자리로 가서 몇 해 간격으로 이어 간다 (11-22, ③은 예전에 남은 세월을 한 번에 흘려보냈다)
  function kgEpEnd(){ const E=S.epi; E.ph='D'; if(E.kw||(S.flags.kgB&&!S.flags.kgGone)){ E.i=Math.max(E.i,EPI_START.length); E.n=E.i-EPI_START.length+(E.kw?ri(19,21):ri(12,14)); } }
  function kgEpStep(){ const E=S.epi;
    if(!E.kw&&(!S.flags.kgB||S.flags.kgGone)){ kgEpEnd(); return false; }
    if(E.ph==='A'){
      if(E.d>=KG_N.A){ E.ph='B'; log('열나흘이 지났다. 이제 달이 지나간다.','sys'); return kgEpStep(); }
      E.d++; E.k++; log(`봄 · ${E.d}일째`,'night');
      if(E.kw){ if(E.d>=KG_N.A) log(KGW_DAYL[S.flags.kg]||EP3_DAYL.d,'n'); else kgWDay(); kgWPick(); H.change(); return true; }
      if(E.d>=KG_N.A) log(KG_DAYL,'n'); else { const pool=KG_DAY.map((_,i)=>i).filter(i=>!E.dayU.includes(i)&&!(KG_DAY_NO[S.flags.kg]||[]).includes(i)); if(pool.length){ const i=pick(pool); E.dayU.push(i); log(KG_DAY[i],'n'); } }
      kgEpPick(); H.change(); return true; }
    if(E.ph==='B'){
      if(E.m>=KG_N.B){ if(E.kw){ log(EP3_END,'sys'); kgEpEnd(); H.change(); return true; } E.ph='C'; log('한 해가 지났다. 이제 해가 지나간다.','sys'); return kgEpStep(); }
      E.m++; E.k++; log(`첫 해 · ${E.m}달째`,'night'); log(E.kw?kgWMon(E.m):(KG_MON[E.m]||''),'n');
      if(E.m===KG_N.B){ S.age++; S.year++; mark('calm'); if(S.age>=40) add({health:-ageWear()}); famYear(); if(S.pending) S.pending=null; }
      if(E.kw) kgWPick(); else kgEpPick(); H.change(); return true; }
    if(E.ph==='C'){
      if(E.cy>=KG_N.C){ kgFadeTry(); kgEpEnd(); return !!S.pending; }
      E.cy++; E.k++; passYears(1); if(S.dead||S.pending) return true; const yu=E.yrU=E.yrU||[], yp=KG_YR.map((_,i)=>i).filter(i=>!yu.includes(i)); if(yp.length){ const i=pick(yp); yu.push(i); log(KG_YR[i],'n'); }
      kgEpPick(); H.change(); return true; }
    return false; }
  function kgEpPick(){ if(S.pending||S.dead) return; const E=S.epi; if(!ch(KG_RATE[E.ph]||.6)) return;
    if(E.ph==='C'&&ch(.5)&&kgPoolMix()) return;   // 11-22: 아홉 해 동안은 절반쯤 이뤄진 세계 사건 · 공용 사건
    const c=KG_EV.filter(kgEpOk); if(c.length) kgEpGo(pick(c)); }
  // 열 해가 지난 뒤: 서번트가 먼저 사라지는 해 (인연 0~1단계 · 3단계에서)
  function kgFadeTry(){ if(S.pending||S.flags.kgGone) return; const st=kgS();
    const z=KG_EV.filter(x=>x.e==='b'&&x.ph==='G'&&(!x.c||x.c())); if(z.length&&(st<=1||st>=3)&&ch(.35)){ S.flags.kgGone=1; kgEpGo(pick(z)); } }
  // ③ 남은 령주로 놓아준다: 그 뒤로는 서번트가 떠난 삶
  function kgRelease(){ S.flags.kgGone=1; S.flags.kgFree=1; }
  // 마지막 해: 세상을 떠나는 장면 (③ 묶인 잔 · ⑤ 돌아선 삶). 선택은 결과만 바꾸고, 고른 뒤에 then이 원래의 마지막을 잇는다
  function kgDeath(then){ if(S.flags.kgLastDone||!S.hero) return false;
    const e=S.flags.kgB&&!S.flags.kgGone?'b':S.flags.kg5?'p':S.flags.kg6?'x':null, c=kgCtx();
    const z=c==='m'||c==='t'||c==='g'?KG_EV.filter(x=>(x.e==='w'||(c==='t'&&x.e==='t'))&&x.ph==='Z'&&(!x.c||x.c())):e?KG_EV.filter(x=>x.e===e&&x.ph==='Z'&&(!x.c||x.c())):[]; if(!z.length) return false;
    S.flags.kgLastDone=1; log('마지막 해','night'); pick(z).f(then); return true; }
  // ⑤ 돌아선 삶 · ⑥ 손을 놓친 잔: 에필로그의 봄 · 첫 해에 섞인다
  function kgMix(){ const E=S.epi; if(!E||S.pending||S.dead) return false; const k=S.flags.kg5?'p':S.flags.kg6?'x':null; if(!k||!ch(k==='x'?.7:.45)) return false;   // 11-22: ⑥은 70%
    const c=KG_EV.filter(x=>x.e===k&&x.ph===E.ph&&!(E.kgU||[]).includes(x.id)&&(!x.mon||x.mon===E.m)&&(!x.c||x.c())); if(!c.length) return false;
    kgEpGo(pick(c)); return true; }
  /* ---------- 11-22: 진심이 이루어진 세계의 에필로그 ----------
     ① 검을 거두지 않은 자(m) · ② 둘이 이긴 세계(t): 봄 열나흘(하루씩) → 첫 해(한 달씩) → 그 뒤(공용 흐름에 「이뤄진 세계」 사건을 섞어 몇 해 간격) → 마지막 해 장면
     ③ 묶인 잔(b): 아홉 해 동안 절반쯤 이뤄진 세계 · 공용 사건을 섞고, 열 해 뒤에도 몇 해 간격으로 이어 간다. 서번트가 먼저 사라졌거나 놓아줬으면 g
     섞는 사건은 진심 성향마다 그 세계의 규칙과 부딪치지 않는 것만 (시트 「검귀 에필로그 추가안」 5 · 6 · 11)
     무게: 무거운 사건 다음 차례는 가볍거나 보통인 사건이 두 배 잘 뜬다 */
  const KG_DAY_NO={avenger:[12],taboo:[7],zeal:[7,12]};   // ③ 하루 줄: 「이상한 일이 없는 신문」 · 「손님을 묻는 이웃」이 그 세계와 부딪치는 것
  const kgCtx=()=>{ const e=S.flags.kgEnd; return e==='m'?'m':e==='t'?'t':e==='b'?(S.flags.kgGone?'g':'b'):null; };
  const kgRelW=n=>{ const c=kgCtx(); if(c==='t'||c==='b') kgRel(n); };   // 인연은 서번트가 곁에 있을 때만
  const kgHeavy=x=>!!x&&(x.hv===1||x.wt==='h');
  const kgPace=x=>{ const E=S.epi; return E&&E.kgHv&&!kgHeavy(x)?2:1; };
  const kgPaced=x=>{ if(S.epi) S.epi.kgHv=kgHeavy(x); };
  const KGW_W=8;   // 이뤄진 세계 사건 하나의 무게 (섞는 사건은 1~1.5)
  // 공용 에필로그 사건: 이뤄진 세계에서 뺄 것
  const KGW_NO={all:['wish_after','survivor'],
    tb:['partner','anniversary','first_snow','lookalike','left_behind','bond_dream','distrust','echo_dream','echo_summon','echo_habit','echo_letter','bedtime','marked_child','movie','homeland','scar_rain'],
    avenger:['af_jd01','other_master'], taboo:[], judge:['table','memorial','af_jd03'],
    cruel:['af_jd04','af_av01','other_master','checkup','kid','legacy','grandkid','bedtime','marked_child','mentor_last','family_knew','friend_key','host_saved','host_hurt','host_lost'],
    zeal:['af_jd01','af_jd04','af_jd07','af_av01','other_master','kid','legacy','grandkid','bedtime','marked_child','victims','memorial','redevelop','movie','mentor_last','family_knew','friend_key','host_saved','host_hurt','host_lost','arc_leyline']};
  const kgWorldNo=id=>{ const c=kgCtx(); if(!c) return false; const k=S.flags.kg;
    if(KGW_NO.all.includes(id)||(KGW_NO[k]||[]).includes(id)) return true;
    if((c==='t'||c==='b')&&KGW_NO.tb.includes(id)) return true;
    return id==='ally_letter'&&(c==='m'||c==='t')&&!!S.flags.kgAllyFight; };
  // ① 섞는 「서번트가 떠난 삶」 사건(봄 · 첫 해)에서 뺄 것: 도시가 평소대로라는 전제 · 그 세계에 없는 사람들
  const KGW_LONE_NO={all:[],
    avenger:['la22','lb07','lb23','lb32'],
    judge:['la11','la26','lb21','lb48'],
    cruel:['lb13','lb26','lb03','lb35','lb48','la42'],
    taboo:[],
    zeal:['la06','la07','la08','la11','la22','la26','la29','la39','la42','lb03','lb07','lb08','lb21','lb23','lb26','lb27','lb31','lb32','lb35','lb39','lb41','lb43','lb48']};
  // ② 섞는 「함께 사는 생」 사건(봄 · 첫 해): 서번트와 둘이서 겪는 것은 모두, 동네 · 가게 · 사람이 나오는 것은 세계마다
  const KGW_STAY={all:['a_sleep','a_rain','a_phone','a_wish','a_last','a_cook','a_scar','a_cat','a_arms','a_shop_m','a_dream','a_patrol','a_clean','a_body','a_hunger','a_cut','a_board','a_song','a_stars','a_wash','a_church',
      'b_room','b_alone','b_wish','b_year','b_pot','b_storm','b_bday','b_hday','b_fade','b_rumor','b_lease'],
    avenger:['a_clothes','a_key','a_face','a_train','a_field','a_market','a_hair','a_book','a_coin','a_work','a_flower','b_pay','b_summer','b_cold','b_study','b_study_s','b_bike','b_friend','b_trip','b_museum','b_fever','b_shop','b_frame','b_hero','b_gift'],
    judge:['a_clothes','a_key','a_face','a_train','a_field','a_market','a_hair','a_book','a_coin','a_work','a_flower','a_name','a_neighbor','a_call','b_pay','b_summer','b_cold','b_study','b_study_s','b_bike','b_friend','b_trip','b_museum','b_fever','b_shop','b_frame','b_side','b_home','b_gift'],
    cruel:['a_clothes','a_key','a_face','a_train','a_field','a_market','a_hair','a_book','a_coin','a_work','a_flower','a_name','a_call','b_pay','b_summer','b_study','b_study_s','b_bike','b_friend','b_trip','b_museum','b_shop','b_frame','b_side','b_home','b_gift'],
    taboo:['a_clothes','a_key','a_face','a_train','a_field','a_market','a_hair','a_book','a_coin','a_work','a_flower','a_name','a_neighbor','a_call','b_pay','b_summer','b_cold','b_study','b_study_s','b_bike','b_friend','b_trip','b_museum','b_fever','b_shop','b_frame','b_hero','b_side','b_home','b_gift'],
    zeal:[]};
  const kgLoneOk=x=>{ const E=S.epi; if(x.ph!==E.ph||(E.lu||[]).includes(x.id)) return false;
    if(x.k&&!x.k.includes('lost')&&!x.k.includes('win')) return false;
    if(x.day&&(E.d<x.day[0]||E.d>x.day[1])) return false; if(x.mon&&(E.m<x.mon[0]||E.m>x.mon[1])) return false;
    if((KGW_LONE_NO.all||[]).includes(x.id)||(KGW_LONE_NO[S.flags.kg]||[]).includes(x.id)) return false;
    return !x.c||x.c(); };
  const kgStayOk=e=>(KGW_STAY.all||[]).concat(KGW_STAY[S.flags.kg]||[]).includes(e.id);
  // 봄 열나흘의 한 줄: 그 세계의 하루 + 후일담 줄(①은 「마스터 승」, ②는 「마지막 두 줄」에서 조건이 맞고 창에 나오지 않은 것)
  function kgWDay(){ const E=S.epi, k=S.flags.kg, af=E.kw==='t'?'t':'m', D=KGW_DAY[k]||[];
    const rows=KG_AF.map((_,i)=>i).filter(i=>KG_AF[i].k===af&&!(E.afU||[]).includes(i)&&(!KG_AF[i].c||KG_AF[i].c()));
    const pool=D.map((_,i)=>'d'+i).concat(rows.map(i=>'a'+i)).filter(i=>!E.dayU.includes(i)); if(!pool.length) return;
    const i=pick(pool); E.dayU.push(i); if(i[0]==='d') log(D[+i.slice(1)],'n'); else for(const l of KG_AF[+i.slice(1)].b()) log(l,'n'); }
  function kgWMon(m){ const x=(KGW_MONX[S.flags.kg]||{})[m]; if(x) return x; return S.epi.kw==='t'?ep2N(EP2_MON[m]||''):(EP3_MON[m]||''); }
  // 봄 · 첫 해의 사건 하나: 날이 정해진 사건 → 이뤄진 세계 사건 · ②용 사건 → (①) 서번트가 떠난 삶 · (②) 함께 사는 생에서 걸러 섞은 것
  function kgWPick(){ if(S.pending||S.dead) return; const E=S.epi, ph=E.ph, t=E.kw==='t';
    if(!t){ const fx=EP3_EV.find(x=>x.must&&kgLoneOk(x)); if(fx){ kgPaced(fx); return ep3Go(fx); } }
    else { const r=relOf(), fx=EP2_EV.find(e=>e.day&&e.day===E.d&&ph==='A'&&kgStayOk(e)&&ep2EvOk(e,r)); if(fx){ kgPaced(fx); return ep2EvGo(fx); }
      if(r&&relDue()){ return relScene(); } }   // 11-22: ②에서도 인연 단계가 오르면 그 장면 (kgrel_apply)
    if(!ch(KG_RATE[ph]||.7)) return;
    const c=KG_EV.filter(x=>(x.e==='w'||x.e==='t')&&x.ph===ph&&!(E.kgU||[]).includes(x.id)&&(!x.c||x.c())).map(x=>({x,w:KGW_W*kgPace(x),go:()=>kgEpGo(x)}));
    if(!t) EP3_EV.filter(x=>!x.must&&kgLoneOk(x)).forEach(x=>c.push({x,w:(x.w||1)*kgPace(x),go:()=>ep3Go(x)}));
    else { const r=relOf(); EP2_EV.filter(e=>!e.day&&kgStayOk(e)&&ep2EvOk(e,r)).forEach(e=>c.push({x:e,w:1.5*kgPace(e),go:()=>ep2EvGo(e)}));
      if(r) EP_REL.filter(x=>x.w>0&&!(E.relUsed||[]).includes(x.id)&&x.c(r)).forEach(x=>c.push({x,w:2*kgPace(x),go:()=>x.f()})); }   // 11-22: 세계에 맞는 인연 사건 (relHome · KG_REL_OK)
    if(!c.length) return; const o=wpick(c,o=>o.w); kgPaced(o.x); o.go(); }
  // ③ 아홉 해: 공용 에필로그 사건 자리에서 하나 (이뤄진 세계 사건 · 걸러진 공용 사건. 연작은 빼고)
  function kgPoolMix(){ const E=S.epi; E.used=E.used||[];
    const c=EPI_POOL.filter(x=>!E.used.includes(x.id)&&!x.arc&&(!x.ke||x.ke==='w')&&x.c()&&!epiBlock(x.id)); if(!c.length) return false;
    const x=wpick(c,x=>(x.w||1)*kgPace(x)); kgPaced(x); E.used.push(x.id); S.resumeEv={src:'EP2',id:'@pool'+x.id}; x.f(); if(!S.pending) S.resumeEv=null; return true; }
  function kgResume(id){ const x=KG_EV.find(x=>x.id===id); if(x){ S.resumeEv={src:'EP2',id:'@kg'+id}; x.f(()=>die(causeFor())); } }
  // 삶 파트 · 전쟁의 복선 (시트 10~11줄)
  function kgOmenLife(){ if(S.phase!=='life') return; S.once=S.once||{}; if((S.once.kgOm||0)>=4) return; const k=kgDeep(); if(!k||!ch(.3)) return;
    const u=S.once.kgOmU||(S.once.kgOmU=[]); const L=(KG_OMEN[k]||[]).filter(t=>!u.includes(t)); if(!L.length) return; const t=pick(L); u.push(t); S.once.kgOm=(S.once.kgOm||0)+1; log(t,'n'); }
  function kgOmenWar(){ const w=W(); if(!w||!w.heroAlive||w.kg||(w.kgOm||0)>=4||!kgDeep()||w.trust<50) return; const st=kgSt(); if(st<1||!ch(.22)) return;
    w.kgOm=(w.kgOm||0)+1; const h=hero(); log(kgSay(h,pick(KG_OMENW[Math.min(3,st)-1])),'voice'); }
