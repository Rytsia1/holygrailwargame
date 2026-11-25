"""Personality-driven AI & 6-Axis Relationship System patch script (airel1125).
Usage: python3 ai_rel_apply.py <game.html>
"""
import sys, os, json, re, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'airel1125' in s:
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

# 1. Core Personality Models, 6-Axis Relationship Matrix & Betrayal Engine in Sim
AI_REL_CORE = r"""
  /* ---------- 성격 모델 & 6축 관계망 (airel1125) ---------- */
  const REL_AXES = ['trust', 'affection', 'fear', 'respect', 'rivalry', 'grudge'];
  const CUNNING_AID = new Set(['priest','atlas','prodigy','fortune','antique','stage','eighth','detective','lecturer']);
  const RUTHLESS_AID = new Set(['killer','exec','executor','burial','apostle','merc','cultist','priest','avenger']);
  const PRIDE_AID = new Set(['heir','lord','collector','wanderer']);
  const LOYAL_AID = new Set(['democrat','veteran','mother','student','sibling','elder','kendo']);

  function servantPersona(h){
    if(!h) return {pride:50,loyalty:50,caution:50,ruthless:40,tags:[]};
    const x = HX[h.id] || {}, tr = h.traits || [];
    const pride = clamp(40 + (x.k==='오만'?40:(x.k==='기품'||x.k==='엄격')?18:x.k==='열정'?12:0) + (tr.includes('명예')?18:0) + (tr.includes('야망')?12:0) - (x.k==='순진'||x.k==='다정'?15:0));
    const loyalty = clamp(40 + (tr.includes('충성')?35:0) + (x.p==='질서'?15:x.p==='혼돈'?-10:0) + (h.sp==='guard'?15:0) - (h.sp==='traitor'?45:0) - (tr.includes('자유')?8:0));
    const caution = clamp(40 + (['caster','shadow','bow'].includes(h.cls)?18:h.cls==='berserk'?-30:0) + (x.k==='냉소'||x.k==='능청'?18:x.k==='광기'?-25:0) + (h.sp==='escape'||h.sp==='intel'?15:0));
    const ruthless = clamp(30 + (x.a==='악'?35:x.a==='선'?-15:0) + (tr.includes('야망')?15:0) - (tr.includes('연민')?25:0) + (x.k==='냉소'||x.k==='광기'?12:0));
    const tags = [];
    if(pride >= 70) tags.push('prideful');
    if(loyalty >= 70) tags.push('loyal');
    if(caution >= 65) tags.push('cunning');
    if(ruthless >= 65) tags.push('ruthless');
    if(h.cls === 'berserk' || x.k === '광기') tags.push('berserk');
    return {pride, loyalty, caution, ruthless, tags};
  }

  function masterPersona(p){
    if(!p) return {pride:45,cunning:45,ruthless:45,loyal:45,caution:45,tags:[]};
    const aid = p.aid || '', tac = p.tac || 'proud';
    const pride = clamp(40 + (PRIDE_AID.has(aid)?35:0) + (tac==='proud'?25:tac==='reckless'?10:tac==='naive'?-15:0));
    const cunning = clamp(35 + (CUNNING_AID.has(aid)?38:0) + (tac==='cunning'?28:tac==='defensive'?15:tac==='reckless'?-20:0));
    const ruthless = clamp(35 + (RUTHLESS_AID.has(aid)?38:0) + (tac==='hunter'?22:tac==='reckless'?12:tac==='naive'||LOYAL_AID.has(aid)?-18:0));
    const loyal = clamp(45 + (LOYAL_AID.has(aid)?28:0) + (tac==='defensive'||tac==='naive'?15:0) - (RUTHLESS_AID.has(aid)?22:0));
    const caution = clamp(40 + (tac==='defensive'||tac==='cunning'?25:tac==='reckless'?-22:0) + (CUNNING_AID.has(aid)?15:0));
    const tags = [];
    if(pride >= 65) tags.push('prideful');
    if(cunning >= 65) tags.push('cunning');
    if(ruthless >= 65) tags.push('ruthless');
    if(loyal >= 65) tags.push('loyal');
    return {pride, cunning, ruthless, loyal, caution, tags};
  }

  function personaOf(who){
    if(who === 'me') return {master:null, servant:servantPersona(hero())};
    if(!who) return null;
    return {master:masterPersona(who), servant:servantPersona(H_BY[who.hero])};
  }

  const pIdOf = x => x === 'me' || x === 'hero' ? x : (typeof x === 'string' ? x : ('p' + x.i));
  const relKey = (a, b) => pIdOf(a) + '|' + pIdOf(b);

  function relSeed(a, b){
    const w = S && S.war;
    const d = {trust:25, affection:10, fear:0, respect:20, rivalry:10, grudge:0};
    if(a === 'me' && b === 'hero'){
      const h = hero(), sp = servantPersona(h), A = S.aff || {};
      d.trust = w ? Math.round(w.trust) : 50;
      d.affection = clamp(Math.round(((w ? w.fit : 60) - 35) * 0.7 + (h && h.traits.includes('연민') ? 10 : 0)));
      d.respect = clamp(20 + (S.circuit || 1) * 5 + Math.round((S.st && S.st.will || 20) * 0.2) + (h && h.traits.includes('명예') && (A.judge || 0) >= 2 ? 12 : 0));
      d.fear = clamp(((A.cruel || 0) + (A.taboo || 0)) * 5);
      d.rivalry = clamp(sp.pride >= 70 ? 20 + (A.zeal || 0) * 3 : 5);
      d.grudge = (w && w.fit < 45) ? 10 : 0;
      return d;
    }
    const pa = w && (w.pairs || []).find(x => 'p'+x.i === a);
    const pb = w && (w.pairs || []).find(x => 'p'+x.i === b);
    if(pa && b === 'me'){
      const mp = masterPersona(pa), A = S.aff || {};
      d.trust = pa.aid === 'executor' ? 5 : pa.aid === 'democrat' ? 40 : 25;
      d.affection = pa.aid === 'democrat' ? 20 : 10;
      d.fear = clamp(Math.round((A.cruel || 0) * 4));
      d.respect = clamp(20 + (S.circuit || 1) * 4);
      d.rivalry = mp.pride >= 70 ? 25 : 10;
      d.grudge = pa.aid === 'executor' ? 15 : 0;
      return d;
    }
    if(pa && pb){
      const pk = PAIRV[pa.hero + '|' + pb.hero] || PAIRV[pb.hero + '|' + pa.hero];
      if(pk){ d.rivalry = clamp(d.rivalry + 28); d.respect = clamp(d.respect + 22); }
      if((pa.aid === 'burial' || pa.aid === 'executor') && pb.aid === 'apostle') d.grudge = 55;
      if(pa.aid === 'apostle' && (pb.aid === 'burial' || pb.aid === 'executor')) d.fear = 25;
    }
    return d;
  }

  function ensureRels(){
    const w = W(); if(!w) return {};
    if(!w.rels) w.rels = {};
    if(!w.rels['me|hero'] && S.hero) w.rels['me|hero'] = relSeed('me', 'hero');
    for(const p of (w.pairs || [])){
      const k = 'p' + p.i + '|me';
      if(!w.rels[k]) w.rels[k] = relSeed('p'+p.i, 'me');
    }
    return w.rels;
  }

  function relGet(a, b){
    const w = W(); if(!w) return {trust:50,affection:15,fear:0,respect:20,rivalry:0,grudge:0};
    ensureRels();
    const ka = pIdOf(a), kb = pIdOf(b), k = ka + '|' + kb;
    if(!w.rels[k]) w.rels[k] = relSeed(ka, kb);
    const r = w.rels[k];
    if(ka === 'me' && kb === 'hero') r.trust = Math.round(w.trust);
    return r;
  }

  function relShift(a, b, delta){
    const w = W(); if(!w || !delta) return null;
    const ka = pIdOf(a), kb = pIdOf(b), r = relGet(ka, kb);
    for(const ax of REL_AXES){
      if(delta[ax]){
        if(ka === 'me' && kb === 'hero' && ax === 'trust'){
          w.trust = clamp(w.trust + delta.trust);
          r.trust = Math.round(w.trust);
        } else {
          r[ax] = clamp((r[ax] || 0) + delta[ax]);
        }
      }
    }
    return r;
  }

  function betrayScore(rel, persona, ctx = {}){
    if(!rel || !persona) return 0.1;
    const ruth = persona.ruthless ?? 40;
    const loy = persona.loyal ?? persona.loyalty ?? 45;
    const tr = rel.trust ?? 25, aff = rel.affection ?? 10, resp = rel.respect ?? 20;
    const fear = rel.fear ?? 0, riv = rel.rivalry ?? 0, grd = rel.grudge ?? 0;
    let s = 0.12 + (ruth - 40) * 0.005 + grd * 0.006 + riv * (ctx.final ? 0.004 : 0.0015);
    s += Math.max(0, 50 - tr) * 0.0055 + Math.max(0, 30 - aff) * 0.003;
    s -= tr * 0.0035 + aff * 0.003 + resp * 0.0025 + (loy - 40) * 0.004;
    s += (ctx.slight || 0) * 0.1 - (ctx.owe || 0) * 0.08;
    const weak = (ctx.seals ?? 1) === 0 || (ctx.hp ?? 100) < 40;
    s += weak ? (fear * 0.003) : -(fear * 0.0045);
    return Math.max(0.01, Math.min(0.95, s));
  }

  function loyalIntercept(b, dmg, srcTxt){
    const w = W(), h = hero(); if(!w || !w.heroAlive || !h) return false;
    const sp = servantPersona(h), rh = relGet('me', 'hero');
    if(sp.loyalty < 70 || rh.grudge >= 45 || w.trust < 30) return false;
    const p = Math.min(0.85, 0.35 + (sp.loyalty - 70) * 0.01 + rh.affection * 0.004 + w.trust * 0.003);
    if(!ch(p)) return false;
    w.hp = clamp(w.hp - Math.max(2, Math.round(dmg * 0.35)));
    log(`${h.name}${J(h.name,이)} 몸을 던져 ${srcTxt} 막아 냈다.`, 'war');
    if(CHK) CHK.push({txt:'「충의」로운 서번트가 당신을 지켜 냈다', ok:true});
    relShift('me', 'hero', {trust:2, affection:3, respect:2});
    return true;
  }
"""
rp("  const W=()=>S.war;", AI_REL_CORE + "  const W=()=>S.war;")

# 2. Initialize rels at summonCast
rp(
"    S.war.queue.push(()=>firstMeeting());",
"    ensureRels();\n    S.war.queue.push(()=>firstMeeting());"
)

# 3. useSeal relationship impact (fear + grudge on forced seals)
rp(
"if(word==='이겨라') w.trust=clamp(w.trust+fitT(w.trust>60?-3:4));",
"if(word==='이겨라') w.trust=clamp(w.trust+fitT(w.trust>60?-3:4));\n    { const h=hero(), sp=servantPersona(h); relShift('me','hero',{fear:10,grudge:(sp.pride>=70||(h&&h.traits.includes('자유')))?8:3,affection:-4}); }"
)

# 4. talk() affection & respect shift
rp(
"w.trust=clamp(w.trust+trustGain(g)); w.hp=clamp(w.hp+5); relGain(8);",
"w.trust=clamp(w.trust+trustGain(g)); w.hp=clamp(w.hp+5); relGain(8); relShift('me','hero',{affection:5,respect:3,grudge:-4});"
)
rp(
"if(g===null){ w.trust=clamp(w.trust-2); log(`${h.name}",
"if(g===null){ w.trust=clamp(w.trust-2); relShift('me','hero',{affection:-3,grudge:4}); log(`${h.name}"
)
rp(
"if(g===null){ w.trust=clamp(w.trust-2); log(pick([",
"if(g===null){ w.trust=clamp(w.trust-2); relShift('me','hero',{affection:-3,grudge:4}); log(pick(["
)

# 5. sealsGone() uses betrayScore
rp(
"    const ambitious = h.sp==='traitor'||h.traits.includes('야망');\n    if(w.trust<35&&(ambitious||ch(.25))){",
"    const sp=servantPersona(h), rh=relGet('me','hero'), bP=betrayScore(rh,sp,{seals:0,hp:w.hp});\n    const ambitious = h.sp==='traitor'||h.traits.includes('야망')||rh.grudge>=60;\n    if((w.trust<35||rh.grudge>=70)&&(ambitious||ch(bP))){"
)

# 6. retreat() — Prideful Servant refuses retreat + Loyal Servant protects retreating Master
rp(
"    if(!sure&&w.trust<DIST&&w.heroAlive&&ch(.3)){ log(`${h.name}${J(h.name,은)} 물러서지 않았다. 당신의 말은 들리지 않는 모양이다.`,'loss'); if(CHK) CHK.push({txt:'「불신」 탓에 서번트가 명령을 듣지 않았다',ok:false}); return clash(0); }",
"    if(!sure&&w.trust<DIST&&w.heroAlive&&ch(.3)){ log(`${h.name}${J(h.name,은)} 물러서지 않았다. 당신의 말은 들리지 않는 모양이다.`,'loss'); if(CHK) CHK.push({txt:'「불신」 탓에 서번트가 명령을 듣지 않았다',ok:false}); relShift('me','hero',{respect:-3,grudge:3}); return clash(0); }\n"
"    { const sp=servantPersona(h), rh=relGet('me','hero');\n"
"      if(!sure&&w.heroAlive&&sp.pride>=70&&!(sp.loyalty>=70&&S.st.health<=40)){\n"
"        const refP=Math.max(0,Math.min(.75,(sp.pride-55)*.012+rh.grudge*.004-rh.respect*.005-(sp.loyalty>=70?.2:0)-(w.trust>=80?.25:0)));\n"
"        if(ch(refP)){ log(`${h.name}: “${h.traits.includes('명예')?'긍지를 버릴 수는 없다. 물러서지 않겠다.':'물러날 이유를 대라. 적 앞에서 등을 돌리지는 않는다.'}”`,'loss'); if(CHK) CHK.push({txt:'「긍지」 높은 서번트가 퇴각을 거부했다',ok:false}); relShift('me','hero',{grudge:3,rivalry:2}); return clash(0); }\n"
"      }\n"
"    }"
)
rp(
"    const p=(sure?1:fleeP(h,myParams().p)*(w.battle.ctx.hunted?HUNT_RET:1))-(sure?0:npFleeMinus(w.battle,'me'));",
"    const _loyB=(!sure&&S.st.health<=40&&servantPersona(h).loyalty>=70)?.18:0;\n"
"    const p=Math.min(.98,(sure?1:fleeP(h,myParams().p)*(w.battle.ctx.hunted?HUNT_RET:1)+_loyB)-(sure?0:npFleeMinus(w.battle,'me')));"
)

# 7. Loyal Servant interception in clash() & npcAct() & shadowVisit() & npcGuard()
rp(
"if(w.heroAlive&&ch(.08-S.st.will/2000)&&w.trust>=60){ w.hp=clamp(w.hp-2); log(`${mN}${J(mN,이)} 몸을 틀어 당신에게 날아드는 파편을 대신 맞았다.`,'war'); if(CHK) CHK.push({txt:'「신뢰」하는 서번트가 당신을 감쌌다',ok:true}); }",
"if(w.heroAlive&&ch(.08-S.st.will/2000)&&(w.trust>=60||servantPersona(h).loyalty>=70)){ w.hp=clamp(w.hp-2); log(`${mN}${J(mN,이)} 몸을 틀어 당신에게 날아드는 파편을 대신 맞았다.`,'war'); if(CHK) CHK.push({txt:servantPersona(h).loyalty>=70?'「충의」로운 서번트가 당신을 지켜 냈다':'「신뢰」하는 서번트가 당신을 감쌌다',ok:true}); relShift('me','hero',{trust:1,affection:2}); }"
)
rp(
"if(e.aid==='exec'&&w.heroAlive&&!b.eMasterDown&&!b.backGuard&&(b.huntNow||ch(.15))&&!npGuard(b)){ b.huntNow=false;",
"if(e.aid==='exec'&&w.heroAlive&&!b.eMasterDown&&!b.backGuard&&(b.huntNow||ch(.15))&&!npGuard(b)&&!loyalIntercept(b,10,'마탄을')){ b.huntNow=false;"
)
rp(
"if(e.aid==='executor'&&ch(.25)&&w.heroAlive&&!npGuard(b)){",
"if(e.aid==='executor'&&ch(.25)&&w.heroAlive&&!npGuard(b)&&!loyalIntercept(b,8,'흑건을')){"
)
rp(
"if(e.aid==='burial'&&ch(.3)&&w.heroAlive&&!npGuard(b)){",
"if(e.aid==='burial'&&ch(.3)&&w.heroAlive&&!npGuard(b)&&!loyalIntercept(b,10,'흑건을')){"
)
rp(
"if(e.aid==='killer'&&w.heroAlive&&ch(.3)&&!npGuard(b)){",
"if(e.aid==='killer'&&w.heroAlive&&ch(.3)&&!npGuard(b)&&!loyalIntercept(b,12,'저격탄을')){"
)
rp(
"const o=[{k:'servant',p:pRoll(40+t.pw*.3+det,50,T.s+off)}];",
"const _loyG=servantPersona(th).loyalty>=70?12:0;\n    const o=[{k:'servant',p:pRoll(40+t.pw*.3+det+_loyG,50,T.s+off)}];"
)
rp(
"if(chkp('신뢰·결계',.45+w.trust/250+w.fort/300)){",
"if(chkp('신뢰·결계',.45+w.trust/250+w.fort/300+(servantPersona(h).loyalty>=70?.2:0))){"
)

# 8. endBattle() relationship updates (me|hero and p|me)
rp(
"if(w.heroAlive&&w.hp<(w.bHp0??w.hp)-8) e.hurtMe=w.day;",
"if(w.heroAlive&&w.hp<(w.bHp0??w.hp)-8) e.hurtMe=w.day;\n"
"      if(!e.cx){\n"
"        const _eh=H_BY[e.hero], _esp=servantPersona(_eh);\n"
"        if(won||e.hp<55) relShift('p'+e.i,'me',{respect:8,fear:e.hp<35?12:6,rivalry:_esp.pride>=65?10:4,grudge:(b.ctx.attack||b.ctx.trap)?12:5});\n"
"        if(b.round>=4) relShift('p'+e.i,'me',{respect:8,rivalry:6});\n"
"        if(b.res==='talk') relShift('p'+e.i,'me',{trust:15,affection:10,respect:8,grudge:-10});\n"
"        if(won&&w.heroAlive) relShift('me','hero',{trust:2,respect:4,affection:3});\n"
"        if(b.res==='lose'||b.res==='retreat') relShift('me','hero',{respect:-2,rivalry:4});\n"
"      }"
)

# 9. NPC Retreat & Combat Lines — Prideful Servant refuses retreat, Cunning Master withdraws early
rp(
"    const ret=st.retreat===0?0:Math.max(8,Math.min(55,Math.round(t.ret+c.ret+(st.retreat-30)*.3)));\n"
"    const floor=Math.max(ret+8,Math.min(85,t.floor+c.floor));",
"    const _sp=servantPersona(H_BY[p.hero]), _mp=masterPersona(p);\n"
"    const ret=st.retreat===0?0:Math.max(6,Math.min(58,Math.round(t.ret+c.ret+(st.retreat-30)*.3-(_sp.pride>=70?10:0)+(_mp.cunning>=70?5:0))));\n"
"    const floor=Math.max(ret+8,Math.min(88,t.floor+c.floor-(_sp.pride>=70?6:0)+(_mp.cunning>=70?6:0)));"
)
rp(
"    if(e.hp<RET&&ch(Math.min(.9,st.rp*fleeP(H_BY[e.hero],npcParams(e).p)/.6)-npFleeMinus(b,'en'))) return 'run';",
"    const _sp=servantPersona(H_BY[e.hero]), _mp=masterPersona(e);\n"
"    if(e.hp<RET&&_sp.pride>=70){\n"
"      if(_mp.cunning>=70&&e.master&&e.seals>0&&ch(.45)){ npcSeal(e,'물러나라'); e._svGrudge=(e._svGrudge||0)+12; return 'seal'; }\n"
"      if(ch(Math.min(.85,st.rp*fleeP(H_BY[e.hero],npcParams(e).p)/.6*.45)-npFleeMinus(b,'en'))) return 'run';\n"
"      if(e.known&&ch(.4)) log('상대 마스터가 싸움에서 발을 빼려다 서번트의 반발에 부딪혔다.','war');\n"
"      return false;\n"
"    }\n"
"    if(e.hp<RET&&ch(Math.min(.9,st.rp*fleeP(H_BY[e.hero],npcParams(e).p)/.6)-npFleeMinus(b,'en'))) return 'run';"
)

# 10. Cunning Master avoids direct fights + Loyal Servant guards hurt Master + Rel-driven NPC target selection
rp(
"function npcWillRaid(p){ const L=npcLines(p); if(p.hp<L.floor) return false; if(p.hp>=WOUND_HP) return true;",
"function npcWillRaid(p){ const L=npcLines(p), _mp=masterPersona(p); if(_mp.cunning>=70&&p.hp<85&&!p.scoutEdge&&!(p.provoked>0)) return false; if(p.hp<L.floor) return false; if(p.hp>=WOUND_HP) return true;"
)
rp(
"    for(const p of avail){ if(p.nAct) continue;\n"
"      const [rp,smT,hpT,hideT]=REST_TAC[p.tac]||[.5,40,50,35], low=p.sm<smT||p.hp<hpT;\n"
"      if(p.master&&low&&ch(Math.min(.9,rp*(p.hp<hpT-10?1.3:1)))){ p.nAct=p.hp<hideT?'hide':'rest'; p.rest=true; }\n"
"      else if(p.master&&w.day<=3&&(p.tac==='cunning'||p.tac==='defensive')&&ch(.3)){ p.nAct='intel'; p.scoutEdge=1; const o=avail.filter(x=>x!==p); if(o.length) addKnow(p,pick(o),20); }",
"    for(const p of avail){ if(p.nAct) continue;\n"
"      const [rp,smT,hpT,hideT]=REST_TAC[p.tac]||[.5,40,50,35], low=p.sm<smT||p.hp<hpT, _mp=masterPersona(p), _sp=servantPersona(H_BY[p.hero]);\n"
"      if(p.master&&p.mHurt>0&&_sp.loyalty>=65){ p.nAct='hide'; p.rest=true; }\n"
"      else if(p.master&&low&&ch(Math.min(.92,rp*(_mp.cunning>=70?1.15:1)*(p.hp<hpT-10?1.3:1)))){ p.nAct=p.hp<hideT||_mp.cunning>=70?'hide':'rest'; p.rest=true; }\n"
"      else if(p.master&&((w.day<=3&&(p.tac==='cunning'||p.tac==='defensive')&&ch(.3))||(_mp.cunning>=70&&w.day<=7&&ch(.42)))){ p.nAct='intel'; p.scoutEdge=1; const o=avail.filter(x=>x!==p); if(o.length) addKnow(p,pick(o),20); }"
)
rp(
"const b=shuffle(avail).find(x=>x!==a&&!done.has(x)&&!(x.ally&&a.ally)&&!ch(Math.min(.5,SV(H_BY[x.hero],'stealth')*.05))&&(x.nAct!=='hide'||ch(.4))); if(!b) continue;",
"const _mpA=masterPersona(a), _cands=avail.filter(x=>x!==a&&!done.has(x)&&!(x.ally&&a.ally)&&!ch(Math.min(.5,SV(H_BY[x.hero],'stealth')*.05))&&(x.nAct!=='hide'||ch(.4)));\n"
"      if(!_cands.length) continue;\n"
"      const b=wpick(_cands,x=>{ const r=relGet('p'+a.i,'p'+x.i); let wt=1+r.grudge*.04+r.rivalry*.025-r.trust*.02-r.respect*.01-(_mpA.cunning>=70?r.fear*.025:r.fear*.01); if(_mpA.cunning>=70){ wt+=(100-x.hp)*.03+(x.mHurt?2:0)-(x.hp>a.hp+15?.6:0); } return Math.max(.08,wt); }); if(!b) continue;"
)
rp(
"    if(r&&r.win&&r.lose&&r.lose.hp<=0&&!r.win.cx&&H_BY[r.win.hero]&&H_BY[r.win.hero].cls==='ego') r.win.hp=clamp(r.win.hp+15);",
"    if(r&&r.win&&r.lose&&!r.win.cx&&!r.lose.cx){ relShift('p'+r.lose.i,'p'+r.win.i,{fear:10,respect:8,rivalry:10,grudge:12}); relShift('p'+r.win.i,'p'+r.lose.i,{respect:6,rivalry:6}); }\n"
"    if(r&&r.win&&r.lose&&r.lose.hp<=0&&!r.win.cx&&H_BY[r.win.hero]&&H_BY[r.win.hero].cls==='ego') r.win.hp=clamp(r.win.hp+15);"
)

# 11. Ruthless Ally Sacrifice & Betrayal System (cxCompRound, threat, allyRaidAsk, allyPick, WAR_EV, allyIntent)
rp(
"if(p.hp<30&&ch(cxTacP(p,2))){ out.push(i); log(`${pN} 조가 더 버티지 못하고 물러났다.`,'war'); }",
"const _mp=masterPersona(p), _bs=p.ally?betrayScore(relGet('p'+p.i,'me'),_mp,{hp:w.hp,seals:w.seals,owe:p.owe,slight:p.slight}):0;\n"
"      if(p.ally&&_mp.ruthless>=65&&p.hp<55&&ch(Math.min(.65,_bs*.5+.12))){ out.push(i); p.ally=false; p.allyGone=true; relShift('p'+p.i,'me',{trust:-30,affection:-20,grudge:20}); log('동맹이 싸움 도중 발을 뺐다. 처음부터 당신을 방패로 삼을 작정이었던 모양이다.','loss'); continue; }\n"
"      if(p.hp<30&&ch(cxTacP(p,2))){ out.push(i); log(`${pN} 조가 더 버티지 못하고 물러났다.`,'war'); }"
)
rp(
"const e=wpick(foes,f=>npcAggr(f)*({hunter:3,reckless:3,proud:2,cunning:2,desperate:2,defensive:1,naive:1}[f.tac]||1)*(f.provoked>0?4:1)*(w.hunted&&['executor','burial'].includes(f.aid)?4:1));",
"const _allyS=w.pairs.find(x=>allyOld(x));\n"
"    if(_allyS&&!w.sacrificed&&masterPersona(_allyS).ruthless>=65){\n"
"      const _bs=betrayScore(relGet('p'+_allyS.i,'me'),masterPersona(_allyS),{seals:w.seals,hp:w.hp,owe:_allyS.owe,slight:_allyS.slight});\n"
"      const _bait=foes.find(x=>x!==_allyS);\n"
"      if(_bait&&ch(_bs*.42)){ w.sacrificed=1; _allyS.ally=false; _allyS.allyGone=true; w.exposure=clamp(w.exposure+expUp(18)); relShift('p'+_allyS.i,'me',{trust:-35,affection:-25,grudge:25}); log('동맹이 등을 돌렸다. 당신의 거처를 다른 조에 팔아넘긴 것이다.','loss'); wrec('mine',`동맹 ${_allyS.mname}${J(_allyS.mname,이)} 거처를 팔아넘겼다`,{p:_allyS.i}); return battle(_bait,{ambushed:true}); }\n"
"    }\n"
"    const e=wpick(foes,f=>{ const _r=relGet('p'+f.i,'me'), _mp=masterPersona(f), _rw=Math.max(.2,1+_r.grudge*.03+_r.rivalry*.02-(_mp.cunning>=70?_r.fear*.025:_r.fear*.01)); return npcAggr(f)*_rw*({hunter:3,reckless:3,proud:2,cunning:2,desperate:2,defensive:1,naive:1}[f.tac]||1)*(f.provoked>0?4:1)*(w.hunted&&['executor','burial'].includes(f.aid)?4:1); });"
)
rp(
"if(!npcWillRaid(e)) return;",
"if(!npcWillRaid(e)) return;\n    if(masterPersona(e).cunning>=70&&!e.scoutEdge&&w.fort>=45&&!(e.provoked>0)&&ch(.4)) return;"
)
rp(
"b.owe=(b.owe||0)+1; b.slight=Math.max(0,(b.slight||0)-1);",
"b.owe=(b.owe||0)+1; b.slight=Math.max(0,(b.slight||0)-1); relShift('p'+b.i,'me',{trust:18,affection:12,respect:10,grudge:-10});"
)
rp(
"if(b.alive&&b.ally){ b.slight=(b.slight||0)+1;",
"if(b.alive&&b.ally){ b.slight=(b.slight||0)+1; relShift('p'+b.i,'me',{trust:-22,affection:-15,grudge:22});"
)
rp(
"b.ally=false; b.allyGone=true; b.cutByMe=true; b.provoked=2;",
"b.ally=false; b.allyGone=true; b.cutByMe=true; b.provoked=2; relShift('p'+b.i,'me',{trust:-35,affection:-25,grudge:35,rivalry:15});"
)
rp(
"const pc=(viaF?-.1:0)+(p.aid==='executor'?-1:p.aid==='democrat'?.2:0)+.3+(p.tac==='naive'||p.tac==='desperate'?.3:0)+(p.tac==='proud'?-.2:0)+S.st.bond/400+(p.hp<50?.15:0)+(p.sym||p.friendly?.2:0)+(CXW()&&CXW().stage>=2?.1:0);",
"const _rp=relGet('p'+p.i,'me'), _mp=masterPersona(p);\n"
"      const pc=(viaF?-.1:0)+(p.aid==='executor'?-1:p.aid==='democrat'?.2:0)+.28+(p.tac==='naive'||p.tac==='desperate'?.28:0)+(_mp.pride>=65?-.15:0)+(_rp.trust-25)*.004+_rp.respect*.003-_rp.grudge*.006+S.st.bond/400+(p.hp<50?.15:0)+(p.sym||p.friendly?.2:0)+(CXW()&&CXW().stage>=2?.1:0);"
)
rp(
"    {w:2,c:()=>hero().sp==='traitor'||(hero().traits.includes('야망')&&W().trust<25),",
"    {w:2,c:()=>hero().sp==='traitor'||((hero().traits.includes('야망')||relGet('me','hero').grudge>=65)&&W().trust<30),"
)
rp(
"    {w:2,c:()=>W().pairs.some(allyOld)&&W().day>=7,f:()=>{const a=W().pairs.find(allyOld);if(ch(Math.max(.03,(a.tac==='cunning'||a.tac==='proud'?.45:.15)+.15*(a.slight||0)-.1*(a.owe||0)))){",
"    {w:2,c:()=>W().pairs.some(allyOld)&&W().day>=7,f:()=>{const a=W().pairs.find(allyOld), _bs=betrayScore(relGet('p'+a.i,'me'),masterPersona(a),{seals:W().seals,hp:W().hp,owe:a.owe,slight:a.slight});if(ch(_bs)){"
)
rp(
"  function allyIntent(a){ let [b,sh,y]=ALLY_B.includes(a.aid)?[.6,.25,.15]:ALLY_Y.includes(a.aid)?[.1,.35,.55]:[.15,.65,.2];\n"
"    if(['hunter','reckless'].includes(a.tac)) b*=1.2; if(S.st.bond>=60) b*=.6; if(a.sym) b*=.5; if(a.slight) b*=1+.5*a.slight; if(a.owe){ b*=Math.max(.3,1-.25*a.owe); y*=1+.2*a.owe; }\n"
"    return wpick(['betray','share','yield'],x=>({betray:b,share:sh,yield:y})[x]); }",
"  function allyIntent(a){ const w=W(), rp=relGet('p'+a.i,'me'), mp=masterPersona(a);\n"
"    let [b,sh,y]=ALLY_B.includes(a.aid)?[.55,.28,.17]:ALLY_Y.includes(a.aid)?[.1,.35,.55]:[.15,.65,.2];\n"
"    const bs=betrayScore(rp,mp,{final:true,seals:w.seals,hp:w.hp,owe:a.owe,slight:a.slight});\n"
"    b=Math.max(.04,b*.5+bs*.65); if(S.st.bond>=60) b*=.7; if(a.sym) b*=.55;\n"
"    sh*=Math.max(.3,1+(rp.trust-30)*.008+(rp.respect-20)*.006-rp.grudge*.008);\n"
"    y*=Math.max(.2,1+rp.affection*.008+rp.fear*.006+(a.owe||0)*.2);\n"
"    return wpick(['betray','share','yield'],x=>({betray:b,share:sh,yield:y})[x]); }"
)

# 12. Sim exports
rp(
"duelStart:c=>duelStart(c||{}), duelView:()=>S?duelView():null,",
"duelStart:c=>duelStart(c||{}), duelView:()=>S?duelView():null, personaOf:who=>S?personaOf(who):null, relMatrix:(a,b)=>S&&S.war?relGet(a,b):null, betrayRisk:p=>S&&S.war&&p?betrayScore(relGet('p'+p.i,'me'),masterPersona(p),{seals:S.war.seals,hp:S.war.hp,owe:p.owe,slight:p.slight}):0,"
)

# 13. CSS for Personality Tags & 6-Axis Relationship Grid
REL_CSS = (
    ".ps-tags{display:flex;flex-wrap:wrap;gap:5px;margin:6px 0}"
    ".ps-tag{font-size:11px;padding:1px 8px;border-radius:999px;border:1px solid rgba(201,164,92,.45);color:var(--gold2);background:rgba(201,164,92,.08)}"
    ".ps-tag.loyal{border-color:rgba(111,191,138,.55);color:#9bd3ac;background:rgba(111,191,138,.09)}"
    ".ps-tag.ruthless,.ps-tag.berserk{border-color:rgba(210,80,90,.55);color:#e6a2a8;background:rgba(210,80,90,.09)}"
    ".ps-tag.cunning{border-color:rgba(140,160,230,.55);color:#b7c9f2;background:rgba(140,160,230,.09)}"
    ".rel6-box{display:grid;grid-template-columns:1fr 1fr;gap:5px 12px;margin:8px 0 4px}"
    "@media (max-width:360px){.rel6-box{grid-template-columns:1fr}}"
    ".rel6-row{display:grid;grid-template-columns:46px minmax(0,1fr) 24px;align-items:center;gap:6px;font-size:11.5px;color:var(--dim)}"
    ".rel6-row .tr{height:5px;border-radius:999px;background:var(--panel2);overflow:hidden}"
    ".rel6-row .tr i{display:block;height:100%;border-radius:999px;background:var(--gold)}"
    ".rel6-row.aff .tr i{background:#d67896}.rel6-row.fear .tr i{background:#8a86c9}.rel6-row.resp .tr i{background:#6eaa8c}.rel6-row.riv .tr i{background:#e0b48a}.rel6-row.grd .tr i{background:#c03a45}"
    ".rel6-row b{font-family:var(--f-mono);font-size:11px;color:var(--text);text-align:right;font-weight:500}"
    ".rel6-risk{display:inline-flex;gap:6px;align-items:center;font-size:11.5px;padding:2px 9px;border-radius:999px;border:1px solid var(--line);color:var(--dim);margin-top:4px}"
    ".rel6-risk.hi{border-color:rgba(210,80,90,.6);color:#e6a2a8}.rel6-risk.mid{border-color:rgba(201,164,92,.6);color:var(--gold2)}.rel6-risk.lo{border-color:rgba(111,191,138,.55);color:#9bd3ac}"
)
rp(".herocard .hname{font-family:var(--f-display);", REL_CSS + ".herocard .hname{font-family:var(--f-display);")

# 14. UI Rendering Helpers & Integration (#heroCard, showInfo('me'), showInfo(pairId))
UI_HELPERS = r"""
const PS_L={prideful:'긍지',loyal:'충의',cunning:'책략',ruthless:'비정',berserk:'광기'};
const REL6_M=[['trust','신뢰',''],['affection','애정','aff'],['fear','두려움','fear'],['respect','경의','resp'],['rivalry','경쟁심','riv'],['grudge','원한','grd']];
function psTagsHtml(p){ if(!p||!p.tags||!p.tags.length) return ''; return `<div class="ps-tags">${p.tags.map(t=>`<span class="ps-tag ${t}">${esc(PS_L[t]||t)}</span>`).join('')}</div>`; }
function rel6Html(r){ if(!r) return ''; return `<div class="rel6-box">${REL6_M.map(([k,l,c])=>`<div class="rel6-row ${c}"><span>${esc(l)}</span><span class="tr"><i style="width:${Math.round(r[k]||0)}%"></i></span><b>${Math.round(r[k]||0)}</b></div>`).join('')}</div>`; }
function riskHtml(p){ const S=Sim.S; if(!S||!S.war||!p||!p.ally||!(p.intel>=50||S.st.bond>=55)) return ''; const v=Sim.betrayRisk(p), cl=v>=.55?'hi':v>=.3?'mid':'lo', lb=v>=.55?'높음':v>=.3?'주의':'낮음';
  return `<div class="rel6-risk ${cl}"><span>배신 가능성</span> · <b>${lb}</b></div>`; }
"""
rp("function bar(lb,v,cls){", UI_HELPERS + "function bar(lb,v,cls){")

rp(
"      ${heroAffRows(h,w)}",
"      ${heroAffRows(h,w)}\n      ${psTagsHtml((Sim.personaOf('me')||{}).servant)}"
)
rp(
"${relRow(Sim.relView())}${relReq(Sim.relView())}${bar('노출',w.exposure,'mana')}",
"${relRow(Sim.relView())}${relReq(Sim.relView())}${rel6Html(Sim.relMatrix('me','hero'))}${bar('노출',w.exposure,'mana')}"
)
rp(
"<dt>궁합</dt><dd>${fitWord(w.fit)}</dd></dl>",
"<dt>궁합</dt><dd>${fitWord(w.fit)}</dd><dt>서번트 성격</dt><dd>${psTagsHtml((Sim.personaOf('me')||{}).servant)||'—'}</dd><dt>관계</dt><dd>${rel6Html(Sim.relMatrix('me','hero'))}</dd></dl>"
)
rp(
"<dt>정보</dt><dd class=\"mono\">${Math.round(p.intel)}/100</dd></dl>",
"<dt>정보</dt><dd class=\"mono\">${Math.round(p.intel)}/100</dd>"
"${p.known||p.ally||!p.alive?`<dt>마스터 성격</dt><dd>${psTagsHtml((Sim.personaOf(p)||{}).master)||'—'}</dd>`:''}"
"${p.revealed?`<dt>서번트 성격</dt><dd>${psTagsHtml((Sim.personaOf(p)||{}).servant)||'—'}</dd>`:''}"
"${p.ally||p.intel>=40||!p.alive?`<dt>관계</dt><dd>${rel6Html(Sim.relMatrix('p'+p.i,'me'))}${riskHtml(p)}</dd>`:''}"
"</dl>"
)

if miss:
    for x in miss:
        print('못 찾음', x)
    sys.exit(1)

open(P, 'w', encoding='utf-8').write(s)
print('airel1125 적용 끝')

# Update i18n
from ai_rel_lines import D, T
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
            nd = 0
            for row in D:
                if row[0] not in dic:
                    dic[row[0]] = row[idx]
                    nd += 1
            body = txt[:m1.start(1)] + json.dumps(dic, ensure_ascii=False, separators=(',', ':')) + ';\nwindow.' + var + '_T=' + json.dumps(tpl, ensure_ascii=False, separators=(',', ':')) + ';' + txt[m1.end(2)+1:]
            open(fp, 'w', encoding='utf-8').write(body)
            h = hashlib.md5(body.encode('utf-8')).hexdigest()[:8]
            s = re.sub(r'assets/i18n/' + lg + r'\.js\?v=[0-9a-f]+', f'assets/i18n/{lg}.js?v={h}', s)
            print(f'{lg}.js 추가 {nd}, hash {h}')
        for lg, idx in (('zhs', 3), ('zht', 4)):
            fp = os.path.join(i18n_dir, lg + '.js')
            if not os.path.exists(fp): continue
            txt = open(fp, encoding='utf-8').read()
            m = re.search(r'window\.I18N_ZH=(\{.*\});?\s*$', txt, re.S)
            if not m: continue
            obj = json.loads(m.group(1))
            dic = obj.get('d', {})
            nd = 0
            for row in D:
                if row[0] not in dic:
                    dic[row[0]] = row[idx]
                    nd += 1
            obj['d'] = dic
            body = txt[:m.start(1)] + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + ';\n'
            open(fp, 'w', encoding='utf-8').write(body)
            h = hashlib.md5(body.encode('utf-8')).hexdigest()[:8]
            s = re.sub(r"\{zhs:'([0-9a-f]+)',zht:'([0-9a-f]+)'\}", lambda m2: f"{{zhs:'{h if lg=='zhs' else m2.group(1)}',zht:'{h if lg=='zht' else m2.group(2)}'}}", s)
            print(f'{lg}.js 추가 {nd}, hash {h}')
        open(P, 'w', encoding='utf-8').write(s)
