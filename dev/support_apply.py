"""11-22: 서버비 후원 안내 (로비 버튼 · 결과 화면 한 줄 · 패치 노트 아래)
- 게임 안에는 결제 화면을 두지 않고 바깥 후원 페이지로만 연결한다. 후원 보상 · 유료 요소 없음
- 한국어 화면: 토스 송금 링크(TOSS, 비어 있으면 숨김) + Buy Me a Coffee / 다른 언어: Buy Me a Coffee
- 로비의 「서버비 후원」 버튼은 안내 창(#info)을 연다. 결과 화면 · 패치 노트 아래 줄도 같은 창을 연다
사용: python3 support_apply.py <game.html> [--toss 주소]"""
import sys, os, json
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
import i18n
try:
    from opencc import OpenCC; CC = OpenCC('s2tw')
except ImportError: CC = None
P = sys.argv[1]
BMC = 'https://buymeacoffee.com/cupnight_'
TOSS = sys.argv[sys.argv.index('--toss') + 1] if '--toss' in sys.argv else ''
s = open(P, encoding='utf-8').read()
if 'function showSupport(' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    if s.count(o) != c: miss.append((o[:90], s.count(o))); return
    s = s.replace(o, n)

CUP = "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 9h12v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z'/%3E%3Cpath d='M16 10h1.5a2.5 2.5 0 0 1 0 5H16M8 3v3M12 3v3'/%3E%3C/svg%3E"
CSS = (".pn-btn.sup{text-decoration:none}"
       ".pn-btn.sup::before{-webkit-mask:url(\"data:image/svg+xml," + CUP + "\") center/contain no-repeat;mask:url(\"data:image/svg+xml," + CUP + "\") center/contain no-repeat}"
       ".sup-end{margin:10px auto 0;max-width:678px;box-sizing:border-box;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:10px 14px;border:1px dashed var(--line);border-radius:10px}"
       ".sup-end p{margin:0;color:var(--dim);font-size:13px;line-height:1.5;flex:1 1 220px}"
       ".sup-box p{margin:0 0 10px;line-height:1.7}.sup-box .sm{color:var(--dim);font-size:12.5px}"
       ".sup-go{display:flex;flex-direction:column;gap:8px;margin-top:14px}"
       ".sup-go a{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:12px 14px;border:1px solid var(--line);border-radius:10px;color:var(--text);text-decoration:none}"
       ".sup-go a:hover{border-color:var(--gold)}.sup-go a b{font-weight:600}.sup-go a span{color:var(--dim);font-size:12px}"
       ".pn-sup{margin-top:16px;padding-top:12px;border-top:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;color:var(--dim);font-size:13px}")
s = s.replace("</style>", CSS + "</style>", 1)

JS = r"""// 11-22: 서버비 후원 안내 (support_apply) — 바깥 후원 페이지로만 연결한다
const SUP_BMC=%s, SUP_TOSS=%s;
function showSupport(){
  const ko=LANG==='ko'&&SUP_TOSS;
  const go=(ko?`<a href="${SUP_TOSS}" target="_blank" rel="noopener"><b>토스로 후원</b><span>국내 계좌 · 수수료 없음</span></a>`:'')
    +`<a href="${SUP_BMC}" target="_blank" rel="noopener"><b>Buy Me a Coffee</b><span>${ko?'카드 · 해외 결제':'카드 · 간편 결제'}</span></a>`;
  $('#infoBody').innerHTML='<div class="eyebrow">후원</div><h2>서버비 후원</h2><div class="sup-box"><p>「성배가 차는 밤」은 개인이 서버 비용을 내며 운영하는 비공식 팬 게임입니다.</p><p>찾아 주시는 분이 늘면서 서버 비용도 늘고 있습니다. 즐겁게 플레이하셨다면 후원으로 응원해 주세요.</p><p class="sm">후원은 게임을 유지하는 데에만 쓰이며, 후원 보상이나 유료 요소는 없습니다. TYPE-MOON 및 공식 권리자와는 관계가 없습니다.</p><div class="sup-go">'+go+'</div></div>';
  infoHeld=false; $('#info').classList.remove('hidden'); }
document.addEventListener('click',e=>{ if(e.target.closest&&e.target.closest('.sup-open')) showSupport(); });
window.__showSupport=showSupport;
""" % (json.dumps(BMC), json.dumps(TOSS))
rp("function showPatch(){", JS + "function showPatch(){")
# 패치 노트 맨 아래
rp("+'</details>').join('');\n  $('#infoBody').innerHTML=html;", "+'</details>').join('')+'<div class=\"pn-sup\"><span>게임을 즐겨 주셔서 감사합니다. 서버비 후원을 받고 있습니다.</span><button class=\"pn-btn sup sup-open\" type=\"button\">서버비 후원</button></div>';\n  $('#infoBody').innerHTML=html;")
# 로비: 「의견 보내기」 옆
rp('<a id="fbBtn" class="pn-btn fb" href="https://x.com/cupnight_" target="_blank" rel="noopener">의견 보내기 <span class="h">@cupnight_</span></a>',
   '<a id="fbBtn" class="pn-btn fb" href="https://x.com/cupnight_" target="_blank" rel="noopener">의견 보내기 <span class="h">@cupnight_</span></a><button id="supBtn" class="pn-btn sup sup-open" type="button">서버비 후원</button>')
rp("mv(foot,'#patchBtn','#scnBtn','#achNewBtn','#fbBtn','#installBtn');", "mv(foot,'#patchBtn','#scnBtn','#achNewBtn','#fbBtn','#supBtn','#installBtn');")
rp("['#patchBtn','#scnBtn','#achNewBtn','#fbBtn','#installBtn'].forEach(s=>{", "['#patchBtn','#scnBtn','#achNewBtn','#fbBtn','#supBtn','#installBtn'].forEach(s=>{")
# 결과 화면: 「의견 보내기」 줄 아래
rp('<a class="pn-btn fb" href="https://x.com/cupnight_" target="_blank" rel="noopener">의견 보내기 <span class="h">@cupnight_</span></a></div>`;',
   '<a class="pn-btn fb" href="https://x.com/cupnight_" target="_blank" rel="noopener">의견 보내기 <span class="h">@cupnight_</span></a></div>\n  <div class="sup-end"><p>즐거우셨다면 서버비 후원으로 응원해 주세요. 개인이 서버 비용을 내며 운영하고 있습니다.</p><button class="pn-btn sup sup-open" type="button">서버비 후원</button></div>`;')
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

# 번역: (한국어, 영어, 일본어, 간체)
TR = [
 ('서버비 후원', 'Support the Server', 'サーバー費の支援', '支持服务器费用'),
 ('후원', 'Support', '支援', '支持'),
 ('「성배가 차는 밤」은 개인이 서버 비용을 내며 운영하는 비공식 팬 게임입니다.',
  '"The Night the Grail Fills" is an unofficial fan game run by one person who pays the server costs.',
  '「聖杯が満ちる夜」は、個人がサーバー費用を負担して運営している非公式のファンゲームです。',
  '《圣杯盈满之夜》是一款由个人承担服务器费用运营的非官方同人游戏。'),
 ('찾아 주시는 분이 늘면서 서버 비용도 늘고 있습니다. 즐겁게 플레이하셨다면 후원으로 응원해 주세요.',
  'As more people play, the server costs keep growing. If you enjoyed the game, please consider supporting it.',
  '遊んでくださる方が増え、サーバー費用も増えています。楽しんでいただけたなら、ご支援で応援していただけると嬉しいです。',
  '随着玩家增多，服务器费用也在增加。如果你玩得开心，欢迎通过支持来鼓励一下。'),
 ('후원은 게임을 유지하는 데에만 쓰이며, 후원 보상이나 유료 요소는 없습니다. TYPE-MOON 및 공식 권리자와는 관계가 없습니다.',
  'Support goes only toward keeping the game running. There are no rewards or paid features. This project is not affiliated with TYPE-MOON or any official rights holder.',
  'ご支援はゲームの維持のためだけに使います。支援による特典や有料要素はありません。本作はTYPE-MOONおよび公式の権利者とは一切関係ありません。',
  '支持仅用于维持游戏运营，没有支持回报或付费内容。本作与TYPE-MOON及官方权利方无关。'),
 ('토스로 후원', 'Support via Toss', 'Tossで支援', '通过Toss支持'),
 ('국내 계좌 · 수수료 없음', 'Korean bank account · No fees', '韓国の口座 · 手数料なし', '韩国账户 · 无手续费'),
 ('카드 · 해외 결제', 'Card · International', 'カード · 海外決済', '银行卡 · 海外支付'),
 ('카드 · 간편 결제', 'Card · Quick checkout', 'カード · かんたん決済', '银行卡 · 快捷支付'),
 ('게임을 즐겨 주셔서 감사합니다. 서버비 후원을 받고 있습니다.',
  'Thank you for playing. Support for server costs is welcome.',
  '遊んでくださってありがとうございます。サーバー費のご支援を受け付けています。',
  '感谢你的游玩。我们正在接受服务器费用的支持。'),
 ('즐거우셨다면 서버비 후원으로 응원해 주세요. 개인이 서버 비용을 내며 운영하고 있습니다.',
  'If you enjoyed it, please consider supporting the server costs. The game is run by one person who pays for the servers.',
  '楽しんでいただけたなら、サーバー費の支援で応援してください。個人がサーバー費用を負担して運営しています。',
  '如果你玩得开心，欢迎支持服务器费用。本游戏由个人承担服务器费用运营。'),
]
s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, _ in TR])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(D0, 'zh', 'done.json'); Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _, _, z in TR:
    if a not in Z:
        if CC is None: raise SystemExit('OpenCC 없음')
        Z[a] = [z, CC.convert(z).replace('“', '「').replace('”', '」')]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('후원 적용 · 사전', nd, '· 중국어', n, '· 토스', TOSS or '없음')
