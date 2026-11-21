// 11-21: 마스터 대 서번트 결투 카드 (상세안 6판) — 왼쪽은 마스터(마름모 「나 마스터」), 오른쪽은 서번트(결심 · 함께 싸우는 조)
function duelVsHtml(){ const V=Sim.duelView&&Sim.duelView(); if(!V) return '';
  const grid=r=>`<div class="pg">${ORD.map(i=>`<div><small>${PL[i]}</small><b>${esc(r[i])}</b></div>`).join('')}</div>`;
  const hw=v=>v>70?'멀쩡함':v>40?'다침':'크게 다침', M=V.me, Sv=V.sv, c=V.comp;
  const me=`<div class="side me"><div class="phd"><div class="mst"><span>나<br>마스터</span></div><div><div class="cl">마스터</div><div class="who2">당신</div></div></div>${grid(M.ranks)}
    <div class="hb"><i style="width:${Math.max(0,M.hp)}%;background:var(--moss)"></i></div><div class="hb sm"><i style="width:${M.odMax?Math.round(M.od/M.odMax*100):0}%"></i></div>
    <div class="meta"><span>건강 ${M.hp}</span><span>오드 ${M.od} / ${M.odMax}</span><span>령주 ${M.seals}</span></div>
    <div class="np2"><span>${M.soy?`마술 소양 ${esc(M.soy)}`:'마술 소양 없음'}</span>${M.arts.map(a=>` · <span>${esc(a)}</span>`).join('')}</div>${modsHtml(M.mods,'me')}</div>`;
  const cr=c?(()=>{ const gone=!c.alive||c.out, st=!c.alive?'쓰러짐':c.out?'물러남':hw(c.hp);
    return `<div class="comp"><small>함께 싸우는 조</small><span class="cf${gone?' off':''}">${faceHtml(c.hero,20,{unk:!c.rev})}${esc(c.name)} · ${st}${gone?'':` · ${c.np?'보구 씀':'보구 남음'}`}</span></div>`; })():'';
  const sv=`<div class="side foe"><div class="phd">${faceHtml(Sv.id,72,{foe:true,flip:true})}<div><div class="cl">나의 서번트였던 자 · ${esc(Sv.cls)}</div><div class="who2">${esc(Sv.name)}</div></div></div>${grid(Sv.ranks)}
    <div class="hb"><i style="width:${Math.max(0,Sv.hp)}%"></i></div><div class="hb sm"><i style="width:${Math.max(0,Sv.sm)}%"></i></div>
    <div class="meta"><span>건강 ${Sv.hp}</span><span>마력 ${Sv.sm}</span>${Sv.mr?`<span>대마력 ${esc(Sv.mr)}</span>`:''}</div>
    <div class="np2">보구 ${esc(Sv.np)}</div>
    <div class="hes"><span>결심</span><span class="lv">${[0,1,2].map(i=>`<i class="${i<=Sv.blade?'on':''}"></i>`).join('')}</span><b>${['굳다','흔들린다','크게 흔들린다'][Sv.blade]}</b></div>${cr}${modsHtml(Sv.mods,'en')}</div>`;
  return me+sv; }
