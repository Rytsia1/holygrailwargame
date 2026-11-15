"""로비 피드백 (11-15)
- 배경음악: 아무 곡도 흐르지 않다가 처음 시작할 때(로비에 들어와 소리를 켰을 때 등) 4초에 걸쳐 작게 시작해 천천히 제 크기로.
  곡이 바뀔 때의 1.2초 교차는 그대로.
- 「이 밤의 이야기와 규칙」: 아래 단추를 '입장'(Enter · 入場)으로, 화면 폭과 상관없이 가운데에.
- 닫기(✕): 「이 밤의 이야기와 규칙」 · 기록(도감 · 지난 생 · 업적)의 ✕를 화면 구석이 아니라 그 창의 세로 띠(본문 폭) 안 오른쪽 위로.
  설정 · 패치 노트 · 인연 소환은 이미 창 안에 있어 그대로.
- 설정 단추: 해 모양 아이콘을 톱니바퀴로(시작 화면 · 로비 둘 다).
- 로비 단추 소리: 로비가 떠 있는 동안 사람이 직접 누른 단추 · 링크에 선택음(u_choice), 닫기 단추에는 낮고 부드러운 소리(u_pause).
  자기 소리가 따로 있는 단추(시작 · 태어나기 · 이어하기)와 소리 끄기는 뺀다. 다른 단추를 대신 누르는 단추(로비 설정 → #setBtn)는 한 번만 울린다.
사용: python3 lobbyfb_apply.py <game.html>"""
import sys
GEAR = ("M10.24 4.81 L10.57 2.51 L13.43 2.51 L13.76 4.81 L15.84 5.67 L17.70 4.27 L19.73 6.30 L18.33 8.16 L19.19 10.24 L21.49 10.57 L21.49 13.43 "
        "L19.19 13.76 L18.33 15.84 L19.73 17.70 L17.70 19.73 L15.84 18.33 L13.76 19.19 L13.43 21.49 L10.57 21.49 L10.24 19.19 L8.16 18.33 L6.30 19.73 "
        "L4.27 17.70 L5.67 15.84 L4.81 13.76 L2.51 13.43 L2.51 10.57 L4.81 10.24 L5.67 8.16 L4.27 6.30 L6.30 4.27 L8.16 5.67Z")
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # 1. 처음 시작하는 배경음악은 4초에 걸쳐 천천히 커진다
    rp("g.gain.setValueAtTime(0,n); g.gain.linearRampToValueAtTime(1,n+(old?1.2:.8));",
       "if(old){ g.gain.setValueAtTime(0,n); g.gain.linearRampToValueAtTime(1,n+1.2); } else { const C=new Float32Array(48); for(let i=0;i<48;i++) C[i]=Math.pow(i/47,2.2); g.gain.setValueCurveAtTime(C,n,4); }")
    # 2. '입장' · 가운데
    rp("go:'이 밤으로 들어간다'", "go:'입장'")
    rp("go:'Into the night'", "go:'Enter'")
    rp("go:'この夜へ'", "go:'入場'")
    rp("body.lb-wide #lbAbout .ab-go{margin-inline:auto}", "#lbAbout .ab-go{margin-inline:auto}")
    # 3. ✕를 창의 세로 띠 안으로 (본문 폭: 이야기 640 · 넓은 화면 880 · 기록 1180)
    rp("#lbAbout[hidden]{display:none}",
       "#lbAbout[hidden]{display:none}\n#lbAbout{--abw:640px}body.lb-wide #lbAbout{--abw:880px}\n"
       "#lbAbout .ab-x{right:max(18px,calc(env(safe-area-inset-right,0px) + 14px),calc((100vw - var(--abw))/2 + 16px))!important}\n"
       "#lbRec .ab-x{right:max(14px,calc(env(safe-area-inset-right,0px) + 10px),calc((100vw - 1180px)/2 + 16px))!important}")
    # 4. 톱니바퀴
    sun_css = "%3Ccircle cx='12' cy='12' r='3'/%3E%3Cpath d='M12 2v3M12 19v3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M2 12h3M19 12h3M4.9 19.1L7 17M17 7l2.1-2.1'/%3E"
    rp(sun_css, "%3Cpath d='" + GEAR + "'/%3E%3Ccircle cx='12' cy='12' r='3.2'/%3E", 2)
    rp("""gear:P('<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>')""",
       """gear:P('<path d=\"""" + GEAR + """\"/><circle cx="12" cy="12" r="3.2"/>')""")
    # 5. 로비 단추 소리
    rp("function sndSync(){ const k=sndScene(); if(k!==undefined) Snd.bgm(k); }",
       "function sndSync(){ const k=sndScene(); if(k!==undefined) Snd.bgm(k); }\n"
       "// 로비 단추 소리: 사람이 직접 누른 단추 · 링크만(자기 소리가 있는 단추 · 소리 끄기는 빼고), 닫기는 낮고 부드럽게\n"
       "document.addEventListener('click',e=>{ try{ if(!e.isTrusted||$('#intro').classList.contains('hidden')) return;\n"
       "  const b=e.target.closest('button,a[href],[role=button],summary'); if(!b||b.disabled||b.closest('[data-nosfx]')) return;\n"
       "  if(b.matches('#startBtn,#contBtn,.lb-go,#sndNo')) return;\n"
       "  const t=(b.textContent||'').trim(), al=b.getAttribute('aria-label')||'';\n"
       "  const close=b.matches('.ab-x,.set-x,.bd-x')||/^(닫기|Close|閉じる)$/.test(t)||/^(닫기|Close|閉じる)$/.test(al);\n"
       "  Snd.sfx(close?'u_pause':'u_choice',{gap:0}); }catch(_){} });")
    print('lobbyfb miss', miss)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
