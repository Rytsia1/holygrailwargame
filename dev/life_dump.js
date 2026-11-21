// 생 전체 문장 모으기: node dev/life_dump.js <game.html> <생 수> <저장 파일>
// 화면 없이(vm) 자동 선택으로 생을 끝까지 돌려, 사건 제목 · 본문 · 선택지 · 기록 줄을 모은다 (번역 검사용: kg_tr_test.js에 넘긴다)
const fs=require('fs'),vm=require('vm');const src=fs.readFileSync(process.argv[2],'utf8');const a=src.indexOf('<script id="sim">')+17,b=src.indexOf('</script>',a);
const ctx={console};ctx.globalThis=ctx;ctx.window=ctx;vm.createContext(ctx);vm.runInContext(src.slice(a,b)+';globalThis.Sim=Sim;',ctx);
const Sim=ctx.Sim;Sim.setHooks(new Proxy({},{get:()=>()=>{}}));
const SEEN=new Set(),see=x=>{ if(typeof x==='string'&&/[가-힣]/.test(x)) x.split('\n').forEach(l=>{ l=l.trim(); if(l) SEEN.add(l); }); };
const N=+process.argv[3]||30;let kids=0;
for(let i=0;i<N;i++){ Sim.newLife({seed:5000+i*13,len:20});Sim.start();const S=Sim.S;let g=0;
  while(Sim.S&&g++<2000000){ const S2=Sim.S; if(S2.pending){ const d=S2.pending; see(d.title); see(d.body); (d.choices||[]).forEach(c=>{see(c.t);see(c.d);}); Sim.resolve(Sim.autoChoice(d)); continue; } if(S2.dead) break; Sim.tick(1); }
  (Sim.S.log||[]).forEach(e=>{ if(!['q','delta','check'].includes(e.k)) see(e.t); }); if((Sim.S.kids||[]).length||JSON.stringify(Sim.S.flags||{}).includes('kid')) kids++; }
fs.writeFileSync(process.argv[4],JSON.stringify([...SEEN]));console.log('생',N,'문장',SEEN.size,'아이 있는 생(추정)',kids);
