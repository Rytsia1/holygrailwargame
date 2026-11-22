"""11-22: 패치 노트 2.02 「새 루트 「본성 속 진심」과 성향 콘텐츠 확장」 (영 · 일 · 중 번역, 번체는 OpenCC)
사용: python3 patch202_apply.py <game.html>"""
import sys, os, json
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
import i18n
try:
    from opencc import OpenCC; CC = OpenCC('s2tw')
except ImportError: CC = None

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if "n:'2.02'" in s: print('이미 적용됨'); sys.exit(0)

# (한국어, 영어, 일본어, 간체) — 번체는 간체에서 OpenCC
T = {
 'title': ('새 루트 「본성 속 진심」과 성향 콘텐츠 확장', 'New Route “The Truth Beneath Your Nature” and Expanded Dispositions', '新ルート「本性に潜む本心」と性向コンテンツの拡張', '新路线「本性深处的真心」与倾向内容扩充'),
 'g1': ('새 루트 「본성 속 진심」', 'New Route: “The Truth Beneath Your Nature”', '新ルート「本性に潜む本心」', '新路线「本性深处的真心」'),
 'a1': ('성배를 쥔 밤, 나의 성향 가운데 하나가 「깊음」에 닿아 있고 서번트가 살아 있다면, 소원 목록 맨 아래에 「본성 속 진심」이 나타납니다.',
        'On the night you hold the Grail, if one of your dispositions has reached “Deep” and your Servant is alive, “The Truth Beneath Your Nature” appears at the bottom of the wish list.',
        '聖杯を手にした夜、自分の性向のひとつが「深い」に達していて、サーヴァントが生きていれば、願いの一覧のいちばん下に「本性に潜む本心」が現れます。',
        '在握住圣杯的那一夜，若你的某一倾向已达到「深」，且从者仍然存活，愿望列表最下方就会出现「本性深处的真心」。'),
 'a2': ('고르면 나흘 동안 잔이 차오르고, 날마다 낮에는 일이 벌어지며 밤에는 서번트가 그 일에 대해 말을 겁니다.',
        'If you choose it, the cup fills over four days: each day something happens, and each night your Servant speaks to you about it.',
        '選ぶと四日かけて杯が満ちていき、毎日、昼には出来事が起こり、夜にはサーヴァントがそのことについて話しかけてきます。',
        '选择后，杯将在四天里渐渐盈满。每天白天会发生事件，夜里从者会就此与你交谈。'),
 'a2a': ('「잔을 내려놓는다」로 언제든 돌아설 수 있습니다.', 'You can turn back at any time with “Set down the cup.”', '「杯を置く」でいつでも引き返せます。', '随时可以通过「放下杯子」回头。'),
 'a3': ('서번트의 결심에 따라 결말이 여러 갈래로 나뉩니다.', 'The ending branches in several directions depending on your Servant’s Resolve.', 'サーヴァントの決意によって、結末がいくつにも分かれます。', '结局会根据从者的决心分成多条岔路。'),
 'a3a': ('결심은 서번트의 성향 · 속성 · 신뢰 · 인연에 따라 다르게 시작합니다.', 'Resolve starts differently depending on the Servant’s dispositions, Alignment, Trust, and Ties.', '決意はサーヴァントの性向・属性・信頼・縁によって、始まる値が変わります。', '决心的初始值会因从者的倾向、属性、信赖与羁绊而不同。'),
 'a3b': ('동맹 조가 살아 있다면 결말에 끼어들 수 있습니다.', 'If an allied team is still alive, they may step into the ending.', '同盟の組が生きていれば、結末に割って入ることがあります。', '若同盟组仍然存活，他们可能会介入结局。'),
 'a4': ('결말마다 이어지는 에필로그 사건이 추가됩니다.', 'Epilogue events that follow each ending have been added.', '結末ごとに続くエピローグのイベントが追加されます。', '新增了各个结局之后的尾声事件。'),
 'a5': ('결과 화면에 결말 이름표와 「본성 속 진심」이 기록됩니다.', 'The result screen now records the ending’s name tag and your “Truth Beneath Your Nature.”', '結果画面に結末の名札と「本性に潜む本心」が記録されます。', '结果画面会记录结局的名牌与「本性深处的真心」。'),
 'a6': ('동맹과 함께 소원을 빌 때도 열립니다. 검은 성배 · 비스트 위기에서는 열리지 않습니다.', 'It also opens when you make a wish together with an ally. It does not open during the Black Grail or Beast crises.', '同盟と共に願うときにも現れます。黒い聖杯・ビーストの危機では現れません。', '与同盟一同许愿时也会出现。黑色圣杯与Beast危机中不会出现。'),
 'a7': ('관련 업적 23종이 추가됩니다.', '23 related achievements have been added.', '関連する実績が23種追加されます。', '新增了23项相关成就。'),
 'g2': ('삶과 성향', 'Life and Dispositions', '人生と性向', '人生与倾向'),
 'b1': ('삶 파트에 성향 사건 46개가 추가됩니다.', '46 disposition events have been added to the Life part.', '人生パートに性向イベントが46個追加されます。', '人生部分新增了46个倾向事件。'),
 'b1a': ('이미 기운 성향이 있으면, 그 성향을 더 기울게 하는 사건이 조금 더 잘 나옵니다.', 'If you already lean toward a disposition, events that push it further appear a little more often.', 'すでに傾いている性向があれば、その性向をさらに傾ける出来事が少し出やすくなります。', '若已有偏向的倾向，进一步加深该倾向的事件会更容易出现一些。'),
 'b1b': ('복수 · 잔혹 · 금기 · 근원 집착 사건이 나오는 나이 폭이 넓어졌습니다.', 'Vengeance, Cruelty, Taboo, and Obsession with the Root events now appear across a wider range of ages.', '復讐・残酷・禁忌・根源への執着のイベントが起こる年齢の幅が広がりました。', '复仇、残酷、禁忌、执着于根源事件出现的年龄范围变宽了。'),
 'b2': ('삶 · 성장 사건의 선택지에 성향이 어느 쪽으로 움직이는지 표시됩니다.', 'Choices in Life and growth events now show which way your dispositions will move.', '人生・成長イベントの選択肢に、性向がどちらへ動くかが表示されます。', '人生与成长事件的选项中会显示倾向将往哪个方向变化。'),
 'b3': ('상태 칸에서 나의 성향(옅음 · 짙음 · 깊음)을 볼 수 있습니다. 성향을 누르면 어떤 서번트와 가까워지고 멀어지는지 보입니다.',
        'You can now see your dispositions (Faint · Strong · Deep) in the status panel. Tap a disposition to see which Servants it draws you closer to or pushes you away from.',
        'ステータス欄で自分の性向（薄い・濃い・深い）を確認できます。性向を押すと、どのサーヴァントと近づき、遠ざかるかが分かります。',
        '可以在状态栏查看自己的倾向（淡、浓、深）。点击倾向即可看到会与哪些从者走近或疏远。'),
 'b4': ('서번트 칸과 정보 창에 서번트의 성향 · 속성 · 궁합이 표시됩니다.', 'The Servant panel and info window now show the Servant’s dispositions, Alignment, and Compatibility.', 'サーヴァント欄と情報ウィンドウに、サーヴァントの性向・属性・相性が表示されます。', '从者栏与信息窗口中会显示从者的倾向、属性与契合度。'),
 'b5': ('성배전쟁 중 나의 성향이 바뀌면 서번트와의 궁합이 다시 계산됩니다.', 'If your dispositions change during the Holy Grail War, your Compatibility with your Servant is recalculated.', '聖杯戦争中に自分の性向が変わると、サーヴァントとの相性が再計算されます。', '圣杯战争中若你的倾向发生变化，与从者的契合度会重新计算。'),
 'g3': ('성배전쟁', 'Holy Grail War', '聖杯戦争', '圣杯战争'),
 'c1': ('갈림길 장면이 더 추가됩니다. 한 전쟁에 최대 5회까지 등장합니다.', 'More Crossroads scenes have been added. They appear up to five times in one war.', '岐路の場面がさらに追加されます。一つの戦争で最大5回まで登場します。', '新增了更多岔路口场景。一场战争中最多出现5次。'),
 'c1a': ('선택에 따라 나의 성향이 바뀝니다.', 'Your choices change your dispositions.', '選択によって自分の性向が変わります。', '你的选择会改变你的倾向。'),
 'c1b': ('습격해 온 조나 서번트를 크게 다치게 한 조를 기억합니다.', 'Teams that raided you or badly wounded your Servant are remembered.', '襲撃してきた組や、サーヴァントに大きな傷を負わせた組を覚えています。', '会记住曾袭击你，或让你的从者身受重伤的组。'),
 'c2': ('전투 중 대화로 동맹이 저절로 맺어지지 않고, 「동맹 제안」 창에서 받아들일지 고르게 변경됩니다.', 'Alliances no longer form automatically from talking during battle; you now choose whether to accept in the “Propose an Alliance” window.', '戦闘中の対話で同盟が自動的に結ばれることはなくなり、「同盟の提案」ウィンドウで受け入れるかどうかを選ぶように変更されます。', '战斗中的对话不再自动结成同盟，改为在「同盟提议」窗口中选择是否接受。'),
 'c3': ('싸움을 약속하는 일은 하루에 하나만 일어나게 변경됩니다.', 'Only one promised fight can now be arranged per day.', '戦いを約束する出来事は一日に一つだけ起こるように変更されます。', '约定决斗的事件改为一天只会发生一次。'),
 'c4': ('결전 날에는 결판 약속이 끼어들지 않습니다.', 'Promised showdowns no longer interrupt the day of the final battle.', '決戦の日には、決着の約束が割り込まなくなります。', '决战之日不会再插入决斗约定。'),
 'c5': ('서번트를 잃은 밤에는 다시 계약하지 않으며, 재계약한 조는 그 밤에 습격하지 않게 변경됩니다.', 'You no longer re-contract on the night you lose your Servant, and a team that has just re-contracted won’t raid that night.', 'サーヴァントを失った夜には再契約せず、再契約した組はその夜に襲撃しないように変更されます。', '失去从者的当晚不会再重新契约，刚重新契约的组当晚也不会发动袭击。'),
 'g4': ('에필로그와 서번트', 'Epilogue and Servants', 'エピローグとサーヴァント', '尾声与从者'),
 'd1': ('에필로그에 성향 사건 50개가 추가됩니다.', '50 disposition events have been added to the epilogue.', 'エピローグに性向イベントが50個追加されます。', '尾声新增了50个倾向事件。'),
 'd2': ('「서번트가 떠난 삶」에도 봄 열나흘과 첫 해 구간이 생기고, 관련 사건이 추가됩니다.', '“A Life After Your Servant Left” now also has the fourteen days of spring and the first year, with related events added.', '「サーヴァントが去った人生」にも春の十四日間と最初の一年の区間ができ、関連するイベントが追加されます。', '「从者离去后的人生」也加入了春天的十四天与第一年的阶段，并新增了相关事件。'),
 'd3': ('알트리아 펜드래곤과 연인이 될 수 있습니다. 관련 애정 대사가 추가됩니다.', 'You can now become lovers with Artoria Pendragon. New affection lines have been added for her.', 'アルトリア・ペンドラゴンと恋人になれます。関連する愛情の台詞が追加されます。', '现在可以与阿尔托莉雅·潘德拉贡成为恋人，并新增了相关的爱情台词。'),
 'g5': ('로비와 기기', 'Lobby and Devices', 'ロビーと端末', '大厅与设备'),
 'e1': ('설정 → 다른 기기와 연결에서 연결된 기기 목록을 보고, 다른 기기를 끊거나 이 기기의 이름을 바꿀 수 있습니다.', 'In Settings → Link devices, you can now see the list of linked devices, disconnect other devices, or rename this one.', '設定 → 他の端末と連携で、連携中の端末一覧を確認し、他の端末を切断したり、この端末の名前を変えたりできます。', '在「设置 → 关联其他设备」中，可以查看已关联的设备列表，断开其他设备，或修改本设备的名称。'),
 'e2': ('로비 메뉴 화면의 언어 버튼이 첫 화면과 같은 모양으로 변경됩니다.', 'The language button on the lobby menu screen now looks the same as on the title screen.', 'ロビーのメニュー画面の言語ボタンが、最初の画面と同じ形に変更されます。', '大厅菜单画面的语言按钮改为与初始画面相同的样式。'),
 'g6': ('수정', 'Fixes', '修正', '修复'),
 'h1': ('기록 복사 문구가 화면 언어와 상관없이 한국어로 복사되던 문제를 수정했습니다.', 'Fixed Copy record always copying the text in Korean regardless of the display language.', '記録をコピーすると、表示言語に関係なく韓国語でコピーされていた問題を修正しました。', '修复了复制记录时，无论界面语言为何都会复制成韩语的问题。'),
 'h2': ('일본어 화면 곳곳에 한국어가 남던 문제를 수정했습니다.', 'Fixed Korean text remaining in various places on the Japanese screen.', '日本語の画面のあちこちに韓国語が残っていた問題を修正しました。', '修复了日语界面各处残留韩语的问题。'),
 'h3': ('새로고침하거나 새 창을 열면 소리가 겹치던 문제를 수정했습니다. 가장 최근에 쓴 창에서만 소리가 납니다.', 'Fixed sound overlapping after reloading or opening a new window. Only the most recently used window plays sound.', '再読み込みしたり新しいウィンドウを開いたりすると、音が重なっていた問題を修正しました。最後に使ったウィンドウだけで音が鳴ります。', '修复了刷新或打开新窗口时声音重叠的问题。现在只有最近使用的窗口会发出声音。'),
 'h4': ('iPhone 홈 화면 앱에서 긴 창이 화면 위로 넘치던 문제를 수정했습니다.', 'Fixed long windows overflowing past the top of the screen in the iPhone Home Screen app.', 'iPhoneのホーム画面アプリで、長いウィンドウが画面の上にはみ出していた問題を修正しました。', '修复了在iPhone主屏幕应用中，较长的窗口超出画面上方的问题。'),
 'h5': ('일부 문장이 번역되지 않고 한국어로 남던 문제를 수정했습니다.', 'Fixed some sentences remaining untranslated in Korean.', '一部の文章が翻訳されず韓国語のまま残っていた問題を修正しました。', '修复了部分句子未被翻译、仍以韩语显示的问题。'),
 'h6': ('키아라 결전에서 호위 센티넬을 쓰러뜨렸을 때는 감독관의 령주를 받지 않게 변경됩니다. 결전 전에 도시의 센티넬을 사냥하면 이전처럼 령주를 받습니다.',
        'Defeating Kiara’s guard Sentinels during the final battle no longer earns a Command Spell from the Overseer. Hunting Sentinels in the city before the final battle still earns one as before.',
        'キアラとの決戦で護衛のセンチネルを倒したときは、監督役から令呪を受け取らないように変更されます。決戦の前に街のセンチネルを狩った場合は、これまでどおり令呪を受け取れます。',
        '在与杀生院祈荒的决战中击倒护卫哨兵时，不再从监督者处获得令咒。决战前在城市中狩猎哨兵，仍会像以前一样获得令咒。'),
}
K = lambda k: T[k][0]
G = [
 ['g1', 'a1', ['a2', ['a2a']], ['a3', ['a3a', 'a3b']], 'a4', 'a5', 'a6', 'a7'],
 ['g2', ['b1', ['b1a', 'b1b']], 'b2', 'b3', 'b4', 'b5'],
 ['g3', ['c1', ['c1a', 'c1b']], 'c2', 'c3', 'c4', 'c5'],
 ['g4', 'd1', 'd2', 'd3'],
 ['g5', 'e1', 'e2'],
 ['g6', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
]
def item(x):
    return [K(x[0]), [K(y) for y in x[1]]] if isinstance(x, list) else K(x)
entry = {'v': '2026.11.22', 'n': '2.02', 't': K('title'), 'g': [[K(g[0]), [item(x) for x in g[1:]]] for g in G]}
js = json.dumps(entry, ensure_ascii=False, separators=(',', ':'))
js = js.replace('"v":', 'v:', 1).replace(',"n":"2.02"', ",n:'2.02'", 1).replace(',"t":', ',t:', 1).replace(',"g":', ',g:', 1)
o = 'const PATCH=[\n'
if s.count(o) != 1: print('못 찾음 PATCH'); sys.exit(1)
s = s.replace(o, o + ' ' + js + ',\n')
s, nd, _ = i18n.add(s, dict_items=[(a, b, c) for a, b, c, _ in T.values()])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(D0, 'zh', 'done.json'); Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _b, _c, d in T.values():
    if a not in Z:
        if CC is None: raise SystemExit('OpenCC 없음')
        Z[a] = [d, CC.convert(d).replace('“', '「').replace('”', '」').replace('聖盃', '聖杯')]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('patch202 적용 · 사전', nd, '· 중국어', n)
