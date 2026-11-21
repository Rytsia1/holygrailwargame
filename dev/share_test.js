// 「기록 복사」 문구 시험: 페이지에서 생을 몇 번 끝까지 돌려 기록을 만들고, 언어마다 shareText()에 한글이 남는지 본다
// 사용: node dev/share_test.js [생 수]   (public/ 사본으로 돌려 중국어 사전도 불러온다)
const {chromium}=require('playwright');const fs=require('fs');(async()=>{const N=+process.argv[2]||4;
fs.writeFileSync('public/_s.html',fs.readFileSync('dev/build/game.html','utf8').replace('function showEnding(r,fromHistory){','globalThis.__share=r=>shareText(r);\nfunction showEnding(r,fromHistory){'));
const b=await chromium.launch();const open=async lang=>{const p=await b.newPage();p.on('pageerror',e=>console.log('오류',lang,e.message));await p.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());
 await p.addInitScript(l=>{try{localStorage.setItem('cupnight.lang',JSON.stringify(l))}catch(e){}},lang);await p.goto('file://'+process.cwd()+'/public/_s.html',{timeout:180000});await p.waitForFunction(()=>typeof Sim==='object'&&typeof globalThis.__share==='function');await p.waitForTimeout(1200);return p;};
const p=await open('ko');
const recs=await p.evaluate(N=>{Sim.setHold&&Sim.setHold(false);for(let i=0;i<N;i++){Sim.newLife({seed:900+i*7,len:20});Sim.start();let g=0;while(Sim.S&&(!Sim.S.dead||Sim.S.pending)&&g++<900000){const S=Sim.S;if(S.pending){Sim.resolve(Sim.autoChoice(S.pending));continue;}Sim.tick(1);}}
 return {h:JSON.parse(localStorage.getItem('cupnight.history.v1')||'[]'),d:[Sim.S&&Sim.S.dead,Sim.S&&Sim.S.phase,Sim.S&&Sim.S.age],k:Object.keys(localStorage)};},N).then(x=>{console.log(JSON.stringify(x.d),x.k.join(' '));return x.h;});
console.log('기록',recs.length);if(recs[1]&&recs[1].hero){recs[1].last='Thank you.';recs[1].lastTo=recs[1].hero.name;}   // 마지막 말 줄도 본다
let bad=0;
console.log('--- ko\n'+await p.evaluate(r=>__share(r),recs[0]));await p.close();
for(const lang of ['en','ja','zhs','zht']){const q=await open(lang);
 const out=await q.evaluate(R=>R.map(r=>__share(r)),recs);
 out.forEach((t,i)=>{ const h=t.split('\n').filter(l=>/[가-힣]/.test(l)); if(h.length){bad++;console.log('한글 남음',lang,i,JSON.stringify(h));} });
 console.log('--- '+lang+'\n'+(process.env.ALL?out.join('\n\n'):out[0]));await q.close();}
fs.unlinkSync('public/_s.html');await b.close();console.log(bad?'한글 남은 기록 '+bad:'모두 옮겨짐')})()
