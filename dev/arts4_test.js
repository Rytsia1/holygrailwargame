// 4 New Magic Learned Arts tests. Usage: node dev/arts4_test.js <game.html>
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const src = fs.readFileSync(process.argv[2] || 'public/index.html', 'utf8');
const a = src.indexOf('<script id="sim">') + 17, b = src.indexOf('</script>', a);
let code = src.slice(a, b).replace(
  'return {cn,ACH:',
  'globalThis.__T={MACT,myMDScore,duelMaster,duelBikis,expUp,infilD,initB,myPower,pastSee,famGuard,mBon,battle,clash,W:()=>S.war};\n  return {cn,ACH:'
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

function startWithArts(arts, seed = 1050, heroId = 'artoria') {
  ctx.globalThis.__FORCE_HERO = heroId;
  Sim.newLife({
    seed, len: 20,
    custom: { on: true, mode: 'free', origin: 'noble', circuit: 5, gift: 'none', arts }
  });
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

// 1. Registration, max level 3, Custom Master limits & ACH auto-generation
test('All 4 Magic Learned Arts registered with max level 3, Custom Master support, and ACH entries', () => {
  const ids = ['projection', 'evocation', 'illusion_art', 'displacement'];
  for (const id of ids) {
    assert.ok(Sim.ARTS[id] && Sim.ARTS[id].br === 'magic', `missing magic art ${id}`);
    assert.strictEqual(Sim.ART_CHAIN[id].max, 3, `${id} max must be 3`);
    assert.ok(Sim.ACH.some(x => x.id === `art_${id}_1`) && Sim.ACH.some(x => x.id === `art_${id}_3`), `missing ACH for ${id}`);
  }
  // Exceeding max lv 3 errors
  const over = Sim.custCost({ on: true, mode: 'free', origin: 'noble', circuit: 5, arts: { projection: 4 } });
  assert.ok(over.errs.some(e => e.includes('최대 단계')));
  // Lv 3 with circuit < C errors
  const lowC = Sim.custCost({ on: true, mode: 'free', origin: 'common', circuit: 2, arts: { displacement: 3 } });
  assert.ok(lowC.errs.some(e => e.includes('C등급')));
  // 4 magic arts errors (>3 limit)
  const four = Sim.custCost({ on: true, mode: 'free', origin: 'noble', circuit: 5, arts: { projection: 1, evocation: 1, illusion_art: 1, displacement: 1 } });
  assert.ok(four.errs.some(e => e.includes('3개')));
});

// 2. Projection Magecraft: MACT.proj, duel weapons, Final Duel biki
test('Projection Magecraft projects combat armament, boosts Master duels, and unlocks lv3 biki', () => {
  const S = startWithArts({ projection: 3 }, 1051);
  S.arts = {};
  const rush0 = T.myMDScore('rush'), atk0 = T.myMDScore('atkM');
  S.arts = { projection: { lv: 3, q: 1, xp: 0, main: true } };
  assert.ok(T.myMDScore('rush') > rush0, 'projection should boost rush with temporary weapon');
  assert.ok(T.myMDScore('atkM') > atk0, 'projection should boost atkM');
  assert.ok(T.duelBikis(T.duelMaster()).some(x => x.k === 'projection'), 'expected projection lv3 biki');

  const e = S.war.pairs[0];
  T.battle(e, {});
  const b = S.war.battle;
  T.MACT.proj.f(b, e);
  assert.ok(b.proj && b.proj.until === b.round + 1 && b.proj.v >= 14, 'lv3 proj lasts 2 rounds with high bonus');
  assert.ok(T.mBon(b) >= b.proj.v);
});

// 3. Spiritual Evocation: MACT.evoke (power + guard + SM regen), pastSee intel, famGuard warning, biki
test('Spiritual Evocation provides possession buff/guard/SM regen, spirit intel, ambush guard, and biki', () => {
  const S = startWithArts({ evocation: 3 }, 1052);
  assert.ok(T.duelBikis(T.duelMaster()).some(x => x.k === 'evocation'), 'expected evocation lv3 biki');
  const e = S.war.pairs[0];
  e.intel = 0; e.pastSeen = false; e.scoutEdge = 1;
  T.pastSee(e);
  assert.ok(e.intel >= 15, 'evocation pastSee should whisper intel');
  T.famGuard(e);
  assert.strictEqual(e.scoutEdge, 0, 'evocation lv>=2 should trigger famGuard ambush warning');

  S.war.sm = 50;
  T.battle(e, {});
  const b = S.war.battle;
  T.MACT.evoke.f(b, e);
  assert.ok(b.evoke && b.evoke.pow >= 14 && b.evoke.guard >= 0.16);
  assert.strictEqual(S.war.sm, 58, 'lv3 evocation should restore +8 SM');
});

// 4. Illusion Arts: MACT.mirage, exposure reduction, infilD & initB ambush bonuses, biki
test('Illusion Arts lowers exposure, boosts infiltration and ambush initiative, deploys decoy, and unlocks biki', () => {
  const S = startWithArts({ illusion_art: 3 }, 1053);
  const e = S.war.pairs[0];
  S.arts = {};
  const inf0 = T.infilD(e, false), exp0 = T.expUp(10);
  S.arts = { illusion_art: { lv: 3, q: 1, xp: 0, main: true } };
  assert.ok(T.duelBikis(T.duelMaster()).some(x => x.k === 'illusion_art'), 'expected illusion_art lv3 biki');
  assert.ok(T.expUp(10) < exp0, 'illusion_art should reduce exposure gain');
  assert.ok(T.infilD(e, false) > inf0, 'illusion_art should boost infilD');

  T.battle(e, { attack: true });
  const b = S.war.battle;
  assert.strictEqual(T.initB(b), 19, 'lv3 illusion_art should boost round-1 ambush initB from 10 to 19');
  T.MACT.mirage.f(b, e);
  assert.ok(b.artIll && b.artIll.until === b.round + 1 && b.artIll.v >= 0.25);
});

// 5. Displacement Magecraft: MACT.swap counter-trap, trap neutralization, Master duel def/trk, biki
test('Displacement Magecraft neutralizes trap penalties, springs automatic counter damage, and unlocks biki', () => {
  const S0 = startWithArts({}, 1054);
  const pwTrap0 = T.myPower({ trap: true });
  const pwNorm0 = T.myPower({ trap: false });
  assert.ok(pwNorm0 - pwTrap0 >= 7.5);

  const S = startWithArts({ displacement: 3 }, 1054);
  assert.ok(T.duelBikis(T.duelMaster()).some(x => x.k === 'displacement'), 'expected displacement lv3 biki');
  assert.strictEqual(T.myPower({ trap: false }) - T.myPower({ trap: true }), 0, 'lv>=2 displacement negates trap penalty');

  const e = S.war.pairs[0];
  e.hp = 90; e.hero = 'kojiro'; e.cls = 'sword';
  T.battle(e, {});
  const b = S.war.battle;
  T.MACT.swap.f(b, e);
  assert.ok(b.dispTrap && b.dispTrap.v >= 15 && b.dispTrap.red >= 0.35);
  // Trigger counter when losing clash (-60 bonus)
  T.clash(-60, 'round');
  if (S.pending) Sim.resolve(0);
  assert.ok(e.hp <= 90 - 15, `expected displacement counter damage on enemy, hp=${e.hp}`);
});

// 6. i18n completeness across en, ja, zhs, zht
test('all 4 new Learned Arts & actions translated in en, ja, zhs, zht bundles', () => {
  const keys = ['투영 마술', '영매 마술', '환술', '치환 마술', '무구 투영', '영령 빙의', '환영 미끼', '치환 반격', '치환으로 자리를 바꾼다'];
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

// 7. Stress test: 20 full war simulations across the 4 new Learned Arts
test('20 full war simulations across all 4 new Learned Arts complete cleanly', () => {
  const builds = [
    { projection: 3, enhance: 2 },
    { evocation: 3, barrier: 2 },
    { illusion_art: 3, mind: 2 },
    { displacement: 3, element: 2 },
  ];
  let done = 0;
  for (let i = 0; i < 20; i++) {
    startWithArts(builds[i % builds.length], 11200 + i, null);
    let g = 0;
    while (Sim.S && !Sim.S.dead && Sim.S.phase === 'war' && g++ < 20000) {
      if (Sim.S.pending) Sim.resolve(Sim.autoChoice(Sim.S.pending));
      else Sim.tick(5);
    }
    done++;
  }
  assert.strictEqual(done, 20);
});

console.log(`ALL ${ok} LEARNED ARTS TESTS PASSED`);
