"""4단계(상태 패널, 11-15): 서번트 · 일곱 조 · 상태 · 익힌 기술 · 올해의 목표 · 가족 카드.
- 카드: 남색 판 + 금빛 겹테 · 제목에 마름모와 흐려지는 선 · 마술 회로는 각진 꼬리표
- 수치 막대는 어두운 홈 + 그라데이션(색 구분 그대로) · 위험 점은 붉은 마름모
- 참가자 행은 둥근 사각형, 내 서번트는 금빛 · 동맹은 초록
- 올해의 목표는 판 단추(고르면 파란 판 + 금빛 밑줄)
- 익힌 기술 · 가족: 오른쪽 값(숙련 단계 · 나이)을 같은 세로줄에 맞춘다
  (그 겨울의 서번트 줄의 ' · 세상을 떠남'을 <b> 안으로 옮겨 칸이 어긋나지 않게)
사용: python3 ig4_apply.py <game.html>"""
import sys
CSS = r'''
/* ---- 4단계: 상태 패널 (ig4_apply) ---- */
/* 4단계: 상태 패널 */
#game aside .card{position:relative;border:1px solid rgba(196,164,104,.22)!important;border-radius:8px!important;background:linear-gradient(180deg,rgba(17,23,40,.94),rgba(8,11,21,.94))!important;box-shadow:inset 0 0 0 3px rgba(8,11,21,.9),inset 0 0 0 4px rgba(196,164,104,.09),0 6px 16px rgba(0,0,0,.35)}
#game aside .card h3{position:relative;justify-content:flex-start;gap:10px;align-items:center;font-family:var(--lbF);font-weight:700;font-size:12.5px;letter-spacing:.12em;color:#c9ad72}
#game aside .card h3::before{content:'';flex:none;width:6px;height:6px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a);box-shadow:0 0 4px rgba(220,190,120,.5)}
#game aside .card h3::after{content:'';flex:1;order:1;height:1px;background:linear-gradient(90deg,rgba(216,189,124,.4),rgba(216,189,124,0))}
#game aside .card h3 small{order:2;font-family:var(--lbF);color:#8f8878}
#game aside .card h3 small#circ{border-radius:4px;border-color:rgba(216,189,124,.5);background:rgba(216,189,124,.08);color:#e8d3a0;font-family:var(--lbF)}
#game aside .card h3 small#circ b{color:#f2e2b4}
/* 서번트·주인공 */
#game .herocard .hname{font-family:var(--lbF);font-weight:700;color:#ece3cc;letter-spacing:.01em}
#game .herocard .htitle{color:#a39c8a;font-family:var(--lbF)}
#game .params div{border-radius:5px;border-color:rgba(196,164,104,.2);background:rgba(216,189,124,.03)}
#game .params small{font-family:var(--lbF);color:#8f8878}
#game .params b{color:#e8d3a0}
#game .np{border-top:0;position:relative;background:linear-gradient(90deg,rgba(216,189,124,.35),rgba(216,189,124,0)) left top/100% 1px no-repeat}
#game aside .np .nh{font-family:var(--lbF);color:#c9ad72;letter-spacing:.06em}
#game aside .np .nh>span:first-child{color:#e2c98e;font-weight:700}
#game aside .np .nh .nr{color:#8f8878;letter-spacing:0;font-family:var(--f-ui)}
#game aside .np-role{border-radius:7px;border-color:rgba(216,189,124,.35);background:linear-gradient(180deg,rgba(17,23,40,.9),rgba(8,11,21,.9));box-shadow:inset 0 0 0 3px rgba(8,11,21,.9),inset 0 0 0 4px rgba(196,164,104,.12)}
#game aside .np-role .rh{color:#e2c98e;font-family:var(--lbF)}
#game .np .nn{font-family:var(--lbF);font-weight:700;color:#e8d3a0}
/* 수치 막대 */
#game .stat .lb,#game .rl-lb{font-family:var(--lbF);color:#a39c8a}
#game .stat .v{color:#ddd3bb}
#game .track{height:5px;border-radius:3px;background:rgba(4,6,12,.8);box-shadow:inset 0 0 0 1px rgba(196,164,104,.14)}
#game .track i{border-radius:3px;background:linear-gradient(90deg,#9c7f45,#e2c98e)}
#game .track.mana i{background:linear-gradient(90deg,#4b5a9a,#8d9de0)}
#game .track.health i{background:linear-gradient(90deg,#4f7a52,#8fbf8a)}
#game .track.hp i{background:linear-gradient(90deg,#8e3440,#d86a74)}
#game .track.wealth i{background:linear-gradient(90deg,#9a5a2c,#e09a5e)}
#game .prof{color:#a39c8a}
#game .hint{color:#7f7a6d}
/* 참가자 */
#game .pair{border-radius:6px;border-color:rgba(196,164,104,.16);background:rgba(8,11,21,.5)}
#game .pair .c{font-family:var(--lbF);font-weight:700;color:#ddd3bb}
#game .pair.me{border-color:rgba(216,189,124,.6);background:linear-gradient(90deg,rgba(216,189,124,.1),rgba(216,189,124,0) 70%)}
#game .pair.me .c{color:#f2e2b4}
#game .pair.ally{border-color:rgba(122,170,120,.55)}
#game .pair .gh-mk{border-radius:3px}
#game .pair-sep{display:flex;align-items:center;gap:8px;font-family:var(--lbF);color:#8f8878}
#game .pair-sep::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(196,164,104,.3),rgba(196,164,104,0))}
#game .dots i{width:6px;height:6px;border-radius:0;transform:rotate(45deg) scale(.85);background:rgba(196,164,104,.18)}
#game .dots i.on{background:#d26a74;box-shadow:0 0 4px rgba(210,106,116,.5)}
#game .rl-na{border-radius:6px}
/* 이번 주 집중 */
#game .focus button{position:relative;border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;background:none!important;border-radius:0!important;padding:1px 2px!important;color:#a39c8a;font-family:var(--lbF);filter:drop-shadow(0 2px 3px rgba(0,0,0,.45))}
#game .focus button[aria-pressed="true"]{border-image-source:var(--lbPR)!important;color:#f3e8cb;text-shadow:0 0 8px rgba(230,200,140,.45)}
#game .focus button[aria-pressed="true"]::after{content:'';position:absolute;left:22%;right:22%;bottom:-4px;height:1px;background:linear-gradient(90deg,transparent,#d8bd7c,transparent)}
#game .focus-d{color:#8f8878}
/* 가족 */
#game .fam{color:#a39c8a}
#game .fam b{color:#e8d3a0;font-weight:600}
/* 익힌 기술 · 가족: 오른쪽 값을 한 줄로 맞춘다 */
#game #arts,#game #fam{grid-template-columns:max-content minmax(0,1fr);column-gap:12px;row-gap:3px}
#game #arts>div:has(>b),#game #fam>div:has(>b){display:contents}
#game #arts>div:not(:has(>b)),#game #fam>div:not(:has(>b)){grid-column:1/-1}
#game #arts>div>b,#game #fam>div>b{min-width:0}
'''
OLD = "rows.push(`<div>배우자 <b>${h.name}</b>${rv.died?' · 세상을 떠남':''}</div>`)"
NEW = "rows.push(`<div>배우자 <b>${h.name}<span>${rv.died?' · 세상을 떠남':''}</span></b></div>`)"
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read()
    assert s.count(OLD) == 1, 'fam spouse line'
    s = s.replace(OLD, NEW)
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    print('ig4 ok')
    open(P, 'w', encoding='utf-8').write(s)
