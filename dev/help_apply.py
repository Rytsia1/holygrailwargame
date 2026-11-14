"""도움말 다듬기 (11-14): 항목 이름은 본문 위 금색 소제목으로, 본문은 한 문장씩 점으로 나눈다. 한국어는 단어 중간에서 끊지 않는다.
- 문장은 뜻을 그대로 두고 쉼표에서 나눈다 · '시작 화면' → '로비' · 보구 격돌 도움말도 '~합니다'체로
- 대상: 익명 통계 · 다른 플레이어의 조 · 다른 기기와 연결 · 인연 소환 · 보구 격돌
사용: python3 help_apply.py <game.html>"""
import sys, i18n

# (항목 이름, [(ko, en, ja), ...]) — 문자열 하나면 그대로 한 덩이
STAT = [
 ('하는 일', [('한 생이 끝날 때 게임 결과를 익명으로 모읍니다.', 'When a life ends, its game result is collected anonymously.', '一つの人生が終わると、ゲーム結果を匿名で集めます。'),
            ('모인 결과는 엔딩 화면의 ‘전체 플레이어 기록’과 도감·업적의 비율로 보여 줍니다.', "The results are shown as ‘All players’ records’ on the ending screen and as percentages in the Codex and achievements.", '集めた結果は、エンディング画面の「全プレイヤーの記録」や図鑑・実績の割合として表示します。'),
            ('기록이 어느 정도 모인 뒤부터 보입니다.', 'These appear once enough records have been collected.', '記録がある程度集まってから表示されます。')]),
 ('보내는 것', '서번트, 결말, 성배의 상태, 도시, 출신, 회로 등급, 나이, 얻은 업적, 언어, 이 기기의 무작위 번호'),
 ('보내지 않는 것', '이름, 소원·남긴 생각·유언처럼 직접 쓴 문장, 세이브 내용'),
 ('끄면', [('내 게임 결과를 더 이상 보내지 않습니다.', 'Your game results are no longer sent.', '自分のゲーム結果を送らなくなります。'),
          ('전체 통계는 끈 뒤에도 그대로 볼 수 있습니다.', 'You can still see the global stats after turning it off.', 'オフにした後も全体統計はそのまま見られます。')])]
GHOST = [
 ('하는 일', [('내 성배전쟁에 가끔 다른 플레이어가 보낸 조가 찾아옵니다.', 'Teams sent by other players sometimes turn up in your Holy Grail War.', '自分の聖杯戦争に、ときどき他のプレイヤーが送った組がやって来ます。'),
            ('1~40년 전 다른 도시의 성배전쟁에서 살아남은 조입니다.', 'They survived a Holy Grail War in another city 1 to 40 years earlier.', '1〜40年前に別の街の聖杯戦争を生き延びた組です。'),
            ('전쟁 제5~7일에 감독관의 통지와 함께 여덟 번째 조로 끼어듭니다.', 'They force their way in as an eighth team on day 5–7, announced by the overseer.', '戦争の5〜7日目に、監督役の通達とともに八番目の組として割り込みます。')]),
 ('그 조의 특징', [('성배가 부른 조가 아니어서, 새 령주 없이 지난 전쟁에서 남긴 령주로 싸웁니다.', 'Since the Grail did not call them, they get no new Command Spells and fight with whatever they had left from their last war.', '聖杯に呼ばれた組ではないため、新しい令呪なしに前の戦争で残した令呪で戦います。'),
               ('그때 만난 서번트를 기억해, 아는 상대와는 더 능숙하게 싸웁니다.', 'They remember the Servants they met then and fight known foes more skillfully.', 'そのとき出会ったサーヴァントを覚えていて、知っている相手とはより巧みに戦います。'),
               ('동맹이 되면 알고 있는 진명과 보구를 알려 줍니다.', 'When allied, they share the True Names and Noble Phantasms they know.', '同盟を結べば、知っている真名と宝具を教えてくれます。')]),
 ('내 조 보내기', [('살아남은 조는 엔딩 화면의 ‘이 조를 다른 성배전쟁으로 보내기’로 보낼 수 있습니다.', 'A surviving team can be sent from ‘Send this team to another Holy Grail War’ on the ending screen.', '生き残った組は、エンディング画面の「この組を別の聖杯戦争へ送る」から送れます。'),
               ('이름은 그대로 또는 무작위 이름으로 보낼 수 있습니다.', 'You can send it under its real name or a random one.', '名前はそのままでも、ランダムな名前でも送れます。'),
               ('보낸 조는 기록 화면에서 언제든 거둘 수 있습니다.', 'You can recall a sent team from the record screen at any time.', '送った組は、記録画面からいつでも呼び戻せます。')]),
 ('이름 신고', [('부적절한 이름은 전쟁 보고서의 ‘이름 신고’로 알려 주세요.', 'Please flag inappropriate names with ‘Report name’ in the war report.', '不適切な名前は、戦争報告の「名前を通報」で知らせてください。'),
             ('서로 다른 세 곳에서 신고가 오면 그 조는 숨겨집니다.', 'A team is hidden once reports come in from three different places.', '異なる3か所から通報が届くと、その組は非表示になります。'),
             ('같은 사람이 여러 번 신고하지 못하도록, 신고할 때만 접속 주소를 되돌릴 수 없게 바꾼 값을 함께 저장합니다.', 'To stop one person from reporting many times, an irreversibly scrambled form of your connection address is stored with a report — and only when you report.', '同じ人が何度も通報できないよう、通報するときだけ接続アドレスを元に戻せない形に変えた値を一緒に保存します。')]),
 ('보낸 조의 소식', [('보낸 조가 다른 성배전쟁에 끼어들면 그 결과가 소식으로 옵니다.', 'When a team you sent joins another Holy Grail War, the outcome comes to you as news.', '送った組が別の聖杯戦争に割り込むと、その結果が便りとして届きます。'),
                ('‘보낸 조 소식 알림’을 끄면 로비의 알림만 뜨지 않습니다.', 'Turning off ‘Team news alerts’ only stops the alert in the lobby.', '「送った組の便りの通知」をオフにすると、ロビーの通知だけが出なくなります。'),
                ('소식은 계속 쌓이고, ‘보낸 조 소식 보기’와 지난 생 기록에서 볼 수 있습니다.', 'News keeps coming in and can be seen via ‘See team news’ and in your past lives.', '便りは引き続き届き、「送った組の便りを見る」や過去の人生の記録で見られます。')]),
 ('끄면', [('내 성배전쟁에 다른 플레이어의 조가 나오지 않습니다.', "Other players' teams will not appear in your Holy Grail Wars.", '自分の聖杯戦争に他プレイヤーの組が出なくなります。'),
          ('내 조를 보내는 것은 끈 뒤에도 할 수 있습니다.', 'You can still send your own teams after turning it off.', '自分の組を送ることは、オフにした後もできます。')])]
SYNC = [
 ('하는 일', [('휴대폰과 PC처럼 여러 기기에서 같은 기록으로 번갈아 할 수 있습니다.', 'Play with the same records on several devices, like your phone and PC.', 'スマホとPCのように、複数の端末で同じ記録を交互に遊べます。'),
            ('한 기기에서 만든 연결 코드를 다른 기기에 넣으면, 그 뒤로 지난 생·도감·업적·이어하기·보낸 조 소식이 자동으로 맞춰집니다.', 'Enter a link code made on one device into another; from then on, past lives, the codex, achievements, your saved life, and news of teams you sent stay in sync automatically.', 'ある端末で作った連携コードを別の端末に入れると、それ以降は過去の人生・図鑑・実績・続きから・送った組の便りが自動で同期されます。'),
            ('기기는 5대까지 연결할 수 있습니다.', 'You can link up to 5 devices.', '端末は5台まで連携できます。')]),
 ('맞추는 때', [('로비를 열 때, 이어하기를 누를 때, 한 생이 끝날 때, 게임을 나갈 때', 'When you open the lobby, press Continue, finish a life, or exit a game', 'ロビーを開いたとき、「続きから」を押したとき、人生が終わったとき、ゲームを抜けたとき'),
             ('플레이 중에는 1분에 한 번', 'Once a minute while playing', 'プレイ中は1分に1回'),
             ('인터넷이 끊겨 있으면 다음 기회에 맞춥니다.', "If you're offline, it syncs at the next chance.", 'オフラインのときは次の機会に同期します。')]),
 ('합치는 방식', [('두 기기에서 따로 플레이해도 지난 생과 업적은 모두 남습니다.', 'Even if you play separately on two devices, every past life and achievement is kept.', '2つの端末で別々に遊んでも、過去の人生と実績はすべて残ります。'),
              ('계약 횟수 같은 숫자는 양쪽에서 늘어난 만큼 더해집니다.', 'Counts like contracts add up what each side gained.', '契約回数などの数は、両方で増えた分が足されます。'),
              ('같은 생을 두 기기에서 따로 진행했다면, 이어하기를 누를 때 하나를 고릅니다.', 'If you continued the same life separately on two devices, you pick one when you press Continue.', '同じ人生を2つの端末で別々に進めた場合は、「続きから」を押したときに1つを選びます。')]),
 ('맞추지 않는 것', [('언어, 연출(시작·격돌·령주), 익명 통계, 다른 플레이어의 조 만나기, 소식 알림 같은 설정은 기기마다 따로 둡니다.', "Settings such as language, effects (opening, clash, Command Spells), anonymous stats, meeting other players' teams, and news alerts stay separate on each device.", '言語、演出（開始・激突・令呪）、匿名統計、他のプレイヤーの組との遭遇、便りの通知などの設定は端末ごとに別々です。')]),
 ('맡기는 것', [('기록 묶음 전체(직접 쓴 이름과 문장 포함)를 압축해 서버에 맡깁니다.', 'All of your records (including names and sentences you wrote) are compressed and kept on the server.', '記録すべて（自分で書いた名前や文章を含む）を圧縮してサーバーに預けます。'),
             ('서버는 연결 키를 되돌릴 수 없게 바꾼 값으로만 찾고, 내용은 열어 보지 않습니다.', 'The server finds them only by an irreversibly transformed version of your link key and never opens the contents.', 'サーバーは連携キーを元に戻せない形に変えた値でしか探さず、中身は開きません。'),
             ('마지막으로 맞춘 지 180일이 지나거나, 모든 기기에서 연결을 끊으면 지워집니다.', 'They are deleted 180 days after the last sync, or when every device unlinks.', '最後の同期から180日が過ぎるか、すべての端末で連携を解除すると削除されます。')]),
 ('연결 코드', [('10분 동안 한 번만 쓸 수 있습니다.', 'It can be used once, within 10 minutes.', '10分以内に一度だけ使えます。'),
             ('코드를 아는 사람은 기록 전체를 받아 갈 수 있으니, 다른 사람에게 보여 주지 마세요.', "Anyone who knows the code can take all of your records, so don't show it to anyone else.", 'コードを知っている人は記録すべてを受け取れるので、他の人に見せないでください。')])]
BOND = [
 ('하는 일', [('지난 생에 계약했던 서번트를 로비의 ‘인연 소환’에서 골라 둡니다.', 'Choose a Servant you contracted in a past life under ‘Bond Summoning’ in the lobby.', '前世に契約したサーヴァントを、ロビーの「縁の召喚」で選んでおきます。'),
            ('소환할 때 촉매 대신 그 서번트를 부를 수 있습니다.', 'When you summon, you can call them instead of using a catalyst.', '召喚のとき、触媒の代わりにそのサーヴァントを呼べます。'),
            ('어벤저·룰러도 고를 수 있습니다.', 'Avengers and Rulers can be chosen too.', 'アヴェンジャー・ルーラーも選べます。')]),
 ('닿을 확률', [('그 서번트와 성배를 쥔 적이 있으면 반드시 옵니다.', "If you've won the Grail with that Servant, they always come.", 'そのサーヴァントと聖杯を手にしたことがあれば、必ず来ます。'),
             ('아니면 10%에서 시작해, 마지막으로 함께한 생의 신뢰 1마다 0.5%씩 더해집니다. (최대 60%)', "Otherwise it starts at 10%, plus 0.5% for each point of trust in your last life together. (Up to 60%)", 'そうでなければ10%から始まり、最後に共にした生の信頼1ごとに0.5%ずつ加わります。（最大60%）'),
             ('닿지 않으면 평소처럼 성배가 고른 서번트가 옵니다.', "If the bond doesn't reach, a Servant the Grail chooses comes as usual.", '届かなければ、いつも通り聖杯が選んだサーヴァントが来ます。')]),
 ('통계', [('인연 소환으로 부른 생은 전체 플레이어 통계에 넣지 않습니다.', "Lives where a Servant was called by Bond Summoning aren't counted in the all-player statistics.", '縁の召喚で呼んだ生は、全プレイヤーの統計に含めません。'),
         ('내 기록과 도감에는 그대로 남습니다.', 'They still remain in your own records and Codex.', '自分の記録と図鑑にはそのまま残ります。')])]
NP = [
 ('격돌', [('같은 합에 양쪽이 보구를 쓰면 격돌합니다.', 'If both sides use a Noble Phantasm in the same exchange, they clash.', '同じ合で双方が宝具を使うと激突します。'),
         ('격돌의 세기는 보구 랭크와 서번트 마력이 바탕입니다.', "A clash's strength rests on the Noble Phantasm's rank and the Servant's mana.", '激突の強さは、宝具のランクとサーヴァントの魔力が土台です。'),
         ('여기에 보구 종류의 상성, 상대 보구를 알고 있는지, 령주로 밀어붙였는지가 더해집니다.', 'On top of that come the type matchup, whether you know the enemy Noble Phantasm, and whether a Command Spell pushed it through.', 'そこに宝具の種別の相性、相手の宝具を知っているか、令呪で押し切ったかが加わります。')]),
 ('꿰뚫음과 상쇄', [('힘의 차이가 크면 이긴 쪽이 상대 보구를 꿰뚫습니다. 피해의 60~100%를 주고, 자신은 여파 10%만 받습니다.', 'If the gap is large, the winner pierces the enemy Noble Phantasm. It deals 60–100% of its damage and takes only 10% backlash itself.', '力の差が大きければ、勝った側が相手の宝具を貫きます。被害の60〜100%を与え、自分は余波の10%だけ受けます。'),
               ('차이가 작으면 두 보구가 함께 흩어지고, 서로 30%씩 받습니다.', 'If the gap is small, both Noble Phantasms scatter and each side takes 30%.', '差が小さければ二つの宝具はともに散り、互いに30%ずつ受けます。')]),
 ('보구 종류', [('대인보구 < 대군보구 < 대성·대국보구 < 대계보구 순으로, 넓을수록 격돌에 유리합니다.', 'Wider is stronger in a clash: Anti-Unit < Anti-Army < Anti-Fortress / Anti-Country < Anti-World.', '対人宝具 < 対軍宝具 < 対城・対国宝具 < 対界宝具の順に、広いほど激突で有利です。'),
             ('대신 좁을수록 보구를 쓸 때 서번트 마력이 덜 듭니다. (대인보구 −20%, 대성·대국보구 +15%, 대계보구 +30%)', 'In return, narrower Noble Phantasms cost less Servant mana to use. (Anti-Unit −20%, Anti-Fortress / Anti-Country +15%, Anti-World +30%)', 'そのかわり、狭いほど宝具を使うときのサーヴァント魔力が少なくて済みます。（対人宝具−20%、対城・対国宝具+15%、対界宝具+30%）'),
             ('결계보구는 대군보구로 봅니다.', 'Bounded Fields are treated as Anti-Army.', '結界宝具は対軍宝具とみなします。')]),
 ('몸을 뺀다', [('보구를 거두고 피하면 일정 확률로 완전히 피합니다. 실패해도 피해는 절반입니다.', 'Withdrawing to evade dodges completely with some chance. Even on a failure, damage is halved.', '宝具を収めて避ければ、一定の確率で完全に避けます。失敗しても被害は半分です。'),
             ('민첩이 높을수록, 상대 보구가 대인보구에 가까울수록 잘 피합니다.', 'Higher Agility and enemy Noble Phantasms closer to Anti-Unit make evasion easier.', '敏捷が高いほど、相手の宝具が対人宝具に近いほど避けやすくなります。'),
             ('공격 보구가 없는 서번트는 더 잘 피합니다.', 'Servants without an attacking Noble Phantasm evade more easily.', '攻撃宝具のないサーヴァントは、より避けやすくなります。')]),
 ('보구의 역할', [('<b>공격·강화</b> 격돌해 피해를 줍니다.', None, None), ('<b>영역</b> 펼쳐 둔 동안 서번트가 더 강하게 싸웁니다.', None, None), ('<b>방어</b> 상대 보구를 막습니다.', None, None),
              ('<b>보조·약화</b> 격돌하지 않고, 몇 합 동안 판을 돕습니다.', None, None), ('<b>특수</b> 보구마다 규칙이 다릅니다.', None, None)]),
 ('남는 효과', [('영역·방벽·보조 효과는 몇 합 동안 남고, 합마다 기록에 남은 합 수가 나옵니다.', 'Fields, barriers and support effects last a few exchanges, and the log shows how many remain each time.', '領域・障壁・補助効果は数合のあいだ残り、合ごとに記録に残りの合数が出ます。'),
             ('남아 있는 동안 서번트 마력이 조금씩 듭니다.', 'They cost a little Servant mana while they last.', '残っているあいだ、サーヴァント魔力が少しずつかかります。')]),
 ('상대 보구', [('상대의 진명이나 보구를 알아내면, 조 목록에서 그 조를 눌러 격돌 역할과 우리 보구와의 비교를 볼 수 있습니다.', "Once you learn an enemy's True Name or Noble Phantasm, tap that team in the team list to see its clash role and how it compares with our Noble Phantasm.", '相手の真名か宝具がわかれば、陣営一覧でその陣営を押して、激突での役割と我々の宝具との比較を見られます。')])]
# 보구의 역할: <b>이름</b>과 설명은 따로 옮겨진다
EXTRA = [('공격·강화', 'Attack · Enhancement', '攻撃・強化'), ('보조·약화', 'Support · Weakening', '補助・弱体'),
 ('격돌해 피해를 줍니다.', 'They clash and deal damage.', '激突して被害を与えます。'),
 ('펼쳐 둔 동안 서번트가 더 강하게 싸웁니다.', 'While it stands, the Servant fights harder.', '展開しているあいだ、サーヴァントがより強く戦います。'),
 ('상대 보구를 막습니다.', 'Blocks enemy Noble Phantasms.', '相手の宝具を防ぎます。'),
 ('격돌하지 않고, 몇 합 동안 판을 돕습니다.', "They don't clash; they help the fight for a few exchanges.", '激突せず、数合のあいだ戦いを助けます。'),
 ('보구마다 규칙이 다릅니다.', 'Each follows its own rules.', '宝具ごとに規則が違います。'),
 ('자세한 내용은 조 목록에서 ‘당신’ 줄을 누르면 보구 칸에 나옵니다.', 'For details, tap your row in the team list and look under Noble Phantasm.', '詳しくは陣営一覧で「あなた」の行を押すと宝具欄に出ます。')]


def js(rows):
    out = []
    for lab, v in rows:
        if isinstance(v, str): out.append(f"['{lab}','{v}']")
        else: out.append(f"['{lab}',[" + ','.join(f"'{x[0]}'" for x in v) + "]]")
    return ',\n    '.join(out)


def trs(*groups):
    r = []
    for g in groups:
        for _, v in g:
            if isinstance(v, list): r += [x for x in v if x[1]]
    return r + EXTRA


CSS = r'''
/* ---- 도움말: 소제목 + 한 문장씩 (help_apply) ---- */
#infoBody dl.help{display:block;margin:12px 0 0}
#infoBody dl.help dt{display:flex;align-items:center;gap:8px;margin:18px 0 7px;font:700 13px var(--lbF,var(--f-story));letter-spacing:.06em;color:#c9ad72}
#infoBody dl.help dt:first-child{margin-top:4px}
#infoBody dl.help dt::before{content:'';flex:none;width:5px;height:5px;transform:rotate(45deg);background:#c9ad72}
#infoBody dl.help dt::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(216,189,124,.32),rgba(216,189,124,0))}
#infoBody dl.help dd{margin:0;font:14px/1.75 var(--f-story);color:#e4dccb}
html[lang=ko] #infoBody dl.help dd{word-break:keep-all}
#infoBody dl.help ul{margin:0;padding:0;list-style:none;display:grid;gap:6px}
#infoBody dl.help li{position:relative;padding-left:14px}
#infoBody dl.help li::before{content:'';position:absolute;left:2px;top:.75em;width:4px;height:4px;border-radius:50%;background:rgba(216,189,124,.75)}
#infoBody dl.help li b{color:#e2c98e;font-weight:700;margin-right:6px}
'''

for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def cut(a, b):  # a로 시작해 b로 끝나는 덩이를 찾는다
        i = s.index(a); j = s.index(b, i) + len(b); return i, j
    def put(a, b, new):
        global s
        try: i, j = cut(a, b)
        except ValueError: miss.append(a[:40]); return
        s = s[:i] + new + s[j:]
    put("const HELP={\n  stat:", "끈 뒤에도 할 수 있습니다.']]}}",
        "const HELP={\n  stat:{t:'익명 통계',rows:[\n    " + js(STAT) + "]},\n  ghost:{t:'다른 플레이어의 조',rows:[\n    " + js(GHOST) + "]}}")
    put("HELP.sync={t:'다른 기기와 연결',rows:[", "보여 주지 마세요.']]};", "HELP.sync={t:'다른 기기와 연결',rows:[\n    " + js(SYNC) + "]};")
    put("HELP.bond={t:'인연 소환',rows:[", "그대로 남습니다.']]};", "HELP.bond={t:'인연 소환',rows:[\n    " + js(BOND) + "]};")
    put("  rows.push(['격돌',", "비교를 볼 수 있다.']);", "  rows.push(" + js(NP) + ");")
    def rp(o, n):
        global s
        if s.count(o) != 1: miss.append((o[:50], s.count(o))); return
        s = s.replace(o, n)
    rp("<br>자세한 내용은 조 목록에서 ‘당신’ 줄을 누르면 보구 칸에 나온다.`", "<br>자세한 내용은 조 목록에서 ‘당신’ 줄을 누르면 보구 칸에 나옵니다.`")
    rp("<dl class=\"row\">${h.rows.map(([a,b])=>`<dt>${a}</dt><dd>${b}</dd>`).join('')}</dl>",
       "<dl class=\"row help\">${h.rows.map(([a,b])=>`<dt>${a}</dt><dd>${Array.isArray(b)?`<ul>${b.map(x=>`<li>${x}</li>`).join('')}</ul>`:b}</dd>`).join('')}</dl>")
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    s, nd, nt = i18n.add(s, trs(STAT, GHOST, SYNC, BOND, NP))
    print('help miss', miss, 'tr', nd)
    open(P, 'w', encoding='utf-8').write(s)
