/* ===== 테스트 조절판 (테스트용 HTML에만 들어간다 · mktest.py) =====
   전투 보정 · 결투 보정 · 마스터 스탯 · 마술회로 · 성향 · 익힌 기술 · 서번트 상태 · 검귀 결심 · 시작 조건(서번트 · 위기 고정) · 빠른 배속.
   설정은 이 브라우저에만 남는다(cupnight.test.v1). */
(()=>{
const K='cupnight.test.v1', D={pow:0,dpow:0,dmgIn:1,dmgOut:1,hero:'',crisis:'nat'};
let T=Object.assign({},D); try{ Object.assign(T,JSON.parse(localStorage.getItem(K)||'{}')); }catch(e){}
const save=()=>{ try{ const {hook:_,...o}=T; localStorage.setItem(K,JSON.stringify(o)); }catch(e){} apply(); };
function apply(){ T.hook=hook; window.__TEST=T; window.__FORCE_HERO=T.hero||undefined; window.__FORCE_CRISIS=T.crisis==='nat'?undefined:T.crisis==='off'?false:T.crisis; badge(); }
const on=()=>T.pow!==0||T.dpow!==0||T.dmgIn!==1||T.dmgOut!==1||!!T.hero||T.crisis!=='nat';
// 받는 피해 · 주는 피해: 전투 중 체력이 줄어드는 만큼에 배율을 곱한다
function wrapHp(o,kind){ if(!o||o.__tw||typeof o.hp!=='number') return; let v=o.hp; Object.defineProperty(o,'__tw',{value:1,enumerable:false});
  Object.defineProperty(o,'hp',{enumerable:true,configurable:true,get(){ return v; },set(n){ const w=Sim.S&&Sim.S.war;
    if(w&&w.battle&&typeof n==='number'&&n<v){ if(kind==='me'&&T.dmgIn!==1) n=Math.max(0,v-(v-n)*T.dmgIn); else if(kind==='e'&&w.battle.e===o&&T.dmgOut!==1) n=Math.max(0,v-(v-n)*T.dmgOut); }
    v=n; }}); }
const wrapAll=()=>{ if(T.dmgIn===1&&T.dmgOut===1) return; const S=Sim.S, w=S&&S.war; if(!w) return; wrapHp(w,'me'); (w.pairs||[]).forEach(p=>wrapHp(p,'e')); ((w.crisis&&w.crisis.units)||[]).forEach(u=>wrapHp(u,'e')); };
setInterval(wrapAll,250);
// 엔진이 합마다 부른다: 이번 합의 나와 상대에 배율을 걸어 둔다
const hook=(w,e)=>{ if(T.dmgIn===1&&T.dmgOut===1) return; wrapHp(w,'me'); wrapHp(e,'e'); };
// ---- 화면 ----
const st=document.createElement('style'); st.textContent=`
#tpBtn{position:fixed;left:max(10px,env(safe-area-inset-left,0px));bottom:max(10px,env(safe-area-inset-bottom,0px));z-index:2147482000;font:600 12px/1 system-ui,sans-serif;padding:8px 11px;border-radius:999px;border:1px solid #6b5a8a;background:#1d1828ee;color:#d8cdf0;cursor:pointer}
#tpBtn.on{border-color:#e3c98d;color:#e3c98d}#tpBtn.on::after{content:" · 보정 켜짐"}
#tpPan{position:fixed;left:max(10px,env(safe-area-inset-left,0px));bottom:calc(max(10px,env(safe-area-inset-bottom,0px)) + 40px);z-index:2147482000;width:min(320px,calc(100vw - 20px));max-height:min(78vh,640px);overflow:auto;box-sizing:border-box;padding:12px 14px;border-radius:12px;border:1px solid #4a3f5e;background:#16121fef;color:#e8e2f2;font:13px/1.5 system-ui,-apple-system,'Malgun Gothic',sans-serif;box-shadow:0 10px 30px #0008}
#tpPan[hidden]{display:none}#tpPan h4{margin:12px 0 6px;font-size:12px;letter-spacing:.08em;color:#b6a8d4}#tpPan h4:first-child{margin-top:0}
#tpPan label{display:grid;grid-template-columns:1fr auto;gap:2px 8px;align-items:center;margin:4px 0}#tpPan label input[type=range]{grid-column:1/-1;width:100%}
#tpPan b{font-weight:600;color:#e3c98d;font-variant-numeric:tabular-nums}
#tpPan .g{display:grid;grid-template-columns:1fr 1fr;gap:4px 10px}#tpPan .g label{grid-template-columns:1fr 64px}
#tpPan input[type=number],#tpPan select{width:100%;box-sizing:border-box;background:#0f0c16;color:#eee;border:1px solid #3d3450;border-radius:6px;padding:3px 6px;font:inherit}
#tpPan .row{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}#tpPan button{font:inherit;font-size:12px;padding:4px 10px;border-radius:7px;border:1px solid #4a3f5e;background:#221c30;color:#e8e2f2;cursor:pointer}#tpPan button:hover{border-color:#e3c98d}
#tpPan .note{font-size:11.5px;color:#9b90b0;margin:4px 0 0}#tpPan .dim{opacity:.45;pointer-events:none}`;
document.head.appendChild(st);
const btn=document.createElement('button'); btn.id='tpBtn'; btn.type='button'; btn.textContent='테스트'; btn.setAttribute('data-notr','');
const pan=document.createElement('div'); pan.id='tpPan'; pan.hidden=true; pan.setAttribute('data-notr','');
const STL={mana:'마력',lore:'지식',will:'정신',bond:'관계',health:'건강'};
const HO=()=>Sim.HEROES.slice().sort((a,b)=>a.name.localeCompare(b.name,'ko')).map(h=>`<option value="${h.id}">${h.name} (${(Sim.CLS[h.cls]||{}).n||h.cls})</option>`).join('');
pan.innerHTML=`<h4>전투</h4>
<label>내 판정 보정 <b id="tpPowN"></b><input id="tpPow" type="range" min="-40" max="60" step="5"></label>
<label>내 서번트가 받는 피해 <b id="tpInN"></b><input id="tpIn" type="range" min="0" max="2" step="0.1"></label>
<label>적에게 주는 피해 <b id="tpOutN"></b><input id="tpOut" type="range" min="0.5" max="3" step="0.1"></label>
<label>마스터 대 서번트 결투 · 내 힘 보정 <b id="tpDpN"></b><input id="tpDp" type="range" min="-40" max="80" step="5"></label>
<h4>마스터</h4><div class="g" id="tpSt"></div><div class="g"><label>마술회로 (1 E ~ 5 A) <input type="number" id="tpCirc" min="1" max="5"></label></div>
<h4>성향</h4><div class="g" id="tpAff"></div>
<h4>익힌 기술 (계통별 단계)</h4><div id="tpArt"></div><p class="note">0 없음 · 1 입문 · 2 숙련 · 3 고위 · 4 비전. 바꾸면 곧바로 전투 · 결투 계산에 쓰인다(계통 수 제한은 무시).</p>
<h4>서번트</h4><div id="tpSv"><div class="row"><button type="button" id="tpFill">체력 · 마력 가득</button></div><div class="g"><label>신뢰 <input type="number" id="tpTrust" min="0" max="100"></label><label>령주 <input type="number" id="tpSeals" min="0" max="3"></label></div></div><p class="note" id="tpSvNote">성배전쟁 중에만 바꿀 수 있습니다.</p>
<h4>시작 조건 (다음 생부터)</h4>
<label style="grid-template-columns:1fr">소환될 서번트<select id="tpHero"><option value="">고정하지 않음</option>${HO()}</select></label>
<label style="grid-template-columns:1fr">후반 위기<select id="tpCx"><option value="nat">자연 (설정대로)</option><option value="off">없음</option><option value="black">검은 성배</option><option value="beast3R">비스트 Ⅲ/R</option></select></label>
<h4>검귀 루트</h4><div id="tpKg"><div class="g"><label style="grid-template-columns:1fr">성향<select id="tpKgK"><option value="avenger">복수</option><option value="judge">정의</option><option value="cruel">잔혹</option><option value="taboo">금기</option><option value="zeal">근원 집착</option></select></label><label>서번트 결심 <input type="number" id="tpKgR" min="0" max="100" value="50"></label></div><div class="row"><button type="button" id="tpKgGo">본성 속 진심으로 바로 들어가기</button></div><p class="note">성배전쟁 중(서번트 생존)에만. 서번트 결심 60 이상 ①④ · 35~59 ③ 령주 창 · 34 이하 ②. 동맹이 살아 있으면 동맹 결전이 먼저 온다.</p></div><div id="tpKgL" class="g"><label>지금 서번트 결심 <input type="number" id="tpKgNow" min="0" max="100"></label><label>의심 <input type="number" id="tpKgSus" min="0" max="3"></label></div><p class="note">검귀 루트 진행 중에만 바뀐다. 넷째 날 밤에 이 값으로 갈래가 정해진다.</p>
<h4>진행</h4><div class="row"><button type="button" data-sp="16">×16</button><button type="button" data-sp="32">×32</button><button type="button" data-sp="1">×1로</button></div>
<div class="row"><button type="button" id="tpReset">보정 모두 끄기</button></div>
<p class="note">이 조절판은 테스트용 파일에만 있습니다. 보정을 켠 채로 얻은 업적 · 기록도 이 브라우저에 그대로 남습니다.</p>`;
document.body.append(btn,pan);
const $=s=>pan.querySelector(s);
const fmt=()=>{ $('#tpPowN').textContent=(T.pow>0?'+':'')+T.pow; $('#tpDpN').textContent=(T.dpow>0?'+':'')+T.dpow; $('#tpInN').textContent='×'+(+T.dmgIn).toFixed(1); $('#tpOutN').textContent='×'+(+T.dmgOut).toFixed(1); };
function badge(){ btn.classList.toggle('on',on()); }
function fill(){ $('#tpPow').value=T.pow; $('#tpDp').value=T.dpow; $('#tpIn').value=T.dmgIn; $('#tpOut').value=T.dmgOut; $('#tpHero').value=T.hero||''; $('#tpCx').value=T.crisis; fmt(); live(); }
function live(){ const S=Sim.S; const g=$('#tpSt');
  if(!g.children.length) g.innerHTML=Object.entries(STL).map(([k,n])=>`<label>${n} <input type="number" data-k="${k}" min="0" max="100"></label>`).join('')+`<label>재산 <input type="number" data-k="wealth" min="0"></label>`;
  g.querySelectorAll('input').forEach(i=>{ if(document.activeElement===i) return; const k=i.dataset.k; i.value=!S?'':k==='wealth'?Math.round(S.wealth||0):Math.round((S.st||{})[k]||0); });
  const w=S&&S.war, wa=!!(w&&S.phase==='war'); $('#tpSv').classList.toggle('dim',!wa); $('#tpKg').classList.toggle('dim',!(wa&&w.heroAlive&&!w.kg)); $('#tpSvNote').hidden=wa;
  const AT=globalThis.__ARTT, ae=document.activeElement;
  if(AT){ const art=$('#tpArt');
    if(!art.children.length){ const BR={magic:'마술',church:'성당교회 비적',martial:'무투',gift:'초능력 · 마안'}, L=AT.list();
      art.innerHTML=Object.keys(BR).map(b=>`<div class="note" style="margin-top:6px">${BR[b]}</div><div class="g">`+L.filter(x=>x[2]===b).map(([k,n])=>`<label>${n} <select data-a="${k}">${[0,1,2,3,4].map(v=>`<option value="${v}">${v}</option>`).join('')}</select></label>`).join('')+'</div>').join(''); }
    const A=S?AT.get():{}; art.querySelectorAll('select').forEach(x=>{ if(x!==ae) x.value=String((A[x.dataset.a]&&A[x.dataset.a].lv)||0); }); art.classList.toggle('dim',!S);
    const af=$('#tpAff'); if(!af.children.length) af.innerHTML=[['avenger','복수'],['judge','정의'],['cruel','잔혹'],['taboo','금기'],['zeal','근원 집착']].map(([k,n])=>`<label>${n} <input type="number" data-f="${k}" min="0" max="20"></label>`).join('');
    const F=S?AT.aff():{}; af.querySelectorAll('input').forEach(x=>{ if(x!==ae) x.value=S?Math.round(F[x.dataset.f]||0):''; });
    if($('#tpCirc')!==ae) $('#tpCirc').value=S?AT.circ():'';
    const g=AT.kg(); $('#tpKgL').classList.toggle('dim',!g); if(g){ if($('#tpKgNow')!==ae) $('#tpKgNow').value=Math.round(g.R); if($('#tpKgSus')!==ae) $('#tpKgSus').value=g.sus||0; } }
  if(wa){ if(document.activeElement!==$('#tpTrust')) $('#tpTrust').value=Math.round(w.trust||0); if(document.activeElement!==$('#tpSeals')) $('#tpSeals').value=w.seals||0; } }
btn.onclick=()=>{ pan.hidden=!pan.hidden; if(!pan.hidden) fill(); };
setInterval(()=>{ if(!pan.hidden) live(); },800);
$('#tpPow').oninput=e=>{ T.pow=+e.target.value; fmt(); save(); };
$('#tpIn').oninput=e=>{ T.dmgIn=+e.target.value; fmt(); save(); };
$('#tpOut').oninput=e=>{ T.dmgOut=+e.target.value; fmt(); save(); };
$('#tpDp').oninput=e=>{ T.dpow=+e.target.value; fmt(); save(); };
$('#tpArt').addEventListener('change',e=>{ const x=e.target; if(x.dataset.a&&globalThis.__ARTT) globalThis.__ARTT.set(x.dataset.a,+x.value); });
$('#tpAff').addEventListener('change',e=>{ const x=e.target, AT=globalThis.__ARTT; if(x.dataset.f&&AT&&Sim.S) AT.aff()[x.dataset.f]=Math.max(0,+x.value||0); });
$('#tpCirc').onchange=e=>{ const AT=globalThis.__ARTT; if(AT&&Sim.S) AT.circ(Math.max(1,Math.min(5,+e.target.value||1))); };
$('#tpKgNow').onchange=e=>{ const g=globalThis.__ARTT&&globalThis.__ARTT.kg(); if(g) g.R=Math.max(0,Math.min(100,+e.target.value||0)); };
$('#tpKgSus').onchange=e=>{ const g=globalThis.__ARTT&&globalThis.__ARTT.kg(); if(g) g.sus=Math.max(0,Math.min(3,+e.target.value||0)); };
$('#tpHero').onchange=e=>{ T.hero=e.target.value; save(); };
$('#tpCx').onchange=e=>{ T.crisis=e.target.value; save(); };
$('#tpSt').addEventListener('change',e=>{ const i=e.target, S=Sim.S; if(!S||!i.dataset.k) return; const v=Math.max(0,+i.value||0); if(i.dataset.k==='wealth') S.wealth=v; else S.st[i.dataset.k]=Math.min(100,v); });
$('#tpFill').onclick=()=>{ const w=Sim.S&&Sim.S.war; if(!w) return; w.hp=100; w.sm=100; live(); };
$('#tpTrust').onchange=e=>{ const w=Sim.S&&Sim.S.war; if(w) w.trust=Math.max(0,Math.min(100,+e.target.value||0)); };
$('#tpSeals').onchange=e=>{ const w=Sim.S&&Sim.S.war; if(w) w.seals=Math.max(0,Math.min(3,+e.target.value||0)); };
pan.querySelectorAll('[data-sp]').forEach(b=>b.onclick=()=>{ if(Sim.S) Sim.S.speed=+b.dataset.sp; });
$('#tpKgGo').onclick=()=>{ const m=globalThis.__KGT&&globalThis.__KGT.start($('#tpKgK').value,+$('#tpKgR').value); if(m) alert(m); else pan.hidden=true; };
$('#tpReset').onclick=()=>{ T=Object.assign({},D); save(); fill(); };
apply();
})();
