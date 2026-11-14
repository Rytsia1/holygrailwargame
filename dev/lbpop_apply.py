"""로비에서 여는 팝업(설정 · 시나리오 · 도움말 · 패치 노트 · 도감 상세)과 기록 화면(도감 · 지난 생 · 업적), 이야기와 규칙에 로비와 같은 고풍 스타일을 입힌다 (11-14).
- 창: 어두운 남색 판(lb2_apply의 --lbPN) · 제목은 고운바탕 금색, 금빛 밑줄과 마름모 · 단추는 작은 판 · 시나리오 선택은 금빛 밑줄
- 기록 화면: 탭은 판(보는 탭은 파란 판) · 카드는 남색 바탕에 금 이중선 · 완전한 사각형(카드 · 칩 · 입력칸)은 모서리를 조금 둥글게
- 지금은 로비에서 열 때만(body.lb-on). 게임 중 팝업은 나중에
사용: python3 lbpop_apply.py <game.html>  (lb2_apply 다음)"""
import sys
CSS = r'''
/* ---- 로비에서 여는 팝업 · 기록 화면: 고풍 스타일 (lbpop_apply) ---- */
body.lb-on .dlg{background:rgba(4,5,10,.62)}
body.lb-on .dlg .sheet{border:12px solid transparent!important;border-image:var(--lbPN) 14 fill / 16px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;padding:14px 16px!important;filter:drop-shadow(0 14px 30px rgba(0,0,0,.6))}
body.lb-on .dlg .sheet h2,body.lb-on #lbRec .past-head h2,body.lb-on #lbAbout .ab-h{font-family:var(--lbF)!important;font-weight:700!important;color:#e8d3a0!important;letter-spacing:.02em}
body.lb-on .dlg .sheet h3,body.lb-on #lbAbout .rules h3{font-family:var(--lbF);color:#e2c98e}
body.lb-on .set-head{border-bottom:0!important;position:relative;background:linear-gradient(90deg,rgba(216,189,124,.5),rgba(216,189,124,0)) left bottom/100% 1px no-repeat}
body.lb-on .set-head::after{content:'';position:absolute;left:-3px;bottom:-3px;width:7px;height:7px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a);box-shadow:0 0 5px rgba(220,190,120,.6)}
body.lb-on .set-sec{border-bottom-color:rgba(196,164,104,.14)!important}
body.lb-on .set-sec p{color:#a39c8a}
body.lb-on .set-sec .set-more{color:#e2c98e}
body.lb-on .set-x,body.lb-on #lbRec .ab-x,body.lb-on #lbAbout .ab-x{border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;width:36px!important;height:36px!important;box-sizing:border-box;display:grid;place-items:center;padding:0!important;color:#d8bd7c!important;font-size:15px!important;line-height:1;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}
/* 단추 */
body.lb-on .dlg .pn-btn,body.lb-on #lbRec .dx-names,body.lb-on #lbRec .pn-btn{border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;padding:3px 10px!important;color:#ddd3bb!important;font-family:var(--lbF);filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}
body.lb-on .dlg .pn-btn::before,body.lb-on #lbRec .pn-btn::before{background:#d8bd7c}
body.lb-on .dlg .pn-btn.st[aria-pressed=false]{color:#8f8878!important}
body.lb-on .dlg .pn-btn.st[aria-pressed=false]::before{background:#6f6676}
body.lb-on .dlg .pn-btn .mono{color:#c9ad72}
body.lb-on #lbRec .dx-names[aria-pressed=true]{color:#f3e8cb!important}
body.lb-on .dlg input[type=range]{accent-color:#d8bd7c}
body.lb-on .scn-seg{border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;border-radius:0!important;padding:0 2px;overflow:visible!important;filter:drop-shadow(0 2px 3px rgba(0,0,0,.45))}
body.lb-on .scn-seg button{position:relative;border-right:0!important;background:none!important;color:#8f8878;font-family:var(--lbF);padding:5px 14px}
body.lb-on .scn-seg button[aria-pressed=true]{background:none!important;color:#f3e8cb;text-shadow:0 0 8px rgba(230,200,140,.5)}
body.lb-on .scn-seg button[aria-pressed=true]::after{content:'';position:absolute;left:22%;right:22%;bottom:2px;height:1px;background:linear-gradient(90deg,transparent,#d8bd7c,transparent)}
body.lb-on .scn-seg button.al[aria-pressed=true]{color:#e6a3a3}
body.lb-on .scn-seg button.al[aria-pressed=true]::after{background:linear-gradient(90deg,transparent,#d26a6a,transparent)}
body.lb-on .dlg .choices .btn,body.lb-on .dlg .choices button{border:10px solid transparent!important;border-image:var(--lbPL) 14 fill / 14px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;color:#ece3cc!important;font-family:var(--lbF)!important;text-align:center!important;padding:4px 10px!important;filter:drop-shadow(0 3px 6px rgba(0,0,0,.5))}
body.lb-on #info .sheet.info>.choices{margin:14px -16px 0!important;padding:10px 16px 12px;background:#090c19}
body.lb-on #info .sheet.info>.choices::before{background:linear-gradient(to bottom,rgba(9,12,25,0),#090c19)}
/* 기록 화면 */
body.lb-on #lbRec .vtabs button{border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;background:none!important;border-radius:0!important;padding:3px 12px!important;color:#a39c8a!important;font-family:var(--lbF);position:relative;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}
body.lb-on #lbRec .vtabs button[aria-pressed=true]{border-image-source:var(--lbPR)!important;color:#f3e8cb!important;text-shadow:0 0 8px rgba(230,200,140,.45)}
body.lb-on #lbRec .vtabs button[aria-pressed=true]::after{content:'';position:absolute;left:18%;right:18%;bottom:0;height:1px;background:linear-gradient(90deg,transparent,#d8bd7c,transparent)}
body.lb-on #lbRec .vtabs button small{color:#c9ad72}
body.lb-on #lbRec .past-head{padding-bottom:10px;position:relative;background:linear-gradient(90deg,rgba(216,189,124,.45),rgba(216,189,124,0)) left bottom/100% 1px no-repeat}
body.lb-on #lbRec .past-head::after{content:'';position:absolute;left:-3px;bottom:-3px;width:7px;height:7px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a)}
body.lb-on #lbRec .past-sum{color:#a39c8a}
body.lb-on #lbRec .past-filter button{border-radius:0!important;border:1px solid rgba(196,164,104,.25)!important;background:none!important;color:#a39c8a!important;font-family:var(--lbF)}
body.lb-on #lbRec .past-filter button[aria-pressed=true]{background:rgba(216,189,124,.1)!important;border-color:#d8bd7c!important;color:#f3e8cb!important}
body.lb-on #lbRec .dx-clsh{font-family:var(--lbF);color:#c9ad72;letter-spacing:.08em}
body.lb-on #lbRec .past-item,body.lb-on #lbRec .dx-card,body.lb-on #lbRec .ac,body.lb-on #lbRec .sk-c{border-radius:0!important;background:linear-gradient(180deg,rgba(17,23,40,.94),rgba(8,11,21,.94))!important;border:1px solid rgba(196,164,104,.24)!important;box-shadow:inset 0 0 0 3px rgba(8,11,21,.9),inset 0 0 0 4px rgba(196,164,104,.1)!important}
body.lb-on #lbRec .past-item{border-left:3px solid var(--rc,rgba(196,164,104,.3))!important}
body.lb-on #lbRec .past-item:hover,body.lb-on #lbRec .dx-card:not(.u):hover{border-color:rgba(216,189,124,.6)!important}
body.lb-on #lbRec .ac.on,body.lb-on #lbRec .ac.fresh{border-color:rgba(216,189,124,.6)!important}
body.lb-on #lbRec .ac.on .ic{border-color:#d8bd7c;color:#f2e2b4;background:rgba(216,189,124,.1)}
body.lb-on #lbRec .ac .ic{border-radius:0;transform:rotate(45deg) scale(.82)}
body.lb-on #lbRec .ac .ic>*{transform:rotate(-45deg)}
body.lb-on #lbRec .past-item .n,body.lb-on #lbRec .dx-card .n,body.lb-on #lbRec .ac .an{font-family:var(--lbF);color:#ece3cc}
body.lb-on #lbRec .past-item .badge{border-radius:0}
body.lb-on #lbRec .dx-bar{border-radius:0}
/* 이 밤의 이야기와 규칙 */
body.lb-on #lbAbout .ab-go{border:10px solid transparent!important;border-image:var(--lbPR) 14 fill / 14px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;color:#f6edd3!important;font:700 17px var(--lbF)!important;letter-spacing:.14em;padding:4px 10px!important;filter:drop-shadow(0 3px 7px rgba(0,0,0,.6)) drop-shadow(0 0 8px rgba(220,190,120,.14))}
body.lb-on #lbAbout .counter{border-color:rgba(216,189,124,.3)!important}
body.lb-on #lbAbout .counter b{color:#e8d3a0}
body.lb-on #info .sheet.info{padding-bottom:0!important}
/* 각진 곳을 조금씩 둥글게 */
#lbBond .bd-rec,#lbBond .bd-card,#lbBond .bd-cls button,#lbBond .bd-q,#lbBond select{border-radius:6px!important}
#lb2 .l2-face{border-radius:6px}
body.lb-on #lbRec .past-filter button,body.lb-on #lbRec .past-item,body.lb-on #lbRec .dx-card,body.lb-on #lbRec .ac,body.lb-on #lbRec .sk-c,body.lb-on #lbRec .past-item .badge,body.lb-on #lbRec .dx-bar{border-radius:7px!important}
body.lb-on #lbRec .ac .ic{border-radius:5px}
'''
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read()
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    open(P, 'w', encoding='utf-8').write(s); print('lbpop ok')
