"""상대 마스터의 소원은 그 사람을 만나거나 전해 들었을 때만 (11-15)
raidintel_apply.py(저격 · 암습)에 이어, 단서가 쌓이는 140곳을 훑어 두 갈래로 고쳤다.
- 'trace' (거처는 알 수 있고 소원은 아님): 동네 산책 · 탐문, 밤 정찰(라이더의 질주 정찰 포함), 뒤밟기 · 미행, 흔적 조사(결계 · 격전지 · 마력의 실 · 탄피 · 덫 · 사역마 · 지맥),
  지붕 정찰 · 사역마의 기억, 교회가 찍어 준 점 · 위치만 기억, 진명 간파의 계시, 공격 행위(함정 · 고지 저격 · 결계 풀기 · 거처 폭파).
- 'watch' (거처도 소원도 아님, 원래 있던 갈래): 다른 조의 싸움을 끝까지 지켜봄, 밤의 질주 소리, 령주 명령을 떨쳐 냄,
  결투 신청을 무시함(대문의 칼자국), 폭발 뒤 거처를 옮김.
단서의 양은 그대로라 진명 · 서번트가 드러나는 속도는 같다. 소원은 대화 · 동맹 · 거래 · 소문 · 편지 · 정보 제공 · 잠입처럼
그 사람에 대해 듣거나 본 단서로 문턱을 넘었을 때만 드러난다.
사용: python3 wishsrc_apply.py <game.html>"""
import sys
TRACE = [
    ("addIntel(t,ri(10,20)+S.st.lore*.06)", "addIntel(t,ri(10,20)+S.st.lore*.06,'trace')"),                 # 동네 산책 · 탐문
    ("+SV(h,'insight')+S.st.lore*.08,'trail');", "+SV(h,'insight')+S.st.lore*.08,'trace');", 2),             # 밤 정찰 · 라이더의 질주 정찰
    ("if(t2){ addIntel(t2,ri(15,25),'trail')", "if(t2){ addIntel(t2,ri(15,25),'trace')"),                     # 돌아오는 길의 흔적
    ("addIntel(p,40,'trail'); return '그는 세 번 길을 꺾고", "addIntel(p,40,'trace'); return '그는 세 번 길을 꺾고"),   # 예배당 뒤밟기
    ("addIntel(p,35,'trail');add({will:-1});return '여자는 병원", "addIntel(p,35,'trace');add({will:-1});return '여자는 병원"),
    ("addIntel(p,45,'trail');add({will:-1});return '아이는", "addIntel(p,45,'trace');add({will:-1});return '아이는"),
    ("addIntel(p,50,'trail');if(ch(.3)){W().queue.unshift(()=>battle(p,{ambushed:true}));return '들켰다.",
     "addIntel(p,50,'trace');if(ch(.3)){W().queue.unshift(()=>battle(p,{ambushed:true}));return '들켰다."),     # 역으로 미행
    ("addIntel(p,50,'trail');if(ch(.4)){add({health:-6});return '갑판에", "addIntel(p,50,'trace');if(ch(.4)){add({health:-6});return '갑판에"),
    ("addIntel(t,30,'trail'); t.fortDown=true;", "addIntel(t,30,'trace'); t.fortDown=true;"),                 # 결계의 흔적
    ("addIntel(t,12,'trail'); return '결계 바깥에", "addIntel(t,12,'trace'); return '결계 바깥에"),
    ("{p:t.i}); addIntel(t,10,'trail'); return `흔적의 크기와", "{p:t.i}); addIntel(t,10,'trace'); return `흔적의 크기와"),   # 격전지의 흔적
    ("addIntel(t,8,'trail'); return '흔적은 이미 식어", "addIntel(t,8,'trace'); return '흔적은 이미 식어"),
    ("addIntel(p,35,'trail'); return '마력의 실을", "addIntel(p,35,'trace'); return '마력의 실을"),           # 쓰러지는 시민들
    ("addIntel(p,45,'trail');return `탄피에", "addIntel(p,45,'trace');return `탄피에"),
    ("forEach(p=>addIntel(p,30));return '결계를 풀자", "forEach(p=>addIntel(p,30,'trace'));return '결계를 풀자"),   # 덫
    ("addIntel(t,22,'trail'); return '서번트가 까마귀를", "addIntel(t,22,'trace'); return '서번트가 까마귀를"),
    ("조가 드나든 흔적을 찾았다.`,'war'); addIntel(t,15,'trail');", "조가 드나든 흔적을 찾았다.`,'war'); addIntel(t,15,'trace');"),
    ("contracted().forEach(p=>addIntel(p,10,'trail'))", "contracted().forEach(p=>addIntel(p,10,'trace'))"),   # 지맥
    ("if(t) addIntel(t,25,'trail'); W().hp", "if(t) addIntel(t,25,'trace'); W().hp"),                         # 지붕 정찰(맡김)
    ("if(t) addIntel(t,15,'trail'); W().exposure", "if(t) addIntel(t,15,'trace'); W().exposure"),             # 지붕 정찰(함께)
    ("if(t) addIntel(t,35,'trail'); return '고양이의", "if(t) addIntel(t,35,'trace'); return '고양이의"),     # 사역마의 기억
    ("w.churchQuest=p.i; addIntel(p,Math.max(0,40-p.intel)+10,'trail')", "w.churchQuest=p.i; addIntel(p,Math.max(0,40-p.intel)+10,'trace')"),
    ("addIntel(t,30,'trail'); return '주소와", "addIntel(t,30,'trace'); return '주소와"),
    ("const doL=()=>{ const t=pick(unk); addIntel(t,Math.max(0,30-t.intel)+10,'trail');", "const doL=()=>{ const t=pick(unk); addIntel(t,Math.max(0,30-t.intel)+10,'trace');"),
    ("p.hp=clamp(p.hp-15); addIntel(p,20,'trail');", "p.hp=clamp(p.hp-15); addIntel(p,20,'trace');"),         # 함정
    ("e.hp=clamp(e.hp-dmg); addIntel(e,10,'trail');", "e.hp=clamp(e.hp-dmg); addIntel(e,10,'trace');"),         # 고지 저격
    ("e.provoked=2; addIntel(e,8,'trail');", "e.provoked=2; addIntel(e,8,'trace');"),
    ("e.noWs=w.day+(big?3:1); addIntel(e,15,'trail');", "e.noWs=w.day+(big?3:1); addIntel(e,15,'trace');"),     # 결계를 풀러 감
    ("e.mHurt=2; e.hp=clamp(e.hp-ri(5,12)); addIntel(e,20,'trail');", "e.mHurt=2; e.hp=clamp(e.hp-ri(5,12)); addIntel(e,20,'trace');"),   # 거처 폭파
]
WATCH = [
    ("addIntel(t,20,'trail'); addIntel(o,20,'trail');", "addIntel(t,20,'watch'); addIntel(o,20,'watch');"),   # 다른 조의 싸움
    ("addIntel(a,10,'trail');", "addIntel(a,10,'watch');"),                                                   # 밤의 질주 소리
    ("if(r==='great'||r==='ok'){ addIntel(p,20,'trail'); log(`${h.name}${J(h.name,이)} 명령을 떨쳐",
     "if(r==='great'||r==='ok'){ addIntel(p,20,'watch'); log(`${h.name}${J(h.name,이)} 명령을 떨쳐"),        # 령주 명령을 떨쳐 냄
    ("p.tac='hunter';addIntel(p,30);return '봉투를", "p.tac='hunter';addIntel(p,30,'watch');return '봉투를"),   # 결투장 무시
    ("w.exposure=clamp(w.exposure-12);addIntel(p,20);return '짐을", "w.exposure=clamp(w.exposure-12);addIntel(p,20,'watch');return '짐을"),
]
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("if(loc&&why!=='raid'&&(!t.wishKnown", "if(loc&&why!=='raid'&&why!=='trace'&&(!t.wishKnown")
    rp("why==='watch'||why==='raid'?'trail':why]", "why==='watch'||why==='raid'||why==='trace'?'trail':why]")
    for x in TRACE + WATCH: rp(*x)
    print('wishsrc miss', miss)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
