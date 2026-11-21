  // 11-22: 삶 · 성장 사건 선택지의 성향 변화 칩(「복수」 성향 ↑) — 선택지 함수의 lean('k',숫자)를 읽는다. 능력치 칩 뒤에 붙는다(end)
  const affChipsOf=f=>{ const m={}; (String(f||'').match(/lean\('\w+',\s*-?\d+\)/g)||[]).forEach(x=>{ const r=x.match(/lean\('(\w+)',\s*(-?\d+)\)/); if(r&&AFFN[r[1]]) m[r[1]]=(m[r[1]]||0)+(+r[2]); });
    const A=Object.keys(m).filter(k=>m[k]).map(k=>({l:`「${AFFN[k]}」 성향 ${m[k]>0?'↑':'↓'}`,c:'',end:1})); return A.length?A:undefined; };
