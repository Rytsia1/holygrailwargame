"""11-21: iPhone 홈 화면 앱(standalone)에서 창을 위로 스크롤할 수 없어 닫기 단추를 못 누르던 문제 (커뮤니티 제보 11-21, iPhone 17e · iOS 27.2.1)
- 홈 화면 앱은 상태 표시줄(black-translucent) 아래까지 화면을 그린다. 그런데 결정 · 정보 창(.dlg)은 위 여백이 16px뿐이라,
  창이 길면 창 윗부분(접기 · 닫기 단추)이 상태 표시줄 뒤에 깔렸고 더 위로는 스크롤되지 않았다
  → .dlg 위 · 양옆 여백에 safe-area를 더한다
- 창 안을 끝까지 스크롤하면 iOS가 뒤의 페이지를 대신 끌어 창이 따라 움직이지 않던 일 → 창 · 시트에 overscroll-behavior:contain
- 캡처 창(.cap-ov)은 내용이 화면보다 길면 가운데 정렬 때문에 위아래가 잘린 채 스크롤이 안 됐다
  → 창 자체를 스크롤되게 하고 상자는 margin:auto로 가운데(길면 위에서부터)
- 시트 높이 한도가 테두리 · 여백을 빼고 재여 긴 창이 위로 넘치던 것 → box-sizing:border-box
- 결과 화면(#ending) 첫 줄도 상태 표시줄 아래로
사용: python3 pwa_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'safe-area · 11-21' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

rp(".dlg{position:fixed;inset:0;z-index:50;display:flex;align-items:flex-end;justify-content:center;background:rgba(10,8,14,.55);padding:16px;padding-bottom:calc(16px + env(safe-area-inset-bottom,0px))}",
   ".dlg{position:fixed;inset:0;z-index:50;display:flex;align-items:flex-end;justify-content:center;background:rgba(10,8,14,.55);padding:16px;padding-bottom:calc(16px + env(safe-area-inset-bottom,0px));"
   "padding-top:calc(16px + env(safe-area-inset-top,0px));padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));overscroll-behavior:contain}"
   "/* 홈 화면 앱: 상태 표시줄 아래로 · 창 안 스크롤이 뒤 페이지로 새지 않게 (safe-area · 11-21) */")
# 높이 한도가 테두리 · 안쪽 여백을 빼고 잰 값이라 긴 창은 위로 18~27px 넘쳐 상태 표시줄 밑으로 들어갔다 → 테두리까지 넣어 잰다
#  (가로 폭은 예전과 같게: 최대 폭 560 + 여백 · 테두리 약 50)
rp(".sheet{width:100%;max-width:560px;max-height:calc(100% - 20px);overflow:auto;",
   ".sheet{width:100%;max-width:610px;box-sizing:border-box;max-height:calc(100% - 20px);overflow:auto;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;")
rp(".cap-ov{position:fixed;inset:0;z-index:80;display:grid;place-items:center;background:rgba(8,6,12,.72);padding:16px}",
   ".cap-ov{position:fixed;inset:0;z-index:80;display:grid;background:rgba(8,6,12,.72);padding:16px;padding-top:calc(16px + env(safe-area-inset-top,0px));padding-bottom:calc(16px + env(safe-area-inset-bottom,0px));overflow-y:auto;overscroll-behavior:contain;-webkit-overflow-scrolling:touch}.cap-ov>*{margin:auto}")
rp("#ending{padding-block:48px}", "#ending{padding-block:48px;padding-top:calc(48px + env(safe-area-inset-top,0px))}")

if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
