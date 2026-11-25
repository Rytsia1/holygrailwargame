// Strategic AI Planner tests. Usage: node dev/plan_test.js <game.html>
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const src = fs.readFileSync(process.argv[2] || 'public/index.html', 'utf8');
const a = src.indexOf('<script id="sim">') + 17, b = src.indexOf('</script>', a);
let code = src.slice(a, b).replace(
  'return {cn,ACH:',
  'globalThis.__T={planFaction,planAllNpc,evalThreat,identifyApex,npcNight,npcNPProb,npcPower,infilD,npcOfferAllyAsk,npcSmOf,W:()=>S.war};\n  return {cn,ACH:'
);
const ctx = { console }; ctx.globalThis = ctx; ctx.window = ctx;
vm.createContext(ctx);
vm.runInContext(code + ';globalThis.Sim=Sim;', ctx);
const Sim = ctx.Sim, T = ctx.__T;
Sim.setHooks(new Proxy({}, { get: () => () => {} }));

let ok = 0;
function test(name, fn) {
  fn();
  ok++;
  console.log('✓', name);
}

function enterWar(seed = 800, forceHero = 'artoria') {
  ctx.globalThis.__FORCE_HERO = forceHero;
  Sim.newLife({ seed, len: 20 });
  Sim.start();
  let g = 0;
  while (Sim.S && !Sim.S.dead && g++ < 400000 && !(Sim.S.phase === 'war' && Sim.S.war && Sim.S.war.heroAlive)) {
    const S = Sim.S;
    if (S.pending) { Sim.resolve(Sim.autoChoice(S.pending)); continue; }
    Sim.tick(1);
  }
  ctx.globalThis.__FORCE_HERO = null;
  assert.strictEqual(Sim.S.phase, 'war');
  return Sim.S;
}

// 1. enterWar initializes p.plan on all alive contracted NPCs
test('enterWar initializes p.plan for every NPC pair', () => {
  const S = enterWar(801, 'artoria');
  assert.ok(S.war.pairs.length >= 6);
  for (const p of S.war.pairs) {
    assert.ok(p.plan, 'missing p.plan');
    assert.ok(['territory_control', 'topple_apex', 'outlast', 'dominate', 'coalition'].includes(p.plan.longGoal));
    assert.ok(['preserve_mana', 'secure_territory', 'gather_intel', 'find_ally', 'hunt_weak', 'strike_apex'].includes(p.plan.shortGoal));
  }
});

// 2. Identify strongest (apexId) and most vulnerable (weakId)
test('identifyApex accurately finds strongest opponent and injured vulnerable opponent', () => {
  const S = enterWar(802, 'artoria');
  const w = S.war;
  for (const p of w.pairs) { p.hp = 90; p.sm = 80; p.pw = 50; p.kills = 0; p.mHurt = 0; }
  const obs = w.pairs[0];
  const apex = w.pairs[1];
  const weak = w.pairs[2];
  apex.pw = 96; apex.kills = 4; apex.workshop = true;
  weak.hp = 24; weak.mHurt = 2; weak.sm = 15; weak.pw = 35;
  obs.know = { [apex.i]: 80, [weak.i]: 80 };
  const pl = T.planFaction(obs);
  assert.strictEqual(pl.apexId, 'p' + apex.i);
  assert.strictEqual(pl.weakId, 'p' + weak.i);
});

// 3. Preserve Mana goal + night execution + combat NP suppression
test('preserve_mana triggers on low SM, rests/hides at night, and suppresses NP usage', () => {
  const S = enterWar(803, 'artoria');
  const w = S.war; w.day = 4; w.heroAlive = false;
  const p = w.pairs[0];
  p.aid = 'scholar'; p.tac = 'cunning'; p.sm = 12; p.hp = 85; p.workshop = true;
  p.plan.fort = 65;
  const pl = T.planFaction(p);
  assert.strictEqual(pl.shortGoal, 'preserve_mana');

  // Combat NP suppression: preserve_mana reduces npcNPProb to 0.25x
  const e = w.pairs[1];
  e.hero = 'artoria'; e.cls = 'sword'; e.hp = 70; e.tac = 'proud';
  e.plan = { shortGoal: 'strike_apex', manaReserve: 25, apexId: 'me', fort: 20 };
  const baseProb = T.npcNPProb({ e, fx: [], ctx: { final: false }, round: 1 });
  e.plan.shortGoal = 'preserve_mana';
  e.plan.apexId = 'p99';
  const lowProb = T.npcNPProb({ e, fx: [], ctx: { final: false }, round: 1 });
  assert.ok(Math.abs(lowProb - baseProb * 0.25) < 1e-6, `expected ${baseProb * 0.25}, got ${lowProb}`);

  // Night execution puts p into rest or hide
  T.npcNight();
  assert.ok(p.nAct === 'rest' || p.nAct === 'hide', `expected rest/hide, got ${p.nAct}`);
  assert.strictEqual(p.rest, true);
});

// 4. Secure Territory goal + fort/workshop progression + defensive bonuses
test('secure_territory boosts fort/workshop and improves defensive power and anti-infiltration', () => {
  const S = enterWar(804, 'artoria');
  const w = S.war; w.day = 3;
  const p = w.pairs[0];
  p.cls = 'caster'; p.hero = 'medea'; p.aid = 'elder'; p.tac = 'defensive';
  p.workshop = false; p.wsProg = 0; p.sm = 90; p.hp = 95; p.plan.fort = 10;
  w.pairs.slice(1).forEach(q => { q.hp = 95; q.sm = 90; q.mHurt = 0; });

  const pwLow = T.npcPower(p, false, 1, false);
  const infLow = T.infilD(p, false);
  const pl = T.planFaction(p);
  assert.strictEqual(pl.shortGoal, 'secure_territory');

  T.npcNight();
  assert.ok(p.plan.fort >= 22, `expected fort >= 22, got ${p.plan.fort}`);
  assert.ok(p.wsProg > 0 || p.workshop, 'expected workshop progress');

  p.plan.fort = 75;
  const pwHigh = T.npcPower(p, false, 1, false);
  const infHigh = T.infilD(p, false);
  assert.ok(pwHigh > pwLow, 'fort should raise defending npcPower');
  assert.ok(infHigh < infLow, 'fort should lower attacker infilD');
});

// 5. Gather Intelligence goal + scoutEdge & apex knowledge gain
test('gather_intel targets unknown apex and grants scoutEdge + knowledge', () => {
  const S = enterWar(805, 'artoria');
  const w = S.war; w.day = 3;
  w.pairs.forEach(q => { q.hp = 95; q.sm = 95; q.mHurt = 0; q.workshop = true; if (q.plan) q.plan.fort = 65; });
  const p = w.pairs[0], apex = w.pairs[1];
  p.aid = 'detective'; p.tac = 'cunning'; p.cls = 'rider'; p.hero = 'alexander';
  p.scoutEdge = 0; p.know = {};
  apex.pw = 92; apex.kills = 3;
  const pl = T.planFaction(p);
  assert.strictEqual(pl.shortGoal, 'gather_intel');

  T.npcNight();
  assert.strictEqual(p.nAct, 'intel');
  assert.strictEqual(p.scoutEdge, 1);
  assert.ok((p.know[apex.i] || 0) >= 25, 'expected knowledge gain on apex');
});

// 6. Find Allies goal + NPC-to-NPC pact & mutual non-aggression
test('find_ally forms NPC-to-NPC pact against apex and shares intel', () => {
  const S = enterWar(806, 'artoria');
  const w = S.war; w.day = 4;
  w.pairs.forEach(q => { q.hp = 95; q.sm = 95; q.mHurt = 0; q.workshop = true; q.scoutEdge = 1; if (q.plan) q.plan.fort = 70; });
  const p = w.pairs[0], q = w.pairs[1], apex = w.pairs[2];
  p.aid = 'democrat'; p.tac = 'naive'; p.pw = 45; p.hp = 60; p.hero = 'hector';
  q.aid = 'student'; q.tac = 'naive'; q.pw = 46; q.hp = 62; q.hero = 'robin';
  apex.pw = 98; apex.kills = 4;
  p.know = { [apex.i]: 70 };
  const pl = T.planFaction(p);
  assert.strictEqual(pl.shortGoal, 'find_ally');

  T.npcNight();
  assert.strictEqual(p.npcAlly, q.i, 'expected p.npcAlly === q.i');
  assert.strictEqual(q.npcAlly, p.i, 'expected q.npcAlly === p.i');
  assert.ok((q.know[apex.i] || 0) >= 20, 'expected pact to share apex intel');
  assert.ok((w.facts || []).some(f => f.type === 'ally_form' || f.type === 'enemy_coop'), 'expected pact recorded in facts');
});

// 7. Hunt Weak & Strike Apex goals
test('hunt_weak targets vulnerable foe and strike_apex targets well-scouted apex', () => {
  const S = enterWar(807, 'artoria');
  const w = S.war; w.day = 6;
  w.pairs.forEach(q => { q.hp = 90; q.sm = 90; q.mHurt = 0; q.workshop = true; q.scoutEdge = 1; if (q.plan) q.plan.fort = 70; });
  const hunter = w.pairs[0], weak = w.pairs[1], apex = w.pairs[2];
  hunter.aid = 'killer'; hunter.tac = 'hunter'; hunter.hero = 'robin'; hunter.hp = 95; hunter.sm = 90;
  weak.hp = 20; weak.mHurt = 2; weak.sm = 10; weak.pw = 40;
  let pl = T.planFaction(hunter);
  assert.strictEqual(pl.shortGoal, 'hunt_weak');
  assert.strictEqual(pl.targetId, 'p' + weak.i);

  // When weak recovers and hunter has high intel + ally + late war against apex -> strike_apex
  weak.hp = 95; weak.mHurt = 0; weak.sm = 90;
  w.day = 10;
  apex.pw = 95; apex.kills = 3;
  hunter.know = { [apex.i]: 85 };
  hunter.npcAlly = w.pairs[3].i;
  pl = T.planFaction(hunter);
  assert.strictEqual(pl.shortGoal, 'strike_apex');
  assert.strictEqual(pl.targetId, 'p' + apex.i);
});

// 8. Proactive NPC-to-Player alliance offer & persistence via snapshot/load
test('npcOfferAllyAsk accepts alliance and snapshot/load preserves p.plan and p.npcAlly', () => {
  const S = enterWar(808, 'artoria');
  let g = 0;
  while (S.war.resumeAt !== 'day' && g++ < 500) {
    if (S.pending) Sim.resolve(Sim.autoChoice(S.pending));
    else Sim.tick(1);
  }
  assert.strictEqual(S.war.resumeAt, 'day');

  const p = S.war.pairs[0], q = S.war.pairs[1];
  p.npcAlly = q.i; q.npcAlly = p.i;
  p.plan.longGoal = 'territory_control';
  p.plan.fort = 54;

  const snap = Sim.snapshot();
  assert.ok(snap, 'snapshot should exist at dayDecision');
  Sim.load(snap);
  assert.strictEqual(Sim.S.war.pairs[0].npcAlly, q.i);
  assert.strictEqual(Sim.S.war.pairs[0].plan.longGoal, 'territory_control');
  assert.strictEqual(Sim.S.war.pairs[0].plan.fort, 54);

  // Test proactive offer
  const offerer = Sim.S.war.pairs[2];
  offerer.known = true;
  T.npcOfferAllyAsk(offerer);
  assert.ok(Sim.S.pending && Sim.S.pending.title === '동맹의 밀서', 'expected alliance offer prompt');
  Sim.resolve(0); // Accept
  assert.strictEqual(offerer.ally, true);
  assert.ok((Sim.S.war.facts || []).some(f => f.type === 'ally_form' && f.actor === 'p' + offerer.i));
});

// 9. All UI/planner translation keys exist in en/ja/zhs/zht
test('all planner UI translation keys present in en, ja, zhs, zht i18n bundles', () => {
  const keys = ['장기 목표', '현재 전략', '경계 대상', '거점 방비', '거점 장악', '강적 타도', '생존 관망', '패권 제압', '연대 구축', '마력 보존', '거점 확보', '첩보 수집', '동맹 모색', '약자 사냥', '강적 기습', '동맹의 밀서'];
  const enCtx = { window: {} }; vm.runInNewContext(fs.readFileSync('public/assets/i18n/en.js', 'utf8'), enCtx);
  const jaCtx = { window: {} }; vm.runInNewContext(fs.readFileSync('public/assets/i18n/ja.js', 'utf8'), jaCtx);
  const zhsCtx = { window: {} }; vm.runInNewContext(fs.readFileSync('public/assets/i18n/zhs.js', 'utf8'), zhsCtx);
  const zhtCtx = { window: {} }; vm.runInNewContext(fs.readFileSync('public/assets/i18n/zht.js', 'utf8'), zhtCtx);
  for (const k of keys) {
    assert.ok(enCtx.window.I18N_EN[k], `missing en key: ${k}`);
    assert.ok(jaCtx.window.I18N_JA[k], `missing ja key: ${k}`);
    assert.ok(zhsCtx.window.I18N_ZH.d[k], `missing zhs key: ${k}`);
    assert.ok(zhtCtx.window.I18N_ZH.d[k], `missing zht key: ${k}`);
  }
});

// 10. Stress test: 25 full wars simulated cleanly
test('25 full war simulations complete cleanly with active Strategic AI Planner', () => {
  let completed = 0, pacts = 0;
  for (let seed = 9100; seed < 9125; seed++) {
    const S = enterWar(seed, null);
    let g = 0;
    while (Sim.S && !Sim.S.dead && Sim.S.phase === 'war' && g++ < 20000) {
      if (Sim.S.pending) Sim.resolve(Sim.autoChoice(Sim.S.pending));
      else Sim.tick(5);
    }
    if (S.war) {
      if ((S.war.facts || []).some(f => f.type === 'ally_form' || f.type === 'enemy_coop')) pacts++;
      completed++;
    }
  }
  assert.strictEqual(completed, 25);
  assert.ok(pacts >= 1, `expected strategic pacts across 25 wars, got ${pacts}`);
});

console.log(`ALL ${ok} STRATEGIC AI PLANNER TESTS PASSED`);
