  /* ── 11-21 마스터 대 서번트 결투 (상세안 6판) ──
     결투 참가자: 마스터(환산 능력치 · 오드 · 건강)와 서번트(마스터 지원 몫을 뺀 전투력 · 마력 · 건강)
     상황 정보(ctx): kind · resolve(결심) · stage(인연 단계) · promise('kept'|'broken'|null) · memory('same'|'again'|'diff'|null) · ally(동행 조 i)
     상태는 S.war.duel에 둔다. 끝나면 duelEnd가 DUEL_END[kind]를 부른다 */
  const DUEL_K={giC:5,giA:2,hA:85,hHi:.3,hP:14,npA:0,npW:90,oddPay:.5,odd0:5,bikiC:20,bikiD:18};
  const DUEL_STR={bajiquan:1,sword:1,agent:1,exorcism:1,anshou:.5,gunfight:.5}, DUEL_AGI={anshou:1,gunfight:1,agent:1,bajiquan:.5,exorcism:.5,sword:.5}, DUEL_MAG={element:1,curse:1,jewel:1,rune:1,necro:1};
  // 비기 갈래: atk 공격 · hex 약화 · wall 방벽 · heal 회복. d: 고위 기준 수치
  const DUEL_BK={element:{g:'atk',d:18,mr:1},jewel:{g:'atk',d:22,mr:1,w:10},body:{g:'atk',d:18,mr:0,ev:1},holy:{g:'atk',d:14,mr:1,av:1},rune:{g:'atk',d:18,mr:1},
    curse:{g:'hex'},mind:{g:'hex'},necro:{g:'hex'},astro:{g:'hex'},familiar:{g:'hex'},barrier:{g:'wall'},puppet:{g:'wall'},heal:{g:'heal'},alchemy:{g:'heal'}};
  const DUEL_BKN={element:'원소 마술 비기',jewel:'보석 마술 비기',body:'몸의 비기',holy:'성언의 비기',rune:'룬 마술 비기',curse:'저주의 비기',mind:'정신 간섭 비기',necro:'강령술 비기',astro:'점성술 비기',familiar:'사역마 비기',barrier:'결계 마술 비기',puppet:'인형술 비기',heal:'치유 마술 비기',alchemy:'연금술 비기'};
  const dStack=L=>{ const g=L.filter(x=>x>0).sort((a,b)=>b-a); return g.length?g[0]+g.slice(1).reduce((s,x)=>s+x*.5,0):0; };
  const dRank=v=>{ const L=['','E','D','C','B','A','EX'], f=Math.max(1,Math.min(6,Math.floor(v+1e-9))); return L[f]+((v-f)>=.5&&f<6?'+':''); };
  // 마스터 환산 (상세안 3-1)
  function duelMaster(){ const A=arts(), lv=id=>(A[id]&&A[id].lv)||0;
    const str=1+dStack(Object.keys(DUEL_STR).map(id=>lv(id)*DUEL_STR[id])), agi=1+dStack(Object.keys(DUEL_AGI).map(id=>lv(id)*DUEL_AGI[id]));
    const ml=Math.max(0,...MARTIAL.map(lv)), dur=1+ml*.5+(lv('enhance')+lv('barrier'))/2+(A.regen?1:0);
    const mana=Math.max(1,Math.min(5,(S.circuit||1)-1))+(S.st.mana>=80?.5:0)+dStack(Object.keys(DUEL_MAG).map(id=>lv(id)*.5));
    const luck=S.st.will>=90?3:S.st.will>=70?2:1;
    const hi=Object.keys(A).filter(id=>ARTS[id]&&A[id].lv>=3), magHi=hi.filter(id=>ARTS[id].br==='magic'||id==='baptism').length;
    let soy=S.st.lore>=60?1:0; const bl=Math.max(lv('barrier'),lv('baptism')); if(bl>=4) soy=Math.max(soy,3); else if(bl>=3) soy=Math.max(soy,2); if(magHi>=2&&soy>0) soy++;
    return {P:[str,agi,Math.min(6,dur),Math.min(6,mana),luck],soy,gi:Math.round((S.circuit||1)*DUEL_K.giC)+hi.length*DUEL_K.giA,hi,lv}; }
  const duelMH=M=>({cls:'master',id:'__master',mrEst:M.soy,s:M.P,sp:null});
  // 쓸 수 있는 비기: 고위 이상 계통마다 하나. 체술 · 강화는 「몸의 비기」 하나로, 세례영창 · 흑건은 「성언의 비기」 하나로 묶는다
  function duelBikis(M){ const out=[], seen=new Set(), L=M.lv;
    for(const id of M.hi){ const k=MARTIAL.includes(id)||id==='enhance'?'body':id==='baptism'||id==='blackkey'?'holy':id; if(!DUEL_BK[k]||seen.has(k)) continue; seen.add(k);
      const lvl=k==='body'?Math.max(L('enhance'),...MARTIAL.map(L)):k==='holy'?Math.max(L('baptism'),L('blackkey')):L(id); out.push({k,x:lvl>=4?1.4:1}); }
    return out; }
  const duelSPow=D=>{ const h=hero(), hp=D.shp, rd=D.r;
    return heroBase(h.s,hp)+clsBonus(h,h.s)+SV(h,'power')*1.2+SV(h,'div')*.8+SV(h,'mad')*.8+SV(h,'rally')*.8+(rd>=2?SV(h,'insight')*.9:0)+underdog(h)
      +(SV(h,'avenge')?(100-hp)*.045*SV(h,'avenge'):0)+(h.sp==='gate'?7+(hp<50?5:0):0)+edgeV(h,hp,rd,false)+(BIAS[h.id]||0)-sjNight(h); };
  const duelNpCost=h=>{ let c=npCostM(h)*(22+npRV(h)*3)*Math.max(.8,Math.min(1.2,1-(PV(h.s[3])-3)*.05)); if(h.cls==='berserk') c*=1.4; if(h.cls==='caster') c*=.85; return Math.round(c); };
  const duelNpDmg=(h,soy)=>Math.max(3,Math.round((8+npRV(h)*2.5)*NP_MUL*Math.max(.8,Math.min(1.25,1+(PV(h.s[3])-3)*.05))*(.85+rnd()*.3)*(1-Math.min(.4,soy*.04))));
  const duelBlade=R=>R>=75?0:R>=50?1:2, DUEL_BW=['굳다','흔들린다','크게 흔들린다'];
  const duelMu=st=>[1,1.25,1.5,2][Math.max(0,Math.min(3,st||0))];
  function duelStart(ctx){ const w=W(), h=hero(); if(!w||!h||w.duel) return;
    const M=duelMaster(), od=oddMax();
    const D=w.duel={ctx:{kind:ctx.kind||'test',resolve:ctx.resolve??60,stage:ctx.stage??((relOf()||{}).stage||0),promise:ctx.promise||null,memory:ctx.memory||null,ally:ctx.ally??null},
      R:ctx.resolve??60,r:1,mhp:S.st.health,od,odMax:od,shp:w.hp,sm:w.sm??100,used:{},talked:{},hesUp:0,wallM:0,curse:null,eyeDeb:null,eyeGuard:null,compel:0,jinx:0,sWall:0,sBuff:0,npUsed:false,mR:0,pre:null,chk:0,compNP:false,compOut:false};
    if(D.ctx.ally!=null){ const p=w.pairs.find(x=>x.i===D.ctx.ally&&x.alive); if(!p) D.ctx.ally=null; }
    const n=h.name;
    log(`잔이 가득 찼다. ${n}${J(n,이)} 당신과 마주 섰다.`,'war');
    log(`${n}: “그 소원만큼은 내가 막겠다.”`,'voice');
    if(D.ctx.ally!=null){ const p=w.pairs.find(x=>x.i===D.ctx.ally); log(`${pName(p)} 조가 ${n} 곁에 섰다. 잔을 막으러 온 것이다.`,'war'); }
    duelRound(); }
  function duelHes(D){ const st=D.ctx.stage; let p=Math.max(.05,Math.min(DUEL_K.hHi,(DUEL_K.hA-D.R)/100))+(D.hesUp>=D.r?.15:0)+(st>=3&&D.mhp<=25?.2:0); return ch(p); }
  function duelRound(){ const w=W(), D=w&&w.duel; if(!D||S.dead) return; const h=hero(), M=duelMaster(), mh=duelMH(M), night=w.tod!=='낮';
    if(D.hesR!==D.r){ D.hesR=D.r; D.hes=duelHes(D); if(D.hes) log(pickNR([`${h.name}의 칼끝이 한순간 흔들렸다.`,`${h.name}${J(h.name,이)} 숨을 한 번 삼켰다. 칼이 늦었다.`],'duelHes'),'war'); }
    const pre=D.mR===D.r, cs=[], ro=r=>isLat(r)?'로':'으로', ER=h.s, eyeOn=giftOn();
    const mr=SV(h,'mr'), cost=(a,b)=>D.od>=b?`[오드 −${a===b?a:a+'~'+b}]`:`[오드 부족 · 건강 −${Math.ceil((b-D.od)*DUEL_K.oddPay)}]`;
    const mc=[Math.max(2,Math.round(5*Math.max(.75,Math.min(1.2,1-(M.P[3]-3)*.08)))),Math.max(2,Math.round(8*Math.max(.75,Math.min(1.2,1-(M.P[3]-3)*.08))))];
    const vMag=atkVal('magic',mh,M.P,h,ER,night)-mr*1.2*.018, vRnd=atkVal('round',mh,M.P,h,ER,night), canMag=mCanMagic();
    const best=canMag&&vMag>vRnd+.02?'magic':'round';
    if(canMag) cs.push({t:'마술로 공격한다',d:`「마력 ${dRank(M.P[3])}」${ro(dRank(M.P[3]))} 상대의 마력과 겨룬다 · 대마력에 막히지만 잘 피해지지 않는다 ${cost(mc[0],mc[1])}`,adv:best==='magic'?'up':'down',advEst:false,auto:best==='magic',f:()=>duelClash('magic')});
    cs.push({t:'체술로 맞선다',d:`「근력 ${dRank(M.P[0])}」${ro(dRank(M.P[0]))} 상대의 내구와 겨룬다 ${cost(3,6)}`,adv:canMag?(best==='round'?'up':'down'):undefined,auto:best==='round',f:()=>duelClash('round')});
    if(!pre){
      // 마스터 행동
      const one=(k,t,d,c,ok,f)=>cs.push({grp:'master',t,d:`${d} ${!ok?'[이미 썼다]':D.od>=c?`[오드 −${c}]`:'[오드 부족]'}`,off:!ok||D.od<c,f:()=>{ D.od-=c; f(); return duelPre(t); }});
      if(canMag){ const L=k=>actLv(k);
        if(L('buff')) one('buff','강화 마술','이번 합 마스터 전투력이 오른다',25,true,()=>{ D.pre={...(D.pre||{}),pow:Math.round(6*actMul('buff'))}; });
        if(L('hex')) one('hex','방해 마술','이번 합 서번트 전투력이 떨어진다 · 대마력이면 절반',25,true,()=>{ D.pre={...(D.pre||{}),deb:Math.round((mr?3:6)*actMul('hex'))}; });
        if(L('ward')) one('ward','엄호 결계','이번 합 마스터가 받는 피해가 준다 · 보구는 막지 못한다',20,true,()=>{ const lv=actLv('ward'); D.pre={...(D.pre||{}),guard:lv>=2?Math.min(.6,(lv>=3?.45:.35)*actQ('ward')):.25}; });
        if(L('heal')) one('heal','응급 치유','마스터 건강 +12 · 결투에서 한 번',30,!D.used.heal,()=>{ D.used.heal=1; const lv=actLv('heal'); D.mhp=Math.min(100,D.mhp+Math.round(HEAL_V[Math.min(3,Math.max(1,lv))]*(lv>=2?actQ('heal'):1))); });
        if(artLv('baptism')) one('bapt','세례영창','이번 합 서번트 전투력이 떨어진다 · 어벤저에게는 두 배 · 대마력이면 절반 · 결투에서 한 번',25,!D.used.bapt,()=>{ D.used.bapt=1; const lv=artLv('baptism'); let v=[0,4,6,8][Math.min(3,lv)]*(lv>=2?artQ('baptism'):1); if(h.cls==='avenger') v*=2; if(mr) v/=2; D.pre={...(D.pre||{}),deb:Math.round(v)}; }); }
      if(artLv('blackkey')) one('key','흑건을 던진다','이번 합 서번트 전투력이 떨어진다',0,true,()=>{ D.pre={...(D.pre||{}),deb:5+(artLv('blackkey')-1)*2}; });
      if(artLv('jewel')) cs.push({grp:'master',t:'보석을 던진다',d:`이번 합 서번트 전투력이 크게 떨어진다 ${S.wealth>=5?'[재산 −5]':'[재산 5 필요]'}`,off:S.wealth<5,f:()=>{ add({wealth:-5}); D.pre={...(D.pre||{}),deb:Math.round((6+artLv('jewel')*3)*(artLv('jewel')>=2?artQ('jewel'):1))}; return duelPre('보석을 던진다'); }});
      // 마안
      if(eyeOn&&DUEL_EYE[S.gift.id]){ const g=S.gift, once=['stone','future','compel'].includes(g.id), used=once&&D.used.eye, gc=giftCost();
        cs.push({grp:'eye',t:GIFTS[g.id].n,d:`${DUEL_EYE[g.id]}${once?' · 결투에서 한 번':''} ${used?'[이미 썼다]':gc?`[건강 −${gc}]`:'[대가 없음]'}`,off:used||D.mhp<=gc+5,f:()=>{ if(once) D.used.eye=1; D.mhp-=gc; duelEye(g.id); return duelPre(GIFTS[g.id].n); }}); }
      // 고위 기술: 비기
      for(const b of duelBikis(M)){ const B=DUEL_BK[b.k], u=D.used['bk_'+b.k], x=b.x;
        const dd=B.g==='atk'?`힘 겨루기 없이 피해 ${Math.round(B.d*x)}${B.mr?' · 대마력에 깎인다':' · 대마력을 무시한다'}${B.av?' · 어벤저에게는 두 배':''} · 그 합의 공격을 대신한다`
          :B.g==='hex'?`네 합 동안 서번트 전투력 −${Math.round(15*x)} · 대마력이면 −${Math.round(9*x)} · 걸고 나서 공격도 한다`
          :B.g==='wall'?`세 합 동안 서번트의 평소 공격이 닿지 않는다 · 그 합의 공격을 대신한다`
          :`마스터 건강 +${Math.round(20*x)} · 보구를 맞는 합에도 회복된다 · 그 합의 공격을 대신한다`;
        cs.push({grp:'arcana',t:DUEL_BKN[b.k],d:`${dd}${B.g!=='heal'?' · 보구에는 진다':''} ${u?'[이미 썼다]':D.od>=DUEL_K.bikiC?`[오드 −${DUEL_K.bikiC}${B.w?` · 재산 −${B.w}`:''}]`:'[오드 부족]'}`,off:!!u||D.od<DUEL_K.bikiC||(B.w&&S.wealth<B.w),
          auto:!u&&D.od>=DUEL_K.bikiC+6&&(D.hes||D.R<40)&&(B.g!=='heal'||D.mhp<=50)&&(B.g!=='wall'||D.mhp<=60),
          f:()=>{ D.used['bk_'+b.k]=1; D.od-=DUEL_K.bikiC; if(B.w) add({wealth:-B.w}); if(B.g==='hex'){ D.curse={until:D.r+3,v:Math.round((mr?9:15)*x)}; log(`당신의 저주가 ${h.name}에게 감겼다. 「${DUEL_BKN[b.k]}」.`,'seal'); return duelPre(DUEL_BKN[b.k]); } return duelClash('bk',b); }}); }
      // 령주: 멈춰라
      if(w.seals>0) cs.push({grp:'seal',t:'령주: 멈춰라',d:`이번 합 서번트 전투력이 크게 떨어지고, 이번 합 보구를 쓰지 못한다${mr?` · 대마력 ${Math.round(Math.max(.4,1-.1*mr)*100)}%만 듣는다`:''} [령주 1획]`,seal:true,f:()=>{ useSeal('멈춰라'); const k=Math.max(.4,1-.1*mr); D.pre={...(D.pre||{}),stop:Math.round(20*k),stopNP:true}; log(k<1?`${h.name}의 몸이 굳었다. 그러나 대마력이 령주를 반쯤 밀어냈다.`:`${h.name}의 몸이 령주에 묶여 굳었다.`,'seal'); return duelPre('령주: 멈춰라'); }}); }
    // 말을 건다
    const T=D.ctx, mu=duelMu(T.stage);
    if(T.promise&&!D.talked.p) cs.push({grp:'talk',t:'그날의 약속',d:T.promise==='kept'?'둘째 날 밤, 지금의 당신으로 남겠다고 한 약속을 꺼낸다 · 결심이 크게 흔들린다 · 그 합에는 공격하지 않는다':'지키지 못한 약속을 꺼낸다 · 결심이 오히려 굳는다 · 그 합에는 공격하지 않는다',st:[{l:'인연 배율',v:'×'+mu}],stL:'인연',f:()=>duelClash('talkP')});
    if(T.memory&&!D.talked.m) cs.push({grp:'talk',t:'그날의 기억',d:T.memory==='again'?'셋째 날 밤의 대답, 「그때도 이랬다」를 꺼낸다 · 결심이 크게 흔들린다 · 그 합에는 공격하지 않는다':T.memory==='same'?'셋째 날 밤의 대답, 「같은 사람이다」를 꺼낸다 · 결심이 흔들린다 · 그 합에는 공격하지 않는다':'셋째 날 밤의 대답, 「그때와는 다르다」를 꺼낸다 · 그 합에는 공격하지 않는다',st:[{l:'인연 배율',v:'×'+mu}],stL:'인연',f:()=>duelClash('talkM')});
    const sw=hpWord(D.shp), mw=hpWord(D.mhp);
    decide({title:`${h.name} · ${D.r}합`,body:`상대 ${sw} · 우리 ${mw} · 결심 ${DUEL_BW[duelBlade(D.R)]}${D.hes?' · 망설인다':''}`,war:true,battle:true,duel:true,choices:cs}); }
  // 마스터 행동을 쓴 뒤: 같은 합에서 공격 방식을 고른다
  function duelPre(t){ const D=W().duel; D.mR=D.r; soon(()=>duelRound(),.9); return ''; }
  const DUEL_EYE={charm:'이번 합 서번트가 한 번 더 머뭇거린다 · 서번트 전투력이 떨어진다',bind:'이번 합 서번트가 한 번 더 머뭇거린다 · 서번트 전투력이 떨어진다',flame:'이번 합 서번트 전투력이 크게 떨어진다',stone:'세 합 동안 서번트가 굳는다 · 대마력이 높을수록 덜 듣는다',future:'세 합 동안 받는 피해를 크게 줄인다',jinx:'흉 표식을 새긴다 · 표식 하나마다 서번트 전투력 −5',compel:'세 합 동안 서번트의 공격 방식을 정한다 · 대마력이면 두 합',telek:'이번 합 받는 피해를 줄인다'};
  function duelEye(id){ const D=W().duel, h=hero(), F=giftF(), mr=SV(h,'mr'), P=D.pre||(D.pre={});
    if(id==='charm'||id==='bind'){ P.reroll=true; P.deb=(P.deb||0)+Math.round((id==='charm'?5:6)+F*1.5); }
    else if(id==='flame') P.deb=(P.deb||0)+Math.round(8+F*2);
    else if(id==='stone') D.eyeDeb={until:D.r+2,v:Math.round((14+F*3)*Math.max(0,1-.15*mr))};
    else if(id==='future') D.eyeGuard={until:D.r+2,v:Math.min(.5,.25+F*.04)};
    else if(id==='jinx') D.jinx=Math.min(3,D.jinx+1);
    else if(id==='compel'){ D.compel=D.r+(mr?1:2); add({will:-2}); lean('cruel',1); }
    else if(id==='telek') P.guard=Math.max(P.guard||0,Math.min(.5,.2+F*.03));
    log(`당신의 눈이 ${h.name}${J(h.name,을)} 붙잡았다. 「${GIFTS[id].n}」.`,'skill'); }
  // 한 합의 처리: kind = magic · round · bk(비기) · talkP · talkM
  function duelClash(kind,bk){ const w=W(), D=w.duel, h=hero(), M=duelMaster(), mh=duelMH(M), night=w.tod!=='낮', n=h.name, P0=D.pre||{}; D.pre=null;
    const b0={mhp:D.mhp,od:D.od,shp:D.shp,sm:D.sm};
    const mr=SV(h,'mr'), talk=kind==='talkP'||kind==='talkM', isBk=kind==='bk', B=isBk?DUEL_BK[bk.k]:null;
    // 망설임 한 번 더 (매료 · 속박)
    if(P0.reroll&&!D.hes&&duelHes(D)){ D.hes=true; log(`${n}${J(n,이)} 당신의 눈을 피하지 못했다. 칼끝이 늦었다.`,'war'); }
    const hes=D.hes;
    // 마스터 공격의 오드
    let pay=0; if(kind==='magic') pay=Math.max(2,Math.round((5+ri(0,3))*Math.max(.75,Math.min(1.2,1-(M.P[3]-3)*.08)))); else if(kind==='round') pay=3+ri(0,3);
    if(pay){ if(D.od>=pay) D.od-=pay; else { const lack=pay-D.od; D.od=0; D.mhp-=lack*DUEL_K.oddPay; log('오드가 바닥났다. 회로를 혹사해 억지로 끌어냈다.','loss'); } }
    // 서번트: 공격 방식 · 마력 · 보구
    let sk='round'; if(!hes&&!(D.compel>=D.r)){ let bv=-9; for(const k of atkKinds(h)){ const v=atkVal(k,h,h.s,mh,M.P,night); if(v>bv+.02){ bv=v; sk=k; } } }
    D.sm=Math.max(0,D.sm-Math.round((3+ri(0,3))*(h.cls==='berserk'?1.4:1)+(SV(h,'mad')?1:0)));
    const npG=Math.max(0,Math.min(1,(D.R-DUEL_K.npA)/DUEL_K.npW)), role=npRole(h); let np=false;
    if(!hes&&!P0.stopNP&&npG>0&&!D.npUsed&&D.sm>=duelNpCost(h)){
      if('AS'.includes(role)){ const p=role==='A'?.1+(D.shp<50?.1:0)+.1+(D.mhp<=35?.25:0):.05+(100-D.shp)*.004+.08; if(ch(p*npG)) np=true; }
      else if(ch((D.r<=2?.3:.08)*npG)){ D.npUsed=true; D.sm-=duelNpCost(h); const a=artOf(h);
        log(`${n}${J(n,이)} 보구를 해방했다. “${a.n}.”`,'war');
        if(role==='D'){ D.sWall=D.r+2; log('보구의 방벽이 서번트를 감쌌다.','war'); } else if(role==='H'){ D.shp=Math.min(100,D.shp+20); log('보구의 빛이 서번트의 상처를 메웠다.','war'); } else { D.sBuff=D.r+2; log('보구의 힘이 서번트를 떠받쳤다.','war'); } } }
    if(np){ D.npUsed=true; D.sm-=duelNpCost(h); log(`${n}${J(n,이)} 보구를 해방했다. “${artOf(h).n}.”`,'war'); }
    // 힘 겨루기
    const chk=D.chk===D.r?ri(6,10):0, oddPen=D.od<=0?DUEL_K.odd0:0;
    const P=heroBase(M.P,D.mhp)+M.gi+(P0.pow||0)+(rnd()*36-18)-oddPen-chk-(kind==='magic'&&h.cls!=='caster'?mr*1.2:0);
    const E=duelSPow(D)-(hes?DUEL_K.hP:0)-(P0.deb||0)-(P0.stop||0)-(D.curse&&D.curse.until>=D.r?D.curse.v:0)-(D.eyeDeb&&D.eyeDeb.until>=D.r?D.eyeDeb.v:0)-D.jinx*5+(rnd()*36-18)-(D.sm<=0?30:D.sm<15?10:0)+(D.sBuff>=D.r?8:0)-(sk==='magic'?M.soy*1.2:0);
    const d=P-E, guard=Math.max(P0.guard||0,D.eyeGuard&&D.eyeGuard.until>=D.r?D.eyeGuard.v:0), wallOn=D.wallM>=D.r;
    const inM=atkM(sk,h,h.s,mh,M.P,night)*(1-guard), outM=kind==='magic'||kind==='round'?atkM(kind,mh,M.P,h,h.s,night):0;
    const sTake=x=>Math.max(1,Math.round((x-grdD(h))*(1-Math.min(.35,SV(h,'evade')*.035))*sgfM(h)*(D.sWall>=D.r?.5:1)));
    const hitMe=x=>{ if(wallOn&&!np) return; D.mhp-=x; };
    // 비기 · 말을 건다 · 보구
    if(talk){ const mu=duelMu(D.ctx.stage);
      if(kind==='talkP'){ D.talked.p=1; if(D.ctx.promise==='kept'){ D.R=Math.max(0,D.R-10*mu); D.hesUp=D.r+2; log(`“지금의 나로 남겠다고 했지.” ${n}의 칼끝이 떨렸다.`,'war'); log(`${n}: “…그 약속을, 지금 꺼내는 건가.”`,'voice'); }
        else { D.R=Math.min(100,D.R+5); log(`지키지 못한 약속을 꺼냈다. ${n}의 눈이 차가워졌다.`,'war'); log(`${n}: “그 말을 할 자격이, 그대에게 있나.”`,'voice'); } }
      else { D.talked.m=1; const v=D.ctx.memory==='again'?12:D.ctx.memory==='same'?8:0; D.R=Math.max(0,D.R-v*mu);
        log(v?`셋째 날 밤의 대답을 꺼냈다. ${n}${J(n,이)} 한순간 눈을 감았다.`:`셋째 날 밤의 대답을 꺼냈다. ${n}${J(n,은)} 아무것도 말하지 않았다.`,'war'); }
      if(np) D.mhp-=duelNpDmg(h,M.soy); else if(d<=-8) hitMe(Math.max(1,Math.round((6+(-d)*.3)*inM))); else if(d<8) hitMe(ri(2,5)); }
    else if(isBk){ const x=bk.x, nm=DUEL_BKN[bk.k];
      if(B.g==='heal'){ D.mhp=Math.min(100,D.mhp+Math.round(20*x)); log(`상처가 빛 속에서 닫혔다. 「${nm}」.`,'skill'); }
      if(np&&B.g!=='heal'){ D.wallM=0; log(`보구 앞에서 비기가 꺾였다. 「${nm}」.`,'loss'); D.mhp-=duelNpDmg(h,M.soy); }
      else if(np){ D.mhp-=duelNpDmg(h,M.soy); }
      else { if(B.g==='atk'){ const v=Math.max(3,Math.round(B.d*x*(B.av&&h.cls==='avenger'?2:1)*(.85+rnd()*.3)*(B.mr?1-Math.min(.4,mr*.04):1)*(B.ev?1-Math.min(.35,SV(h,'evade')*.035):1))); D.shp-=v; log(`힘 겨루기를 건너뛰고, 비기가 ${n}에게 닿았다. 「${nm}」.`,'skill'); }
        if(B.g==='wall'){ D.wallM=D.r+2; log(`당신의 둘레에 결계가 섰다. 서번트의 칼이 닿지 않는다. 「${nm}」.`,'skill'); }
        if(!(D.wallM>=D.r)){ if(d<=-8) hitMe(Math.max(1,Math.round((6+(-d)*.3)*inM))); else if(d<8) hitMe(ri(2,5)); } } }
    else if(np){ hitMe(duelNpDmg(h,M.soy)); if(wallOn){ D.wallM=0; log('보구가 결계를 깨뜨렸다.','loss'); }
      if(d>=8) D.shp-=sTake((6+d*.3)*outM); else if(d>-8) D.shp-=ri(2,5); }
    else { const rv=Math.abs(d)>=8&&ch(revP(d>0?h.s:M.P))?(d>0?'e':'m'):null;
      if(Math.abs(d)<8){ hitMe(Math.round(ri(3,7)*(1-guard))); D.shp-=ri(3,7)*(D.sWall>=D.r?.5:1); log(pickNR(['칼끝과 마력이 몇 번이고 엇갈렸다. 승부가 나지 않는다.','서로 한 걸음씩 물러섰다. 숨을 고른다.'],'duelEven'),'war'); }
      else if(rv==='m'){ D.shp-=sTake((6+8*.3)*outM); hitMe(ri(1,5)); log(`밀리던 당신이 한순간 틈을 비집고 들어갔다. 일격이 ${n}에게 닿았다.`,'war'); }
      else if(rv==='e'){ hitMe(Math.max(1,Math.round((6+8*.3)*inM))); D.shp-=ri(1,4); log(`몰아붙이던 순간, ${n}의 칼이 먼저 닿았다.`,'loss'); }
      else if(d>0){ if(ch(dodgeP(h.s[1],M.P[1])*(kind==='magic'?MG.dodge:1))){ hitMe(ri(1,3)); log(`${n}${J(n,이)} 당신의 공격을 흘려 냈다.`,'war'); }
        else { D.shp-=sTake((6+d*.3)*outM); hitMe(ri(1,5)); log(kind==='magic'?pickNR([`마탄이 ${n}의 어깨를 꿰뚫었다.`,`당신의 마술이 ${n}${J(n,을)} 덮쳤다.`],'duelMagW'):pickNR([`강화를 두른 팔로 자루를 걷어 내고, ${n}의 품으로 파고들었다.`,`당신의 일격이 ${n}의 옆구리에 꽂혔다.`],'duelRndW'),'war'); } }
      else { if(ch(dodgeP(M.P[1],h.s[1])*(sk==='magic'?MG.dodge:1))){ D.shp-=ri(1,3); log(`${n}의 일격을 간신히 피했다.`,'war'); }
        else { hitMe(Math.max(1,Math.round((6+(-d)*.3)*inM))); D.shp-=ri(1,5); log(pickNR([`${n}의 칼이 당신을 베고 지나갔다.`,`피할 틈이 없었다. ${n}의 일격이 당신에게 꽂혔다.`],'duelLose'),'loss'); } } }
    if(hes&&!talk) log('✓ 망설임 — 서번트의 공격이 한 박자 늦었다','check');
    if(wallOn&&!np&&!talk&&!isBk) log('✓ 결계 — 서번트의 칼이 닿지 않았다','check');
    duelComp(D,Math.max(0,b0.shp-D.shp));
    D.mhp=Math.max(0,Math.round(D.mhp)); D.shp=Math.max(0,Math.round(D.shp)); D.od=Math.max(0,Math.round(D.od));
    const out=[], dl=(l,a,b)=>{ const v=Math.round(b)-Math.round(a); if(v) out.push(`${l} ${v>0?'+':'−'}${Math.abs(v)}`); };
    dl('건강',b0.mhp,D.mhp); dl('오드',b0.od,D.od); dl('적 서번트 건강',b0.shp,D.shp); dl('적 서번트 마력',b0.sm,D.sm);
    if(out.length) log(out.join(' · '),'delta');
    if(D.mhp<=0||D.shp<=0) return duelEnd(D.shp<=0&&D.mhp>0);
    D.r++; soon(()=>duelRound()); return ''; }
  // 동행: 서번트 쪽에 선 동맹 조 (지금 동행 규칙 · 상대는 마스터)
  function duelComp(D,lost){ if(D.ctx.ally==null||D.compOut||D.shp<=0||D.mhp<=0) return; const w=W(), p=w.pairs.find(x=>x.i===D.ctx.ally); if(!p||!p.alive){ D.compOut=true; return; }
    const ph=H_BY[p.hero], pN=pName(p), M=duelMaster(), mh=duelMH(M);
    if(ch(.3)) p.hp=clamp(p.hp-ri(3,8));
    if(!D.compNP&&p.hp>20&&(D.shp<=35||D.mhp<=35||D.r>=2&&ch(.15))&&ch(.7)){ D.compNP=true; const v=Math.max(3,Math.round(duelNpDmg(ph,M.soy)*CXB.np)); D.mhp-=v; log(`보구 해방 — ${pN}의 「${artOf(ph).n}」. 당신이 빛에 휩쓸렸다.`,'allynp'); return; }
    const act=Math.max(.3,Math.min(.85,.5+(npcPower(p,false,1)-CXB.ref)*.01))*(.5+.5*p.hp/100);
    if(ch(act)){ if(lost>=6&&ch(.7)){ const a=Math.round(lost*(.35+rnd()*.2)); D.shp=Math.min(100,D.shp+a); p.hp=clamp(p.hp-Math.round(a*1.2)); log(`${pN}${J(pN,이)} 사이로 뛰어들어 서번트에게 향하던 일격을 대신 받았다.`,'war'); }
      else if(ch(.25)){ D.chk=D.r+1; log(`${pN}${J(pN,이)} 옆에서 당신의 발을 묶었다.`,'war'); }
      else { const PP=npcParams(p).p; let k='round',bv=-9; for(const kk of atkKinds(ph)){ const v=atkVal(kk,ph,PP,mh,M.P,true); if(v>bv+.02){ bv=v; k=kk; } }
        if(ch(dodgeP(M.P[1],PP[1])*(k==='magic'?MG.dodge:1))) log(`${pN}의 일격을 간신히 피했다.`,'war');
        else { D.mhp-=Math.max(2,Math.round((4+ri(0,5))*CXB.ad*atkM(k,ph,PP,mh,M.P,true)*(.6+.4*p.hp/100))); log(`${pN}${J(pN,이)} 옆에서 파고들었다. 당신의 옆구리가 베였다.`,'loss'); } } }
    if(p.hp<=0||p.hp<30&&ch(.5)){ D.compOut=true; log(`${pN} 조가 더 버티지 못하고 물러났다.`,'war'); } }
  // 끝: 결과를 되돌려 쓰고, 상황별 뒤처리를 부른다
  const DUEL_END={test:win=>log(win?'결투가 끝났다. 당신이 서 있었다.':'결투가 끝났다. 서번트의 칼이 당신 앞에서 멈췄다.','war')};
  // 결과는 선택이 끝난 뒤(큐)에서 되돌려 쓴다: 마지막 합의 변화 칩에 섞이지 않게
  function duelEnd(win){ const w=W(), D=w.duel, h=hero(); if(!D) return; D.res=win?'win':'lose';
    log(win?`${h.name}${J(h.name,이)} 무릎을 꿇었다. 칼이 손에서 미끄러졌다.`:`${h.name}의 칼끝이 당신의 목 앞에서 멈췄다.`,win?'war':'loss');
    soon(()=>{ const D2=w.duel; if(!D2) return; S.st.health=Math.max(1,Math.min(100,D2.mhp)); w.hp=Math.max(0,D2.shp); w.sm=D2.sm;
      const k=D2.ctx.kind, won=D2.res==='win'; w.duelLast={kind:k,res:D2.res,r:D2.r,R:Math.round(D2.R)}; w.duel=null;
      // 11-22: 서번트끼리의 전투처럼 결과를 알리는 창(닫으면 뒤처리)
      decide({title:`${h.name} · 결투 종료`,body:`${won?'당신이 이겼다':'당신이 졌다'} · 상대 ${hpWord(Math.max(0,D2.shp))} · 당신 ${hpWord(Math.max(0,D2.mhp))}`,war:true,silent:true,choices:[{t:'닫기',auto:true,f:()=>{ (DUEL_END[k]||DUEL_END.test)(won); return null; }}]}); }); return ''; }
  // 상세 화면용 정보
  function duelView(){ const w=W(), D=w&&w.duel; if(!D) return null; const h=hero(), M=duelMaster(), mr=SV(h,'mr'), A=artOf(h);
    const hiN=M.hi.map(id=>`${ARTS[id].n} · ${ART_TIER[M.lv(id)]}`), mods={me:[],en:[]};
    mods.me.push({n:'잔의 힘',v:M.gi,d:'가득 찬 잔을 쥔 사람이다. 회로가 그릇이고, 고위 기술이 그 힘을 다루는 솜씨다',x:`회로 ${GR[S.circuit]||'?'} · 고위 기술 ${M.hi.length}`});
    if(D.chk===D.r) mods.me.push({n:'협공을 받는다',v:-8,d:'동행 조가 발을 묶었다',dur:'이번 합'});
    if(D.od<=0) mods.me.push({n:'오드 바닥',v:-DUEL_K.odd0,d:'오드가 바닥났다. 공격할 때마다 건강을 깎는다'});
    if(mr) mods.en.push({n:'대마력',v:mr*1.2,d:'마술로 칠 때 힘이 깎이고, 마술 피해도 줄어든다',x:skillsOf(h).filter(x=>x.k==='mr').map(x=>`${x.n} ${x.r}`).join(' · ')});
    mods.en.push({n:'마스터 지원 없음',v:-6,d:'마스터가 보태던 몫 없이, 서번트 혼자의 힘으로 싸운다'});
    if(D.hes) mods.en.push({n:'망설임',v:-DUEL_K.hP,d:'결심이 흔들려 이번 합 공격이 늦다 · 보구를 쓰지 않는다',dur:'이번 합'});
    if(D.curse&&D.curse.until>=D.r) mods.en.push({n:'저주',v:-D.curse.v,d:'비기의 저주가 몸을 묶고 있다',dur:`${D.curse.until-D.r+1}합`});
    if(D.wallM>=D.r) mods.me.push({n:'결계',v:8,d:'서번트의 평소 공격이 닿지 않는다 · 보구에는 깨진다',dur:`${D.wallM-D.r+1}합`});
    const comp=D.ctx.ally!=null?(()=>{ const p=w.pairs.find(x=>x.i===D.ctx.ally); return p?{hero:p.hero,name:pName(p),rev:!!p.revealed,hp:p.hp,alive:p.alive,out:D.compOut,np:D.compNP}:null; })():null;
    return {r:D.r,me:{ranks:M.P.slice(0,5).map(dRank),hp:Math.round(D.mhp),od:Math.round(D.od),odMax:D.odMax,seals:w.seals,soy:M.soy?dRank(M.soy):'',arts:hiN,mods:mods.me,mage:mCanMagic()},
      sv:{id:h.id,name:h.name,cls:CLS[h.cls].n,ranks:h.s.slice(0,5),hp:Math.round(D.shp),sm:Math.round(D.sm),mr:skillsOf(h).filter(x=>x.k==='mr').map(x=>x.r)[0]||'',np:`${A.n} · ${A.r}`,blade:duelBlade(D.R),hes:!!D.hes,mods:mods.en},comp}; }
