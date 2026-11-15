"""인연 갈래 고르기 (11-15)
- 인연 1단계 장면 「처음 부른 이름」에서 애정 · 우정을 고른다. 성별과 상관없이 모두에게 묻고, 엘키두(성별 없음)도 애정을 고를 수 있다.
- 자동 결정은 예전 규칙을 따른다: 이성이면 애정, 같은 성별 · 성별 없음이면 우정.
- 고르지 않고 우정으로 바로 가는 경우는 그대로: 미성년 마스터 · 아이 서번트 · 연인 불가 서번트 · 배우자가 살아 있는 마스터.
  이 우정 이유(미성년 · 배우자)는 이제 성별과 상관없이 붙어서, 에필로그의 애정 전환 장면도 같은 성별 · 엘키두에게 열린다.
- 1단계 전 서번트 카드: 다음 「호감 · 전우」.
- 대사 두 줄: 길가메시 3단계 '왕비의 자리' → '왕좌 옆자리' (한·영·일) · 슈텐도지 아침 일본어 「旦那はん」 → 「主はん」
- 서번트와의 아이: 같은 성별 · 성별 없음이면 「아이를 갖는다」가 빠지고 입양 · 둘로 충분하다만 남는다.
사용: python3 relpick_apply.py <game.html>"""
import sys, i18n
Q = '그 목소리에 어떤 마음으로 대답할지, 당신은 잠깐 망설였다.'
D = [
    (Q, 'You hesitated for a moment, unsure what feeling to answer that voice with.', 'その声にどんな気持ちで応えるか、あなたは少し迷った。'),
    ('마음을 담아 이름으로 대답한다', 'Answer with their name, heart and all', '想いを込めて名前で応える'),
    ('등을 맡기듯 이름으로 대답한다', 'Answer with their name, as one who trusts them with your back', '背中を預けるように名前で応える'),
    ('인연이 애정으로 이어진다 · 호감 → 연모 → 연인', 'Your bond grows into affection · Fondness → Yearning → Lovers', '縁が愛情へとつながる · 好意 → 恋慕 → 恋人'),
    ('인연이 우정으로 이어진다 · 전우 → 절친 → 지기', 'Your bond grows into friendship · Comrades → Close Friends → Sworn Friends', '縁が友情へとつながる · 戦友 → 親友 → 無二の友'),
    ('호감 · 전우', 'Fondness · Comrades', '好意 · 戦友'),
]
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # 고를 수 있는지 · 우정 이유(성별과 상관없이)
    rp("  function relWhy(h){\n    if(!h||!S.sex||h.sex==='x'||h.sex===S.sex) return null;",
       "  const relSame=h=>!h||!S.sex||h.sex==='x'||h.sex===S.sex;   // 같은 성별 · 성별 없음(엘키두)\n"
       "  const relCanPick=h=>!!h&&!!S.sex&&!relWhy(h);   // 인연 1단계에서 애정 · 우정을 고를 수 있다\n"
       "  function relWhy(h){\n    if(!h||!S.sex) return null;")
    rp("w.rel={h:S.hero,track:relTrack(h),stage:0,pt:0,open:0}; w.rel.why=w.rel.track==='friend'?relWhy(h):null; }",
       "w.rel={h:S.hero,track:relTrack(h),stage:0,pt:0,open:0}; w.rel.why=w.rel.track==='friend'?relWhy(h):null; w.rel.pick=relCanPick(h)?1:0; }\n"
       "    if(w.rel.pick===undefined) w.rel.pick=!w.rel.stage&&relCanPick(H_BY[S.hero])?1:0; // 예전 세이브: 아직 1단계 전이면 고를 수 있다")
    # 인연 1단계 장면: 고르기
    rp("    const u=rluQ(h,rlu(h,'s'+st));",
       "    if(st===1&&r.pick){ relPick(r,h,m,war); H.change(); return; }\n    const u=rluQ(h,rlu(h,'s'+st));")
    rp("  function relTry(){",
       "  function relPick(r,h,m,war){ const L=RLX.sc.love[1], F=RLX.sc.friend[1], def=relTrack(h);\n"
       "    const body=m?[rlp(h,F.bm),'" + Q + "'].join(' '):[rlp(h,L.b[war?0:1]),'" + Q + "'].join(' ');\n"
       "    const go=tr=>{ r.track=tr; r.pick=0; r.why=null; const sc=tr==='love'?L:F, u=rluQ(h,rlu(h,'s1',tr)); relStageUp(r,1,h); return [rlp(h,sc.c[0].r),u].filter(Boolean).join(' '); };\n"
       "    decide({title:L.t,body,war,choices:[\n"
       "      {t:'마음을 담아 이름으로 대답한다',d:'인연이 애정으로 이어진다 · 호감 → 연모 → 연인',auto:def==='love',f:()=>go('love')},\n"
       "      {t:'등을 맡기듯 이름으로 대답한다',d:'인연이 우정으로 이어진다 · 전우 → 절친 → 지기',auto:def!=='love',f:()=>go('friend')}]}); }\n"
       "  function relTry(){")
    # 서번트 카드: 1단계 전에는 두 갈래를 함께 적는다
    rp("next:r.stage<3?{n:REL_ST[r.track][r.stage+1],",
       "pick:!!(r.pick&&!r.stage),next:r.stage<3?{n:r.pick&&!r.stage?'호감 · 전우':REL_ST[r.track][r.stage+1],")
    # 서번트와의 아이: 같은 성별 · 성별 없음이면 낳는 선택지가 빠진다
    rp("{ let nm=null; const late=femAge()>45;",
       "{ let nm=null; const late=femAge()>45||relSame(H_BY[S.hero]);")
    # 마스터의 성별을 전제한 대사 두 줄(같은 성별 애정이 열리며 어긋나게 된 것)
    rp("왕비의 자리는 주지 않는다.", "왕좌 옆자리는 주지 않는다.", 3)   # 길가메시 3단계 · 대사와 번역 틀 두 곳
    rp("I will not give you a queen's throne.", "I will not give you the seat beside my throne.")
    rp("王妃の座はやらぬ。", "玉座の隣の座はやらぬ。")
    rp("おはよう、旦那はん。", "おはよう、主はん。")   # 슈텐도지 아침(일본어만)
    # 도감의 '연인이 될 수 없는 서번트' 표시: 엘키두도 이제 애정을 고를 수 있다
    rp("relLoveOk:id=>!REL_CHILD.includes(id)&&!REL_NOLOVE.includes(id)&&!!H_BY[id]&&H_BY[id].sex!=='x',",
       "relLoveOk:id=>!REL_CHILD.includes(id)&&!REL_NOLOVE.includes(id)&&!!H_BY[id],")
    s, nd, nt = i18n.add(s, D, [])
    print('relpick miss', miss, 'tr', nd, nt)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
