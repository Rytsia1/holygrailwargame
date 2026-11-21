"""11-21: 보육원 출신의 부모 → 선생님 바꿔 쓰기(orf) 정리 (커뮤니티 제보 11-21: 아이 관련 사건이 일본어판에서 한국어로)
① orf()가 바꾼 문장 중 번역이 없던 3줄(어린 시절 사건 g/l2_27 · 장난감 사건) → 영 · 일 · 중 간체 · 번체 추가
   (보육원 출신으로 250번 돌려 본 생에서 실제로 나온, 번역 없는 바꿔 쓴 줄은 이것뿐이었다)
② 의뢰인 사건 l2_43: '딸은 왔다. 하지만 아버지를 알아보지 못했다'의 아버지는 의뢰인인데,
   보육원 출신이면 '선생님을 알아보지 못했다'로 바뀌어 뜻이 틀어지고 번역도 없었다 → 이 사건은 바꿔 쓰지 않는다(noOrf)
사용: python3 orphan_apply.py <game.html>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'noOrf' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

rp("    {id:'l2_43',a:[18,30],w:4.5,", "    {id:'l2_43',a:[18,30],w:4.5,noOrf:1,")   # 아버지 = 의뢰인
rp("  function showEv(e){\n", "  function showEv(e){ const orf=e.noOrf?(t=>t):orf0;   // noOrf: 부모가 아닌 사람의 부모 이야기는 바꿔 쓰지 않는다 (11-21)\n")
rp("  function orf(t){\n", "  function orf(t){\n", 1)
s = s.replace("  function orf(t){\n", "  const orf0=t=>orf(t);\n  function orf(t){\n", 1)
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

D = [
 ('그 아이는 혼이 났다. 장난감은 돌아오지 않았지만, 선생님이 새것을 사 주었다.',
  'That kid got a scolding. The toy never came back, but the teacher bought you a new one.',
  'その子は叱られた。おもちゃは戻らなかったが、先生が新しいのを買ってくれた。',
  '那孩子挨了骂。玩具没能拿回来，不过老师给你买了个新的。', '那孩子挨了罵。玩具沒能拿回來，不過老師給你買了個新的。'),
 ('선생님 곁에서 잠든다', 'Fall asleep next to the teacher', '先生のそばで眠る', '依偎在老师身边睡着', '依偎在老師身邊睡著'),
 ('선생님의 숨소리를 세다가 잠들었다.', "You fell asleep counting the teacher's breaths.", '先生の寝息を数えているうちに眠った。',
  '你数着老师的呼吸声睡着了。', '你數著老師的呼吸聲睡著了。'),
]
s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, *_ in D], [])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _b, _c, d, e in D:
    if a not in Z: Z[a] = [d, e]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 사전', nd, '· 중국어', n)
