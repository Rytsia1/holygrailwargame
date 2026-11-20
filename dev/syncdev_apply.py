"""11-20: 기기 연결 — 연결된 기기 목록 보기 · 다른 기기 끊기 · 이 기기 이름 바꾸기
- 서버(src/worker.js)가 기기마다 출입증(dk)을 준다. 이 기기는 dk를 연결 상태(K_SYNC)에 두고 모든 맞춤 요청에 함께 보낸다.
  dk가 없으면(업데이트 전에 연결한 기기) reg:1을 보내 출입증을 받는다.
- 설정 → 다른 기기와 연결: 기기 목록(이 기기 · 다른 기기 · 아직 확인되지 않은 기기), 끊기, 이름 바꾸기
- 다른 기기에서 끊긴 기기는 다음 맞춤 때 연결이 풀리고 안내를 띄운다(기록은 그대로)
사용: python3 syncdev_apply.py <game.html>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'function devLbl(' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

# ① 도우미: 기기 종류 · 요청 몸통 · 끊긴 기기 처리
rp("function syncGone(){ store.del(K_SYNC);",
   "// 기기 종류(목록에 보이는 이름): 운영체제 · 브라우저\n"
   "function devLbl(){ const u=navigator.userAgent||''; const os=/iPhone/.test(u)?'iPhone':(/iPad/.test(u)||(/Macintosh/.test(u)&&navigator.maxTouchPoints>1))?'iPad':/Android/.test(u)?'Android':/Windows/.test(u)?'Windows':/CrOS/.test(u)?'ChromeOS':/Mac OS X|Macintosh/.test(u)?'Mac':/Linux/.test(u)?'Linux':'';\n"
   "  const br=/SamsungBrowser/.test(u)?'Samsung Internet':/Whale/.test(u)?'Whale':/Edg(e|A|iOS)?\\//.test(u)?'Edge':/OPR\\/|Opera/.test(u)?'Opera':/Firefox|FxiOS/.test(u)?'Firefox':/CriOS|Chrome\\//.test(u)?'Chrome':/Safari/.test(u)?'Safari':'';\n"
   "  return [os,br].filter(Boolean).join(' · ')||'Browser'; }\n"
   "// 요청에 붙이는 이 기기의 출입증: 없으면 reg로 받아 온다(업데이트 전에 연결한 기기)\n"
   "const sk=st=>({key:st.key,...(st.dk?{dk:st.dk}:{reg:1}),lbl:devLbl()}), skL=st=>({key:st.key,...(st.dk?{dk:st.dk}:{})});\n"
   "function gotDk(st,j){ if(!j||!j.dk) return; if(st) st.dk=j.dk; const c=syncSt(); if(c) store.set(K_SYNC,{...c,dk:j.dk}); }\n"
   "const isKicked=r=>r&&r.s===403&&r.j&&r.j.error==='kicked';\n"
   "const K_SYKICK='cupnight.synckick.v1', SY_KMSG='다른 기기에서 이 기기의 연결을 끊었습니다. 이 기기의 기록은 그대로 남아 있습니다.';\n"
   "function syncKicked(){ store.del(K_SYNC); store.del(K_SYNCALT); SYUI.devs=null; store.set(K_SYKICK,1); syncUI('off',{msg:SY_KMSG}); toast(SY_KMSG); }\n"
   "function syncGone(){ store.del(K_SYNC);")
# ② 맞춤(받기 · 올리기)
rp("  if(!o.pushOnly){ const r=await sapi('pull',{key:st.key,have:st.ver});\n    if(r.s===404&&r.j.error==='gone'){ syncGone(); return {gone:true}; }",
   "  if(!o.pushOnly){ const r=await sapi('pull',{...sk(st),have:st.ver});\n    if(isKicked(r)){ syncKicked(); return {gone:true}; } gotDk(st,r.j);\n    if(r.s===404&&r.j.error==='gone'){ syncGone(); return {gone:true}; }")
rp("const pu=await sapi('push',{key:st.key,base:ver,z},o.keep&&z.length<60000);",
   "const pu=await sapi('push',{...sk(st),base:ver,z},o.keep&&z.length<60000); if(isKicked(pu)){ syncKicked(); return {gone:true}; } gotDk(st,pu.j);")
# ③ 코드 기다리는 동안 · 코드 만들기 · 새 묶음
rp("const r=await sapi('pull',{key:s.key,have:s.ver}); if(r.j&&r.j.ok&&(r.j.devs||1)>n0){",
   "const r=await sapi('pull',{...sk(s),have:s.ver}); if(isKicked(r)){ clearInterval(SYUI.poll); syncKicked(); return; } gotDk(s,r.j); if(r.j&&r.j.ok&&(r.j.devs||1)>n0){")
rp("const r=await sapi('new',{z:await syncEnc(L)}); if(!r.j.ok){ toast(syncErr(r.j.error)); return; }\n    st={key:r.j.key,ver:r.j.ver,base:L,n:1,at:Date.now()};",
   "const r=await sapi('new',{z:await syncEnc(L),lbl:devLbl()}); if(!r.j.ok){ toast(syncErr(r.j.error)); return; }\n    st={key:r.j.key,dk:r.j.dk,ver:r.j.ver,base:L,n:1,at:Date.now()};")
rp("const c=await sapi('code',{key:st.key}); if(!c.j.ok){ toast(syncErr(c.j.error)); if(c.j.error==='gone') syncGone(); else syncUI(); return; }",
   "const c=await sapi('code',sk(st)); if(isKicked(c)){ syncKicked(); return; } gotDk(st,c.j); if(!c.j.ok){ toast(syncErr(c.j.error)); if(c.j.error==='gone') syncGone(); else syncUI(); return; }")
# ④ 나가기 · 들어오기
rp("  if(st&&(st.n||1)<=1){ await sapi('leave',{key:st.key}); store.del(K_SYNC); }",
   "  if(st&&(st.n||1)<=1){ await sapi('leave',skL(st)); store.del(K_SYNC); }")
rp("const r=await sapi('join',{code:v}); if(!r.j.ok){", "const r=await sapi('join',{code:v,lbl:devLbl()}); if(!r.j.ok){")
rp("catch(e){ sapi('leave',{key:r.j.key}); syncUI('input',{msg:'받은 기록을 읽지 못했습니다.'}); return; }",
   "catch(e){ sapi('leave',{key:r.j.key,dk:r.j.dk}); syncUI('input',{msg:'받은 기록을 읽지 못했습니다.'}); return; }")
rp("SYUI.join={key:r.j.key,ver:r.j.ver,n:r.j.devs,L,R,m};", "SYUI.join={key:r.j.key,dk:r.j.dk,ver:r.j.ver,n:r.j.devs,L,R,m};")
rp("if(J) sapi('leave',{key:J.key}); syncUI('off'); });", "if(J) sapi('leave',{key:J.key,dk:J.dk}); syncUI('off'); });")
rp("  store.set(K_SYNC,{key:J.key,ver:J.ver,base:J.R,n:J.n,at:Date.now()});", "  store.set(K_SYNC,{key:J.key,dk:J.dk,ver:J.ver,base:J.R,n:J.n,at:Date.now()});")
rp("await syncRun({}); await sapi('leave',{key:st.key}); store.del(K_SYNC); store.del(K_SYNCALT);",
   "await syncRun({}); const cur=syncSt()||st; await sapi('leave',skL(cur)); store.del(K_SYNC); store.del(K_SYNCALT); SYUI.devs=null;")
rp("const SYUI={mode:'off',manual:false,code:null,exp:0,tick:0,poll:0,join:null};",
   "const SYUI={mode:'off',manual:false,code:null,exp:0,tick:0,poll:0,join:null,devs:null,ren:false};")

# 끊긴 안내: 설정이 열려 있을 때 보여 주면 지운다. 새로 연결하면 지운다
rp("  clearInterval(SYUI.tick); clearInterval(SYUI.poll); const st=syncSt(); if(!mode) mode=st?'on':'off'; SYUI.mode=mode;",
   "  clearInterval(SYUI.tick); clearInterval(SYUI.poll); const st=syncSt(); if(!mode) mode=st?'on':'off'; SYUI.mode=mode;\n"
   "  if(st) store.del(K_SYKICK); else if(mode==='off'&&!o.msg&&store.get(K_SYKICK)) o.msg=SY_KMSG;\n"
   "  if(o.msg===SY_KMSG&&!$('#setDlg').classList.contains('hidden')) store.del(K_SYKICK);")
# ⑤ '연결됨' 화면: 기기 목록 + 이 기기 연결 끊기
rp("""else if(mode==='on') b=`${msg}<p class="sy-meta">${`기기 ${st.n||1}대 · 마지막으로 맞춘 때 ${syncAgo(st.at)}`}</p><div class="sy-row">""",
   """else if(mode==='on') b=`${msg}<p class="sy-meta">${`기기 ${st.n||1}대 · 마지막으로 맞춘 때 ${syncAgo(st.at)}`}</p>${syDevHtml()}<div class="sy-row">""")
rp("""<button class="pn-btn warn" id="syLeave" type="button">연결 끊기</button>""",
   """<button class="pn-btn warn" id="syLeave" type="button">이 기기 연결 끊기</button>""")
rp("  btn('syNow',async()=>{ SYUI.manual=true; syncAfter(await syncRun({})); syncUI('on'); });",
   "  btn('syNow',async()=>{ SYUI.manual=true; const r=await syncRun({}); if(r&&r.gone){ SYUI.manual=false; return; } syncAfter(r); if(syncSt()) syncUI('on'); });   // 끊겼으면 끊긴 안내를 그대로 둔다")
rp("  btn('syLeave',async()=>syncLeaveAsk());",
   "  btn('syLeave',async()=>syncLeaveAsk());\n"
   "  if(mode==='on') syDevBind(el, btn);")

# ⑥ 기기 목록 그리기 · 불러오기 · 끊기 · 이름 바꾸기
DEV_JS = r"""
/* 연결된 기기 목록 (11-20) */
const SY_IC={ph:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/></svg>',
  pc:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16v4"/></svg>',
  q:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 0 1 4.6 1.3c0 1.7-2.1 2-2.1 3.4M12 17h.01"/></svg>'};
const syDevName=d=>d.name||d.lbl||'Browser';
const syDay=t=>{ try{ return new Date(t).toLocaleDateString({ja:'ja-JP',en:'en-US',zhs:'zh-CN',zht:'zh-TW'}[LANG]||'ko-KR',{month:'short',day:'numeric'}); }catch(e){ return ''; } };
function syDevHtml(){ const D=SYUI.devs; if(!D) return `<ul class="sy-devs" id="syDevs" aria-busy="true"><li class="sy-dev wait"><span class="tx"><small>기기 목록을 불러오는 중</small></span></li></ul>`;
  const row=d=>{ const me=d.id===D.me, ic=/iPhone|Android|iPad/.test(d.lbl||'')?SY_IC.ph:SY_IC.pc;
    const nm=me&&SYUI.ren?`<span class="sy-ren"><input id="syRenIn" maxlength="24" value="${esc(d.name||'')}" placeholder="${esc(d.lbl||'')}" aria-label="기기 이름" data-notr><button type="button" class="sy-mini" id="syRenOk">저장</button><button type="button" class="sy-mini" id="syRenNo">취소</button></span>`
      :`<b><span data-notr>${esc(syDevName(d))}</span>${me?'<span class="me">이 기기</span><button type="button" class="ren" id="syRen">이름 바꾸기</button>':''}</b>`;
    return `<li class="sy-dev"><span class="ic">${ic}</span><span class="tx">${nm}<small><span>${esc(syDay(d.first))}</span> <span>연결</span> · ${me?'<span>지금 사용 중</span>':`<span>마지막 접속</span> <span>${syncAgo(d.seen)}</span>`}</small></span>${me?'':`<button type="button" class="kick" data-k="${esc(d.id)}">끊기</button>`}</li>`; };
  const unk=D.unk>0?`<li class="sy-dev old"><span class="ic">${SY_IC.q}</span><span class="tx"><b>${`아직 확인되지 않은 기기 ${D.unk}대`}</b><small>업데이트 전에 연결된 기기입니다. 그 기기에서 게임을 열면 이름이 나타납니다.</small></span><button type="button" class="kick" data-k="unk">끊기</button></li>`:'';
  return `<ul class="sy-devs" id="syDevs">${D.list.map(row).join('')}${unk}</ul>`; }
async function syDevLoad(){ const st=syncSt(); if(!st||!st.dk){ return; } const r=await sapi('devs',skL(st));
  if(isKicked(r)){ syncKicked(); return; } if(!r.j||!r.j.ok){ if(r.j&&r.j.error==='gone'){ syncGone(); return; } SYUI.devs=null; const u=$('#syDevs'); if(u) u.remove(); return; }
  SYUI.devs=r.j; const c=syncSt(); if(c&&r.j.devs&&c.n!==r.j.devs) store.set(K_SYNC,{...c,n:r.j.devs});
  if(SYUI.mode==='on'&&!$('#setDlg').classList.contains('hidden')) syncUI('on'); }
function syDevBind(el,btn){ const st=syncSt();
  if(!SYUI.devs&&st){ if(st.dk) syDevLoad(); else syncRun({}).then(r=>{ if(r&&!r.gone) syDevLoad(); }); } // 출입증이 아직 없으면 한 번 맞춰서 받아 온다
  btn('syRen',async()=>{ SYUI.ren=true; syncUI('on'); setTimeout(()=>{ const i=$('#syRenIn'); if(i){ i.focus(); i.select(); } },30); });
  btn('syRenNo',async()=>{ SYUI.ren=false; syncUI('on'); });
  btn('syRenOk',async()=>{ const s=syncSt(), v=($('#syRenIn')||{}).value||''; if(!s) return; const r=await sapi('name',{...skL(s),name:v.trim()});
    if(isKicked(r)){ syncKicked(); return; } if(r.j&&r.j.ok) SYUI.devs=r.j; else toast(syncErr(r.j&&r.j.error)); SYUI.ren=false; syncUI('on'); });
  const ri=$('#syRenIn'); if(ri) ri.onkeydown=e=>{ if(e.key==='Enter'){ e.preventDefault(); $('#syRenOk').click(); } else if(e.key==='Escape'){ e.preventDefault(); $('#syRenNo').click(); } };
  el.querySelectorAll('.sy-dev .kick').forEach(x=>x.onclick=()=>syKickAsk(x.dataset.k)); }
function syKickAsk(k){ const D=SYUI.devs; if(!D) return; const d=k==='unk'?null:D.list.find(x=>x.id===k); if(k!=='unk'&&!d) return;
  const warn=d&&D.unk>0?`<p class="hint sy-warn">${`아직 확인되지 않은 기기 ${D.unk}대도 함께 끊깁니다.`} <span>계속 쓸 기기라면 먼저 그 기기에서 게임을 한 번 열고 나서 끊어 주세요.</span></p>`:'';
  const body=d?`<h2>선택한 기기의 연결을 끊을까요?</h2><p class="sy-kname" data-notr>${esc(syDevName(d))}</p><p class="hint" style="margin:8px 0 0">그 기기는 다음에 맞추려 할 때 연결이 풀려, 이 기록을 더 받거나 바꿀 수 없습니다. 그 기기에 이미 있던 기록은 그 기기에 남습니다. 다시 쓰려면 새 연결 코드로 연결하면 됩니다.</p>${warn}`
    :`<h2>확인되지 않은 기기의 연결을 끊을까요?</h2><p class="hint" style="margin:8px 0 0">${`업데이트 전에 연결된 기기 ${D.unk}대가 끊깁니다.`} <span>계속 쓸 기기라면 그 기기에서 새 연결 코드로 다시 연결하면 됩니다.</span></p>`;
  $('#infoBody').innerHTML=`<div class="eyebrow">다른 기기와 연결</div>${body}<div class="choices" style="margin-top:16px"><button class="choice" id="syKOk" type="button"><span class="ct">연결 끊기</span></button><button class="choice" id="syKNo" type="button"><span class="ct">취소</span></button></div>`;
  $('#infoClose').style.display='none'; infoHeld=false; $('#info').classList.remove('hidden');
  $('#syKNo').onclick=()=>closeInfo();
  $('#syKOk').onclick=async()=>{ const st=syncSt(); closeInfo(); if(!st) return; const r=await sapi('kick',{...skL(st),...(d?{id:d.id}:{unk:1})});
    if(isKicked(r)){ syncKicked(); return; } if(!r.j||!r.j.ok){ toast(syncErr(r.j&&r.j.error)); return; }
    SYUI.devs=r.j; const c=syncSt(); if(c) store.set(K_SYNC,{...c,n:r.j.devs}); syncUI('on',{msg:'연결을 끊었습니다.'}); }; }
"""
rp("function syncLeaveAsk(){", DEV_JS.lstrip('\n') + "function syncLeaveAsk(){")

# ⑦ 설정을 열 때마다 목록을 새로 받는다
rp("const SYUI={mode:'off',manual:false,code:null,exp:0,tick:0,poll:0,join:null,devs:null,ren:false};",
   "const SYUI={mode:'off',manual:false,code:null,exp:0,tick:0,poll:0,join:null,devs:null,ren:false};\n"
   "// 설정을 닫으면 기기 목록을 비워 두어, 다음에 열 때 새로 받아 온다\n"
   "new MutationObserver(()=>{ const d=$('#setDlg'); if(d&&d.classList.contains('hidden')){ SYUI.devs=null; SYUI.ren=false; } })\n"
   "  .observe(document.getElementById('setDlg')||document.body,{attributes:true,attributeFilter:['class']});")

# ⑧ 스타일
rp(".set-sec p.sy-msg{", ".sy-devs{list-style:none;margin:0 0 12px;padding:0;border:1px solid var(--line);border-radius:var(--r);overflow:hidden}"
   ".sy-dev{display:flex;align-items:center;gap:10px;padding:10px 12px;background:var(--panel2);border-top:1px solid var(--line)}.sy-dev:first-child{border-top:0}"
   ".sy-dev .ic{width:28px;height:28px;flex:none;border-radius:50%;display:grid;place-items:center;background:rgba(201,164,92,.1);color:var(--gold2)}.sy-dev .ic svg{width:14px;height:14px}"
   ".sy-dev .tx{flex:1;min-width:0}.sy-dev b{display:block;font-weight:500;color:var(--text);font-size:13.5px;overflow-wrap:anywhere}.sy-dev small{display:block;color:var(--dim);font-size:12px;margin-top:1px}"
   ".sy-dev .me{font-size:11px;color:#9bd3ac;border:1px solid rgba(111,191,138,.45);border-radius:999px;padding:1px 7px;margin-left:6px;vertical-align:1px;white-space:nowrap}"
   ".sy-dev .kick{flex:none;background:none;border:1px solid rgba(200,80,90,.5);color:#e6a2a8;border-radius:999px;font-size:12px;padding:4px 12px;cursor:pointer;font:inherit;font-size:12px}"
   ".sy-dev .ren{background:none;border:0;color:var(--faint);font-size:12px;cursor:pointer;padding:0 0 0 6px;text-decoration:underline;font:inherit;font-size:12px}"
   ".sy-dev.old{background:transparent}.sy-dev.old .ic{background:rgba(255,255,255,.05);color:var(--faint)}.sy-dev.wait small{padding:2px 0}"
   ".sy-ren{display:flex;gap:6px;align-items:center;flex-wrap:wrap}.sy-ren input{flex:1;min-width:120px;background:var(--ink);border:1px solid var(--gold);border-radius:6px;color:var(--text);font:inherit;font-size:13.5px;padding:5px 8px}"
   ".sy-mini{background:none;border:1px solid var(--line);color:var(--dim);border-radius:999px;font:inherit;font-size:12px;padding:4px 10px;cursor:pointer}"
   ".sy-kname{margin:6px 0 0;color:var(--gold2);font-size:15px}.sy-warn{margin:10px 0 0!important;color:#e6a2a8!important}"
   ".set-sec p.sy-msg{")

# ⑨ 도움말: 맡기는 것에 기기 목록 정보
rp("'마지막으로 맞춘 지 180일이 지나거나, 모든 기기에서 연결을 끊으면 지워집니다.']],",
   "'마지막으로 맞춘 지 180일이 지나거나, 모든 기기에서 연결을 끊으면 지워집니다.','기기 목록을 위해 기기 종류(예: iPhone · Safari), 직접 붙인 이름, 연결한 때, 마지막으로 맞춘 때를 함께 맡깁니다.']],\n"
   "    ['기기 목록',['연결된 기기는 설정의 ‘다른 기기와 연결’에서 볼 수 있습니다.','다른 기기를 끊으면 그 기기는 다음에 맞출 때 연결이 풀립니다. 그 기기에 있던 기록은 그대로 남습니다.','업데이트 전에 연결된 기기는 그 기기에서 게임을 한 번 열 때까지 ‘아직 확인되지 않은 기기’로 보입니다. 다른 기기를 끊으면 확인되지 않은 기기도 함께 끊깁니다.']],")
rp("gone:'연결된 기록 묶음이 서버에 없습니다',", "gone:'연결된 기록 묶음이 서버에 없습니다',self:'이 기기는 아래 ‘이 기기 연결 끊기’로 끊어 주세요',kicked:'다른 기기에서 이 기기의 연결을 끊었습니다',")

if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

# 번역
from syncdev_lines import D, T
s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, *_ in D], [(a, b, c) for a, b, c, *_ in T])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _b, _c, d, e in D + T:
    if a not in Z: Z[a] = [d, e]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 사전', nd, '· 틀', nt, '· 중국어', n)
