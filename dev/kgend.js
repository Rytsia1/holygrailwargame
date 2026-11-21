  // 11-21: 검귀 루트 결말 전용 장면 (시안 8~10) — 등 뒤의 칼 · 막아선 칼 · 둘이 이긴 세계
  const kgFill=(cx,base,s,frac,col,a)=>{ const top=base-160*s, bot=base-72*s, y=bot-(bot-top)*frac; c.save(); cupPath(cx,base,s); c.clip(); const g=c.createLinearGradient(0,y,0,bot); g.addColorStop(0,`rgba(${col},${.95*a})`); g.addColorStop(1,`rgba(${col},${.6*a})`); c.fillStyle=g; c.fillRect(cx-70*s,y,140*s,bot-y+2); c.strokeStyle=`rgba(255,200,205,${.7*a})`; c.lineWidth=1.2*D; c.beginPath(); c.ellipse(cx,y,Math.max(4,(64-56*Math.max(0,(y-top)/(bot-top)))*s),3*s,0,0,Math.PI*2); c.stroke(); c.restore(); };
  const kgCup=(cx,base,s,ig,col,dim)=>{ c.save(); c.globalAlpha*=1-.6*dim; cupLight(cx,base,s,ig,col); c.restore(); };
  const kgWishRed=()=>{ WISH.style.color='#ffe9ec'; WC.forEach(e=>{ if(e.style.opacity>0) e.style.textShadow=e.style.textShadow.replace(/255,\s*220,\s*150/,'255,90,110'); }); };
  SCN.kgF={HOLD:7.0,init(){ setWish(opt.wish); setText('등 뒤의 칼','찰나의 순간, 잔과 함께 등을 베였다.','당신의 사고는 이어지지 않았다.','rgba(220,50,70,.9)'); OUT=99; this.SP=null; },
   frame(t,dt){ const s=S_()*.9, cx=W/2, base=H*.58, top=H*.6, inA=io(seg(t,0,.4)), CUT=1.45;
    const CC=[cx+6*s,base-118*s], ang=Math.PI/2+.5, F0=Math.hypot(W,H), ux=Math.cos(ang), uy=Math.sin(ang), P1=[CC[0]-ux*F0,CC[1]-uy*F0], P2=[CC[0]+ux*F0,CC[1]+uy*F0], dx=P2[0]-P1[0], dy=P2[1]-P1[1], nx=-uy, ny=ux;
    const world=dim=>{ c.fillStyle=`rgba(4,4,10,${inA})`; c.fillRect(0,0,W,H); night(inA,t); pool(t,top,inA*.8);
      glow(cx,base-160*s,170*s,'235,50,75',.4*inA*(1-dim)); c.save(); c.beginPath(); c.rect(0,0,W,top+6*D); c.clip(); kgCup(cx,base,s,.6+.3*Math.sin(t*3),[255,80,100],.2+.6*dim); kgFill(cx,base,s,1,'200,30,55',inA*(1-.5*dim)); c.restore(); };
    if(t<CUT) world(0);
    else { const sp=oc(seg(t,CUT+.08,CUT+.7)), off=(10+6*seg(t,CUT+.7,3))*D*sp, slide=18*D*sp, dim=seg(t,CUT,2.6);
      c.fillStyle='#000'; c.fillRect(0,0,W,H);
      const half=sg=>{ c.save(); c.beginPath(); const F=F0*2; c.moveTo(P1[0]-ux*F,P1[1]-uy*F); c.lineTo(P2[0]+ux*F,P2[1]+uy*F); c.lineTo(P2[0]+ux*F+nx*F*sg,P2[1]+uy*F+ny*F*sg); c.lineTo(P1[0]-ux*F+nx*F*sg,P1[1]-uy*F+ny*F*sg); c.closePath(); c.clip();
        c.translate(nx*off*sg+ux*slide*(sg>0?1:-.4),ny*off*sg+uy*slide*(sg>0?1:-.4)); world(dim); c.restore(); };
      half(1); half(-1);
      const seam=1-seg(t,CUT+.2,3.6); if(seam>0){ c.save(); c.strokeStyle=`rgba(255,${Math.round(240-160*seg(t,CUT,2.2))},${Math.round(240-170*seg(t,CUT,2.2))},${.9*seam})`; c.lineWidth=(1.2+2*pulse(t,CUT+.05,.12))*D; c.shadowColor='rgba(255,80,100,1)'; c.shadowBlur=14*D; c.beginPath(); c.moveTo(P1[0],P1[1]); c.lineTo(P2[0],P2[1]); c.stroke(); c.restore(); }
      const hx=cx, hy=base-120*s; if(!this.SP) this.SP=burst(70,hx,hy,60,320,40,83,.8,1.7,160); c.save(); c.globalCompositeOperation='lighter'; sparks(this.SP,dt,1,()=> '255,90,110'); c.restore();
      glow(hx,hy,140*s,'255,60,85',.55*pulse(t,CUT+.2,.25)); wave(hx,hy,seg(t,CUT+.15,CUT+1.0),Math.min(W,H)*.3,'255,80,100',5,.55);
      const lid=io(seg(t,2.5,3.4)); if(lid>0){ c.fillStyle='#000'; c.fillRect(0,0,W,H*.5*lid); c.fillRect(0,H-H*.5*lid,W,H*.5*lid); }
      const beat=pulse(t,2.6,.07)+.6*pulse(t,3.15,.07); if(beat>.02){ const vg=c.createRadialGradient(cx,H/2,Math.min(W,H)*.15,cx,H/2,Math.max(W,H)*.7); vg.addColorStop(0,'rgba(0,0,0,0)'); vg.addColorStop(1,`rgba(150,10,30,${.55*beat})`); c.fillStyle=vg; c.fillRect(0,0,W,H); }
      const rest=seg(t,3.2,3.5)*(1-seg(t,4.2,5.4)); if(rest>0){ c.save(); c.strokeStyle=`rgba(200,40,60,${.6*rest})`; c.lineWidth=1*D; c.shadowColor='rgba(255,60,80,1)'; c.shadowBlur=8*D; c.beginPath(); c.moveTo(P1[0],P1[1]); c.lineTo(P2[0],P2[1]); c.stroke(); c.restore(); }
      kick(t,CUT,12,.45); kick(t,2.6,4,.2); kick(t,3.15,2,.18); }
    const sw=seg(t,CUT-.06,CUT+.06); if(sw>0&&t<CUT+.25){ const k=oc(sw), a=1-seg(t,CUT+.06,CUT+.25); c.save(); c.lineCap='round'; c.strokeStyle=`rgba(255,255,255,${a})`; c.lineWidth=3*D; c.shadowColor='rgba(220,230,255,1)'; c.shadowBlur=24*D; c.beginPath(); c.moveTo(P1[0],P1[1]); c.lineTo(P1[0]+dx*k,P1[1]+dy*k); c.stroke(); c.restore(); }
    flash(pulse(t,CUT+.03,.05)*.55,'255,250,255');
    wish(t,.3,CUT-.05); kgWishRed(); text(t,3.6,4.6); }};
  SCN.kgS={HOLD:7.0,init(){ setWish(''); setText('막아선 칼','무자비한 본성은 저지되었고,','서번트의 표정에는 연민만이 가득했다.','rgba(210,220,240,.9)'); OUT=99; this.SH=null; },
   frame(t,dt){ const s=S_()*.72, cx=W/2, top=H*.6, base=top-2*D, inA=io(seg(t,0,.4)), dawn=io(seg(t,1.2,3.6)), BRK=2.6;
    c.fillStyle=`rgba(4,4,10,${inA})`; c.fillRect(0,0,W,H); night(inA*(1-.7*dawn),t);
    if(dawn>0){ const g=c.createLinearGradient(0,top,0,0); g.addColorStop(0,`rgba(214,206,214,${.55*dawn})`); g.addColorStop(.25,`rgba(150,160,190,${.38*dawn})`); g.addColorStop(.7,`rgba(60,70,100,${.25*dawn})`); g.addColorStop(1,`rgba(20,22,40,${.1*dawn})`); c.fillStyle=g; c.fillRect(0,0,W,top); glow(cx,top,Math.max(W,H)*.45,'255,236,210',.35*dawn); }
    pool(t,top,inA*(.6+.3*dawn));
    const red=1-dawn*.7, gone=seg(t,BRK,BRK+.5), rimY=base-160*s;
    if(gone<1){ c.save(); c.globalAlpha=inA*(1-gone); c.beginPath(); c.rect(0,0,W,top+4*D); c.clip(); glow(cx,rimY+40*s,160*s,'235,50,75',.45*red); kgCup(cx,base,s,.4*red+.1,[255,80+Math.round(120*dawn),100+Math.round(90*dawn)],.4); kgFill(cx,base,s,1,`${Math.round(200+20*dawn)},${Math.round(30+120*dawn)},${Math.round(55+110*dawn)}`,1);
      const ck=seg(t,BRK-.45,BRK); if(ck>0){ c.strokeStyle=`rgba(255,245,235,${.9*ck})`; c.lineWidth=1*D; c.shadowColor='rgba(255,230,210,1)'; c.shadowBlur=6*D; const R=rng(17); for(let i=0;i<6;i++){ let x=cx+(R()-.5)*90*s, y=rimY+R()*70*s; c.beginPath(); c.moveTo(x,y); for(let j=0;j<4*ck;j++){ x+=(R()-.5)*26*s; y+=(6+R()*14)*s; c.lineTo(x,y); } c.stroke(); } }
      c.restore(); }
    if(t>=BRK){ if(!this.SH){ const R=rng(29); this.SH=[...Array(90)].map(()=>{ const x=cx+(R()-.5)*120*s, y=rimY+R()*140*s; return {x,y,vx:(R()-.5)*30*D,vy:-(10+R()*40)*D,r:(.6+R()*1.8)*D,l:2.2+R()*2.2,g:-6}; }); }
      c.save(); c.globalCompositeOperation='lighter'; sparks(this.SH,dt,1,()=> '255,236,214'); c.restore(); glow(cx,rimY+50*s,120*s,'255,240,225',.5*pulse(t,BRK+.05,.25)); }
    const S=S_(), bx=cx, gy=H*.2, tip=top+34*D, bw=5.5*S;
    if(dawn>0){ c.save(); c.globalAlpha=.55*dawn; const sl=(H-top)*(.35+.35*dawn); c.beginPath(); c.moveTo(bx-bw*.8,top+6*D); c.lineTo(bx+bw*.8,top+6*D); c.lineTo(bx+bw*3.2,top+sl); c.lineTo(bx-bw*3.2,top+sl); c.closePath(); const g=c.createLinearGradient(0,top,0,top+sl); g.addColorStop(0,'rgba(0,0,0,.9)'); g.addColorStop(1,'rgba(0,0,0,0)'); c.fillStyle=g; c.fill(); c.restore(); }
    c.save(); c.globalAlpha=inA;
    const blade=new Path2D(); blade.moveTo(bx-bw,gy+10*S); blade.lineTo(bx+bw,gy+10*S); blade.lineTo(bx+bw*.9,tip-20*S); blade.lineTo(bx,tip); blade.lineTo(bx-bw*.9,tip-20*S); blade.closePath();
    c.fillStyle='#0b0a12'; c.fill(blade);
    c.save(); c.clip(blade); const eg=c.createLinearGradient(bx-bw,0,bx+bw,0); eg.addColorStop(0,`rgba(225,230,245,${.15+.55*dawn})`); eg.addColorStop(.35,'rgba(0,0,0,0)'); eg.addColorStop(.7,'rgba(0,0,0,0)'); eg.addColorStop(1,`rgba(255,70,95,${.5*red})`); c.fillStyle=eg; c.fillRect(bx-bw,gy,bw*2,tip-gy); c.restore();
    c.strokeStyle=`rgba(255,110,125,${.55*red})`; c.lineWidth=1*D; c.stroke(blade);
    c.fillStyle='#0b0a12'; c.strokeStyle=`rgba(200,190,200,${.25+.35*dawn})`; c.lineWidth=1*D; c.beginPath(); c.rect(bx-bw*4.2,gy+4*S,bw*8.4,7*S); c.fill(); c.stroke();
    c.beginPath(); c.rect(bx-bw*.55,gy-40*S,bw*1.1,44*S); c.fill(); c.stroke(); c.beginPath(); c.arc(bx,gy-44*S,bw*.9,0,Math.PI*2); c.fill(); c.stroke();
    c.restore();
    const gl=seg(t,3.1,3.7); if(gl>0&&gl<1){ const y=lerp(gy+14*S,tip-22*S,io(gl)); glow(bx-bw*.6,y,26*S,'255,250,240',.9*Math.sin(gl*Math.PI)); glow(bx-bw*.6,y,8*S,'255,255,255',Math.sin(gl*Math.PI)); }
    text(t,3.6,4.6); }};
  SCN.kgT={HOLD:7.4,init(){ setWish(opt.wish); setText('둘이 이긴 세계','둘이 이긴 세계의 첫 아침이 왔다.','그 세계는 아주 조용했다.','rgba(230,190,200,.85)'); OUT=99; this.LT=null; this.FZ=0; },
   frame(t,dt){ const s=S_()*.82, cx=W/2, top=H*.6, base=top-4*D, inA=io(seg(t,0,.4)), FL=1.2, dawn=io(seg(t,2.6,4.4));
    if(!this.LT){ const R=rng(44), B=[]; let x=-10*D; while(x<W+10*D){ const w=(12+R()*30)*D, h=(14+R()*(Math.abs(x-cx)<70*s?14:56))*D; const win=[]; for(let i=0;i<Math.floor(w*h/(90*D*D));i++) if(R()<.6) win.push({x:x+2*D+R()*(w-4*D),y:top-h+2*D+R()*(h-4*D),p:R()}); B.push({x,w,h,win}); x+=w+(R()<.3?R()*8*D:0); } this.LT=B; }
    c.fillStyle=`rgba(4,4,10,${inA})`; c.fillRect(0,0,W,H); night(inA*(1-dawn),t);
    if(dawn>0){ const g=c.createLinearGradient(0,top,0,0); g.addColorStop(0,`rgba(196,168,176,${.45*dawn})`); g.addColorStop(.35,`rgba(120,108,124,${.32*dawn})`); g.addColorStop(1,`rgba(40,36,48,${.25*dawn})`); c.fillStyle=g; c.fillRect(0,0,W,top); }
    const fr=seg(t,FL,FL+2.2), rr=(fr*.35+.65*io(fr))*W*.62;
    for(const b of this.LT){ const d=Math.abs(b.x+b.w/2-cx), hit=rr>d?seg(rr-d,0,60*D):0; c.fillStyle=`rgba(${Math.round(12+60*hit*(1-dawn))},10,16,${inA})`; c.fillRect(b.x,top-b.h,b.w,b.h+2*D);
      for(const w of b.win){ const off=rr>Math.abs(w.x-cx)+w.p*30*D; if(off) continue; c.fillStyle=`rgba(255,214,150,${(.75+.25*Math.sin(t*3+w.p*9))*inA})`; c.fillRect(w.x,w.y,2*D,2*D); } }
    if(!this.FZ&&t>FL+1.8) this.FZ=t; pool(this.FZ||t,top,inA*(.7-.3*dawn));
    const empty=seg(t,FL+.6,FL+2.2), rimY=base-160*s;
    c.save(); c.beginPath(); c.rect(0,0,W,top+4*D); c.clip(); glow(cx,rimY+40*s,180*s,'235,50,75',.45*(1-empty)*inA); kgCup(cx,base,s,.5*(1-empty)+.08,[255,80,100],.3+.6*empty); kgFill(cx,base,s,1-.95*empty,'200,30,55',inA*(1-empty*.8)); c.restore();
    if(t>=FL){ c.save(); c.globalCompositeOperation='lighter'; c.lineCap='round'; for(const sd of [-1,1]){ const k=io(seg(t,FL,FL+.9)), fa=.75*(1-seg(t,FL+1.2,FL+2.4)); if(fa<=0) continue; c.strokeStyle=`rgba(255,90,110,${fa})`; c.lineWidth=3*s; c.shadowColor='rgba(255,60,80,1)'; c.shadowBlur=12*D; c.beginPath(); c.moveTo(cx+sd*64*s,rimY); c.quadraticCurveTo(cx+sd*70*s,rimY+80*s*k,cx+sd*(46+10*k)*s,rimY+160*s*k); c.stroke(); } c.restore();
      const wa=1-seg(t,FL+1.2,FL+2.6); if(wa>0){ c.save(); c.globalCompositeOperation='lighter'; for(const k2 of [0,.12,.24]){ const r=Math.max(0,rr-k2*W*.3); if(r<=0) continue; c.strokeStyle=`rgba(255,70,95,${.6*wa*(1-k2*2)})`; c.lineWidth=(3-k2*6)*D; c.shadowColor='rgba(255,60,80,1)'; c.shadowBlur=16*D; c.beginPath(); c.ellipse(cx,top+2*D,r,r*.07,0,0,Math.PI*2); c.stroke(); } c.restore(); glow(cx,top,rr*.9,'200,30,55',.18*wa); }
      kick(t,FL,5,.5); }
    const fy=top+6*D, gap=9*S_(), fx0=cx-Math.min(W*.34,230*S_()), ap=inA*(.9+.1*Math.sin(t*2));
    [[fx0-gap,'255,214,150'],[fx0+gap,'255,236,220']].forEach(([x,col])=>{ glow(x,fy,24*S_(),col,.45*ap); c.beginPath(); c.arc(x,fy,2.6*D,0,Math.PI*2); c.fillStyle=`rgba(${col},${ap})`; c.fill(); c.save(); c.globalAlpha=.25*ap; c.fillStyle=`rgba(${col},1)`; c.fillRect(x-.6*D,fy+4*D,1.2*D,(10+6*dawn)*S_()); c.restore(); });
    wish(t,.3,FL+1.0); kgWishRed(); text(t,3.8,4.8); }};
