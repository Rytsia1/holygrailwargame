// 검귀 루트 번역 시험: 결말마다 돌려 나온 기록 · 창 제목 · 본문 · 선택지를 tr()에 넣어 한글이 남는지 본다
// 사용: node dev/kg_tr_test.js [en|ja|zhs|zht] [보여 줄 개수]
const {chromium}=require('playwright');const fs=require('fs');(async()=>{const lang=process.argv[2]||'en',SHOW=+process.argv[3]||15;
let s=fs.readFileSync('dev/build/game.html','utf8');
s=s.replace('  return {cn,ACH:','  globalThis.__T={kgStart,W:()=>S.war,S:()=>S};\n  return {cn,ACH:').replace('const _trc=new Map();','globalThis.__tr=s=>tr(s);\nconst _trc=new Map();');
fs.writeFileSync('dev/build/_k.html',s);
const b=await chromium.launch();const p=await b.newPage();await p.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());
await p.addInitScript(l=>{globalThis.__FORCE_CRISIS=false;try{localStorage.setItem('cupnight.lang',JSON.stringify(l))}catch(e){}},lang);
await p.goto('file://'+process.cwd()+'/dev/build/_k.html');await p.waitForFunction(()=>typeof Sim==='object'&&Sim.HEROES&&globalThis.__T);
const out=await p.evaluate(()=>{const T=globalThis.__T,H=/[가-힣]/,bad={};let tot=0;
 const chk=(x,w)=>{if(!x||typeof x!=='string')return;for(const l of x.split('\n')){const t=l.trim();if(!t||!H.test(t))continue;tot++;const r=__tr(t);if(H.test(r))bad[t]=w+' → '+r.slice(0,60);}};
 function toWar(seed){Sim.newLife({seed,len:20});Sim.start();let g=0;while(Sim.S&&!Sim.S.dead&&g++<400000&&!(Sim.S.phase==='war'&&Sim.S.war&&Sim.S.war.heroAlive)){const S=Sim.S;if(S.pending){Sim.resolve(Sim.autoChoice(S.pending));continue;}Sim.tick(1);}return Sim.S.phase==='war';}
 function drive(pol,lim,stop){let g=0;while(g++<lim){const S=Sim.S;if(!S)break;if(stop&&stop(S))break;if(S.pending){const d=S.pending;chk(d.title,'title');chk(d.body,'body');(d.choices||[]).forEach(c=>{chk(c.t,'choice');chk(c.d,'desc');});let i=-1;const want=pol[d.title];if(want!=null)i=d.choices.findIndex(c=>!c.off&&c.t.startsWith(want));if(i<0)i=Sim.autoChoice(d);Sim.resolve(i);continue;}if(S.dead)break;Sim.tick(1);}}
 const C=[{hero:'robin',R:10},{hero:'robin',R:45,pol:{'마지막 밤':'령주로 명한다'}},{hero:'lancelot',R:45,pol:{'마지막 밤':'령주로 명한다'}},{hero:'arjuna',R:45,pol:{'마지막 밤':'령주로 명한다'}},{hero:'robin',R:80},{hero:'robin',R:60,hp:2},
  {hero:'robin',R:80,bet:true},{hero:'robin',R:80,bet:true,sus:2,pol:{'등 뒤':'령주로 멈춰라'}},{hero:'robin',R:50,pol:{'가까운 사람':'잔을 내려놓는다'}},{hero:'robin',R:50,trust:80,pol:{'흔적':'잔을 내려놓는다','잔을 내려놓은 손':'잔의 빛으로'}},
  {hero:'robin',R:10,ally:true},{hero:'robin',R:45,ally:true,pol:{'마지막 밤':'령주로 명한다'}},{hero:'alexander',R:10},{hero:'jeanne',R:45,pol:{'마지막 밤':'령주로 명한다'}},{hero:'mordred',R:50,pol:{'흔적':'잔을 내려놓는다'}}];
 const ks=['avenger','judge','cruel','taboo','zeal'];let seed=31;
 for(let ci=0;ci<C.length*2;ci++){const o=C[ci%C.length],k=ks[ci%5];while(!toWar(seed++));const S=T.S(),w=T.W();S.hero=o.hero;S.aff[k]=9;w.heroAlive=true;w.hp=90;w.sm=90;w.trust=o.trust??70;w.seals=3;w.cupPure=true;w.rel={h:o.hero,track:'friend',stage:ci%4,pt:50,open:1,pick:0,why:null};let a=null;
  for(const q of w.pairs){if(o.ally&&q.alive&&!q.ally&&!a){q.ally=true;a=q;}else if(q.alive&&q!==a){q.alive=false;q.hp=0;}} if(!o.ally)for(const q of w.pairs)q.ally=false; w.queue=[];S.pending=null;
  const n0=S.log.length;T.kgStart(k,null);const g=w.kg;g.R=o.R;g.lock=true;g.bet=!!o.bet;if(o.sus)g.sus=o.sus;if(o.hp)w.hp=o.hp;
  drive(o.pol||{},300000,null);
  S.log.slice(n0).forEach(e=>{if(e.k!=='q'&&e.k!=='delta'&&e.k!=='check')chk(e.t,e.k);});}
 return {tot,bad};});
const B=Object.entries(out.bad);console.log(lang,'checked',out.tot,'untranslated',B.length);B.slice(0,SHOW).forEach(([k,w])=>console.log(' ',w.split(' → ')[0],'|',k.slice(0,120),'\n     →',w.split(' → ')[1]));
fs.unlinkSync('dev/build/_k.html');await b.close()})()
