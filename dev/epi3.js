  /* ---------- 11-21: 서번트가 떠난 삶의 봄과 첫 해 · 에필로그 성향 사건 ----------
     떠난 갈래: away 세상을 보러 보냄 · win 소원을 이루고 사라짐 · lost 전쟁에서 잃음. 단꿈의 생 · 숙청으로 떠난 삶은 예전 방식 그대로
     A 봄의 열나흘(하루씩) → B 첫 해(한 달씩, 2~12달째) → D 예전 방식. 함께 사는 생과 달리 C(열 해)는 두지 않는다 */
  const afS=k=>((S.aff&&S.aff[k])||0)>=({judge:3,avenger:3}[k]||4), afD=k=>((S.aff&&S.aff[k])||0)>=8;
  const lkM=()=>isMage()&&!S.flags.mundane;
  const lkKid=()=>((S.fam&&S.fam.kids)||[]).length>0;
  const lkFam=()=>{ const F=S.fam||{}; return !!((F.father&&F.father.alive)||(F.mother&&F.mother.alive)||(F.spouse&&F.spouse.alive)||(F.kids||[]).length); };
  const lkJob=()=>!!S.flags.job&&S.flags.job!=='연구';
  const lkOther=()=>(WV().pairs||[]).some(p=>p.mname&&p.master!==false);
  const lkStray=()=>(WV().pairs||[]).some(p=>p.alive&&!p.out);
  function loneKind(){ if(!S.hero||!H_BY[S.hero]||S.flags.bxDream||stayHome()) return null;
    if(S.flags.stay) return S.flags.stayAway&&!S.flags.stayDied&&S.flags.stayAwayWhy==='travel'?'away':null;
    return GRAIL()?'win':'lost'; }
  const ep3K=()=>(S.epi&&S.epi.lone)||'lost';
  const EP3_RATE={A:.7,B:.75};
  /*EP3_DATA*/
  function ep3Start(k){ const E=S.epi; E.ph='A'; E.lone=k; E.d=0; E.m=1; E.k=0; E.dayU=[]; E.lu=[]; }
  function ep3Ok(x){ const E=S.epi; if(x.ph!==E.ph||(E.lu||[]).includes(x.id)) return false;
    if(x.k&&!x.k.includes(E.lone)) return false;
    if(x.day&&(E.d<x.day[0]||E.d>x.day[1])) return false; if(x.mon&&(E.m<x.mon[0]||E.m>x.mon[1])) return false;
    return !x.c||x.c(); }
  function ep3Go(x){ const E=S.epi; E.lu=E.lu||[]; E.lu.push(x.id); E.used=E.used||[]; if(x.blk) for(const b of x.blk) if(!E.used.includes(b)) E.used.push(b);
    S.resumeEv={src:'EP2',id:'@lone'+x.id}; x.f(); if(!S.pending) S.resumeEv=null; }
  function ep3Pick(){ if(S.pending||S.dead) return; const E=S.epi;
    const fx=EP3_EV.find(x=>x.must&&ep3Ok(x)); if(fx) return ep3Go(fx);
    if(!ch(EP3_RATE[E.ph])) return;
    const c=EP3_EV.filter(x=>!x.must&&ep3Ok(x)); if(c.length) ep3Go(wpick(c,x=>x.w||1)); }
  // 한 걸음. true면 이 걸음을 여기서 처리했다
  function ep3Step(){ const E=S.epi, K=E.lone;
    if(E.ph==='A'){
      if(E.d>=EP2_N.A){ E.ph='B'; log('열나흘이 지났다. 이제 달이 지나간다.','sys'); return ep3Step(); }
      E.d++; E.k++; log(`봄 · ${E.d}일째`,'night');
      if(E.d>=EP2_N.A) log(EP3_DAYL[K]||EP3_DAYL.d,'n');
      else { const kk=EP3_DAYK[K]||[], pool=EP3_DAY.map((_,i)=>i).concat(kk.map((_,i)=>100+i)).filter(i=>!E.dayU.includes(i)); if(pool.length){ const i=pick(pool); E.dayU.push(i); log(i>=100?kk[i-100]:EP3_DAY[i],'n'); } }
      ep3Pick(); H.change(); return true; }
    if(E.ph==='B'){
      if(E.m>=EP2_N.B){ E.ph='D'; log(EP3_END,'sys'); H.change(); return true; }
      E.m++; E.k++; log(`첫 해 · ${E.m}달째`,'night');
      const mk=(EP3_MONK[K]||{})[E.m]; log(mk&&ch(.6)?mk:EP3_MON[E.m],'n');
      if(E.m===EP2_N.B){ S.age++; S.year++; mark('calm'); if(S.age>=40) add({health:-ageWear()}); famYear(); if(S.pending) S.pending=null; }   // 첫 해의 끝: 한 살을 먹는다 (이 구간에는 사망 판정이 없다)
      ep3Pick(); H.change(); return true; }
    return false; }
