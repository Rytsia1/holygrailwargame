// 이미 이루어진 소원 시험: node dev/lw_test.js <game.html>
const fs=require('fs'),vm=require('vm');const src=fs.readFileSync(process.argv[2],'utf8');const a=src.indexOf('<script id="sim">')+17,b=src.indexOf('</script>',a);
let code=src.slice(a,b).replace('  return {cn,ACH:','  globalThis.__T={grantHero,relOf,W:()=>S.war,S:()=>S};\n  return {cn,ACH:');
const ctx={console};ctx.globalThis=ctx;ctx.window=ctx;vm.createContext(ctx);vm.runInContext(code+';globalThis.Sim=Sim;',ctx);
const Sim=ctx.Sim,T=ctx.__T;Sim.setHooks(new Proxy({},{get:()=>()=>{}}));
function toWar(seed){ Sim.newLife({seed,len:20});Sim.start();let g=0;while(Sim.S&&!Sim.S.dead&&g++<400000&&!(Sim.S.phase==='war'&&Sim.S.war&&Sim.S.war.heroAlive)){const S=Sim.S;if(S.pending){Sim.resolve(Sim.autoChoice(S.pending));continue;}Sim.tick(1);} return Sim.S.phase==='war'; }
let seed=1; const cases=[['suzuka','love',3,true,true],['frankenstein','love',3,true,true],['tamamo','love',3,true,true],['passionlip','love',3,true,true],['serenity','love',3,true,true],['melusine','love',3,true,true],['melusine','friend',3,true,true],
 ['suzuka','love',2,true,false],['suzuka','friend',3,true,false],['suzuka','love',3,false,false],['scathach','love',3,true,false],['tamamo','love',3,true,true,20]];
let bad=0;
for(const [id,track,stage,pure,expect,trust] of cases){
  while(!toWar(seed++));
  const S=T.S(), w=T.W(); S.hero=id; w.rel={h:id,track,stage,pt:90,open:1,pick:0,why:null}; w.cupPure=pure; w.cupKnown=true; w.trust=trust??92; w.heroAlive=true;
  const n0=S.log.length; S.flags.wishText='x';
  T.grantHero(null);
  const got=!!(S.flags.loveWish&&S.flags.stay===id&&S.flags.endFx==='loveWish');
  const lines=S.log.slice(n0).map(e=>e.t).filter(Boolean);
  if(got!==expect){ bad++; console.log('✗',id,track,stage,pure,'expected',expect,'got',got, S.flags.endFx); }
  else console.log('✓',id,track,stage,pure?'맑음':'검음',trust??92,'→',got?'수육':'다른 결말('+S.flags.endFx+')');
  if(got&&(id==='frankenstein'||id==='suzuka')) lines.slice(0,3).forEach(l=>console.log('    ',l.slice(0,140)));
  if(got) console.log('     기록:',S.flags.wishText);
}
console.log(bad?'실패 '+bad:'모두 통과');
