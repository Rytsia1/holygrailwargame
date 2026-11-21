// 검귀 루트 번역 시험: kg_test.js가 모은 문장(DUMP)을 tr()에 넣어 한글이 남는지 본다
// 사용: DUMP=파일 node dev/kg_test.js dev/build/game.html; node dev/kg_tr_test.js 파일 [en|ja|zhs|zht] [보여 줄 개수]
const {chromium}=require('playwright');const fs=require('fs');(async()=>{const L=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),lang=process.argv[3]||'en',SHOW=+process.argv[4]||30;
let s=fs.readFileSync('dev/build/game.html','utf8').replace('const _trc=new Map();','globalThis.__tr=s=>tr(s);\nconst _trc=new Map();');
fs.writeFileSync('dev/build/_k.html',s);
const b=await chromium.launch();const p=await b.newPage();await p.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());
await p.addInitScript(l=>{try{localStorage.setItem('cupnight.lang',JSON.stringify(l))}catch(e){}},lang);
await p.goto('file://'+process.cwd()+'/dev/build/_k.html');await p.waitForFunction(()=>typeof globalThis.__tr==='function'&&typeof Sim==='object');
await p.waitForTimeout(1500);
const bad=await p.evaluate(L=>{const H=/[가-힣]/;L=[...new Set(L.flatMap(t=>t.replace(/\uE000\w\uE001[^\uE001]*\uE001([^\uE001]*)\uE001([^\uE002]*)\uE002/g,'\n$1\n$2\n').split('\n').map(x=>x.trim()).filter(Boolean)))];return L.map(t=>[t,__tr(t)]).filter(([t,r])=>H.test(r));},L);
console.log(lang,'checked',L.length,'untranslated',bad.length);bad.slice(0,SHOW).forEach(([k,r])=>console.log(' ',k.slice(0,130),'\n    →',r.slice(0,130)));
fs.unlinkSync('dev/build/_k.html');await b.close()})()
