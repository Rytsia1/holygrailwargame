"""Custom Master (커스텀 마스터) patch script.
Usage: python3 custom_apply.py <game.html>
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'custom1125' in s:
    print('이미 적용됨')
    sys.exit(0)

miss = []
def rp(o, n):
    global s
    k = s.count(o)
    if k != 1:
        miss.append((o[:80], k))
        return
    s = s.replace(o, n)

# 1. Sim: custClamp, custCost, custRanges
SIM_CUST = r"""
  /* ---------- 커스텀 마스터 (custom1125) ---------- */
  const CUST_BUDGET = 10;
  const CUST_ART_COST = [0, 2, 4, 7, 11];
  const CUST_GIFT_COST = [0, 2, 4, 6, 9];
  const CUST_ST_KEYS = ['mana', 'lore', 'will', 'bond', 'health', 'wealth'];
  function custRanges(originId, circuit){
    const o = ORIGINS.find(x=>x.id===originId) || ORIGINS[5];
    const c = clamp(Math.round(+circuit||o.circ[0]), 1, 5);
    return {
      o,
      circ: o.circ,
      st: {
        mana: [c*7, c*7+8],
        lore: [0, 4],
        will: [15, 35],
        bond: o.orphan ? [15, 30] : [40, 60],
        health: [70, 92],
        wealth: o.wealth,
      }
    };
  }
  function custClamp(raw){
    const c = raw && typeof raw === 'object' ? raw : {};
    const mode = c.mode === 'free' ? 'free' : 'pt';
    const o = ORIGINS.find(x=>x.id===c.origin) || ORIGINS[5];
    const circuit = clamp(Math.round(+c.circuit || o.circ[0]), 1, 5);
    const rng = custRanges(o.id, circuit);
    const st = {};
    for(const k of CUST_ST_KEYS){
      const d = rng.st[k], mid = Math.round((d[0]+d[1])/2);
      const rawV = c.st && c.st[k] != null ? +c.st[k] : mid;
      st[k] = clamp(Math.round(isNaN(rawV)?mid:rawV), 0, k==='mana' ? 40+circuit*12 : 100);
    }
    const arts = {};
    if(c.arts && typeof c.arts === 'object'){
      for(const [id, lvRaw] of Object.entries(c.arts)){
        if(!ART_CHAIN[id]) continue;
        const lv = clamp(Math.round(+lvRaw||0), 0, ART_CHAIN[id].max);
        if(lv > 0) arts[id] = lv;
      }
    }
    const fam = FAMILY_ART[o.id] || [];
    let main = c.main && arts[c.main] ? c.main : null;
    if(!main && Object.keys(arts).length){
      main = fam.find(id=>arts[id]) || Object.keys(arts)[0];
    }
    const cityObj = c.city ? CITIES.find(x=>x.n===c.city) : null;
    const era = (c.era==='past'||c.era==='future'||c.era==='present') ? c.era : 'present';
    let gift = 'random', giftGr = 1;
    if(c.gift === 'none') gift = 'none';
    else if(c.gift && GIFTS[c.gift]){
      gift = c.gift;
      const [g0, g1] = GIFTS[gift].g;
      giftGr = clamp(Math.round(+c.giftGr||g0), g0, g1);
    }
    return { on:!!c.on, mode, origin:o.id, city:cityObj?cityObj.n:'', era, circuit, st, arts, main, gift, giftGr };
  }
  function custCost(raw){
    const c = raw && typeof raw === 'object' ? raw : {};
    const mode = c.mode === 'free' ? 'free' : 'pt';
    const o = ORIGINS.find(x=>x.id===c.origin) || ORIGINS[5];
    const circuit = clamp(Math.round(+c.circuit || o.circ[0]), 1, 5);
    const rng = custRanges(o.id, circuit);
    const errs = [];
    let cost = 0;
    if(circuit > o.circ[1]) cost += (circuit - o.circ[1]) * 3;
    const manaCapV = 40 + circuit * 12;
    const stIn = c.st || {};
    for(const k of CUST_ST_KEYS){
      const d = rng.st[k], mid = Math.round((d[0]+d[1])/2);
      const v = clamp(Math.round(stIn[k]!=null && !isNaN(+stIn[k]) ? +stIn[k] : mid), 0, 100);
      if(k==='mana' && v > manaCapV) errs.push('초기 마력이 마술회로 상한을 넘었습니다.');
      if(v < d[0]) cost += Math.ceil((d[0] - v) / 5);
      else if(v > d[1]) cost += Math.ceil((v - d[1]) / 5);
    }
    const fam = FAMILY_ART[o.id] || [];
    let famUsed = false, magicN = 0, bodyN = 0;
    const artsIn = c.arts || {};
    const activeIds = Object.keys(artsIn).filter(id=>ART_CHAIN[id] && (+artsIn[id]||0) > 0);
    const mainId = c.main && activeIds.includes(c.main) ? c.main : (fam.find(id=>activeIds.includes(id)) || activeIds[0] || null);
    for(const id of activeIds){
      const lv = Math.round(+artsIn[id]||0);
      const C = ART_CHAIN[id], A = ARTS[id];
      if(lv > C.max) errs.push('선택한 기술의 최대 단계를 넘었습니다.');
      if(A.br === 'magic') magicN++;
      else if(A.br === 'martial' || A.br === 'church') bodyN++;
      if(A.br === 'magic' && lv >= 3 && circuit < 3) errs.push('고위(3단계) 마술은 마술회로 C등급 이상이 필요합니다.');
      if(lv >= 4 && (mainId !== id || circuit < 5)) errs.push('비전(4단계)은 본계 기술이면서 마술회로 A등급이 필요합니다.');
      let ac = CUST_ART_COST[clamp(lv, 0, 4)];
      if(!famUsed && fam.includes(id)){ ac = Math.max(0, ac - 2); famUsed = true; }
      cost += ac;
    }
    if(magicN > 3) errs.push('마술 계통은 3개까지 고를 수 있습니다.');
    if(bodyN > 2) errs.push('무투·교회 계통은 2개까지 고를 수 있습니다.');
    if(c.gift && c.gift !== 'random' && c.gift !== 'none' && GIFTS[c.gift]){
      const [g0, g1] = GIFTS[c.gift].g;
      const gr = clamp(Math.round(+c.giftGr||g0), g0, g1);
      cost += CUST_GIFT_COST[gr];
    }
    if(mode !== 'free' && cost > CUST_BUDGET) errs.push('포인트 예산을 초과했습니다.');
    return { cost, max: CUST_BUDGET, errs: [...new Set(errs)] };
  }
"""
rp("  const O = ()=>ORIGINS.find(o=>o.id===S.origin);", SIM_CUST + "  const O = ()=>ORIGINS.find(o=>o.id===S.origin);")

# 2. Sim: newLife(opt) custom support
rp(
"""    const origin = wpick(ORIGINS,o=>o.w);
    const circuit = ri(origin.circ[0],origin.circ[1]);
    const birthYear = opt.era==='past'? ri(1930,1965) : opt.era==='future'? ri(2030,2060) : ri(1975,2005);
    const city = wpick(CITIES,c=>CITY_W[c.loc]||1);""",
"""    const cu = opt.custom ? custClamp(opt.custom) : null;
    const origin = (cu && ORIGINS.find(o=>o.id===cu.origin)) || wpick(ORIGINS,o=>o.w);
    const circuit = cu ? cu.circuit : ri(origin.circ[0],origin.circ[1]);
    const era = cu ? cu.era : opt.era;
    const birthYear = era==='past'? ri(1930,1965) : era==='future'? ri(2030,2060) : ri(1975,2005);
    const city = (cu && cu.city && CITIES.find(c=>c.n===cu.city)) || wpick(CITIES,c=>CITY_W[c.loc]||1);"""
)

rp(
"""    S.warYear = S.birthYear + S.warAge;
    S.flags.everLost = 0;
    arts(); giftRoll(); // 가문 본계(마술 가문·교회 출신), 초능력 잠재
    return S;""",
"""    S.warYear = S.birthYear + S.warAge;
    S.flags.everLost = 0;
    if(cu){
      S.st = { mana: cu.st.mana, lore: cu.st.lore, will: cu.st.will, bond: cu.st.bond, health: cu.st.health };
      S.wealth = cu.st.wealth;
      S.custom = { mode: cu.mode };
      S.arts = {};
      const ks = Object.keys(cu.arts);
      const mId = cu.main && cu.arts[cu.main] ? cu.main : (ks[0] || null);
      for(const id of ks){
        const lv = cu.arts[id];
        S.arts[id] = { lv, q: 1, xp: 0, at: 0, ...(id===mId ? {main:true} : {}) };
        if(ARTS[id].br === 'magic' && !origin.mage){ S.flags.awakened = 1; S.flags.awAge = 0; }
        if(ARTS[id].br === 'church' && !origin.church){ S.flags.churchTie = 1; }
        if(id === 'familiar' && !S.flags.familiar){ S.flags.familiar = '까마귀'; }
      }
      if(cu.gift === 'random') giftRoll();
      else if(cu.gift !== 'none' && GIFTS[cu.gift]) S.gift = { id: cu.gift, gr: cu.giftGr, awake: false, ctl: 0 };
    } else {
      arts(); giftRoll(); // 가문 본계(마술 가문·교회 출신), 초능력 잠재
    }
    return S;"""
)

# 3. Sim: giftEvent guarantee awake at age 18 for S.custom
rp(
"    if(!g.awake){ if(!g.due&&S.age>=6&&S.age<=18&&hrand('giftA')<.15*(S.flags.lossAge===S.age?3:1)) g.due='awake'; }",
"    if(!g.awake){ if(!g.due&&S.age>=6&&S.age<=18&&(hrand('giftA')<.15*(S.flags.lossAge===S.age?3:1)||(S.custom&&S.age===18))) g.due='awake'; }"
)

# 4. Sim: start() log
rp(
"    log(`마술회로 ${GR[S.circuit]}등급.",
"    if(S.custom) log('커스텀 마스터로 태어났다.','sys');\n    log(`마술회로 ${GR[S.circuit]}등급."
)

# 5. Sim: record() custom field
rp(
"seed:S.seed, ts:Date.now(), warYear:S.warYear,",
"seed:S.seed, ts:Date.now(), custom:S.custom?1:undefined, warYear:S.warYear,"
)

# 6. Sim: exports
rp(
"CLS,GR,HEROES,H_BY,ORIGINS,FOCUS,LEN,",
"CLS,GR,HEROES,H_BY,ORIGINS,CITIES,ARTS,ART_TIER,FAMILY_ART,GIFTS,GRADE_N,ART_CHAIN:Object.fromEntries(Object.entries(ART_CHAIN).map(([k,v])=>[k,{max:v.max,st:v.st}])),custCost,custClamp,custRanges,FOCUS,LEN,"
)

# 7. CSS for #custDlg, .cust-btn, .badge.cust
CUST_CSS = (
    ".cust-btn{grid-column:1/-1;padding:9px 14px;font-size:13.5px;border:1px solid rgba(201,164,92,.45);border-radius:var(--r);background:var(--panel2);color:var(--gold2);cursor:pointer}"
    ".cust-btn.on{border-color:var(--gold);background:rgba(201,164,92,.14)}"
    ".cust-sheet{max-width:520px}"
    ".cust-top{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;margin:10px 0 6px}"
    ".cust-top .scn-seg{margin-bottom:0}"
    ".cust-meter{font:500 13px var(--f-mono);color:var(--gold2);margin:6px 0 0}"
    ".cust-meter.over{color:#e6a3a3}"
    ".cust-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}"
    "@media (max-width:440px){.cust-row{grid-template-columns:1fr}}"
    ".cust-fld{display:grid;gap:5px}"
    ".cust-fld label,.cust-sub{font-size:12px;color:var(--dim)}"
    ".cust-fld select,.cust-art select,.cust-gift select{background:var(--ink);border:1px solid var(--line);border-radius:8px;color:var(--text);font:inherit;font-size:13px;padding:7px 9px;max-width:100%}"
    ".cust-circ button.free{box-shadow:inset 0 -2px 0 rgba(120,200,150,.7)}"
    ".cust-stats{display:grid;gap:10px;margin-top:10px}"
    ".cust-st{display:grid;gap:4px}"
    ".cust-st-h{display:flex;justify-content:space-between;align-items:center;font-size:12.5px}"
    ".cust-st-h b{font-family:var(--f-mono);color:var(--text)}"
    ".cust-st-h small{font-size:11.5px;color:var(--faint)}"
    ".cust-st-h small.paid{color:var(--gold2)}"
    ".cust-sl{position:relative;height:24px;display:flex;align-items:center}"
    ".cust-band{position:absolute;left:0;right:0;height:6px;border-radius:999px;background:rgba(255,255,255,.08);pointer-events:none;overflow:hidden}"
    ".cust-band i{position:absolute;top:0;bottom:0;background:rgba(111,191,138,.42);border-radius:999px}"
    ".cust-sl input[type=range]{position:relative;z-index:1;width:100%;margin:0;accent-color:var(--gold);background:transparent}"
    ".cust-arts{display:grid;gap:12px;margin-top:10px}"
    ".cust-br{display:grid;gap:6px}"
    ".cust-br-t{font-size:11.5px;letter-spacing:.08em;color:var(--faint)}"
    ".cust-art{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:8px;align-items:center;padding:6px 8px;border:1px solid var(--line);border-radius:8px;background:rgba(255,255,255,.02)}"
    ".cust-art .nm{font-size:13px;color:var(--text);display:flex;flex-wrap:wrap;gap:5px;align-items:center;min-width:0}"
    ".cust-art .fam{font-size:10.5px;padding:1px 6px;border-radius:999px;border:1px solid rgba(111,191,138,.5);color:#9bd3ac}"
    ".cust-art .main{display:inline-flex;align-items:center;gap:4px;font-size:12px;color:var(--dim);white-space:nowrap;cursor:pointer}"
    ".cust-art .main input{accent-color:var(--gold)}"
    ".cust-gift{display:grid;gap:10px;margin-top:10px}"
    ".cust-errs{margin:12px 0 0;padding:8px 12px;border-radius:8px;border:1px solid rgba(210,70,80,.5);background:rgba(180,50,60,.12);color:#f0a8ae;font-size:12.5px;line-height:1.5}"
    ".cust-errs.hidden{display:none}"
    ".cust-foot{display:flex;gap:8px;justify-content:flex-end;margin-top:14px;padding-top:12px;border-top:1px solid var(--line)}"
    ".cust-foot .btn{padding:8px 16px;font-size:13.5px}"
    ".past-item .badge.cust{border-color:rgba(160,180,230,.55);color:#b7c9f2}"
    "#lb2 .l2-custw{display:contents}"
    "#lb2 .l2-cust{order:5}"
)
rp(".scn-cat{font:500 11.5px var(--f-mono);", CUST_CSS + ".scn-cat{font:500 11.5px var(--f-mono);")

# 8. HTML: Lobby v1 button in .born-row and #custDlg after #scnDlg
rp(
'<div class="born-row"><button class="btn primary" id="startBtn">태어나기</button><div class="sex-pick" id="sexPick" role="group" aria-label="성별"><button type="button" data-s="">무작위</button><button type="button" data-s="f">여성</button><button type="button" data-s="m">남성</button></div></div>',
'<div class="born-row"><button class="btn primary" id="startBtn">태어나기</button><div class="sex-pick" id="sexPick" role="group" aria-label="성별"><button type="button" data-s="">무작위</button><button type="button" data-s="f">여성</button><button type="button" data-s="m">남성</button></div><button class="cust-btn" id="custBtn" type="button">커스텀 마스터</button></div>'
)

CUST_DLG_HTML = """<div class="dlg hidden" id="custDlg" role="dialog" aria-modal="true" aria-label="커스텀 마스터" style="z-index:55"><div class="sheet info set-sheet cust-sheet"><div class="set-head"><h2>커스텀 마스터</h2><button class="set-x" id="custX" type="button" aria-label="닫기">×</button></div>
<div class="cust-top">
  <div class="scn-seg" id="custOnSeg" role="group" aria-label="커스텀 마스터"><button type="button" data-on="0">무작위 출생</button><button type="button" data-on="1">커스텀 마스터로 태어나기</button></div>
  <div class="scn-seg" id="custModeSeg" role="group" aria-label="모드"><button type="button" data-m="pt">포인트</button><button type="button" data-m="free">무제한</button></div>
</div>
<p class="cust-meter" id="custMeter"></p>
<div id="custBody">
  <div class="scn-sec"><div class="scn-t">출신 · 도시 · 시대</div>
    <div class="cust-row">
      <div class="cust-fld"><label for="custOrigin">출신</label><select id="custOrigin"></select></div>
      <div class="cust-fld"><label for="custCity">도시</label><select id="custCity"></select></div>
    </div>
    <div class="cust-fld" style="margin-top:10px"><label>시대</label><div class="scn-seg" id="custEraSeg" role="group" aria-label="시대"><button type="button" data-e="past">과거</button><button type="button" data-e="present">현재</button><button type="button" data-e="future">미래</button></div></div>
  </div>
  <div class="scn-sec"><div class="scn-t">마술회로</div><div class="scn-seg cust-circ" id="custCircSeg" role="group" aria-label="마술회로"></div><p class="cust-sub" id="custCircHint"></p></div>
  <div class="scn-sec"><div class="scn-t">초기 능력치</div><div class="cust-stats" id="custStats"></div></div>
  <div class="scn-sec"><div class="scn-t">익힌 기술</div><div class="cust-arts" id="custArts"></div></div>
  <div class="scn-sec"><div class="scn-t">마안 · 초능력</div><div class="cust-gift"><select id="custGift"></select><div class="scn-seg hidden" id="custGiftGrSeg" role="group" aria-label="등급"></div></div></div>
</div>
<div class="cust-errs hidden" id="custErrs"></div>
<div class="cust-foot"><button class="btn" id="custReset" type="button">초기화</button><button class="btn primary" id="custSave" type="button">저장</button></div>
</div></div>"""

rp(
'<div class="dlg hidden" id="scnDlg"',
CUST_DLG_HTML + '\n<div class="dlg hidden" id="scnDlg"'
)

# 9. JS: Custom Master state, UI, birth() integration
CUST_JS = r"""
const K_CUST='cupnight.custom.v1';
function custDefault(originId){
  const o=Sim.ORIGINS.find(x=>x.id===originId)||Sim.ORIGINS[5];
  const c=o.circ[0], r=Sim.custRanges(o.id,c), st={};
  for(const k of ['mana','lore','will','bond','health','wealth']) st[k]=Math.round((r.st[k][0]+r.st[k][1])/2);
  const fam=(Sim.FAMILY_ART[o.id]||[])[0];
  return {on:false,mode:'pt',origin:o.id,city:'',era:'present',circuit:c,st,arts:fam?{[fam]:1}:{},main:fam||null,gift:'random',giftGr:1};
}
function custLoad(){ const v=store.get(K_CUST); return v?Sim.custClamp(v):custDefault('common'); }
function custActive(){ const c=store.get(K_CUST); return !!(c&&c.on&&Sim.custCost(c).errs.length===0); }
function custForBirth(){ const c=store.get(K_CUST); if(!c||!c.on) return null; const cl=Sim.custClamp(c); return Sim.custCost(cl).errs.length?null:cl; }
let CUST_D=null;
function custBuildOnce(){
  const selO=$('#custOrigin'); if(!selO||selO.options.length) return;
  const T=x=>typeof tr==='function'?tr(x):x;
  selO.innerHTML=Sim.ORIGINS.map(o=>`<option value="${o.id}">${esc(T(o.label))}</option>`).join('');
  $('#custCity').innerHTML=`<option value="">${esc(T('무작위'))}</option>`+Sim.CITIES.map(c=>`<option value="${esc(c.n)}">${esc(T(c.n))}</option>`).join('');
  $('#custCircSeg').innerHTML=[1,2,3,4,5].map(g=>`<button type="button" data-c="${g}">${Sim.GR[g]}</button>`).join('');
  const SL=[['mana','마력'],['lore','지식'],['will','정신'],['bond','관계'],['health','건강'],['wealth','재산']];
  $('#custStats').innerHTML=SL.map(([k,l])=>`<div class="cust-st" data-k="${k}"><div class="cust-st-h"><span>${esc(T(l))}</span><span><b class="v"></b> · <small class="c"></small></span></div><div class="cust-sl"><div class="cust-band"><i></i></div><input type="range" min="0" max="100" data-st="${k}"></div></div>`).join('');
  const BR=[['magic','마술'],['church','교회'],['martial','무투']];
  const TI=Sim.ART_TIER;
  $('#custArts').innerHTML=BR.map(([br,bl])=>{
    const ids=Object.keys(Sim.ART_CHAIN).filter(id=>Sim.ARTS[id]&&Sim.ARTS[id].br===br);
    return `<div class="cust-br"><div class="cust-br-t">${esc(T(bl))}</div>${ids.map(id=>{
      const mx=Sim.ART_CHAIN[id].max;
      const opts=`<option value="0">${esc(T('없음'))}</option>`+[1,2,3,4].filter(n=>n<=mx).map(n=>`<option value="${n}">${esc(T(TI[n]))}</option>`).join('');
      return `<div class="cust-art" data-a="${id}"><span class="nm"><span>${esc(T(Sim.ARTS[id].n))}</span><span class="fam hidden">${esc(T('가문 무료'))}</span></span><select data-art="${id}">${opts}</select><label class="main"><input type="radio" name="custMain" value="${id}"><span>${esc(T('본계'))}</span></label></div>`;
    }).join('')}</div>`;
  }).join('');
  $('#custGift').innerHTML=`<option value="random">${esc(T('무작위'))}</option><option value="none">${esc(T('없음'))}</option>`+Object.entries(Sim.GIFTS).map(([id,g])=>`<option value="${id}">${esc(T(g.n))}</option>`).join('');
  $('#custGiftGrSeg').innerHTML=[1,2,3,4].map(g=>`<button type="button" data-g="${g}">${esc(T(Sim.GRADE_N[g]))}</button>`).join('');
}
function custRender(){
  if(!CUST_D) return;
  const T=x=>typeof tr==='function'?tr(x):x;
  const d=CUST_D, res=Sim.custCost(d), rng=Sim.custRanges(d.origin,d.circuit), fam=Sim.FAMILY_ART[d.origin]||[];
  document.querySelectorAll('#custOnSeg button').forEach(b=>b.setAttribute('aria-pressed',String((b.dataset.on==='1')===d.on)));
  document.querySelectorAll('#custModeSeg button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.m===d.mode)));
  $('#custModeSeg').classList.toggle('hidden',!d.on);
  $('#custBody').classList.toggle('hidden',!d.on);
  const meter=$('#custMeter');
  if(!d.on){ meter.textContent=''; meter.classList.remove('over'); }
  else if(d.mode==='free'){ meter.textContent=T('무제한 모드 · 구조 제한은 유지됩니다'); meter.classList.remove('over'); }
  else { const rem=res.max-res.cost; meter.textContent=`${T('남은 포인트')} ${rem} / ${res.max}`; meter.classList.toggle('over',rem<0); }
  $('#custOrigin').value=d.origin;
  $('#custCity').value=d.city||'';
  document.querySelectorAll('#custEraSeg button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.e===d.era)));
  document.querySelectorAll('#custCircSeg button').forEach(b=>{
    const g=+b.dataset.c;
    b.setAttribute('aria-pressed',String(g===d.circuit));
    b.classList.toggle('free',g>=rng.circ[0]&&g<=rng.circ[1]);
  });
  const circCost=d.circuit>rng.circ[1]?(d.circuit-rng.circ[1])*3:0;
  $('#custCircHint').textContent=`${Sim.GR[rng.circ[0]]}–${Sim.GR[rng.circ[1]]} ${T('무료')}`+(circCost?` · +${circCost}pt`:'');
  for(const k of ['mana','lore','will','bond','health','wealth']){
    const row=$(`#custStats .cust-st[data-k="${k}"]`), [lo,hi]=rng.st[k], v=d.st[k];
    const inp=row.querySelector('input'); inp.value=v;
    row.querySelector('.v').textContent=v;
    const band=row.querySelector('.cust-band i'); band.style.left=lo+'%'; band.style.width=Math.max(2,hi-lo)+'%';
    const sc=v<lo?Math.ceil((lo-v)/5):v>hi?Math.ceil((v-hi)/5):0;
    const ce=row.querySelector('.c'); ce.textContent=sc?`+${sc}pt`:`${T('무료')} (${lo}–${hi})`; ce.classList.toggle('paid',sc>0);
  }
  const activeIds=Object.keys(d.arts).filter(id=>d.arts[id]>0);
  const mainId=d.main&&activeIds.includes(d.main)?d.main:(fam.find(id=>activeIds.includes(id))||activeIds[0]||null);
  d.main=mainId;
  document.querySelectorAll('#custArts .cust-art').forEach(el=>{
    const id=el.dataset.a, lv=d.arts[id]||0;
    el.querySelector('select').value=String(lv);
    el.querySelector('.fam').classList.toggle('hidden',!fam.includes(id));
    const r=el.querySelector('input[type=radio]'); r.disabled=!lv; r.checked=(mainId===id);
  });
  $('#custGift').value=d.gift;
  const gs=$('#custGiftGrSeg'), G=Sim.GIFTS[d.gift];
  gs.classList.toggle('hidden',!G);
  if(G){
    d.giftGr=Math.max(G.g[0],Math.min(G.g[1],d.giftGr||G.g[0]));
    gs.querySelectorAll('button').forEach(b=>{
      const g=+b.dataset.g, ok=g>=G.g[0]&&g<=G.g[1];
      b.disabled=!ok; b.style.opacity=ok?'':'0.35';
      b.setAttribute('aria-pressed',String(g===d.giftGr));
    });
  }
  const errs=d.on?res.errs:[];
  const eb=$('#custErrs'); eb.classList.toggle('hidden',!errs.length);
  eb.innerHTML=errs.map(e=>`<div>• ${esc(T(e))}</div>`).join('');
  $('#custSave').disabled=errs.length>0;
  const cb=$('#custBtn'); if(cb) cb.classList.toggle('on',custActive());
}
function custOpen(){
  custBuildOnce();
  CUST_D=custLoad();
  custRender();
  $('#custDlg').classList.remove('hidden');
}
function custClose(){ $('#custDlg').classList.add('hidden'); }
if($('#custDlg')){
  if($('#custBtn')) $('#custBtn').onclick=custOpen;
  $('#custOnSeg').addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b) return; CUST_D.on=b.dataset.on==='1'; custRender(); });
  $('#custModeSeg').addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b) return; CUST_D.mode=b.dataset.m; custRender(); });
  $('#custOrigin').addEventListener('change',e=>{
    const on=CUST_D.on, mode=CUST_D.mode, city=CUST_D.city, era=CUST_D.era, gift=CUST_D.gift, giftGr=CUST_D.giftGr;
    CUST_D=custDefault(e.target.value); CUST_D.on=on; CUST_D.mode=mode; CUST_D.city=city; CUST_D.era=era; CUST_D.gift=gift; CUST_D.giftGr=giftGr;
    custRender();
  });
  $('#custCity').addEventListener('change',e=>{ CUST_D.city=e.target.value; custRender(); });
  $('#custEraSeg').addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b) return; CUST_D.era=b.dataset.e; custRender(); });
  $('#custCircSeg').addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b) return; CUST_D.circuit=+b.dataset.c; custRender(); });
  $('#custStats').addEventListener('input',e=>{ const i=e.target.closest('input[data-st]'); if(!i) return; CUST_D.st[i.dataset.st]=+i.value; custRender(); });
  $('#custArts').addEventListener('change',e=>{
    const s=e.target.closest('select[data-art]');
    if(s){ const lv=+s.value; if(lv>0) CUST_D.arts[s.dataset.art]=lv; else delete CUST_D.arts[s.dataset.art]; custRender(); return; }
    const r=e.target.closest('input[name="custMain"]'); if(r){ CUST_D.main=r.value; custRender(); }
  });
  $('#custGift').addEventListener('change',e=>{ CUST_D.gift=e.target.value; const G=Sim.GIFTS[CUST_D.gift]; if(G) CUST_D.giftGr=G.g[0]; custRender(); });
  $('#custGiftGrSeg').addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b||b.disabled) return; CUST_D.giftGr=+b.dataset.g; custRender(); });
  $('#custReset').onclick=()=>{ const on=CUST_D.on, mode=CUST_D.mode; CUST_D=custDefault(CUST_D.origin); CUST_D.on=on; CUST_D.mode=mode; custRender(); };
  $('#custSave').onclick=()=>{
    if(CUST_D.on&&Sim.custCost(CUST_D).errs.length) return;
    if(CUST_D.on) store.set(K_CUST,Sim.custClamp(CUST_D));
    else store.set(K_CUST,{...Sim.custClamp(CUST_D),on:false});
    custClose();
    const cb=$('#custBtn'); if(cb) cb.classList.toggle('on',custActive());
    if(window.__lbCustRefresh) window.__lbCustRefresh();
  };
  document.addEventListener('click',e=>{ if(e.target.closest('#custX')||e.target.id==='custDlg') custClose(); });
  document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&!$('#custDlg').classList.contains('hidden')) custClose(); });
  { const cb=$('#custBtn'); if(cb) cb.classList.toggle('on',custActive()); }
}
"""

rp(
"function birth(){ window.__lbBirth=true; try{ Snd.bgm(null); }catch(e){} sndEndJ=false; gcEvent('born','태어나기'); store.del(K_SAVE); saveMark(null); const bid=bondPick(); Sim.newLife({len,sex:store.get(K_SEX)||null,bond:bid?{id:bid,p:bondChance(bid)}:null,moon:moonVow(),send:moonMark('_bbsend')}); Birth.run(()=>{ window.__lbBirth=false; ghLoad(); enterGame(true); Sim.start(); playClaim(null); }); }",
CUST_JS + "\nfunction birth(){ window.__lbBirth=true; try{ Snd.bgm(null); }catch(e){} sndEndJ=false; gcEvent('born','태어나기'); store.del(K_SAVE); saveMark(null); const bid=bondPick(); const cu=custForBirth(); Sim.newLife({len,sex:store.get(K_SEX)||null,bond:bid?{id:bid,p:bondChance(bid)}:null,moon:moonVow(),send:moonMark('_bbsend'),custom:cu}); Birth.run(()=>{ window.__lbBirth=false; ghLoad(); enterGame(true); Sim.start(); playClaim(null); }); }"
)

# 10. gsSend + end hook + renderPast
rp(
"function gsSend(r){ if(!API_OK||store.get(K_NOSTAT)||r.bond) return;",
"function gsSend(r){ if(!API_OK||store.get(K_NOSTAT)||r.bond||r.custom) return;"
)

rp(
"if(Sim.S&&Sim.S.flags&&Sim.S.flags.bondSummon) r.bond=1;",
"if(Sim.S&&Sim.S.flags&&Sim.S.flags.bondSummon) r.bond=1;\n    if(Sim.S&&Sim.S.custom) r.custom=1;"
)

rp(
"if(r.hero&&Sim.S&&Sim.S.hero&&!r.bond) gcEvent('servant-'+Sim.S.hero,",
"if(r.hero&&Sim.S&&Sim.S.hero&&!r.bond&&!r.custom) gcEvent('servant-'+Sim.S.hero,"
)

rp(
"""''; })()}<span class="badge">${rlab(r,k)}</span>""",
"""''; })()}${r.custom?'<span class="badge cust">커스텀</span>':''}<span class="badge">${rlab(r,k)}</span>"""
)

# 11. Lobby v2: TX.cust / TX.custSub / TX.custOn / TX.custBorn + .l2-custw + custRow() + refresh()
rp(
"scn:'시나리오',scnSub:'성배전쟁의 흐름을 바꾸는 사건 설정',",
"scn:'시나리오',scnSub:'성배전쟁의 흐름을 바꾸는 사건 설정',cust:'커스텀 마스터',custSub:'태어나기 전에 출신·능력치·기술 고르기',custOn:'커스텀 마스터 활성',custBorn:'커스텀 마스터',"
)
rp(
"scn:'Scenarios',scnSub:'Settings for events that reshape the Grail War',",
"scn:'Scenarios',scnSub:'Settings for events that reshape the Grail War',cust:'Custom Master',custSub:'Choose origin, stats, and arts before birth',custOn:'Custom Master active',custBorn:'Custom Master',"
)
rp(
"scn:'シナリオ',scnSub:'聖杯戦争の流れを変える出来事の設定',",
"scn:'シナリオ',scnSub:'聖杯戦争の流れを変える出来事の設定',cust:'カスタムマスター',custSub:'生まれる前に出身・能力値・技術を選ぶ',custOn:'カスタムマスター有効',custBorn:'カスタムマスター',"
)
rp(
"scn:'剧本',scnSub:'改变圣杯战争走向的事件设置',",
"scn:'剧本',scnSub:'改变圣杯战争走向的事件设置',cust:'自定义御主',custSub:'出生前选择出身、能力值与技术',custOn:'自定义御主已启用',custBorn:'自定义御主',"
)
rp(
"scn:'劇本',scnSub:'改變聖杯戰爭走向的事件設定',",
"scn:'劇本',scnSub:'改變聖杯戰爭走向的事件設定',cust:'自訂御主',custSub:'出生前選擇出身、能力值與技術',custOn:'自訂御主已啟用',custBorn:'自訂御主',"
)

rp(
"""    <div class="l2-bondw"></div>
    <div class="l2-scnw"></div>""",
"""    <div class="l2-bondw"></div>
    <div class="l2-custw"></div>
    <div class="l2-scnw"></div>"""
)

rp(
"    bondRow(); scnRow(); menu(st); sndUpd(); fitLinks(); }",
"    bondRow(); custRow(); scnRow(); menu(st); sndUpd(); fitLinks(); }"
)

rp(
"  function scnRow(){",
"  function custRow(){ const w=$2('.l2-custw'); if(!w) return; const on=typeof custActive==='function'&&custActive();\n"
"    w.innerHTML=`<button type=\"button\" class=\"l2-scn l2-cust\" aria-haspopup=\"dialog\">${I.scn}<span class=\"t\"><b></b><small></small></span><span class=\"go\" aria-hidden=\"true\">›</span></button>`;\n"
"    w.querySelector('b').textContent=TX.cust; w.querySelector('small').textContent=on?TX.custOn:TX.custSub; w.querySelector('button').onclick=()=>{ if(typeof custOpen==='function') custOpen(); };\n"
"    const bd=$2('.l2-bd'); if(bd) bd.textContent=on?TX.custBorn:TX.bornDesc; }\n"
"  window.__lbCustRefresh=custRow;\n"
"  function scnRow(){"
)

if miss:
    for x in miss:
        print('못 찾음', x)
    sys.exit(1)

open(P, 'w', encoding='utf-8').write(s)
print('custom1125 적용 끝')

# Update i18n if I18N_DICT is inline (dev/build/game.html), or external i18n files if released (public/index.html)
from custom_lines import D, T
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

import re
if re.search(r'const I18N_DICT=\{en:\{', s):
    import i18n
    s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, *_ in D], [(a, b, c) for a, b, c, *_ in T])
    open(P, 'w', encoding='utf-8').write(s)
    print('인라인 사전 추가', nd, nt)
else:
    # Patch external public/assets/i18n/{en,ja,zhs,zht}.js if present next to P
    import hashlib
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
