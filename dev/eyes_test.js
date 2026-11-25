// 6 New Mystic Eyes & Rainbow Grade tests. Usage: node dev/eyes_test.js <game.html>
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const src = fs.readFileSync(process.argv[2] || 'public/index.html', 'utf8');
const a = src.indexOf('<script id="sim">') + 17, b = src.indexOf('</script>', a);
let code = src.slice(a, b).replace(
  'return {cn,ACH:',
  'globalThis.__T={MACT,duelEye,deathGrasp,expUp,addIntel,scout,npcInitB,npcRetreat,npFieldDur,npWallDur,npSupDur,npBase,clash,battle,threat,giftRoll,giftCost,giftOn,giftIs,fxL,W:()=>S.war};\n  return {cn,ACH:'
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

function startWithEye(id, gr = 3, seed = 950, heroId = 'artoria') {
  ctx.globalThis.__FORCE_HERO = heroId;
  Sim.newLife({
    seed, len: 20,
    custom: { on: true, mode: 'free', origin: 'noble', circuit: 5, gift: id, giftGr: gr, arts: { element: 2 } }
  });
  Sim.start();
  let g = 0;
  while (Sim.S && !Sim.S.dead && g++ < 400000 && !(Sim.S.phase === 'war' && Sim.S.war && Sim.S.war.heroAlive)) {
    const S = Sim.S;
    if (S.pending) { Sim.resolve(Sim.autoChoice(S.pending)); continue; }
    Sim.tick(1);
  }
  ctx.globalThis.__FORCE_HERO = null;
  if (Sim.S.gift) { Sim.S.gift.awake = true; Sim.S.gift.ctl = 2; }
  assert.strictEqual(Sim.S.phase, 'war');
  return Sim.S;
}

// 1. Data registration, Rainbow Grade 5, 10pt budget cost, and Death Perception extreme rarity
test('GIFTS registers 6 new eyes, Grade 5 무지개 costs 10pt, and Death Perception is rarest', () => {
  for (const id of ['illusion', 'clairvoyance', 'immob', 'vtheft', 'prolong', 'death']) {
    assert.ok(Sim.GIFTS[id], `missing GIFTS.${id}`);
  }
  assert.strictEqual(Sim.GRADE_N[5], '무지개');
  const weights = Object.entries(Sim.GIFTS).filter(([k, v]) => k !== 'blood').map(([k, v]) => [k, v.w]).sort((x, y) => x[1] - y[1]);
  assert.strictEqual(weights[0][0], 'death', 'death must be the rarest eye');
  assert.ok(weights[0][1] <= 0.25);

  const cl = Sim.custClamp({ on: true, mode: 'pt', origin: 'noble', circuit: 3, gift: 'death', giftGr: 5 });
  assert.strictEqual(cl.giftGr, 5);
  const res = Sim.custCost({ on: true, mode: 'pt', origin: 'noble', circuit: 3, arts: {}, gift: 'death', giftGr: 5 });
  assert.strictEqual(res.cost, 10, `expected 10pt for Rainbow, got ${res.cost}`);
  assert.strictEqual(res.errs.length, 0, '10pt Rainbow within default 10pt budget should have 0 errs');
});

// 2. Illusion: suppresses exposure, activates b.eyeIll, and triggers decoy misdirection
test('Illusion reduces exposure gain, sets b.eyeIll, and misdirects threats', () => {
  const S = startWithEye('illusion', 3, 951);
  assert.strictEqual(T.expUp(10) < 10, true, 'illusion should reduce exposure gain');
  const e = S.war.pairs[0];
  T.battle(e, {});
  const b = S.war.battle;
  T.MACT.eye.f(b, e);
  assert.ok(b.eyeIll && b.eyeIll.v > 0.2, 'expected active eyeIll mirage');
  assert.ok(b.mDeb && b.mDeb.v > 0, 'expected perceptual debuff');
});

// 3. Clairvoyance: boosts intel, expands scout range (+1 target), and reduces ambush initB
test('Clairvoyance boosts intel, hits second target on scout, and blunts ambush initiative', () => {
  const S = startWithEye('clairvoyance', 3, 952);
  const w = S.war;
  w.pairs.forEach(p => { p.intel = 0; p.known = false; });
  T.addIntel(w.pairs[0], 10, 'trace');
  assert.ok(w.pairs[0].intel > 10, `expected clairvoyance intel boost > 10, got ${w.pairs[0].intel}`);

  T.scout();
  const touched = w.pairs.filter(p => p.intel > 0).length;
  assert.ok(touched >= 2, `expected clairvoyance scout to touch >=2 targets, got ${touched}`);

  T.battle(w.pairs[1], { ambushed: true });
  assert.ok(T.npcInitB(S.war.battle) < 10, 'clairvoyance should lower ambush initiative bonus');
});

// 4. Immobilization: sets b.eyeImmob, empowers next strike, and reduces enemy retreat chance
test('Immobilization applies motion drag, retreat penalty, and next-strike bonus', () => {
  const S = startWithEye('immob', 3, 953);
  const e = S.war.pairs[0];
  T.battle(e, {});
  const b = S.war.battle;
  T.MACT.eye.f(b, e);
  assert.ok(b.eyeImmob && b.eyeImmob.agiPen >= 2);
  assert.ok(b.eyeImmob.fleePen >= 0.3);
  assert.strictEqual(b.immobNext, 1);
  T.clash(0);
  assert.strictEqual(b.immobNext, 0, 'next-strike bonus should be consumed by clash');
});

// 5. Vision Theft: steals intel, extracts third-party know, reveals kit, lowers exposure
test('Vision Theft steals target intel, third-party know, hidden kit, and reduces exposure', () => {
  const S = startWithEye('vtheft', 3, 954);
  const w = S.war;
  w.exposure = 40;
  const e = w.pairs[0], third = w.pairs[1];
  e.intel = 0; e.scoutEdge = 1; e.kitSeen = false;
  e.know = { [third.i]: 50 };
  third.intel = 0;
  T.battle(e, {});
  const b = S.war.battle;
  T.MACT.eye.f(b, e);
  assert.ok(e.intel >= 20, 'expected stolen target intel');
  assert.strictEqual(e.kitSeen, true, 'expected kit revealed');
  assert.strictEqual(e.scoutEdge, 0, 'expected scoutEdge stripped');
  assert.ok(w.exposure < 40, 'expected exposure lowered');
  assert.ok(third.intel >= 15, 'expected third-party knowledge transferred from e.know');
});

// 6. Prolongation: passively +1 NP durations and actively extends + amplifies buffs/debuffs
test('Prolongation extends active buffs/debuffs/NP durations and amplifies values', () => {
  const S = startWithEye('prolong', 4, 955, 'medea');
  const e = S.war.pairs[0];
  T.battle(e, {});
  const b = S.war.battle;
  const fDur = T.npFieldDur(b, 'me');
  assert.ok(fDur >= 3);
  b.mPow = { r: b.round, v: 10 };
  b.eWeak = { until: b.round + 1, v: 8 };
  T.fxL(b).push({ side: 'me', type: 'sup', id: 'merlin', left: 2, age: 0 });
  T.MACT.eye.f(b, e);
  assert.ok(b.mPow.until >= b.round + 2 && b.mPow.v > 10, 'expected mPow extended & amplified');
  assert.ok(b.eWeak.until >= b.round + 3 && b.eWeak.v > 8, 'expected eWeak extended & amplified');
  assert.strictEqual(T.fxL(b).find(x => x.side === 'me').left, 4, 'expected NP sup extended by +2 at ctl=2');
});

// 7. Death Perception: balance restrictions, regen disable, defense pierce, Point of Death vs normal vs Boss
test('Death Perception enforces balance restrictions, disables regen, pierces defenses, and spares Boss instant-kill', () => {
  const S = startWithEye('death', 5, 956, 'artoria');
  const e = S.war.pairs[0];
  S.st.will = 20;
  T.battle(e, {});
  assert.strictEqual(T.MACT.eye.req(), false, 'requires will >= 35');
  S.st.will = 70; S.st.health = 95;
  S.war.battle.ctx.remote = true;
  assert.strictEqual(T.MACT.eye.req(), false, 'cannot invoke Death Perception remotely via familiar');
  S.war.battle.ctx.remote = false;
  assert.strictEqual(T.MACT.eye.req(), true);

  const hpBefore = S.st.health, willBefore = S.st.will;
  T.MACT.eye.f(S.war.battle, e);
  assert.ok(S.st.health < hpBefore && S.st.will < willBefore, 'expected heavy physical & mental strain');
  assert.ok(e.noRegen >= 3, 'expected enemy regeneration disabled');

  // Force Point of Death against Boss -> NO instant kill (hp stays > 0 if high HP)
  const boss = { i: 99, cx: 'boss', cls: 'avenger', hero: 'dantes', hp: 100, alive: true, seals: 0, pw: 70 };
  S.war.battle.e = boss;
  S.war.battle.eyeDeath = { until: S.war.battle.round + 2, mode: 'point', pointDone: false };
  boss.hp = 90;
  T.clash(30, 'round');
  assert.ok(boss.alive && boss.hp > 0, 'Boss must resist Point of Death instant execution');

  // Force Point of Death against normal Servant -> executes (hp === 0)
  const norm = S.war.pairs[1];
  let executed = false;
  for (let k = 0; k < 12; k++) {
    S.war.heroAlive = true; S.war.hp = 100; S.war.sm = 100; S.pending = null;
    norm.hp = 85; norm.alive = true; norm.cx = null; norm.bxNun = false; norm.usedRevive = false;
    norm.hero = 'kojiro'; norm.cls = 'sword';
    T.battle(norm, {});
    S.war.battle.eyeDeath = { until: S.war.battle.round + 5, mode: 'point', pointDone: false };
    T.clash(60, 'round');
    if (S.pending) Sim.resolve(0);
    if (norm.hp === 0) { executed = true; break; }
  }
  assert.ok(executed, 'Point of Death should be able to execute a normal Servant');

  // Special existence resistance test (Divine boss vs plain servant)
  const plain = { i: 50, hero: 'kojiro', aid: 'student', hp: 80, alive: true };
  const divBoss = { i: 51, hero: 'karna', aid: 'apostle', cx: 'boss', hp: 80, alive: true };
  const gPlain = T.deathGrasp(plain, S.war.battle);
  const gDiv = T.deathGrasp(divBoss, S.war.battle);
  assert.ok(gPlain.p > gDiv.p, `expected plain read prob (${gPlain.p}) > divine boss (${gDiv.p})`);
});

// 8. Translation keys present in all 4 external i18n files
test('all 6 new Mystic Eyes & 무지개 keys present in en, ja, zhs, zht bundles', () => {
  const keys = ['무지개', '환각의 마안', '천리안의 마안', '정지의 마안', '탈시의 마안', '연장의 마안', '직사의 마안', '무지개의 눈'];
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

// 9. Full war stress test across all 6 new Mystic Eyes
test('24 full wars across all 6 new Mystic Eyes complete cleanly without exceptions', () => {
  const ids = ['illusion', 'clairvoyance', 'immob', 'vtheft', 'prolong', 'death'];
  let done = 0;
  for (let i = 0; i < 24; i++) {
    const id = ids[i % ids.length];
    const gr = id === 'death' ? 5 : id === 'prolong' ? 4 : 3;
    const S = startWithEye(id, gr, 9800 + i, null);
    let g = 0;
    while (Sim.S && !Sim.S.dead && Sim.S.phase === 'war' && g++ < 20000) {
      if (Sim.S.pending) Sim.resolve(Sim.autoChoice(Sim.S.pending));
      else Sim.tick(5);
    }
    done++;
  }
  assert.strictEqual(done, 24);
});

console.log(`ALL ${ok} MYSTIC EYES TESTS PASSED`);
