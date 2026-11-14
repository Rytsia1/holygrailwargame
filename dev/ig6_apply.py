"""6단계(전투 · 위기, 11-15): 전투 비교 카드 · 효과 칩 · 칩 설명 말풍선 · 위기 현판 모서리.
- 비교 카드: 남색 카드 + 겹테(나 금빛 · 적 붉은빛), 이름 명조 굵게, 막대는 어두운 홈 + 그라데이션
- 효과 칩: 모서리만 둥근 사각형 · 말풍선: 남색 + 금빛 겹테
- 화면을 덮는 연출(보스 등장 · 보구 격돌 · 령주 · 죽음)은 그대로
사용: python3 ig6_apply.py <game.html>"""
import sys
CSS = r'''
/* ---- 6단계: 전투 · 위기 (ig6_apply) ---- */
/* 6단계: 전투 · 위기 */
#dlg .vs .side{border-radius:7px;border:1px solid rgba(196,164,104,.2);background:linear-gradient(180deg,rgba(17,23,40,.94),rgba(8,11,21,.94));box-shadow:inset 0 0 0 3px rgba(8,11,21,.9),inset 0 0 0 4px rgba(196,164,104,.08)}
#dlg .vs .side.me{border-color:rgba(216,189,124,.5);box-shadow:inset 0 0 0 3px rgba(8,11,21,.9),inset 0 0 0 4px rgba(216,189,124,.14)}
#dlg .vs .side.foe{border-color:rgba(210,106,116,.5);background:linear-gradient(180deg,rgba(28,14,24,.94),rgba(12,7,14,.94));box-shadow:inset 0 0 0 3px rgba(12,7,14,.9),inset 0 0 0 4px rgba(210,106,116,.14)}
#dlg .vs .who2{font-family:var(--lbF);font-weight:700;color:#ece3cc}
#dlg .vs .side.me .who2{color:#f2e2b4}
#dlg .vs .side.foe .who2{color:#f3d2d6}
#dlg .vs .who2 small{font-family:var(--lbF);font-weight:400;color:#8f8878}
#dlg .vs .cl{font-family:var(--lbF);color:#8f8878}
#dlg .vs .pg small{font-family:var(--lbF);color:#7f7a6d}
#dlg .vs .pg b{color:#e8d3a0}
#dlg .vs .hb{height:5px;background:rgba(4,6,12,.8);box-shadow:inset 0 0 0 1px rgba(196,164,104,.14)}
#dlg .vs .hb i{background:linear-gradient(90deg,#8e3440,#d86a74)}
#dlg .vs .hb.sm{height:3px}
#dlg .vs .hb.sm i{background:linear-gradient(90deg,#4b5a9a,#8d9de0)}
#dlg .vs .meta{color:#a39c8a}
#dlg .vs .np2{color:#8f8878}
/* 효과 칩과 설명 말풍선 */
.mc{border-radius:4px}
.mc.g{border-color:rgba(216,189,124,.5);color:#e8d3a0;background:rgba(216,189,124,.06)}
.mc.r{border-color:rgba(210,106,116,.5);color:#eeb0b6;background:rgba(210,106,116,.06)}
.mpop{background:linear-gradient(180deg,#121829,#0a0e1b);border-color:rgba(196,164,104,.35);border-radius:7px;box-shadow:0 10px 24px rgba(0,0,0,.6),inset 0 0 0 3px rgba(10,14,27,.9),inset 0 0 0 4px rgba(196,164,104,.1)}
.mpop:before{background:#121829;border-color:rgba(196,164,104,.35)}
.mpop b{font-family:var(--lbF);font-weight:700}
.mpop.g b{color:#e8d3a0}
.mpop small{color:#8f8878}
/* 위기 현판 */
#pairs .cxb{border-radius:7px}
/* 연출 점검(11-15): 명조 굵은 이름이 넓어 칭호가 잘리지 않게 한 단계 줄인다 */
#dlg .vs .who2{font-size:15px}
#dlg .vs .who2 small{font-size:11.5px;margin-left:5px}
'''
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read()
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    print('ig6 ok')
    open(P, 'w', encoding='utf-8').write(s)
