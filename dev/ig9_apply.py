"""9단계(마무리, 11-15): 알림 · 업적 알림 · 기록 캡처 창 · 보낸 조 창.
- 알림: 작은 판 · 업적 알림: 남색 판 + 금빛 마름모
- 기록 캡처 창: 남색 판 · 금빛 밑줄 제목 · 판 단추
- 보낸 조 창(#info .gt-pop): 소식 상자 겹테 · 판 단추 · 안내 문구 옆 흐려지는 금빛 줄
사용: python3 ig9_apply.py <game.html>"""
import sys
CSS = r'''
/* ---- 9단계: 마무리 (ig9_apply) ---- */
/* 9단계: 남은 것들 — 알림 · 업적 알림 · 기록 캡처 창 · 보낸 조 창 */
.toast:not(.ach){border:7px solid transparent;border-image:var(--lbTG) 14 fill / 12px / 0 stretch;background:none;border-radius:0;padding:2px 12px;color:#e8d3a0;font-family:var(--lbF);font-weight:700;filter:drop-shadow(0 4px 10px rgba(0,0,0,.6))}
.toast.ach{border:10px solid transparent;border-image:var(--lbPN) 14 fill / 14px / 0 stretch;background:none;border-radius:0;box-shadow:none;padding:2px 12px 2px 4px;color:#ece3cc;font-family:var(--lbF);filter:drop-shadow(0 8px 18px rgba(0,0,0,.65)) drop-shadow(0 0 10px rgba(220,190,120,.12))}
.toast.ach i{border-radius:0;width:22px;height:22px;margin:0 4px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a);box-shadow:0 0 8px rgba(220,190,120,.45)}
.toast.ach i>*{transform:rotate(-45deg)}
.toast.ach i{font-size:0}
.toast.ach i::after{content:'';width:6px;height:6px;background:#1a1408;transform:none}
.toast.ach small{color:#a39c8a;font-weight:400}
/* 기록 캡처 창 */
.cap-ov{background:rgba(4,5,10,.62)}
.cap-box{border:12px solid transparent;border-image:var(--lbPN) 14 fill / 16px / 0 stretch;background:none;border-radius:0;padding:12px 14px 10px;filter:drop-shadow(0 14px 30px rgba(0,0,0,.6))}
.cap-box h3{position:relative;font-family:var(--lbF);font-weight:700;color:#e8d3a0;padding-bottom:10px;background:linear-gradient(90deg,rgba(216,189,124,.5),rgba(216,189,124,0)) left bottom/100% 1px no-repeat}
.cap-box h3::after{content:'';position:absolute;left:-3px;bottom:-3px;width:7px;height:7px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a);box-shadow:0 0 5px rgba(220,190,120,.6)}
.cap-box label{font-family:var(--lbF);color:#ece3cc}
.cap-box label.sub{color:#a39c8a}
.cap-box input{accent-color:#d8bd7c}
.cap-box .note{color:#8f8878}
/* 보낸 조 창(#info) */
#info .gt-pop .report.gh{border:1px solid rgba(196,164,104,.2);border-radius:7px;background:linear-gradient(180deg,rgba(6,8,16,.85),rgba(10,13,24,.85));box-shadow:inset 0 0 0 3px rgba(6,8,16,.9),inset 0 0 0 4px rgba(196,164,104,.08)}
#info .gt-pop .meta{font-family:var(--lbF);color:#8f8878}
#info .gt-pop .why{border-left:0;position:relative;padding-left:12px;color:#8f8878}
#info .gt-pop .why::before{content:'';position:absolute;left:0;top:4px;bottom:4px;width:1px;background:linear-gradient(180deg,rgba(216,189,124,.5),rgba(216,189,124,.05))}
/* 캡처 창 · 정보 창 속 일반 단추 */
.cap-box .btn,#info .actions .btn{border:9px solid transparent!important;border-image:var(--lbTG) 14 fill / 13px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;padding:3px 12px!important;color:#ddd3bb!important;font-family:var(--lbF);font-weight:700;filter:drop-shadow(0 2px 4px rgba(0,0,0,.5))}
.cap-box .btn.primary,#info .actions .btn.primary{border-image-source:var(--lbPR)!important;color:#f6edd3!important;letter-spacing:.04em}
.cap-box .btn:disabled,#info .actions .btn:disabled{opacity:.45}
'''
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read()
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    print('ig9 ok')
    open(P, 'w', encoding='utf-8').write(s)
