"""11-17: 서번트 성별 바꾸기 — 프렐라티는 남성, 카게키요는 여성
- SEX_OVR에 prelati:'m', kagekiyo:'f' (지칭 · 인연 기본 트랙 · 이모/삼촌 같은 말은 h.fem을 따라 저절로 바뀐다)
- 두 서번트를 3인칭으로 가리키는 지문 '(그녀는 …)' / '(그는 …)'을 바꾸고, 영 · 일 · 중 번역도 맞춘다
- 이름으로 가리키는 영어 번역(he/his)도 카게키요는 she/her로
사용: python3 sexfix_apply.py <game.html>"""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if "prelati:'m'" in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    cut = s.find('const I18N_DICT')
    k = s[:cut].count(o)
    if k != c: miss.append((o[:80], k)); return
    s = s[:cut].replace(o, n) + s[cut:]

rp("const SEX_OVR={enkidu:'x',caenis:'m',melusine:'f'};",
   "const SEX_OVR={enkidu:'x',caenis:'m',melusine:'f',prelati:'m',kagekiyo:'f'};   // 11-17: 프렐라티 남성 · 카게키요 여성")

m = re.search(r'const I18N_DICT=(\{.*?\});\n', s, re.S); D = json.loads(m.group(1))
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8'))

PRE = ['웃다가 문득 입을 다물었다.', '장바구니를 흔들며 앞질러 걸었다.', '카드 한 장을 뒤집어 보였다. 아무 그림도 없었다.',
       '베개 옆에 종이꽃 하나를 두고 갔다.', '당신 손에 카드 한 장을 쥐여 주었다.', '웃으며 당신 이마에 손가락을 댔다.',
       '잔 두 개를 든 채 잠깐 망설였다.', '아이를 안고 숨을 죽였다.', '당신 어깨를 친 손으로 카드를 튕겼다.',
       '잔 하나를 뒤집어 보였다가 바로 돌려놓았다.', '마지막 카드를 당신 주머니에 넣었다.',
       '흩어지는 손을 흔들어 작은 불꽃을 피웠다.', '잔에 동전 하나를 넣었다가 사라지게 했다.']
KAG = ['장바구니를 쥔 채 멈춰 섰다.', '창가에서 몸을 돌렸다.', '당신 손을 잡았다가, 서툴게 놓았다.', '당신 손을 더듬어 찾아 꼭 쥐었다.',
       '창을 열어 두고 오래 바람을 맞았다.', '아이를 칼처럼 받쳐 든 채 굳어 버렸다.', '당신 어깨를 친 제 손을 내려다보았다.',
       '문 앞에 칼을 무릎에 놓고 앉아 있었다.', '붉은 깃발 조각을 당신 손목에 감아 주었다.', '당신 어깨를 짚고 오래 서 있었다.',
       '잔 하나를 바다 쪽 창가에 먼저 놓았다.']

def to_m(en, ja, zh):
    en = re.sub(r'\bShe\b', 'He', en); en = re.sub(r'\bshe\b', 'he', en); en = re.sub(r'\bher\b', 'his', en)
    return en, ja.replace('彼女は', '彼は'), [z.replace('她', '他') for z in zh]
def to_f(en, ja, zh):
    en = re.sub(r'\bHe\b', 'She', en); en = re.sub(r'\bhe\b', 'she', en); en = re.sub(r'\bhis\b', 'her', en)
    return en, re.sub(r'彼は', '彼女は', ja), [z.replace('他', '她') for z in zh]

items = []
for body, old, new, conv in [(x, '그녀는 ', '그는 ', to_m) for x in PRE] + [(x, '그는 ', '그녀는 ', to_f) for x in KAG]:
    ko0, ko1 = old + body, new + body
    tail = ' …{M}. 헤이케' if body == '당신 어깨를 친 제 손을 내려다보았다.' else ''   # 같은 지문이 다른 서번트(가웨인 쪽)에도 있다
    rp('(' + ko0 + ')' + tail, '(' + ko1 + ')' + tail)
    if ko0 not in D['en'] or ko0 not in Z: miss.append(('번역 없음', ko0)); continue
    en, ja, zh = conv(D['en'][ko0], D['ja'][ko0], Z[ko0])
    items.append((ko1, en, ja, zh))
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

# 이름으로 가리키는 영어 번역: 카게키요 he → she (일본어 · 중국어는 대명사가 없어 그대로)
OVR = {
    '…헤이케의 어린 임금. 바다로 갔다. 카게키요는, 따라가지 못했다. 그날부터, 죽지 못한다.':
        '…The young emperor of the Heike. Went into the sea. Kagekiyo, could not follow. From that day, she cannot die.',
    '…딸이, 찾아왔다. 늙은 장님에게. 카게키요는, 모른다고 했다. …부끄러웠다. 그것뿐.':
        '…My daughter, came looking. For the old blind one. Kagekiyo said, she knew no such girl. …I was ashamed. That is all.',
    '카게키요는 "겐지"라는 글자를 보면 칼을 뽑으려 했다.':
        'Whenever Kagekiyo saw the characters for “Genji,” she tried to draw her sword.',
    '카게키요는 해변에 서서 파도를 오래 보았다. 바다를 향해 무언가 중얼거리고는 등을 돌렸다.':
        'Kagekiyo stood on the beach and watched the waves for a long time. She muttered something toward the sea, then turned her back.',
}
for k in OVR:
    if k not in D['en']: print('못 찾음', k); sys.exit(1)

s, nd, _ = i18n.add(s, dict_items=[(a, b, c) for a, b, c, _z in items])
s, no, _ = i18n.add(s, dict_items=[(k, v, D['ja'][k]) for k, v in OVR.items()], overwrite=True)
open(P, 'w', encoding='utf-8').write(s)
n = 0
for a, _b, _c, z in items:
    if a not in Z: Z[a] = z; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 지문', len(items), '· 새 번역', nd, '· 영어 고침', no, '· 중국어', n)
for a, b, c, z in items[:2] + items[-2:]: print(' ', a, '|', b, '|', c, '|', z[0])
