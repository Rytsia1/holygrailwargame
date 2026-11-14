"""3단계(기록 피드, 11-15): 지금 일어난 일 · 생애 기록 제목 · 날짜 바뀌는 줄 · 고른 행동 · 효과 칩 · 이전 기록 더 보기.
- 지금 일어난 일: 흐려지는 세로선 + 마름모(평소 금 · 전쟁 붉은빛), 옅은 남색 바탕
- 날짜 바뀌는 줄: 마름모 + 날짜 + 흐려지는 선 · 고른 행동은 금 마름모 · 칩은 모서리만 둥근 사각형 · 더 보기는 판 단추
- 사건 종류별 글자색은 그대로
사용: python3 ig3_apply.py <game.html>"""
import sys
CSS = r'''
/* ---- 3단계: 기록 피드 (ig3_apply) ---- */
/* 3단계: 기록 피드 */
#game .now{position:relative;border-left:0!important;padding:12px 16px 12px 22px!important;background:linear-gradient(90deg,rgba(14,19,34,.72),rgba(14,19,34,.35) 70%,rgba(14,19,34,0));border-radius:0 8px 8px 0}
#game .now::before{content:'';position:absolute;left:0;top:10px;bottom:10px;width:2px;background:linear-gradient(180deg,#d8bd7c,rgba(216,189,124,.15))}
#game .now::after{content:'';position:absolute;left:-2.5px;top:6px;width:7px;height:7px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a);box-shadow:0 0 5px rgba(220,190,120,.6)}
#game.war .now::before{background:linear-gradient(180deg,#d26a74,rgba(210,106,116,.15))}
#game.war .now::after{background:linear-gradient(135deg,#f6c0c5,#b8444f);box-shadow:0 0 5px rgba(230,110,120,.6)}
#game .now .when{font-family:var(--lbF);color:#c9ad72;letter-spacing:.08em}
#game.war .now .when{color:#e09aa2}
#game .now .txt{color:#efe7d6}
#game .feed h3{display:flex;align-items:center;gap:10px;font-family:var(--lbF);font-weight:700;font-size:12.5px;letter-spacing:.12em;color:#c9ad72;margin-bottom:6px}
#game .feed h3::before{content:'';flex:none;width:6px;height:6px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a)}
#game .feed h3::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(216,189,124,.4),rgba(216,189,124,0))}
#game .entry{border-top-color:rgba(196,164,104,.1)!important}
#game .entry .t{font-family:var(--lbF);font-size:11.5px;color:#7f7a6d;letter-spacing:.02em}
#game .entry.war .t{color:#c9727a}
#game .entry.night{border-top:0!important;margin-top:10px;padding-top:10px}
#game .entry.night .b{display:flex;align-items:center;gap:10px;font-family:var(--lbF)!important;font-weight:700}
#game .entry.night .b::before{content:'';flex:none;width:7px;height:7px;transform:rotate(45deg);background:linear-gradient(135deg,#f6c0c5,#b8444f)}
#game .entry.night .b::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(240,162,168,.5),rgba(240,162,168,0))}
#game:not(.war) .entry.night .b{color:#e8d3a0}
#game:not(.war) .entry.night .b::before{background:linear-gradient(135deg,#f2e2b4,#b8975a)}
#game:not(.war) .entry.night .b::after{background:linear-gradient(90deg,rgba(216,189,124,.45),rgba(216,189,124,0))}
#game .entry.q .qt{font-family:var(--lbF);color:#8f8878}
#game .entry.q .pk{font-family:var(--lbF);color:#e2c98e}
#game .entry.q .pk::before{content:'';display:inline-block;width:5px;height:5px;margin:0 8px 2px 1px;transform:rotate(45deg);background:#c9ad72;vertical-align:middle}
#game .delta span{border-radius:4px}
#game .delta span.grp{color:#a39c8a;font-family:var(--lbF)}
#game .entry.guide .b,#game .sub.guide{border-radius:0 6px 6px 0}
#game .more{border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;background:none!important;border-radius:0!important;color:#ddd3bb!important;font-family:var(--lbF);padding:2px 14px!important;justify-self:center;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}
'''
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read()
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    print('ig3 ok')
    open(P, 'w', encoding='utf-8').write(s)
