"""11-20: 전쟁 중에도 궁합이 조금씩 바뀐다
- 소환 때 정한 궁합을 기본 점수(능력치 몫, 그대로)와 성향 보정(마스터 성향 몫)으로 나눠 기억한다
- 마스터 성향이 기준선(잔혹 · 금기 · 근원 집착 4, 정의 · 복수 3)을 넘거나 내려올 때만 성향 보정을 다시 계산한다
- 처음 궁합에서 +10까지, 아래로는 관계 단계에 따라 −10 / −7 / −4 / 0까지
- 점수가 바뀌면 칩 한 줄, 등급이 바뀌면 서번트 문장 한 줄
- 재계약한 서번트는 궁합 60에서 같은 규칙으로. 이 패치 전에 시작한 전쟁은 바뀌지 않는다
사용: python3 fitlive_apply.py <game.html>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'function fitLive(' in s: print('이미 적용됨'); sys.exit(0)
miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)

rp("""    if(S.aff[k]>=8&&!S.once['lean2_'+k]){ S.once['lean2_'+k]=1; log(AFFL[k][1],'sys'); }
  }""",
   """    if(S.aff[k]>=8&&!S.once['lean2_'+k]){ S.once['lean2_'+k]=1; log(AFFL[k][1],'sys'); }
    fitLive(k,S.aff[k]-n,S.aff[k]);
  }
  // 11-20: 전쟁 중 궁합 — 소환 때의 기본 점수는 그대로, 성향 보정만 기준선을 넘나들 때 다시 계산한다
  // 처음 궁합에서 위로 +10, 아래로는 관계 단계(0~3)에 따라 −10 · −7 · −4 · 0까지
  const FIT_TH={cruel:4,taboo:4,zeal:4,judge:3,avenger:3}, FIT_LO=[10,7,4,0];
  function fitLive(k,b,a){ const w=S.war; if(!w||S.phase!=='war'||!w.heroAlive||w.ended||w.fitB==null||!(k in FIT_TH)) return;
    const th=FIT_TH[k]; if((b>=th)===(a>=th)) return; const h=hero(); if(!h) return;
    const f0=w.fit0??60, of=w.fit??60, nf=Math.max(f0-FIT_LO[fitRel()],Math.min(f0+10,fitScore(h,w.fitB)));
    if(nf===of) return; const t0=fitTier(w); w.fit=nf; const t1=fitTier(w);
    if(CHK) CHK.push(nf>of?{txt:'궁합이 조금 가까워졌다',ok:true}:{txt:'궁합이 조금 멀어졌다',ok:false});
    if(t0!==t1){ const n=h.name; log(nf>of?`${n}${J(n,이)} 당신 쪽으로 반걸음 다가섰다. 궁합 ‘${t0} → ${t1}’.`:`${n}${J(n,이)} 당신을 보는 눈이 달라졌다. 궁합 ‘${t0} → ${t1}’.`,'voice'); } }""")
# 소환: 기본 점수(fitB)와 처음 궁합(fit0)을 함께 기억
rp("S.war={fit:fitScore(h,match),", "S.war={fit:fitScore(h,match),fitB:match,fit0:fitScore(h,match),")
# 재계약: 궁합 60에서 출발. 지금 성향 보정을 뺀 값을 기본 점수로
rp("w.trust=40; w.fit=60; w.frag=0;", "w.trust=40; w.fit=60; w.fit0=60; w.fitB=60-fitScore(H_BY[e.hero],0); w.frag=0;")

if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)

D = [
    ("궁합이 조금 가까워졌다", "Your compatibility grew a little closer", "相性が少し近づいた", "契合度稍微拉近了", "契合度稍微拉近了"),
    ("궁합이 조금 멀어졌다", "Your compatibility drifted a little apart", "相性が少し離れた", "契合度稍微疏远了", "契合度稍微疏遠了"),
]
T = [
    ("{0~이} 당신 쪽으로 반걸음 다가섰다. 궁합 ‘어긋남 → 보통’.", "{0} took half a step toward you. Compatibility: ‘Poor → Neutral’.", "{0}があなたの方へ半歩近づいた。相性「悪い → 普通」。", "{0}朝你靠近了半步。契合度「不合 → 普通」。", "{0}朝你靠近了半步。契合度「不合 → 普通」。"),
    ("{0~이} 당신 쪽으로 반걸음 다가섰다. 궁합 ‘보통 → 잘 맞음’.", "{0} took half a step toward you. Compatibility: ‘Neutral → Good’.", "{0}があなたの方へ半歩近づいた。相性「普通 → 良い」。", "{0}朝你靠近了半步。契合度「普通 → 契合」。", "{0}朝你靠近了半步。契合度「普通 → 契合」。"),
    ("{0~이} 당신을 보는 눈이 달라졌다. 궁합 ‘잘 맞음 → 보통’.", "{0} looks at you differently now. Compatibility: ‘Good → Neutral’.", "{0}があなたを見る目が変わった。相性「良い → 普通」。", "{0}看你的眼神变了。契合度「契合 → 普通」。", "{0}看你的眼神變了。契合度「契合 → 普通」。"),
    ("{0~이} 당신을 보는 눈이 달라졌다. 궁합 ‘보통 → 어긋남’.", "{0} looks at you differently now. Compatibility: ‘Neutral → Poor’.", "{0}があなたを見る目が変わった。相性「普通 → 悪い」。", "{0}看你的眼神变了。契合度「普通 → 不合」。", "{0}看你的眼神變了。契合度「普通 → 不合」。"),
]
s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, *_ in D], [(a, b, c) for a, b, c, *_ in T])
open(P, 'w', encoding='utf-8').write(s)
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
Z = json.load(open(zp, encoding='utf-8')); n = 0
for a, _b, _c, d, e in D + T:
    if a not in Z: Z[a] = [d, e]; n += 1
json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('적용 끝 · 사전', nd, '· 틀', nt, '· 중국어', n)
