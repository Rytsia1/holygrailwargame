// Emergent Narrative Generator tests. Usage: node dev/narr_test.js <game.html>
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const src = fs.readFileSync(process.argv[2] || 'public/index.html', 'utf8');
const a = src.indexOf('<script id="sim">') + 17, b = src.indexOf('</script>', a);
let code = src.slice(a, b).replace(
  'return {cn,ACH:',
  'globalThis.__T={recFact,pairSnap,makeStray,strayFightNight,npcEnemyCoop,coalNight,retreat,useSeal,allyFinal,W:()=>S.war};\n  return {cn,ACH:'
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

function enterWar(seed = 777, forceHero = null) {
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

// 1. Strict grounding: no facts -> no arcs
test('Empty fact ledger produces zero fabricated narrative arcs', () => {
  const S = enterWar(701, 'artoria');
  S.war.facts = [];
  const N = Sim.narrative('en');
  assert.strictEqual(N.arcs.length, 0);
  assert.strictEqual(N.factCount, 0);
});

// 2. Scenario 1: Master betrays alliance (with causal chain from ally_form -> ally_ignore -> ally_betray)
test('Alliance betrayal produces grounded betrayal arc with causal factIds & story beat', () => {
  const S = enterWar(702, 'artoria');
  const w = S.war, p = w.pairs[0];
  p.ally = true; p.mname = '볼프강';
  const f1 = T.recFact('ally_form', { actor: 'p' + p.i, target: 'me', who: { a: T.pairSnap(p), b: T.pairSnap('me') } });
  const f2 = T.recFact('ally_ignore', { actor: 'p' + p.i, target: 'me', who: { a: T.pairSnap(p), b: T.pairSnap('me') }, causeId: f1.id });
  const f3 = T.recFact('ally_betray', {
    actor: 'p' + p.i, target: 'me',
    who: { a: T.pairSnap(p), b: T.pairSnap('me') },
    causeId: f2.id, meta: { kind: 'sellout' }, beat: true
  });
  const N = Sim.narrative('ko');
  const arc = N.arcs.find(x => x.kind === 'betrayal');
  assert.ok(arc, 'expected betrayal arc');
  assert.ok(arc.body.includes('볼프강'), 'betrayal body must mention betrayer name');
  assert.ok(arc.factIds.includes(f1.id) && arc.factIds.includes(f2.id) && arc.factIds.includes(f3.id));
  assert.ok(S.log.some(e => e.k === 'story' && e.fact && e.fact.id === f3.id), 'expected live story beat in log');
});

// 3. Scenario 2: Servant refuses command (real retreat(false) refusal after seal_force)
test('Prideful Servant refusing retreat generates order_refuse fact and defiance arc', () => {
  const S = enterWar(703, 'gilgamesh');
  const w = S.war, e = w.pairs[0];
  w.trust = 40;
  T.useSeal('힘을 보여라');
  let refused = false;
  for (let i = 0; i < 60 && !refused; i++) {
    w.battle = { e, ctx: {}, round: 2, maxR: 6, res: 'draw', fx: [], od: 100 };
    w.hp = 80; w.heroAlive = true; e.hp = 80; e.alive = true;
    T.retreat(false);
    if ((w.facts || []).some(f => f.type === 'order_refuse')) refused = true;
  }
  assert.ok(refused, 'expected gilgamesh to refuse retreat at least once');
  const refF = w.facts.find(f => f.type === 'order_refuse');
  assert.ok(refF.causeId, 'order_refuse should link causally to prior seal_force');
  const N = Sim.narrative('en');
  const arc = N.arcs.find(x => x.kind === 'defiance');
  assert.ok(arc, 'expected defiance arc');
  assert.ok(arc.body.includes('gilgamesh') || arc.body.includes('길가메시'));
});

// 4. Scenario 3: Two enemies forced to cooperate (duel_clash -> npcEnemyCoop / coalNight)
test('Two former enemies forced to cooperate generate enemy_coop arc linked to prior clash', () => {
  const S = enterWar(704, 'emiya');
  const w = S.war;
  const a = w.pairs[0], b = w.pairs[1], boss = w.pairs[2];
  a.mname = '에드워드'; b.mname = '카타리나';
  w.day = 5;
  const du = T.recFact('duel_clash', { actor: 'p' + a.i, target: 'p' + b.i, who: { a: T.pairSnap(a), b: T.pairSnap(b) } });
  // Ensure dominant threat triggers coop deterministically via coalNight
  w.coal = { a: a.i, b: b.i, d: 5 };
  T.coalNight();
  const coopF = w.facts.find(f => f.type === 'enemy_coop');
  assert.ok(coopF, 'expected enemy_coop fact from coalNight');
  assert.strictEqual(coopF.causeId, du.id, 'enemy_coop should link causally to prior duel_clash');
  const N = Sim.narrative('en');
  const arc = N.arcs.find(x => x.kind === 'enemy_coop');
  assert.ok(arc, 'expected enemy_coop arc');
  assert.ok(arc.body.includes('에드워드') && arc.body.includes('카타리나'));
});

// 5. Scenario 4: Master dies, Servant continues fighting (makeStray -> strayFightNight)
test('Masterless Servant continues fighting and generates masterless arc', () => {
  const S = enterWar(705, 'artoria');
  const w = S.war;
  const fallen = w.pairs[0], killer = w.pairs[1];
  fallen.hero = 'cuchulainn'; fallen.cls = 'lance'; fallen.revealed = true; fallen.hp = 90; fallen.sm = 90;
  killer.hp = 90; killer.sm = 90; killer.mname = '마르쿠스';
  w.day = 4; w.nf = [];
  T.makeStray(fallen, killer);
  assert.ok(fallen.strayFactId, 'makeStray must record master_die_stray fact');
  for (let i = 0; i < 15 && !w.facts.some(f => f.type === 'stray_fight'); i++) {
    w.nf = [];
    fallen.alive = true; fallen.hp = 90;
    killer.alive = true; killer.master = true; killer.hp = 90;
    T.strayFightNight();
  }
  const sf = w.facts.find(f => f.type === 'stray_fight');
  assert.ok(sf, 'expected stray_fight to trigger');
  assert.strictEqual(sf.causeId, fallen.strayFactId, 'stray_fight must link causally to master_die_stray');
  const N = Sim.narrative('en');
  const arc = N.arcs.find(x => x.kind === 'masterless');
  assert.ok(arc, 'expected masterless arc');
  assert.ok(arc.factIds.includes(fallen.strayFactId) && arc.factIds.includes(sf.id));
});

// 6. Multilingual rendering across ko, en, ja, zhs, zht
test('Narrative renders in all 5 languages (ko, en, ja, zhs, zht)', () => {
  const S = enterWar(706, 'gilgamesh');
  const w = S.war, p = w.pairs[0];
  p.mname = 'Elena'; p.hero = 'medea'; p.cls = 'caster'; p.revealed = true;
  const f1 = T.recFact('ally_form', { actor: 'p' + p.i, target: 'me', who: { a: T.pairSnap(p), b: T.pairSnap('me') } });
  T.recFact('ally_betray', { actor: 'p' + p.i, target: 'me', who: { a: T.pairSnap(p), b: T.pairSnap('me') }, causeId: f1.id, meta: { kind: 'final' } });
  const mockTr = x => ({ '캐스터': 'Caster', '메데이아': 'Medea', '길가메시': 'Gilgamesh' }[x] || x);
  for (const lg of ['ko', 'en', 'ja', 'zhs', 'zht']) {
    const N = Sim.narrative(lg, lg === 'en' ? mockTr : x => x);
    assert.ok(N.title && N.title.length > 0, `missing title for ${lg}`);
    assert.ok(N.arcs.length >= 1, `missing arcs for ${lg}`);
    assert.ok(N.arcs[0].body.length > 10, `empty body for ${lg}`);
  }
  const enN = Sim.narrative('en', mockTr);
  assert.ok(!/[가-힣]/.test(enN.title) && !/[가-힣]/.test(enN.arcs[0].body), `Hangul leaked in EN narrative: ${enN.arcs[0].body}`);
});

// 7. Persistence via warDigest() & snapshot()/load()
test('snapshot(), load(), and record().wd.facts preserve narrative facts', () => {
  const S = enterWar(707, 'artoria');
  let g = 0;
  while (S.phase === 'war' && !S.dead && g++ < 5000 && !(S.pending && S.war.resumeAt === 'day' && !S.war.queue.length)) {
    if (S.pending) { Sim.resolve(Sim.autoChoice(S.pending)); continue; }
    Sim.tick(1);
  }
  const p = S.war.pairs[0];
  T.recFact('ally_form', { actor: 'p' + p.i, target: 'me', who: { a: T.pairSnap(p), b: T.pairSnap('me') } });
  T.recFact('ally_betray', { actor: 'p' + p.i, target: 'me', who: { a: T.pairSnap(p), b: T.pairSnap('me') }, meta: { kind: 'sellout' } });
  const snap = Sim.snapshot();
  assert.ok(snap && snap.war && Array.isArray(snap.war.facts) && snap.war.facts.length >= 2);
  Sim.load(snap);
  const rec = Sim.record();
  assert.ok(rec.wd && Array.isArray(rec.wd.facts) && rec.wd.facts.length >= 2);
  const N = Sim.narrativeFrom(rec.wd, 'en');
  assert.ok(N.arcs.some(x => x.kind === 'betrayal'));
});

// 8. 20 full wars stability
test('20 full wars complete cleanly with emergent narrative generation active', () => {
  let totalFacts = 0;
  for (let seed = 2001; seed <= 2020; seed++) {
    Sim.newLife({ seed, len: 20 });
    Sim.start();
    let g = 0;
    while (Sim.S && !Sim.S.dead && g++ < 500000) {
      const S = Sim.S;
      if (S.pending) { Sim.resolve(Sim.autoChoice(S.pending)); continue; }
      Sim.tick(1);
    }
    assert.ok(g < 500000, `seed ${seed} exceeded tick limit`);
    const rec = Sim.record();
    if (rec.wd && rec.wd.facts) totalFacts += rec.wd.facts.length;
  }
  assert.ok(totalFacts > 0, 'expected real simulation facts to be recorded across 20 runs');
});

console.log(`All ${ok} Emergent Narrative tests passed.`);
