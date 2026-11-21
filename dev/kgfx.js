/* ---- 11-21: 검귀 루트 연출 — 본성 속 진심(진입) · 등 뒤의 칼 (시안 artifact 8KHJyg1AG3xAgahncqnQHL 7판) ----
   그림은 결말 연출(normalEndShow)의 맑은 성배 · 밤 · 빛의 수면 · 파동을 같은 식으로 그린다 */
function kgInFx(fx){ xfxGo('j_kg_in',()=>kgInShow(fx)); }
function kgBackFx(fx){ xfxGo('j_kg_back_'+(fx.v||'a'),()=>kgBackShow(fx)); }
// 그리기 도구: V(캔버스)에 묶는다
function kgPaint(V){ const {cl,seg,io,oc}=XF, c=V.c; let SHK=0;
  const P={
    get W(){ return V.W; }, get H(){ return V.H; }, get D(){ return V.D; },
    S_:()=>Math.min(V.W,V.H,640*V.D)/430,
    shk:()=>{ const s=SHK; SHK=0; return s; },
    kick:(t,at,amp,dur)=>{ if(t>=at&&t<at+dur) SHK+=amp*Math.pow(1-(t-at)/dur,2); },
    flash:(a,col='255,240,220')=>{ if(a>.01){ c.fillStyle=`rgba(${col},${Math.min(1,a)})`; c.fillRect(0,0,V.W,V.H); } },
    glow:(x,y,r,col,a)=>{ if(a<=.01||r<=0) return; const g=c.createRadialGradient(x,y,0,x,y,r); g.addColorStop(0,`rgba(${col},${Math.min(1,a)})`); g.addColorStop(1,`rgba(${col},0)`); c.fillStyle=g; c.fillRect(x-r,y-r,r*2,r*2); },
    wave:(x,y,k,maxR,col,w=10,sq=1)=>{ if(k<=0||k>=1) return; const D=V.D, r=oc(k)*maxR; c.save(); c.lineWidth=(w*(1-k)+1.5)*D; c.strokeStyle=`rgba(${col},${.9*(1-k)})`; c.shadowColor=`rgba(${col},1)`; c.shadowBlur=26*D*(1-k); c.beginPath(); c.ellipse(x,y,r,r*sq,0,0,Math.PI*2); c.stroke(); c.restore(); },
    sparks:(list,dt,a,col)=>{ const D=V.D; for(const e of list){ e.vy+=(e.g??-40)*D*dt; e.vx*=.985; e.x+=e.vx*dt; e.y+=e.vy*dt; e.l-=dt; if(e.l<=0) continue; c.beginPath(); c.arc(e.x,e.y,e.r,0,Math.PI*2); c.fillStyle=`rgba(${col},${Math.min(1,e.l)*a})`; c.fill(); } },
    burst:(n,x,y,v0,v1,up,seed,l0,l1,g)=>{ const R=XF.rng(seed), D=V.D; return [...Array(n)].map(()=>{ const a=R()*Math.PI*2, v=(v0+R()*(v1-v0))*D; return {x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v-up*D,r:(.8+R()*2)*D,l:l0+R()*(l1-l0),g}; }); },
    night:(a,t)=>{ const {W,H,D}=V; c.fillStyle=`rgba(8,8,20,${.95*a})`; c.fillRect(0,0,W,H); const vg=c.createRadialGradient(W/2,H*.45,Math.min(W,H)*.25,W/2,H*.45,Math.max(W,H)*.75); vg.addColorStop(0,'rgba(0,0,0,0)'); vg.addColorStop(1,`rgba(2,2,8,${.8*a})`); c.fillStyle=vg; c.fillRect(0,0,W,H);
      for(const s of KGX_STARS){ c.beginPath(); c.arc(s.x*W,s.y*H,s.r*D,0,Math.PI*2); c.fillStyle=`rgba(230,230,255,${a*(.35+.35*Math.sin(t*2+s.p))})`; c.fill(); } },
    pool:(t,top,a)=>{ if(a<=0) return; const {W,H,D}=V, sf=x=>top+(Math.sin(x/W*6+t*1.6)*5+Math.sin(x/W*15-t*2.2)*2)*D; c.save(); c.globalAlpha=a; c.beginPath(); c.moveTo(0,H); for(let x=0;x<=W;x+=6*D) c.lineTo(x,sf(x)); c.lineTo(W,H); c.closePath();
      const g=c.createLinearGradient(0,top,0,H); g.addColorStop(0,'rgba(255,220,150,.32)'); g.addColorStop(.3,'rgba(120,90,60,.18)'); g.addColorStop(1,'rgba(10,8,20,0)'); c.fillStyle=g; c.fill();
      c.beginPath(); for(let x=0;x<=W;x+=6*D){ const y=sf(x); x?c.lineTo(x,y):c.moveTo(x,y); } c.strokeStyle='rgba(255,230,170,.7)'; c.lineWidth=1.4*D; c.shadowColor='rgba(255,210,140,1)'; c.shadowBlur=12*D; c.stroke(); c.restore(); },
    cupPath:(cx,base,s)=>{ c.beginPath(); c.moveTo(cx-64*s,base-160*s);
      c.bezierCurveTo(cx-64*s,base-112*s,cx-40*s,base-80*s,cx-10*s,base-72*s); c.bezierCurveTo(cx-7*s,base-58*s,cx-6*s,base-34*s,cx-8*s,base-24*s); c.bezierCurveTo(cx-14*s,base-12*s,cx-40*s,base-9*s,cx-42*s,base);
      c.lineTo(cx+42*s,base); c.bezierCurveTo(cx+40*s,base-9*s,cx+14*s,base-12*s,cx+8*s,base-24*s); c.bezierCurveTo(cx+6*s,base-34*s,cx+7*s,base-58*s,cx+10*s,base-72*s); c.bezierCurveTo(cx+40*s,base-80*s,cx+64*s,base-112*s,cx+64*s,base-160*s); c.closePath(); },
    // 맑은 성배 (dim: 불이 꺼진 정도)
    cupLight:(cx,base,s,ig,col=[255,226,160],dim=0)=>{ const D=V.D, k=1-dim*.65; P.cupPath(cx,base,s); const g=c.createLinearGradient(cx-64*s,0,cx+64*s,0); g.addColorStop(0,`rgba(255,236,200,${.55*k})`); g.addColorStop(.2,`rgba(150,120,80,${.35*k})`); g.addColorStop(.6,`rgba(110,90,60,${.3*k})`); g.addColorStop(.88,`rgba(220,190,140,${.45*k})`); g.addColorStop(1,`rgba(255,245,220,${.7*k})`); c.fillStyle=g; c.fill();
      c.lineWidth=1.4*D; c.strokeStyle=`rgba(255,236,190,${.7*(1-dim*.5)})`; c.shadowColor='rgba(255,220,150,.9)'; c.shadowBlur=14*D*(1-dim); c.stroke(); c.shadowBlur=0;
      const rimY=base-160*s; c.beginPath(); c.ellipse(cx,rimY,63*s,9*s,0,0,Math.PI*2); const rg=c.createRadialGradient(cx,rimY,2*s,cx,rimY,63*s); rg.addColorStop(0,`rgba(255,255,240,${Math.min(1,ig)})`); rg.addColorStop(.4,`rgba(${col},${.8*Math.min(1,ig)})`); rg.addColorStop(1,`rgba(120,90,50,${.6*(1-dim*.6)})`); c.fillStyle=rg; c.fill();
      c.shadowColor=`rgba(${col},1)`; c.shadowBlur=26*D*ig; c.lineWidth=2.2*D; c.strokeStyle=`rgba(255,240,200,${Math.min(1,.9*ig+.25*(1-dim))})`; c.stroke(); c.shadowBlur=0; },
    // 손등의 령주: 그 생의 문양
    crest:(cx,cy,R,lit,a)=>{ const D=V.D; let pd; try{ pd=Sim.seal().p; }catch(e){ pd=['M12 40 C 24 50, 40 50, 52 40','M50 46 C 54 28, 44 14, 32 10','M14 46 C 10 28, 20 14, 32 10']; }
      c.save(); const sc=R*2/64; c.translate(cx-32*sc,cy-32*sc); c.scale(sc,sc); c.lineCap='round'; c.globalAlpha=a;
      pd.map(d=>new Path2D(d)).forEach((p,i)=>{ c.lineWidth=3.2; c.strokeStyle='rgba(150,104,116,.8)'; c.stroke(p); const k=lit[i]||0; if(k>0){ c.shadowColor=`rgba(255,60,80,${k})`; c.shadowBlur=14*D/sc*k; c.strokeStyle=`rgba(255,${90+80*k|0},${100+60*k|0},${k})`; c.lineWidth=2.6; c.stroke(p); c.shadowBlur=0; } }); c.restore(); } };
  return P; }
const KGX_STARS=(()=>{ const R=XF.rng(3); return [...Array(70)].map(()=>({x:R(),y:R()*.6,r:.4+R()*1.2,p:R()*6})); })();
// 글자: 제목 · 줄 · 부제 둘, 위쪽 한 줄(소원 · 지문)
function kgTxtH(title,sub,sub2){ const tt=title?tr(title):''; return `<div class="kgx-w"></div><div class="xd-txt"><div class="xd-d${[...tt].length>5?' long':''}">${[...tt].map(ch=>`<span>${ch===' '?'&nbsp;':esc(ch)}</span>`).join('')}</div><div class="xd-rule"></div><div class="xd-s">${esc(sub?tr(sub):'')}</div><div class="xd-s kgx-s2">${esc(sub2||'')}</div></div>`; }
function kgTxt(V){ const {seg,io,oc}=XF, o=V.o, CH=[...o.querySelectorAll('.xd-d span')], rule=o.querySelector('.xd-rule'), s1=o.querySelector('.xd-s'), s2=o.querySelector('.kgx-s2'), W=o.querySelector('.kgx-w');
  if(!CH.length) rule.style.display='none';
  let WC=[];
  return {
    setW(t){ W.innerHTML=kgWrap(W,t).map(l=>l.split(' ').map(w=>`<span class="ww">${[...w].map(ch=>`<span class="c">${esc(ch)}</span>`).join('')}</span>`).join(' ')).join('<br>'); WC=[...W.querySelectorAll('span.c')]; },
    red(on){ W.classList.toggle('red',on); },
    w(t,a,fadeAt,col){ const gap=Math.min(.06,1.2/Math.max(1,WC.length)), out=fadeAt==null?0:io(seg(t,fadeAt,fadeAt+.7)); W.style.opacity=(seg(t,a-.1,a+.1)*(1-out)).toFixed(3);
      WC.forEach((el,i)=>{ const k=seg(t,a+i*gap,a+i*gap+.4); el.style.opacity=oc(k).toFixed(3); el.style.textShadow=`0 0 ${(4+14*(1-k)).toFixed(1)}px rgba(${col},.9)`; }); },
    txt(t,a,s2At){ const gap=Math.min(.08,.9/Math.max(1,CH.length));
      CH.forEach((el,i)=>{ const k=seg(t,a+i*gap,a+i*gap+.55); el.style.opacity=oc(k).toFixed(3); el.style.filter=`blur(${((1-k)*9).toFixed(2)}px)`; el.style.transform=`translateY(${((1-oc(k))*6).toFixed(1)}px) scale(${(1+(1-k)*.18).toFixed(3)})`; });
      if(CH.length){ const r=oc(seg(t,a+.45,a+1.05)); rule.style.width=(r*Math.min(260,innerWidth*.6))+'px'; rule.style.opacity=r; }
      const s=oc(seg(t,a+(CH.length?.6:0),a+(CH.length?1.15:.55))); s1.style.opacity=s; s1.style.filter=`blur(${((1-s)*4).toFixed(2)}px)`;
      s2.style.opacity=s2At!=null?oc(seg(t,s2At,s2At+.5)):0; } }; }
// 줄바꿈: 한 줄에 다 들어가지 않으면 문장이 끝나는 자리에서 먼저 나누고, 그래도 길면 띄어쓰기에서만 넘어간다 (글자 중간에서 끊기지 않게)
function kgWrap(el,text){ try{ const st=getComputedStyle(el), cv=kgWrap.c||(kgWrap.c=document.createElement('canvas')), x=cv.getContext('2d'); x.font=`${st.fontSize} ${st.fontFamily}`;
  const maxW=Math.max(40,el.clientWidth-parseFloat(st.paddingLeft||0)-parseFloat(st.paddingRight||0))*.98, wd=t=>x.measureText(t).width;
  if(wd(text)<=maxW) return [text];
  const S=text.match(/[^.!?…。！？]+(?:[.!?…。！？]+[”’」』)]*)?\s*|[.!?…。！？]+\s*/g)||[text], L=[]; let cur='';
  for(const sn of S){ const nx=cur+sn; if(cur&&wd(nx.trim())>maxW){ L.push(cur.trim()); cur=sn; } else cur=nx; }
  if(cur.trim()) L.push(cur.trim()); return L; }catch(e){ return [text]; } }
const kgShake=(V,P)=>{ const s=P.shk(), cv=V.o.querySelector('canvas'); cv.style.transform=s>0?`translate(${((Math.random()-.5)*s).toFixed(1)}px,${((Math.random()-.5)*s).toFixed(1)}px)`:''; };
const kgQ=w=>{ const q=tr('“'+w+'.”'); return /[가-힣]/.test(q)&&LANG!=='ko'?(LANG==='ja'||LANG==='zht'?'「'+tr(w)+'」':'“'+tr(w)+'.”'):q; };

/* 본성 속 진심: 성배 선택 창의 줄들이 금빛으로 떴다가 흩어지고, 맨 아래 한 줄이 핏빛으로 다시 새겨진다 → 불 꺼진 잔 · 한 방울 · 나흘 (8.4초) */
function kgInShow(fx){
  const {seg,io,oc}=XF, lerp=(a,b,k)=>a+(b-a)*k, T=8.4, wish=fx.wish||'';
  const V=xfxOpen('kgx',tr('본성 속 진심'),kgTxtH('본성 속 진심','잔은 바닥만 젖었다.',tr('가득 차기까지 나흘.')),T,frame); fxSnd(V.o,'j_kg_in');
  const P=kgPaint(V), X=kgTxt(V); X.setW(kgQ(wish)); X.red(true);
  const L=(fx.lines&&fx.lines.length?fx.lines:['본성 속 진심: “'+wish+'”']).map(x=>tr(x)), n=L.length;
  const FS=(()=>{ try{ return getComputedStyle(document.documentElement).getPropertyValue('--f-story').trim()||'serif'; }catch(e){ return 'serif'; } })();
  function frame(t,dt){ const {c}=V, W=V.W, H=V.H, D=V.D; c.clearRect(0,0,W,H); const s=P.S_()*.85, cx=W/2, base=H*.53, inA=io(seg(t,0,.45)), out=io(seg(t,T-.6,T));
    const off=seg(t,1.6,2.3), top=H*.6;
    c.fillStyle=`rgba(4,4,10,${inA*(1-out)})`; c.fillRect(0,0,W,H);   // 뒤의 게임 화면이 비치지 않게
    c.save(); c.globalAlpha=1-out;
    P.night(inA,t); P.pool(t,top,inA*oc(seg(t,.1,.9))*(1-off*.7));
    P.glow(cx,H*.3,Math.max(W,H)*.5,'255,214,140',.22*seg(t,.2,.9)*(1-off));
    const red=seg(t,1.8,2.8); if(red>0){ const g=c.createRadialGradient(cx,H*.45,Math.min(W,H)*.22,cx,H*.45,Math.max(W,H)*.78); g.addColorStop(0,'rgba(0,0,0,0)'); g.addColorStop(1,`rgba(80,6,20,${.6*red})`); c.fillStyle=g; c.fillRect(0,0,W,H); }
    // 선택 창의 줄들 (맨 아래가 고른 줄)
    const fs=Math.max(12.5*D,Math.min(20*D,W*.03)), lh=fs*1.85, y0=H*.33-lh*(n-1)/2, yW=H*.12+fs*1.5;
    c.textAlign='center'; c.textBaseline='middle'; c.font=`${fs}px ${FS}`;
    L.forEach((l,i)=>{ const last=i===n-1; let a=seg(t,.25+i*.12,.7+i*.12), y=y0+i*lh, k=0;
      if(!last){ k=seg(t,1.6+i*.06,2.35+i*.06); a*=1-k; y-=k*lh*1.4; }
      else { y=lerp(y,yW,io(seg(t,1.9,2.5))); a*=1-seg(t,2.45,2.65); }
      if(a<=0) return;
      let fz=fs; const mw=c.measureText(l).width; if(mw>W*.92){ fz=fs*W*.92/mw; c.font=`${fz}px ${FS}`; }
      c.save(); c.globalAlpha=a*inA; c.fillStyle=last&&off>0?`rgba(255,${Math.round(241-150*off)},${Math.round(210-120*off)},1)`:'#fff1d2';
      c.shadowColor=last&&off>.3?'rgba(235,60,85,.9)':'rgba(255,220,150,.9)'; c.shadowBlur=(8+14*k)*D; if(k>0) c.filter=`blur(${(k*6).toFixed(1)}px)`; c.fillText(l,cx,y); c.restore(); c.font=`${fs}px ${FS}`; });
    // 불 꺼진 잔이 떠오르고 한 방울
    const R0=3.7, b=base+150*s*(1-oc(seg(t,R0,R0+1.1)));
    if(t>R0){ c.save(); c.globalAlpha*=inA*seg(t,R0,R0+.3); c.beginPath(); c.rect(0,0,W,top+6*D); c.clip(); P.cupLight(cx,b,s,.06,[230,90,110],.85); c.restore(); }
    const rimY=b-160*s, PD=4.9;
    if(t>=PD&&t<PD+.42){ const k=seg(t,PD+.05,PD+.4), y=lerp(yW+fs*.9,rimY,k*k), r=Math.max(2.5*D,3.4*s)*(t<PD+.05?seg(t,PD,PD+.05):1);
      P.glow(cx,y,r*5,'235,60,85',.5); c.fillStyle='rgba(255,120,135,.95)'; c.beginPath(); c.ellipse(cx,y,r*.8,r*1.5,0,0,Math.PI*2); c.fill(); }
    const wet=seg(t,PD+.4,PD+.8);
    if(wet>0){ c.save(); P.cupPath(cx,b,s); c.clip(); P.glow(cx,b-82*s,34*s,'230,50,75',.85*wet*(1-.25*seg(t,PD+1.4,PD+3))); c.restore();
      P.wave(cx,rimY,seg(t,PD+.4,PD+1.3),64*s,'235,80,100',6,.14); P.kick(t,PD+.4,3,.3); }
    // 나흘: 빈 마름모 넷
    const ny=b+19*s, gap=24*s, Q=PD+1.2;
    for(let i=0;i<4;i++){ const a=seg(t,Q+i*.32,Q+.3+i*.32); if(a<=0) continue; const x=cx+(i-1.5)*gap, r=5.5*s*(.6+.4*oc(a));
      c.save(); c.globalAlpha*=a; c.strokeStyle='rgba(255,226,170,.9)'; c.lineWidth=1.3*D; c.shadowColor='rgba(255,210,140,.9)'; c.shadowBlur=8*D*(1-a*.5); c.beginPath(); c.moveTo(x,ny-r); c.lineTo(x+r,ny); c.lineTo(x,ny+r); c.lineTo(x-r,ny); c.closePath(); c.stroke(); c.restore(); }
    c.restore();
    X.w(t,2.6,T-.6,'235,60,85'); X.txt(t,Q+.4,Q+1.2); V.o.querySelector('.xd-txt').style.opacity=(1-out).toFixed(3); kgShake(V,P); }
}

/* 등 뒤의 칼: 가득 찬 잔 · 등 뒤의 온기 → 정적 · 칼빛 → 칼이 가른다. a 즉시 암전 / b 령주로 멈춰라 / c 알면서 둔다 / h 동맹 앞에서 칼이 먼저 닿는다 */
function kgBackShow(fx){
  const {seg,io,oc}=XF, lerp=(a,b,k)=>a+(b-a)*k, pulse=(t,at,w)=>Math.exp(-Math.pow((t-at)/w,2)), v=fx.v||'a';
  const T={a:6.0,b:6.6,c:6.2,h:3.8}[v]||6;
  const top0=v==='c'?'알고 있었다. 그래도 돌아보지 않았다.':'등 뒤의 온기가 한 걸음 가까워졌다.';
  const sub={a:'당신의 시점은 거기서 끊겼다.',b:'칼끝이 목 한 뼘 앞에서 멈췄다.',c:'끝까지, 당신이 고른 대로.',h:'등 뒤에서 칼이 먼저 닿았다.'}[v];
  const V=xfxOpen('kgx',tr('등 뒤의 칼'),kgTxtH('',sub,v==='b'&&fx.line?tr(fx.line):''),T,frame); fxSnd(V.o,'j_kg_back_'+v);
  const P=kgPaint(V), X=kgTxt(V); X.setW(tr(top0));
  const DU=(()=>{ const R=XF.rng(11); return [...Array(80)].map(()=>({x:R(),y:R(),r:R(),v:.3+R()*.7})); })(); let SH=null;
  const lit=[0,0,0], si=Math.max(0,Math.min(2,fx.i??1));
  function frame(t,dt){ const {c}=V, W=V.W, H=V.H, D=V.D; c.clearRect(0,0,W,H); const s=P.S_(), cx=W/2, base=H*.6, top=H*.6;
    const FZ=v==='b'?2.05:99, tf=Math.min(t,FZ), frozen=v==='b'?seg(t,2.05,2.35):0, inA=io(seg(t,0,.35)), hush=seg(t,1.4,1.6);
    c.fillStyle=`rgba(4,4,10,${inA})`; c.fillRect(0,0,W,H);
    P.night(inA,tf); P.pool(hush>0?Math.min(tf,1.5):tf,top,inA);
    c.save(); c.beginPath(); c.rect(0,0,W,top+6*D); c.clip(); P.cupLight(cx,base,s,(1.15+.18*Math.sin(Math.min(tf,1.5)*5))*inA); c.restore();
    P.glow(cx,base-150*s,230*s,'255,220,150',.45*inA);
    const warm=seg(tf,0,1.4)*(v==='c'?1:1-hush*.6); if(warm>0) P.glow(cx,H*1.08,H*(.5+.35*seg(tf,0,1.4)),'255,170,90',.55*warm);
    // 칼빛 반짝임
    const gl=seg(t,1.5,1.6)*(1-seg(t,1.72,1.95));
    if(gl>0){ const x=W*.86,y=H*.12, r=26*s*gl; c.save(); c.globalAlpha=gl; c.strokeStyle='rgba(225,240,255,1)'; c.lineWidth=1.2*D; c.shadowColor='rgba(200,230,255,1)'; c.shadowBlur=14*D;
      c.beginPath(); c.moveTo(x-r,y); c.lineTo(x+r,y); c.moveTo(x,y-r*.7); c.lineTo(x,y+r*.7); c.stroke(); c.restore(); P.glow(x,y,r*1.6,'200,225,255',.5*gl); }
    // 칼
    const ax=W*1.05, ay=-H*.05, bx=-W*.05, by=H*1.02, S0=1.95, sk=v==='b'?Math.min(seg(t,S0,S0+.25),.46):seg(t,S0,S0+.25);
    if(t>=S0&&!(v==='a'&&t>=2.2)&&!(v==='c'&&t>3.4)&&!(v==='h'&&t>2.9)){ const hx=lerp(ax,bx,sk), hy=lerp(ay,by,sk), k0=Math.max(0,sk-(v==='b'?.32:.45)), tx=lerp(ax,bx,k0), ty=lerp(ay,by,k0), fa=v==='h'?1-seg(t,2.4,2.9):1;
      c.save(); c.globalAlpha=fa; c.lineCap='round'; c.strokeStyle='rgba(220,40,60,.35)'; c.lineWidth=16*s; c.shadowColor='rgba(255,60,80,1)'; c.shadowBlur=30*D; c.beginPath(); c.moveTo(tx,ty); c.lineTo(hx,hy); c.stroke(); c.restore();
      const g=c.createLinearGradient(tx,ty,hx,hy); g.addColorStop(0,'rgba(160,20,40,0)'); g.addColorStop(.7,'rgba(230,60,80,.7)'); g.addColorStop(1,'rgba(255,248,248,1)');
      c.save(); c.globalAlpha=fa; c.strokeStyle=g; c.lineWidth=4.5*s; c.lineCap='round'; c.beginPath(); c.moveTo(tx,ty); c.lineTo(hx,hy); c.stroke();
      c.strokeStyle='rgba(255,255,255,.95)'; c.lineWidth=1.4*s; c.shadowColor='rgba(220,235,255,1)'; c.shadowBlur=10*D; c.beginPath(); c.moveTo(lerp(tx,hx,.55),lerp(ty,hy,.55)); c.lineTo(hx,hy); c.stroke(); c.restore(); }
    if(v!=='b'){ P.kick(t,2.12,v==='h'?14:10,.35); P.flash(pulse(t,2.15,.05)*.3,'255,235,235'); }
    if(v==='h'){ const hit=seg(t,2.15,2.3)*(1-seg(t,2.6,3.6)); if(hit>0){ const g=c.createRadialGradient(cx,H*.5,Math.min(W,H)*.15,cx,H*.5,Math.max(W,H)*.75); g.addColorStop(0,'rgba(0,0,0,0)'); g.addColorStop(1,`rgba(150,10,30,${.7*hit})`); c.fillStyle=g; c.fillRect(0,0,W,H); } }
    // 령주로 멈춰라: 색이 빠지고 빛가루가 멎고 령주 한 획이 타오른다
    if(v==='b'&&t>=2.05){ c.save(); c.globalCompositeOperation='saturation'; c.fillStyle=`rgba(128,128,128,${.85*frozen})`; c.fillRect(0,0,W,H); c.restore();
      c.fillStyle=`rgba(16,22,38,${.28*frozen})`; c.fillRect(0,0,W,H);
      DU.forEach(p=>{ c.fillStyle=`rgba(220,232,250,${.55*frozen*p.v})`; c.beginPath(); c.arc(p.x*W,p.y*H,D*(.6+p.r*1.4),0,Math.PI*2); c.fill(); });
      const sx=W*.2, sy=H*.7, R=Math.min(58*s,W*.12), burn=seg(t,2.12,2.5)*(1-.6*seg(t,3.4,5.5));
      P.glow(sx,sy,R*2.6,'230,40,70',.5*seg(t,2.12,2.5)); lit[si]=burn; P.crest(sx,sy,R,lit,seg(t,2.1,2.3));
      P.wave(sx,sy,seg(t,2.15,3.2),Math.max(W,H)*.8,'255,70,90',10,1); P.kick(t,2.06,7,.3); P.flash(pulse(t,2.08,.05)*.3,'255,90,110'); }
    // 암전
    let black=0; if(v==='a') black=t>=2.2?1:0; if(v==='c') black=io(seg(t,2.25,3.45)); black=Math.max(black,io(seg(t,T-.5,T))*(v==='b'||v==='h'?1:0));
    if(black>0){ c.fillStyle=`rgba(0,0,0,${black})`; c.fillRect(0,0,W,H); }
    if(v==='a'&&t>=2.2){ const k=seg(t,2.2,2.9); if(k<1){ c.save(); c.fillStyle=`rgba(230,50,70,${.95*(1-k)})`; c.shadowColor='rgba(255,60,80,1)'; c.shadowBlur=10*D; c.fillRect(0,H*.5-D,W*oc(seg(t,2.2,2.34)),Math.max(1,1.5*D)); c.restore(); }
      if(t>=3.7){ if(!SH) SH=P.burst(46,cx,base-160*s,40,170,90,23,1.6,2.6,420); c.save(); c.globalCompositeOperation='lighter'; P.sparks(SH,dt,1,'255,214,150'); c.restore(); P.glow(cx,base-160*s,60*s,'255,214,150',.25*pulse(t,3.75,.15)); } }
    X.w(t,.25,v==='c'?2.6:1.7,'255,220,150'); X.txt(t,{a:2.75,b:2.6,c:3.6,h:2.5}[v]??2.6,v==='b'?4.2:null); kgShake(V,P); }
}

/* ---- 11-21 2차: 날마다 바뀌는 카드 · 잔이 가득 차는 순간 · 결투 시작 (시안 9판) ---- */
function kgDayFx(fx){ xfxGo('j_kg_day'+(fx.d||1),()=>kgDayShow(fx)); }
function kgFullFx(fx){ xfxGo(fx.v==='g'?'j_kg_full_g':'j_kg_full_r',()=>kgFullShow(fx)); }
function kgDuelFx(fx){ xfxGo('j_kg_duel',()=>kgDuelShow(fx)); }
// 잔 속에 고인 것: frac 0~1 (몸통 바닥 → 입구)
function kgBowl(V,P,cx,base,s,frac,col,a){ const c=V.c, top=base-160*s, bot=base-72*s, y=bot-(bot-top)*frac; c.save(); P.cupPath(cx,base,s); c.clip();
  const g=c.createLinearGradient(0,y,0,bot); g.addColorStop(0,`rgba(${col},${.95*a})`); g.addColorStop(1,`rgba(${col},${.6*a})`); c.fillStyle=g; c.fillRect(cx-70*s,y,140*s,bot-y+2);
  c.strokeStyle=`rgba(255,200,205,${.7*a})`; c.lineWidth=1.2*V.D; c.beginPath(); c.ellipse(cx,y,Math.max(4,(64-56*Math.max(0,(y-top)/(bot-top)))*s),3*s,0,0,Math.PI*2); c.stroke(); c.restore(); }
function kgDiam(V,cx,y,s,lit,newA,empty){ const c=V.c, D=V.D, gap=24*s; for(let i=0;i<4;i++){ const x=cx+(i-1.5)*gap, r=5.5*s, on=!empty&&i<lit, nw=i===lit-1; c.save();
  c.beginPath(); c.moveTo(x,y-r); c.lineTo(x+r,y); c.lineTo(x,y+r); c.lineTo(x-r,y); c.closePath();
  if(on){ const a=nw?newA:1; c.fillStyle=`rgba(230,60,85,${.9*a})`; c.shadowColor='rgba(255,70,90,1)'; c.shadowBlur=(nw?14:6)*D*a; c.fill(); }
  c.strokeStyle='rgba(255,226,170,.85)'; c.lineWidth=1.2*D; c.shadowBlur=0; c.stroke(); c.restore(); } }

/* 날 카드: 작은 「진심」 · 불 꺼진 잔에 하루치 핏빛이 차오르고 오늘의 마름모가 켜진다 (2.7초) */
function kgDayShow(fx){
  const {seg,io,oc}=XF, lerp=(a,b,k)=>a+(b-a)*k, T=2.7, d=Math.max(1,Math.min(4,fx.d||1)), DN=['첫째 날','둘째 날','셋째 날','넷째 날'];
  const V=xfxOpen('kgx',`${tr('진심')} · ${tr(DN[d-1])}`,kgTxtH(DN[d-1],fx.ev||''),T,frame); fxSnd(V.o,'j_kg_day'+d);
  const P=kgPaint(V), X=kgTxt(V), FS=(()=>{ try{ return getComputedStyle(document.documentElement).getPropertyValue('--f-story').trim()||'serif'; }catch(e){ return 'serif'; } })();
  function frame(t,dt){ const {c}=V, W=V.W, H=V.H, D=V.D; c.clearRect(0,0,W,H); const s=P.S_()*.8, cx=W/2, base=H*.56, inA=io(seg(t,0,.3)), out=io(seg(t,T-.4,T));
    c.save(); c.globalAlpha=1-out; c.fillStyle=`rgba(4,4,10,${inA})`; c.fillRect(0,0,W,H); P.night(inA*.8,t);
    P.glow(cx,base-110*s,170*s,'200,40,70',.18*inA);
    c.save(); c.globalAlpha*=inA; c.textAlign='center'; c.textBaseline='middle'; c.font=`${Math.max(12*D,15*s)}px ${FS}`; c.fillStyle='rgba(240,160,170,.85)'; c.shadowColor='rgba(235,60,85,.8)'; c.shadowBlur=8*D; c.fillText([...tr('진심')].join(LANG==='en'?'':'  '),cx,H*.13); c.restore();
    c.save(); c.globalAlpha*=inA; P.cupLight(cx,base,s,.05,[230,90,110],.85); c.restore();
    const fr=lerp((d-1)/4,d/4,io(seg(t,.4,1.4))); if(fr>0) kgBowl(V,P,cx,base,s,fr,'200,30,55',inA);
    if(t>1.3) P.wave(cx,base-160*s+(1-fr)*88*s,seg(t,1.3,2.1),60*s,'235,80,100',5,.15);
    kgDiam(V,cx,base+19*s,s,d,seg(t,1.25,1.5)); c.restore();
    X.txt(t,1.0); V.o.querySelector('.xd-txt').style.opacity=(1-out).toFixed(3); }
}

/* 잔이 가득 차는 순간: r 본성에 삼켜진다(붉게 넘침) / g 흘러넘치던 본성이 고요해졌다(금빛으로 가라앉음) (4.6초) */
function kgFullShow(fx){
  const {seg,io,oc}=XF, lerp=(a,b,k)=>a+(b-a)*k, pulse=(t,at,w)=>Math.exp(-Math.pow((t-at)/w,2)), T=4.6, g0=fx.v==='g';
  const V=xfxOpen('kgx',tr('넷째 날 밤'),kgTxtH('넷째 날 밤',g0?'잔이 가득 찼다.':'본성에 삼켜진다.',g0?tr('흘러넘치던 본성이 고요해졌다.'):''),T,frame); fxSnd(V.o,g0?'j_kg_full_g':'j_kg_full_r');
  const P=kgPaint(V), X=kgTxt(V); let SP=null;
  if(!g0) V.o.querySelector('.xd-rule').style.background='linear-gradient(90deg,transparent,rgba(230,70,90,.95),transparent)';
  else V.o.querySelector('.xd-rule').style.background='linear-gradient(90deg,transparent,rgba(240,200,130,.95),transparent)';
  function frame(t,dt){ const {c}=V, W=V.W, H=V.H, D=V.D; c.clearRect(0,0,W,H); const s=P.S_()*.9, cx=W/2, base=H*.58, inA=io(seg(t,0,.4)), top=H*.6, out=io(seg(t,T-.5,T));
    c.save(); c.globalAlpha=1-out; c.fillStyle=`rgba(4,4,10,${inA})`; c.fillRect(0,0,W,H); P.night(inA,t); P.pool(t,top,inA*.8);
    const FULL=1.6, fr=lerp(.75,1,io(seg(t,.3,FULL))), gold=g0?seg(t,FULL,FULL+.5):0;
    const col=gold>0?`${Math.round(200+55*gold)},${Math.round(30+180*gold)},${Math.round(55+75*gold)}`:'200,30,55';
    c.save(); c.beginPath(); c.rect(0,0,W,top+6*D); c.clip();
    const ig=t<FULL?.05:(!g0?.05+1.1*seg(t,FULL,FULL+.3):.05+.9*gold); P.cupLight(cx,base,s,ig,!g0?[255,80,100]:[255,226,160],.85*(1-gold));
    kgBowl(V,P,cx,base,s,fr,col,inA); c.restore();
    const rimY=base-160*s;
    if(!g0&&t>=FULL){ const L=io(seg(t,FULL,FULL+1.3)); c.save(); c.globalCompositeOperation='lighter'; c.lineCap='round';
      for(const sd of [-1,1]) for(const off of [0,.35,.7]){ const k=Math.max(0,L-off*.3); if(k<=0) continue; c.strokeStyle=`rgba(255,90,110,${.75*(1-seg(t,3.4,4.4))})`; c.lineWidth=(3-off*2)*s; c.shadowColor='rgba(255,60,80,1)'; c.shadowBlur=12*D;
        c.beginPath(); for(let q=0;q<=k;q+=.02){ const yy=rimY+q*(base-rimY); const ww=yy<base-72*s?(64-54*Math.pow((yy-rimY)/(88*s),1.6))*s:(10+32*Math.pow(Math.max(0,(yy-(base-72*s))/(72*s)),3))*s; const x=cx+sd*(ww+2*s+off*3*s); q?c.lineTo(x,yy):c.moveTo(x,yy); } c.stroke(); }
      c.restore();
      if(!SP) SP=P.burst(60,cx,rimY,60,260,180,31,1.0,1.8,-60); c.save(); c.globalCompositeOperation='lighter'; P.sparks(SP,dt,1,'255,110,125'); c.restore();
      P.glow(cx,rimY,150*s,'235,50,75',.5*seg(t,FULL,FULL+.2)*(1-.5*seg(t,2.4,4.4)));
      P.wave(cx,rimY,seg(t,FULL,FULL+1.0),Math.max(W,H)*.6,'255,80,100',12,.35); P.kick(t,FULL,8,.4); P.flash(pulse(t,FULL+.02,.06)*.35,'255,120,130'); }
    if(g0&&t>=FULL){ P.glow(cx,rimY,170*s,'255,220,150',.45*gold*(1-.4*seg(t,3,4.6))); P.wave(cx,rimY,seg(t,FULL+.1,FULL+1.6),Math.max(W,H)*.5,'255,226,170',8,.35); }
    c.restore();
    X.txt(t,2.2,g0?3.0:null); V.o.querySelector('.xd-txt').style.opacity=(1-out).toFixed(3); kgShake(V,P); }
}

/* 결투 시작: 서번트 초상이 돌아서서 당신을 본다 · 테두리가 핏빛으로 금 간다 · 칼이 세워진다 · 첫마디 (5.4초) */
function kgDuelShow(fx){
  const {seg,io,oc}=XF, T=5.4;
  const V=xfxOpen('kgx',`${tr(fx.name||'')} · ${tr('나의 서번트였던 자')}`,kgTxtH(fx.name||'',`${tr('나의 서번트였던 자')}${fx.cls?' · '+tr(fx.cls):''}`,tr('서번트가 당신의 앞을 막아섰다.')),T,frame); fxSnd(V.o,'j_kg_duel');
  const P=kgPaint(V), X=kgTxt(V); X.setW(fx.line?kgLine(fx.line):''); X.red(true);
  const img=new Image(); img.src=`assets/portraits/${fx.id}.webp`;
  function frame(t,dt){ const {c}=V, W=V.W, H=V.H, D=V.D; c.clearRect(0,0,W,H); const s=P.S_(), cx=W/2, top=H*.62, inA=io(seg(t,0,.4)), out=io(seg(t,T-.5,T));
    c.save(); c.globalAlpha=1-out; c.fillStyle=`rgba(4,4,10,${inA})`; c.fillRect(0,0,W,H); P.night(inA,t); P.pool(t,top,inA*.7);
    P.glow(cx,-H*.1,H*.75,'235,60,85',.28*inA);
    const R=Math.min(58*s,W*.15), px=cx, py=H*.4, ap=oc(seg(t,.2,.8)), fl=seg(t,1.1,1.55), sx=Math.cos(Math.PI*fl), red=seg(t,1.3,1.6), crack=seg(t,1.45,1.7);
    const bl=oc(seg(t,1.6,2.0));
    if(bl>0){ const bx=px+R*.95, by0=py+R*.5, by1=Math.max(H*.27,py+R*.3-(R*1.9)*bl); c.save(); c.lineCap='round'; c.strokeStyle='rgba(220,40,60,.35)'; c.lineWidth=10*s; c.shadowColor='rgba(255,60,80,1)'; c.shadowBlur=24*D; c.beginPath(); c.moveTo(bx,by0); c.lineTo(bx,by1); c.stroke();
      c.strokeStyle='rgba(240,245,255,.95)'; c.lineWidth=3*s; c.shadowColor='rgba(210,230,255,1)'; c.shadowBlur=10*D; c.beginPath(); c.moveTo(bx,by0); c.lineTo(bx,by1); c.stroke(); c.restore();
      const gl=seg(t,1.85,1.95)*(1-seg(t,2.05,2.4)); if(gl>0){ const r=22*s*gl; c.save(); c.strokeStyle='rgba(235,245,255,1)'; c.lineWidth=1.2*D; c.shadowColor='rgba(200,230,255,1)'; c.shadowBlur=12*D; c.beginPath(); c.moveTo(bx-r,by1); c.lineTo(bx+r,by1); c.moveTo(bx,by1-r*.8); c.lineTo(bx,by1+r*.8); c.stroke(); c.restore(); } }
    if(ap>0){ c.save(); c.globalAlpha*=ap*inA; c.translate(px,py+(1-ap)*20*s);
      P.glow(0,0,R*2.2,red>0?'235,60,85':'255,214,150',.35+.25*red);
      c.save(); c.beginPath(); c.arc(0,0,R,0,Math.PI*2); c.clip(); c.fillStyle='#2b2534'; c.fillRect(-R,-R,2*R,2*R); c.scale(Math.abs(sx)<.02?.02*Math.sign(sx||1):sx,1); if(img.complete&&img.naturalWidth) c.drawImage(img,-R,-R,2*R,2*R);
      if(red>0){ c.fillStyle=`rgba(120,10,30,${.18*red})`; c.fillRect(-R,-R,2*R,2*R); } c.restore();
      const rc=red>0?`${Math.round(226+9*red)},${Math.round(196-136*red)},${Math.round(138-53*red)}`:'226,196,138';
      c.lineWidth=2.4*D; c.strokeStyle=`rgba(${rc},1)`; c.shadowColor=`rgba(${rc},1)`; c.shadowBlur=12*D; c.beginPath(); c.arc(0,0,R,0,Math.PI*2); c.stroke();
      if(crack>0){ c.shadowBlur=6*D; c.strokeStyle=`rgba(255,120,130,${crack})`; c.lineWidth=1.4*D; [[.2,.9],[1.35,.7],[2.7,.8],[4.1,.6]].forEach(([a0,l])=>{ c.beginPath(); c.moveTo(Math.cos(a0)*R,Math.sin(a0)*R); c.lineTo(Math.cos(a0+.08)*R*(1-.28*l*crack),Math.sin(a0+.08)*R*(1-.28*l*crack)); c.lineTo(Math.cos(a0-.05)*R*(1-.45*l*crack),Math.sin(a0-.05)*R*(1-.45*l*crack)); c.stroke(); }); }
      c.restore(); P.kick(t,1.5,6,.3); }
    c.restore();
    X.w(t,2.4,T-.5,'235,60,85'); X.txt(t,2.0,3.2); V.o.querySelector('.xd-txt').style.opacity=(1-out).toFixed(3); kgShake(V,P); }
}
// 서번트 대사 한 줄을 그 언어의 따옴표로
function kgLine(l){ const q=tr(l).replace(/^[“「]|[”」]$/g,''); if(/^\(/.test(q)||/^（/.test(q)) return q; return LANG==='ja'||LANG==='zht'?'「'+q+'」':'“'+q+'”'; }
