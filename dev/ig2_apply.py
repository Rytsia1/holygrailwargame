"""2단계(게임 화면 틀, 11-15): 위쪽 이름 줄 · 조작 줄 · 진행 막대 · 모바일 아래 탭 · PC 두 칸 경계.
- 이름 · 성별 · 나이 · 날짜는 세로 가운데 정렬, 칩은 모서리만 살짝 둥근 사각형
- 조작 줄: 시간 판(일시정지 + 배속, 고른 배속은 금빛 밑줄) · 소리 판 · 자동 결정(켜면 파란 판) · 나가기
- 진행 막대: 금빛(전쟁 중 붉은빛) · 아래 탭: 남색 바탕, 위 경계 금선과 마름모, 고른 탭 금빛 밑줄 · PC: 오른쪽 칸 앞 금선
사용: python3 ig2_apply.py <game.html>"""
import sys
CSS = r'''
/* ---- 2단계: 게임 화면 틀 (ig2_apply) ---- */
/* 2단계: 게임 화면 틀 */
.bar{background:linear-gradient(180deg,rgba(9,12,24,.97),rgba(9,12,24,.93))!important;border-bottom:0!important}
.prog{height:2px;background:rgba(216,189,124,.16)!important}
.prog i{background:linear-gradient(90deg,#b8975a,#f2e2b4)!important;box-shadow:0 0 6px rgba(230,200,138,.55)}
.game.war .prog i{background:linear-gradient(90deg,#8e2a33,#e0707a)!important;box-shadow:0 0 6px rgba(224,112,122,.5)}
.who .nm{font-family:var(--lbF);font-weight:700;color:#f1e6cf}
.who .age{color:#e2c98e}
.who .yr{color:#8f8878}
.who .chip,#game .chip{border-radius:4px;border-color:rgba(196,164,104,.35);color:#a39c8a;font-family:var(--lbF);letter-spacing:.04em}
#game .chip.war{border-color:rgba(210,69,79,.75);color:#f0a2a8;background:rgba(120,20,30,.18)}
.ctrl{gap:6px!important}
.ctrl .sep{display:none!important}
.ctrl>button,.ctrl .cg-time{height:34px;box-sizing:border-box;border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}
.ctrl>button{padding:0 8px!important;color:#ddd3bb!important;font-family:var(--lbF)!important;font-size:12.5px!important;display:inline-flex;align-items:center}
.ctrl .cg-time{display:inline-flex;align-items:stretch;padding:0 2px}
.ctrl .cg-time button{position:relative;border:0!important;background:none!important;border-radius:0!important;padding:0 7px!important;color:#8f8878!important;font-family:var(--f-mono);font-size:12.5px}
.ctrl .cg-time button[aria-pressed=true]{color:#f3e8cb!important;text-shadow:0 0 8px rgba(230,200,140,.5)}
.ctrl .cg-time button[aria-pressed=true]::after{content:'';position:absolute;left:18%;right:18%;bottom:1px;height:1px;background:linear-gradient(90deg,transparent,#d8bd7c,transparent)}
.ctrl .cg-time #pauseBtn{color:#d8bd7c!important}
.ctrl .cg-time #pauseBtn::after{display:none}
.ctrl .cg-time #pauseBtn+button{margin-left:2px;box-shadow:inset 1px 0 0 rgba(196,164,104,.22)!important}
.ctrl .sndq{color:#8f8878!important}.ctrl .sndq.on{color:#e2c98e!important}
.ctrl #autoBtn[aria-pressed=true]{border-image-source:var(--lbPR)!important;color:#f3e8cb!important;text-shadow:0 0 8px rgba(230,200,140,.45)}
.keys-g{color:#8f8878!important}
/* 모바일 아래 탭 */
.tabs{background:linear-gradient(180deg,rgba(9,12,24,.97),rgba(6,8,16,.99))!important;border-top:0!important}
.tabs::before{content:'';position:absolute;left:0;right:0;top:0;height:1px;background:linear-gradient(90deg,transparent,rgba(216,189,124,.5) 18%,rgba(216,189,124,.5) 82%,transparent)}
.tabs::after{content:'';position:absolute;left:50%;top:-3.5px;width:7px;height:7px;transform:translateX(-50%) rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a);box-shadow:0 0 5px rgba(220,190,120,.6)}
.tabs button{position:relative;font-family:var(--lbF)!important;color:#8f8878!important;letter-spacing:.1em}
.tabs button[aria-pressed=true]{color:#f3e8cb!important;text-shadow:0 0 8px rgba(230,200,140,.45)}
.tabs button[aria-pressed=true]::after{content:'';position:absolute;left:38%;right:38%;bottom:7px;height:1px;background:linear-gradient(90deg,transparent,#d8bd7c,transparent)}
/* PC 두 칸: 오른쪽 칸 앞에 금선 */
@media (min-width:901px){#game aside{position:relative}#game aside::before{content:'';position:absolute;left:-15px;top:0;bottom:0;width:1px;background:linear-gradient(180deg,rgba(216,189,124,.4),rgba(216,189,124,.12) 60%,rgba(216,189,124,0))}#game aside::after{content:'';position:absolute;left:-18.5px;top:-2px;width:7px;height:7px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a)}}
@media (max-width:440px){.ctrl{gap:4px!important}.ctrl .cg-time{padding:0 1px}.ctrl .cg-time button{padding:0 5px!important;font-size:12px}.ctrl>button{padding:0 5px!important;font-size:12px!important}.ctrl .sndq{gap:2px!important}}

.who{align-items:center!important}
.who .chip.sx{align-self:auto!important}
'''
OLD = '<button id="pauseBtn" aria-pressed="false" title="일시정지 (스페이스)">❚❚</button>\n        <span class="sep"></span>\n        <button data-sp="1"'
NEW = '<span class="cg-time"><button id="pauseBtn" aria-pressed="false" title="일시정지 (스페이스)">❚❚</button><button data-sp="1"'
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n):
        global s
        if s.count(o) != 1: miss.append((o[:50], s.count(o))); return
        s = s.replace(o, n)
    rp(OLD, NEW)
    rp('<button data-sp="8" aria-pressed="false" title="8배속 (4)">8×</button>', '<button data-sp="8" aria-pressed="false" title="8배속 (4)">8×</button></span>')
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    print('ig2 miss', miss)
    open(P, 'w', encoding='utf-8').write(s)
