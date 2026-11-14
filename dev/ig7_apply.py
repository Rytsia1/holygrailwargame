"""7단계(태어나기, 11-15): 이름 짓기 창 · 건너뛰기 단추. 도시 · 지도 · 달 연출은 그대로.
- 창: 남색 판 · 첫 문장 아래 금빛 밑줄과 마름모
- 입력칸: 어두운 남색 + 금빛 테두리(입력 중) · 이름 미리보기: 명조 굵게 + 양옆 금빛 줄
- 단추: 다른 이름 = 작은 판 · 이 이름으로 = 파란 판
사용: python3 ig7_apply.py <game.html>"""
import sys
CSS = r'''
/* ---- 7단계: 태어나기 (ig7_apply) ---- */
/* 7단계: 태어나기 */
.birth .b-name{border:12px solid transparent!important;border-image:var(--lbPN) 14 fill / 16px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;padding:14px 16px 10px!important;filter:drop-shadow(0 14px 30px rgba(0,0,0,.65))}
.birth .b-lead{font-family:var(--lbF);color:#ece3cc;padding-bottom:10px;position:relative;background:linear-gradient(90deg,rgba(216,189,124,.45),rgba(216,189,124,0)) left bottom/100% 1px no-repeat}
.birth .b-lead::after{content:'';position:absolute;left:-3px;bottom:-3px;width:7px;height:7px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a);box-shadow:0 0 5px rgba(220,190,120,.6)}
.birth .b-f>span{font-family:var(--lbF);color:#c9ad72;letter-spacing:.06em}
.birth .b-f input{border-radius:6px;border-color:rgba(196,164,104,.28);background:rgba(6,8,16,.85);color:#f0e6cc;box-shadow:inset 0 1px 3px rgba(0,0,0,.5)}
.birth .b-f input:focus{outline:none;border-color:#d8bd7c;box-shadow:inset 0 1px 3px rgba(0,0,0,.5),0 0 0 2px rgba(216,189,124,.18)}
.birth .b-prev{display:flex;align-items:center;justify-content:center;gap:12px;font-family:var(--lbF);font-weight:700;color:#f2e2b4;text-shadow:0 0 12px rgba(230,200,140,.3)}
.birth .b-prev::before,.birth .b-prev::after{content:'';flex:0 1 54px;height:1px;background:linear-gradient(90deg,rgba(216,189,124,0),rgba(216,189,124,.6))}
.birth .b-prev::after{background:linear-gradient(90deg,rgba(216,189,124,.6),rgba(216,189,124,0))}
.birth .b-act .btn{border:9px solid transparent!important;border-image:var(--lbTG) 14 fill / 13px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;padding:3px 12px!important;color:#ddd3bb!important;font-family:var(--lbF);font-weight:700;filter:drop-shadow(0 2px 4px rgba(0,0,0,.5))}
.birth .b-act .btn.primary{border-image-source:var(--lbPR)!important;color:#f6edd3!important;letter-spacing:.06em;filter:drop-shadow(0 3px 7px rgba(0,0,0,.6)) drop-shadow(0 0 8px rgba(220,190,120,.14))}
.birth .b-opt{font-family:var(--lbF);color:#8f8878}
.birth .b-opt input{accent-color:#d8bd7c}
.birth .b-skip{border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;background:none!important;border-radius:0!important;padding:1px 10px!important;color:#c9ad72;font-family:var(--lbF);filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}
.birth .b-skip:hover{color:#f3e8cb}
'''
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read()
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    print('ig7 ok')
    open(P, 'w', encoding='utf-8').write(s)
