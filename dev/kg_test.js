// 검귀 루트 시험: node dev/kg_test.js <game.html> [이름]
// 결말마다 상황을 만들어 끝까지 돌리고, 오류 없이 끝나는지 · 원하는 결말이 나오는지 본다
const fs=require('fs'),vm=require('vm');const src=fs.readFileSync(process.argv[2],'utf8');const a=src.indexOf('<script id="sim">')+17,b=src.indexOf('</script>',a);
let code=src.slice(a,b).replace('  return {cn,ACH:','  globalThis.__T={finale,kgStart,kgEndX,relOf,W:()=>S.war,S:()=>S,H_BY,KG_EV,KG_AF,stayHome};\n  return {cn,ACH:');
const ctx={console};ctx.globalThis=ctx;ctx.window=ctx;vm.createContext(ctx);vm.runInContext(code+';globalThis.Sim=Sim;',ctx);
const Sim=ctx.Sim,T=ctx.__T;Sim.setHooks(new Proxy({},{get:()=>()=>{}}));
function toWar(seed){ Sim.newLife({seed,len:20});Sim.start();let g=0;while(Sim.S&&!Sim.S.dead&&g++<400000&&!(Sim.S.phase==='war'&&Sim.S.war&&Sim.S.war.heroAlive)){const S=Sim.S;if(S.pending){Sim.resolve(Sim.autoChoice(S.pending));continue;}Sim.tick(1);} return Sim.S.phase==='war'; }
// pol: {제목: 고를 선택(앞부분 일치)}
const SEEN=new Set(); const see=x=>{ if(typeof x==='string'&&/[가-힣]/.test(x)) x.split('\n').forEach(l=>{ l=l.trim(); if(l) SEEN.add(l); }); };
function drive(pol,lim=300000,stop){ let g=0; while(g++<lim){ const S=Sim.S; if(!S) break; if(stop&&stop(S)) break;
    if(S.pending){ const d=S.pending; see(d.title); see(d.body); (d.choices||[]).forEach(c=>{ see(c.t); see(c.d); }); let i=-1; const want=pol[d.title]; if(want!=null) i=d.choices.findIndex(c=>!c.off&&c.t.startsWith(want)); if(i<0) i=Sim.autoChoice(d); Sim.resolve(i); continue; }
    if(S.dead) break; Sim.tick(1); } }
let seed=11, bad=0;
const sel=process.argv[3];
function setup(o){ while(!toWar(seed++)); const S=T.S(), w=T.W(); S.hero=o.hero; S.aff=S.aff||{}; S.aff[o.k||'avenger']=9; w.heroAlive=true; w.hp=90; w.sm=90; w.trust=o.trust??70; w.seals=o.seals??3; w.cupPure=true;
  w.rel={h:o.hero,track:o.track||'friend',stage:o.stage??1,pt:50,open:1,pick:0,why:null};
  for(const p of w.pairs){ if(o.ally&&p.alive&&!p.ally&&!o._a){ p.ally=true; o._a=p; } else if(p.alive&&p!==o._a){ p.alive=false; p.hp=0; } }
  if(!o.ally) for(const p of w.pairs) if(p.ally) p.ally=false;
  w.queue=[]; w.ended=true; S.pending=null; return {S,w}; }
const C=[
 {n:'② 함께 간다',hero:'robin',R:10,want:'t'},
 {n:'③ 묶인 잔 → 에필로그 끝까지',hero:'robin',R:45,seals:3,pol:{'마지막 밤':'령주로 명한다'},want:'b',epi:true},
 {n:'③ 대마력 A가 버팀 → 결투',hero:'sigurd',R:45,seals:3,pol:{'마지막 밤':'령주로 명한다'},want:/[ms]/},
 {n:'③ 령주 없음 · 결심 52 → 결투',hero:'robin',R:52,seals:0,want:/[ms]/},
 {n:'① 막아선다',hero:'robin',R:80,want:/[ms]/},
 {n:'④ 등 뒤의 칼(의심 0)',hero:'robin',R:80,bet:true,want:'f'},
 {n:'④ 의심 2 · 령주 멈춰라 → 결투',hero:'robin',R:80,bet:true,sus:2,pol:{'등 뒤':'령주로 멈춰라'},want:/[mf]/},
 {n:'④ 의심 2 · 그대로 둔다',hero:'robin',R:80,bet:true,sus:2,pol:{'등 뒤':'그대로 둔다'},want:'f'},
 {n:'⑤ 둘째 날 지키고 잔을 내려놓는다 → 에필로그',hero:'robin',R:50,pol:{'가까운 사람':'잔을 내려놓는다'},want:'p',epi:true},
 {n:'⑤ 남긴다 → 함께 사는 생',hero:'robin',R:50,trust:80,pol:{'흔적':'잔을 내려놓는다','잔을 내려놓은 손':'잔의 빛으로'},want:'p',epi:true},
 {n:'② + 동맹 결전',hero:'robin',R:10,ally:true,want:/[tx]/,epi:true},
 {n:'③ + 동맹 결전',hero:'robin',R:45,ally:true,pol:{'마지막 밤':'령주로 명한다'},want:/[bx]/,epi:true},
 {n:'④ + 동맹(의심 2)',hero:'robin',R:80,bet:true,sus:2,ally:true,want:/[mf]/},
 {n:'① 마스터 승(서번트가 거의 쓰러진 채)',hero:'robin',R:60,hp:2,want:'m',epi:true},
 {n:'① + 동맹 동행',hero:'robin',R:80,ally:true,want:/[ms]/},
 {n:'말을 잃은 서번트 ③',hero:'lancelot',R:45,pol:{'마지막 밤':'령주로 명한다'},want:'b',epi:true},
];
for(const o of C){ if(sel&&!o.n.includes(sel)) continue;
  try{
    const {S,w}=setup(o); const n0=S.log.length;
    T.kgStart(o.k||'avenger',null); if(o.hp) w.hp=o.hp; const g=w.kg; g.R=o.R; g.lock=o.R!=null&&!o.free; g.bet=!!o.bet; if(o.sus) g.sus=o.sus;
    drive(o.pol||{},200000,S2=>S2.phase!=='war'||S2.dead);
    const end=S.flags.kgEnd; let ok=o.want instanceof RegExp?o.want.test(end||''):end===o.want;
    if(!ok&&o.ally&&S.dead&&!end){ ok=true; o.epi=false; console.log('  (동맹 결전에서 마스터가 쓰러짐 — 운에 따른 정상 결말)'); }
    let ep='';
    if(o.epi&&!S.dead){ const n1=S.log.length; drive(o.pol||{},900000); const ks=(S.epi&&S.epi.kgU)||[]; ep=` · 에필로그 ${S.dead?'끝('+S.age+'세 '+S.cause+')':'안 끝남'} · 검귀 사건 ${ks.length}개 [${ks.slice(0,8).join(' ')}]`; if(!S.dead) ok=false; }
    S.log.slice(n0).forEach(e=>{ if(!['q','delta','check'].includes(e.k)) see(e.t); });
    if(!ok) bad++;
    const F=S.flags; console.log(ok?'✓':'✗',o.n,'→',end,F.endFx||'',ep,['kgAllyFight','kgAllyWin','kgLastDone','kgGone','kgFree'].filter(k=>F[k]).join(','));
    if(process.env.V) S.log.slice(n0).forEach(e=>e.t&&console.log('   ',(e.k||'').padEnd(6),String(e.t).replace(/\n/g,' / ').slice(0,170)));
  }catch(e){ bad++; console.log('✗',o.n,'오류',e.stack.split('\n').slice(0,4).join(' | ')); }
}
console.log(bad?'실패 '+bad:'모두 통과');
if(process.env.DUMP) fs.writeFileSync(process.env.DUMP,JSON.stringify([...SEEN]));
