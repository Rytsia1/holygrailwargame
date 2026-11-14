"""1단계(공통 부품, 11-15): 로비에서만 쓰던 판 · 단추 · 창 스타일을 게임 전체의 창으로 넓힌다.
- 정보 창(내 서번트 · 다른 조) · 도움말 · 설정 · 시나리오: 남색 판 창, 금색 제목과 밑줄, 판 단추. 사건 선택 창(#dlg)은 5단계에서
- 정보 창 안쪽: 구역 이름 금색, 구역 사이 금선, 스킬 · 보구 이름 명조, 격돌 역할 상자 금 이중선
- 소리 빠른 조절: 남색 판 창 · 「소리」 줄에 켜기/끄기 스위치(평면 동그라미 손잡이, 글자는 지금 상태 켜짐/꺼짐)
사용: python3 ig1_apply.py <game.html>"""
import sys, i18n
CSS = r'''
/* ---- 1단계: 게임 전체의 창 · 공통 부품 (ig1_apply) ---- */
.dlg:not(#dlg){background:rgba(4,5,10,.62)}
.dlg:not(#dlg) .sheet{border:12px solid transparent!important;border-image:var(--lbPN) 14 fill / 16px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;padding:14px 16px!important;filter:drop-shadow(0 14px 30px rgba(0,0,0,.6))}
.dlg:not(#dlg) .sheet h2,#lbRec .past-head h2,#lbAbout .ab-h{font-family:var(--lbF)!important;font-weight:700!important;color:#e8d3a0!important;letter-spacing:.02em}
.dlg:not(#dlg) .sheet h3,#lbAbout .rules h3{font-family:var(--lbF);color:#e2c98e}
.set-head{border-bottom:0!important;position:relative;background:linear-gradient(90deg,rgba(216,189,124,.5),rgba(216,189,124,0)) left bottom/100% 1px no-repeat}
.set-head::after{content:'';position:absolute;left:-3px;bottom:-3px;width:7px;height:7px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a);box-shadow:0 0 5px rgba(220,190,120,.6)}
.set-sec{border-bottom-color:rgba(196,164,104,.14)!important}
.set-sec p{color:#a39c8a}
.set-sec .set-more{color:#e2c98e}
.set-x,#lbRec .ab-x,#lbAbout .ab-x{border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;width:36px!important;height:36px!important;box-sizing:border-box;display:grid;place-items:center;padding:0!important;color:#d8bd7c!important;font-size:15px!important;line-height:1;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}
.dlg:not(#dlg) .pn-btn,#lbRec .dx-names,#lbRec .pn-btn{border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;padding:3px 10px!important;color:#ddd3bb!important;font-family:var(--lbF);filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}
.dlg:not(#dlg) .pn-btn::before,#lbRec .pn-btn::before{background:#d8bd7c}
.dlg:not(#dlg) .pn-btn.st[aria-pressed=false]{color:#8f8878!important}
.dlg:not(#dlg) .pn-btn.st[aria-pressed=false]::before{background:#6f6676}
.dlg:not(#dlg) .pn-btn .mono{color:#c9ad72}
.dlg:not(#dlg) input[type=range]{accent-color:#d8bd7c}
.scn-seg{border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;border-radius:0!important;padding:0 2px;overflow:visible!important;filter:drop-shadow(0 2px 3px rgba(0,0,0,.45))}
.scn-seg button{position:relative;border-right:0!important;background:none!important;color:#8f8878;font-family:var(--lbF);padding:5px 14px}
.scn-seg button[aria-pressed=true]{background:none!important;color:#f3e8cb;text-shadow:0 0 8px rgba(230,200,140,.5)}
.scn-seg button[aria-pressed=true]::after{content:'';position:absolute;left:22%;right:22%;bottom:2px;height:1px;background:linear-gradient(90deg,transparent,#d8bd7c,transparent)}
.scn-seg button.al[aria-pressed=true]{color:#e6a3a3}
.scn-seg button.al[aria-pressed=true]::after{background:linear-gradient(90deg,transparent,#d26a6a,transparent)}
.dlg:not(#dlg) .choices .btn,.dlg:not(#dlg) .choices button{border:10px solid transparent!important;border-image:var(--lbPL) 14 fill / 14px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;color:#ece3cc!important;font-family:var(--lbF)!important;text-align:center!important;padding:4px 10px!important;filter:drop-shadow(0 3px 6px rgba(0,0,0,.5))}
#info .sheet.info>.choices{margin:14px -16px 0!important;padding:10px 16px 12px;background:#090c19}
#info .sheet.info>.choices::before{background:linear-gradient(to bottom,rgba(9,12,25,0),#090c19)}
#info .sheet.info{padding-bottom:0!important}
/* 정보 창 안쪽 */
#info .sheet h2{font-family:var(--lbF)!important;font-weight:700!important;color:#e8d3a0!important}
#info .np{border-top:0;padding-top:12px;position:relative;background:linear-gradient(90deg,rgba(216,189,124,.32),rgba(216,189,124,0)) left top/100% 1px no-repeat}
#info .np .nh{font-family:var(--lbF);color:#c9ad72;letter-spacing:.06em}
#info .np .nh .nr{color:#8f8878;letter-spacing:0;font-family:var(--f-ui)}
#info .sk li b{font-family:var(--lbF);color:#ece3cc}
#info .sk li .mono{color:#e2c98e}
#info .sk li small{color:#8f8878}
#info .nn{font-family:var(--lbF);color:#f2dfae}
#info dl.row:not(.help) dt{color:#8f8878}
#info dl.row:not(.help) dd{color:#e4dccb}
#info .np-role{border-radius:7px;border-color:rgba(216,189,124,.35);background:linear-gradient(180deg,rgba(17,23,40,.9),rgba(8,11,21,.9));box-shadow:inset 0 0 0 3px rgba(8,11,21,.9),inset 0 0 0 4px rgba(196,164,104,.12)}
#info .np-role .rh{color:#e2c98e;font-family:var(--lbF)}
#info .frag{font-family:var(--f-story);color:#cbbf9f}
.q-help{border-color:rgba(216,189,124,.45)!important;color:#d8bd7c!important;background:rgba(8,11,21,.6)!important}
/* 소리 빠른 조절 */
.sndpop{border:12px solid transparent!important;border-image:var(--lbPN) 14 fill / 16px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;padding:6px 8px!important;filter:drop-shadow(0 12px 26px rgba(0,0,0,.6))}
.sp-play{border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;background:none!important;border-radius:0!important;padding:2px 12px 2px 8px!important;color:#e2c98e!important;font-family:var(--lbF)!important}
.sp-row{font-family:var(--lbF);color:#a39c8a}
.sp-row b{color:#e2c98e}
.sndpop input[type=range]{accent-color:#d8bd7c}
.sp-note,.sp-st{color:#8f8878}
#info .sheet h2{position:relative;padding-bottom:10px;margin-bottom:10px;background:linear-gradient(90deg,rgba(216,189,124,.5),rgba(216,189,124,0)) left bottom/100% 1px no-repeat}
#info .sheet h2::after{content:'';position:absolute;left:-3px;bottom:-3px;width:7px;height:7px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a);box-shadow:0 0 5px rgba(220,190,120,.6)}
#info .np .nh>span:first-child{color:#e2c98e;font-weight:700}

/* 소리 켜기 · 끄기: 스위치 (평면 동그라미 손잡이) */
.sp-top{display:grid;grid-template-columns:4.6em auto minmax(0,1fr);gap:10px;align-items:center}
.sp-lab{font-family:var(--lbF);color:#a39c8a;font-size:13px}
.sp-st{display:none!important}
.sndpop .sp-play{position:relative;width:76px;height:30px;padding:0!important;border:1px solid #6c685d!important;border-image:none!important;border-radius:999px!important;background:linear-gradient(180deg,#0e1322,#070913)!important;box-shadow:inset 0 0 0 2px #070913,inset 0 0 0 3px rgba(196,164,104,.18)!important;filter:none!important;cursor:pointer;transition:background .25s,border-color .25s,box-shadow .25s}
.sndpop .sp-play .sp-i{display:none}
.sndpop .sp-play #sndQLbl{position:absolute;right:11px;top:50%;transform:translateY(-50%);font:12px var(--lbF);color:#8f8878;letter-spacing:.06em;white-space:nowrap}
.sndpop .sp-play::after{content:'';position:absolute;left:4px;top:50%;width:22px;height:22px;margin-top:-11px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#8a8577,#4a463e 70%);box-shadow:0 1px 3px rgba(0,0,0,.6),inset 0 0 0 1px rgba(255,255,255,.08);transition:left .25s,background .25s,box-shadow .25s}
.sndpop .sp-play::before{content:'';position:absolute;z-index:1;left:11.5px;top:50%;width:7px;height:7px;margin-top:-3.5px;transform:rotate(45deg);background:rgba(10,12,22,.45);transition:left .25s}
.sndpop .sp-play[aria-pressed=true]{border-color:#d8bd7c!important;background:linear-gradient(180deg,#2a3866,#141c3a)!important;box-shadow:inset 0 0 0 2px #0d1229,inset 0 0 0 3px rgba(216,189,124,.35),0 0 10px rgba(220,190,120,.22)!important}
.sndpop .sp-play[aria-pressed=true] #sndQLbl{right:auto;left:12px;color:#f3e8cb}
.sndpop .sp-play[aria-pressed=true]::after{left:calc(100% - 26px);background:radial-gradient(circle at 35% 30%,#fbf0cf,#d8bd7c 55%,#a8884e);box-shadow:0 0 8px rgba(230,200,138,.6),0 1px 3px rgba(0,0,0,.5)}
.sndpop .sp-play[aria-pressed=true]::before{left:calc(100% - 18.5px);background:rgba(90,60,20,.55)}
.sndpop .sp-play::before{display:none}
.sndpop .sp-play::after{background:#6c685d!important;box-shadow:none!important;width:20px;height:20px;margin-top:-10px;left:5px}
.sndpop .sp-play[aria-pressed=true]::after{background:#e2c98e!important;left:calc(100% - 25px)}
.sndpop .sp-play[aria-pressed=true]{box-shadow:inset 0 0 0 2px #0d1229,inset 0 0 0 3px rgba(216,189,124,.35)!important}
'''
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n):
        global s
        if s.count(o) != 1: miss.append((o[:50], s.count(o))); return
        s = s.replace(o, n)
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    rp('<div class="sp-top"><button class="sp-play" id="sndQPlay" type="button" aria-pressed="false">',
       '<div class="sp-top"><span class="sp-lab" id="sndQName">소리</span><button class="sp-play" id="sndQPlay" type="button" role="switch" aria-checked="false" aria-labelledby="sndQName" aria-pressed="false">')
    rp("p.setAttribute('aria-pressed',on?'true':'false'); $('#sndQLbl').textContent=tr(on?'일시정지':'재생');",
       "p.setAttribute('aria-pressed',on?'true':'false'); p.setAttribute('aria-checked',on?'true':'false'); $('#sndQLbl').textContent=tr(on?'켜짐':'꺼짐');")
    s, nd, nt = i18n.add(s, [('켜짐', 'On', 'オン'), ('꺼짐', 'Off', 'オフ')])
    print('ig1 miss', miss, 'tr', nd)
    open(P, 'w', encoding='utf-8').write(s)
