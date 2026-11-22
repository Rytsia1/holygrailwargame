"""11-22: 본성 속 진심(검귀 루트) 업적 23개 — 결말 7 · 진입 · 마스터 승 · 성향별 진입 5 · 성향별 마스터 승 5 · 숨겨진 3 · 싸움 · 삶 · 기록
- 기록이 없던 것은 새로 남긴다: kgStop(등 뒤의 칼을 령주로 멈춤) · kgKnew(알면서 받아들임). 고요해진 잔은 kgOff, 놓아준 해는 kgFree를 그대로 본다
- 「일곱 갈래의 밤」은 여러 생에 걸친 기록(meta): 도감 기록 c.kgE에 지난 생의 결말 키를 모은다(예전 생은 처음 한 번 생 기록에서 채움)
- 번역: 영어 · 일본어는 i18n.add, 중국어는 zh/done.json(간체 · OpenCC 번체)
사용: python3 kgach_apply.py <game.html>"""
import sys, os, json
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
import i18n
try:
    from opencc import OpenCC; CC = OpenCC('s2tw')
except ImportError: CC = None
P = sys.argv[1]
s = open(P, encoding='utf-8').read(); miss = []
if "id:'kg_in'" in s: print('이미 적용됨'); sys.exit(0)
def rp(o, n, c=1):
    global s
    if s.count(o) != c: miss.append((o[:80], s.count(o))); return
    s = s.replace(o, n)
E = '성배전쟁의 끝'
TN = {'avenger': ('복수', 'Vengeance', '復讐', '复仇'), 'judge': ('정의', 'Justice', '正義', '正义'), 'cruel': ('잔혹', 'Cruelty', '残酷', '残酷'),
      'taboo': ('금기', 'Taboo', '禁忌', '禁忌'), 'zeal': ('근원 집착', 'Obsession with the Root', '根源への執着', '执着于根源')}
# (id, 분류, 숨김, 판정, (이름 ko en ja zhs), (설명 ko en ja zhs))
A = [
 ('kg_in', E, 0, "!!S.flags.kg", ('본성 속 진심', 'The Truth Beneath Your Nature', '本性に潜む本心', '本性深处的真心'),
  ('본성 속 진심을 잔에 맡겼다', 'Entrusted the truth beneath your nature to the cup', '本性に潜む本心を杯に託した', '将本性深处的真心托付给了杯')),
 ('kg_m', E, 0, "S.flags.kgEnd==='m'", ('검을 거두지 않은 자', 'The One Who Did Not Sheathe the Blade', '剣を収めなかった者', '未曾收剑之人'),
  ('서번트를 꺾고 본성 속 진심을 이루었다', 'Defeated your Servant and fulfilled the truth beneath your nature', 'サーヴァントを打ち破り、本性に潜む本心を叶えた', '击败从者，实现了本性深处的真心')),
 ('kg_t', E, 0, "S.flags.kgEnd==='t'", ('둘이 이긴 세계', 'The World Two Won', '二人が勝った世界', '二人赢来的世界'),
  ('서번트와 함께 본성 속 진심을 이루었다', 'Fulfilled the truth beneath your nature together with your Servant', 'サーヴァントと共に本性に潜む本心を叶えた', '与从者一同实现了本性深处的真心')),
 ('kg_b', E, 0, "S.flags.kgEnd==='b'", ('묶인 잔', 'The Bound Cup', '縛られた杯', '被束缚的杯'),
  ('령주로 서번트를 묶고 본성 속 진심을 이루었다', 'Bound your Servant with a Command Spell and fulfilled the truth beneath your nature', '令呪でサーヴァントを縛り、本性に潜む本心を叶えた', '以令咒束缚从者，实现了本性深处的真心')),
 ('kg_s', E, 0, "S.flags.kgEnd==='s'", ('막아선 칼', 'The Blade That Stood in the Way', '立ちはだかった刃', '挡路之刃'),
  ('서번트가 끝내 당신을 막아섰다', 'Your Servant stood in your way to the very end', 'サーヴァントが最後まであなたの前に立ちはだかった', '从者终究挡在了你的面前')),
 ('kg_p', E, 0, "S.flags.kgEnd==='p'", ('잔을 내려놓은 손', 'The Hand That Set Down the Cup', '杯を置いた手', '放下杯子的手'),
  ('나흘 사이에 잔을 내려놓았다', 'Set down the cup within the four days', '四日のうちに杯を置いた', '在四天之内放下了杯子')),
 ('kg_x', E, 0, "S.flags.kgEnd==='x'", ('손을 놓친 잔', 'The Cup That Slipped Away', '手を離れた杯', '脱手之杯'),
  ('잔을 막으러 온 동맹에게 서번트를 잃었다', 'Lost your Servant to the ally who came to stop the cup', '杯を止めに来た同盟に、サーヴァントを失った', '在前来阻止杯的同盟面前失去了从者')),
]
EN_IN = {'avenger': ('나를 짓밟은 모든 것에', 'To Everything That Trampled Me', '私を踏みにじったすべてに', '致所有践踏过我的一切'),
         'judge': ('누구도 거역할 수 없는', 'That No One Can Defy', '誰も逆らえない', '无人能违抗'),
         'cruel': ('약한 것이 없는 세상', 'A World with Nothing Weak', '弱いもののいない世界', '没有弱者的世界'),
         'taboo': ('문 너머를 이쪽으로', 'Beyond the Door, onto This Side', '扉の向こうをこちらへ', '将门的彼方引向这一侧'),
         'zeal': ('도시 전부를 디딤돌로', 'The Whole City as a Stepping Stone', '街のすべてを踏み台に', '以整座城市为垫脚石')}
EN_M = {'avenger': ('지워진 명단', 'The Erased List', '消された名簿', '被抹去的名单'),
        'judge': ('같은 시각, 같은 말', 'Same Hour, Same Words', '同じ時刻、同じ言葉', '同一时刻，同一句话'),
        'cruel': ('불 꺼진 병원', 'The Darkened Hospital', '灯の消えた病院', '熄了灯的医院'),
        'taboo': ('비치지 않는 거울', 'The Mirror That Shows No One', '誰も映らない鏡', '照不出人的镜子'),
        'zeal': ('잠든 도시', 'The Sleeping City', '眠る街', '沉睡的城市')}
for k, t in TN.items():
    A.append(('kg_in_' + k, E, 0, "S.flags.kg==='%s'" % k, EN_IN[k],
              ('「%s」의 본성 속 진심을 잔에 맡겼다' % t[0], 'Entrusted your truth of “%s” to the cup' % t[1], '「%s」の本性に潜む本心を杯に託した' % t[2], '将「%s」的本性深处的真心托付给了杯' % t[3])))
for k, t in TN.items():
    A.append(('kg_m_' + k, E, 0, "S.flags.kgEnd==='m'&&S.flags.kg==='%s'" % k, EN_M[k],
              ('서번트를 꺾고 「%s」의 진심을 이루었다' % t[0], 'Defeated your Servant and fulfilled your truth of “%s”' % t[1], 'サーヴァントを打ち破り、「%s」の本心を叶えた' % t[2], '击败从者，实现了「%s」的真心' % t[3])))
A += [
 ('kg_stop', '싸움', 0, "!!S.flags.kgStop", ('알고 있었다', 'I Knew', '知っていた', '我早就知道'),
  ('어긋남을 알아채고, 등 뒤의 칼을 령주로 멈춰 세웠다', 'Noticed what was off, and stopped the knife in your back with a Command Spell', '違和感に気づき、背中の刃を令呪で止めた', '察觉到了异样，用令咒止住了背后之刃')),
 ('kg_free', '삶', 0, "!!S.flags.kgFree", ('놓아준 해', 'The Year You Let Go', '手放した年', '放手的那一年'),
  ('묶인 잔의 서번트를 남은 령주로 놓아주었다', 'Released the Servant of the Bound Cup with your remaining Command Spell', '縛られた杯のサーヴァントを、残った令呪で解き放った', '用剩下的令咒放走了被束缚之杯的从者')),
 ('kg_f', '숨겨진 업적', 1, "S.flags.kgEnd==='f'", ('그 사람인 채로', 'As the Person You Were', 'その人のままで', '就这样作为那个人'),
  ('곁에 서 있던 서번트가 당신의 끝을 정했다', 'The Servant at your side decided your end', '隣に立っていたサーヴァントが、あなたの終わりを決めた', '站在身旁的从者决定了你的结局')),
 ('kg_knew', '숨겨진 업적', 1, "!!S.flags.kgKnew", ('알면서 둔 칼', 'The Blade You Knew Of', '知りながら受けた刃', '明知而受的刃'),
  ('등 뒤의 칼을 알면서 받아들였다', 'Knew of the knife in your back, and accepted it', '背中の刃を知りながら受け入れた', '明知背后之刃，仍接受了它')),
 ('kg_calm', '숨겨진 업적', 1, "!!S.flags.kgOff", ('고요해진 잔', 'The Quieted Cup', '静まった杯', '平静下来的杯'),
  ('나흘 사이 본성이 옅어져, 잔이 가득 찼을 때 진심이 사라져 있었다', 'Your nature faded over the four days; when the cup filled, the truth was gone', '四日のあいだに本性が薄れ、杯が満ちたとき本心は消えていた', '四天里本性渐渐淡去，杯满之时，真心已不在')),
]
META = ('kg7', '기록', ('일곱 갈래의 밤', 'Night of Seven Paths', '七つに分かれた夜', '七条岔路之夜'),
        ('본성 속 진심의 결말 일곱을 모두 보았다', 'Saw all seven endings of the truth beneath your nature', '本性に潜む本心の七つの結末をすべて見た', '见证了本性深处的真心的全部七种结局'))
assert len(A) == 22
# 업적 목록 맨 끝에
lines = []
for i, c, h, t, n, d in A:
    lines.append("    {id:'%s',cat:'%s',%sn:'%s',d:'%s',t:()=>%s}," % (i, c, "h:1," if h else "", n[0], d[0], t))
lines.append("    {id:'%s',cat:'%s',n:'%s',d:'%s',meta:1}," % (META[0], META[1], META[2][0], META[3][0]))
rp("t:()=>!!S.flags.relLate},\n  ];", "t:()=>!!S.flags.relLate},\n" + "\n".join(lines) + "   // 11-22 본성 속 진심 (kgach_apply)\n  ];")
# 기록 남기기
rp("{t:'령주로 멈춰라',seal:true,d:`칼이 닿기 전에 멈춰 세운다 [령주 1획 · 남은 ${w.seals}획]`,f:()=>{ useSeal(",
   "{t:'령주로 멈춰라',seal:true,d:`칼이 닿기 전에 멈춰 세운다 [령주 1획 · 남은 ${w.seals}획]`,f:()=>{ S.flags.kgStop=1; useSeal(")
rp("function kgFallBack(knew){ const w=W(), g=w.kg, h=hero(); kgClose(); g.end='f'; S.flags.kgEnd='f';",
   "function kgFallBack(knew){ const w=W(), g=w.kg, h=hero(); kgClose(); g.end='f'; S.flags.kgEnd='f'; if(knew) S.flags.kgKnew=1;")
# 여러 생: 결말 키 모으기 · 일곱 갈래
rp("  for(const id of r.rel||[]) if(Sim.H_BY[id]) dexHero(c,id).rh=1;",
   "  for(const id of r.rel||[]) if(Sim.H_BY[id]) dexHero(c,id).rh=1;\n  if(r.kg){ c.kgE=c.kgE||{}; c.kgE[r.kg]=1; }   // 본성 속 진심의 결말 (kgach_apply)")
rp("  if(relTopCount(c)>=10) add('rel10');\n  return out; }",
   "  if(relTopCount(c)>=10) add('rel10');\n"
   "  if(!c.kgE){ c.kgE={}; (store.get(K_HIST)||[]).forEach(r=>{ if(r&&r.kg) c.kgE[r.kg]=1; }); }\n"
   "  if(['m','t','b','s','f','p','x'].every(k=>c.kgE[k])) add('kg7');\n  return out; }")
rp("rel10:`${Math.min(10,relTopCount(c))}/10`};", "rel10:`${Math.min(10,relTopCount(c))}/10`,kg7:`${['m','t','b','s','f','p','x'].filter(k=>(c.kgE||{})[k]).length}/7`};")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
allT = [(a[4][0], a[4][1], a[4][2], a[4][3]) for a in A] + [(a[5][0], a[5][1], a[5][2], a[5][3]) for a in A] + [META[2], META[3]]
# 이미 게임에 있는 이름(결말 이름표)은 사전에 이미 있으니 i18n.add가 건너뛴다
s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, _ in allT])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(D0, 'zh', 'done.json'); Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _, _, z in allT:
    if a not in Z:
        if CC is None: raise SystemExit('OpenCC 없음')
        Z[a] = [z, CC.convert(z).replace('“', '「').replace('”', '」').replace('聖盃', '聖杯')]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('kgach 적용 · 업적', len(A) + 1, '· 사전', nd, '· 중국어', n)
