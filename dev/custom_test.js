// Custom Master unit tests. Usage: node dev/custom_test.js <game.html>
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const src = fs.readFileSync(process.argv[2] || 'public/index.html', 'utf8');
const a = src.indexOf('<script id="sim">') + 17, b = src.indexOf('</script>', a);
const code = src.slice(a, b);
const ctx = { console }; ctx.globalThis = ctx; ctx.window = ctx;
vm.createContext(ctx);
vm.runInContext(code + ';globalThis.Sim=Sim;', ctx);
const Sim = ctx.Sim;
Sim.setHooks(new Proxy({}, { get: () => () => {} }));

let ok = 0;
function test(name, fn) {
  fn();
  ok++;
  console.log('✓', name);
}

// 1. noble B circuit + family art lv1 = 0
test('noble B circuit + family art lv1 = 0', () => {
  const r = Sim.custCost({
    mode: 'pt', origin: 'noble', circuit: 4,
    st: { mana: 30, lore: 2, will: 25, bond: 50, health: 80, wealth: 70 },
    arts: { element: 1 }, main: 'element', gift: 'random'
  });
  assert.strictEqual(r.cost, 0);
  assert.strictEqual(r.errs.length, 0);
});

// 2. noble A circuit + family art lv2 + gift 중 = 6
test('noble A circuit + family art lv2 + gift mid = 6', () => {
  const r = Sim.custCost({
    mode: 'pt', origin: 'noble', circuit: 5,
    st: { mana: 38, lore: 2, will: 25, bond: 50, health: 80, wealth: 70 },
    arts: { element: 2 }, main: 'element', gift: 'charm', giftGr: 2
  });
  assert.strictEqual(r.cost, 6);
  assert.strictEqual(r.errs.length, 0);
});

// 3. common A circuit = 6
test('common A circuit = 6', () => {
  const r = Sim.custCost({
    mode: 'pt', origin: 'common', circuit: 5,
    st: { mana: 38, lore: 2, will: 25, bond: 50, health: 80, wealth: 40 },
    arts: {}, gift: 'none'
  });
  assert.strictEqual(r.cost, 6);
  assert.strictEqual(r.errs.length, 0);
});

// 4. compel jewel grade = 9
test('mata compel jewel = 9', () => {
  const r = Sim.custCost({
    mode: 'pt', origin: 'common', circuit: 2,
    st: { mana: 18, lore: 2, will: 25, bond: 50, health: 80, wealth: 40 },
    arts: {}, gift: 'compel', giftGr: 4
  });
  assert.strictEqual(r.cost, 9);
  assert.strictEqual(r.errs.length, 0);
});

// 5. 4 magic arts -> error
test('4 magic arts -> error', () => {
  const r = Sim.custCost({
    mode: 'free', origin: 'noble', circuit: 5,
    st: { mana: 38, lore: 2, will: 25, bond: 50, health: 80, wealth: 70 },
    arts: { element: 1, barrier: 1, rune: 1, jewel: 1 }, main: 'element', gift: 'none'
  });
  assert.ok(r.errs.length > 0, 'expected error for 4 magic arts');
});

// 6. lv4 without circuit A -> error
test('lv4 without circuit A -> error', () => {
  const r = Sim.custCost({
    mode: 'free', origin: 'noble', circuit: 4,
    st: { mana: 32, lore: 2, will: 25, bond: 50, health: 80, wealth: 70 },
    arts: { element: 4 }, main: 'element', gift: 'none'
  });
  assert.ok(r.errs.length > 0, 'expected error for lv4 without A circuit');
});

// 7. mana > manaCap() -> error
test('mana > manaCap() -> error', () => {
  const r = Sim.custCost({
    mode: 'free', origin: 'common', circuit: 1, // cap = 52
    st: { mana: 60, lore: 2, will: 25, bond: 50, health: 80, wealth: 40 },
    arts: {}, gift: 'none'
  });
  assert.ok(r.errs.length > 0, 'expected error for mana > manaCap');
});

// 8. free mode ignores budget > 10 but keeps structural limits
test('free mode ignores budget but enforces structural limits', () => {
  const okFree = Sim.custCost({
    mode: 'free', origin: 'common', circuit: 5,
    st: { mana: 95, lore: 90, will: 90, bond: 90, health: 95, wealth: 90 },
    arts: { element: 4, barrier: 3, bajiquan: 3 }, main: 'element', gift: 'compel', giftGr: 4
  });
  assert.ok(okFree.cost > 10);
  assert.strictEqual(okFree.errs.length, 0);
});

// 9. newLife({custom}) sets origin, circuit, st, arts, gift, flags.awakened, record().custom
test('newLife({custom}) applies all custom fields and flags', () => {
  const S = Sim.newLife({
    seed: 12345, len: 20,
    custom: {
      on: true, mode: 'pt', origin: 'common', city: '런던', era: 'past', circuit: 3,
      st: { mana: 25, lore: 10, will: 30, bond: 45, health: 85, wealth: 50 },
      arts: { element: 2, familiar: 1 }, main: 'element', gift: 'future', giftGr: 3
    }
  });
  assert.strictEqual(S.origin, 'common');
  assert.strictEqual(S.circuit, 3);
  assert.strictEqual(S.city.n, '런던');
  assert.ok(S.birthYear >= 1930 && S.birthYear <= 1965);
  assert.strictEqual(S.st.mana, 25);
  assert.strictEqual(S.st.lore, 10);
  assert.strictEqual(S.wealth, 50);
  assert.strictEqual(S.arts.element.lv, 2);
  assert.strictEqual(S.arts.element.main, true);
  assert.strictEqual(S.arts.familiar.lv, 1);
  assert.strictEqual(S.flags.familiar, '까마귀');
  assert.strictEqual(S.flags.awakened, 1);
  assert.strictEqual(S.gift.id, 'future');
  assert.strictEqual(S.gift.gr, 3);
  assert.strictEqual(S.custom.mode, 'pt');
  assert.strictEqual(Sim.record().custom, 1);
});

// 10. normal newLife({}) has no S.custom
test('normal newLife({}) unchanged', () => {
  const S = Sim.newLife({ seed: 99, len: 20 });
  assert.strictEqual(S.custom, undefined);
  assert.strictEqual(Sim.record().custom, undefined);
});

console.log(`All ${ok} tests passed.`);
