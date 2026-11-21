"""11-21: 검귀 루트 배경음악 K1~K7 (모두 오리지널 작곡, dev/kgbgm/*.py · 공통 엔진 eng.py · FluidR3 GM 렌더 + 합성 층).
참고곡(사무라이 렘넌트 OST)의 템포 · 구성 · 짜임만 재서 맞췄고 소리 · 선율 · 화성은 쓰지 않았다.
- K1 kgduel  마스터 대 서번트 결투(w.duel.ctx가 있는 동안)
- K2 kgday  본성 속 진심 나흘의 낮 · 밤(11-22 밤도 낮 곡으로 통일, K3 kgnight는 쓰지 않음)
- K6 kglast  마지막 밤: 잔이 가득 찬 뒤(kgFinal이 g.fin을 켬) 결전 · 결투가 시작되기 전까지
- K7 kgally  잔을 막으러 온 동맹과의 결전(battle ctx.kgAlly) · 결전 사이사이(동맹 결전이 시작된 뒤 끝나기 전)에도 이어서
- K4 kgbound  묶인 잔(③) 에필로그
- K5 end_kg  검귀 결말의 결과 화면(기록 r.kg) · j_end_kg은 그 앞부분 14초(결말 연출 소리 j_end_kgF/S/T도 이것을 뒤에 붙임, 나머지 검귀 결말 연출은 j_end_kg)
사용: python3 kgbgm_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read(); miss = []
def rp(o, n):
    global s
    if s.count(o) != 1: miss.append((o[:70], s.count(o))); return
    s = s.replace(o, n)
M = {'kgally': (81.668, 4.272, 81.168), 'kgduel': (99.5, 15.0, 99.0), 'kgday': (94.25, 18.75, 93.75), 'kgnight': (100.5, 12.0, 100.0),
     'kgbound': (71.75, 11.25, 71.25), 'kglast': (56.5, 8.0, 56.0), 'end_kg': (140.02, 30.52, 139.52)}
M.pop('kgnight')   # 11-22: 나흘의 밤도 낮 곡(K2)으로 통일 — K3은 쓰지 않는다(악보 dev/kgbgm/k3_night.py는 남겨 둠)
rp('"final":{"d":73.93,"ls":10.07,"le":73.43}', '"final":{"d":73.93,"ls":10.07,"le":73.43},' + ','.join(f'"{k}":{{"d":{d},"ls":{a},"le":{b}}}' for k, (d, a, b) in M.items()) + ',"j_end_kg":{"d":14.04}')
rp("if(S.phase==='epi') return 'epi';", "if(S.phase==='epi') return S.flags.kgEnd==='b'?'kgbound':'epi';")
rp("  const b=w.battle; if(b&&b.e){", "  if((w.duel&&w.duel.ctx)||(w.duelLast&&w.kg&&!w.kg.done)) return 'kgduel';   // 결투가 끝난 뒤 결과 창 · 결말까지 결투 곡을 이어서\n  const b=w.battle; if(b&&b.e){")
rp("if(b.ctx&&b.ctx.final) return 'final';", "if(b.ctx&&b.ctx.kgAlly) return 'kgally'; if(b.ctx&&b.ctx.final) return 'final';")
rp("  return w.tod==='밤'?'night':'day';\n}", "  if(w.kg&&!w.kg.done) return S.flags.kgAllyFight&&w.kg.fin?'kgally':w.kg.fin?'kglast':'kgday';\n  return w.tod==='밤'?'night':'day';\n}")
rp("bx:S.flags.bxEnd?'moon':S.flags.bxDream?'dream':'',", "bx:S.flags.bxEnd?'moon':S.flags.bxDream?'dream':'', kg:S.flags.kgEnd||'',")
rp("function sndEndOf(r){ if(r.bx==='moon') return 'f';", "function sndEndOf(r){ if(r.kg) return 'kg'; if(r.bx==='moon') return 'f';")
rp("const END_SK={", "const END_SK={kgM:'j_end_kgN',kgB:'j_end_kgN',kgP:'j_end_kgN',kgP2:'j_end_kgN',kgX:'j_end_kgN',")
# 11-22: 검귀 결말 연출이 나오면 전투 곡을 끄고, 그 뒤에 이어질 곡(에필로그 / 묶인 잔 / 기록 화면의 검귀 엔딩 곡)을 7초에 걸쳐 천천히 키운다.
#   결말 연출 소리는 효과만 두고(곡을 붙이지 않음), 그 곡이 실제 장면으로 넘어갈 때까지 다른 곡으로 바뀌지 않게 잠가 둔다
rp("function bgm(k){ want=k; if(!on()) return; const c=wake(); if(!c) return; if(cur&&cur.k===k) return;", "function bgm(k,fi){ want=k; if(!on()) return; const c=wake(); if(!c) return; if(cur&&cur.k===k) return;")
rp("const old=cur; cur=k?{k}:null; fadeOut(old,1.2); if(!k) return; const me=cur;", "const old=cur; cur=k?{k}:null; fadeOut(old,fi?.9:1.2); if(!k) return; const me=cur;")
rp("g.gain.linearRampToValueAtTime(1,n+(old?1.2:.8));", "g.gain.linearRampToValueAtTime(1,n+(fi||(old?1.2:.8)));")
rp("function sndSync(){ const k=sndScene(); if(k!==undefined) Snd.bgm(k); }",
   "function sndSync(){ let k=sndScene(); const L=window.__bgmLock; if(L){ if(k===L.k||performance.now()>L.until) window.__bgmLock=null; else k=L.k; } if(k!==undefined) Snd.bgm(k); }\n"
   "function kgEndBgm(key){ if(!/^kg/.test(key||'')) return; try{ const S=Sim.S, f=(S&&S.flags)||{}; const k=(S&&S.dead)||['f','s'].includes(f.kgEnd)?'end_kg':f.kgEnd==='b'?'kgbound':'epi';\n"
   "  window.__bgmLock={k,until:performance.now()+120000}; if(k==='end_kg') Snd.setEnd('end_kg'); Snd.bgm(k,7); }catch(e){} }")
rp("function normalEndShow(fx,key){", "function normalEndShow(fx,key){ kgEndBgm(key);")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
