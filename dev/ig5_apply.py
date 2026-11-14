"""5단계(선택 팝업, 11-15): 결정 창(#dlg) · 잠시 접기 · 펼치기 알약.
- 창: 남색 판(로비 팝업과 같은 판) · 성배 장면의 금빛/보랏빛 후광은 그림자로 유지
- 제목: 명조 + 금빛 밑줄과 마름모(성배전쟁 중에는 붉은빛)
- 지금까지 · 이번 전투 상자: 금빛 겹테 · 머리글에 마름모와 줄
- 선택지: 사선 판(테두리는 한 단계 어둡게, 가리키면 원래 밝기 + 은은한 빛) · 칩과 번호는 모서리만 둥근 사각형
- 펼치기 알약: 파란 판 + 금 마름모
사용: python3 ig5_apply.py <game.html>"""
import sys
CSS = r'''
/* ---- 5단계: 선택 팝업 (ig5_apply) ---- */
/* 5단계: 선택 팝업 */
:root{--lbPLd:url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20width%3D%2748%27%20height%3D%2748%27%20viewBox%3D%270%200%2048%2048%27%3E%3Cdefs%3E%3ClinearGradient%20id%3D%27g%27%20x1%3D%270%27%20y1%3D%270%27%20x2%3D%270%27%20y2%3D%271%27%3E%3Cstop%20offset%3D%270%27%20stop-color%3D%27%230f1426%27%20stop-opacity%3D%270.9%27%2F%3E%3Cstop%20offset%3D%271%27%20stop-color%3D%27%23070a15%27%20stop-opacity%3D%270.9%27%2F%3E%3C%2FlinearGradient%3E%3ClinearGradient%20id%3D%27s%27%20x1%3D%270%27%20y1%3D%270%27%20x2%3D%271%27%20y2%3D%271%27%3E%3Cstop%20offset%3D%270%27%20stop-color%3D%27%2357534a%27%2F%3E%3Cstop%20offset%3D%27.5%27%20stop-color%3D%27%238c8572%27%2F%3E%3Cstop%20offset%3D%271%27%20stop-color%3D%27%2357534a%27%2F%3E%3C%2FlinearGradient%3E%3Cfilter%20id%3D%27n%27%3E%3CfeTurbulence%20type%3D%27fractalNoise%27%20baseFrequency%3D%27.9%27%20numOctaves%3D%272%27%20seed%3D%273%27%2F%3E%3CfeColorMatrix%20values%3D%270%200%200%200%20.85%20%200%200%200%200%20.78%20%200%200%200%200%20.6%20%200%200%200%200.035%200%27%2F%3E%3CfeComposite%20in2%3D%27SourceGraphic%27%20operator%3D%27in%27%2F%3E%3C%2Ffilter%3E%3C%2Fdefs%3E%3Cpath%20d%3D%27M7%20.7H41L47.3%207V41L41%2047.3H7L.7%2041V7Z%27%20fill%3D%27url%28%23g%29%27%2F%3E%3Cpath%20d%3D%27M7%20.7H41L47.3%207V41L41%2047.3H7L.7%2041V7Z%27%20fill%3D%27%23000%27%20filter%3D%27url%28%23n%29%27%2F%3E%3Cpath%20d%3D%27M7%20.7H41L47.3%207V41L41%2047.3H7L.7%2041V7Z%27%20fill%3D%27none%27%20stroke%3D%27url%28%23s%29%27%20stroke-width%3D%271.2%27%2F%3E%3Cpath%20d%3D%27M8.5%203.6H39.5L44.4%208.5V39.5L39.5%2044.4H8.5L3.6%2039.5V8.5Z%27%20fill%3D%27none%27%20stroke%3D%27rgba%28196%2C164%2C104%2C.22%29%27%20stroke-width%3D%27.8%27%2F%3E%3Cpath%20d%3D%27M3.6%203.6l1.6%201.6-1.6%201.6-1.6-1.6zM44.4%203.6l1.6%201.6-1.6%201.6-1.6-1.6zM3.6%2041.2l1.6%201.6-1.6%201.6-1.6-1.6zM44.4%2041.2l1.6%201.6-1.6%201.6-1.6-1.6z%27%20fill%3D%27%237f6c49%27%2F%3E%3C%2Fsvg%3E")}
#dlg{background:rgba(4,5,10,.6)}
#dlg .sheet{border:12px solid transparent!important;border-image:var(--lbPN) 14 fill / 16px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;padding:16px 18px!important;filter:drop-shadow(0 14px 30px rgba(0,0,0,.6))}
#dlg #sheet.grail{filter:drop-shadow(0 14px 30px rgba(0,0,0,.6)) drop-shadow(0 0 36px rgba(224,178,92,.28))}
#dlg #sheet.grail.dark{filter:drop-shadow(0 14px 30px rgba(0,0,0,.6)) drop-shadow(0 0 36px rgba(140,50,160,.4))}
/* 제목 */
#dlg .sheet h2{position:relative;font-family:var(--lbF)!important;font-weight:700;color:#e8d3a0;letter-spacing:.02em;padding-bottom:10px;margin-bottom:6px;background:linear-gradient(90deg,rgba(216,189,124,.5),rgba(216,189,124,0)) left bottom/100% 1px no-repeat}
#dlg .sheet h2::after{content:'';position:absolute;left:-3px;bottom:-3px;width:7px;height:7px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a);box-shadow:0 0 5px rgba(220,190,120,.6)}
#dlg .sheet.war h2{color:#f0c9cc;background-image:linear-gradient(90deg,rgba(210,106,116,.55),rgba(210,106,116,0))}
#dlg .sheet.war h2::after{background:linear-gradient(135deg,#f6c0c5,#b8444f);box-shadow:0 0 5px rgba(230,110,120,.6)}
#dlg .sheet.grail h2{color:#f2e2b4}
#dlg .sheet .body{color:#ece3cc}
/* 잠시 접기 */
#dlg .dfold{border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;background:none!important;border-radius:0!important;padding:0 8px!important;margin:-6px -6px 8px 12px;height:32px;color:#c9ad72;font-family:var(--lbF);font-size:12px;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}
#dlg .dfold:hover,#dlg .dfold:focus-visible{color:#f3e8cb}
/* 지금까지 · 이번 전투 */
#dlg .recent{border-radius:7px;border:1px solid rgba(196,164,104,.2);background:linear-gradient(180deg,rgba(6,8,16,.85),rgba(10,13,24,.85));box-shadow:inset 0 0 0 3px rgba(6,8,16,.9),inset 0 0 0 4px rgba(196,164,104,.08)}
#dlg .recent .rh{display:flex;align-items:center;gap:8px;font-family:var(--lbF);font-weight:700;font-size:11.5px;color:#c9ad72}
#dlg .recent .rh::before{content:'';flex:none;width:5px;height:5px;transform:rotate(45deg);background:#c9ad72}
#dlg .recent .rh::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(216,189,124,.35),rgba(216,189,124,0))}
#dlg .recent .rl.pk{font-family:var(--lbF);color:#e2c98e}
/* 선택지 */
#dlg .choice{border:10px solid transparent!important;border-image:var(--lbPLd) 14 fill / 14px / 0 stretch!important;background:none!important;border-radius:0!important;padding:3px 6px;color:#ece3cc;filter:drop-shadow(0 3px 6px rgba(0,0,0,.45));transition:filter .15s}
#dlg .choice.grp{padding-right:86px} #dlg .choice.hasadv{padding-right:70px} #dlg .choice.sub{padding-top:2px;padding-bottom:2px}
#dlg .choice .kn{left:2px;top:3px} #dlg .choice .adv{right:2px;top:2px} #dlg .choice.grp .gch{right:4px;top:4px}
@media (hover:hover) and (pointer:fine){#dlg .choice{padding-left:32px}}
#dlg .choice .ct{font-family:var(--lbF);font-weight:700;font-size:15.5px;color:#f0e6cc}
#dlg .choice .cd{color:#a39c8a}
#dlg .choice:hover:not(:disabled),#dlg .choice:focus-visible{border-image-source:var(--lbPL)!important;filter:drop-shadow(0 3px 6px rgba(0,0,0,.45)) drop-shadow(0 0 6px rgba(220,190,120,.35))}
#dlg .sheet.war .choice:hover:not(:disabled),#dlg .sheet.war .choice:focus-visible{filter:drop-shadow(0 3px 6px rgba(0,0,0,.45)) drop-shadow(0 0 6px rgba(220,100,110,.4))}
#dlg .choice .kn{border-radius:4px!important;border-color:rgba(216,189,124,.35)!important;color:#c9ad72!important;font-family:var(--lbF)}
#dlg .choice .cs span,#dlg .choice .adv,#dlg .ai-main,#dlg .ai-steps span{border-radius:4px}
#dlg .choice .bfoot{border-top:1px solid rgba(196,164,104,.14)}
#dlg .choice .bfoot .bg>span:first-child,#dlg .choice .cs .lbl{font-family:var(--lbF)}
#dlg .choice.seal .ct{color:#ff9aa2}
#dlg .choices .subs{border-left:1px solid rgba(216,189,124,.3)}
#dlg .choice.grp.seal+.subs{border-left-color:rgba(210,106,116,.5)}
/* 한 줄 남기기 */
#dlg .sheet textarea{border-radius:7px;border-color:rgba(196,164,104,.3);background:rgba(6,8,16,.8);font-family:var(--lbF)}
#dlg .sheet textarea:focus{outline:none;border-color:#d8bd7c}
/* 접었을 때 '펼치기' */
#dlg.folded .dpill{border:9px solid transparent!important;border-image:var(--lbPR) 14 fill / 13px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;padding:3px 12px!important;font-family:var(--lbF);color:#f3e8cb;filter:drop-shadow(0 4px 10px rgba(0,0,0,.6)) drop-shadow(0 0 8px rgba(220,190,120,.14))}
#dlg.folded .dpill .dp-dot{border-radius:0;width:7px;height:7px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a)}
#dlg.folded .dpill .dp-e{color:#e2c98e;font-size:12.5px}
/* 연출 점검(11-15): 긴 제목이 낱말 가운데서 끊기지 않게 */
#dlg .sheet h2{word-break:keep-all;overflow-wrap:anywhere}
'''
# 작별 연출이 창을 밝힐 때 창 그림자(filter)를 지우지 않게
BYE_OLD = "sh.style.filter=`brightness(${1+.35*glow}) saturate(${1+.2*glow})`"
BYE_NEW = "sh.style.filter=`${sh.__f0} brightness(${1+.35*glow}) saturate(${1+.2*glow})`"
BYE_AT_OLD = "const r=sh.getBoundingClientRect(), cols=Math.ceil(r.width/CELL), rows=Math.ceil(r.height/CELL);"
BYE_AT_NEW = "const r=sh.getBoundingClientRect(), cols=Math.ceil(r.width/CELL), rows=Math.ceil(r.height/CELL); sh.style.filter=''; sh.__f0=(f=>f==='none'?'':f)(getComputedStyle(sh).filter);"
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read()
    assert s.count(BYE_OLD) == 1 and s.count(BYE_AT_OLD) == 1, 'byeGate'
    s = s.replace(BYE_OLD, BYE_NEW).replace(BYE_AT_OLD, BYE_AT_NEW)
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    print('ig5 ok')
    open(P, 'w', encoding='utf-8').write(s)
