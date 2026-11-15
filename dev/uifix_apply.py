"""UI 최신화 남은 곳 (11-15)
- 기술 사건 창의 설명 상자(계통 이름 · 입문/숙련/고위 · 익히면 할 수 있는 것): 둥근 모서리 + 왼쪽 금색 막대의 예전 모양을
  새 창 장식(얇은 금테 틀)으로. 단계 칩은 둥근 알약 대신 다른 칩과 같은 각진 칩, 지금 단계는 금테 + 은은한 금빛,
  목록 점은 마름모.
- 결정 창의 「잠시 접기」: 제목 줄이 단추를 덮어 위 · 오른쪽 가장자리만 눌리던 것을, 단추를 제목 위로 올려 단추 전체가 눌리게.
- 유리/불리 (추측) 선택지의 구분선이 틀 밖으로 삐져나가던 것: 오른쪽 여백을 표시 폭에 맞춰 110px로.
- 비스트 위기 밤 선택지: 「센티넬을 사냥한다」 · 「토벌령을 따른다」를 맨 위(1 · 2번)로.
사용: python3 uifix_apply.py <game.html>"""
import sys
CSS = ("#dlg .ai{border:7px solid transparent!important;border-image:var(--lbTG) 14 fill / 12px / 0 stretch!important;background:none!important;"
       "border-radius:0!important;padding:6px 9px 8px!important;margin:12px 0 10px;filter:drop-shadow(0 2px 5px rgba(0,0,0,.4))}\n"
       "#dlg .ai-n{font-family:var(--lbF);font-weight:700;font-size:14.5px;color:#e2c98e;letter-spacing:.02em}\n"
       "#dlg .ai-l{font-family:var(--lbF);color:#a39c8a}\n"
       "#dlg .ai li{color:#ddd3bb}\n"
       "#dlg .ai li:before{border-radius:0;width:4px;height:4px;transform:rotate(45deg);background:#d8bd7c}\n"
       "#dlg .ai-steps span,#dlg .ai-main{border-radius:4px;border:1px solid rgba(216,189,124,.26);background:rgba(9,8,15,.35);color:#8f877a;font-family:var(--lbF)}\n"
       "#dlg .ai-steps span.stp-d{color:#b5aa8f;border-color:rgba(216,189,124,.42)}\n"
       "#dlg .ai-steps span.stp-c{color:#f3e8cb;background:rgba(216,189,124,.2);border-color:#d8bd7c;text-shadow:0 0 6px rgba(230,200,140,.45)}\n"
       "#dlg .ai-main{color:#e2c98e;border-color:rgba(216,189,124,.55)}\n"
       # 잠시 접기: 제목 줄이 단추 위를 덮어 가장자리만 눌리던 것 → 단추를 제목 위로
       "#dlg .dfold{position:relative;z-index:2}\n"
       # 유리/불리 (추측) 표시가 있는 선택지: 새 창에서 오른쪽 여백이 70px로 줄었는데 구분선은 예전 여백(118px)만큼 늘려 틀 밖으로 삐져나감
       # → 여백을 표시 폭에 맞춰 110px로, 구분선은 그 여백 끝까지(−104px)
       "#dlg .choice.hasadv.est{padding-right:110px}")
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    a = "#dlg .choice .cs span,#dlg .choice .adv,#dlg .ai-main,#dlg .ai-steps span{border-radius:4px}"
    if s.count(a) != 1: miss.append((a[:60], s.count(a)))
    else: s = s.replace(a, a + "\n" + CSS)
    # 비스트 위기(봉인 중) 밤 선택지: 센티넬 사냥 · 토벌령을 맨 위로(1 · 2번). 자동 결정은 auto 표시끼리 무작위라 순서와 상관없다
    for o, n in (("ch_.push({t:'센티넬을 사냥한다'", "ch_.unshift({t:'센티넬을 사냥한다'"),
                 ("ch_.push({t:'토벌령을 따른다'", "ch_.splice(ch_[0]&&ch_[0].t==='센티넬을 사냥한다'?1:0,0,{t:'토벌령을 따른다'")):
        if s.count(o) != 1: miss.append((o[:60], s.count(o)))
        else: s = s.replace(o, n)
    print('uifix miss', miss)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
