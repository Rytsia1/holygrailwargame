// 검귀 루트 화면 시험: 실제 화면(UI 훅)을 붙인 채 결말마다 전쟁 끝까지 돌리고 에필로그를 조금 진행해, 페이지 오류가 없는지 본다
// 사용: node dev/kg_ui_test.js [언어]
const {chromium}=require('playwright');const fs=require('fs'),vm=require('vm');(async()=>{const lang=process.argv[2]||'ko';
// 전쟁까지는 화면 없이(vm) 빠르게 가서 그 상태를 페이지에 불러온다
const src=fs.readFileSync('dev/build/game.html','utf8'),A=src.indexOf('<script id="sim">')+17,B=src.indexOf('</script>',A);
const ctx={console};ctx.globalThis=ctx;ctx.window=ctx;vm.createContext(ctx);vm.runInContext(src.slice(A,B)+';globalThis.Sim=Sim;',ctx);const VS=ctx.Sim;VS.setHooks(new Proxy({},{get:()=>()=>{}}));
const STATES=[];let sd=71;while(STATES.length<8){VS.newLife({seed:sd++,len:20});VS.start();let g=0;while(VS.S&&!VS.S.dead&&g++<400000&&!(VS.S.phase==='war'&&VS.S.war&&VS.S.war.heroAlive)){const S=VS.S;if(S.pending){VS.resolve(VS.autoChoice(S.pending));continue;}VS.tick(1);} if(VS.S.phase==='war'){ VS.S.pending=null; STATES.push(JSON.stringify(VS.S,(k,v)=>typeof v==='function'?undefined:v)); }}
let s=fs.readFileSync('dev/build/game.html','utf8').replace('  return {cn,ACH:','  globalThis.__T={kgStart,W:()=>S.war,S:()=>S};\n  return {cn,ACH:');
fs.writeFileSync('dev/build/_u.html',s);
const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message+' @ '+(e.stack||'').split('\n')[1]));
await p.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());
await p.addInitScript(l=>{try{localStorage.setItem('cupnight.lang',JSON.stringify(l))}catch(e){}},lang);
await p.goto('file://'+process.cwd()+'/dev/build/_u.html',{timeout:180000});await p.waitForFunction(()=>typeof Sim==='object'&&globalThis.__T);
const C=[['t','robin',10,{}],['b','robin',45,{'마지막 밤':'령주로 명한다'}],['m','robin',60,{},2],['s','robin',80,{}],['f','robin',80,{},0,1],['p','robin',50,{'흔적':'잔을 내려놓는다'}],['p2','robin',50,{'흔적':'잔을 내려놓는다','잔을 내려놓은 손':'잔의 빛으로'}],['x','robin',10,{},0,0,1]];
let ci=0;for(const [n,hero,R,pol,hp,bet,ally] of C){ const st=STATES[ci++];
 const r=await p.evaluate(({hero,R,pol,hp,bet,ally,st})=>{const T=globalThis.__T;Sim.load(JSON.parse(st));Sim.setHold(false);document.querySelectorAll('#cfx,.xfx').forEach(e=>e.remove());
  const toWar=sd=>{Sim.newLife({seed:sd,len:20});Sim.start();let g=0;while(Sim.S&&!Sim.S.dead&&g++<400000&&!(Sim.S.phase==='war'&&Sim.S.war&&Sim.S.war.heroAlive)){const S=Sim.S;if(S.pending){Sim.resolve(Sim.autoChoice(S.pending));continue;}Sim.tick(1);}return Sim.S.phase==='war';};
  const S=T.S(),w=T.W();S.hero=hero;S.aff.avenger=9;w.heroAlive=true;w.hp=90;w.sm=90;w.trust=80;w.seals=3;w.cupPure=true;w.rel={h:hero,track:'friend',stage:1,pt:50,open:1,pick:0,why:null};let a=null;
  for(const q of w.pairs){if(ally&&q.alive&&!q.ally&&!a){q.ally=true;q.pw=99;q.hp=100;a=q;}else if(q.alive&&q!==a){q.alive=false;q.hp=0;}} if(!ally)for(const q of w.pairs)q.ally=false; w.queue=[];S.pending=null;
  T.kgStart('avenger',null);const g=w.kg;g.R=R;g.lock=true;g.bet=!!bet;if(hp)w.hp=hp;if(ally)w.hp=3;
  let k=0;while(k++<200000){const S2=Sim.S;if(S2.dead||k>150000)break;if(S2.phase==='epi'&&S2.epi&&(S2.epi.k||0)>8)break;if(S2.pending){const d=S2.pending;let i=-1;const want=pol[d.title];if(want!=null)i=d.choices.findIndex(c=>!c.off&&c.t.startsWith(want));if(i<0)i=Sim.autoChoice(d);Sim.resolve(i);continue;}Sim.setHold(false);Sim.tick(1);}
  return [S.flags.kgEnd,S.flags.endFx,Sim.S.phase,Sim.S.dead];},{hero,R,pol,hp,bet,ally,st});
 await p.waitForTimeout(400);console.log(n,'→',JSON.stringify(r));}
console.log('오류',errs.length);errs.slice(0,10).forEach(e=>console.log(' ',e.slice(0,300)));
fs.unlinkSync('dev/build/_u.html');await b.close()})()
