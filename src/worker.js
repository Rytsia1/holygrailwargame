// 성배가 차는 밤 — 서버 쪽 코드
// 게임 파일(public/)은 클라우드플레어가 바로 내주고, 여기서는 /api/ 요청만 받는다.
//
//   GET  /api/health  상태 확인
//   POST /api/life    한 생이 끝날 때 게임 결과를 익명으로 받는다
//   POST /api/life/fix  새 서번트가 허용 목록에 빠져 있던 동안 서번트 칸이 빈 채 저장된 생을 그 기기의 기록으로 채운다
//   GET  /api/stats   모인 결과를 합쳐 돌려준다 (합친 결과를 D1 한 줄로 두고 10분마다 한 요청만 다시 센다)
//                     ?since=&until= (ms 시각, since=new는 신규 서번트 17명이 처음 기록된 때) — 그 기간만 클래스·서번트·엔딩별로 (통계 페이지 /stats.html)
//   POST /api/ghost   살아남은 조를 다른 겨울로 보낸다 (이름을 공개하기로 한 경우에만 이름 포함)
//   GET  /api/ghost   ?year=&dev= — 1~40년 앞선 전쟁에서 살아남은 다른 기기의 조를 몇 개 받는다
//   POST /api/ghost/shown · /withdraw · /report — 등장 횟수, 거두기, 신고(3번이면 숨김)
//   POST /api/ghost/result  그 조가 끼어든 전쟁의 결과(받은 기기가 전쟁이 끝날 때 한 번 보냄)
//   POST /api/ghost/news    보낸 기기가 자기 조들의 결과 소식을 받아 간다(받은 쪽 플레이어 정보는 담지 않음)
//   POST /api/ghost/mine    보낸 기기(와 연결된 기기)가 아직 거두지 않은 조 목록 — 시작 화면 '보낸 조' 탭
//   POST /api/sync/new · /code · /join · /pull · /push · /leave · /devs · /kick · /name
//        기기 연결: 같은 사람이 웹·모바일을 오가며 같은 기록을 쓰도록, 압축한 기록 묶음을 비밀 키로 맡아 둔다.
//        키 자체는 저장하지 않고 해시만 둔다. 연결 코드는 10분 동안 한 번만 쓸 수 있다.
//        기기마다 따로 출입증(dk)을 주고 해시만 둔다. 목록에서 다른 기기를 끊으면 그 기기의 출입증만 지운다.
//        기기 목록에는 기기 종류(예: 'iPhone · Safari'), 직접 붙인 이름, 연결한 때, 마지막으로 맞춘 때만 남긴다.
//        마지막 접근 뒤 180일이 지나거나 모든 기기가 연결을 끊으면 지운다. 내용은 열어 보지 않는다(크기만 본다).
//
// 받는 것: 서번트·클래스, 엔딩 종류, 성배 상태, 도시, 출신, 회로 등급, 사망 나이, 언어,
//          그 기기에서 지금까지 연 업적 목록, 기기마다 무작위로 만든 번호.
// 받지 않는 것: 이름, 소원·유언처럼 직접 쓴 문장, IP 주소.
//   (이름 신고만은 같은 사람이 여러 번 신고하지 못하도록, 접속 주소를 서버만 아는 값으로 섞어 되돌릴 수 없게 만든
//    짧은 값을 신고 기록에 함께 남긴다. 접속 주소 자체는 저장하지 않는다.)
//
// 보안: 모든 요청은 누구나 스크립트로 보낼 수 있다고 보고 검사한다.
//   - 본문 크기를 읽으면서 제한한다(content-length를 믿지 않는다)
//   - 서번트·클래스·업적·출신·도시는 게임에 있는 값만 받는다(src/known.js, 빌드 때 자동 생성)
//   - 모든 /api/ 요청에 접속 주소별 속도 제한을 건다
//   - 한 기기가 하루에 보낼 수 있는 결과 수, 보낼 수 있는 조 수를 제한한다
//   - 신고는 서로 다른 접속 주소 3곳에서 와야 숨김 처리된다
import { KNOWN } from './known.js';

const json = (data, status = 200, extra = {}) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', 'x-content-type-options': 'nosniff', ...extra },
  });

const HEROES = KNOWN.heroes, ACH = new Set(KNOWN.ach), ORIGINS = new Set(KNOWN.origins), CITIES = new Set(KNOWN.cities);
const heroOk = h => (typeof h === 'string' && Object.prototype.hasOwnProperty.call(HEROES, h) ? h : null);

// 본문을 읽으면서 크기를 센다. 넘으면 그 자리에서 멈춘다.
async function readJson(request, max) {
  if (!request.body) return null;
  const reader = request.body.getReader();
  const chunks = []; let size = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > max) { try { await reader.cancel(); } catch {} throw new TooBig(); }
    chunks.push(value);
  }
  const buf = new Uint8Array(size); let o = 0;
  for (const c of chunks) { buf.set(c, o); o += c.byteLength; }
  try { return JSON.parse(new TextDecoder().decode(buf)); } catch { return null; }
}
class TooBig extends Error {}

const ipOf = request => request.headers.get('cf-connecting-ip') || 'x';
// 접속 주소별 속도 제한(분당 20번). 종류마다 따로 센다.
async function slowDown(env, request, kind) {
  if (!env.RL) return false;
  const { success } = await env.RL.limit({ key: kind + ':' + ipOf(request) });
  return !success;
}
const SLOW = () => json({ ok: false, error: 'slow_down' }, 429);

const SCHEMA = [
  `CREATE TABLE IF NOT EXISTS lives (
     id TEXT PRIMARY KEY, ts INTEGER NOT NULL, dev TEXT NOT NULL, lang TEXT,
     hero TEXT, cls TEXT, ending TEXT NOT NULL, cup TEXT, city TEXT, origin TEXT, circuit INTEGER, age INTEGER)`,
  `CREATE INDEX IF NOT EXISTS lives_hero ON lives(hero)`,
  `CREATE TABLE IF NOT EXISTS devices (dev TEXT PRIMARY KEY, first INTEGER NOT NULL, last INTEGER NOT NULL, lives INTEGER NOT NULL DEFAULT 0)`,
  `CREATE TABLE IF NOT EXISTS dev_ach (dev TEXT NOT NULL, ach TEXT NOT NULL, PRIMARY KEY (dev, ach))`,
  `CREATE TABLE IF NOT EXISTS ghosts (
     id TEXT PRIMARY KEY, dev TEXT NOT NULL, created INTEGER NOT NULL, year INTEGER NOT NULL,
     hero TEXT NOT NULL, cls TEXT NOT NULL, lang TEXT, data TEXT NOT NULL,
     shown INTEGER NOT NULL DEFAULT 0, reports INTEGER NOT NULL DEFAULT 0, hidden INTEGER NOT NULL DEFAULT 0)`,
  `CREATE INDEX IF NOT EXISTS ghosts_year ON ghosts(year)`,
  `CREATE TABLE IF NOT EXISTS ghost_reports (id TEXT NOT NULL, dev TEXT NOT NULL, ts INTEGER NOT NULL, PRIMARY KEY (id, dev))`,
  `CREATE INDEX IF NOT EXISTS lives_dev ON lives(dev, ts)`,
  `CREATE INDEX IF NOT EXISTS lives_ts ON lives(ts)`,
  `CREATE INDEX IF NOT EXISTS ghosts_dev ON ghosts(dev)`,
  `CREATE TABLE IF NOT EXISTS ghost_seen (id TEXT NOT NULL, dev TEXT NOT NULL, ts INTEGER NOT NULL, PRIMARY KEY (id, dev))`,
  `CREATE TABLE IF NOT EXISTS ghost_flags (id TEXT NOT NULL, who TEXT NOT NULL, dev TEXT, ts INTEGER NOT NULL, PRIMARY KEY (id, who))`,
  `CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS ghost_results (
     id TEXT NOT NULL, dev TEXT NOT NULL, owner TEXT NOT NULL, ts INTEGER NOT NULL,
     year INTEGER NOT NULL, city TEXT, join_day INTEGER NOT NULL, ending TEXT NOT NULL, out_day INTEGER, tod TEXT, by_who TEXT, ally INTEGER NOT NULL DEFAULT 0,
     name TEXT, hero TEXT, cls TEXT, sent_year INTEGER, sent_city TEXT, PRIMARY KEY (id, dev))`,
  `CREATE INDEX IF NOT EXISTS ghost_results_owner ON ghost_results(owner, ts)`,
  // 검은 성배 루트를 치른 생만 따로 남긴다(보스 밸런스 점검용). lives와 같은 id.
  `CREATE TABLE IF NOT EXISTS cx_lives (
     id TEXT PRIMARY KEY, ts INTEGER NOT NULL, dev TEXT NOT NULL, hero TEXT, cls TEXT,
     cx_end TEXT NOT NULL, by_who TEXT NOT NULL, fate TEXT NOT NULL, mode TEXT, st INTEGER, comp INTEGER, tries INTEGER, sk INTEGER, day INTEGER)`,
  `CREATE INDEX IF NOT EXISTS cx_lives_ts ON cx_lives(ts)`,
  // 기기 연결: gid = 비밀 키의 SHA-256. data = 기기가 압축해 보낸 기록 묶음(서버는 열어 보지 않는다)
  `CREATE TABLE IF NOT EXISTS sync_groups (gid TEXT PRIMARY KEY, ver INTEGER NOT NULL, ts INTEGER NOT NULL, seen INTEGER NOT NULL, devs INTEGER NOT NULL, size INTEGER NOT NULL, data TEXT NOT NULL)`,
  `CREATE INDEX IF NOT EXISTS sync_groups_seen ON sync_groups(seen)`,
  `CREATE TABLE IF NOT EXISTS sync_codes (code TEXT PRIMARY KEY, gid TEXT NOT NULL, key TEXT NOT NULL, exp INTEGER NOT NULL)`,
  // 연결된 기기 하나하나: did = 그 기기만 가진 출입증(dk)의 SHA-256, pid = 목록에서 고를 때 쓰는 짧은 번호,
  // name = 직접 붙인 이름, lbl = 기기 종류(예: 'iPhone · Safari'), first = 연결한 때, seen = 마지막으로 맞춘 때
  `CREATE TABLE IF NOT EXISTS sync_devs (did TEXT PRIMARY KEY, gid TEXT NOT NULL, pid TEXT NOT NULL, name TEXT NOT NULL DEFAULT '', lbl TEXT NOT NULL DEFAULT '', first INTEGER NOT NULL, seen INTEGER NOT NULL)`,
  `CREATE INDEX IF NOT EXISTS sync_devs_gid ON sync_devs(gid)`,
  // 통계 스냅숏: 합친 결과를 한 줄로 남겨 둔다. busy = 지금 다시 세고 있는 요청이 잡은 시각
  `CREATE TABLE IF NOT EXISTS stats_snap (k TEXT PRIMARY KEY, at INTEGER NOT NULL, busy INTEGER NOT NULL DEFAULT 0, body TEXT NOT NULL)`,
  // 11-22: 전체 통계용 누적 수. 트리거가 lives · dev_ach에 줄이 들어갈 때마다 더한다(처음 한 번만 CNT_SETUP이 채움)
  `CREATE TABLE IF NOT EXISTS c_tot (k TEXT PRIMARY KEY, v INTEGER NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS c_hero (hero TEXT PRIMARY KEY, n INTEGER NOT NULL, g INTEGER NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS c_end (ending TEXT PRIMARY KEY, n INTEGER NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS c_cup (cup TEXT PRIMARY KEY, n INTEGER NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS c_ach (ach TEXT PRIMARY KEY, n INTEGER NOT NULL)`,
  // 11-23: 검은 성배 집계 누적 수(빈 값은 '' · -1로 두어 같은 줄로 묶이게 한다)
  `CREATE TABLE IF NOT EXISTS c_cxr (cx_end TEXT NOT NULL, by_who TEXT NOT NULL, fate TEXT NOT NULL, comp INTEGER NOT NULL, mode TEXT NOT NULL, n INTEGER NOT NULL, tr INTEGER NOT NULL, PRIMARY KEY (cx_end, by_who, fate, comp, mode))`,
  `CREATE TABLE IF NOT EXISTS c_cxc (cls TEXT NOT NULL, mode TEXT NOT NULL, n INTEGER NOT NULL, me INTEGER NOT NULL, alive INTEGER NOT NULL, PRIMARY KEY (cls, mode))`,
];
// 스키마 준비: 한 번 끝나면 표시만 남긴다. 준비 중인 promise를 여러 요청이 나눠 기다리면, 그 promise를 만든 요청이
// 먼저 끝났을 때 나머지가 'This promise was created by a request that has since ended'로 실패하므로 요청마다 직접 기다린다.
// (처음 켜질 때 몇 요청이 같이 돌려도 CREATE ... IF NOT EXISTS라 괜찮다)
let schemaOk = false;
const ensureSchema = async env => {
  if (schemaOk) return;
  await env.DB.batch(SCHEMA.map(s => env.DB.prepare(s)));
  schemaOk = true;
};

const ENDINGS = new Set(['shared', 'victor', 'lost', 'survived', 'collapsed', 'withdrew', 'refused', 'dead', 'none']);
const ID = /^[A-Za-z0-9_-]{1,40}$/;
// 검은 성배 결과: 결말 · 보스를 쓰러뜨린 쪽 · 내 서번트의 끝
const CX_END = new Set(['seal', 'key', 'break', 'claim', 'flood', 'npcBreak', 'npcClaim', 'none']);
const CX_BY = new Set(['me', 'npc', 'none']);
const CX_MODE = new Set(['nat', 'always']); // 시나리오 설정: 자연 발생 · 항상
const CX_FATE = new Set(['alive', 'boss', 'shadow', 'fight', 'swallow', 'defect', 'keyGone', 'other']);
function cxOk(c) {
  if (!c || typeof c !== 'object') return null;
  const end = CX_END.has(c.end) ? c.end : null, by = CX_BY.has(c.by) ? c.by : null, fate = CX_FATE.has(c.fate) ? c.fate : null;
  if (!end || !by || !fate) return null;
  return { end, by, fate, mode: CX_MODE.has(c.mode) ? c.mode : 'nat', st: int(c.st, 0, 3), comp: int(c.comp, 0, 6), tries: int(c.tries, 0, 60), sk: int(c.sk, 0, 30), day: int(c.day, 0, 30) };
}               // 서번트·업적·클래스·출신 같은 내부 이름
const str = (v, re) => (typeof v === 'string' && re.test(v) ? v : null);
const int = (v, lo, hi) => (Number.isInteger(v) && v >= lo && v <= hi ? v : null);

async function postLife(request, env) {
  if (await slowDown(env, request, 'l')) return SLOW();
  const b = await readJson(request, 8000);
  if (!b) return json({ ok: false, error: 'bad_json' }, 400);
  if (b.v !== 1) return json({ ok: false, error: 'bad_version' }, 400);

  const id = str(b.life, ID), dev = str(b.dev, ID), ending = ENDINGS.has(b.end) ? b.end : null;
  if (!id || !dev || !ending) return json({ ok: false, error: 'bad_fields' }, 400);
  const hero = heroOk(b.hero), cls = hero && b.cls === HEROES[hero] ? b.cls : null;
  const cup = b.cup === 'pure' || b.cup === 'dark' ? b.cup : null;
  const lang = ['ko', 'en', 'ja'].includes(b.lang) ? b.lang : null;
  const ach = Array.isArray(b.ach) ? [...new Set(b.ach.filter(a => typeof a === 'string' && ACH.has(a)))] : [];
  const city = typeof b.city === 'string' && CITIES.has(b.city) ? b.city : null;
  const origin = typeof b.origin === 'string' && ORIGINS.has(b.origin) ? b.origin : null;
  const now = Date.now();

  await ensureSchema(env);
  // 한 기기가 하루에 보낼 수 있는 결과는 150개까지
  const day = await env.DB.prepare(`SELECT COUNT(*) AS n FROM lives WHERE dev = ? AND ts > ?`).bind(dev, now - 864e5).first();
  if (day && day.n >= 150) return json({ ok: false, error: 'too_many' }, 429);
  const ins = await env.DB.prepare(
    `INSERT OR IGNORE INTO lives (id, ts, dev, lang, hero, cls, ending, cup, city, origin, circuit, age)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
  ).bind(id, now, dev, lang, hero, hero ? cls : null, ending, cup, city, origin, int(b.circuit, 0, 9), int(b.age, 0, 150)).run();
  const fresh = ins.meta && ins.meta.changes > 0;
  const cx = hero ? cxOk(b.cx) : null;

  const stmts = [
    env.DB.prepare(
      `INSERT INTO devices (dev, first, last, lives) VALUES (?, ?, ?, ?)
       ON CONFLICT(dev) DO UPDATE SET last = excluded.last, lives = devices.lives + excluded.lives`
    ).bind(dev, now, now, fresh ? 1 : 0),
    // 업적은 한 문장으로 넣는다 (11-23: 업적마다 한 문장씩이라 한 판에 평균 60개, 전체 쿼리의 절반이 이것이었다 → D1 overloaded)
    ...(ach.length ? [env.DB.prepare(`INSERT OR IGNORE INTO dev_ach (dev, ach) SELECT ?1, value FROM json_each(?2)`).bind(dev, JSON.stringify(ach))] : []),
  ];
  if (cx && fresh) stmts.push(env.DB.prepare(
    `INSERT OR IGNORE INTO cx_lives (id, ts, dev, hero, cls, cx_end, by_who, fate, mode, st, comp, tries, sk, day) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
  ).bind(id, now, dev, hero, cls, cx.end, cx.by, cx.fate, cx.mode, cx.st, cx.comp, cx.tries, cx.sk, cx.day));
  await env.DB.batch(stmts);
  return json({ ok: true, fresh });
}


// 11월 1일 배포 전까지 허용 목록에 빠져 있던 새 서번트 17명. 그동안 보낸 생은 서번트 칸이 빈 채 저장됐다.
// 같은 기기가 보낸 같은 생이고, 서번트 칸이 비어 있고, 전쟁을 치른 생이고, 그 기간에 저장된 기록만 고친다. 새 기록은 더하지 않는다.
const FIXABLE = new Set(['baobhan', 'barghest', 'melusine', 'muramasa', 'ishtar', 'ereshkigal', 'lanling', 'habetrot', 'quetzalcoatl', 'kama', 'sheba', 'asclepius', 'constantine', 'huyan', 'lilith', 'yuyoku', 'nameless']);
const FIX_BEFORE = Date.UTC(2026, 10, 2, 15, 0, 0);
async function fixLives(request, env) {
  if (await slowDown(env, request, 'f')) return SLOW();
  const b = await readJson(request, 6000);
  const dev = str(b && b.dev, ID);
  if (!b || b.v !== 1 || !dev || !Array.isArray(b.list)) return json({ ok: false, error: 'bad_fields' }, 400);
  const list = b.list.slice(0, 60).map(x => {
    const id = str(x && x.life, ID), hero = heroOk(x && x.hero);
    return id && hero && FIXABLE.has(hero) ? [id, hero, HEROES[hero]] : null;
  }).filter(Boolean);
  if (!list.length) return json({ ok: true, fixed: 0 });
  await ensureSchema(env);
  const rs = await env.DB.batch(list.map(([id, hero, cls]) => env.DB.prepare(
    `UPDATE lives SET hero = ?, cls = ? WHERE id = ? AND dev = ? AND hero IS NULL AND ending != 'none' AND ts < ?`
  ).bind(hero, cls, id, dev, FIX_BEFORE)));
  return json({ ok: true, fixed: rs.reduce((a, r) => a + ((r.meta && r.meta.changes) || 0), 0) });
}

// ---- 다른 겨울에서 온 조 ----
// A가 살아남은 조를 보내고(POST /api/ghost), B의 전쟁이 열릴 때 1~40년 앞선 전쟁의 조를 받아 간다(GET /api/ghost).
const NAME_OK = /^[0-9A-Za-z가-힣ぁ-んァ-ヶー一-龯 .·'-]{1,20}$/;
const BAD = ['씨발', '시발', 'ㅅㅂ', '병신', 'ㅂㅅ', '좆', '존나', '개새', '새끼', '니미', '느금', '애미', '애비', '섹스', '보지', '자지', '창녀', '걸레', '장애인', '틀딱', '한남', '김치녀', '일베',
  'fuck', 'shit', 'bitch', 'cunt', 'dick', 'pussy', 'nigg', 'fag', 'rape', 'nazi', 'hitler', 'porn', 'sex',
  'ちんこ', 'まんこ', 'セックス', '死ね', 'きちがい', 'ガイジ'];
const badName = n => { const t = n.toLowerCase().replace(/[\s.·'-]/g, ''); return BAD.some(w => t.includes(w)); };
const GHOST_ENDS = new Set(['victor', 'shared', 'survived', 'withdrew']);
const TACS = new Set(['proud', 'hunter', 'cunning', 'defensive', 'naive', 'reckless', 'desperate']);

function cleanGhost(b) {
  const name = typeof b.name === 'string' ? b.name.trim().replace(/\s+/g, ' ') : '';
  if (!NAME_OK.test(name)) return [null, 'bad_name'];
  if (badName(name)) return [null, 'name_blocked'];
  const hero = heroOk(b.hero), cls = hero && b.cls === HEROES[hero] ? b.cls : null, year = int(b.year, 1900, 2140);
  if (!hero || !cls || !year || !GHOST_ENDS.has(b.end)) return [null, 'bad_fields'];
  const know = Array.isArray(b.know) ? [...new Map(b.know.slice(0, 12).filter(k => k && heroOk(k.h) && k.h !== hero).map(k => [k.h, k])).values()].slice(0, 8).map(k => ({
    h: k.h, n: k.n ? 1 : 0, a: k.a ? 1 : 0, f: k.f ? 1 : 0, k: k.k ? 1 : 0, al: k.al ? 1 : 0,
  })) : [];
  return [{
    name, hero, cls, year, end: b.end,
    sex: b.sex === 'f' ? 'f' : 'm',
    age: int(b.age, 10, 90) ?? 25,
    city: typeof b.city === 'string' && CITIES.has(b.city) ? b.city : '',
    circuit: int(b.circuit, 0, 9) ?? 0,
    trust: int(b.trust, 0, 100) ?? 50,
    bond: int(b.bond, 0, 200) ?? 50,
    kills: int(b.kills, 0, 9) ?? 0,
    n: int(b.n, 1, 1e6),
    seals: int(b.seals, 0, 3) ?? 0,
    pw: int(b.pw, 40, 95) ?? 70,
    tac: TACS.has(b.tac) ? b.tac : 'defensive',
    know,
  }, null];
}

async function postGhost(request, env) {
  if (await slowDown(env, request, 'g')) return SLOW();
  const b = await readJson(request, 6000);
  if (!b) return json({ ok: false, error: 'bad_json' }, 400);
  const dev = str(b.dev, ID);
  if (b.v !== 1 || !dev) return json({ ok: false, error: 'bad_fields' }, 400);
  const [g, err] = cleanGhost(b);
  if (!g) return json({ ok: false, error: err }, 400);
  await ensureSchema(env);
  const mine = await env.DB.prepare(`SELECT COUNT(*) AS n FROM ghosts WHERE dev = ?`).bind(dev).first();
  if (mine && mine.n >= 30) return json({ ok: false, error: 'too_many' }, 429);
  const id = 'g' + crypto.randomUUID().replace(/-/g, '').slice(0, 20);
  const lang = ['ko', 'en', 'ja'].includes(b.lang) ? b.lang : null;
  await env.DB.prepare(`INSERT INTO ghosts (id, dev, created, year, hero, cls, lang, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`)
    .bind(id, dev, Date.now(), g.year, g.hero, g.cls, lang, JSON.stringify(g)).run();
  return json({ ok: true, id });
}

// 유령 후보: 조 id는 무작위 글자라 id 순서가 곧 섞인 순서다. 무작위 위치에서 시작해 id 순서로 GH_N개를 읽는다
// (예전 ORDER BY random()은 조건에 맞는 조를 모두 읽고 섞었다). +year: 연도 색인 대신 id 색인을 타게 한다.
// 11-25: 읽은 후보는 연도마다 1분 동안 메모리에 둔다. 같은 promise를 요청끼리 나눠 기다리지 않는다(11-17 수정 2와 같은 까닭) — 동시에 비면 각자 읽는다
const GH_N = 48, GH_TTL = 60e3, GH_KEYS = 64, GH_POOL = new Map();
async function ghostPool(env, year) {
  const now = Date.now(), c = GH_POOL.get(year);
  if (c && now - c.at < GH_TTL) return c.list;
  const pivot = 'g' + crypto.randomUUID().replace(/-/g, '').slice(0, 20);
  const pick = op => env.DB.prepare(
    `SELECT id, dev, data FROM ghosts WHERE id ${op} ? AND hidden = 0 AND +year BETWEEN ? AND ? ORDER BY id LIMIT ${GH_N}`
  ).bind(pivot, year - 40, year - 1).all();
  let { results } = await pick('>=');
  if (results.length < GH_N) {   // 끝에 닿으면 처음부터 이어서
    // 11-23: 조가 드문 연도대에서는 처음부터 id 순으로 훑으면 표 대부분(수만 줄, 0.5~0.8초)을 읽어 D1을 막았다.
    // pivot 뒤 구간(f)에서 찾은 수로 전체를 어림해, 드물면 연도 색인으로 그 연도대만 읽는다
    const f = 1 - parseInt(pivot.slice(1, 9), 16) / 2 ** 32, est = f > 0.02 ? results.length / f : 0;
    const rest = est < 3000
      ? await env.DB.prepare(`SELECT id, dev, data FROM ghosts INDEXED BY ghosts_year WHERE year BETWEEN ? AND ? AND id < ? AND hidden = 0 ORDER BY id LIMIT ${GH_N}`)
          .bind(year - 40, year - 1, pivot).all()
      : await pick('<');
    results = results.concat(rest.results).slice(0, GH_N);
  }
  GH_POOL.delete(year); GH_POOL.set(year, { at: now, list: results });
  while (GH_POOL.size > GH_KEYS) GH_POOL.delete(GH_POOL.keys().next().value);   // 오래 안 쓴 연도부터 비운다
  return results;
}

async function getGhost(request, url, env) {
  if (await slowDown(env, request, 'q')) return SLOW();
  const year = int(Number(url.searchParams.get('year')), 1900, 2140);
  const dev = str(url.searchParams.get('dev'), ID) || '-';
  if (!year) return json({ ok: false, error: 'bad_year' }, 400);
  await ensureSchema(env);
  // 11-25: 연도마다 후보(GH_N개)를 이 서버(isolate) 메모리에 1분 동안 두고, 그 안에서 자기 조를 빼고 4개를 고른다
  //   (예전: 요청마다 DB에서 12개를 읽었다 — 하루 112만 번, D1 실행 시간의 32%)
  const pool = await ghostPool(env, year);
  const cand = pool.filter(r => r.dev !== dev);
  for (let i = cand.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [cand[i], cand[j]] = [cand[j], cand[i]]; }
  const list = cand.slice(0, 4).map(r => ({ id: r.id, ...JSON.parse(r.data) }));
  return json({ ok: true, list });
}

async function ghostShown(request, env) {
  if (await slowDown(env, request, 's')) return SLOW();
  const b = await readJson(request, 500);
  const id = str(b && b.id, ID), dev = str(b && b.dev, ID);
  if (!id || !dev) return json({ ok: false, error: 'bad_fields' }, 400);
  await ensureSchema(env);
  // 같은 기기에서 같은 조는 한 번만 센다
  const r = await env.DB.prepare(`INSERT OR IGNORE INTO ghost_seen (id, dev, ts) SELECT id, ?, ? FROM ghosts WHERE id = ?`).bind(dev, Date.now(), id).run();
  if (r.meta && r.meta.changes > 0) await env.DB.prepare(`UPDATE ghosts SET shown = shown + 1 WHERE id = ?`).bind(id).run();
  return json({ ok: true });
}

async function withdrawGhost(request, env) {
  if (await slowDown(env, request, 'w')) return SLOW();
  const b = await readJson(request, 500);
  const id = str(b && b.id, ID), dev = str(b && b.dev, ID);
  if (!id || !dev) return json({ ok: false, error: 'bad_fields' }, 400);
  await ensureSchema(env);
  const r = await env.DB.prepare(`DELETE FROM ghosts WHERE id = ? AND dev = ?`).bind(id, dev).run();
  return json({ ok: true, removed: (r.meta && r.meta.changes) || 0 });
}

// 접속 주소를 서버만 아는 무작위 값과 섞어 되돌릴 수 없는 짧은 값으로 바꾼다(신고 중복 확인용)
// (값만 기억한다 — 위 ensureSchema와 같은 까닭으로 promise를 요청끼리 나눠 기다리지 않는다)
let saltV = null;
const salt = async env => {
  if (saltV) return saltV;
  const rnd = [...crypto.getRandomValues(new Uint8Array(24))].map(x => x.toString(16).padStart(2, '0')).join('');
  await env.DB.prepare(`INSERT OR IGNORE INTO meta (k, v) VALUES ('salt', ?)`).bind(rnd).run();
  const row = await env.DB.prepare(`SELECT v FROM meta WHERE k = 'salt'`).first();
  return (saltV = row.v);
};
async function whoKey(env, request) {
  const data = new TextEncoder().encode((await salt(env)) + '|' + ipOf(request));
  const h = new Uint8Array(await crypto.subtle.digest('SHA-256', data));
  return [...h.slice(0, 8)].map(x => x.toString(16).padStart(2, '0')).join('');
}

async function reportGhost(request, env) {
  if (await slowDown(env, request, 'r')) return SLOW();
  const b = await readJson(request, 500);
  const id = str(b && b.id, ID), dev = str(b && b.dev, ID);
  if (!id || !dev) return json({ ok: false, error: 'bad_fields' }, 400);
  await ensureSchema(env);
  const who = await whoKey(env, request);
  const r = await env.DB.prepare(`INSERT OR IGNORE INTO ghost_flags (id, who, dev, ts) SELECT id, ?, ?, ? FROM ghosts WHERE id = ?`).bind(who, dev, Date.now(), id).run();
  if (r.meta && r.meta.changes > 0) {
    // 서로 다른 접속 주소 3곳에서 신고가 오면 숨긴다
    await env.DB.prepare(`UPDATE ghosts SET reports = (SELECT COUNT(*) FROM ghost_flags WHERE ghost_flags.id = ghosts.id),
                            hidden = CASE WHEN (SELECT COUNT(*) FROM ghost_flags WHERE ghost_flags.id = ghosts.id) >= 3 THEN 1 ELSE hidden END
                          WHERE id = ?`).bind(id).run();
  }
  return json({ ok: true });
}

// 그 조가 끼어든 전쟁의 결과. 실제로 그 조를 만난 기기(ghost_seen)만, 조마다 한 번 보낼 수 있다.
const RESULT_ENDS = new Set(['win', 'shared', 'alive', 'out']);
async function ghostResult(request, env) {
  if (await slowDown(env, request, 'x')) return SLOW();
  const b = await readJson(request, 800);
  const id = str(b && b.id, ID), dev = str(b && b.dev, ID);
  if (!id || !dev || !RESULT_ENDS.has(b.end)) return json({ ok: false, error: 'bad_fields' }, 400);
  const year = int(b.year, 1900, 2140), join = int(b.join, 1, 14);
  const out = b.end === 'out', day = out ? int(b.day, 1, 14) : null;
  if (!year || !join || (out && (!day || day < join))) return json({ ok: false, error: 'bad_fields' }, 400);
  const tod = out && ['낮', '밤', '새벽'].includes(b.tod) ? b.tod : null;
  const by = out && ['me', 'other', 'none'].includes(b.by) ? b.by : null;
  const city = typeof b.city === 'string' && CITIES.has(b.city) ? b.city : '';
  await ensureSchema(env);
  const g = await env.DB.prepare(`SELECT g.dev AS owner, g.year AS year, g.data AS data FROM ghosts g JOIN ghost_seen s ON s.id = g.id AND s.dev = ? WHERE g.id = ?`).bind(dev, id).first();
  if (!g) return json({ ok: false, error: 'not_seen' }, 404);
  if (year <= g.year || year > g.year + 40) return json({ ok: false, error: 'bad_fields' }, 400);
  const d = JSON.parse(g.data);
  await env.DB.prepare(`INSERT OR IGNORE INTO ghost_results (id, dev, owner, ts, year, city, join_day, ending, out_day, tod, by_who, ally, name, hero, cls, sent_year, sent_city)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`)
    .bind(id, dev, g.owner, Date.now(), year, city, join, b.end, day, tod, by, b.ally ? 1 : 0, d.name, d.hero, d.cls, d.year, d.city || '').run();
  return json({ ok: true });
}

// 보낸 기기가 자기 조들의 소식을 받아 간다. 기기 번호는 주소에 남지 않도록 본문으로 받는다.
async function ghostNews(request, env) {
  if (await slowDown(env, request, 'n')) return SLOW();
  const b = await readJson(request, 300);
  const dev = str(b && b.dev, ID);
  if (!dev) return json({ ok: false, error: 'bad_fields' }, 400);
  // 연결된 기기들이 보낸 조의 소식도 함께(기기 번호 최대 8개)
  const devs = [...new Set([dev, ...(Array.isArray(b.devs) ? b.devs : []).map(d => str(d, ID)).filter(Boolean)])].slice(0, 8);
  await ensureSchema(env);
  const { results } = await env.DB.prepare(
    `SELECT id, ts, year, city, join_day, ending, out_day, tod, by_who, ally, name, hero, cls, sent_year, sent_city
       FROM ghost_results WHERE owner IN (${devs.map(() => '?').join(',')}) ORDER BY ts DESC LIMIT 200`).bind(...devs).all();
  const list = results.map(r => ({ id: r.id, ts: r.ts, year: r.year, city: r.city || '', join: r.join_day, end: r.ending, day: r.out_day, tod: r.tod,
    by: r.by_who, ally: !!r.ally, name: r.name, hero: r.hero, cls: r.cls, sentYear: r.sent_year, sentCity: r.sent_city || '' }));
  return json({ ok: true, list });
}

// 보낸 기기(와 연결된 기기, 최대 8개)가 아직 거두지 않은 조. 지난 생 기록이 기기에서 밀려나도 이 목록으로 거둘 수 있다.
async function ghostMine(request, env) {
  if (await slowDown(env, request, 'm')) return SLOW();
  const b = await readJson(request, 300);
  const dev = str(b && b.dev, ID);
  if (!dev) return json({ ok: false, error: 'bad_fields' }, 400);
  const devs = [...new Set([dev, ...(Array.isArray(b.devs) ? b.devs : []).map(d => str(d, ID)).filter(Boolean)])].slice(0, 8);
  await ensureSchema(env);
  const { results } = await env.DB.prepare(
    `SELECT id, dev, created, hidden, data FROM ghosts WHERE dev IN (${devs.map(() => '?').join(',')}) ORDER BY created DESC LIMIT 300`).bind(...devs).all();
  const list = results.map(r => { let d = {}; try { d = JSON.parse(r.data) || {}; } catch (e) {}
    return { id: r.id, dev: r.dev, at: r.created, hidden: !!r.hidden, name: d.name || '', hero: d.hero, cls: d.cls, year: d.year, city: d.city || '', n: d.n || null }; });
  return json({ ok: true, list, max: 30 });
}

// ---- 기기 연결 ----
const SYNC_KEY = /^[A-Za-z0-9_-]{32,64}$/, SYNC_DATA = /^[zj]:/, SYNC_MAX = 1_400_000, SYNC_DEVS = 5;
const SYNC_ABC = '23456789ABCDEFGHJKMNPQRSTUVWXYZ'; // 헷갈리는 0·O·1·I·L은 뺀다
const SYNC_TTL = 180 * 864e5, CODE_TTL = 10 * 60e3;
const b64u = a => btoa(String.fromCharCode(...a)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
async function gidOf(key) { const h = new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(key))); return b64u(h); }
function syncCode() { const out = []; while (out.length < 8) { const r = crypto.getRandomValues(new Uint8Array(16)); for (const x of r) if (x < 248 && out.length < 8) out.push(SYNC_ABC[x % 31]); } return out.join(''); }
const syncData = z => (typeof z === 'string' && SYNC_DATA.test(z) && z.length <= SYNC_MAX ? z : null);
// 11-25: 출입증(dk)을 함께 주면 그 기기 줄도 같은 쿼리로 읽는다(dj) — 예전에는 묶음 조회 · 기기 조회를 따로 2번 했다(하루 각 500만 번)
async function syncLite(env, key, dk) { if (!str(key, SYNC_KEY)) return null; const gid = await gidOf(key);
  if (!str(dk, SYNC_DK)) return await env.DB.prepare(`SELECT gid, ver, seen, devs FROM sync_groups WHERE gid = ?`).bind(gid).first(); // 기록 묶음(data) 없이
  const r = await env.DB.prepare(`SELECT g.gid, g.ver, g.seen, g.devs, d.did, d.pid, d.lbl, d.seen AS dseen FROM sync_groups g LEFT JOIN sync_devs d ON d.did = ? AND d.gid = g.gid WHERE g.gid = ?`).bind(await gidOf(dk), gid).first();
  if (!r) return null;
  return { gid: r.gid, ver: r.ver, seen: r.seen, devs: r.devs, dj: { dk, d: r.did ? { did: r.did, pid: r.pid, lbl: r.lbl, seen: r.dseen } : null } }; }
async function syncGroup(env, key) { if (!str(key, SYNC_KEY)) return null; const gid = await gidOf(key); const g = await env.DB.prepare(`SELECT gid, ver, seen, devs, data FROM sync_groups WHERE gid = ?`).bind(gid).first(); return g; }
const SYNC_DK = /^[A-Za-z0-9_-]{32}$/;
const devTxt = (v, n) => (typeof v === 'string' ? v.replace(/[\u0000-\u001f\u007f<>]/g, '').replace(/\s+/g, ' ').trim().slice(0, n) : '');
async function devAdd(env, gid, lbl, now) {
  const dk = b64u(crypto.getRandomValues(new Uint8Array(24)));
  await env.DB.prepare(`INSERT INTO sync_devs (did, gid, pid, name, lbl, first, seen) VALUES (?, ?, ?, '', ?, ?, ?)`)
    .bind(await gidOf(dk), gid, b64u(crypto.getRandomValues(new Uint8Array(6))), devTxt(lbl, 40), now, now).run();
  return dk;
}
const devCount = async (env, gid) => ((await env.DB.prepare(`SELECT COUNT(*) AS n FROM sync_devs WHERE gid = ?`).bind(gid).first()) || {}).n || 0;
// 기기 확인. 출입증(dk)을 내면 그 기기 줄이 있어야 한다(없으면 끊긴 기기).
// 출입증이 없으면 업데이트 전에 연결된 기기: 확인되지 않은 자리(devs − 기기 줄 수)가 남아 있을 때만 받는다.
//   reg(새 화면)면 그 자리를 출입증으로 바꿔 주고, reg가 없으면(옛 화면) 출입증 없이 그대로 받는다.
//   자리가 없으면 새 화면에는 'kicked', 옛 화면에는 'gone'(옛 화면은 gone이면 연결을 지운다)
async function syncAuth(env, b, g) {
  const now = Date.now();
  if (b.dk !== undefined) {
    if (!str(b.dk, SYNC_DK)) return { err: 'kicked' };
    const d = g.dj && g.dj.dk === b.dk ? g.dj.d   // syncLite가 같은 쿼리로 읽어 둔 기기 줄
      : await env.DB.prepare(`SELECT did, pid, lbl, seen FROM sync_devs WHERE did = ? AND gid = ?`).bind(await gidOf(b.dk), g.gid).first();
    if (!d) return { err: 'kicked' };
    const lbl = devTxt(b.lbl, 40);
    if (now - d.seen > 36e5 || (lbl && lbl !== d.lbl)) await env.DB.prepare(`UPDATE sync_devs SET seen = ?, lbl = CASE WHEN ? <> '' THEN ? ELSE lbl END WHERE did = ?`).bind(now, lbl, lbl, d.did).run();
    return { d };
  }
  if (g.devs - await devCount(env, g.gid) <= 0) return { err: b.reg ? 'kicked' : 'gone' };
  if (b.reg) return { dk: await devAdd(env, g.gid, b.lbl, now) };
  return {};
}
const authFail = a => json({ ok: false, error: a.err }, a.err === 'kicked' ? 403 : 404);
async function syncTouch(env, g) { const now = Date.now(); if (now - g.seen > 864e5) await env.DB.prepare(`UPDATE sync_groups SET seen = ? WHERE gid = ?`).bind(now, g.gid).run(); }

// 11-25: 오래된 묶음 · 코드 · 끊긴 기기 줄 정리는 1시간에 한 번만 (예전: 새 연결마다 — 하루 5천 번, 한 번에 0.1 ~ 0.18초씩 D1을 잡아 다른 요청이 밀려 실패)
// meta의 sync_clean 시각을 먼저 잡은 한 요청만 지운다. 이 서버(isolate)가 한 시간 안에 이미 확인했으면 DB도 보지 않는다
const SYNC_CLEAN = 36e5; let syncCleanAt = 0;
async function syncClean(env, now) {
  if (now - syncCleanAt < SYNC_CLEAN) return; syncCleanAt = now;
  const c = await env.DB.prepare(`INSERT INTO meta (k, v) VALUES ('sync_clean', ?) ON CONFLICT(k) DO UPDATE SET v = excluded.v WHERE CAST(meta.v AS INTEGER) < ?`).bind(String(now), now - SYNC_CLEAN).run();
  if (!(c.meta && c.meta.changes > 0)) return;
  await env.DB.batch([env.DB.prepare(`DELETE FROM sync_groups WHERE seen < ?`).bind(now - SYNC_TTL), env.DB.prepare(`DELETE FROM sync_codes WHERE exp < ?`).bind(now),
    env.DB.prepare(`DELETE FROM sync_devs WHERE gid NOT IN (SELECT gid FROM sync_groups)`)]);
}
async function syncNew(request, env) {
  if (await slowDown(env, request, 's')) return SLOW();
  const b = await readJson(request, 1_500_000); const z = syncData(b && b.z);
  if (!z) return json({ ok: false, error: 'bad_fields' }, 400);
  await ensureSchema(env);
  const now = Date.now();
  await syncClean(env, now);
  const key = b64u(crypto.getRandomValues(new Uint8Array(24))), gid = await gidOf(key);
  await env.DB.prepare(`INSERT INTO sync_groups (gid, ver, ts, seen, devs, size, data) VALUES (?, 1, ?, ?, 1, ?, ?)`).bind(gid, now, now, z.length, z).run();
  const dk = await devAdd(env, gid, b.lbl, now);
  return json({ ok: true, key, dk, ver: 1, devs: 1 });
}
async function syncMakeCode(request, env) {
  if (await slowDown(env, request, 's')) return SLOW();
  const b = await readJson(request, 400);
  await ensureSchema(env);
  const g = await syncLite(env, b && b.key, b && b.dk);
  if (!g) return json({ ok: false, error: 'gone' }, 404);
  const a = await syncAuth(env, b, g); if (a.err) return authFail(a);
  if (g.devs >= SYNC_DEVS) return json({ ok: false, error: 'full' }, 409);
  const now = Date.now();
  await env.DB.batch([env.DB.prepare(`DELETE FROM sync_codes WHERE gid = ? OR exp < ?`).bind(g.gid, now)]);
  for (let i = 0; i < 4; i++) {
    const code = syncCode();
    const r = await env.DB.prepare(`INSERT OR IGNORE INTO sync_codes (code, gid, key, exp) VALUES (?, ?, ?, ?)`).bind(code, g.gid, b.key, now + CODE_TTL).run();
    if (r.meta && r.meta.changes > 0) return json({ ok: true, code, exp: now + CODE_TTL, ...(a.dk ? { dk: a.dk } : {}) });
  }
  return json({ ok: false, error: 'server' }, 500);
}
async function syncJoin(request, env) {
  if (await slowDown(env, request, 'j')) return SLOW();
  const b = await readJson(request, 200);
  const code = typeof (b && b.code) === 'string' ? b.code.toUpperCase().replace(/[^0-9A-Z]/g, '') : '';
  if (code.length !== 8 || [...code].some(c => !SYNC_ABC.includes(c))) return json({ ok: false, error: 'bad_code' }, 404);
  await ensureSchema(env);
  const now = Date.now();
  const c = await env.DB.prepare(`SELECT gid, key, exp FROM sync_codes WHERE code = ?`).bind(code).first();
  if (!c || c.exp < now) return json({ ok: false, error: 'bad_code' }, 404);
  await env.DB.prepare(`DELETE FROM sync_codes WHERE code = ?`).bind(code).run(); // 한 번만
  const g = await env.DB.prepare(`SELECT gid, ver, devs, data FROM sync_groups WHERE gid = ?`).bind(c.gid).first();
  if (!g) return json({ ok: false, error: 'gone' }, 404);
  if (g.devs >= SYNC_DEVS) return json({ ok: false, error: 'full' }, 409);
  await env.DB.prepare(`UPDATE sync_groups SET devs = devs + 1, seen = ? WHERE gid = ?`).bind(now, g.gid).run();
  const dk = await devAdd(env, g.gid, b.lbl, now);
  return json({ ok: true, key: c.key, dk, ver: g.ver, z: g.data, devs: g.devs + 1 });
}
async function syncPull(request, env) {
  if (await slowDown(env, request, 'p')) return SLOW();
  const b = await readJson(request, 400);
  await ensureSchema(env);
  const g = await syncLite(env, b && b.key, b && b.dk);
  if (!g) return json({ ok: false, error: 'gone' }, 404);
  const a = await syncAuth(env, b, g); if (a.err) return authFail(a);
  await syncTouch(env, g);
  const dk = a.dk ? { dk: a.dk } : {};
  if (Number.isInteger(b.have) && b.have === g.ver) return json({ ok: true, same: true, ver: g.ver, devs: g.devs, ...dk });
  const full = await env.DB.prepare(`SELECT ver, devs, data FROM sync_groups WHERE gid = ?`).bind(g.gid).first();
  if (!full) return json({ ok: false, error: 'gone' }, 404);
  return json({ ok: true, ver: full.ver, z: full.data, devs: full.devs, ...dk });
}
async function syncPush(request, env) {
  if (await slowDown(env, request, 'u')) return SLOW();
  const b = await readJson(request, 1_500_000); const z = syncData(b && b.z);
  if (!z || !Number.isInteger(b.base) || !str(b.key, SYNC_KEY)) return json({ ok: false, error: 'bad_fields' }, 400);
  await ensureSchema(env);
  const g0 = await syncLite(env, b.key, b.dk);
  if (!g0) return json({ ok: false, error: 'gone' }, 404);
  const a = await syncAuth(env, b, g0); if (a.err) return authFail(a);
  const gid = g0.gid, now = Date.now(), dk = a.dk ? { dk: a.dk } : {};
  // 마지막으로 받은 판(base)이 서버의 최신일 때만 덮는다. 그 사이 다른 기기가 올렸으면 최신을 돌려줘 기기에서 합치게 한다.
  const r = await env.DB.prepare(`UPDATE sync_groups SET ver = ver + 1, data = ?, size = ?, ts = ?, seen = ? WHERE gid = ? AND ver = ?`).bind(z, z.length, now, now, gid, b.base).run();
  if (r.meta && r.meta.changes > 0) return json({ ok: true, ver: b.base + 1, ...dk });
  const g = await env.DB.prepare(`SELECT ver, devs, data FROM sync_groups WHERE gid = ?`).bind(gid).first();
  if (!g) return json({ ok: false, error: 'gone' }, 404);
  return json({ ok: false, error: 'conflict', ver: g.ver, z: g.data, devs: g.devs, ...dk }, 409);
}
async function syncLeave(request, env) {
  if (await slowDown(env, request, 's')) return SLOW();
  const b = await readJson(request, 400);
  if (!str(b && b.key, SYNC_KEY)) return json({ ok: false, error: 'bad_fields' }, 400);
  await ensureSchema(env);
  const g = await syncLite(env, b.key);
  if (!g) return json({ ok: true });
  const gid = g.gid;
  // 끊긴 기기(출입증 줄이 없음)나 자리가 없는 옛 기기가 나가도 남은 기기 수는 줄이지 않는다
  let mine = false;
  if (str(b.dk, SYNC_DK)) { const r = await env.DB.prepare(`DELETE FROM sync_devs WHERE did = ? AND gid = ?`).bind(await gidOf(b.dk), gid).run(); mine = !!(r.meta && r.meta.changes > 0); }
  else if (b.dk === undefined) mine = g.devs - await devCount(env, gid) > 0;
  if (!mine) return json({ ok: true });
  await env.DB.batch([env.DB.prepare(`UPDATE sync_groups SET devs = devs - 1 WHERE gid = ?`).bind(gid), env.DB.prepare(`DELETE FROM sync_groups WHERE gid = ? AND devs <= 0`).bind(gid), env.DB.prepare(`DELETE FROM sync_codes WHERE gid = ?`).bind(gid),
    env.DB.prepare(`DELETE FROM sync_devs WHERE gid = ? AND NOT EXISTS (SELECT 1 FROM sync_groups WHERE gid = ?)`).bind(gid, gid)]);
  return json({ ok: true });
}

// 연결된 기기 목록: 출입증이 있는 기기만 볼 수 있다. unk = 아직 출입증을 받지 않은(업데이트 전에 연결된) 기기 수
async function syncDevList(env, g, me) {
  const { results } = await env.DB.prepare(`SELECT pid, name, lbl, first, seen FROM sync_devs WHERE gid = ? ORDER BY first`).bind(g.gid).all();
  return { ok: true, me, list: results.map(r => ({ id: r.pid, name: r.name, lbl: r.lbl, first: r.first, seen: r.seen })), unk: Math.max(0, g.devs - results.length), devs: g.devs, max: SYNC_DEVS };
}
async function syncDevs(request, env) {
  if (await slowDown(env, request, 's')) return SLOW();
  const b = await readJson(request, 400);
  await ensureSchema(env);
  const g = await syncLite(env, b && b.key, b && b.dk);
  if (!g) return json({ ok: false, error: 'gone' }, 404);
  if (!str(b.dk, SYNC_DK)) return json({ ok: false, error: 'kicked' }, 403);
  const a = await syncAuth(env, b, g); if (a.err) return authFail(a);
  return json(await syncDevList(env, g, a.d.pid));
}
// 다른 기기 끊기: id = 끊을 기기, unk = 확인되지 않은 기기만 끊기.
// 어느 쪽이든 확인되지 않은 자리는 함께 없앤다(끊긴 기기가 출입증을 버리고 옛 기기인 척 다시 들어오지 못하게)
async function syncKick(request, env) {
  if (await slowDown(env, request, 's')) return SLOW();
  const b = await readJson(request, 400);
  await ensureSchema(env);
  const g = await syncLite(env, b && b.key, b && b.dk);
  if (!g) return json({ ok: false, error: 'gone' }, 404);
  if (!str(b.dk, SYNC_DK)) return json({ ok: false, error: 'kicked' }, 403);
  const a = await syncAuth(env, b, g); if (a.err) return authFail(a);
  const id = typeof b.id === 'string' && /^[A-Za-z0-9_-]{8}$/.test(b.id) ? b.id : null;
  if (!id && !b.unk) return json({ ok: false, error: 'bad_fields' }, 400);
  if (id === a.d.pid) return json({ ok: false, error: 'self' }, 400);
  const st = [];
  if (id) st.push(env.DB.prepare(`DELETE FROM sync_devs WHERE gid = ? AND pid = ?`).bind(g.gid, id));
  st.push(env.DB.prepare(`UPDATE sync_groups SET devs = (SELECT COUNT(*) FROM sync_devs WHERE gid = ?) WHERE gid = ?`).bind(g.gid, g.gid));
  st.push(env.DB.prepare(`DELETE FROM sync_codes WHERE gid = ?`).bind(g.gid)); // 끊긴 기기가 미리 만들어 둔 연결 코드도 무른다
  await env.DB.batch(st);
  return json(await syncDevList(env, await syncLite(env, b.key), a.d.pid));
}
// 이 기기의 이름 바꾸기(빈 칸이면 기기 종류로 돌아간다)
async function syncName(request, env) {
  if (await slowDown(env, request, 's')) return SLOW();
  const b = await readJson(request, 500);
  await ensureSchema(env);
  const g = await syncLite(env, b && b.key, b && b.dk);
  if (!g) return json({ ok: false, error: 'gone' }, 404);
  if (!str(b.dk, SYNC_DK)) return json({ ok: false, error: 'kicked' }, 403);
  const a = await syncAuth(env, b, g); if (a.err) return authFail(a);
  await env.DB.prepare(`UPDATE sync_devs SET name = ? WHERE did = ?`).bind(devTxt(b.name, 24), a.d.did).run();
  return json(await syncDevList(env, g, a.d.pid));
}

// 검은 성배 집계: 결말×보스를 쓰러뜨린 쪽×내 서번트의 끝×함께 싸운 조 수로 묶은 줄과, 클래스별 판수·내가 쓰러뜨린 수
const cxQ = (env, W, B) => [
  env.DB.prepare(`SELECT cx_end, by_who, fate, comp, mode, COUNT(*) AS n, SUM(tries) AS tr FROM cx_lives WHERE ${W} GROUP BY cx_end, by_who, fate, comp, mode`).bind(...B),
  env.DB.prepare(`SELECT cls, mode, COUNT(*) AS n, SUM(by_who = 'me') AS me, SUM(fate = 'alive') AS alive FROM cx_lives WHERE ${W} GROUP BY cls, mode`).bind(...B),
];
const cxOut = (rows, cls) => ({
  n: rows.results.reduce((a, r) => a + r.n, 0),
  rows: rows.results.map(r => [r.cx_end, r.by_who, r.fate, r.comp, r.n, r.tr || 0, r.mode || 'nat']),
  cls: cls.results.filter(r => r.cls).map(r => [r.cls, r.n, r.me || 0, r.alive || 0, r.mode || 'nat']),
});

// 신규 서번트(2026.10.30) — 통계 페이지의 '신규 서번트 이후' 기준점
const NEW_HEROES = ['baobhan','barghest','melusine','muramasa','ishtar','ereshkigal','lanling','habetrot','quetzalcoatl','kama','sheba','asclepius','constantine','huyan','lilith','yuyoku','nameless'];
const tsArg = v => { const n = Number(v); return Number.isFinite(n) && n > 0 && n < 1e14 ? Math.floor(n) : null; };
// 11-22: 전체 통계를 매번 lives(약 68만 줄) · dev_ach(약 1,170만 줄)에서 GROUP BY로 세면 한 번에 15~20초가 걸리고,
// D1은 쿼리를 하나씩 처리하므로 그동안 다른 요청이 모두 밀려 'D1 DB is overloaded'(7429)로 실패했다(요청의 약 30%).
// → 줄이 들어갈 때 트리거로 누적 수(c_*)를 더하고, 전체 통계는 누적 수만 읽는다.
// 처음 채우기: ① 트리거를 만들면서 그 순간의 MAX(rowid)를 meta에 적고(한 batch = 한 트랜잭션이라 그 뒤 줄은 트리거가 센다)
//              ② 그 rowid까지를 조각(CNT_STEP 줄)씩 나눠 더한다. 조각마다 진행 위치를 같은 batch로 적어, 끊겨도 이어서 센다.
// 다 채우기 전에는 지난 스냅숏을 그대로 준다.
const CNT = {
  lives: {
    step: 100000,
    setup: [
      `DELETE FROM c_tot`, `DELETE FROM c_hero`, `DELETE FROM c_end`, `DELETE FROM c_cup`,
      `CREATE TRIGGER IF NOT EXISTS c_lives_ins AFTER INSERT ON lives BEGIN
         INSERT INTO c_tot (k, v) VALUES ('lives', 1) ON CONFLICT(k) DO UPDATE SET v = v + 1;
         INSERT INTO c_tot (k, v) SELECT 'war', 1 WHERE NEW.hero IS NOT NULL ON CONFLICT(k) DO UPDATE SET v = v + 1;
         INSERT INTO c_tot (k, v) SELECT 'agesum', NEW.age WHERE NEW.age IS NOT NULL ON CONFLICT(k) DO UPDATE SET v = v + excluded.v;
         INSERT INTO c_tot (k, v) SELECT 'agecnt', 1 WHERE NEW.age IS NOT NULL ON CONFLICT(k) DO UPDATE SET v = v + 1;
         INSERT INTO c_hero (hero, n, g) SELECT NEW.hero, 1, NEW.ending IN ('victor', 'shared') WHERE NEW.hero IS NOT NULL ON CONFLICT(hero) DO UPDATE SET n = n + 1, g = g + excluded.g;
         INSERT INTO c_end (ending, n) VALUES (NEW.ending, 1) ON CONFLICT(ending) DO UPDATE SET n = n + 1;
         INSERT INTO c_cup (cup, n) SELECT NEW.cup, 1 WHERE NEW.cup IS NOT NULL ON CONFLICT(cup) DO UPDATE SET n = n + 1;
       END`,
      // /api/life/fix: 서번트 칸이 비어 있던 생에 서번트를 채울 때 (아직 조각이 세지 않은 옛 줄이면 그 조각이 고친 값을 세므로 건너뛴다)
      `CREATE TRIGGER IF NOT EXISTS c_lives_fix AFTER UPDATE OF hero ON lives
         WHEN OLD.hero IS NULL AND NEW.hero IS NOT NULL AND (NEW.rowid <= (SELECT CAST(v AS INTEGER) FROM meta WHERE k = 'cnt_lives_at')
                                                         OR NEW.rowid > (SELECT CAST(v AS INTEGER) FROM meta WHERE k = 'cnt_lives_max')) BEGIN
         INSERT INTO c_tot (k, v) VALUES ('war', 1) ON CONFLICT(k) DO UPDATE SET v = v + 1;
         INSERT INTO c_hero (hero, n, g) VALUES (NEW.hero, 1, NEW.ending IN ('victor', 'shared')) ON CONFLICT(hero) DO UPDATE SET n = n + 1, g = g + excluded.g;
       END`,
    ],
    chunk: [
      `INSERT INTO c_tot (k, v) SELECT 'lives', COUNT(*) FROM lives WHERE rowid > ?1 AND rowid <= ?2 ON CONFLICT(k) DO UPDATE SET v = v + excluded.v`,
      `INSERT INTO c_tot (k, v) SELECT 'war', COUNT(*) FROM lives WHERE rowid > ?1 AND rowid <= ?2 AND hero IS NOT NULL ON CONFLICT(k) DO UPDATE SET v = v + excluded.v`,
      `INSERT INTO c_tot (k, v) SELECT 'agesum', COALESCE(SUM(age), 0) FROM lives WHERE rowid > ?1 AND rowid <= ?2 ON CONFLICT(k) DO UPDATE SET v = v + excluded.v`,
      `INSERT INTO c_tot (k, v) SELECT 'agecnt', COUNT(age) FROM lives WHERE rowid > ?1 AND rowid <= ?2 ON CONFLICT(k) DO UPDATE SET v = v + excluded.v`,
      `INSERT INTO c_hero (hero, n, g) SELECT hero, COUNT(*), SUM(ending IN ('victor', 'shared')) FROM lives WHERE rowid > ?1 AND rowid <= ?2 AND hero IS NOT NULL GROUP BY hero
         ON CONFLICT(hero) DO UPDATE SET n = n + excluded.n, g = g + excluded.g`,
      `INSERT INTO c_end (ending, n) SELECT ending, COUNT(*) FROM lives WHERE rowid > ?1 AND rowid <= ?2 GROUP BY ending ON CONFLICT(ending) DO UPDATE SET n = n + excluded.n`,
      `INSERT INTO c_cup (cup, n) SELECT cup, COUNT(*) FROM lives WHERE rowid > ?1 AND rowid <= ?2 AND cup IS NOT NULL GROUP BY cup ON CONFLICT(cup) DO UPDATE SET n = n + excluded.n`,
    ],
  },
  ach: {
    step: 500000,
    setup: [
      `DELETE FROM c_ach`,
      `CREATE TRIGGER IF NOT EXISTS c_ach_ins AFTER INSERT ON dev_ach BEGIN
         INSERT INTO c_ach (ach, n) VALUES (NEW.ach, 1) ON CONFLICT(ach) DO UPDATE SET n = n + 1;
       END`,
    ],
    chunk: [
      `INSERT INTO c_ach (ach, n) SELECT ach, COUNT(*) FROM dev_ach WHERE rowid > ?1 AND rowid <= ?2 GROUP BY ach ON CONFLICT(ach) DO UPDATE SET n = n + excluded.n`,
    ],
  },
};
CNT.cx = {
  step: 100000,
  setup: [
    `DELETE FROM c_cxr`, `DELETE FROM c_cxc`,
    `CREATE TRIGGER IF NOT EXISTS c_cx_ins AFTER INSERT ON cx_lives BEGIN
       INSERT INTO c_cxr (cx_end, by_who, fate, comp, mode, n, tr) VALUES (NEW.cx_end, NEW.by_who, NEW.fate, COALESCE(NEW.comp, -1), COALESCE(NEW.mode, ''), 1, COALESCE(NEW.tries, 0))
         ON CONFLICT(cx_end, by_who, fate, comp, mode) DO UPDATE SET n = n + 1, tr = tr + excluded.tr;
       INSERT INTO c_cxc (cls, mode, n, me, alive) VALUES (COALESCE(NEW.cls, ''), COALESCE(NEW.mode, ''), 1, NEW.by_who = 'me', NEW.fate = 'alive')
         ON CONFLICT(cls, mode) DO UPDATE SET n = n + 1, me = me + excluded.me, alive = alive + excluded.alive;
     END`,
  ],
  chunk: [
    `INSERT INTO c_cxr (cx_end, by_who, fate, comp, mode, n, tr) SELECT cx_end, by_who, fate, COALESCE(comp, -1), COALESCE(mode, ''), COUNT(*), COALESCE(SUM(tries), 0)
       FROM cx_lives WHERE rowid > ?1 AND rowid <= ?2 GROUP BY 1, 2, 3, 4, 5 ON CONFLICT(cx_end, by_who, fate, comp, mode) DO UPDATE SET n = n + excluded.n, tr = tr + excluded.tr`,
    `INSERT INTO c_cxc (cls, mode, n, me, alive) SELECT COALESCE(cls, ''), COALESCE(mode, ''), COUNT(*), SUM(by_who = 'me'), SUM(fate = 'alive')
       FROM cx_lives WHERE rowid > ?1 AND rowid <= ?2 GROUP BY 1, 2 ON CONFLICT(cls, mode) DO UPDATE SET n = n + excluded.n, me = me + excluded.me, alive = alive + excluded.alive`,
  ],
};
const TBL = { lives: 'lives', ach: 'dev_ach', cx: 'cx_lives' };
class NotReady extends Error {}
// 누적 수가 준비됐으면 true. 아니면 budget(ms) 안에서 조각을 더 세고 false. 전체 통계를 다시 세는 차례를 잡은 요청(한 번에 하나)만 부른다
async function cntReady(env, budget) {
  const t0 = Date.now(), M = {};
  const keys = Object.keys(CNT).flatMap(n => [`cnt_${n}`, `cnt_${n}_max`, `cnt_${n}_at`]);
  const { results } = await env.DB.prepare(`SELECT k, v FROM meta WHERE k IN (${keys.map(() => '?').join(', ')})`).bind(...keys).all();
  for (const r of results) M[r.k] = r.v;
  let ready = true;
  for (const name of Object.keys(CNT)) {
    if (M[`cnt_${name}`] === '1') continue;
    const C = CNT[name];
    if (M[`cnt_${name}_max`] == null) {
      await env.DB.batch([...C.setup.map(q => env.DB.prepare(q)),
        env.DB.prepare(`INSERT OR REPLACE INTO meta (k, v) SELECT 'cnt_${name}_max', CAST(COALESCE(MAX(rowid), 0) AS TEXT) FROM ${TBL[name]}`),
        env.DB.prepare(`INSERT OR REPLACE INTO meta (k, v) VALUES ('cnt_${name}_at', '0')`)]);
      const r = await env.DB.prepare(`SELECT v FROM meta WHERE k = ?`).bind(`cnt_${name}_max`).first();
      M[`cnt_${name}_max`] = r.v; M[`cnt_${name}_at`] = '0';
    }
    const max = +M[`cnt_${name}_max`]; let at = +M[`cnt_${name}_at`];
    for (let first = true; at < max && (first || Date.now() - t0 < budget); first = false) {   // 적어도 한 조각은 센다
      const hi = Math.min(max, at + C.step);
      await env.DB.batch([...C.chunk.map(q => env.DB.prepare(q).bind(at, hi)),
        env.DB.prepare(`INSERT OR REPLACE INTO meta (k, v) VALUES (?, ?)`).bind(`cnt_${name}_at`, String(hi))]);
      at = hi;
    }
    if (at >= max) await env.DB.prepare(`INSERT OR REPLACE INTO meta (k, v) VALUES (?, '1')`).bind(`cnt_${name}`).run();
    else ready = false;
  }
  return ready;
}

// 통계 스냅숏: 합친 결과를 stats_snap에 한 줄로 두고, 10분이 지나면 한 요청만 다시 센다.
// (예전에는 Cache API에 10분 캐시했는데, 데이터센터마다 따로라 거의 매번 전체를 다시 셌다)
// 다시 세는 동안 다른 요청은 지난 결과를 받는다. 처음이라 지난 결과가 없을 때만 기다린다.
const SNAP_TTL = 10 * 60000, SNAP_LOCK = 2 * 60000;
// 11-23: 기간 통계(since/until)는 lives를 기간으로 GROUP BY해 한 번에 3~5초 D1을 잡으므로 1시간에 한 번만 다시 센다
const snapTtl = key => (key === 'all' ? SNAP_TTL : 60 * 60000);
// 11-25: 받은 스냅숏을 이 서버(isolate) 메모리에 1분 동안 둔다 (예전: 통계 요청마다 stats_snap을 읽었다 — 하루 61만 번)
const SNAP_MEM = 60e3, snapMem = new Map();
async function snapStats(env, ctx, key, build) {
  const now = Date.now();
  const m = snapMem.get(key); if (m && now - m.at < SNAP_MEM) return m.body;
  const row = await env.DB.prepare(`SELECT at, body FROM stats_snap WHERE k = ?`).bind(key).first();
  if (row && row.body && now - row.at < snapTtl(key)) { snapMem.set(key, { at: now, body: row.body }); if (snapMem.size > 64) snapMem.delete(snapMem.keys().next().value); return row.body; }
  // 다시 셀 차례를 잡는다: busy가 비었거나 너무 오래된 경우에만 한 요청이 잡는다
  const claim = await env.DB.prepare(
    `INSERT INTO stats_snap (k, at, busy, body) VALUES (?, 0, ?, '') ON CONFLICT(k) DO UPDATE SET busy = excluded.busy WHERE stats_snap.busy < ?`
  ).bind(key, now, now - SNAP_LOCK).run();
  const mine = !!(claim.meta && claim.meta.changes);
  const redo = async () => {
    try {
      const body = JSON.stringify(await build({ old: !!(row && row.body) }));
      await env.DB.batch([
        env.DB.prepare(`UPDATE stats_snap SET at = ?, busy = 0, body = ? WHERE k = ?`).bind(Date.now(), body, key),
        env.DB.prepare(`DELETE FROM stats_snap WHERE k != 'all' AND at < ? AND busy < ?`).bind(now - 86400000, now - SNAP_LOCK),   // 하루 넘게 안 쓴 기간 통계는 지운다
      ]);
      return body;
    } catch (e) {
      // 11-22: 실패해도 차례(busy)는 바로 풀지 않는다 — 풀면 다음 요청이 곧바로 다시 세어 무거운 쿼리가 몰렸다. SNAP_LOCK(2분)이 지나면 다시 잡을 수 있다.
      // 누적 수를 조각으로 채우는 중(NotReady)이면 다음 요청이 이어서 세도록 푼다
      if (e instanceof NotReady) await env.DB.prepare(`UPDATE stats_snap SET busy = 0 WHERE k = ?`).bind(key).run().catch(() => {});
      throw e;
    }
  };
  if (row && row.body) {               // 지난 결과가 있으면 그것을 바로 주고, 차례를 잡았으면 뒤에서 다시 센다
    if (mine) ctx.waitUntil(redo().catch(e => { if (!(e instanceof NotReady)) console.error('stats redo', e && e.message); }));
    return row.body;
  }
  return mine ? redo() : JSON.stringify(await build());   // 처음: 지난 결과가 없으니 센다
}
const statsRes = body => new Response(body, {
  status: 200,
  headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'public, max-age=600', 'x-content-type-options': 'nosniff' },
});

// 기간을 정해 합친다. 시각은 분 단위로 맞추고, 같은 기간은 스냅숏 한 줄을 같이 쓴다.
async function getStatsRange(request, env, ctx, url) {
  const sRaw = url.searchParams.get('since'), uRaw = url.searchParams.get('until');
  await ensureSchema(env);
  let since = sRaw === 'new' ? null : tsArg(sRaw), until = tsArg(uRaw);
  if (sRaw === 'new') {
    const r = await env.DB.prepare(`SELECT MIN(ts) AS t0 FROM lives WHERE hero IN (${NEW_HEROES.map(() => '?').join(',')})`).bind(...NEW_HEROES).first();
    since = (r && r.t0) || null;
  }
  const M = 60000; since = since ? Math.floor(since / M) * M : 0; until = until ? Math.ceil(until / M) * M : 0;
  const W = `ts >= ?${until ? ' AND ts < ?' : ''}`, B = until ? [since, until] : [since];
  const q = (sql) => env.DB.prepare(sql).bind(...B);
  const body = await snapStats(env, ctx, `r:${since}:${until}`, async () => {
    const [tot, heroes, cls, ends, cxr, cxc] = await env.DB.batch([
      q(`SELECT COUNT(*) AS lives, COUNT(DISTINCT dev) AS players, MIN(ts) AS first, MAX(ts) AS last, ROUND(AVG(age), 1) AS avgAge,
                SUM(hero IS NOT NULL) AS warLives, SUM(hero IS NOT NULL AND ending IN ('victor', 'shared')) AS wins FROM lives WHERE ${W}`),
      q(`SELECT hero, COUNT(*) AS n, SUM(ending IN ('victor', 'shared')) AS g FROM lives WHERE ${W} AND hero IS NOT NULL GROUP BY hero`),
      q(`SELECT cls, COUNT(*) AS n, SUM(ending IN ('victor', 'shared')) AS g FROM lives WHERE ${W} AND hero IS NOT NULL GROUP BY cls`),
      q(`SELECT ending, COUNT(*) AS n FROM lives WHERE ${W} GROUP BY ending`),
      ...cxQ(env, W, B),
    ]);
    const t = tot.results[0] || {};
    return {
      ok: true, at: Date.now(), range: { since, until: until || null },
      lives: t.lives || 0, players: t.players || 0, warLives: t.warLives || 0, wins: t.wins || 0,
      first: t.first || null, last: t.last || null, avgAge: t.avgAge || null,
      heroes: Object.fromEntries(heroes.results.map(r => [r.hero, [r.n, r.g || 0]])),
      cls: Object.fromEntries(cls.results.filter(r => r.cls).map(r => [r.cls, [r.n, r.g || 0]])),
      ends: Object.fromEntries(ends.results.map(r => [r.ending, r.n])),
      cx: cxOut(cxr, cxc),
    };
  });
  return statsRes(body);
}

async function getStats(request, env, ctx) {
  if (await slowDown(env, request, 't')) return SLOW();
  const url = new URL(request.url);
  if (url.searchParams.has('since') || url.searchParams.has('until')) return getStatsRange(request, env, ctx, url);
  await ensureSchema(env);
  const body = await snapStats(env, ctx, 'all', async ({ old }) => {
    // 11-22: 누적 수에서 읽는다. 아직 채우는 중이면 지난 스냅숏을 두고(한 번에 3초까지만 센다), 지난 것이 없으면 끝까지 센다
    if (!(await cntReady(env, old ? 3000 : Infinity))) throw new NotReady();
    const [tot, heroes, ends, cups, ach, cxr, cxc] = await env.DB.batch([
      env.DB.prepare(`SELECT (SELECT v FROM c_tot WHERE k = 'lives') AS lives, (SELECT COUNT(*) FROM devices) AS players,
                             (SELECT MIN(ts) FROM lives) AS since,
                             (SELECT ROUND(1.0 * (SELECT v FROM c_tot WHERE k = 'agesum') / NULLIF((SELECT v FROM c_tot WHERE k = 'agecnt'), 0), 1)) AS avgAge,
                             (SELECT v FROM c_tot WHERE k = 'war') AS warLives`),
      env.DB.prepare(`SELECT hero, n, g FROM c_hero WHERE n > 0`),
      env.DB.prepare(`SELECT ending, n FROM c_end WHERE n > 0`),
      env.DB.prepare(`SELECT cup, n FROM c_cup WHERE n > 0`),
      env.DB.prepare(`SELECT ach, n FROM c_ach WHERE n > 0`),
      // 11-23: 검은 성배 집계도 누적 수에서 (cx_lives 전체 GROUP BY가 한 번에 0.2~0.3초씩 D1을 잡았다)
      env.DB.prepare(`SELECT cx_end, by_who, fate, NULLIF(comp, -1) AS comp, NULLIF(mode, '') AS mode, n, tr FROM c_cxr WHERE n > 0`),
      env.DB.prepare(`SELECT NULLIF(cls, '') AS cls, NULLIF(mode, '') AS mode, n, me, alive FROM c_cxc WHERE n > 0`),
    ]);
    const t = tot.results[0] || {};
    return {
      ok: true,
      at: Date.now(),
      lives: t.lives || 0,
      players: t.players || 0,
      warLives: t.warLives || 0,
      since: t.since || null,
      avgAge: t.avgAge || null,
      heroes: Object.fromEntries(heroes.results.map(r => [r.hero, [r.n, r.g || 0]])),
      ends: Object.fromEntries(ends.results.map(r => [r.ending, r.n])),
      cups: Object.fromEntries(cups.results.map(r => [r.cup, r.n])),
      ach: Object.fromEntries(ach.results.map(r => [r.ach, r.n])),
      cx: cxOut(cxr, cxc),
    };
  });
  return statsRes(body);
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    try {
      if (url.pathname === '/api/health') return json({ ok: true, time: new Date().toISOString(), db: !!env.DB });
      if (url.pathname === '/api/life') {
        if (request.method !== 'POST') return json({ ok: false, error: 'method' }, 405, { allow: 'POST' });
        return await postLife(request, env);
      }
      if (request.method === 'POST' && url.pathname === '/api/life/fix') return await fixLives(request, env);
      if (url.pathname === '/api/stats') {
        if (request.method !== 'GET') return json({ ok: false, error: 'method' }, 405, { allow: 'GET' });
        return await getStats(request, env, ctx);
      }
      if (url.pathname === '/api/ghost') {
        if (request.method === 'POST') return await postGhost(request, env);
        if (request.method === 'GET') return await getGhost(request, url, env);
        return json({ ok: false, error: 'method' }, 405);
      }
      if (request.method === 'POST' && url.pathname === '/api/ghost/shown') return await ghostShown(request, env);
      if (request.method === 'POST' && url.pathname === '/api/ghost/withdraw') return await withdrawGhost(request, env);
      if (request.method === 'POST' && url.pathname === '/api/ghost/report') return await reportGhost(request, env);
      if (request.method === 'POST' && url.pathname === '/api/ghost/result') return await ghostResult(request, env);
      if (request.method === 'POST' && url.pathname === '/api/ghost/news') return await ghostNews(request, env);
      if (request.method === 'POST' && url.pathname === '/api/ghost/mine') return await ghostMine(request, env);
      if (request.method === 'POST' && url.pathname.startsWith('/api/sync/')) {
        const f = { new: syncNew, code: syncMakeCode, join: syncJoin, pull: syncPull, push: syncPush, leave: syncLeave, devs: syncDevs, kick: syncKick, name: syncName }[url.pathname.slice(10)];
        if (f) return await f(request, env);
      }
      if (url.pathname.startsWith('/api/')) return json({ ok: false, error: 'not_found' }, 404);
    } catch (e) {
      if (e instanceof TooBig) return json({ ok: false, error: 'too_big' }, 413);
      console.error(`${request.method} ${url.pathname} — ${(e && e.name) || 'Error'}: ${(e && e.message) || e}`, e && e.stack);
      return json({ ok: false, error: 'server' }, 500);
    }
    return env.ASSETS.fetch(request);
  },
};
