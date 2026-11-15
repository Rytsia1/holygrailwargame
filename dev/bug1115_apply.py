"""11-15 커뮤니티 버그 제보 반영 (노션 「커뮤니티 버그 제보」의 신규 9건)
① 직장 연락: 「직장 동료가 묻는」 낮 사건이 날마다 되풀이되던 것 → 전쟁에서 한 번. 회사원만(떠돌며 연구하는 사람에게는 상사·동료가 없다).
   며칠 쉬겠다고 했거나 휴가를 냈으면 「직장의 전화」도 오지 않는다.
② 「놀이터의 아이」: 여성 마스터에게는 "아줌마".
③ 「강연 의뢰」: 수육한 서번트가 곁에 있으면 / 소환하지 않았으면 결과 문장이 다르다.
④ 서번트와의 아이 「마술 각인」: 각인을 실제로 받은 사람에게만(고아·각성만 한 사람에게 본가의 편지가 오던 것).
⑤ 「형제」 동맹 거절: 형제가 각인을 받았으면 / 아무도 받지 않았으면 대사가 다르다.
⑥ 결과 화면 령주: 남은 획을 '3 − 쓴 획'이 아니라 전쟁이 끝날 때 실제로 남은 획으로(사건으로 더 받은 령주 반영).
⑦ 에필로그 「검은 옷의 대행자」: 교회 출신 · 교회와 인연을 맺은 사람 · 감독관은 '쓰러뜨린 마스터의 가문이 낸 진정'만으로는 오지 않는다.
⑧ 전투 중 대화로 상대가 무기를 거두면 그날 밤 행동이 끝난다(습격 · 밤 사건이 이어지지 않는다). 다시 붙어 응급 치유를 또 쓰던 것.
⑨ 마의 피 · 과거시의 마안: 전투 행동이 없는 마안은 상태 패널에 늘 켜져 있는 효과를 한 줄로 보여 준다.
사용: python3 bug1115_apply.py <game.html>"""
import sys, i18n
D = [
    ('아이는 편의점 도시락을 같이 먹고 갔다. 헤어질 때 말했다. “아줌마는 나중에 이길게요.”',
     'The child shared a convenience store bento with you and then left. As you parted, they said, “I\'ll beat you later, ma\'am.”',
     '子どもはコンビニ弁当を一緒に食べて帰っていった。別れ際に言った。「おばさんには後で勝つからね」'),
    ('아줌마는 나중에 이길게요.', 'I\'ll beat you later, ma\'am.', 'おばさんには後で勝つからね'),
    ('강의실 맨 앞줄의 학생이 질문했다. “서번트를 만나 본 적이 있으세요?” 고개를 저었다. 그 겨울, 당신은 끝내 아무도 부르지 않았다.',
     'A student in the front row asked, “Have you ever met a Servant?” You shook your head. That winter, you never called anyone.',
     '講義室の最前列の学生が質問した。「サーヴァントに会ったことはありますか？」首を横に振った。あの冬、あなたは結局誰も呼ばなかった。'),
    ('강의실 맨 앞줄의 학생이 질문했다. “서번트를 만나 본 적이 있으세요?” 고개를 저었다. 책으로만 아는 전쟁을 두 시간 동안 이야기했다.',
     'A student in the front row asked, “Have you ever met a Servant?” You shook your head, and spent two hours talking about a war you knew only from books.',
     '講義室の最前列の学生が質問した。「サーヴァントに会ったことはありますか？」首を横に振った。本でしか知らない戦争について、二時間話した。'),
    ('“각인을 받은 건 나야. 이번만큼은 내가 끝까지 가야 해.” 형제는 돌아섰다.',
     '“I\'m the one who received the Crest. This time, I have to see it through.” Your sibling turned away.',
     '「刻印を受け継いだのは俺だ。今度ばかりは最後まで行かなきゃならない」兄弟は背を向けた。'),
    ('“너랑 손잡으면 끝에 가서 더 힘들어져.” 형제는 돌아섰다.',
     '“If we join hands now, the end will only be harder.” Your sibling turned away.',
     '「お前と手を組んだら、最後がもっとつらくなる」兄弟は背を向けた。'),
    ('마스터끼리 맞붙을 때 「정면으로 덤빈다」 · 「몸을 숨긴다」 · 「허를 찌른다」가 강해진다',
     'Strengthens “Charge head-on” · “Go into hiding” · “Catch them off guard” when Masters clash',
     'マスター同士の対決で「正面から飛びかかる」・「身を隠す」・「虚を突く」が強くなる'),
    ('전투에 들어서면 상대 조가 걸어온 길을 읽는다',
     'When a battle begins, you read the path the enemy team has walked',
     '戦闘に入ると、相手陣営が歩んできた道を読み取る'),
]
T = [
    ('동맹 {0} 조가 {1} 조에게 습격당했다는 소식은 새벽에야 들었다.',
     'You only heard at dawn that your ally, the {0} team, had been attacked by the {1} team.',
     '同盟の{0}陣営が{1}陣営に襲われたという知らせは、明け方になってようやく届いた。'),
    ('강의실 맨 뒷줄에 {0~이} 앉아 있었다. 질문 시간에 한 학생이 “서번트는 전쟁이 끝나면 어디로 가나요?”라고 물었다. 대답하는 동안 웃음을 참기 어려웠다.',
     '{0} was sitting in the back row of the lecture hall. During questions, a student asked, “Where do Servants go when the war ends?” It was hard not to laugh while you answered.',
     '講義室の最後列に{0}が座っていた。質問の時間、ある学生が「サーヴァントは戦争が終わるとどこへ行くんですか？」と尋ねた。答える間、笑いをこらえるのが大変だった。'),
]
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # ① 직장 연락
    rp("{w:3,c:()=>S.flags.job==='회사'||S.flags.job==='연구',f:()=>decide({title:'낮',body:'직장 동료가 요즘 무슨 일 있느냐고 물었다. 눈 밑이 검다고 했다.',war:true,choices:[",
       "{w:3,c:()=>S.flags.job==='회사'&&!W().ctCowork&&!W().leave,f:()=>{ W().ctCowork=true; decide({title:'낮',body:'직장 동료가 요즘 무슨 일 있느냐고 물었다. 눈 밑이 검다고 했다.',war:true,choices:[")
    rp("{t:'며칠 쉬겠다고 한다',f:()=>{add({wealth:-3,health:3});return '휴가를 냈다. 책상 위 화분에 물 줄 사람을 부탁했다.'}}]})},",
       "{t:'며칠 쉬겠다고 한다',f:()=>{add({wealth:-3,health:3});W().leave=true;return '휴가를 냈다. 책상 위 화분에 물 줄 사람을 부탁했다.'}}]}); }},")
    rp("{w:2,c:()=>!!S.flags.job&&S.flags.job!=='가문'&&!W().ctWork,f:()=>{const w=W();w.ctWork=true;decide({title:'직장의 전화',",
       "{w:2,c:()=>S.flags.job==='회사'&&!W().ctWork&&!W().leave,f:()=>{const w=W();w.ctWork=true;decide({title:'직장의 전화',")
    rp("{t:'휴가를 낸다',d:'재산 −',auto:true,f:()=>{add({wealth:-4});return '2주 휴가를 냈다. 상사는 한숨을 쉬었다.'}},",
       "{t:'휴가를 낸다',d:'재산 −',auto:true,f:()=>{add({wealth:-4});W().leave=true;return '2주 휴가를 냈다. 상사는 한숨을 쉬었다.'}},")
    # ② 놀이터의 아이
    rp("헤어질 때 말했다. “아저씨는 나중에 이길게요.”`}",
       "헤어질 때 말했다. “${S.sex==='f'?'아줌마':'아저씨'}는 나중에 이길게요.”`}")
    # ③ 강연 의뢰
    rp("{t:'맡는다',f:()=>{add({wealth:8,lore:2,will:-1});return '강의실 맨 앞줄의 학생이 질문했다. “서번트를 다시 만나고 싶으세요?” 대답하지 못했다.'}},",
       "{t:'맡는다',f:()=>{add({wealth:8,lore:2,will:-1});"
       "if(S.hero&&stayHome()){ const h=H_BY[S.hero]; return `강의실 맨 뒷줄에 ${h.name}${J(h.name,이)} 앉아 있었다. 질문 시간에 한 학생이 “서번트는 전쟁이 끝나면 어디로 가나요?”라고 물었다. 대답하는 동안 웃음을 참기 어려웠다.`; }"
       "if(!S.hero) return S.flags.war==='refused'||S.war?'강의실 맨 앞줄의 학생이 질문했다. “서번트를 만나 본 적이 있으세요?” 고개를 저었다. 그 겨울, 당신은 끝내 아무도 부르지 않았다.':'강의실 맨 앞줄의 학생이 질문했다. “서번트를 만나 본 적이 있으세요?” 고개를 저었다. 책으로만 아는 전쟁을 두 시간 동안 이야기했다.';"
       "return '강의실 맨 앞줄의 학생이 질문했다. “서번트를 다시 만나고 싶으세요?” 대답하지 못했다.'}},")
    # ④ 아이에게 마술 각인
    rp("{id:'lv_crest',w:2,c:()=>stayHome()&&!!relKid()&&relKid().age>=10&&isMage(),",
       "{id:'lv_crest',w:2,c:()=>stayHome()&&!!relKid()&&relKid().age>=10&&isMage()&&!!S.flags.crest,")
    # ⑤ 형제 동맹 거절
    rp("addIntel(p,40);return '“그럴 거면 처음부터 각인을 양보했어야지.” 형제는 돌아섰다.'}},",
       "addIntel(p,40);return S.flags.sibHeir?'“각인을 받은 건 나야. 이번만큼은 내가 끝까지 가야 해.” 형제는 돌아섰다.':S.flags.crest?'“그럴 거면 처음부터 각인을 양보했어야지.” 형제는 돌아섰다.':'“너랑 손잡으면 끝에 가서 더 힘들어져.” 형제는 돌아섰다.'}},")
    # ⑥ 결과 화면의 남은 령주
    rp("seals:w.sealLog||[], np:", "seals:w.sealLog||[], sealsLeft:Math.max(0,w.seals||0), np:")
    rp("const used=wd.seals.length;",
       "const used=wd.seals.length, left=wd.sealsLeft!=null?wd.sealsLeft:Math.max(0,3-used); // 사건으로 더 받은 령주도 센다")
    rp("const sealDots=[0,1,2].map(i=>`<i class=\"${i<used?'used':''}\"></i>`).join('');",
       "const sealDots=Array.from({length:Math.max(3,used+left)},(_,i)=>`<i class=\"${i<used?'used':''}\"></i>`).join('');")
    rp("${used}획 사용 · ${3-used}획 남음", "${used}획 사용 · ${left}획 남음")
    rp("seals:Math.max(0,3-((wd.seals||[]).length)),",
       "seals:Math.min(3,wd.sealsLeft!=null?wd.sealsLeft:Math.max(0,3-((wd.seals||[]).length))),")
    # ⑦ 교회 사람에게는 '가문의 진정'만으로 대행자가 오지 않는다
    rp("c:()=>!!(S.flags.civ||S.flags.killedMaster||S.flags.cupDisaster||S.flags.churchOwe)",
       "c:()=>!!(S.flags.civ||(S.flags.killedMaster&&!(S.origin==='church'||S.flags.churchTie||S.flags.overseer))||S.flags.cupDisaster||S.flags.churchOwe)")
    rp(":S.flags.killedMaster?'검은 옷의 남자가",
       ":S.flags.killedMaster&&!(S.origin==='church'||S.flags.churchTie||S.flags.overseer)?'검은 옷의 남자가")
    # ⑧ 대화로 끝난 밤
    rp("      b.res='talk'; return endBattle(); }",
       "      if(w.tod==='밤') w.quietN=w.day; // 말로 끝난 밤: 그날 밤 행동은 여기서 끝난다(습격 · 밤 사건 없음)\n      b.res='talk'; return endBattle(); }")
    rp("  function threat(){\n    const w=W(); if(w.ended||!w.heroAlive||S.pending) return;",
       "  function threat(){\n    const w=W(); if(w.ended||!w.heroAlive||S.pending) return; if(w.quietN===w.day) return;")
    rp("  function warEvent(){\n    const w=W(); if(w.ended||!w.heroAlive||S.pending||S.dead) return;",
       "  function warEvent(){\n    const w=W(); if(w.ended||!w.heroAlive||S.pending||S.dead) return; if(w.quietN===w.day) return;")
    # 최후의 결전은 말로 멈출 수 없다(멈춰도 곧바로 다시 붙어, 응급 치유를 새로 쓰며 이기던 것)
    rp("    if(ch(stop)){", "    if(!b.ctx.final&&ch(stop)){")
    # 말로 끝난 밤에는 동맹의 급한 연락에도 달려가지 않는다(그 싸움은 그들끼리 결판난다 · 외면으로 치지 않는다)
    rp("    const a=pairBy(r.a), b=pairBy(r.b); if(!a||!b||!a.alive||!b.alive||!b.ally||!a.master) return;",
       "    const a=pairBy(r.a), b=pairBy(r.b); if(!a||!b||!a.alive||!b.alive||!b.ally||!a.master) return;\n"
       "    if(w.quietN===w.day){ log(`동맹 ${pName(b)} 조가 ${pName(a)} 조에게 습격당했다는 소식은 새벽에야 들었다.`,'war'); allyRaidFight(a,b); return; }")
    # ⑨ 전투 행동이 없는 마안의 효과
    rp("return {n:GIFTS[g.id].n,gr:GRADE_N[g.gr],ctl:['제어 못 함','제어 보통','제어 능숙'][g.ctl||0]}; }",
       "return {n:GIFTS[g.id].n,gr:GRADE_N[g.gr],ctl:['제어 못 함','제어 보통','제어 능숙'][g.ctl||0],"
       "fx:{blood:'마스터끼리 맞붙을 때 「정면으로 덤빈다」 · 「몸을 숨긴다」 · 「허를 찌른다」가 강해진다',past:'전투에 들어서면 상대 조가 걸어온 길을 읽는다'}[g.id]||''}; }")
    rp("if(g) ar.push(`<div>${esc(g.n)} <b>${esc(g.gr)} · ${esc(g.ctl)}</b></div>`); }",
       "if(g){ ar.push(`<div>${esc(g.n)} <b>${esc(g.gr)} · ${esc(g.ctl)}</b></div>`); if(g.fx) ar.push(`<div class=\"gfx\">${esc(g.fx)}</div>`); } }")
    rp("</style>", "#arts .gfx{font-size:12px;line-height:1.45;color:#a39c8a;margin-top:-1px}\n</style>")
    s, nd, nt = i18n.add(s, D, T)
    print('bug1115 miss', miss, 'tr', nd, nt)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
