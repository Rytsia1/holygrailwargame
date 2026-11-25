"""Emergent Narrative Generator patch script (narr1125).
Usage: python3 narr_apply.py <game.html>
"""
import sys, os, json, re, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'narr1125' in s:
    print('이미 적용됨')
    sys.exit(0)

miss = []
def rp(o, n):
    global s
    k = s.count(o)
    if k != 1:
        miss.append((o[:90], k))
        return
    s = s.replace(o, n)

# 1. Sim: Fact Ledger, Story Beats, Causal Arc Detector & Multilingual Chronicle Generator
NARR_CORE = r"""
  /* ---------- 창발적 서사 생성기 (narr1125) ---------- */
  function pairSnap(p){
    if(!p) return null;
    if(p === 'me') return { id:'me', name:S.name, cls:S.hero?CLS[S.hero].n:'', hero:S.hero&&H_BY[S.hero]?H_BY[S.hero].name:'' };
    const h = p.hero && H_BY[p.hero];
    return { id:'p'+p.i, i:p.i, name:p.mname||'', cls:p.cls&&CLS[p.cls]?CLS[p.cls].n:'', hero:h?h.name:'', revealed:!!p.revealed, known:!!p.known };
  }
  function narrName(sn, trFn, isServ){
    if(!sn) return '';
    if(sn.id === 'me'){ return isServ ? trFn(sn.hero || sn.cls) : trFn(sn.name); }
    const c = trFn(sn.cls || '???');
    if(isServ) return sn.revealed && sn.hero ? `${trFn(sn.hero)} (${c})` : c;
    return sn.name ? `${trFn(sn.name)} (${c})` : c;
  }
  function recFact(type, data = {}){
    const w = W(); if(!w) return null;
    w.facts = w.facts || [];
    if(w.facts.length >= 120) return null;
    const f = {
      id: (w.factSeq = (w.factSeq || 0) + 1),
      d: w.day || 0,
      tod: w.tod || '낮',
      type,
      actor: data.actor || null,
      target: data.target || null,
      who: data.who || null,
      rel: data.rel ? { ...data.rel } : null,
      persona: data.persona || null,
      causeId: data.causeId || null,
      meta: data.meta || null,
    };
    w.facts.push(f);
    if(data.beat){
      const koTxt = narrBeat(f, 'ko', x=>x);
      if(koTxt) log(koTxt, 'story', { fact: f });
    }
    return f;
  }
  function lastFactOf(types, pred){
    const w = W(); if(!w || !w.facts) return null;
    const ts = Array.isArray(types) ? types : [types];
    for(let i = w.facts.length - 1; i >= 0; i--){
      const f = w.facts[i];
      if(ts.includes(f.type) && (!pred || pred(f))) return f;
    }
    return null;
  }

  function narrBeat(f, lg='ko', trFn){
    if(!f) return '';
    const L = ['ko','en','ja','zhs','zht'].includes(lg) ? lg : 'ko';
    const T = trFn || (typeof tr === 'function' ? tr : x => x);
    const w = f.who || {};
    const aM = w.a ? narrName(w.a, T, false) : (w.aLabel ? T(w.aLabel) : '');
    const aS = w.a ? narrName(w.a, T, true) : '';
    const bM = w.b ? narrName(w.b, T, false) : (w.bLabel ? T(w.bLabel) : '');
    const bS = w.b ? narrName(w.b, T, true) : '';
    const m = f.meta || {};
    if(f.type === 'ally_betray' || f.type === 'ally_abandon'){
      const mid = f.type === 'ally_abandon';
      return {
        ko: mid ? `${aM}${J(aM,'은')} 가장 위험한 순간에 발을 빼며 동맹을 방패로 내던졌다.` : `${aM}${J(aM,'은')} 동맹의 약속을 깨고 칼끝을 돌렸다.`,
        en: mid ? `${aM} slipped away at the height of battle, leaving their ally as a shield.` : `${aM} broke the alliance and turned the blade against their partner.`,
        ja: mid ? `${aM}は戦いの最中に手を引き、同盟を盾にして姿を消した。` : `${aM}は同盟の誓いを破り、仲間へ刃を向けた。`,
        zhs: mid ? `${aM}在最凶险的时刻抽身而退，把同盟当成了盾牌。` : `${aM}撕毁了同盟之约，将刀锋转向了同伴。`,
        zht: mid ? `${aM}在最凶險的時刻抽身而退，把同盟當成了盾牌。` : `${aM}撕毀了同盟之約，將刀鋒轉向了同伴。`,
      }[L];
    }
    if(f.type === 'order_refuse'){
      const sv = w.a && w.a.id === 'me' ? T(w.a.hero || '') : aS;
      return {
        ko: `${sv}${J(sv,'은')} 물러서라는 명령을 꺾고 스스로 전장에 남았다.`,
        en: `${sv} defied the order to withdraw and stood their ground.`,
        ja: `${sv}は退却の命を退け、自ら戦場に踏みとどまった。`,
        zhs: `${sv}违抗了撤退的命令，独自留在了战场上。`,
        zht: `${sv}違抗了撤退的命令，獨自留在了戰場上。`,
      }[L];
    }
    if(f.type === 'enemy_coop'){
      return {
        ko: `서로 칼을 겨누던 ${aM} 조와 ${bM} 조가 공동의 위협 앞에서 손을 잡았다.`,
        en: `Former foes ${aM} and ${bM} set aside their blades to face a common threat.`,
        ja: `刃を交えていた${aM}と${bM}が、共通の脅威を前に手を組んだ。`,
        zhs: `曾兵戎相见的${aM}与${bM}在共同的威胁面前暂时联手。`,
        zht: `曾兵戎相見的${aM}與${bM}在共同的威脅面前暫時聯手。`,
      }[L];
    }
    if(f.type === 'stray_fight'){
      const rev = m.revenge;
      return {
        ko: rev ? `주인을 잃은 ${aS}${J(aS,'은')} 복수를 쫓아 ${bM} 조의 밤을 덮쳤다.` : `주인을 잃은 ${aS}${J(aS,'은')} 홀로 싸움을 이어 가며 ${bM} 조와 맞부딪쳤다.`,
        en: rev ? `Masterless ${aS} hunted down ${bM} in vengeance for their fallen Master.` : `Despite losing their Master, ${aS} fought on alone and clashed with ${bM}.`,
        ja: rev ? `主を失った${aS}は仇を追い、${bM}へ夜襲を仕掛けた。` : `主を失った${aS}はなお戦いを続け、${bM}と激突した。`,
        zhs: rev ? `失去御主的${aS}追寻复仇，夜袭了${bM}。` : `失去御主的${aS}依然独自继续战斗，与${bM}正面交锋。`,
        zht: rev ? `失去御主的${aS}追尋復仇，夜襲了${bM}。` : `失去御主的${aS}依然獨自繼續戰鬥，與${bM}正面交鋒。`,
      }[L];
    }
    if(f.type === 'servant_defect'){
      return {
        ko: `신뢰가 무너진 끝에서, ${aS}${J(aS,'은')} 옛 주인을 버리고 전장을 떠났다.`,
        en: `With trust shattered, ${aS} abandoned their Master and walked away from the contract.`,
        ja: `信頼が崩れ去った末に、${aS}は主を見限り契約を断ち切った。`,
        zhs: `在信任彻底崩塌之后，${aS}背弃了旧主，转身离去。`,
        zht: `在信任徹底崩塌之後，${aS}背棄了舊主，轉身離去。`,
      }[L];
    }
    return '';
  }

  function detectArcs(facts){
    const byId = new Map((facts || []).map(f => [f.id, f]));
    const arcs = [];
    const used = new Set();

    // 1) Pengkhianatan Aliansi (Betrayal)
    for(const f of facts){
      if(f.type !== 'ally_betray' && f.type !== 'ally_abandon') continue;
      const chain = [f.id];
      let cur = f.causeId ? byId.get(f.causeId) : null;
      const causeTypes = [];
      let guard = 0;
      while(cur && guard++ < 5){
        chain.unshift(cur.id);
        causeTypes.push(cur.type);
        cur = cur.causeId ? byId.get(cur.causeId) : null;
      }
      // Cari ally_form sebelumnya jika belum masuk chain
      const form = facts.find(x => x.type === 'ally_form' && x.d <= f.d && (x.actor === f.actor || x.target === f.actor) && !chain.includes(x.id));
      if(form) chain.unshift(form.id);
      const ignored = facts.find(x => x.type === 'ally_ignore' && x.d <= f.d && x.actor === f.actor);
      if(ignored && !chain.includes(ignored.id)) chain.push(ignored.id);
      const after = facts.find(x => (x.type === 'kill' || x.type === 'duel_clash') && x.d >= f.d && (x.actor === f.actor || x.target === f.actor));
      if(after && !chain.includes(after.id)) chain.push(after.id);
      chain.forEach(id => used.add(id));
      arcs.push({ kind:'betrayal', fact:f, form, ignored, after, factIds:chain });
    }

    // 2) Master Gugur, Servant Terus Bertarung (Masterless)
    for(const f of facts){
      if(f.type !== 'master_die_stray') continue;
      const fights = facts.filter(x => (x.type === 'stray_fight' || x.type === 'stray_recontract' || x.type === 'kill') && (x.causeId === f.id || (x.actor === f.actor && x.d >= f.d)));
      if(!fights.length) continue;
      const fids = [f.id, ...fights.map(x => x.id)];
      arcs.push({ kind:'masterless', fact:f, fights, factIds:fids });
    }

    // 3) Dua Musuh Terpaksa Bekerja Sama (Forced Cooperation)
    for(const f of facts){
      if(f.type !== 'enemy_coop') continue;
      const prior = f.causeId ? byId.get(f.causeId) : facts.find(x => x.type === 'duel_clash' && x.d <= f.d && ((x.actor === f.actor && x.target === f.target) || (x.actor === f.target && x.target === f.actor)));
      const fids = [prior ? prior.id : null, f.id].filter(Boolean);
      arcs.push({ kind:'enemy_coop', fact:f, prior, factIds:fids });
    }

    // 4) Servant Menolak Perintah / Membangkang (Defiance)
    const refuses = facts.filter(f => f.type === 'order_refuse' || f.type === 'servant_defect');
    if(refuses.length){
      const seals = facts.filter(f => f.type === 'seal_force' && f.d <= refuses[refuses.length - 1].d);
      const fids = [...seals.map(x => x.id), ...refuses.map(x => x.id)];
      arcs.push({ kind:'defiance', fact:refuses[0], refuses, seals, factIds:fids });
    }

    // 5) Kesetiaan Loyal Servant (Devotion)
    const prots = facts.filter(f => f.type === 'servant_protect');
    if(prots.length >= 1){
      arcs.push({ kind:'devotion', fact:prots[0], prots, factIds:prots.map(x => x.id) });
    }

    return arcs;
  }

  function renderNarrative(facts, ctx = {}, lg = 'ko', trFn){
    const L = ['ko','en','ja','zhs','zht'].includes(lg) ? lg : 'ko';
    const T = trFn || (typeof tr === 'function' ? tr : x => x);
    const list = Array.isArray(facts) ? facts : [];
    const arcs = detectArcs(list);
    const outArcs = [];
    const dayTag = d => ({ ko:`제${d}일`, en:`Day ${d}`, ja:`${d}日目`, zhs:`第${d}天`, zht:`第${d}天` }[L]);

    for(const a of arcs){
      const f = a.fact, w = f.who || {};
      if(a.kind === 'betrayal'){
        const mN = narrName(w.a, T, false), d0 = a.form ? a.form.d : f.d, d1 = f.d;
        const why = a.ignored ? {
          ko:'구원 요청을 외면당했던 밤의 원한이 쌓인 결과였다.',
          en:'It was the price of an earlier plea for aid left unanswered.',
          ja:'かつて救援を求めた夜に見捨てられた恨みが積もった結果だった。',
          zhs:'那是昔日求援却遭冷眼旁观后积攒的怨恨所致。',
          zht:'那是昔日求援卻遭冷眼旁觀後積攢的怨恨所致。',
        }[L] : (f.persona && f.persona.ruthless >= 65) ? {
          ko:'처음부터 타인을 이용하다 버릴 계산이 서 있던 비정한 결단이었다.',
          en:'Cold calculation drove them from the first—allies were only shields to discard.',
          ja:'最初から他者を利用し切り捨てる計算の上に立った非情な決断だった。',
          zhs:'从一开始便算计着利用并舍弃同伴，这是毫无怜悯的决断。',
          zht:'從一開始便算計著利用並捨棄同伴，這是毫無憐憫的決斷。',
        }[L] : {
          ko:'금 간 신뢰는 끝내 회복되지 못했다.',
          en:'Once fractured, their trust never healed.',
          ja:'ひび割れた信頼はついに戻ることはなかった。',
          zhs:'裂痕既生，彼此的信任终究未能挽回。',
          zht:'裂痕既生，彼此的信任終究未能挽回。',
        }[L];
        const act = f.type === 'ally_abandon' ? {
          ko:`${dayTag(d1)}, ${mN}${J(mN,'은')} 난전 한가운데서 발을 빼며 동맹을 방패로 세웠다.`,
          en:`On ${dayTag(d1)}, ${mN} withdrew mid-battle, abandoning their ally to take the blow.`,
          ja:`${dayTag(d1)}、${mN}は乱戦のただ中で手を引き、同盟を盾にして姿を消した。`,
          zhs:`${dayTag(d1)}，${mN}在混战中抽身而退，将同盟留作挡箭牌。`,
          zht:`${dayTag(d1)}，${mN}在混戰中抽身而退，將同盟留作擋箭牌。`,
        }[L] : (f.meta && f.meta.kind === 'sellout') ? {
          ko:`${dayTag(d1)}, ${mN}${J(mN,'은')} 동맹의 거처를 다른 진영에 팔아넘겼다.`,
          en:`On ${dayTag(d1)}, ${mN} betrayed the pact by selling out their ally's hideout to rival hunters.`,
          ja:`${dayTag(d1)}、${mN}は同盟の拠点を他陣営に売り渡した。`,
          zhs:`${dayTag(d1)}，${mN}背弃盟约，将同盟的据点出卖给了敌方。`,
          zht:`${dayTag(d1)}，${mN}背棄盟約，將同盟的據點出賣給了敵方。`,
        }[L] : {
          ko:`${dayTag(d0)}에 맺은 손을 뒤로한 채, ${dayTag(d1)}에 ${mN}${J(mN,'은')} 동맹에게 칼을 겨누었다.`,
          en:`Forgetting the oath sworn on ${dayTag(d0)}, ${mN} turned their blade against their ally on ${dayTag(d1)}.`,
          ja:`${dayTag(d0)}に結んだ手を裏切り、${dayTag(d1)}、${mN}は同盟へと刃を向けた。`,
          zhs:`背弃了${dayTag(d0)}的盟约，${mN}在${dayTag(d1)}向同盟举起了刀刃。`,
          zht:`背棄了${dayTag(d0)}的盟約，${mN}在${dayTag(d1)}向同盟舉起了刀刃。`,
        }[L];
        outArcs.push({
          id: 'betrayal_' + f.id, kind: 'betrayal',
          title: { ko:'끊어진 맹세', en:'Broken Oaths', ja:'砕かれた誓約', zhs:'破碎的盟誓', zht:'破碎的盟誓' }[L],
          body: `${act} ${why}`,
          days: [d0, d1], factIds: a.factIds
        });
      } else if(a.kind === 'masterless'){
        const sN = narrName(w.a, T, true), d0 = f.d, cnt = a.fights.length;
        const lastF = a.fights[cnt - 1];
        const re = a.fights.find(x => x.type === 'stray_recontract');
        const rev = a.fights.some(x => x.meta && x.meta.revenge);
        const tail = re ? {
          ko:`결국 ${dayTag(re.d)}에 새 마스터와 다시 계약을 맺으며 전장에 남았다.`,
          en:`Eventually on ${dayTag(re.d)}, they forged a new pact and stayed in the war.`,
          ja:`やがて${dayTag(re.d)}、新たなマスターと契約を結び直し戦場に留まった。`,
          zhs:`最终在${dayTag(re.d)}与新御主缔结契约，留在了战局之中。`,
          zht:`最終在${dayTag(re.d)}與新御主締結契約，留在了戰局之中。`,
        }[L] : {
          ko:`주인의 죽음 뒤에도 ${cnt}차례나 검을 맞대며 마지막 마력이 다할 때까지 싸움을 멈추지 않았다.`,
          en:`Even after their Master fell, they crossed blades ${cnt} more time${cnt>1?'s':''}, refusing to fade quietly.`,
          ja:`主を失った後も${cnt}度にわたり刃を交え、残る魔力が尽きるまで戦い続けた。`,
          zhs:`在御主身亡后仍${cnt}次挥刃交锋，直至魔力耗尽也未曾停步。`,
          zht:`在御主身亡後仍${cnt}次揮刃交鋒，直至魔力耗盡也未曾停步。`,
        }[L];
        const mid = rev ? {
          ko:`특히 마스터를 쓰러뜨린 원수를 쫓아 밤거리를 덮쳤다.`,
          en:`Driven by vengeance, they hunted down the very faction that slew their Master.`,
          ja:`とりわけ主を討った仇を追い、夜の街で襲撃を仕掛けた。`,
          zhs:`更是追猎着杀害御主的仇敌，在夜色中发动反击。`,
          zht:`更是追獵著殺害御主的仇敵，在夜色中發動反擊。`,
        }[L] : '';
        outArcs.push({
          id: 'masterless_' + f.id, kind: 'masterless',
          title: { ko:'주인 없는 칼날', en:'A Blade Without a Master', ja:'主なき刃', zhs:'无主之刃', zht:'無主之刃' }[L],
          body: `${{
            ko:`${dayTag(d0)}, 마스터가 쓰러졌지만 ${sN}${J(sN,'은')} 흩어지지 않았다.`,
            en:`On ${dayTag(d0)}, their Master perished, yet ${sN} refused to vanish.`,
            ja:`${dayTag(d0)}、マスターが倒れてなお、${sN}は消滅を拒んだ。`,
            zhs:`${dayTag(d0)}，御主虽已陨落，${sN}却并未就此消散。`,
            zht:`${dayTag(d0)}，御主雖已隕落，${sN}卻並未就此消散。`,
          }[L]} ${mid ? mid + ' ' : ''}${tail}`,
          days: [d0, lastF.d], factIds: a.factIds
        });
      } else if(a.kind === 'enemy_coop'){
        const aM = narrName(w.a, T, false), bM = narrName(w.b, T, false);
        const tgt = (f.meta && f.meta.vsLabel) ? T(f.meta.vsLabel) : '';
        const pre = a.prior ? {
          ko:`${dayTag(a.prior.d)}에 이미 칼을 맞댔던 사이였지만,`,
          en:`Though they had crossed blades on ${dayTag(a.prior.d)},`,
          ja:`${dayTag(a.prior.d)}には互いに刃を交えた仲だったが、`,
          zhs:`尽管${dayTag(a.prior.d)}两人还曾拔刀相向，`,
          zht:`儘管${dayTag(a.prior.d)}兩人還曾拔刀相向，`,
        }[L] : {
          ko:`적대하던 두 진영이었으나,`,
          en:`Though sworn rivals in the war,`,
          ja:`相容れぬ敵同士であったものの、`,
          zhs:`本是彼此敌对的两方，`,
          zht:`本是彼此敵對的兩方，`,
        }[L];
        outArcs.push({
          id: 'coop_' + f.id, kind: 'enemy_coop',
          title: { ko:'적과의 동행', en:'Reluctant Alliance', ja:'敵との共闘', zhs:'强敌暂盟', zht:'強敵暫盟' }[L],
          body: `${pre} ${{
            ko:`${dayTag(f.d)}에 ${aM}${J(aM,'과')} ${bM}${J(bM,'은')} ${tgt ? tgt + '이라는 ' : ''}거대한 위협 앞에서 잠시 손을 잡았다.`,
            en:`on ${dayTag(f.d)}, ${aM} and ${bM} were forced to join forces${tgt ? ` against ${tgt}` : ' against a greater threat'}.`,
            ja:`${dayTag(f.d)}、${aM}と${bM}は${tgt ? `${tgt}という` : ''}強大な脅威を前にやむなく手を結んだ。`,
            zhs:`在${dayTag(f.d)}，${aM}与${bM}面对${tgt ? `${tgt}这一` : ''}共同的强敌，不得不暂时并肩。`,
            zht:`在${dayTag(f.d)}，${aM}與${bM}面對${tgt ? `${tgt}這一` : ''}共同的強敵，不得不暫時並肩。`,
          }[L]}`,
          days: [a.prior ? a.prior.d : f.d, f.d], factIds: a.factIds
        });
      } else if(a.kind === 'defiance'){
        const r0 = a.refuses[0], rw = r0.who || {};
        const sv = rw.a && rw.a.id === 'me' ? T(rw.a.hero || '') : narrName(rw.a, T, true);
        const hasDef = a.refuses.some(x => x.type === 'servant_defect');
        const sealTxt = a.seals.length ? {
          ko:`령주(${a.seals.length}획)로 얽어매려던 균열 끝에`,
          en:`Strained by ${a.seals.length} forced Command Spell${a.seals.length>1?'s':''},`,
          ja:`${a.seals.length}画の令呪による強制で深まった亀裂の末に、`,
          zhs:`在${a.seals.length}道强行令咒积累的裂痕下，`,
          zht:`在${a.seals.length}道強行令咒累積的裂痕下，`,
        }[L] : {
          ko:`주종 사이의 불화와 자존심이 맞부딪치며,`,
          en:`Where pride collided with a Master's command,`,
          ja:`主従の矜持と不信がぶつかり合い、`,
          zhs:`主从间的骄傲与命令发生碰撞，`,
          zht:`主從間的驕傲與命令發生碰撞，`,
        }[L];
        outArcs.push({
          id: 'defiance_' + r0.id, kind: 'defiance',
          title: { ko:'꺾이지 않은 의지', en:'Unbowed Defiance', ja:'折れぬ意志', zhs:'不屈的抗命', zht:'不屈的抗命' }[L],
          body: `${sealTxt} ${{
            ko:`${dayTag(r0.d)}에 ${sv}${J(sv,'은')} 명령을 정면으로 거부했다.${hasDef ? ' 결국 계약마저 끊어지고 말았다.' : ''}`,
            en:`on ${dayTag(r0.d)}, ${sv} defied their Master's order.${hasDef ? ' Ultimately, even the contract shattered.' : ''}`,
            ja:`${dayTag(r0.d)}、${sv}は主の命令を正面から拒んだ。${hasDef ? 'ついには契約までもが断ち切られた。' : ''}`,
            zhs:`${dayTag(r0.d)}，${sv}正面违抗了御主的命令。${hasDef ? '最终连契约也彻底断裂。' : ''}`,
            zht:`${dayTag(r0.d)}，${sv}正面違抗了御主的命令。${hasDef ? '最終連契約也徹底斷裂。' : ''}`,
          }[L]}`,
          days: [r0.d, a.refuses[a.refuses.length - 1].d], factIds: a.factIds
        });
      } else if(a.kind === 'devotion'){
        const p0 = a.prots[0], pw = p0.who || {}, sv = T((pw.a && pw.a.hero) || '');
        const cnt = a.prots.length;
        outArcs.push({
          id: 'devotion_' + p0.id, kind: 'devotion',
          title: { ko:'방패가 된 충의', en:'Shield of Loyalty', ja:'盾となった忠義', zhs:'化为盾牌的忠义', zht:'化為盾牌的忠義' }[L],
          body: {
            ko:`전쟁 내내 ${sv}${J(sv,'은')} 마스터의 안전을 가장 먼저 두었다. ${cnt}번의 위기 속에서 몸을 던져 치명상을 막아 냈다.`,
            en:`Throughout the war, ${sv} placed their Master's life above their own, stepping into harm's way ${cnt} time${cnt>1?'s':''}.`,
            ja:`戦いを通じて${sv}はマスターの命を何より重んじ、${cnt}度の危機で身を挺して一撃を防ぎ切った。`,
            zhs:`整场战争中，${sv}始终将御主的安危置于首位，在${cnt}次险境中挺身挡下了致命一击。`,
            zht:`整場戰爭中，${sv}始終將御主的安危置於首位，在${cnt}次險境中挺身擋下了致命一擊。`,
          }[L],
          days: [p0.d, a.prots[cnt - 1].d], factIds: a.factIds
        });
      }
    }

    // Judul Dinamis berdasarkan arc paling dominan yang benar-benar terjadi
    const pri = ['betrayal','masterless','enemy_coop','defiance','devotion'];
    const lead = pri.map(k => outArcs.find(x => x.kind === k)).find(Boolean);
    const TITLES = {
      betrayal: { ko:'배신으로 얼룩진 겨울', en:'The Winter of Broken Oaths', ja:'裏切りに染まった冬', zhs:'背叛染红的冬夜', zht:'背叛染紅的冬夜' },
      masterless: { ko:'주인 없는 칼날이 남긴 밤', en:'The Night of the Masterless Blade', ja:'主なき刃の残響', zhs:'无主之刃的冬夜', zht:'無主之刃的冬夜' },
      enemy_coop: { ko:'적과 등을 맞댄 겨울', en:'Enemies Under One Banner', ja:'敵と背中を預けた夜', zhs:'敌手并肩的冬夜', zht:'敵手並肩的冬夜' },
      defiance: { ko:'명령을 거스른 영령의 기록', en:'Chronicle of the Unbowed Hero', ja:'命に背いた英霊の記録', zhs:'违命英灵的战纪', zht:'違命英靈的戰紀' },
      devotion: { ko:'끝까지 주인을 지킨 밤', en:'Vigil of Unyielding Loyalty', ja:'主を守り抜いた冬', zhs:'誓死护主的冬夜', zht:'誓死護主的冬夜' },
      plain: { ko:'성배가 차오른 겨울의 기록', en:'Chronicle of the Winter War', ja:'聖杯戦争の記録', zhs:'圣杯战争战纪', zht:'聖杯戰爭戰紀' },
    };
    const title = TITLES[lead ? lead.kind : 'plain'][L];
    return { title, arcs: outArcs, factCount: list.length };
  }

  // Stray Servant terus bertarung di malam hari sebelum memudar
  function strayFightNight(){
    const w = W(), svs = strays().filter(p => p.alive && !p.master && p.stray > 0 && !(w.nf || []).some(f => f.includes(p.i)));
    if(!svs.length) return;
    for(const st of svs){
      const sp = servantPersona(H_BY[st.hero]);
      const targets = contracted().filter(x => x.alive && !x.bxNun && !(w.nf || []).some(f => f.includes(x.i)));
      if(!targets.length) continue;
      const revTarget = st.killerId ? targets.find(x => x.i === st.killerId) : null;
      if(!revTarget && sp.pride < 60 && !sp.tags.includes('berserk') && !ch(.35)) continue;
      if(revTarget ? !ch(.75) : !ch(.5)) continue;
      const tgt = revTarget || wpick(targets, x => 1 + (x.hp < 60 ? 1.5 : 0));
      if(!tgt) continue;
      const { win, lose } = npcFight(st, tgt, false, true);
      w.nf.push([st.i, tgt.i]);
      recFact('stray_fight', {
        actor: 'p'+st.i, target: 'p'+tgt.i,
        who: { a: pairSnap(st), b: pairSnap(tgt) },
        causeId: st.strayFactId || null,
        meta: { revenge: tgt.i === st.killerId, won: win === st, killed: lose.hp <= 0 },
        beat: st.known || tgt.known || st.revealed || tgt.revealed || tgt.i === st.killerId
      });
      const seen = st.known || tgt.known || tgt.ally || tgt.ally || ch(.5);
      if(lose.hp <= 0){
        const lh = H_BY[lose.hero];
        if(lh.sp === 'revive' && !lose.usedRevive){ lose.usedRevive = true; lose.hp = 45; continue; }
        lose.alive = false; lose.revealed = true;
        pairOut(lose, '주인 잃은 서번트에게 쓰러졌다', seen ? win : null);
        log(`감독관의 통지: ${cn(lose)} 조 탈락.${seen ? ` 주인 잃은 ${pName(win)}의 손에.` : ''}`, 'notice');
      }
    }
  }

  // Dua musuh terpaksa bekerja sama menghadapi ancaman dominan
  function npcEnemyCoop(){
    const w = W(); if(w.day < 4 || w.coopDone) return;
    const cs = contracted().filter(p => p.alive && p.master && !p.ally && !p.bxNun && !(p.halt > 0) && !(w.nf || []).some(f => f.includes(p.i)));
    if(cs.length < 3) return;
    // Cari ancaman dominan (NPC kuat dengan kills >= 2 atau pemain dengan kills >= 2)
    let threatTgt = null, vsMe = false;
    const bossNpc = cs.slice().sort((a,b) => (b.pw + (b.kills||0)*12) - (a.pw + (a.kills||0)*12))[0];
    if((w.kills || 0) >= 2 && w.heroAlive && !w.hid && ch(.35)){ vsMe = true; }
    else if(bossNpc && ((bossNpc.kills || 0) >= 2 || bossNpc.pw >= 76) && ch(.35)){ threatTgt = bossNpc; }
    if(!vsMe && !threatTgt) return;
    const pool = cs.filter(p => p !== threatTgt && (!vsMe || !p.ally));
    if(pool.length < 2) return;
    let pairA = null, pairB = null, priorFact = null;
    for(let i = 0; i < pool.length && !pairA; i++){
      for(let j = i + 1; j < pool.length; j++){
        const a = pool[i], b = pool[j], r = relGet('p'+a.i, 'p'+b.i);
        const du = lastFactOf('duel_clash', x => (x.actor==='p'+a.i && x.target==='p'+b.i) || (x.actor==='p'+b.i && x.target==='p'+a.i));
        if(du || r.rivalry >= 15 || r.grudge >= 10){ pairA = a; pairB = b; priorFact = du; break; }
      }
    }
    if(!pairA || !pairB) return;
    w.coopDone = w.day;
    relShift('p'+pairA.i, 'p'+pairB.i, { trust: 15, respect: 10, grudge: -8 });
    relShift('p'+pairB.i, 'p'+pairA.i, { trust: 15, respect: 10, grudge: -8 });
    if(vsMe){
      recFact('enemy_coop', {
        actor:'p'+pairA.i, target:'p'+pairB.i,
        who:{ a: pairSnap(pairA), b: pairSnap(pairB) },
        causeId: priorFact ? priorFact.id : null,
        meta:{ kind:'npc_pact', vsLabel: S.name },
        beat: true
      });
      w.coal = { a: pairA.i, b: pairB.i, d: w.day };
      return;
    }
    recFact('enemy_coop', {
      actor:'p'+pairA.i, target:'p'+pairB.i,
      who:{ a: pairSnap(pairA), b: pairSnap(pairB) },
      causeId: priorFact ? priorFact.id : null,
      meta:{ kind:'npc_pact', vsLabel: threatTgt.mname || cn(threatTgt) },
      beat: !!(pairA.known || pairB.known || threatTgt.known)
    });
    for(const atk of [pairA, pairB]){
      if(!threatTgt.alive) break;
      const { win, lose } = npcFight(atk, threatTgt, false, true);
      w.nf.push([atk.i, threatTgt.i]);
      if(lose.hp <= 0){
        const lh = H_BY[lose.hero];
        if(lh.sp === 'revive' && !lose.usedRevive){ lose.usedRevive = true; lose.hp = 45; continue; }
        lose.alive = false; lose.revealed = true;
        pairOut(lose, '임시로 손을 잡은 두 조에게 쓰러졌다', win);
        log(`감독관의 통지: ${cn(lose)} 조 탈락.`, 'notice');
      }
    }
  }
"""
rp("  function pairSnap", "/* placeholder */") if False else None
rp("  const W=()=>S.war;", NARR_CORE + "  const W=()=>S.war;")

# 2. Track facts on Alliance, Help, Ignore, Betrayal, Abandonment, Coalition, Enemy Cooperation
rp(
"if(ch(pc)){p.ally=true;p.allyDay=W().day;S.flags.allyName=p.mname;allyConfide(p);wrec('ally',`${cn(p)} 조 ${p.mname}${J(p.mname,과)} 동맹`,{p:p.i});log(`${p.mname}${J(p.mname,이)} 동맹을 받아들였다. 마지막 둘이 남을 때까지만.`,'war');}",
"if(ch(pc)){p.ally=true;p.allyDay=W().day;S.flags.allyName=p.mname;allyConfide(p);wrec('ally',`${cn(p)} 조 ${p.mname}${J(p.mname,과)} 동맹`,{p:p.i});log(`${p.mname}${J(p.mname,이)} 동맹을 받아들였다. 마지막 둘이 남을 때까지만.`,'war'); const _af=recFact('ally_form',{actor:'p'+p.i,target:'me',who:{a:pairSnap(p),b:pairSnap('me')},rel:relGet('p'+p.i,'me'),persona:masterPersona(p)}); if(p.fought){ const _df=lastFactOf('duel_clash',x=>x.actor==='p'+p.i||x.target==='p'+p.i); recFact('enemy_coop',{actor:'p'+p.i,target:'me',who:{a:pairSnap(p),b:pairSnap('me')},causeId:_df?_df.id:_af&&_af.id,meta:{kind:'truce_ally'},beat:true}); } }"
)
rp(
"{t:'손을 잡는다',f:()=>{ e.ally=true;e.allyDay=w.day; e.known=true; S.flags.allyName=e.mname;allyConfide(e);wrec('ally',`${cn(e)} 조 ${e.mname}${J(e.mname,과)} 동맹`,{p:e.i}); return `${pName(e)} 조와 동맹을 맺었다.`; }},",
"{t:'손을 잡는다',f:()=>{ e.ally=true;e.allyDay=w.day; e.known=true; S.flags.allyName=e.mname;allyConfide(e);wrec('ally',`${cn(e)} 조 ${e.mname}${J(e.mname,과)} 동맹`,{p:e.i}); const _af=recFact('ally_form',{actor:'p'+e.i,target:'me',who:{a:pairSnap(e),b:pairSnap('me')},rel:relGet('p'+e.i,'me'),persona:masterPersona(e)}); const _df=lastFactOf('duel_clash',x=>x.actor==='p'+e.i||x.target==='p'+e.i); recFact('enemy_coop',{actor:'p'+e.i,target:'me',who:{a:pairSnap(e),b:pairSnap('me')},causeId:_df?_df.id:(_af&&_af.id),meta:{kind:'truce_ally'},beat:true}); return `${pName(e)} 조와 동맹을 맺었다.`; }},"
)
rp(
"b.owe=(b.owe||0)+1; b.slight=Math.max(0,(b.slight||0)-1); relShift('p'+b.i,'me',{trust:18,affection:12,respect:10,grudge:-10});",
"b.owe=(b.owe||0)+1; b.slight=Math.max(0,(b.slight||0)-1); relShift('p'+b.i,'me',{trust:18,affection:12,respect:10,grudge:-10}); recFact('ally_help',{actor:'me',target:'p'+b.i,who:{a:pairSnap('me'),b:pairSnap(b)},rel:relGet('p'+b.i,'me')});"
)
rp(
"if(b.alive&&b.ally){ b.slight=(b.slight||0)+1; relShift('p'+b.i,'me',{trust:-22,affection:-15,grudge:22}); if(ch(Math.min(.9,",
"if(b.alive&&b.ally){ b.slight=(b.slight||0)+1; relShift('p'+b.i,'me',{trust:-22,affection:-15,grudge:22}); const _ig=recFact('ally_ignore',{actor:'p'+b.i,target:'me',who:{a:pairSnap(b),b:pairSnap('me')},rel:relGet('p'+b.i,'me')}); if(ch(Math.min(.9,"
)
rp(
"if(p.ally&&_mp.ruthless>=65&&p.hp<55&&ch(Math.min(.65,_bs*.5+.12))){ out.push(i); p.ally=false; p.allyGone=true; relShift('p'+p.i,'me',{trust:-30,affection:-20,grudge:20}); log('동맹이 싸움 도중 발을 뺐다. 처음부터 당신을 방패로 삼을 작정이었던 모양이다.','loss'); continue; }",
"if(p.ally&&_mp.ruthless>=65&&p.hp<55&&ch(Math.min(.65,_bs*.5+.12))){ out.push(i); p.ally=false; p.allyGone=true; relShift('p'+p.i,'me',{trust:-30,affection:-20,grudge:20}); const _pr=lastFactOf(['ally_ignore','ally_form'],x=>x.actor==='p'+p.i); recFact('ally_abandon',{actor:'p'+p.i,target:'me',who:{a:pairSnap(p),b:pairSnap('me')},rel:relGet('p'+p.i,'me'),persona:_mp,causeId:_pr&&_pr.id,meta:{kind:'midfight'},beat:true}); log('동맹이 싸움 도중 발을 뺐다. 처음부터 당신을 방패로 삼을 작정이었던 모양이다.','loss'); continue; }"
)
rp(
"if(_bait&&ch(_bs*.42)){ w.sacrificed=1; _allyS.ally=false; _allyS.allyGone=true; w.exposure=clamp(w.exposure+expUp(18)); relShift('p'+_allyS.i,'me',{trust:-35,affection:-25,grudge:25}); log('동맹이 등을 돌렸다. 당신의 거처를 다른 조에 팔아넘긴 것이다.','loss'); wrec('mine',`동맹 ${_allyS.mname}${J(_allyS.mname,이)} 거처를 팔아넘겼다`,{p:_allyS.i}); return battle(_bait,{ambushed:true}); }",
"if(_bait&&ch(_bs*.42)){ w.sacrificed=1; _allyS.ally=false; _allyS.allyGone=true; w.exposure=clamp(w.exposure+expUp(18)); relShift('p'+_allyS.i,'me',{trust:-35,affection:-25,grudge:25}); const _pr=lastFactOf(['ally_ignore','ally_form'],x=>x.actor==='p'+_allyS.i); recFact('ally_betray',{actor:'p'+_allyS.i,target:'me',who:{a:pairSnap(_allyS),b:pairSnap('me')},rel:relGet('p'+_allyS.i,'me'),persona:masterPersona(_allyS),causeId:_pr&&_pr.id,meta:{kind:'sellout'},beat:true}); log('동맹이 등을 돌렸다. 당신의 거처를 다른 조에 팔아넘긴 것이다.','loss'); wrec('mine',`동맹 ${_allyS.mname}${J(_allyS.mname,이)} 거처를 팔아넘겼다`,{p:_allyS.i}); return battle(_bait,{ambushed:true}); }"
)
rp(
"const _bs=betrayScore(relGet('p'+a.i,'me'),masterPersona(a),{seals:W().seals,hp:W().hp,owe:a.owe,slight:a.slight});if(ch(_bs)){a.ally=false;a.allyGone=true;log(`동맹 ${a.mname}${J(a.mname,이)} 등을 돌렸다.`,'loss');battle(a,{ambushed:true});}",
"const _bs=betrayScore(relGet('p'+a.i,'me'),masterPersona(a),{seals:W().seals,hp:W().hp,owe:a.owe,slight:a.slight});if(ch(_bs)){a.ally=false;a.allyGone=true;const _pr=lastFactOf(['ally_ignore','ally_form'],x=>x.actor==='p'+a.i);recFact('ally_betray',{actor:'p'+a.i,target:'me',who:{a:pairSnap(a),b:pairSnap('me')},rel:relGet('p'+a.i,'me'),persona:masterPersona(a),causeId:_pr&&_pr.id,meta:{kind:'ambush'},beat:true});log(`동맹 ${a.mname}${J(a.mname,이)} 등을 돌렸다.`,'loss');battle(a,{ambushed:true});}"
)
rp(
"if(it==='betray'){ a.ally=false; S.flags.allyBetrayed=1; log(`손을 내민 순간, ${a.mname}의 서번트가 먼저 움직였다. 처음부터 이럴 생각이었던 것이다.`,'loss');",
"if(it==='betray'){ a.ally=false; S.flags.allyBetrayed=1; const _pr=lastFactOf(['ally_ignore','ally_form'],x=>x.actor==='p'+a.i); recFact('ally_betray',{actor:'p'+a.i,target:'me',who:{a:pairSnap(a),b:pairSnap('me')},rel:relGet('p'+a.i,'me'),persona:masterPersona(a),causeId:_pr&&_pr.id,meta:{kind:'final'},beat:true}); log(`손을 내민 순간, ${a.mname}의 서번트가 먼저 움직였다. 처음부터 이럴 생각이었던 것이다.`,'loss');"
)
rp(
"    w.coalNext=live[1]?live[1].i:null;",
"    w.coalNext=live[1]?live[1].i:null;\n    if(live.length>=2){ const _du=lastFactOf('duel_clash',x=>(x.actor==='p'+live[0].i&&x.target==='p'+live[1].i)||(x.actor==='p'+live[1].i&&x.target==='p'+live[0].i)); recFact('enemy_coop',{actor:'p'+live[0].i,target:'p'+live[1].i,who:{a:pairSnap(live[0]),b:pairSnap(live[1])},causeId:_du&&_du.id,meta:{kind:'coalition',vsLabel:S.name},beat:true}); }"
)

# 3. Track facts on Command Spells, Order Refusal, Servant Defection, Loyal Protection
rp(
"    { const h=hero(), sp=servantPersona(h); relShift('me','hero',{fear:10,grudge:(sp.pride>=70||(h&&h.traits.includes('자유')))?8:3,affection:-4}); }",
"    { const h=hero(), sp=servantPersona(h); relShift('me','hero',{fear:10,grudge:(sp.pride>=70||(h&&h.traits.includes('자유')))?8:3,affection:-4}); recFact('seal_force',{actor:'me',target:'hero',who:{a:pairSnap('me')},rel:relGet('me','hero'),meta:{word}}); }"
)
rp(
"if(CHK) CHK.push({txt:'「불신」 탓에 서번트가 명령을 듣지 않았다',ok:false}); relShift('me','hero',{respect:-3,grudge:3}); return clash(0);",
"if(CHK) CHK.push({txt:'「불신」 탓에 서번트가 명령을 듣지 않았다',ok:false}); relShift('me','hero',{respect:-3,grudge:3}); const _sf=lastFactOf('seal_force'); recFact('order_refuse',{actor:'hero',target:'me',who:{a:pairSnap('me')},rel:relGet('me','hero'),causeId:_sf&&_sf.id,meta:{reason:'distrust'},beat:true}); return clash(0);"
)
rp(
"if(CHK) CHK.push({txt:'「긍지」 높은 서번트가 퇴각을 거부했다',ok:false}); relShift('me','hero',{grudge:3,rivalry:2}); return clash(0);",
"if(CHK) CHK.push({txt:'「긍지」 높은 서번트가 퇴각을 거부했다',ok:false}); relShift('me','hero',{grudge:3,rivalry:2}); const _sf=lastFactOf('seal_force'); recFact('order_refuse',{actor:'hero',target:'me',who:{a:pairSnap('me')},rel:relGet('me','hero'),persona:sp,causeId:_sf&&_sf.id,meta:{reason:'pride'},beat:true}); return clash(0);"
)
rp(
"      if(e.known&&ch(.4)) log('상대 마스터가 싸움에서 발을 빼려다 서번트의 반발에 부딪혔다.','war');\n      return false;",
"      recFact('order_refuse',{actor:'p'+e.i,target:'p'+e.i,who:{a:pairSnap(e)},persona:_sp,meta:{reason:'pride',npc:1},beat:!!e.known});\n      if(e.known&&ch(.4)) log('상대 마스터가 싸움에서 발을 빼려다 서번트의 반발에 부딪혔다.','war');\n      return false;"
)
rp(
"log(`${h.name}${J(h.name,은)} 당신을 내려다보았다. ${qv(h,'betray')} 그리고 ${tgt.mname}의 진영으로 걸어갔다.`,'loss');",
"const _or=lastFactOf(['order_refuse','seal_force']); recFact('servant_defect',{actor:'hero',target:'me',who:{a:pairSnap('me'),b:pairSnap(tgt)},rel:relGet('me','hero'),causeId:_or&&_or.id,beat:true});\n        log(`${h.name}${J(h.name,은)} 당신을 내려다보았다. ${qv(h,'betray')} 그리고 ${tgt.mname}의 진영으로 걸어갔다.`,'loss');"
)
rp(
"    relShift('me', 'hero', {trust:2, affection:3, respect:2});\n    return true;",
"    relShift('me', 'hero', {trust:2, affection:3, respect:2});\n    recFact('servant_protect',{actor:'hero',target:'me',who:{a:pairSnap('me')},rel:relGet('me','hero'),persona:sp});\n    return true;"
)

# 4. Masterless Servant continuation (makeStray, strayFightNight, npcRecontract) & Duel/Kill facts
rp(
"function makeStray(e){ const eh=H_BY[e.hero], d=strayDays(eh); e.master=false; e.mDied=true; e.stray=d; e.wishKnown=false; if(!W().stray||!W().stray.alive) W().stray=e; return d; }",
"function makeStray(e,by){ const eh=H_BY[e.hero], d=strayDays(eh); e.master=false; e.mDied=true; e.stray=d; e.wishKnown=false; e.killerId=by==='me'?'me':(by&&by.i?by.i:null); const _mf=recFact('master_die_stray',{actor:'p'+e.i,target:e.killerId==='me'?'me':(e.killerId?'p'+e.killerId:null),who:{a:pairSnap(e),b:by?pairSnap(by):null},meta:{days:d}}); e.strayFactId=_mf?_mf.id:null; if(!W().stray||!W().stray.alive) W().stray=e; return d; }"
)
rp("if(ch(.6)){ const d=makeStray(e);", "if(ch(.6)){ const d=makeStray(e,'me');")
rp("if(ch(.7)){ makeStray(lose);", "if(ch(.7)){ makeStray(lose,win);")
rp("if(ch(.7)) makeStray(t);", "if(ch(.7)) makeStray(t,by);")
rp("if(ch(.7)){ const d=makeStray(lose);", "if(ch(.7)){ const d=makeStray(lose,win);")
rp("if(ch(.7)) makeStray(lose);", "if(ch(.7)) makeStray(lose,win);")
rp(
"    wrec('hint',`${cn(s)} 서번트가 ${m.known?m.mname:'다른 마스터'}${J(m.known?m.mname:'다른 마스터',과)} 다시 계약했다`); }",
"    recFact('stray_recontract',{actor:'p'+s.i,target:'p'+m.i,who:{a:pairSnap(s),b:pairSnap(m)},causeId:s.strayFactId||null});\n    wrec('hint',`${cn(s)} 서번트가 ${m.known?m.mname:'다른 마스터'}${J(m.known?m.mname:'다른 마스터',과)} 다시 계약했다`); }"
)
rp(
"    const truce=huntOn(); huntNpc();",
"    const truce=huntOn(); huntNpc();\n    if(!truce){ strayFightNight(); npcEnemyCoop(); }"
)
rp(
"    if(r&&r.win&&r.lose&&!r.win.cx&&!r.lose.cx){ relShift('p'+r.lose.i,'p'+r.win.i,{fear:10,respect:8,rivalry:10,grudge:12}); relShift('p'+r.win.i,'p'+r.lose.i,{respect:6,rivalry:6}); }",
"    if(r&&r.win&&r.lose&&!r.win.cx&&!r.lose.cx){ relShift('p'+r.lose.i,'p'+r.win.i,{fear:10,respect:8,rivalry:10,grudge:12}); relShift('p'+r.win.i,'p'+r.lose.i,{respect:6,rivalry:6}); if(r.win.master&&r.lose.master) recFact('duel_clash',{actor:'p'+r.win.i,target:'p'+r.lose.i,who:{a:pairSnap(r.win),b:pairSnap(r.lose)}}); }"
)
rp(
"if(b.res==='talk') relShift('p'+e.i,'me',{trust:15,affection:10,respect:8,grudge:-10});",
"if(b.res==='talk') relShift('p'+e.i,'me',{trust:15,affection:10,respect:8,grudge:-10});\n        recFact('duel_clash',{actor:'me',target:'p'+e.i,who:{a:pairSnap('me'),b:pairSnap(e)},meta:{res:b.res}});"
)

# 5. Persist compact facts in warDigest() & export Sim.narrative / Sim.narrBeat
rp(
"tl:(w.tl||[]).slice(0,80), last:w.lastVoice||'',",
"tl:(w.tl||[]).slice(0,80), facts:(w.facts||[]).slice(-60), last:w.lastVoice||'',"
)
rp(
"betrayRisk:p=>S&&S.war&&p?betrayScore(relGet('p'+p.i,'me'),masterPersona(p),{seals:S.war.seals,hp:S.war.hp,owe:p.owe,slight:p.slight}):0,",
"betrayRisk:p=>S&&S.war&&p?betrayScore(relGet('p'+p.i,'me'),masterPersona(p),{seals:S.war.seals,hp:S.war.hp,owe:p.owe,slight:p.slight}):0, narrative:(lg,trFn)=>S&&S.war?renderNarrative(S.war.facts||[],{day:S.war.day},lg,trFn):null, narrativeFrom:(wd,lg,trFn)=>wd?renderNarrative(wd.facts||[],wd,lg,trFn):null, narrBeat:(f,lg,trFn)=>narrBeat(f,lg,trFn),"
)

# 6. CSS for .entry.story & Chronicle box
NARR_CSS = (
    ".entry.story .b,.sub.story{color:#e6d9f2;font-family:var(--f-story);font-style:italic;border-left:2px solid rgba(180,150,220,.65);padding:4px 10px;background:rgba(160,130,210,.06);border-radius:0 6px 6px 0}"
    ".narr-btn{margin-left:auto;background:none;border:1px solid rgba(201,164,92,.4);color:var(--gold2);border-radius:999px;font:500 11px var(--f-ui);padding:2px 9px;cursor:pointer}"
    ".narr-btn:hover{background:rgba(201,164,92,.12)}"
    ".narr-box{display:grid;gap:10px;margin:8px 0 14px}"
    ".narr-title{font-family:var(--f-display);font-size:18px;color:var(--gold2);margin:0 0 6px}"
    ".narr-arc{padding:10px 12px;border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:8px;background:rgba(255,255,255,.02)}"
    ".narr-arc.betrayal{border-left-color:#c03a45}.narr-arc.masterless{border-left-color:#8a86c9}.narr-arc.enemy_coop{border-left-color:#86ab92}.narr-arc.defiance{border-left-color:#e0b48a}.narr-arc.devotion{border-left-color:#9bd3ac}"
    ".narr-arc h5{margin:0 0 4px;font-size:13px;color:var(--gold2);display:flex;justify-content:space-between;align-items:center}"
    ".narr-arc h5 small{font-family:var(--f-mono);font-size:11px;color:var(--faint);font-weight:400}"
    ".narr-arc p{margin:0;font-family:var(--f-story);font-size:13.5px;line-height:1.65;color:var(--text)}"
)
rp(".entry.guide .b,.sub.guide{", NARR_CSS + ".entry.guide .b,.sub.guide{")

# 7. UI: addEntry story rendering, War Chronicle button on #pairsCard, & warReport Chronicle section
rp(
"const sub=document.createElement('span'); sub.className='sub '+e.k; sub.textContent=e.t;",
"const sub=document.createElement('span'); sub.className='sub '+e.k; sub.textContent=(e.k==='story'&&e.fact&&typeof Sim.narrBeat==='function')?Sim.narrBeat(e.fact,typeof LANG==='string'?LANG:'ko',tr):e.t;"
)
rp(
"} else { b.textContent=e.t; { const fh=lineFace(e);",
"} else { b.textContent=(e.k==='story'&&e.fact&&typeof Sim.narrBeat==='function')?Sim.narrBeat(e.fact,typeof LANG==='string'?LANG:'ko',tr):e.t; { const fh=lineFace(e);"
)
rp(
'<div class="card hidden" id="pairsCard"><h3 title="눌러서 자세히"><span id="pairsTitle">같은 성배를 다투는 일곱 조</span> <small id="pairsLeft"></small></h3><div class="pairs" id="pairs"></div></div>',
'<div class="card hidden" id="pairsCard"><h3 title="눌러서 자세히" style="display:flex;align-items:center;gap:6px"><span id="pairsTitle">같은 성배를 다투는 일곱 조</span> <small id="pairsLeft"></small><button type="button" class="narr-btn" id="narrOpenBtn">전쟁 서사</button></h3><div class="pairs" id="pairs"></div></div>'
)
rp(
"function riskHtml(p){",
"function narrHtml(N, isEnd){ if(!N) return ''; const arcs=N.arcs||[];\n"
"  const body=arcs.length?arcs.map(a=>`<div class=\"narr-arc ${a.kind}\"><h5><span>${esc(a.title)}</span><small>${a.days&&a.days.length?`D${a.days[0]}${a.days[1]&&a.days[1]!==a.days[0]?'–'+a.days[1]:''}`:''}</small></h5><p>${esc(a.body)}</p></div>`).join(''):`<p class=\"nodata\">${esc(tr(isEnd?'아직 뚜렷한 이야기가 엮이지 않았습니다.':'아직 기록된 사건이 부족합니다. 전쟁이 깊어지면 사건들이 하나의 서사로 이어집니다.'))}</p>`;\n"
"  return `<div class=\"narr-box\" data-notr><div class=\"narr-title\">${esc(N.title)}</div>${body}</div>`; }\n"
"function showNarrative(){ const N=Sim.narrative(typeof LANG==='string'?LANG:'ko',tr); if(!N) return;\n"
"  $('#infoBody').innerHTML=`<div class=\"eyebrow\">${esc(tr('전쟁 서사'))}</div>${narrHtml(N,false)}`;\n"
"  if($('#info').classList.contains('hidden')){ infoHeld=!Sim.S.paused; if(infoHeld){ Sim.S.paused=true; syncCtrl(); } clearTimeout(autoTimer); }\n"
"  $('#info').classList.remove('hidden'); }\n"
"document.addEventListener('click',e=>{ if(e.target.closest('#narrOpenBtn')){ e.stopPropagation(); showNarrative(); } });\n"
"function riskHtml(p){"
)
rp(
"    <h4>14일의 기록</h4><details open>",
"    ${(()=>{ const N=Sim.narrativeFrom(wd,typeof LANG==='string'?LANG:'ko',typeof tr==='function'?tr:x=>x); return N&&N.arcs&&N.arcs.length?`<h4>그 겨울의 서사</h4>${narrHtml(N,true)}`:''; })()}\n    <h4>14일의 기록</h4><details open>"
)

if miss:
    for x in miss:
        print('못 찾음', x)
    sys.exit(1)

open(P, 'w', encoding='utf-8').write(s)
print('narr1125 적용 끝')

# Update i18n
from narr_lines import D, T
zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh', 'done.json')
if os.path.exists(zp):
    Z = json.load(open(zp, encoding='utf-8'))
    nz = 0
    for a, _b, _c, d, e in D + T:
        if a not in Z:
            Z[a] = [d, e]
            nz += 1
    if nz:
        json.dump(Z, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('zh/done.json 추가', nz)

if re.search(r'const I18N_DICT=\{en:\{', s):
    import i18n
    s, nd, nt = i18n.add(s, [(a, b, c) for a, b, c, *_ in D], [(a, b, c) for a, b, c, *_ in T])
    open(P, 'w', encoding='utf-8').write(s)
    print('인라인 사전 추가', nd, nt)
else:
    base_dir = os.path.dirname(os.path.abspath(P))
    i18n_dir = os.path.join(base_dir, 'assets', 'i18n')
    if os.path.isdir(i18n_dir):
        for lg, var, idx in (('en', 'I18N_EN', 1), ('ja', 'I18N_JA', 2)):
            fp = os.path.join(i18n_dir, lg + '.js')
            if not os.path.exists(fp): continue
            txt = open(fp, encoding='utf-8').read()
            m1 = re.search(r'window\.' + var + r'=(\{.*?\});\nwindow\.' + var + r'_T=(\[.*?\]);', txt, re.S)
            if not m1: continue
            dic = json.loads(m1.group(1))
            tpl = json.loads(m1.group(2))
            nd = 0
            for row in D:
                if row[0] not in dic:
                    dic[row[0]] = row[idx]
                    nd += 1
            body = txt[:m1.start(1)] + json.dumps(dic, ensure_ascii=False, separators=(',', ':')) + ';\nwindow.' + var + '_T=' + json.dumps(tpl, ensure_ascii=False, separators=(',', ':')) + ';' + txt[m1.end(2)+1:]
            open(fp, 'w', encoding='utf-8').write(body)
            h = hashlib.md5(body.encode('utf-8')).hexdigest()[:8]
            s = re.sub(r'assets/i18n/' + lg + r'\.js\?v=[0-9a-f]+', f'assets/i18n/{lg}.js?v={h}', s)
            print(f'{lg}.js 추가 {nd}, hash {h}')
        for lg, idx in (('zhs', 3), ('zht', 4)):
            fp = os.path.join(i18n_dir, lg + '.js')
            if not os.path.exists(fp): continue
            txt = open(fp, encoding='utf-8').read()
            m = re.search(r'window\.I18N_ZH=(\{.*\});?\s*$', txt, re.S)
            if not m: continue
            obj = json.loads(m.group(1))
            dic = obj.get('d', {})
            nd = 0
            for row in D:
                if row[0] not in dic:
                    dic[row[0]] = row[idx]
                    nd += 1
            obj['d'] = dic
            body = txt[:m.start(1)] + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + ';\n'
            open(fp, 'w', encoding='utf-8').write(body)
            h = hashlib.md5(body.encode('utf-8')).hexdigest()[:8]
            s = re.sub(r"\{zhs:'([0-9a-f]+)',zht:'([0-9a-f]+)'\}", lambda m2: f"{{zhs:'{h if lg=='zhs' else m2.group(1)}',zht:'{h if lg=='zht' else m2.group(2)}'}}", s)
            print(f'{lg}.js 추가 {nd}, hash {h}')
        open(P, 'w', encoding='utf-8').write(s)
