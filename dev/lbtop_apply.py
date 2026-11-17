"""11-17: 로비 배경 위쪽에 하늘 없는 띠가 생기던 문제
- 화면이 덜 넓은 비율(가로/세로 약 1.15~1.47, 예: 1440x1100 · 1280x1024)에서
  '배경 폭의 78%는 늘 보이게' 하는 확대 상한(sMax)에 걸리면 배경이 아래로 내려가(y>0) 위쪽에 단색 띠가 보였다.
  2단계는 도시 아랫줄을 화면 맨 아래(0.97vh)로 내리므로 더 잘 걸린다.
- 이제: 상한을 적용한 뒤에도 y>0이면 배경 위 끝을 화면 위에 붙인다(y=0). 그러면 아래가 모자라면 세로를 채울 만큼만 더 키운다.
  도시 아랫줄은 그만큼 조금 위로 올라간다.
사용: python3 lbtop_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if '배경 위 끝은 늘 화면 위에' in s: print('이미 적용됨'); sys.exit(0)
o = "const sMax=vw/(W*.78);if(s>sMax){s=sMax;y=line-FY*s}\n"
n = ("const sMax=vw/(W*.78);if(s>sMax){s=sMax;y=line-FY*s}\n"
     " if(y>0){y=0;if(H*s<vh)s=vh/H}   // 배경 위 끝은 늘 화면 위에: 상한에 걸려 내려가면 위쪽에 하늘 없는 띠가 보인다 (11-17)\n")
if s.count(o) != 1: print('못 찾음', s.count(o)); sys.exit(1)
s = s.replace(o, n)
open(P, 'w', encoding='utf-8').write(s)
print('적용 끝')
