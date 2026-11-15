"""사람이 된 솔로몬 (11-15)
- 성배에 솔로몬의 소원(사람이 되는 것)을 빌면: 성배가 맑고 신뢰 60 이상이면 사람이 되어 곁에 남는다(수육처럼 에필로그를 함께). 모자라면 예전처럼 떠난다.
  소원 선택지 아래에 남는 조건과 지금 신뢰를 보여 준다.
- 에필로그에서 서번트의 힘으로 해결하던 선택지 11곳을 솔로몬의 재능(지혜 · 지식 · 의사 · 사람들의 신뢰)으로 바꾼다.
- 서번트의 힘이 드러나는 생활 사건 5개(쓸 일 없는 힘 · 무구 · 공방 · 대련 · 마술)는 나오지 않고, 재능 사건 6개를 새로 넣는다.
- 운동회 이어달리기 결과 · '좌' 대사(결혼 반지 · 노환 이별)를 사람에게 맞게.
- 서번트 카드: 「사람이 됨 · 함께 산 지 N년」.
사용: python3 solhuman_apply.py <game.html>"""
import sys, json, re, i18n

SOL = {  # 바뀌는 선택지 (한국어, 영어, 일본어)
 'hunt_t': ('솔로몬이 사냥꾼의 다음 밤을 짚는다', 'Solomon pins down the hunter\'s next night', 'ソロモンが狩人の次の夜を読む'),
 'hunt_d': ('반드시 피한다 · 사냥꾼은 도시를 떠난다', 'Certain to avoid him · the hunter leaves the city', '必ず避ける · 狩人は街を去る'),
 'hunt_r': ('솔로몬은 피해자 명단과 달력을 나란히 놓고 한참 보았다. “다음은 비 오는 목요일, 강 건너다.” 그날 밤 둘은 다른 동네 여관에 있었다. 사냥꾼은 빈집만 보고 도시를 떠났다.',
            'Solomon laid the list of victims beside the calendar and studied them for a long time. “Next is a rainy Thursday, across the river.” That night the two of you were at an inn in another neighborhood. The hunter found only an empty house and left the city.',
            'ソロモンは被害者の名簿と暦を並べて、長いこと眺めていた。「次は雨の木曜、川向こうだ」その夜、二人は別の町の宿にいた。狩人は空き家だけを見て、街を去った。'),
 'wit_t': ('솔로몬이 증인으로 나선다', 'Solomon steps forward as a witness', 'ソロモンが証人として名乗り出る'),
 'wit_d': ('심문이 쉬워진다', 'The interrogation becomes easier', '尋問が楽になる'),
 'wit_r': ('솔로몬은 사람이 된 뒤 받은 이름으로 증언했다. 그 겨울의 날짜를 하나도 틀리지 않았다. 대행자는 그 이름을 적고 고개를 갸웃했다.',
           'Solomon testified under the name he took after becoming human. He did not get a single date of that winter wrong. The Executor wrote the name down and tilted his head.',
           'ソロモンは人間になってから得た名前で証言した。あの冬の日付を一つも間違えなかった。代行者はその名を書き留め、首をかしげた。'),
 'def_t': ('솔로몬이 변론을 맡는다', 'Solomon takes up your defense', 'ソロモンが弁論を引き受ける'),
 'def_d': ('반드시 종결된다 · 교회와 척지지 않는다', 'Certain to be closed · no enmity with the Church', '必ず終結する · 教会と敵対しない'),
 'def_r': ('솔로몬은 그 겨울의 일을 처음부터 끝까지 말했다. 율법의 말로 묻고, 율법의 말로 답했다. 대행자는 한참 뒤 수첩을 덮었다. “…이런 변론은 처음 듣습니다. 이 건은 종결합니다.”',
           'Solomon recounted that winter from beginning to end. He asked in the words of the Law and answered in the words of the Law. After a long while, the Executor closed his notebook. “…I have never heard a defense like this. This matter is closed.”',
           'ソロモンはあの冬のことを最初から最後まで語った。律法の言葉で問い、律法の言葉で答えた。代行者はしばらくして手帳を閉じた。「…このような弁論は初めて聞きます。この件は終結とします」'),
 'chase_b': ('그 뒤로 몇 해마다 검은 옷의 사람들이 찾아왔다. 당신과 솔로몬은 도시를 옮겨 다니며 살았다. 이번에는 다섯 명이다.',
             'For years after that, the people in black kept coming. You and Solomon lived moving from city to city. This time there are five of them.',
             'それから数年ごとに、黒衣の者たちがやって来た。あなたとソロモンは街を転々として暮らした。今度は五人だ。'),
 'chase_t': ('솔로몬이 길을 짠다', 'Solomon plans the route', 'ソロモンが道筋を立てる'),
 'chase_d': ('반드시 따돌린다 · 재산 −8', 'Certain to shake them off · Wealth −8', '必ず振り切る · 財産 −8'),
 'chase_r': ('솔로몬은 지도 위에 길을 세 갈래 그렸다. 하나는 미끼, 하나는 쉬어 가는 길, 하나가 진짜였다. 검은 옷들은 미끼를 따라 바다까지 갔다. 그 뒤로 다시 오지 않았다.',
             'Solomon drew three routes on the map. One was a decoy, one a road to rest on, and one was real. The people in black followed the decoy all the way to the sea. They never came again.',
             'ソロモンは地図の上に道を三本引いた。一本は囮、一本は休むための道、一本が本物だった。黒衣の者たちは囮を追って海まで行った。それきり二度と来なかった。'),
 'exe_t': ('솔로몬이 협회와 담판한다', 'Solomon negotiates with the Association', 'ソロモンが協会と談判する'),
 'exe_d': ('반드시 물러간다 · 지식 −5', 'Certain to make him withdraw · Knowledge −5', '必ず引き下がらせる · 知識 −5'),
 'exe_r': ('솔로몬은 집행자를 식탁에 앉혔다. 차 한 잔이 식는 동안, 협회가 수백 년 풀지 못한 문제 하나의 답을 종이에 적어 건넸다. “이것과 바꾸지.” 집행자는 종이를 오래 들여다보다 일어섰다. 다시는 오지 않았다.',
           'Solomon sat the enforcer down at the table. In the time it took a cup of tea to cool, he wrote out on paper the answer to a problem the Association had failed to solve for centuries, and handed it over. “I\'ll trade you this.” The enforcer stared at the paper for a long time, then rose. He never came again.',
           'ソロモンは執行者を食卓に座らせた。茶が一杯冷める間に、協会が数百年解けなかった問題の答えを紙に書いて渡した。「これと引き換えだ」執行者は紙を長いこと見つめ、立ち上がった。二度と来なかった。'),
 'lab_t': ('솔로몬이 서류로 데리러 온다', 'Solomon comes for you with paperwork', 'ソロモンが書類で迎えに来る'),
 'lab_d': ('반드시 빠져나온다', 'Certain to get out', '必ず抜け出す'),
 'lab_r': ('사흘째 아침, 하얀 방의 문이 열렸다. 의사 가운 차림의 솔로몬이 이송 서류를 들고 서 있었다. 서명은 완벽했고, 아무도 의심하지 않았다. 그날부터 둘은 이름을 바꾸어 살았다.',
           'On the third morning, the door of the white room opened. Solomon stood there in a doctor\'s coat, holding transfer papers. The signatures were perfect, and no one suspected a thing. From that day on, the two of you lived under new names.',
           '三日目の朝、白い部屋の扉が開いた。医師の白衣を着たソロモンが移送書類を持って立っていた。署名は完璧で、誰も疑わなかった。その日から、二人は名を変えて暮らした。'),
 'ley_t': ('솔로몬이 대피 순서를 짠다', 'Solomon plans the evacuation', 'ソロモンが避難の順番を決める'),
 'ley_d': ('모두 대피한다 · 영맥은 운에 맡긴다', 'Everyone evacuates · the ley line is left to luck', '全員避難する · 霊脈は運次第'),
 'ley_r': ('솔로몬은 동네 지도를 한 번 보고 대피 순서를 정했다. 노인이 사는 집부터, 계단 없는 길로. 아무도 다치지 않았다.',
           'Solomon glanced at the neighborhood map once and set the order of evacuation. Houses with elderly residents first, by routes without stairs. No one was hurt.',
           'ソロモンは町内の地図を一度見て、避難の順番を決めた。老人の住む家から、階段のない道で。誰も怪我をしなかった。'),
 'mud_t': ('솔로몬이 옛 기록에서 방법을 찾는다', 'Solomon finds a way in old records', 'ソロモンが古い記録から方法を探す'),
 'mud_d': ('반드시 마른다 · 지식 +3', 'Certain to dry up · Knowledge +3', '必ず乾く · 知識 +3'),
 'mud_r': ('솔로몬은 도서관에서 사흘을 보냈다. 성배보다 오래된 문헌 속에 진흙을 말리는 방법이 있었다. 소금과 햇빛, 그리고 원한의 주인 이름을 불러 주는 일. 웅덩이는 일주일 만에 말랐다.',
           'Solomon spent three days in the library. In texts older than the Grail, there was a way to dry the mud. Salt and sunlight, and calling the names of those who held the grudges. The pool dried up within a week.',
           'ソロモンは図書館で三日を過ごした。聖杯より古い文献の中に、泥を乾かす方法があった。塩と陽の光、そして怨みの主の名を呼んでやること。水たまりは一週間で乾いた。'),
 'cup_t': ('솔로몬이 의식의 허점을 짚는다', 'Solomon points out the flaw in the ritual', 'ソロモンが儀式の隙を指摘する'),
 'cup_d': ('반드시 막는다', 'Certain to stop it', '必ず阻止する'),
 'cup_r': ('솔로몬은 의식진을 한 번 보더니 분필로 선 하나를 그었다. “이 각도면 잔이 차지 않는다.” 사흘 뒤 의식은 연기만 피우고 끝났다.',
           'Solomon took one look at the ritual circle and drew a single line in chalk. “At this angle, the cup won\'t fill.” Three days later, the ritual ended in nothing but smoke.',
           'ソロモンは儀式陣を一目見ると、チョークで線を一本引いた。「この角度なら杯は満ちない」三日後、儀式は煙を上げただけで終わった。'),
 'thief_t': ('솔로몬이 이웃을 깨운다', 'Solomon wakes the neighbors', 'ソロモンが隣人を起こす'),
 'thief_d': ('반드시 지켜 낸다', 'Certain to protect it', '必ず守り抜く'),
 'thief_r': ('솔로몬이 복도 불을 켜고 이웃집 문을 차례로 두드렸다. 동네 사람들이 하나둘 나왔다. 낯선 사람들은 그 많은 얼굴 앞에서 등을 돌렸다.',
             'Solomon switched on the hallway light and knocked on the neighbors\' doors one after another. People from the neighborhood came out one by one. Faced with so many faces, the strangers turned and left.',
             'ソロモンは廊下の明かりをつけ、隣家の扉を順に叩いた。町の人々が一人、また一人と出てきた。見知らぬ者たちは、その大勢の顔の前で背を向けた。'),
 'crest_t': ('솔로몬이 재판을 연다', 'Solomon holds a trial', 'ソロモンが裁きを開く'),
 'crest_d': ('반드시 되찾는다', 'Certain to get it back', '必ず取り戻す'),
 'crest_r': ('솔로몬은 친척의 공방에 혼자 들어갔다. 한 시간 뒤 각인을 담은 상자를 들고 나왔다. 무슨 이야기를 했느냐고 묻자, 공정한 재판을 했을 뿐이라고 했다.',
             'Solomon went into your relative\'s workshop alone. An hour later he came out carrying a box with the Crest inside. When you asked what he had said, he told you he had only held a fair trial.',
             'ソロモンは親戚の工房に一人で入っていった。一時間後、刻印の入った箱を持って出てきた。何を話したのかと尋ねると、公正な裁きをしただけだと言った。'),
 'run_r': ('숨이 턱까지 차서 들어왔다. 뒤에서 두 번째였다. 솔로몬은 순위표를 한참 들여다보며 웃었다. “사람의 다리로 뛴 기록이다.”',
           'He came in completely out of breath. Second to last. Solomon looked at the results board for a long time and smiled. “That\'s a record run on human legs.”',
           '息を切らしてゴールした。後ろから二番目だった。ソロモンは順位表を長いこと眺めて笑った。「人間の脚で走った記録だ」'),
 'stay_r': ('며칠 뒤 그는 이름을 바꾸었다. 떠나지는 않았다. “세상을 처음부터 다시 보려면, 같이 볼 사람이 있어야 한다.” 그날부터 현관에 신발이 한 켤레 늘었다.',
            'A few days later, he changed his name. He did not leave. “To see the world again from the beginning, I need someone to see it with.” From that day on, there was one more pair of shoes by the door.',
            '数日後、彼は名を変えた。去りはしなかった。「世界を一から見直すには、一緒に見る者が要る」その日から、玄関の靴が一足増えた。'),
}
D = [v for k, v in SOL.items()] + [
    ('곁에 남는 조건', 'To stay by your side', 'そばに残る条件'),
    ('성배가 맑을 때', 'If the Grail is clean', '聖杯が澄んでいるとき'),
    ('신뢰 60 이상', 'Trust 60+', '信頼60以上'),
    ('사람이 됨', 'Became human', '人間になった'),
    ('사람이 됨 · 지금은 곁에 없음', 'Became human · Not by your side now', '人間になった · 今はそばにいない'),
    ('사람이 됨 · 함께 살기 시작함', 'Became human · Just started living together', '人間になった · 共に暮らし始めた'),
]
T = [
    ('사람이 됨 · 함께 산 지 {0}일', 'Became human · {0} days together', '人間になった · 共に暮らして{0}日'),
    ('사람이 됨 · 함께 산 지 {0}달', 'Became human · {0} months together', '人間になった · 共に暮らして{0}か月'),
    ('사람이 됨 · 함께 산 지 {0}년', 'Became human · {0} years together', '人間になった · 共に暮らして{0}年'),
]

# 새 재능 사건 6개 (RLEP · EP2_EV)
NEW = [
 ('s_exam', 'B', {'pass': 'rel5', 'wait': 'will2'}, None,
  ('합격자 명단', 'The List of Names', '合格者名簿'),
  [('솔로몬이 의사 국가시험을 보겠다고 했다. 식탁은 몇 달째 두꺼운 책으로 덮여 있었다.',
    'Solomon said he would take the national medical exam. For months, the dining table was buried under thick books.',
    'ソロモンが医師国家試験を受けると言った。食卓は何か月も分厚い本で埋まっていた。'),
   ('새벽에 깨어 보니 거실 불이 켜져 있었다. 솔로몬이 해부학 책을 펴 놓고 혼자 중얼거리고 있었다.',
    'You woke before dawn to find the living room light on. Solomon had an anatomy book open and was muttering to himself.',
    '明け方に目を覚ますと、居間の明かりがついていた。ソロモンが解剖学の本を広げて、一人でつぶやいていた。'),
   ('“미리 알 수 없는 시험은 처음이다.” 솔로몬은 그 말을 하며 이상하게 즐거워 보였다.',
    '“It\'s my first exam I can\'t know in advance.” Saying so, Solomon looked strangely happy.',
    '「先がわからない試験は初めてだ」そう言うソロモンは、妙に楽しそうだった。')],
  [('pass', ('발표 날 명단을 같이 찾는다', 'Search the list together on announcement day', '発表の日、一緒に名簿を探す'),
    [('화면 속 명단을 위에서부터 같이 읽어 내려갔다. 새 이름이 거기 있었다. 솔로몬은 한참 그 글자를 손가락으로 짚고 있었다.',
      'You read down the list on the screen together from the top. The new name was there. Solomon kept his finger on those letters for a long time.',
      '画面の名簿を上から一緒に読んでいった。新しい名前がそこにあった。ソロモンはしばらくその文字を指でなぞっていた。'),
     ('“붙었다.” 짧게 말하고 그는 창밖을 보았다. “반지 없이 얻은 것 중에 이게 처음이다.”',
      '“I passed.” He said it briefly and looked out the window. “This is the first thing I\'ve earned without the rings.”',
      '「受かった」短く言って、彼は窓の外を見た。「指輪なしで得たものは、これが初めてだ」')]),
   ('wait', ('결과는 혼자 보게 둔다', 'Let him see the results alone', '結果は一人で見させる'),
    [('저녁에 돌아온 솔로몬의 손에 꽃 한 다발이 들려 있었다. 결과는 묻지 않아도 알 수 있었다.',
      'Solomon came home that evening holding a bouquet of flowers. You didn\'t need to ask about the results.',
      '夕方に帰ってきたソロモンの手には花束があった。結果は聞かなくてもわかった。'),
     ('“먼저 알게 해서 미안하다. 다음부터는 같이 보자.” 솔로몬은 그렇게 말하고 쑥스럽게 웃었다.',
      '“Sorry I found out first. Next time, let\'s look together.” Solomon said, smiling sheepishly.',
      '「先に知ってしまってすまない。次からは一緒に見よう」ソロモンはそう言って照れくさそうに笑った。')])]),
 ('s_clinic', 'C', {'listen': 'rel5', 'tea': 'bond2'}, 's_exam',
  ('첫 진료', 'The First Patient', '初めての診察'),
  [('수련의가 된 솔로몬이 첫 환자를 본 날이었다. 저녁 내내 그 이야기만 했다.',
    'It was the day Solomon, now a resident, saw his first patient. He talked about nothing else all evening.',
    '研修医になったソロモンが初めて患者を診た日だった。夜の間ずっとその話ばかりしていた。'),
   ('“앞날이 보이지 않으니, 지금 보이는 것을 전부 봐야 한다.” 솔로몬의 진료는 다른 의사들보다 늘 오래 걸린다고 했다.',
    '“Since I can\'t see the future, I have to see everything that\'s in front of me.” They said Solomon\'s examinations always took longer than the other doctors\'.',
    '「先が見えないからこそ、今見えるものを全部見なければならない」ソロモンの診察は他の医師よりいつも長いと言われていた。')],
  [('listen', ('끝까지 이야기를 들어 준다', 'Listen to the whole story', '最後まで話を聞く'),
    [('첫 환자는 기침이 오래 낫지 않는 할머니였다. 솔로몬은 그 기침 소리를 흉내 내며 무엇을 들었는지 하나하나 설명했다. 당신은 끝까지 들었다.',
      'His first patient was an old woman whose cough wouldn\'t go away. Solomon imitated the cough and explained, one by one, everything he had heard. You listened to the very end.',
      '最初の患者は咳が長く治らないお婆さんだった。ソロモンはその咳の音を真似て、何を聞いたのかを一つずつ説明した。あなたは最後まで聞いた。')]),
   ('tea', ('따뜻한 차를 내준다', 'Make him a warm cup of tea', '温かいお茶を出す'),
    [('찻잔을 받은 솔로몬이 그제야 손을 떨었다. “사람을 고치는 건 왕국을 다스리는 것보다 무섭군.”',
      'Only when he took the cup did Solomon\'s hands start to shake. “Healing a person is more frightening than ruling a kingdom.”',
      '湯呑みを受け取ったソロモンは、そこで初めて手を震わせた。「人を治すのは、王国を治めるより恐ろしいな」')])]),
 ('s_judge', 'B', {'watch': 'will2', 'proud': 'rel5'}, None,
  ('골목의 재판관', 'The Judge of the Alley', '路地の裁き手'),
  [('아랫집과 윗집이 주차 자리를 두고 몇 달째 다투고 있었다. 솔로몬이 둘을 놀이터 벤치에 앉혔다.',
    'The downstairs and upstairs neighbors had been fighting over a parking space for months. Solomon sat them both down on a playground bench.',
    '下の家と上の家が駐車場所をめぐって何か月も揉めていた。ソロモンが二人を公園のベンチに座らせた。'),
   ('동네 할머니 둘이 텃밭 경계를 두고 언성을 높였다. 지나가던 솔로몬이 걸음을 멈췄다.',
    'Two old women in the neighborhood raised their voices over the boundary of a vegetable patch. Solomon, passing by, stopped in his tracks.',
    '町内のお婆さん二人が菜園の境界をめぐって声を荒げていた。通りかかったソロモンが足を止めた。')],
  [('watch', ('멀리서 지켜본다', 'Watch from a distance', '遠くから見守る'),
    [('한 시간 뒤, 둘은 악수를 하고 헤어졌다. 솔로몬은 아무것도 나눠 주지 않았다. 다만 둘 다 자기가 이겼다고 생각했다.',
      'An hour later, the two shook hands and parted. Solomon hadn\'t divided anything. Yet both of them believed they had won.',
      '一時間後、二人は握手をして別れた。ソロモンは何も分け与えなかった。ただ、二人とも自分が勝ったと思っていた。')]),
   ('proud', ('그 뒤로 찾아오는 사람들을 맞는다', 'Welcome the people who start coming by', 'その後訪ねてくる人々を迎える'),
    [('그 뒤로 저녁마다 누군가 초인종을 눌렀다. 상의할 일이 있다는 사람들이었다. 솔로몬은 차를 내놓고 끝까지 들었다. 판결은 늘 짧았다.',
      'After that, someone rang the doorbell every evening. People with something to talk over. Solomon served tea and listened to the end. His verdicts were always short.',
      'それからは毎晩、誰かが呼び鈴を鳴らした。相談事があるという人たちだった。ソロモンは茶を出して最後まで聞いた。裁きはいつも短かった。')])]),
 ('s_names', 'A', {'quiz': 'rel4', 'walk': 'bond2'}, None,
  ('나무와 짐승의 이름', 'The Names of Trees and Beasts', '木と獣の名'),
  [('식물원에 갔다. 솔로몬은 팻말을 보기도 전에 나무 이름을 먼저 말했다. 백향목 앞에서는 오래 서 있었다.',
    'You went to the botanical garden. Solomon named each tree before he even looked at the sign. He stood a long time in front of the cedar.',
    '植物園に行った。ソロモンは札を見る前に木の名を口にした。レバノン杉の前では長いこと立ち止まっていた。'),
   ('동물원에 갔다. 솔로몬은 우리마다 멈춰 서서 그 짐승이 무엇을 먹고 어디서 자는지 설명했다. 사육사가 놀란 얼굴로 돌아보았다.',
    'You went to the zoo. Solomon stopped at every enclosure and explained what each animal ate and where it slept. A keeper turned around, astonished.',
    '動物園に行った。ソロモンは檻ごとに立ち止まり、その獣が何を食べ、どこで眠るのかを説明した。飼育員が驚いた顔で振り返った。')],
  [('quiz', ('하나씩 맞혀 보라고 한다', 'Ask him to name them one by one', '一つずつ当ててみろと言う'),
    [('“예전에는 반지가 가르쳐 주었다. 이번엔 책에서 배웠다.” 하나도 틀리지 않았다. 마지막 하나만 일부러 틀린 것 같았다.',
      '“Once, the rings taught me. This time, I learned from books.” He didn\'t get a single one wrong. Only the last one, he seemed to miss on purpose.',
      '「昔は指輪が教えてくれた。今度は本で学んだ」一つも間違えなかった。最後の一つだけ、わざと間違えたようだった。')]),
   ('walk', ('천천히 같이 걷는다', 'Walk slowly together', 'ゆっくり一緒に歩く'),
    [('솔로몬은 모르는 새 한 마리를 보고 처음으로 고개를 저었다. “모르는 게 남아 있어서 다행이다.” 둘은 그 새 이름을 집에 와서 같이 찾았다.',
      'At the sight of a bird he didn\'t know, Solomon shook his head for the first time. “I\'m glad there\'s still something I don\'t know.” The two of you looked up its name together back home.',
      'ソロモンは知らない鳥を一羽見て、初めて首を横に振った。「知らないものが残っていてよかった」二人はその鳥の名を家に帰って一緒に調べた。')])]),
 ('s_lang', 'B', {'help': 'bond2', 'learn': 'rel5'}, None,
  ('세 번째 언어', 'A Third Language', '三つ目の言葉'),
  [('솔로몬이 몇 달 만에 새 언어를 하나 더 익혔다. 이주민 상담소에서 통역 봉사를 하겠다고 했다.',
    'Within a few months, Solomon had picked up yet another language. He said he would volunteer as an interpreter at the immigrant counseling center.',
    'ソロモンが数か月で新しい言葉をもう一つ覚えた。移住者相談所で通訳のボランティアをすると言った。'),
   ('시장에서 길을 잃은 외국인 가족을 만났다. 솔로몬이 그들의 말로 말을 걸자, 아이가 울음을 그쳤다.',
    'At the market, you met a foreign family who had lost their way. When Solomon spoke to them in their own language, the child stopped crying.',
    '市場で道に迷った外国人の家族に出会った。ソロモンが彼らの言葉で話しかけると、子どもが泣きやんだ。')],
  [('help', ('같이 따라나선다', 'Go along with him', '一緒についていく'),
    [('상담소의 긴 줄이 솔로몬 앞에서 조금씩 줄었다. 당신은 서류를 나르고 물을 따랐다. 돌아오는 길에 그가 말했다. “말이 통한다는 건 이렇게 큰일이었군.”',
      'The long line at the center shrank, little by little, in front of Solomon. You carried papers and poured water. On the way home he said, “So being understood is this big a thing.”',
      '相談所の長い列が、ソロモンの前で少しずつ短くなった。あなたは書類を運び、水を注いだ。帰り道に彼が言った。「言葉が通じるというのは、これほど大きなことだったのだな」')]),
   ('learn', ('당신에게도 가르쳐 달라고 한다', 'Ask him to teach you too', 'あなたにも教えてほしいと頼む'),
    [('솔로몬은 생각보다 엄한 선생이었다. 대신 당신이 한 문장을 맞힐 때마다 자기 일처럼 기뻐했다.',
      'Solomon turned out to be a stricter teacher than you expected. But every time you got a sentence right, he was as happy as if it were his own.',
      'ソロモンは思ったより厳しい先生だった。その代わり、あなたが一文正しく言えるたびに、自分のことのように喜んだ。')])]),
 ('s_shelter', 'C', {'build': 'rel5', 'sit': 'will2'}, None,
  ('작은 쉼터', 'A Small Shelter', '小さな東屋'),
  [('동네 놀이터 옆에 정자를 새로 짓는다고 했다. 설계를 맡을 사람이 없다는 말에 솔로몬이 손을 들었다.',
    'They were going to build a new pavilion by the neighborhood playground. When no one could be found to design it, Solomon raised his hand.',
    '町内の公園の横に東屋を新しく建てるという。設計する人がいないと聞いて、ソロモンが手を挙げた。'),
   ('식탁 위에 정자 도면이 펼쳐져 있었다. 기둥이 일곱 개였다. “성전보다는 작지만, 누구든 쉬어 갈 수 있다.”',
    'The pavilion\'s plans were spread across the dining table. Seven pillars. “It\'s smaller than a temple, but anyone can rest here.”',
    '食卓の上に東屋の図面が広げてあった。柱は七本。「神殿よりは小さいが、誰でも休んでいける」')],
  [('build', ('공사를 같이 돕는다', 'Help with the construction', '工事を一緒に手伝う'),
    [('주말마다 둘이 나무를 날랐다. 완성된 날, 동네 아이들이 먼저 올라가 뛰었다. 솔로몬은 그 소리를 오래 듣고 있었다.',
      'Every weekend the two of you hauled wood. On the day it was finished, the neighborhood kids ran up into it first. Solomon listened to their noise for a long time.',
      '毎週末、二人で木材を運んだ。完成した日、町の子どもたちが真っ先に上がって駆け回った。ソロモンはその声を長いこと聞いていた。')]),
   ('sit', ('완성되면 같이 앉아 본다', 'Sit there together once it\'s done', '完成したら一緒に座ってみる'),
    [('저녁 무렵 둘이 정자에 앉았다. 바람이 기둥 사이로 지나갔다. “왕궁 창문보다 여기가 더 넓게 보인다.”',
      'Toward evening, the two of you sat in the pavilion. The wind passed between the pillars. “From here, the world looks wider than from the palace window.”',
      '夕暮れどき、二人は東屋に腰を下ろした。風が柱の間を抜けていった。「王宮の窓より、ここのほうが広く見える」')])]),
]

for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    k = lambda key: SOL[key][0].replace("'", "\\'")
    def choice(t, d, body, auto='true', pre=''):
        return "{t:'%s',d:'%s',auto:%s,f:()=>{ %s }}" % (k(t), k(d), auto, body)
    # 판정 함수
    rp("  const stayHome=()=>!!S.flags.stay&&!S.flags.stayAway&&!S.flags.stayDied&&!!S.hero;",
       "  const stayHome=()=>!!S.flags.stay&&!S.flags.stayAway&&!S.flags.stayDied&&!!S.hero;\n"
       "  const solH=()=>!!S.flags.solomonHuman&&S.hero==='solomon'&&stayHome();   // 사람이 되어 곁에 남은 솔로몬: 서번트의 힘 대신 재능으로")
    # 소원: 맑은 성배 · 신뢰 60 이상이면 곁에 남는다
    rp("log('며칠 뒤 그는 이름을 바꾸고 도시를 떠났다. 몇 해 뒤, 의사 국가시험 합격자 명단에서 낯선 이름을 하나 보았다. 이유는 모르지만, 그 사람이라는 걸 알았다.','joy');\n      add({bond:8,will:4}); S.flags.solomonHuman=1; sharedOut(shared); warOver(); return; }",
       "if(w.trust>=STAY_NEED){ log('" + k('stay_r') + "','joy'); add({bond:10,will:4}); S.flags.solomonHuman=1; S.flags.stay=h.id; S.flags.endFx='stay'; sharedOut(shared); warOver(); return; }\n"
       "      log('며칠 뒤 그는 이름을 바꾸고 도시를 떠났다. 몇 해 뒤, 의사 국가시험 합격자 명단에서 낯선 이름을 하나 보았다. 이유는 모르지만, 그 사람이라는 걸 알았다.','joy');\n      add({bond:8,will:4}); S.flags.solomonHuman=1; sharedOut(shared); warOver(); return; }")
    rp("ch_.push({t:`${h.name}의 소원을 빈다`,d:`“${h.wish}”`,",
       "ch_.push({t:`${h.name}의 소원을 빈다`,d:`“${h.wish}”`,...(h.id==='solomon'?{foot:[['곁에 남는 조건',['성배가 맑을 때','신뢰 60 이상']],['현재',[`신뢰 ${Math.round(w.trust)}`]]]}:{}),")
    # 에필로그 연작: 서번트의 힘 → 솔로몬의 재능
    def swap(anchor, new_choice, cond_old):
        rp(anchor, "...(solH()?[" + new_choice + "]:[])," + anchor.replace(cond_old, cond_old + "&&!solH()", 1))
    swap("...(stayHome()?[{t:nf('{N이} 막아선다',H_BY[S.hero])", choice('hunt_t', 'hunt_d', "add({bond:5,will:2}); arcEnd(); return '%s';" % k('hunt_r')), "stayHome()")
    swap("...(sv?[{t:nf('{N을} 숨긴다',H_BY[S.hero])", choice('wit_t', 'wit_d', "p.proof=1; add({bond:2}); arcSet(1); return '%s';" % k('wit_r'), 'false'), "sv")
    rp("pen=sv&&!p.svHid?20:0;", "pen=sv&&!p.svHid&&!solH()?20:0;")
    swap("...(sv?[{t:nf('{N이} 나선다',H_BY[S.hero])", choice('def_t', 'def_d', "add({will:4,bond:3}); return ok('%s');" % k('def_r')), "sv")
    rp("      decide({title:'검은 옷의 추격',",
       "      if(solH()){ decide({title:'검은 옷의 추격',body:'" + k('chase_b') + "',choices:[" + choice('chase_t', 'chase_d', "arcEnd(); add({wealth:-8,bond:4}); return '%s';" % k('chase_r')) +
       ",{t:'더 멀리 떠난다',d:'재산 −15',f:()=>{ arcEnd(); add({wealth:-15,bond:3}); return '바다를 건넜다. 새 도시에서는 아무도 검은 옷을 입지 않았다.'; }}]}); return; }\n"
       "      decide({title:'검은 옷의 추격',")
    swap("...(sv?[{t:nf('{N이} 막는다',H_BY[S.hero])", choice('exe_t', 'exe_d', "add({lore:-5,bond:4}); arcEnd(); return '%s';" % k('exe_r')), "sv")
    swap("...(stayHome()?[{t:nf('{N이} 문을 부순다',h)", choice('lab_t', 'lab_d', "add({bond:5}); return out('%s');" % k('lab_r')), "stayHome()")
    swap("...(sv?[{t:nf('{N이} 영맥을 받아 낸다',H_BY[S.hero])", choice('ley_t', 'ley_d', "add({bond:3}); log('%s','war'); return fin(true,ch(p.drain?.6:.25),false);" % k('ley_r')), "sv")
    swap("...(sv?[{t:nf('{N이} 진흙을 받아 낸다',H_BY[S.hero])", choice('mud_t', 'mud_d', "arcEnd(); add({lore:3,bond:3}); S.flags.mudDry=1; return '%s';" % k('mud_r')), "sv")
    swap("...(sv?[{t:nf('{N과} 함께 간다',H_BY[S.hero])", choice('cup_t', 'cup_d', "arcEnd(); add({bond:3,will:5}); S.flags.shardBroke=1; return '%s';" % k('cup_r'), '!p.own'), "sv")
    swap("...(sv?[{t:nf('{N이} 지킨다',H_BY[S.hero])", choice('thief_t', 'thief_d', "add({bond:4}); arcEnd(); return '%s';" % k('thief_r')), "sv")
    swap("...(sv?[{t:nf('{N과} 함께 되찾으러 간다',H_BY[S.hero])", choice('crest_t', 'crest_d', "arcEnd(); add({mana:25,bond:3}); delete S.flags.crestLost; return '%s';" % k('crest_r'), 'false'), "sv")
    # 생활 사건: 서번트의 힘이 드러나는 5개는 빼고, 재능 사건은 사람이 된 솔로몬에게만
    rp("    if(e.ph!==E.ph||(E.relUsed||[]).includes(e.id)) return false;",
       "    if(e.ph!==E.ph||(E.relUsed||[]).includes(e.id)) return false;\n"
       "    if(e.sol?!solH():solH()&&['b_fade','a_arms','a_shop_m','c_spar','c_spell'].includes(e.id)) return false; if(e.after&&!(E.relUsed||[]).includes(e.after)) return false;")
    rp("return '일등이었다. 2등과의 차이가 너무 커서 아무도 박수를 치지 못했다.'",
       "return solH()?'" + k('run_r') + "':'일등이었다. 2등과의 차이가 너무 커서 아무도 박수를 치지 못했다.'")
    # '좌'로 돌아가는 것을 전제한 줄은 사람이 된 솔로몬에게서 뺀다
    rp("    let B=o.b||(m&&E.bm?E.bm:E.b);",
       "    const solF=a=>{ if(!solH()||!Array.isArray(a)) return a; const f=a.filter(x=>!/좌에|좌로|좌에서/.test(JSON.stringify(x))); return f.length?f:a; };\n"
       "    let B=solF(o.b||(m&&E.bm?E.bm:E.b));")
    rp("const R=(o.r&&o.r[c.key])||c.r;", "const R=solF((o.r&&o.r[c.key])||c.r);")
    rp("pick(REL_OLD[k])", "pick(solH()?REL_OLD[k].filter(x=>!/좌에/.test(x[0])):REL_OLD[k])", 2)
    # 서번트 카드
    rp("swapped:!!r.swapped,", "swapped:!!r.swapped,human:!!S.flags.solomonHuman&&S.hero==='solomon',")
    rp("const sub=v.died?", "let sub=v.died?")
    rp(":'수육 · 함께 살기 시작함';", ":'수육 · 함께 살기 시작함'; if(v.human) sub=sub.replace(/^수육 · /,'사람이 됨 · ');")
    # 새 사건
    i = s.index('EP2_EV='); E, end = json.JSONDecoder().raw_decode(s[i + 7:])
    for sid, ph, fx, after, *_ in NEW:
        e = {'id': sid, 'ph': ph, 'fx': fx, 'love': [], 'sol': 1}
        if after: e['after'] = after
        E.append(e)
    s = s[:i + 7] + json.dumps(E, ensure_ascii=False) + s[i + 7 + end:]
    add = {}
    for sid, ph, fx, after, t, bs, cs in NEW:
        add[sid] = {'t': t[0], 'b': [[b[0]] for b in bs], 'c': [{'key': ck, 't': ct[0], 'r': [[r[0]] for r in rs]} for ck, ct, rs in cs]}
        D.append(t); D.extend(bs)
        for ck, ct, rs in cs: D.append(ct); D.extend(rs)
    rp("Object.assign(RLEP,{\"a_clothes\":", "Object.assign(RLEP," + json.dumps(add, ensure_ascii=False) + ");\n  Object.assign(RLEP,{\"a_clothes\":")
    # 영어 · 일본어: 따옴표 대사가 섞인 문장은 대사만 따로도 넣는다
    extra = []
    for ko, en, ja in D:
        mk, me, mj = re.findall(r'“([^”]*)”', ko), re.findall(r'“([^”]*)”', en), re.findall(r'「([^」]*)」', ja)
        if mk and len(mk) == len(me) == len(mj):
            extra += list(zip(mk, me, mj))
    s, nd, nt = i18n.add(s, D + extra, T)
    print('solhuman miss', miss, 'tr', nd, nt)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
