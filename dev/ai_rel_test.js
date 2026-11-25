// Personality-driven AI & 6-Axis Relationship System tests.
// Usage: node dev/ai_rel_test.js <game.html>
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const src = fs.readFileSync(process.argv[2] || 'public/index.html', 'utf8');
const a = src.indexOf('<script id="sim">') + 17, b = src.indexOf('</script>', a);
let code = src.slice(a, b).replace(
  'return {cn,ACH:',
  'globalThis.__T={servantPersona,masterPersona,ensureRels,relGet,relShift,betrayScore,retreat,npcWillRaid,npcRetreat,npcLines,allyIntent,loyalIntercept,W:()=>S.war,setHero:id=>{S.hero=id;}};\n  return {cn,ACH:'
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

// Helper to advance a life into the Holy Grail War
function enterWar(seed = 101, forceHero = null) {
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
  assert.strictEqual(Sim.S.phase, 'war', 'expected war phase');
  T.ensureRels();
  return Sim.S;
}

// 1. Personality Models
test('Servant personality models classify Prideful, Loyal, Cunning, Ruthless correctly', () => {
  const gil = T.servantPersona(Sim.H_BY.gilgamesh);
  const ozy = T.servantPersona(Sim.H_BY.ozymandias);
  assert.ok(gil.pride >= 70 && gil.tags.includes('prideful'), 'Gilgamesh should be prideful');
  assert.ok(ozy.pride >= 70 && ozy.tags.includes('prideful'), 'Ozymandias should be prideful');

  const leo = T.servantPersona(Sim.H_BY.leonidas);
  const diar = T.servantPersona(Sim.H_BY.diarmuid);
  const bedi = T.servantPersona(Sim.H_BY.bedivere);
  assert.ok(leo.loyalty >= 70 && leo.tags.includes('loyal'), 'Leonidas should be loyal');
  assert.ok(diar.loyalty >= 70 && diar.tags.includes('loyal'), 'Diarmuid should be loyal');
  assert.ok(bedi.loyalty >= 70 && bedi.tags.includes('loyal'), 'Bedivere should be loyal');

  const medea = T.servantPersona(Sim.H_BY.medea);
  assert.ok(medea.caution >= 65 && medea.tags.includes('cunning'), 'Medea should be cunning');
  assert.ok(medea.ruthless >= 65 && medea.tags.includes('ruthless'), 'Medea should be ruthless');
});

test('Master personality models classify Cunning, Ruthless, Prideful, Loyal archetypes', () => {
  const priest = T.masterPersona({ aid: 'priest', tac: 'cunning' });
  const atlas = T.masterPersona({ aid: 'atlas', tac: 'defensive' });
  assert.ok(priest.cunning >= 70 && priest.tags.includes('cunning'), 'Priest should be cunning');
  assert.ok(atlas.cunning >= 70 && atlas.tags.includes('cunning'), 'Atlas should be cunning');

  const killer = T.masterPersona({ aid: 'killer', tac: 'hunter' });
  const exec = T.masterPersona({ aid: 'exec', tac: 'hunter' });
  assert.ok(killer.ruthless >= 70 && killer.tags.includes('ruthless'), 'Killer should be ruthless');
  assert.ok(exec.ruthless >= 70 && exec.tags.includes('ruthless'), 'Exec should be ruthless');

  const lord = T.masterPersona({ aid: 'lord', tac: 'proud' });
  assert.ok(lord.pride >= 70 && lord.tags.includes('prideful'), 'Lord should be prideful');

  const dem = T.masterPersona({ aid: 'democrat', tac: 'naive' });
  assert.ok(dem.loyal >= 70 && dem.tags.includes('loyal'), 'Democrat should be loyal');
});

// 2. 6-Axis Relationship Graph initialization, mutation, clamping & Trust sync
test('6-axis relationship matrix initializes, mutates, clamps [0,100], and syncs with w.trust', () => {
  const S = enterWar(202, 'gilgamesh');
  const w = S.war;
  const r = Sim.relMatrix('me', 'hero');
  assert.strictEqual(r.trust, Math.round(w.trust));
  for (const ax of ['trust', 'affection', 'fear', 'respect', 'rivalry', 'grudge']) {
    assert.ok(r[ax] >= 0 && r[ax] <= 100, `${ax} out of bounds: ${r[ax]}`);
  }
  const t0 = w.trust;
  T.relShift('me', 'hero', { trust: 15, affection: 200, fear: -50, respect: 12, rivalry: 8, grudge: 10 });
  assert.strictEqual(w.trust, Math.min(100, t0 + 15));
  assert.strictEqual(Sim.relMatrix('me', 'hero').trust, Math.round(w.trust));
  assert.strictEqual(Sim.relMatrix('me', 'hero').affection, 100);
  assert.strictEqual(Sim.relMatrix('me', 'hero').fear, 0);
});

// 3. Prideful Servant refuses retreat vs Command Spell always succeeds
test('Prideful Servant refuses retreat significantly more often than non-prideful Servant', () => {
  let prideRefusals = 0, calmRefusals = 0;
  const S1 = enterWar(303, 'gilgamesh');
  S1.war.trust = 50;
  const e1 = S1.war.pairs[0];
  for (let i = 0; i < 80; i++) {
    S1.war.battle = { e: e1, ctx: {}, round: 2, maxR: 6, res: 'draw', fx: [], od: 100 };
    S1.war.hp = 80; S1.war.heroAlive = true; e1.hp = 80; e1.alive = true;
    T.retreat(false);
    if (S1.war.battle && S1.war.battle.res !== 'retreat') prideRefusals++;
  }
  const S2 = enterWar(304, 'robin');
  S2.war.trust = 50;
  const e2 = S2.war.pairs[0];
  for (let i = 0; i < 80; i++) {
    S2.war.battle = { e: e2, ctx: {}, round: 2, maxR: 6, res: 'draw', fx: [], od: 100 };
    S2.war.hp = 80; S2.war.heroAlive = true; e2.hp = 80; e2.alive = true;
    T.retreat(false);
    if (S2.war.battle && S2.war.battle.res !== 'retreat') calmRefusals++;
  }
  assert.ok(prideRefusals > calmRefusals + 5, `expected prideRefusals (${prideRefusals}) > calmRefusals (${calmRefusals})`);

  // Command Spell retreat(true) always bypasses pride refusal
  const S3 = enterWar(305, 'gilgamesh');
  S3.war.trust = 20;
  S3.war.battle = { e: S3.war.pairs[0], ctx: {}, round: 2, maxR: 6, res: 'draw', fx: [], od: 100 };
  T.retreat(true);
  assert.strictEqual(S3.war.battle, null, 'retreat(true) should always end battle');
});

// 4. Cunning Master avoids direct fights when unprepped/wounded
test('Cunning Master avoids direct unprepped raids compared to Reckless Master', () => {
  enterWar(404);
  const cunP = { i: 1, aid: 'priest', tac: 'cunning', hero: 'medea', cls: 'caster', pw: 65, hp: 78, sm: 90, master: true, alive: true, seals: 3 };
  const reckP = { i: 2, aid: 'avenger', tac: 'reckless', hero: 'heracles', cls: 'berserk', pw: 65, hp: 78, sm: 90, master: true, alive: true, seals: 3 };
  let cunRaids = 0, reckRaids = 0;
  for (let i = 0; i < 60; i++) {
    if (T.npcWillRaid(cunP)) cunRaids++;
    if (T.npcWillRaid(reckP)) reckRaids++;
  }
  assert.strictEqual(cunRaids, 0, 'unprepped cunning master at <85 HP should avoid direct raid');
  assert.ok(reckRaids > 30, `reckless master should still raid often (${reckRaids}/60)`);
});

// 5. Loyal Servant intercepts damage & helps Master retreat safely
test('Loyal Servant intercepts lethal/chip damage aimed at Master', () => {
  const S = enterWar(505, 'leonidas');
  const w = S.war;
  w.trust = 55;
  S.st.health = 80;
  let blocked = 0;
  for (let i = 0; i < 60; i++) {
    w.hp = 100;
    w.battle = { e: w.pairs[0], ctx: {}, round: 1, maxR: 5, res: 'draw', fx: [] };
    if (T.loyalIntercept(w.battle, 10, '마탄을')) blocked++;
  }
  assert.ok(blocked >= 10, `expected loyal Servant to intercept often (${blocked}/60)`);
  assert.strictEqual(S.st.health, 80, 'Master health should remain untouched by loyalIntercept');
});

// 6. Ruthless Master betrayalScore & allyIntent driven by 6-axis relationships
test('Betrayal score responds to Ruthless persona, Grudge, Trust, and Fear duality', () => {
  const ruth = T.masterPersona({ aid: 'killer', tac: 'hunter' });
  const loy = T.masterPersona({ aid: 'democrat', tac: 'naive' });
  const highGrudge = { trust: 10, affection: 5, fear: 5, respect: 15, rivalry: 40, grudge: 80 };
  const highBond = { trust: 90, affection: 80, fear: 10, respect: 85, rivalry: 10, grudge: 0 };

  const bBad = T.betrayScore(highGrudge, ruth, { seals: 1, hp: 60 });
  const bGood = T.betrayScore(highBond, loy, { seals: 3, hp: 90 });
  assert.ok(bBad > 0.65, `expected high betrayal score (${bBad})`);
  assert.ok(bGood < 0.1, `expected low betrayal score (${bGood})`);

  // Fear deters betrayal while strong, flips when weak
  const fearfulRel = { trust: 25, affection: 10, fear: 80, respect: 20, rivalry: 20, grudge: 40 };
  const bStrong = T.betrayScore(fearfulRel, ruth, { seals: 3, hp: 90 });
  const bWeak = T.betrayScore(fearfulRel, ruth, { seals: 0, hp: 25 });
  assert.ok(bWeak > bStrong + 0.3, `expected fear to flip when target weakens (${bStrong} -> ${bWeak})`);
});

// 7. Snapshot / Load serialization preserves S.war.rels
test('snapshot() and load() preserve 6-axis relationship state', () => {
  const S = enterWar(606, 'artoria');
  let g = 0;
  while (S.phase === 'war' && !S.dead && g++ < 5000 && !(S.pending && S.war.resumeAt === 'day' && !S.war.queue.length)) {
    if (S.pending) { Sim.resolve(Sim.autoChoice(S.pending)); continue; }
    Sim.tick(1);
  }
  T.relShift('me', 'hero', { affection: 25, respect: 18, grudge: 14 });
  const pid = 'p' + S.war.pairs[0].i;
  T.relShift(pid, 'me', { fear: 33, rivalry: 44 });
  const snap = Sim.snapshot();
  assert.ok(snap && snap.war && snap.war.rels, 'snapshot should contain war.rels');
  Sim.load(snap);
  assert.strictEqual(Sim.relMatrix('me', 'hero').affection, snap.war.rels['me|hero'].affection);
  assert.strictEqual(Sim.relMatrix(pid, 'me').fear, snap.war.rels[pid + '|me'].fear);
  assert.strictEqual(Sim.relMatrix(pid, 'me').rivalry, snap.war.rels[pid + '|me'].rivalry);
});

// 8. Full war simulation stability across 20 seeds
test('20 full wars complete cleanly without exceptions', () => {
  for (let seed = 1001; seed <= 1020; seed++) {
    Sim.newLife({ seed, len: 20 });
    Sim.start();
    let g = 0;
    while (Sim.S && !Sim.S.dead && g++ < 500000) {
      const S = Sim.S;
      if (S.pending) { Sim.resolve(Sim.autoChoice(S.pending)); continue; }
      Sim.tick(1);
    }
    assert.ok(g < 500000, `seed ${seed} exceeded tick limit`);
  }
});

console.log(`All ${ok} AI & Relationship tests passed.`);
