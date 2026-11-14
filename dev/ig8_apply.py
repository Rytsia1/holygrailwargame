"""8단계(결과 화면, 11-15): 한 사람의 기록 · 성배전쟁 기록 · 보내기 · 의견 카드 · 단추.
- 카드: 남색 + 금빛 겹테 · 제목에 금빛 밑줄과 마름모 · 소제목에 마름모와 흐려지는 줄
- 특별한 결말(검은 성배 · 단꿈 · 달로 간 잔)은 바탕만 남색으로 맞추고 고유 꾸밈은 그대로, 이름 · 마름모는 결말 색
- 단추: 다시 태어나기 · 보낼 조 확인하기 = 파란 판, 나머지 = 작은 판
- 캡처 이미지(.cap-stage)는 그대로
사용: python3 ig8_apply.py <game.html>"""
import sys
CSS = r'''
/* ---- 8단계: 결과 화면 (ig8_apply) ---- */
/* 8단계: 결과 화면 */
#ending .record,#ending .report,#ending .fb-end,#ending .scn-note{border-radius:8px}
#ending .record:not(.grail):not(.rdream):not(.rmoon),#ending .report,#ending .fb-end{border:1px solid rgba(196,164,104,.22);background:linear-gradient(180deg,rgba(17,23,40,.95),rgba(8,11,21,.95));box-shadow:inset 0 0 0 3px rgba(8,11,21,.9),inset 0 0 0 4px rgba(196,164,104,.09),0 8px 22px rgba(0,0,0,.4)}
#ending .record.grail:not(.dark){background:radial-gradient(120% 60% at 50% -10%,rgba(224,178,92,.10),transparent 60%),linear-gradient(180deg,rgba(17,23,40,.96),rgba(8,11,21,.96))}
#ending .record .eyebrow{display:flex;align-items:center;gap:8px;font-family:var(--lbF);font-weight:700;color:#c9ad72;letter-spacing:.12em}
#ending .record .eyebrow::before{content:'';flex:none;width:6px;height:6px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a)}
#ending .record .endtag{border-radius:4px;font-family:var(--lbF)}
#ending .record .rn{font-family:var(--lbF);font-weight:700;color:#f2e2b4;letter-spacing:.02em}
#ending .record dt,#ending .report .mine dt{font-family:var(--lbF);color:#a39c8a}
#ending .record dd{color:#ece3cc}
#ending .record blockquote,#ending .report blockquote{border-left:0;position:relative;padding-left:16px}
#ending .record blockquote::before,#ending .report blockquote::before{content:'';position:absolute;left:0;top:4px;bottom:4px;width:2px;background:linear-gradient(180deg,#d8bd7c,rgba(216,189,124,.15))}
#ending .record.rdream blockquote::before{background:linear-gradient(180deg,#f08cb8,rgba(240,140,184,.15))}
#ending .record.rmoon blockquote::before{background:linear-gradient(180deg,#e86aa8,rgba(232,106,168,.15))}
#ending .record .notes span{font-family:var(--lbF);color:#c9ad72}
/* 성배전쟁 기록 · 그 밖의 보고 카드 */
#ending .report h3{position:relative;font-family:var(--lbF);font-weight:700;color:#e8d3a0;padding-bottom:10px;margin-bottom:8px;background:linear-gradient(90deg,rgba(216,189,124,.45),rgba(216,189,124,0)) left bottom/100% 1px no-repeat}
#ending .report h3::after{content:'';position:absolute;left:-3px;bottom:-3px;width:7px;height:7px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a);box-shadow:0 0 5px rgba(220,190,120,.6)}
#ending .report .sub{color:#8f8878}
#ending .report h4{display:flex;align-items:center;gap:8px;font-family:var(--lbF);font-weight:700;font-size:12.5px;color:#c9ad72}
#ending .report h4::before{content:'';flex:none;width:5px;height:5px;transform:rotate(45deg);background:#c9ad72}
#ending .report h4::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(216,189,124,.35),rgba(216,189,124,0))}
#ending .report .verdict{font-family:var(--lbF);font-weight:700;color:#f0e6cc;background:linear-gradient(90deg,rgba(216,189,124,.08),rgba(8,11,21,.4));border-radius:0 6px 6px 0}
#ending .report .verdict small{font-weight:400}
#ending .report .stats div{border-radius:6px;background:rgba(6,8,16,.6);box-shadow:inset 0 0 0 1px rgba(196,164,104,.16)}
#ending .report .stats b{color:#e8d3a0}
#ending .report .stats span{font-family:var(--lbF);color:#8f8878}
#ending .report .seals i{border-radius:2px}
#ending .report .pairs-t td{border-top-color:rgba(196,164,104,.12)}
#ending .report .pairs-t tr.me td{background:rgba(216,189,124,.07)}
#ending .report .pairs-t .c{font-family:var(--lbF);font-weight:700}
#ending .report summary{font-family:var(--lbF);color:#c9ad72;cursor:pointer}
#ending .report .tl .dy>b{font-family:var(--lbF);font-weight:700;color:#c9ad72}
#ending .lf-chip{border-radius:4px}
/* 단추 */
#ending .btn{border:9px solid transparent!important;border-image:var(--lbTG) 14 fill / 13px / 0 stretch!important;background:none!important;border-radius:0!important;box-shadow:none!important;padding:4px 14px!important;color:#ddd3bb!important;font-family:var(--lbF);font-weight:700;filter:drop-shadow(0 2px 4px rgba(0,0,0,.5))}
#ending .btn.primary{border-image-source:var(--lbPR)!important;color:#f6edd3!important;letter-spacing:.06em;filter:drop-shadow(0 3px 7px rgba(0,0,0,.6)) drop-shadow(0 0 8px rgba(220,190,120,.14))}
#ending .btn:hover:not(:disabled){color:#f3e8cb!important}
#ending .pn-btn{border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;background:none!important;border-radius:0!important;padding:3px 10px!important;color:#ddd3bb!important;font-family:var(--lbF);filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}
#ending .pn-btn::before{background:#d8bd7c}
#ending .fb-end p{font-family:var(--lbF);color:#ece3cc}
#ending .scn-note{border-color:rgba(216,189,124,.35);background:rgba(216,189,124,.05)}
/* 특별한 결말: 바탕만 남색으로 맞추고, 결말 고유의 색은 이름 · 마름모에 */
#ending .record.grail.dark{background:radial-gradient(120% 60% at 50% -10%,rgba(150,50,160,.14),transparent 60%),linear-gradient(180deg,rgba(17,20,38,.96),rgba(9,9,20,.96))}
#ending .record.grail.dark .rn{color:#efd2ea}
#ending .record.grail.dark .eyebrow{color:#c99ac4}
#ending .record.grail.dark .eyebrow::before{background:linear-gradient(135deg,#f0c8ea,#a2408c)}
#ending .record.rdream{background:radial-gradient(120% 70% at 50% -10%,rgba(255,170,205,.13),transparent 60%),linear-gradient(180deg,#111729,#090c17)}
#ending .record.rmoon{background:linear-gradient(180deg,#111729,#090c17) padding-box,linear-gradient(90deg,#e86aa8,#cfd6ff 55%,#9fb0ff) border-box}
#ending .record.rdream .rn{color:#ffe0ec}
#ending .record.rmoon .rn{color:#eef0ff}
#ending .record.rdream .eyebrow,#ending .record.rmoon .eyebrow{color:var(--tc)}
#ending .record.rdream .eyebrow::before,#ending .record.rmoon .eyebrow::before{background:var(--tc)}
'''
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read()
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    print('ig8 ok')
    open(P, 'w', encoding='utf-8').write(s)
