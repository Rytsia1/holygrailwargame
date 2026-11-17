"""11-17: 패치 노트 2.01 「UI 스타일 개선 및 인연관계 개선」 (영 · 일 · 중 번역)
사용: python3 patch201_apply.py <game.html>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if "n:'2.01'" in s: print('이미 적용됨'); sys.exit(0)

TITLE = 'UI 스타일 개선 및 인연관계 개선'
# (한국어, 영어, 일본어, 간체, 번체)
T = {
 'title': (TITLE, 'UI Style and Bond Improvements', 'UIスタイルと絆の改善', 'UI风格与羁绊关系改进', 'UI風格與羈絆關係改進'),
 'g1': ('로비와 화면', 'Lobby and Screens', 'ロビーと画面', '大厅与画面', '大廳與畫面'),
 'a1': ('시작 화면이 두 단계로 변경됩니다.', 'The start screen now has two stages.', 'スタート画面が二段階に変更されます。', '开始画面改为两个阶段。', '開始畫面改為兩個階段。'),
 'a1a': ('배경과 제목 화면에서 누르면 시작 버튼 등이 나옵니다.', 'Tap the background-and-title screen to bring up the start buttons and more.', '背景とタイトルの画面を押すと、スタートボタンなどが表示されます。', '在背景与标题画面点击后，会出现开始按钮等。', '在背景與標題畫面點擊後，會出現開始按鈕等。'),
 'a2': ('로비와 게임 전체의 UI 스타일이 변경됩니다.', 'The UI style of the lobby and the whole game has been changed.', 'ロビーとゲーム全体のUIスタイルが変更されます。', '大厅与整个游戏的UI风格已更改。', '大廳與整個遊戲的UI風格已更改。'),
 'a3': ('언어 선택이 로비 위쪽 단추 하나로 합쳐지고, 누르면 언어 창이 열리게 변경됩니다.', 'Language selection is now a single button at the top of the lobby that opens a language window.', '言語選択がロビー上部のボタン一つにまとまり、押すと言語ウィンドウが開くように変更されます。', '语言选择合并为大厅上方的一个按钮，点击后会打开语言窗口。', '語言選擇合併為大廳上方的一個按鈕，點擊後會開啟語言視窗。'),
 'a4': ('도움말이 항목마다 금색 소제목과 한 문장씩 나눈 목록으로 개선되었습니다.', 'Help now has gold subheadings for each topic and lists split into single sentences.', 'ヘルプが項目ごとに金色の小見出しと一文ずつの箇条書きに改善されました。', '帮助改为每个条目带金色小标题，并按句分成列表。', '說明改為每個條目帶金色小標題，並按句分成列表。'),
 'g2': ('사운드', 'Sound', 'サウンド', '声音', '聲音'),
 'b1': ('로비 배경음악 5곡이 추가됩니다. 로비에 들어올 때마다 바로 앞 곡을 빼고 한 곡이 무작위로 재생됩니다.', 'Five lobby BGM tracks have been added. Each time you enter the lobby, one plays at random, never the same as the last.', 'ロビーのBGMが5曲追加されます。ロビーに入るたびに、直前の曲を除いた一曲がランダムに流れます。', '新增5首大厅背景音乐。每次进入大厅时，会从中随机播放一首（不会与上一首重复）。', '新增5首大廳背景音樂。每次進入大廳時，會從中隨機播放一首（不會與上一首重複）。'),
 'g3': ('서번트와의 인연', 'Bonds with Your Servant', 'サーヴァントとの絆', '与从者的羁绊', '與從者的羈絆'),
 'c1': ('인연 1단계 「처음 부른 이름」에서 애정과 우정 중 하나를 고를 수 있습니다.', 'At bond stage 1, “The First Time They Said Your Name,” you can now choose between affection and friendship.', '絆の第1段階「初めて呼んだ名前」で、愛情と友情のどちらかを選べます。', '在羁绊第1阶段「第一次叫出的名字」中，可以在爱情与友情之间选择。', '在羈絆第1階段「第一次叫出的名字」中，可以在愛情與友情之間選擇。'),
 'c1a': ('성별과 관계없이 고를 수 있습니다.', 'You can choose regardless of gender.', '性別に関係なく選べます。', '与性别无关，都可以选择。', '與性別無關，都可以選擇。'),
 'c1b': ('미성년, 배우자가 있는 경우, 우정으로만 이어지는 서번트는 이전처럼 우정 루트로 진행됩니다.', 'Minors, Masters with a spouse, and friendship-only Servants still follow the friendship route as before.', '未成年、配偶者がいる場合、友情のみで結ばれるサーヴァントは、これまで通り友情ルートで進みます。', '未成年、已有配偶，以及只能发展友情的从者，仍会像以前一样走友情路线。', '未成年、已有配偶，以及只能發展友情的從者，仍會像以前一樣走友情路線。'),
 'c2': ('멀린, 솔로몬, 시바의 여왕, 엘키두와도 연인이 될 수 있습니다. 관련 애정 대사가 추가됩니다.', 'Merlin, Solomon, the Queen of Sheba, and Enkidu can now become your lover. New affection lines have been added for them.', 'マーリン、ソロモン、シバの女王、エルキドゥとも恋人になれます。関連する愛情台詞が追加されます。', '现在也可以与梅林、所罗门、示巴女王、恩奇都成为恋人。新增了相关的爱情台词。', '現在也可以與梅林、所羅門、示巴女王、恩奇都成為戀人。新增了相關的愛情台詞。'),
 'c3': ('사랑이나 곁에 있는 것이 소원인 서번트와 연인이 된 뒤 맑은 성배에 그 서번트의 소원을 빌었을 때의 결말이 변경됩니다.', 'The ending has changed for when you become lovers with a Servant whose wish is love or to stay by someone’s side, then wish their wish upon a pure Grail.', '愛や誰かのそばにいることを願うサーヴァントと恋人になった後、清らかな聖杯にそのサーヴァントの願いを託したときの結末が変更されます。', '与愿望是爱情或陪伴在身边的从者成为恋人后，向纯净的圣杯许下该从者的愿望时，结局有所改变。', '與願望是愛情或陪伴在身邊的從者成為戀人後，向純淨的聖杯許下該從者的願望時，結局有所改變。'),
 'c4': ('솔로몬의 소원을 이뤘을 때, 신뢰가 60 이상이면 솔로몬이 곁에 남도록 변경됩니다.', 'When you grant Solomon’s wish, he now stays by your side if Trust is 60 or higher.', 'ソロモンの願いを叶えたとき、信頼が60以上ならソロモンがそばに残るように変更されます。', '实现所罗门的愿望时，若信赖在60以上，所罗门会留在你身边。', '實現所羅門的願望時，若信賴在60以上，所羅門會留在你身邊。'),
 'c4a': ("에필로그에서 '서번트의 힘' 대신 '재능' 선택지와 사건이 등장합니다.", 'In the epilogue, “talent” choices and events appear instead of “Servant power.”', 'エピローグでは「サーヴァントの力」の代わりに「才能」の選択肢とイベントが登場します。', '尾声中会出现「才能」选项与事件，取代「从者之力」。', '尾聲中會出現「才能」選項與事件，取代「從者之力」。'),
 'c5': ('일부 서번트의 성별이 변경됩니다.', 'Some Servants’ genders have been changed.', '一部のサーヴァントの性別が変更されます。', '部分从者的性别有所更改。', '部分從者的性別有所更改。'),
 'c5a': ('프랑수아 프렐라티: 남성', 'François Prelati: male', 'フランソワ・プレラーティ：男性', '弗朗索瓦·普勒拉蒂：男性', '弗朗索瓦·普勒拉蒂：男性'),
 'c5b': ('타이라노 카게키요: 여성', 'Taira no Kagekiyo: female', '平景清：女性', '平景清：女性', '平景清：女性'),
 'g4': ('서번트 도감', 'Servant Codex', 'サーヴァント図鑑', '从者图鉴', '從者圖鑑'),
 'd1': ('계약한 서번트의 상세에 성유물이 표시됩니다.', 'Details of contracted Servants now show their relic.', '契約したサーヴァントの詳細に聖遺物が表示されます。', '已契约从者的详情中会显示圣遗物。', '已契約從者的詳情中會顯示聖遺物。'),
 'd2': ('손에 넣은 적이 있는 성유물이라면, 그 주인을 아직 만나지 못했어도 ??? 칸에 「‘성유물’의 주인」으로 표시됩니다.', 'If you have ever held a relic, its owner’s ??? slot shows “Owner of ‘relic’” even before you meet them.', '手に入れたことのある聖遺物なら、その持ち主にまだ出会っていなくても、??? 欄に「『聖遺物』の持ち主」と表示されます。', '只要曾经拿到过某件圣遗物，即使还没遇到它的主人，??? 栏也会显示为「“圣遗物”的主人」。', '只要曾經拿到過某件聖遺物，即使還沒遇到它的主人，??? 欄也會顯示為「「聖遺物」的主人」。'),
 'd2a': ('이번 업데이트 뒤 손에 넣은 성유물부터 기록됩니다.', 'Only relics obtained after this update are recorded.', 'このアップデート以降に手に入れた聖遺物から記録されます。', '从本次更新后拿到的圣遗物开始记录。', '從本次更新後拿到的聖遺物開始記錄。'),
 'g5': ('성배전쟁', 'Holy Grail War', '聖杯戦争', '圣杯战争', '聖杯戰爭'),
 'e1': ('상대 마스터의 소원은 직접 만나거나 전해 들었을 때만 알 수 있게 변경됩니다.', 'You can now learn an enemy Master’s wish only by meeting them or hearing it from someone.', '相手マスターの願いは、直接会うか伝え聞いたときにだけ分かるように変更されます。', '现在只有亲自见面或从他人处听说时，才能得知对方御主的愿望。', '現在只有親自見面或從他人處聽說時，才能得知對方御主的願望。'),
 'e1a': ('정찰, 미행, 흔적, 저격·암습을 막아 낸 단서로는 거처까지만 드러납니다.', 'Scouting, tailing, traces, and clues from fending off snipes and ambushes reveal only their base.', '偵察、尾行、痕跡、狙撃・暗襲を防いだ手がかりでは、拠点までしか分かりません。', '侦察、跟踪、痕迹，以及挡下狙击·暗袭得到的线索，只能查出据点。', '偵察、跟蹤、痕跡，以及擋下狙擊·暗襲得到的線索，只能查出據點。'),
 'e2': ('마스터의 오드가 전투마다가 아니라 하루 단위로 회복하도록 변경됩니다.', 'A Master’s Od now recovers once per day instead of after every battle.', 'マスターのオドが、戦闘ごとではなく一日単位で回復するように変更されます。', '御主的小源改为按天恢复，而不是每场战斗恢复。', '御主的小源改為按天恢復，而不是每場戰鬥恢復。'),
 'e3': ('최후의 결전은 대화로 멈출 수 없게 변경됩니다.', 'The final battle can no longer be stopped by talking.', '最後の決戦は、対話で止められないように変更されます。', '最后的决战无法再通过对话停止。', '最後的決戰無法再透過對話停止。'),
 'e4': ('검은 성배나 비스트가 강림한 뒤, 다른 조들이 보스와 싸우러 갈 확률이 증가하며, 최종일이 가까울수록 더 자주 가게끔 변경됩니다.', 'After the Black Grail or the Beast descends, other teams are more likely to go fight the boss, and go more often as the final day nears.', '黒い聖杯やビーストが降臨した後、他の陣営がボスと戦いに行く確率が上がり、最終日が近いほど頻繁に向かうように変更されます。', '黑色圣杯或Beast降临后，其他组前去与首领战斗的概率提高，越接近最后一天越常前往。', '黑色聖杯或Beast降臨後，其他組前去與首領戰鬥的機率提高，越接近最後一天越常前往。'),
 'g6': ('후반 위기 · 비스트 Ⅲ/R', 'Late-war Crisis · Beast III/R', '後半の危機・ビーストIII/R', '后半危机 · Beast Ⅲ/R', '後半危機 · Beast Ⅲ/R'),
 'f1': ('범위 보구가 키아라 곁의 호위 센티넬까지 휩쓸 수 있습니다. 확률은 보구의 범위에 따라 차이가 있습니다.', 'Area Noble Phantasms can now sweep up the Sentinels guarding Kiara. The chance depends on the Noble Phantasm’s range.', '範囲宝具がキアラのそばの護衛センチネルまで巻き込めます。確率は宝具の範囲によって異なります。', '范围宝具可以波及祈荒身边的护卫哨兵。概率因宝具范围而异。', '範圍寶具可以波及祈荒身邊的護衛哨兵。機率因寶具範圍而異。'),
 'f2': ('호위 센티넬의 밤 회복이 감소합니다.', 'Guard Sentinels now recover less at night.', '護衛センチネルの夜の回復量が減少します。', '护卫哨兵的夜间恢复减少。', '護衛哨兵的夜間恢復減少。'),
 'f3': ('밤 선택지에서 「센티넬을 사냥한다」와 「토벌령을 따른다」가 맨 위로 오도록 변경됩니다.', 'In night choices, “Hunt a Sentinel” and “Follow the subjugation order” now appear at the top.', '夜の選択肢で「センチネルを狩る」と「討伐令に従う」が一番上に来るように変更されます。', '夜晚选项中，「狩猎哨兵」与「遵从讨伐令」改为排在最上方。', '夜晚選項中，「狩獵哨兵」與「遵從討伐令」改為排在最上方。'),
 'f4': ('센티넬이 된 수녀의 서번트는 이미 알던 진명과 보구가 그대로 보입니다.', 'For the Sister’s Servant who became a Sentinel, the True Name and Noble Phantasm you already knew stay visible.', 'センチネルとなった修道女のサーヴァントは、既に知っていた真名と宝具がそのまま表示されます。', '成为哨兵的修女的从者，已知的真名与宝具会照常显示。', '成為哨兵的修女的從者，已知的真名與寶具會照常顯示。'),
 'g7': ('수정', 'Fixes', '修正', '修复', '修復'),
 'h1': ('업적 「호위를 걷어 내다」가 강림 전에 센티넬을 모두 쓰러뜨리면 열리지 않던 문제를 수정했습니다.', 'Fixed the achievement “Clearing the Guard” not unlocking if you defeated every Sentinel before the descent.', '実績「護衛を払いのけて」が、降臨前にセンチネルを全て倒すと解除されなかった問題を修正しました。', '修复了在降临前击倒所有哨兵时，成就「剥除护卫」无法解锁的问题。', '修復了在降臨前擊倒所有哨兵時，成就「剝除護衛」無法解鎖的問題。'),
 'h1a': ('설명도 「센티넬을 모두 걷어 내고 키아라를 쓰러뜨렸다」로 변경됩니다.', 'Its description is now “Defeated Kiara after every Sentinel had fallen.”', '説明も「センチネルをすべて退け、キアラを倒した」に変更されます。', '说明也改为「剥除了所有哨兵并击倒了祈荒」。', '說明也改為「剝除了所有哨兵並擊倒了祈荒」。'),
 'h2': ('직장을 쉬거나 떠돌며 연구하는 중에도 직장 연락이 오던 문제를 수정했습니다.', 'Fixed work calls still coming while you were on leave or wandering in research.', '仕事を休んでいたり、放浪しながら研究している間も職場から連絡が来ていた問題を修正しました。', '修复了在休假或四处游历研究期间仍会接到工作联系的问题。', '修復了在休假或四處遊歷研究期間仍會接到工作聯繫的問題。'),
 'h3': ("여성 마스터를 놀이터의 아이가 '아저씨'라고 부르던 문제를 수정했습니다.", 'Fixed the child at the playground calling a female Master “mister.”', '公園の子どもが女性マスターを「おじさん」と呼んでいた問題を修正しました。', '修复了游乐场的孩子把女性御主叫成「大叔」的问题。', '修復了遊樂場的孩子把女性御主叫成「大叔」的問題。'),
 'h4': ('시계탑 강연에서 수육한 서번트가 곁에 있거나 서번트를 부르지 않았는데도 재회를 묻던 문제를 수정했습니다.', 'Fixed the Clock Tower lecture asking about a reunion even when your incarnated Servant was beside you or you never summoned one.', '時計塔の講演で、受肉したサーヴァントがそばにいたり、サーヴァントを呼ばなかったのに再会について尋ねられていた問題を修正しました。', '修复了时钟塔讲座中，即使受肉的从者就在身边或从未召唤从者，仍被问到是否想重逢的问题。', '修復了時鐘塔講座中，即使受肉的從者就在身邊或從未召喚從者，仍被問到是否想重逢的問題。'),
 'h5': ('각인을 받지 않은 마스터에게 아이의 각인을 묻는 편지가 오던 문제를 수정했습니다.', 'Fixed letters asking about your child’s Crest arriving for Masters who never received a Crest.', '刻印を受け継いでいないマスターに、子どもの刻印について尋ねる手紙が届いていた問題を修正しました。', '修复了未继承刻印的御主收到询问孩子刻印的信件的问题。', '修復了未繼承刻印的御主收到詢問孩子刻印的信件的問題。'),
 'h6': ('형제의 동맹 거절 대사가 각인의 행방에 맞지 않던 문제를 수정했습니다.', 'Fixed your sibling’s alliance-refusal line not matching who actually had the Crest.', '兄弟が同盟を断る台詞が、刻印の行方と合っていなかった問題を修正しました。', '修复了兄弟姐妹拒绝结盟的台词与刻印归属不符的问题。', '修復了兄弟姊妹拒絕結盟的台詞與刻印歸屬不符的問題。'),
 'h7': ('사건으로 령주를 더 받았을 때 결과 화면의 남은 령주 수가 틀리던 문제를 수정했습니다.', 'Fixed the remaining Command Spells on the results screen being wrong when you gained extra Spells from events.', 'イベントで令呪を追加で得たとき、結果画面の残り令呪数が間違っていた問題を修正しました。', '修复了通过事件额外获得令咒时，结算画面剩余令咒数错误的问题。', '修復了透過事件額外獲得令咒時，結算畫面剩餘令咒數錯誤的問題。'),
 'h8': ('교회 출신이나 교회와 인연을 맺은 마스터에게도 교회가 시비를 걸러 오던 문제를 수정했습니다.', 'Fixed the Church coming to pick a fight even with Masters from the Church or tied to it.', '教会出身や教会と縁を結んだマスターにも、教会が言いがかりをつけに来ていた問題を修正しました。', '修复了教会仍会找教会出身或与教会有渊源的御主麻烦的问题。', '修復了教會仍會找教會出身或與教會有淵源的御主麻煩的問題。'),
 'h9': ('마의 피와 과거시의 마안처럼 전투 행동이 없는 마안은 상태 패널에 효과가 표시됩니다.', 'Mystic Eyes with no battle action, like Demon blood and the Mystic Eyes of Retrocognition, now show their effect on the status panel.', '魔の血や過去視の魔眼のように戦闘行動のない魔眼は、ステータスパネルに効果が表示されます。', '像魔之血、过去视魔眼这类没有战斗行动的魔眼，效果会显示在状态面板上。', '像魔之血、過去視魔眼這類沒有戰鬥行動的魔眼，效果會顯示在狀態面板上。'),
 'h10': ('물러설 때 퇴각 소리와 막음 소리가 겹치던 문제를 수정했습니다.', 'Fixed the retreat sound overlapping with the block sound when falling back.', '退くときに、撤退の音と防御の音が重なっていた問題を修正しました。', '修复了撤退时撤退音效与格挡音效重叠的问题。', '修復了撤退時撤退音效與格擋音效重疊的問題。'),
 'h11': ('결정 창 제목이 낱말 중간에서 끊기거나 비교 카드의 칭호가 잘리던 문제를 수정했습니다.', 'Fixed decision-window titles breaking mid-word and titles being cut off on comparison cards.', '決定ウィンドウのタイトルが単語の途中で改行されたり、比較カードの称号が切れていた問題を修正しました。', '修复了决定窗口标题在词语中间断行、对比卡片上的称号被截断的问题。', '修復了決定視窗標題在詞語中間斷行、對比卡片上的稱號被截斷的問題。'),
 'h12': ('서버가 몰릴 때 기기 연결, 다른 조 불러오기, 기록 보내기가 가끔 실패하던 문제를 수정했습니다.', 'Fixed device linking, loading other teams, and sending records sometimes failing when the server was busy.', 'サーバーが混雑しているときに、機器連携、他の陣営の読み込み、記録の送信がときどき失敗していた問題を修正しました。', '修复了服务器繁忙时，设备连接、读取其他组、发送记录偶尔失败的问题。', '修復了伺服器繁忙時，裝置連結、讀取其他組、傳送記錄偶爾失敗的問題。'),
}
K = lambda k: T[k][0]
G = [
 ['g1', ['a1', ['a1a']], 'a2', 'a3', 'a4'],
 ['g2', 'b1'],
 ['g3', ['c1', ['c1a', 'c1b']], 'c2', 'c3', ['c4', ['c4a']], ['c5', ['c5a', 'c5b']]],
 ['g4', 'd1', ['d2', ['d2a']]],
 ['g5', ['e1', ['e1a']], 'e2', 'e3', 'e4'],
 ['g6', 'f1', 'f2', 'f3', 'f4'],
 ['g7', ['h1', ['h1a']], 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12'],
]
def item(x):
    return [K(x[0]), [K(y) for y in x[1]]] if isinstance(x, list) else K(x)
entry = {'v': '2026.11.17', 'n': '2.01', 't': K('title'), 'g': [[K(g[0]), [item(x) for x in g[1:]]] for g in G]}
js = json.dumps(entry, ensure_ascii=False, separators=(',', ':'))
js = js.replace('"v":', 'v:', 1).replace(',"n":"2.01"', ",n:'2.01'", 1).replace(',"t":', ',t:', 1).replace(',"g":', ',g:', 1)
o = 'const PATCH=[\n'
if s.count(o) != 1: print('못 찾음 PATCH'); sys.exit(1)
s = s.replace(o, o + ' ' + js + ',\n')

s, nd, _ = i18n.add(s, dict_items=[(a, b, c) for a, b, c, *_ in T.values()])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
if os.path.exists(zp):
    Z = json.load(open(zp, encoding='utf-8')); n = 0
    for a, _b, _c, d, e in T.values():
        if a not in Z: Z[a] = [d, e]; n += 1
    json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0); print('중국어 사전', n)
print('적용 끝 · 사전', nd)
