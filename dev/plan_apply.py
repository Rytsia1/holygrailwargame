"""Strategic AI Planner patch script (plan1125).
Usage: python3 plan_apply.py <game.html>
"""
import sys, os, json, re, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'plan1125' in s:
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

# 1. CSS for Strategic AI Plan tags in showInfo
rp(
".rel6-risk.lo{border-color:rgba(111,191,138,.55);color:#9bd3ac}",
".rel6-risk.lo{border-color:rgba(111,191,138,.55);color:#9bd3ac}.plan-pill{display:inline-block;font-size:11.5px;padding:1px 9px;border-radius:999px;border:1px solid rgba(201,164,92,.45);color:var(--gold2);background:rgba(201,164,92,.08)}.plan-pill.short{border-color:rgba(140,160,230,.55);color:#b7c9f2;background:rgba(140,160,230,.09)}"
)

# 2. Sim: Strategic AI Planner core (plan1125)
PLAN_CORE = r"""
  /* ---------- 전략 AI 플래너 (plan1125) ---------- */
  const PLAN_LONG = {
    territory_control: '거점 장악',
    topple_apex: '강적 타도',
    outlast: '생존 관망',
    dominate: '패권 제압',
    coalition: '연대 구축',
  };
  const PLAN_SHORT = {
    preserve_mana: '마력 보존',
    secure_territory: '거점 확보',
    gather_intel: '첩보 수집',
    find_ally: '동맹 모색',
    hunt_weak: '약자 사냥',
    strike_apex: '강적 기습',
  };

  function evalThreat(obs, cand){
    const w = W(); if(!w || !obs) return 0;
    if(cand === 'me'){
      if(!w.heroAlive) return 0;
      const known = Math.min(100, (w.exposure || 0) + (obs.known ? 25 : 0) + (obs.knowMe || 0));
      const estPw = known >= 40 ? myPower() : 58 + (w.kills || 0) * 8;
      return estPw + (w.kills || 0) * 10 + (w.workshop ? 8 : 0) + (w.fort >= 50 ? 6 : 0) + (relGet('p'+obs.i, 'me').fear || 0) * 0.25;
    }
    if(!cand || !cand.alive || cand.cx) return 0;
    const kn = npcKnow(obs, cand);
    const estPw = kn >= 35 ? npcPower(cand, false, 1) : (cand.pw || 55) + 10;
    const fort = (cand.plan && cand.plan.fort) || 0;
    return estPw + (cand.kills || 0) * 10 + (cand.workshop ? 8 : 0) + fort * 0.12 + (relGet('p'+obs.i, 'p'+cand.i).fear || 0) * 0.25;
  }

  function identifyApex(obs){
    const w = W(); if(!w || !obs) return { apexId:null, apexScore:0, myScore:0, weakId:null, weakVuln:0 };
    const myScore = npcPower(obs, false, 1) + (obs.kills || 0) * 10 + (obs.workshop ? 8 : 0);
    const foes = contracted().filter(q => q !== obs && q.alive && !q.cx && q.i !== obs.npcAlly);
    const cands = foes.map(q => ({ id:'p'+q.i, p:q, isMe:false }));
    if(w.heroAlive && !obs.ally) cands.push({ id:'me', p:null, isMe:true });

    let apexId = null, apexScore = -1;
    let weakId = null, weakVuln = -1, weakHp = 100, weakMHurt = 0, weakSm = 100;
    for(const c of cands){
      const sc = evalThreat(obs, c.isMe ? 'me' : c.p);
      if(sc > apexScore){ apexScore = sc; apexId = c.id; }
      const hp = c.isMe ? w.hp : c.p.hp;
      const sm = c.isMe ? (w.sm ?? 100) : npcSmOf(c.p);
      const mh = c.isMe ? 0 : (c.p.mHurt || 0);
      const se = c.isMe ? (w.seals ?? 3) : (c.p.seals ?? 3);
      const vuln = (100 - hp) + (mh > 0 ? 28 : 0) + (sm < 30 ? 20 : 0) + (se === 0 ? 12 : 0) - sc * 0.15;
      if(vuln > weakVuln){
        weakVuln = vuln; weakId = c.id; weakHp = hp; weakMHurt = mh; weakSm = sm;
      }
    }
    const weakIsVuln = !!(weakId && (weakHp < 65 || weakMHurt > 0 || weakSm < 30));
    return { apexId, apexScore: Math.max(0, apexScore), myScore, weakId, weakVuln, weakHp, weakMHurt, weakSm, weakIsVuln };
  }

  function pickLongGoal(p, idf, mp, sp){
    const eh = H_BY[p.hero];
    const mage = isMageH(eh) || p.cls === 'caster';
    const cur = p.plan && p.plan.longGoal;
    const sc = {
      territory_control: (mage ? 42 : 8) + (p.tac === 'defensive' ? 28 : 0) + (!p.workshop && mage ? 15 : 0) + (cur === 'territory_control' ? 22 : 0),
      topple_apex: (idf.apexScore > idf.myScore + 8 ? 34 : 5) + (mp.cunning >= 65 ? 20 : 0) + (p.tac === 'hunter' || p.tac === 'cunning' ? 18 : 0) + (cur === 'topple_apex' ? 22 : 0),
      outlast: (mp.cunning >= 70 ? 26 : 6) + (idf.myScore < idf.apexScore - 12 ? 22 : 0) + (p.hp < 60 ? 18 : 0) + (p.tac === 'cunning' || p.tac === 'defensive' ? 14 : 0) + (cur === 'outlast' ? 22 : 0),
      dominate: (sp.pride >= 70 ? 26 : 6) + (mp.madness >= 65 ? 22 : 0) + (p.tac === 'reckless' ? 24 : 0) + (idf.myScore >= idf.apexScore - 2 && p.hp >= 65 ? 24 : 0) + (cur === 'dominate' ? 22 : 0),
      coalition: (p.npcAlly != null || p.ally ? 45 : 0) + (idf.apexScore > idf.myScore + 6 ? 26 : 4) + (mp.loyalty >= 60 ? 18 : 0) + (p.tac === 'naive' || p.tac === 'desperate' ? 18 : 0) - (sp.pride >= 80 ? 20 : 0) + (cur === 'coalition' ? 20 : 0),
    };
    let best = 'outlast', bestV = -1e9;
    for(const k of Object.keys(sc)){
      if(sc[k] > bestV){ bestV = sc[k]; best = k; }
    }
    return best;
  }

  function planFaction(p){
    const w = W(); if(!w || !p || !p.alive || p.cx) return null;
    const eh = H_BY[p.hero];
    if(!p.plan){
      p.plan = {
        fort: (p.cls === 'caster' || ['lord', 'elder', 'collector'].includes(p.aid)) ? 22 : 12,
        manaReserve: 30,
        longGoal: null,
        shortGoal: 'gather_intel',
        apexId: null,
        weakId: null,
        targetId: null,
        scores: {},
        updatedDay: -1,
      };
    }
    const mp = masterPersona(p), sp = servantPersona(eh);
    const manaReserve = clamp(25 + (mp.cunning >= 65 ? 15 : 0) + (p.tac === 'defensive' ? 12 : 0) - (p.tac === 'reckless' ? 10 : 0), 15, 55);
    const sm = npcSmOf(p);
    const fort = clamp(p.plan.fort || 12, 0, 80);
    const idf = identifyApex(p);
    const longGoal = pickLongGoal(p, idf, mp, sp);

    let apexIntel = 0;
    if(idf.apexId === 'me'){
      apexIntel = Math.min(100, (w.exposure || 0) + (p.known ? 25 : 0) + (p.knowMe || 0));
    } else if(idf.apexId){
      const ap = pairBy(Number(idf.apexId.slice(1)));
      if(ap) apexIntel = npcKnow(p, ap);
    }

    const allyCands = (!p.ally && p.npcAlly == null && p.master && !p.bxNun && p.aid !== 'executor' && p.aid !== 'burial')
      ? contracted().filter(q => q !== p && q.alive && !q.bxNun && !q.cx && !q.ally && q.npcAlly == null && ('p'+q.i) !== idf.apexId && relGet('p'+p.i, 'p'+q.i).grudge < 25)
      : [];
    const canOfferMe = !p.ally && p.npcAlly == null && p.master && !p.bxNun && p.known && !allyBlock() && w.heroAlive && idf.apexId !== 'me' && relGet('p'+p.i, 'me').grudge < 25;
    const canAlly = allyCands.length > 0 || canOfferMe;

    const mage = isMageH(eh) || p.cls === 'caster';
    const scores = {
      preserve_mana:
        (sm < manaReserve ? (sm < 20 ? 78 : 62) : sm < manaReserve + 15 ? 24 : 4)
        + (p.hp < 55 ? 32 : p.hp < 75 ? 12 : 0)
        + ((p.mHurt || 0) > 0 ? 18 : 0)
        + (mp.cunning >= 65 ? 8 : 0)
        + (longGoal === 'outlast' ? 10 : 0)
        - (p.tac === 'reckless' ? 16 : 0),
      secure_territory:
        (fort < 35 ? 30 : fort < 55 ? 16 : 2)
        + (!p.workshop && mage ? 34 : 0)
        + (w.day >= 7 && w.day <= 9 && !w.altarPreNpc && !w.altarPre && mage ? 26 : 0)
        + (longGoal === 'territory_control' ? 18 : 0)
        + (p.tac === 'defensive' ? 12 : 0)
        - (w.day >= 11 ? 20 : 0),
      gather_intel:
        (idf.apexId ? (apexIntel < 35 ? 36 : apexIntel < 55 ? 20 : 4) : 10)
        + (!p.scoutEdge ? 14 : -16)
        + (mp.cunning >= 65 && w.day <= 7 ? 14 : 0)
        + (p.cls === 'rider' || p.cls === 'shadow' ? 8 : 0)
        + (longGoal === 'topple_apex' && apexIntel < 50 ? 10 : 0),
      find_ally: canAlly
        ? ((idf.apexScore > idf.myScore + 8 ? 36 : 10)
          + (longGoal === 'coalition' ? 22 : 0)
          + (p.hp < 65 ? 8 : 0)
          + (w.day >= 2 && w.day <= 10 ? 8 : -20)
          - (sp.pride >= 80 ? 18 : 0))
        : -99,
      hunt_weak: (idf.weakId && idf.weakIsVuln)
        ? ((p.hp >= 50 && sm >= 25 ? 42 : 16)
          + (idf.weakHp < 40 ? 18 : 8)
          + (idf.weakMHurt > 0 ? 12 : 0)
          + (mp.ruthless >= 60 || p.tac === 'hunter' || p.tac === 'cunning' ? 14 : 0)
          + (longGoal === 'dominate' || longGoal === 'topple_apex' ? 6 : 0))
        : 0,
      strike_apex: idf.apexId
        ? ((apexIntel >= 45 ? 28 : 6)
          + (p.scoutEdge ? 14 : 0)
          + (p.npcAlly != null || p.ally ? 16 : 0)
          + (p.hp >= 65 && sm >= manaReserve ? 14 : -18)
          + (w.day >= 9 ? 16 : 0)
          + (longGoal === 'topple_apex' || longGoal === 'dominate' ? 12 : 0))
        : 0,
    };

    let shortGoal = 'gather_intel', bestS = -1e9;
    for(const k of Object.keys(scores)){
      if(scores[k] > bestS){ bestS = scores[k]; shortGoal = k; }
    }
    const targetId = shortGoal === 'hunt_weak'
      ? idf.weakId
      : (shortGoal === 'strike_apex' || shortGoal === 'gather_intel')
        ? (idf.apexId || idf.weakId)
        : (idf.apexId || idf.weakId);

    p.plan.fort = fort;
    p.plan.manaReserve = manaReserve;
    p.plan.longGoal = longGoal;
    p.plan.shortGoal = shortGoal;
    p.plan.apexId = idf.apexId;
    p.plan.weakId = idf.weakId;
    p.plan.targetId = targetId;
    p.plan.scores = scores;
    p.plan.updatedDay = w.day || 0;
    return p.plan;
  }

  function planCleanup(){
    const w = W(); if(!w || !w.pairs) return;
    const aliveMasters = contracted().filter(q => !q.cx);
    for(const p of w.pairs){
      if(p.npcAlly == null) continue;
      const al = pairBy(p.npcAlly);
      if(!p.alive || !p.master || p.ally || !al || !al.alive || !al.master || al.ally || aliveMasters.length <= 2){
        if(al && al.npcAlly === p.i) al.npcAlly = null;
        p.npcAlly = null;
      }
    }
  }

  function planAllNpc(){
    const w = W(); if(!w || !w.pairs) return;
    planCleanup();
    for(const p of w.pairs){
      if(p.alive && p.master && !p.cx) planFaction(p);
    }
  }

  function npcOfferAllyAsk(p){
    const w = W(); if(!w || w.ended || !w.heroAlive || !p || !p.alive || !p.master || p.ally || allyBlock()) return;
    w.npcAllyAsk = w.day;
    const pl = p.plan || planFaction(p);
    const ap = pl && pl.apexId && pl.apexId !== 'me' ? pairBy(Number(pl.apexId.slice(1))) : null;
    const apexLbl = ap ? cn(ap) : '최강의 조';
    decide({
      title: '동맹의 밀서',
      body: `${cn(p)} 조의 사신이 비밀리에 찾아왔다. “지금 이대로는 ${apexLbl} 조를 막기 어렵다. 마지막 둘이 남을 때까지 손을 잡지 않겠나.”`,
      war: true,
      choices: [
        {
          t: '받아들인다',
          d: '임시 동맹을 맺고 적을 견제한다',
          auto: (w.pairs.filter(x => x.alive && x.master).length >= 3),
          f: () => {
            p.ally = true; p.allyDay = w.day; p.npcAlly = null; S.flags.allyName = p.mname;
            allyConfide(p);
            relShift('p'+p.i, 'me', { trust: 16, respect: 10, grudge: -8 });
            wrec('ally', `${cn(p)} 조 ${p.mname}${J(p.mname,과)} 동맹`, { p: p.i });
            const _af = recFact('ally_form', { actor:'p'+p.i, target:'me', who:{a:pairSnap(p), b:pairSnap('me')}, rel:relGet('p'+p.i,'me'), persona:masterPersona(p) });
            if(p.fought){
              const _df = lastFactOf('duel_clash', x => x.actor==='p'+p.i || x.target==='p'+p.i);
              recFact('enemy_coop', { actor:'p'+p.i, target:'me', who:{a:pairSnap(p), b:pairSnap('me')}, causeId:_df?_df.id:(_af&&_af.id), meta:{kind:'truce_ally'}, beat:true });
            }
            log(`${p.mname}${J(p.mname,과)} 동맹을 맺었습니다. 마지막 둘이 남을 때까지 등을 맡기기로 했다.`, 'war');
            return '비밀리에 동맹의 표식을 나누어 가졌다.';
          }
        },
        {
          t: '거절한다',
          d: '홀로 싸우겠다며 사신을 돌려보낸다',
          f: () => {
            relShift('p'+p.i, 'me', { respect: -4 });
            return `${p.mname}의 사신은 조용히 고개를 끄덕이고 어둠 속으로 사라졌다.`;
          }
        }
      ]
    });
  }
"""
rp(
"  const W=()=>S.war;",
PLAN_CORE + "\n  const W=()=>S.war;"
)

# 3. Init planner in enterWar & dayStart
rp(
"    ensureRels();\n    S.war.queue.push(()=>firstMeeting());",
"    ensureRels();\n    planAllNpc();\n    S.war.queue.push(()=>firstMeeting());"
)
rp(
"    if(w.day===14) log('마지막 날. 오늘 밤 끝나지 않으면 성배는 남은 이들을 한자리로 불러 모은다.','war');",
"    if(w.day===14) log('마지막 날. 오늘 밤 끝나지 않으면 성배는 남은 이들을 한자리로 불러 모은다.','war');\n    planAllNpc();"
)

# 4. Territory defense (p.plan.fort) in npcPower, infilD, npcGuard, npcDuel
rp(
"    if(vsMe) v+=W().exposure*.12+(p.mark==='me'?8:0);",
"    if(!att&&p.plan&&p.plan.fort) v+=Math.round(p.plan.fort*.08);\n    if(vsMe) v+=W().exposure*.12+(p.mark==='me'?8:0);"
)
rp(
"return (P[1]*2+SV(h,'stealth')*1.5+P[4]*1.5+(e.intel||0)*.12+8)-(10+(est?6:asnFoe(e,'night'))+(e.cls==='caster'?8:0)+(e.workshop?6:0)-(e.hp<40?4:0)+asnAlert(e)*5);",
"return (P[1]*2+SV(h,'stealth')*1.5+P[4]*1.5+(e.intel||0)*.12+8)-(10+(est?6:asnFoe(e,'night'))+(e.cls==='caster'?8:0)+(e.workshop?6:0)+((e.plan&&e.plan.fort)?Math.round(e.plan.fort*.1):0)-(e.hp<40?4:0)+asnAlert(e)*5);"
)
rp(
"    if(home) o.push({k:'home',p:pRoll(17+(t.cls==='caster'?25:0)+(t.workshop?6:0)+asnSk(th,'night',true)*.5,40,T.h+off)});",
"    if(home) o.push({k:'home',p:pRoll(17+(t.cls==='caster'?25:0)+(t.workshop?6:0)+Math.round(((t.plan&&t.plan.fort)||0)*.25)+asnSk(th,'night',true)*.5,40,T.h+off)});"
)
rp(
"+(x.p.altarFort?10:0)",
"+(x.p.altarFort?10:0)+(x===B&&x.p.plan&&x.p.plan.fort?Math.round(x.p.plan.fort*.08):0)"
)

# 5. Preserve mana inside combat (npcNPProb & npcDuel prob)
rp(
"    else if(eh.id==='circe') p=fxGet(b,'en','pig')?0:(rd<=2?.35:.08);\n    else p=0;\n    return p; }",
"    else if(eh.id==='circe') p=fxGet(b,'en','pig')?0:(rd<=2?.35:.08);\n    else p=0;\n    if(e.plan&&(e.plan.shortGoal==='preserve_mana'||npcSmOf(e)<e.plan.manaReserve)&&!fin&&e.hp>=35&&e.plan.apexId!=='me') p*=.25;\n    return p; }"
)
rp(
"      else if(id==='circe') p=get(x.o,'pig')?0:(r<=2?.35:.08);\n      else p=0; return p; };",
"      else if(id==='circe') p=get(x.o,'pig')?0:(r<=2?.35:.08);\n      else p=0;\n      if(x.p.plan&&(x.p.plan.shortGoal==='preserve_mana'||npcSmOf(x.p)<x.p.plan.manaReserve)&&!final&&x.p.hp>=35&&x.p.plan.apexId!=='p'+x.o.p.i) p*=.25;\n      return p; };"
)

# 6. NPC-to-NPC alliance immunity + planner alignment in npcClassNight
rp(
"const others=a=>cs.filter(x=>x!==a&&x.alive&&x.master&&!(x.ally&&a.ally)&&!x.bxNun);",
"const others=a=>cs.filter(x=>x!==a&&x.alive&&x.master&&!(x.ally&&a.ally)&&!(a.npcAlly&&a.npcAlly===x.i)&&!x.bxNun);"
)
rp(
"      if(!a.alive||!a.master||a.halt>0) continue; const ah=H_BY[a.hero], A=V(a), ts=others(a); if(!ts.length) continue;",
"      if(!a.alive||!a.master||a.halt>0||(a.plan&&a.plan.shortGoal==='preserve_mana')) continue; const ah=H_BY[a.hero], A=V(a), ts=others(a); if(!ts.length) continue;"
)
rp(
"      if(a.cls==='caster'&&!a.workshop&&ch(0.6)){ // 공방을 짓는다\n        a.wsProg=Math.min(100,(a.wsProg||0)+ri(12,24)+Math.round(A[3]*2)); if(a.wsProg>=100){ a.workshop=true; if(a.known&&ch(.6)) log(`${pName(a)} 조의 거처 쪽에서 마력의 맥박이 느껴진다. 공방이 완성된 것 같다.`); }\n        a.nAct='class'; continue; }",
"      if(a.cls==='caster'&&!a.workshop&&ch(0.6)){ // 공방을 짓는다\n        a.wsProg=Math.min(100,(a.wsProg||0)+ri(12,24)+Math.round(A[3]*2)); if(a.wsProg>=100){ a.workshop=true; if(a.known&&ch(.6)) log(`${pName(a)} 조의 거처 쪽에서 마력의 맥박이 느껴진다. 공방이 완성된 것 같다.`); }\n        if(a.plan&&a.plan.shortGoal==='secure_territory'){ a.plan.fort=clamp((a.plan.fort||12)+ri(12,18),0,80); a.rest=true; }\n        a.nAct='class'; continue; }"
)

# 7. Strategic Planner execution + NPC pacts + target selection in npcNight & threat
OLD_NIGHT_HEAD = "    const w=W(); if(w.ended) return; w.nf=[]; for(const p of w.pairs){ p.nAct=null; p.rest=false; }"
NEW_NIGHT_HEAD = "    const w=W(); if(w.ended) return; w.nf=[]; for(const p of w.pairs){ p.nAct=null; p.rest=false; }\n    planAllNpc();"
rp(OLD_NIGHT_HEAD, NEW_NIGHT_HEAD)

OLD_NIGHT_DECIDE = """    for(const p of avail){ if(p.nAct) continue;
      const [rp,smT,hpT,hideT]=REST_TAC[p.tac]||[.5,40,50,35], low=p.sm<smT||p.hp<hpT, _mp=masterPersona(p), _sp=servantPersona(H_BY[p.hero]);
      if(p.master&&p.mHurt>0&&_sp.loyalty>=65){ p.nAct='hide'; p.rest=true; }
      else if(p.master&&low&&ch(Math.min(.92,rp*(_mp.cunning>=70?1.15:1)*(p.hp<hpT-10?1.3:1)))){ p.nAct=p.hp<hideT||_mp.cunning>=70?'hide':'rest'; p.rest=true; }
      else if(p.master&&((w.day<=3&&(p.tac==='cunning'||p.tac==='defensive')&&ch(.3))||(_mp.cunning>=70&&w.day<=7&&ch(.42)))){ p.nAct='intel'; p.scoutEdge=1; const o=avail.filter(x=>x!==p); if(o.length) addKnow(p,pick(o),20); } // 정보를 모은다: 다음 싸움 첫 합 +6, 다른 조 하나의 정보 +20
      else p.nAct='out'; }
    const act=shuffle(avail.filter(p=>p.nAct==='out'));
    const pressure=(.16+w.day*.03)*(w.crisis&&!w.crisis.done?[1,1,.8,.5][w.crisis.stage]:1); // 검은 성배가 넘치기 시작하면 조끼리의 싸움이 줄어든다
    const done=new Set(); let reported=0; bxNunHunt(avail,done);
    for(const a of act){
      if(done.has(a)||!ch(Math.min(.95,pressure*npcAggr(a)))||!npcWillRaid(a)) continue;
      const _mpA=masterPersona(a), _cands=avail.filter(x=>x!==a&&!done.has(x)&&!(x.ally&&a.ally)&&!ch(Math.min(.5,SV(H_BY[x.hero],'stealth')*.05))&&(x.nAct!=='hide'||ch(.4)));
      if(!_cands.length) continue;
      const b=wpick(_cands,x=>{ const r=relGet('p'+a.i,'p'+x.i); let wt=1+r.grudge*.04+r.rivalry*.025-r.trust*.02-r.respect*.01-(_mpA.cunning>=70?r.fear*.025:r.fear*.01); if(_mpA.cunning>=70){ wt+=(100-x.hp)*.03+(x.mHurt?2:0)-(x.hp>a.hp+15?.6:0); } return Math.max(.08,wt); }); if(!b) continue; // 쉬는 조도 습격받을 수 있다. 숨죽인 조는 잘 들키지 않는다
      done.add(a);done.add(b);"""

NEW_NIGHT_DECIDE = """    const done=new Set(); let reported=0;
    // 전략 AI 플래너: 단기 목표 실행 및 NPC 동맹·배신 처리
    for(const p of avail){
      if(done.has(p)) continue;
      const _mp=masterPersona(p), _sp=servantPersona(H_BY[p.hero]);
      // 1) 기존 NPC 동맹 배신 체크 (비정한 마스터가 약해진 파트너를 배신)
      if(p.npcAlly!=null && _mp.ruthless>=65){
        const q=pairBy(p.npcAlly);
        if(q && q.alive && q.master && q.hp<40 && !done.has(q) && ch(Math.min(.55, betrayScore(relGet('p'+p.i,'p'+q.i), _mp, {hp:q.hp,seals:q.seals})*.45))){
          p.npcAlly=null; q.npcAlly=null;
          relShift('p'+q.i,'p'+p.i,{trust:-35,grudge:35});
          const _pr=lastFactOf(['ally_form','enemy_coop'],x=>(x.actor==='p'+p.i&&x.target==='p'+q.i)||(x.actor==='p'+q.i&&x.target==='p'+p.i));
          recFact('ally_betray',{actor:'p'+p.i,target:'p'+q.i,who:{a:pairSnap(p),b:pairSnap(q)},rel:relGet('p'+q.i,'p'+p.i),persona:_mp,causeId:_pr&&_pr.id,meta:{kind:'npc_betray'},beat:!!(p.known||q.known)});
          done.add(p); done.add(q);
          const {win,lose}=npcFight(p,q,false,true); w.nf.push([p.i,q.i]);
          if(lose.hp<=0){ const lh=H_BY[lose.hero]; if(lh.sp==='revive'&&!lose.usedRevive){lose.usedRevive=true;lose.hp=45;} else { lose.alive=false; lose.revealed=true; pairOut(lose,'동맹의 배신으로 쓰러졌다',win); log(`감독관의 통지: ${cn(lose)} 조 탈락.`,'notice'); } }
          continue;
        }
      }
      if(p.nAct) continue;
      if(p.master && p.mHurt>0 && _sp.loyalty>=65){ p.nAct='hide'; p.rest=true; continue; }
      const pl = p.plan || planFaction(p), sg = pl ? pl.shortGoal : 'out';
      if(sg === 'preserve_mana'){
        p.nAct = (p.hp < 60 || _mp.cunning >= 70) ? 'hide' : 'rest';
        p.rest = true;
        continue;
      }
      if(sg === 'secure_territory'){
        pl.fort = clamp((pl.fort || 12) + ri(12, 18), 0, 80);
        if(!p.workshop && isMageH(H_BY[p.hero])){
          p.wsProg = Math.min(100, (p.wsProg || 0) + ri(22, 34));
          if(p.wsProg >= 100){ p.workshop = true; if(p.known && ch(.6)) log(`${pName(p)} 조의 거처가 한층 더 견고한 마술 공방으로 거듭났다.`); }
        }
        if(w.day >= 7 && w.day <= 9 && !w.altarPreNpc && !w.altarPre && isMageH(H_BY[p.hero]) && ch(.35)){
          p.altarPre = true; w.altarPreNpc = true;
        }
        p.nAct = 'hide'; p.rest = true;
        continue;
      }
      if(sg === 'gather_intel'){
        p.nAct = 'intel'; p.scoutEdge = 1;
        const tid = pl.targetId;
        if(tid === 'me' && w.heroAlive){ p.knowMe = Math.min(100, (p.knowMe || 0) + 25); w.exposure = clamp(w.exposure + expUp(4)); }
        else if(tid && tid.startsWith('p')){ const tgt = pairBy(Number(tid.slice(1))); if(tgt && tgt.alive) addKnow(p, tgt, 25); }
        else { const o = avail.filter(x => x !== p && x.i !== p.npcAlly); if(o.length) addKnow(p, pick(o), 25); }
        continue;
      }
      if(sg === 'find_ally'){
        const cand = (!p.ally && p.npcAlly == null && !p.bxNun && p.aid !== 'executor' && p.aid !== 'burial')
          ? avail.find(q => q !== p && q.alive && q.master && !q.bxNun && !q.ally && q.npcAlly == null && ('p'+q.i) !== pl.apexId && q.aid !== 'executor' && q.aid !== 'burial' && relGet('p'+p.i,'p'+q.i).grudge < 25)
          : null;
        if(cand){
          p.npcAlly = cand.i; cand.npcAlly = p.i;
          const r0 = relGet('p'+p.i, 'p'+cand.i);
          const du = lastFactOf('duel_clash', x => (x.actor==='p'+p.i && x.target==='p'+cand.i) || (x.actor==='p'+cand.i && x.target==='p'+p.i));
          relShift('p'+p.i, 'p'+cand.i, { trust:15, respect:8, grudge:-6 });
          relShift('p'+cand.i, 'p'+p.i, { trust:15, respect:8, grudge:-6 });
          if(pl.apexId && pl.apexId.startsWith('p')){ const ap = pairBy(Number(pl.apexId.slice(1))); if(ap){ addKnow(p, ap, 20); addKnow(cand, ap, 20); } }
          else if(pl.apexId === 'me'){ p.knowMe = (p.knowMe || 0) + 15; cand.knowMe = (cand.knowMe || 0) + 15; }
          if(du || r0.rivalry >= 15 || r0.grudge >= 10){
            recFact('enemy_coop', { actor:'p'+p.i, target:'p'+cand.i, who:{a:pairSnap(p), b:pairSnap(cand)}, causeId:du?du.id:null, meta:{kind:'npc_pact'}, beat:!!(p.known||cand.known) });
          } else {
            recFact('ally_form', { actor:'p'+p.i, target:'p'+cand.i, who:{a:pairSnap(p), b:pairSnap(cand)}, rel:relGet('p'+p.i,'p'+cand.i), persona:_mp });
          }
          p.nAct = 'intel'; continue;
        }
        if(p.known && !p.ally && p.npcAlly == null && !allyBlock() && !w.npcAllyAsk && w.day >= 2 && w.heroAlive && pl.apexId !== 'me' && relGet('p'+p.i,'me').grudge < 25 && ch(.45)){
          w.npcAllyAsk = w.day;
          w.queue.push(() => npcOfferAllyAsk(p));
          p.nAct = 'intel'; continue;
        }
      }
      if(sg === 'hunt_weak' || sg === 'strike_apex'){ p.nAct = 'out'; continue; }
      const [rp,smT,hpT,hideT]=REST_TAC[p.tac]||[.5,40,50,35], low=p.sm<smT||p.hp<hpT;
      if(p.master&&low&&ch(Math.min(.92,rp*(_mp.cunning>=70?1.15:1)*(p.hp<hpT-10?1.3:1)))){ p.nAct=p.hp<hideT||_mp.cunning>=70?'hide':'rest'; p.rest=true; }
      else p.nAct='out';
    }
    const act=shuffle(avail.filter(p=>p.nAct==='out'));
    const pressure=(.16+w.day*.03)*(w.crisis&&!w.crisis.done?[1,1,.8,.5][w.crisis.stage]:1); // 검은 성배가 넘치기 시작하면 조끼리의 싸움이 줄어든다
    bxNunHunt(avail,done);
    for(const a of act){
      if(done.has(a)||!ch(Math.min(.95,pressure*npcAggr(a)))||!npcWillRaid(a)) continue;
      const _mpA=masterPersona(a), _cands=avail.filter(x=>x!==a&&!done.has(x)&&!(x.ally&&a.ally)&&!(a.npcAlly&&a.npcAlly===x.i)&&!ch(Math.min(.5,SV(H_BY[x.hero],'stealth')*.05))&&(x.nAct!=='hide'||ch(.4)));
      if(!_cands.length) continue;
      const b=wpick(_cands,x=>{ const r=relGet('p'+a.i,'p'+x.i); let wt=1+r.grudge*.04+r.rivalry*.025-r.trust*.02-r.respect*.01-(_mpA.cunning>=70?r.fear*.025:r.fear*.01); if(_mpA.cunning>=70){ wt+=(100-x.hp)*.03+(x.mHurt?2:0)-(x.hp>a.hp+15?.6:0); } if(a.plan&&a.plan.targetId==='p'+x.i) wt*=3.5; return Math.max(.08,wt); }); if(!b) continue; // 쉬는 조도 습격받을 수 있다. 숨죽인 조는 잘 들키지 않는다
      done.add(a);done.add(b);"""

rp(OLD_NIGHT_DECIDE, NEW_NIGHT_DECIDE)

# Coordinated follow-up strike by NPC ally after strike_apex fight if target survived
OLD_NIGHT_AFTER = """      } else if(reported<2){ log(`${pick([`${pick(CX().sites)} 쪽 하늘이 붉게 번쩍였다.`,`${pick(CX().sites)} 쪽에서 굉음이 들렸다.`,'고층 빌딩 꼭대기에서 불꽃이 튀었다.','어딘가에서 성당 종이 한밤에 울렸다.'])}${seen&&(a.known||b.known)?` ${pName(a)} 조와 ${pName(b)} 조였다.`:''}`); reported++; }
    }"""

NEW_NIGHT_AFTER = """      } else if(reported<2){ log(`${pick([`${pick(CX().sites)} 쪽 하늘이 붉게 번쩍였다.`,`${pick(CX().sites)} 쪽에서 굉음이 들렸다.`,'고층 빌딩 꼭대기에서 불꽃이 튀었다.','어딘가에서 성당 종이 한밤에 울렸다.'])}${seen&&(a.known||b.known)?` ${pName(a)} 조와 ${pName(b)} 조였다.`:''}`); reported++; }
      if(b.alive && a.alive && a.npcAlly!=null && a.plan && a.plan.shortGoal==='strike_apex' && a.plan.targetId==='p'+b.i){
        const al=pairBy(a.npcAlly);
        if(al && al.alive && al.master && !done.has(al) && !(al.halt>0) && !w.nf.some(f=>f.includes(al.i))){
          done.add(al);
          const {win:w2, lose:l2}=npcFight(al,b,false,true); w.nf.push([al.i,b.i]);
          if(l2.hp<=0){ const lh2=H_BY[l2.hero]; if(lh2.sp==='revive'&&!l2.usedRevive){l2.usedRevive=true;l2.hp=45;} else { l2.alive=false; l2.revealed=true; pairOut(l2,'다른 조들의 협공에 쓰러졌다',seen?w2:null); log(`감독관의 통지: ${cn(l2)} 조 탈락.`,'notice'); if(l2.ally){log(`동맹 ${l2.mname}의 조가 무너졌다.`,'loss');S.flags.allyName=l2.mname;} reported++; } }
        }
      }
    }"""
rp(OLD_NIGHT_AFTER, NEW_NIGHT_AFTER)

# Target bias in threat() against player ('me')
rp(
"const e=wpick(foes,f=>{ const _r=relGet('p'+f.i,'me'), _mp=masterPersona(f), _rw=Math.max(.2,1+_r.grudge*.03+_r.rivalry*.02-(_mp.cunning>=70?_r.fear*.025:_r.fear*.01)); return npcAggr(f)*_rw*({hunter:3,reckless:3,proud:2,cunning:2,desperate:2,defensive:1,naive:1}[f.tac]||1)*(f.provoked>0?4:1)*(w.hunted&&['executor','burial'].includes(f.aid)?4:1); });",
"const e=wpick(foes,f=>{ const _r=relGet('p'+f.i,'me'), _mp=masterPersona(f), _rw=Math.max(.2,1+_r.grudge*.03+_r.rivalry*.02-(_mp.cunning>=70?_r.fear*.025:_r.fear*.01)), _pt=(f.plan&&(f.plan.shortGoal==='hunt_weak'||f.plan.shortGoal==='strike_apex')&&f.plan.targetId==='me')?3.5:1; return npcAggr(f)*_rw*_pt*({hunter:3,reckless:3,proud:2,cunning:2,desperate:2,defensive:1,naive:1}[f.tac]||1)*(f.provoked>0?4:1)*(w.hunted&&['executor','burial'].includes(f.aid)?4:1); });"
)

# 8. Export on Sim
rp(
"narrBeat:(f,lg,trFn)=>narrBeat(f,lg,trFn),",
"narrBeat:(f,lg,trFn)=>narrBeat(f,lg,trFn), planOf:p=>S&&S.war&&p?(p.plan||planFaction(p)):null, planAll:()=>S&&S.war?planAllNpc():null, planMeta:()=>({LONG:PLAN_LONG,SHORT:PLAN_SHORT}),"
)

# 9. UI helper planHtml & showInfo integration
rp(
"function riskHtml(p){",
"""function planHtml(p){ const S=Sim.S, pl=Sim.planOf(p); if(!S||!S.war||!pl) return '';
  const M=Sim.planMeta(), lg=M.LONG[pl.longGoal]||pl.longGoal, sg=M.SHORT[pl.shortGoal]||pl.shortGoal;
  let tgt='';
  if(pl.apexId==='me') tgt='<span>당신</span>';
  else if(pl.apexId&&pl.apexId.startsWith('p')){
    const ap=S.war.pairs.find(x=>'p'+x.i===pl.apexId);
    if(ap) tgt=ap.revealed?`${esc(Sim.H_BY[ap.hero].name)} (${esc(Sim.CLS[ap.cls].n)})`:`${esc(Sim.cn(ap))} 조`;
  }
  return `<dt>장기 목표</dt><dd><span class="plan-pill">${esc(lg)}</span></dd><dt>현재 전략</dt><dd><span class="plan-pill short">${esc(sg)}</span></dd>${tgt?`<dt>경계 대상</dt><dd>${tgt}</dd>`:''}<dt>거점 방비</dt><dd class="mono">${Math.round(pl.fort||0)}</dd>`;
}
function riskHtml(p){"""
)
rp(
"${p.ally||p.intel>=40||!p.alive?`<dt>관계</dt><dd>${rel6Html(Sim.relMatrix('p'+p.i,'me'))}${riskHtml(p)}</dd>`:''}</dl>",
"${p.ally||p.intel>=40||!p.alive?`<dt>관계</dt><dd>${rel6Html(Sim.relMatrix('p'+p.i,'me'))}${riskHtml(p)}</dd>`:''}${p.ally||p.intel>=60||!p.alive?planHtml(p):''}</dl>"
)

if miss:
    for x in miss:
        print('못 찾음', x)
    sys.exit(1)

open(P, 'w', encoding='utf-8').write(s)
print('plan1125 적용 끝')

# Update i18n
from plan_lines import D, T
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
