"""중국어 간체(zhs) · 번체(zht)를 게임에 넣는다 (11-16).
- 번역 사전은 게임 파일에 넣지 않고 public/assets/i18n/zhs.js · zht.js로 따로 둔다(중국어를 고른 사람만 받는다).
  로딩 화면 스크립트가 언어를 보고 그 파일을 먼저 불러온다. 사전에 없는 문장은 영어로 보인다.
- 엔진: 언어 목록 · 글꼴 · 문장 부호(CJK 붙여 쓰기 · 따옴표) · 사람 이름 · 숫자 틀 · 판정 칩 · 화면 문구 · 로비 문구.
- 공개 전(ZH_ON=false): 언어 창에 보이지 않고, 브라우저 언어로 고르지 않는다. 주소 뒤 ?lang=zhs · ?lang=zht로만 켤 수 있다.
사용: python3 dev/zh/zh_apply.py <game.html> [--on]   (--on: 공개 — 언어 창 · 자동 선택 켜기)
"""
import sys, os, re, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import zh_data as Z

args = [a for a in sys.argv[1:] if not a.startswith('--')]; ON = '--on' in sys.argv
P = args[0]
s = open(P, encoding='utf-8').read()

miss = []
def rp(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: miss.append((o[:90], k)); return
    s = s.replace(o, n)
def js(x): return "'" + x.replace('\\', '\\\\').replace("'", "\\'") + "'"

# ---- ① 사전 파일 ----
done = json.load(open(os.path.join(HERE, 'done.json'), encoding='utf-8'))
D = json.loads(re.search(r'const I18N_DICT=(\{.*?\});\n', s, re.S).group(1))
T = json.loads(re.search(r'const I18N_TPL=(\{.*?\});\n', s, re.S).group(1))
ver = {}
out_dir = os.path.join(os.path.dirname(os.path.abspath(P)), 'assets', 'i18n')
if not os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(P)), 'assets')):
    out_dir = os.path.join(ROOT, 'public', 'assets', 'i18n')
os.makedirs(out_dir, exist_ok=True)
for li, lg in ((0, 'zhs'), (1, 'zht')):
    d = {k: done[k][li] for k in D['en'] if k in done}
    # 첫 자리가 끼워 넣는 말인데 중국어에서는 그 말이 문장 가운데로 가는 틀: 앞 문장까지 삼키지 않게 한 문장만 받는다(x)
    t = []
    for x in T['en']:
        if x[0] not in done: continue
        v = done[x[0]][li]; e = [x[0], v] + x[2:]
        if re.match(r'\{0[~}]', x[0]) and not v.startswith('{0}') and not (len(e) > 2 and e[2]):
            e = e[:2] + [1]
        t.append(e)
    body = '/* 성배가 차는 밤 — 중국어 ' + ('간체' if lg == 'zhs' else '번체') + ' 사전 (dev/zh/zh_apply.py가 만든다) */\nwindow.I18N_ZH=' + json.dumps({'d': d, 't': t}, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(out_dir, lg + '.js'), 'w', encoding='utf-8').write(body)
    ver[lg] = hashlib.md5(body.encode('utf-8')).hexdigest()[:8]
    print(lg, '사전', len(d), '틀', len(t), f'{len(body.encode())/1e6:.1f}MB')

# 이미 넣은 파일: 사전 파일만 새로 만들고 불러오는 주소의 버전을 바꾼다 (--on이면 공개로)
if 'const ZH_ON=' in s:
    s = re.sub(r"\{zhs:'[0-9a-f]{8}',zht:'[0-9a-f]{8}'\}\[L\]", "{zhs:'" + ver['zhs'] + "',zht:'" + ver['zht'] + "'}[L]", s)
    if ON: s = s.replace('const ZH_ON=false;', 'const ZH_ON=true;').replace('const ZO=false,', 'const ZO=true,')
    open(P, 'w', encoding='utf-8').write(s); print('사전만 새로 만듦' + (' · 공개' if ON else '')); sys.exit(0)

# ---- ② 로딩 화면: 언어 읽기 + 중국어 사전 불러오기 ----
rp("(()=>{let L='ko';try{const v=JSON.parse(localStorage.getItem('cupnight.lang')||'null');if(['ko','en','ja'].includes(v))L=v;else{const n=((navigator.languages&&navigator.languages[0])||navigator.language||'ko').toLowerCase();L=n.startsWith('ko')?'ko':n.startsWith('ja')?'ja':'en'}}catch(e){}\n document.querySelector('#ldTxt span').textContent={ko:'성배에 마력이 차오른다',en:'Mana is filling the Grail',ja:'聖杯に魔力が満ちていく'}[L];})();",
   "(()=>{let L='ko';const ZO=false,LS=['ko','en','ja','zhs','zht'];try{const q=new URLSearchParams(location.search).get('lang');if(LS.includes(q))localStorage.setItem('cupnight.lang',JSON.stringify(q));const v=JSON.parse(localStorage.getItem('cupnight.lang')||'null');if(LS.includes(v))L=v;else{const n=((navigator.languages&&navigator.languages[0])||navigator.language||'ko').toLowerCase();L=n.startsWith('ko')?'ko':n.startsWith('ja')?'ja':(ZO&&n.startsWith('zh'))?(/hant|tw|hk|mo/.test(n)?'zht':'zhs'):'en'}}catch(e){}\n"
   " if(L==='zhs'||L==='zht') document.write('<script src=\"assets/i18n/'+L+'.js?v='+{zhs:'" + ver['zhs'] + "',zht:'" + ver['zht'] + "'}[L]+'\"><\\/script>');\n"
   " document.querySelector('#ldTxt span').textContent={ko:'성배에 마력이 차오른다',en:'Mana is filling the Grail',ja:'聖杯に魔力が満ちていく',zhs:'魔力正在注满圣杯',zht:'魔力正在注滿聖杯'}[L];})();")

# ---- ③ 언어 목록 · 사전 ----
rp("const LANGS=['ko','en','ja'];", "const LANGS=['ko','en','ja','zhs','zht'];\nconst ZH_ON=false;   // 중국어 공개 전: 언어 창에 없고 자동으로 고르지 않는다(주소 ?lang=zhs · zht로만) — zh_apply.py --on으로 켠다")
rp("  return n.startsWith('ko')?'ko':n.startsWith('ja')?'ja':'en'; })();",
   "  return n.startsWith('ko')?'ko':n.startsWith('ja')?'ja':(ZH_ON&&n.startsWith('zh'))?(/hant|tw|hk|mo/.test(n)?'zht':'zhs'):'en'; })();\n"
   "const ZH=LANG==='zhs'||LANG==='zht', CJK=ZH||LANG==='ja';\n"
   "const _ZHD=ZH&&typeof window!=='undefined'&&window.I18N_ZH||null;   // 중국어 사전(따로 불러온 파일). 없는 문장은 영어로")
rp("const I18N_D=(typeof I18N_DICT!=='undefined'&&I18N_DICT[LANG])||{};",
   "const I18N_D=ZH?Object.assign({},(typeof I18N_DICT!=='undefined'&&I18N_DICT.en)||{},_ZHD?_ZHD.d:{}):((typeof I18N_DICT!=='undefined'&&I18N_DICT[LANG])||{});")

# ---- ④ 숫자 틀(I18N_PAT) ----
m = re.search(r'const I18N_PAT=\[\n(.*?)\n\];', s, re.S)
lines = m.group(1).split('\n'); assert len(lines) == len(Z.PAT), (len(lines), len(Z.PAT))
nl = []
for ln, (a, b) in zip(lines, Z.PAT):
    assert ln.endswith("'}],"), ln
    nl.append(ln[:-3] + ', zhs:' + js(a) + ', zht:' + js(b) + '}],')
s = s[:m.start(1)] + '\n'.join(nl) + s[m.end(1):]

# ---- ⑤ 사람 이름 ----
m = re.search(r'const I18N_NAMES=(\{.*?\});\n', s)
N = json.loads(m.group(1))
for k, v in N.items(): v += list(Z.NAMES[k])
s = s[:m.start(1)] + json.dumps(N, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]
rp("const _ZH_SUR={'장':['Zhang','張'],'류':['Liu','劉']};", "const _ZH_SUR={'장':['Zhang','張','z','张','張'],'류':['Liu','劉','z','刘','劉']};")
rp("  const L=LANG==='ja'?1:0;\n  if(t.includes(' ')){", "  const L=LANG==='ja'?1:LANG==='zhs'?3:LANG==='zht'?4:0;\n  if(t.includes(' ')){")
rp("const z=zh&&_ZH_SUR[p]; const e=z?[z[0],z[1],'z']:_NM[p];", "const z=zh&&_ZH_SUR[p]; const e=z||_NM[p];")
rp("    if(L&&(kinds.has('j')||kinds.has('z'))) return out.join('');", "    if(ZH) return out.join(kinds.has('w')?'·':'');\n    if(L&&(kinds.has('j')||kinds.has('z'))) return out.join('');")
rp("return L?es[1]+'・'+eg[1]:es[0]+' '+eg[0]; }", "return ZH?es[L]+eg[L]:L?es[1]+'・'+eg[1]:es[0]+' '+eg[0]; }")

# ---- ⑥ 문장 부호 · 따옴표 ----
rp("return lead+(LANG==='ja'?'「'+q.replace(/。$/,'')+'」':'“'+q+'”')+trail;", "return lead+(LANG==='ja'?'「'+q.replace(/。$/,'')+'」':LANG==='zht'?'「'+q+'」':'“'+q+'”')+trail;")
rp("if(d3!=null) return lead+d3+(LANG==='ja'?'。':'.')+trail;", "if(d3!=null) return lead+d3+(CJK?'。':'.')+trail;")
rp("LANG==='ja'?'、':', '", "CJK?'、':', '", 2)
rp("return lead+(LANG==='ja'?q.replace(/朕/g,'余'):q)+trail;", "return lead+(CJK?q.replace(/朕/g,'余'):q)+trail;")
rp("o+=(LANG==='ja'&&ok&&out[k+1][1])?'':(sep||' ');", "o+=(CJK&&ok&&out[k+1][1])?'':(sep||' ');")
rp("LANG==='ja'?'':' '", "CJK?'':' '", 3)
rp("    return LANG==='ja'?nm+'：「'+q+'」':nm+': “'+q+'”'; }", "    return LANG==='ja'||LANG==='zht'?nm+'：「'+q+'」':LANG==='zhs'?nm+'：“'+q+'”':nm+': “'+q+'”'; }")
rp("  return nm+(LANG==='ja'?'：':': ')+b; }", "  return nm+(CJK?'：':': ')+b; }")

# 중국어: 문장 부호 뒤 띄어쓰기 지우기
rp("let r=_tr1(s); if(LANG==='ja') r=r.replace(/。」/g,'」').replace(/。）/g,'）');", "let r=_tr1(s); if(LANG==='ja') r=r.replace(/。」/g,'」').replace(/。）/g,'）'); if(ZH) r=r.replace(/([。！？」”』…])[ ]+(?=\\S)/g,'$1');")

# 중국어: 한 문장만 받는 틀(x)이 앞 문장 때문에 안 맞으면, 뒤쪽에 틀을 맞추고 앞 문장들은 따로 옮긴다(맨 바깥에서만)
rp("  { const v=_trTpl(t); if(v!=null) return lead+v+trail; }\n",
   "  { const v=_trTpl(t); if(v!=null) return lead+v+trail; }\n"
   "  if(ZH&&!_tplDepth){ const re=/[.!?…”」]\\s+/g; let mm; while((mm=re.exec(t))){ const k=mm.index+mm[0].length, tail=t.slice(k); if(!tail) break; const v=_trTpl(tail); if(v==null||HANGUL.test(v)) continue; const h=tr(t.slice(0,k).trim()); if(!HANGUL.test(h)) return lead+h+v+trail; } }\n")

# ---- ⑦ 문장 틀: 대명사 · 사전 ----
rp("const _PRON={'그':{he:'he',him:'him',his:'his',He:'He',His:'His',ja:'彼'},'그녀':{he:'she',him:'her',his:'her',He:'She',His:'Her',ja:'彼女'}};",
   "const _PRON={'그':{he:'he',him:'him',his:'his',He:'He',His:'His',ja:'彼',zh:'他'},'그녀':{he:'she',him:'her',his:'her',He:'She',His:'Her',ja:'彼女',zh:'她'}};")
rp("const L=(typeof I18N_TPL!=='undefined'&&I18N_TPL[LANG])||[];",
   "const L=ZH?(()=>{ const z=_ZHD?_ZHD.t:[], h=new Set(z.map(x=>x[0])); return z.concat(((typeof I18N_TPL!=='undefined'&&I18N_TPL.en)||[]).filter(x=>!h.has(x[0]))); })():((typeof I18N_TPL!=='undefined'&&I18N_TPL[LANG])||[]);")
rp("if(p) return LANG==='ja'?p.ja:(p[f]||q); }", "if(p) return LANG==='ja'?p.ja:ZH?p.zh:(p[f]||q); }")

# ---- ⑧ 판정 칩 ----
m = re.search(r'const I18N_CHIP=\{\n(.*?)\n\};', s, re.S)
nl = []
for ln in m.group(1).split('\n'):
    k = re.match(r"^ '(.*?)':", ln).group(1); a, b = Z.CHIP[k]
    assert ln.endswith("'},"), ln
    nl.append(ln[:-2] + ',zhs:' + js(a) + ',zht:' + js(b) + '},')
s = s[:m.start(1)] + '\n'.join(nl) + s[m.end(1):]
rp("  const L=LANG==='ja'?'ja':'en'; let ok=true;", "  const L=CJK?LANG:'en'; let ok=true;")
rp("    const q=L==='ja'?xs.map(x=>'「'+x+'」'):xs.map(x=>'“'+x+'”');\n    return L==='ja'?q.join('と'):",
   "    const q=CJK?xs.map(x=>'「'+x+'」'):xs.map(x=>'“'+x+'”');\n    return L==='ja'?q.join('と'):ZH?(q.length<3?q.join('和'):q.slice(0,-1).join('、')+'和'+q[q.length-1]):")

# ---- ⑨ 시작: html lang · 글꼴 · 제목 ----
rp("  document.documentElement.lang=LANG;", "  document.documentElement.lang={zhs:'zh-Hans',zht:'zh-Hant'}[LANG]||LANG;")
rp("&display=swap'; document.head.appendChild(l); }\n  const T={en:'The Night the Grail Fills',ja:'聖杯が満ちる夜'}[LANG]; document.title=T;",
   "&display=swap'; document.head.appendChild(l); }\n"
   "  if(ZH){ const f=LANG==='zht'?'TC':'SC', l=document.createElement('link'); l.rel='stylesheet'; l.href='https://fonts.googleapis.com/css2?family=Noto+Serif+'+f+':wght@400;600&family=Noto+Sans+'+f+':wght@400;500;600&display=swap'; document.head.appendChild(l); }\n"
   "  const T={en:'The Night the Grail Fills',ja:'聖杯が満ちる夜',zhs:'圣杯满溢之夜',zht:'聖杯滿溢之夜'}[LANG]; document.title=T;")
rp("ja:'聖杯が<br>満ちる<em>夜</em>'}[LANG];", "ja:'聖杯が<br>満ちる<em>夜</em>',zhs:'圣杯<br>满溢<em>之夜</em>',zht:'聖杯<br>滿溢<em>之夜</em>'}[LANG];")
rp("ja:'日本語訳は追加されたばかりです。不自然な表現や韓国語のまま残っている文章があれば、お知らせください。'}[LANG];",
   "ja:'日本語訳は追加されたばかりです。不自然な表現や韓国語のまま残っている文章があれば、お知らせください。',zhs:'中文翻译刚刚加入。如果发现不自然的表达，或仍是韩语、英语的文字，请告诉我们。',zht:'中文翻譯剛剛加入。如果發現不自然的表達，或仍是韓文、英文的文字，請告訴我們。'}[LANG];")

# ---- ⑩ 화면 문구(계절 · 출신 장면 · 이름 짓기) ----
rp("ja:['春','夏','秋','冬']};", "ja:['春','夏','秋','冬'],zhs:['春','夏','秋','冬'],zht:['春','夏','秋','冬']};")
rp("LANG==='ja'?`${y}年、${n}`:", "LANG==='ja'?`${y}年、${n}`:ZH?`${y}年${n}`:")
rp("""date:(y,m,d)=>`${y}年${m}月${d}日`},
}[LANG]||null;""", """date:(y,m,d)=>`${y}年${m}月${d}日`},
  zhs:{exo:g=>`退魔 · 第${g}代`,house:s=>`${s}家`,gen:(g,f)=>f?`第${g}代 · 书库与债务`:`第${g}代 · 三百年`,eldest:'长嗣',register:'洗礼名册',cert:'出 生 证 明',f:['姓名','出生日期','出生地点'],stamp:'受理',date:(y,m,d)=>`${y}年${m}月${d}日`},
  zht:{exo:g=>`退魔 · 第${g}代`,house:s=>`${s}家`,gen:(g,f)=>f?`第${g}代 · 書庫與債務`:`第${g}代 · 三百年`,eldest:'長嗣',register:'洗禮名冊',cert:'出 生 證 明',f:['姓名','出生日期','出生地點'],stamp:'受理',date:(y,m,d)=>`${y}年${m}月${d}日`},
}[LANG]||null;""")
rp("""lead:sx=>`${sx==='f'?'女の子':'男の子'}が生まれた。名前をつけてください。`},
}[LANG]||null;""", """lead:sx=>`${sx==='f'?'女の子':'男の子'}が生まれた。名前をつけてください。`},
  zhs:{skip:'跳过',sur:'姓',given:'名',dice:'换个名字',ok:'就用这个名字',fix:'下次也用这个名字',nofx:'下次起跳过开场演出',aria:'降生',lead:sx=>`${sx==='f'?'女孩':'男孩'}出生了。请为孩子取个名字。`},
  zht:{skip:'跳過',sur:'姓',given:'名',dice:'換個名字',ok:'就用這個名字',fix:'下次也用這個名字',nofx:'下次起跳過開場演出',aria:'降生',lead:sx=>`${sx==='f'?'女孩':'男孩'}出生了。請為孩子取個名字。`},
}[LANG]||null;""")
rp("""concat(LANG==='ja'?["16px 'Noto Serif JP'","16px 'Noto Sans JP'"]:[]);""",
   """concat(LANG==='ja'?["16px 'Noto Serif JP'","16px 'Noto Sans JP'"]:ZH?["16px 'Noto Serif "+(LANG==='zht'?'TC':'SC')+"'","16px 'Noto Sans "+(LANG==='zht'?'TC':'SC')+"'"]:[]);""")
rp("const disp=v=>{ if(LANG==='ko'||!v) return v; const k=LANG==='ja'?1:0;", "const disp=v=>{ if(LANG==='ko'||!v) return v; const k=LANG==='ja'?1:LANG==='zhs'?3:LANG==='zht'?4:0;")
rp("if(LANG==='ja'&&a&&b&&kana.test(a)&&kana.test(b)&&S.city.loc!=='ja') v=L.order==='sg'?a+'・'+b:b+'・'+a; else v=Sim.fullName(a,b);",
   "if(LANG==='ja'&&a&&b&&kana.test(a)&&kana.test(b)&&S.city.loc!=='ja') v=L.order==='sg'?a+'・'+b:b+'・'+a; else if(ZH&&a&&b&&!/[가-힣]/.test(a+b)&&!['ko','ja','zh'].includes(S.city.loc)) v=L.order==='sg'?a+'·'+b:b+'·'+a; else v=Sim.fullName(a,b);")
# 캔버스 글꼴: 일본어 글꼴 뒤에 중국어 글꼴(받은 쪽만 쓰인다)
rp("'Noto Serif JP', ", "'Noto Serif JP', 'Noto Serif SC', 'Noto Serif TC', ", 18)
rp("'Noto Sans JP', ", "'Noto Sans JP', 'Noto Sans SC', 'Noto Sans TC', ", 8)
# CSS
rp(".lang-en .title{font-size:clamp(40px,6vw,64px)}",
   ".lang-zhs{--f-display:'Noto Serif SC','Song Myung','Gowun Batang',serif;--f-story:'Noto Serif SC','Gowun Batang',serif;--f-ui:'Noto Sans SC','IBM Plex Sans KR',system-ui,sans-serif}\n"
   ".lang-zht{--f-display:'Noto Serif TC','Song Myung','Gowun Batang',serif;--f-story:'Noto Serif TC','Gowun Batang',serif;--f-ui:'Noto Sans TC','IBM Plex Sans KR',system-ui,sans-serif}\n"
   ".lang-en .title{font-size:clamp(40px,6vw,64px)}")
rp(".lang-en .hname,.lang-ja .hname{", ".lang-en .hname,.lang-ja .hname,.lang-zhs .hname,.lang-zht .hname{")
rp(".lang-ja .title{font-size:clamp(40px,6.5vw,72px);line-height:1.15}", ".lang-ja .title,.lang-zhs .title,.lang-zht .title{font-size:clamp(40px,6.5vw,72px);line-height:1.15}")

# ---- ⑪ 서번트 말투(시구르드: 在下 · 阁下) ----
rp("""  ja:{sigurd:[[/俺|オレ|僕/g,'当方'],[/お前|おまえ|あんた|あなた|君(?![主子臨])/g,'貴殿']]}};""",
   """  ja:{sigurd:[[/俺|オレ|僕/g,'当方'],[/お前|おまえ|あんた|あなた|君(?![主子臨])/g,'貴殿']]},
  zhs:{sigurd:[[/我(?!们)/g,'在下'],[/你(?!们)/g,'阁下']]},
  zht:{sigurd:[[/我(?!們)/g,'在下'],[/你(?!們)/g,'閣下']]}};""")

# ---- ⑫ 언어 창 ----
rp("const LANG_LIST=[['ko','한국어'],['en','English'],['ja','日本語']];",
   "const LANG_LIST=[['ko','한국어'],['en','English'],['ja','日本語']].concat(ZH_ON||ZH?[['zhs','简体中文'],['zht','繁體中文']]:[]);")
rp("const LANG_SUB={ko:{ko:'한국어',en:'영어',ja:'일본어',zh:'중국어 (간체)',cur:'사용 중',t:'언어',x:'닫기'},\n"
   "  en:{ko:'Korean',en:'English',ja:'Japanese',zh:'Chinese (Simplified)',cur:'In use',t:'Language',x:'Close'},\n"
   "  ja:{ko:'韓国語',en:'英語',ja:'日本語',zh:'中国語（簡体字）',cur:'使用中',t:'言語',x:'閉じる'}};",
   "const LANG_SUB={ko:{ko:'한국어',en:'영어',ja:'일본어',zhs:'중국어 (간체)',zht:'중국어 (번체)',cur:'사용 중',t:'언어',x:'닫기'},\n"
   "  en:{ko:'Korean',en:'English',ja:'Japanese',zhs:'Chinese (Simplified)',zht:'Chinese (Traditional)',cur:'In use',t:'Language',x:'Close'},\n"
   "  ja:{ko:'韓国語',en:'英語',ja:'日本語',zhs:'中国語（簡体字）',zht:'中国語（繁体字）',cur:'使用中',t:'言語',x:'閉じる'},\n"
   "  zhs:{ko:'韩语',en:'英语',ja:'日语',zhs:'简体中文',zht:'繁体中文',cur:'使用中',t:'语言',x:'关闭'},\n"
   "  zht:{ko:'韓語',en:'英語',ja:'日語',zhs:'簡體中文',zht:'繁體中文',cur:'使用中',t:'語言',x:'關閉'}};")
rp("""<span><b lang="'+l+'">'+n+'</b>""", """<span><b lang="'+({zhs:'zh-Hans',zht:'zh-Hant'}[l]||l)+'">'+n+'</b>""")

# ---- ⑬ 로비 문구 ----
rp("""set:'設定'}}[typeof LANG==='string'&&['en','ja'].includes(LANG)?LANG:'ko'];""",
   """set:'設定'},
    zhs:{more:'这一夜的故事与规则',go:'入场',spoil:'※ 可能包含有关TYPE-MOON世界观的剧透。',none:'还没有亮灯的窗，<br>也没有升起的星。',lit:(a,b)=>`<b>${a}</b>段人生点亮了灯火，<br><b>${b}</b>位英灵化作了星辰。`,close:'关闭',snd:'声音开关',set:'设置'},
    zht:{more:'這一夜的故事與規則',go:'入場',spoil:'※ 可能包含有關TYPE-MOON世界觀的劇透。',none:'還沒有亮燈的窗，<br>也沒有升起的星。',lit:(a,b)=>`<b>${a}</b>段人生點亮了燈火，<br><b>${b}</b>位英靈化作了星辰。`,close:'關閉',snd:'聲音開關',set:'設定'}}[typeof LANG==='string'&&['en','ja','zhs','zht'].includes(LANG)?LANG:'ko'];""")
rp("const TX={ko:{c:'닫기',t:'지난 기록'},en:{c:'Close',t:'Records'},ja:{c:'閉じる',t:'これまでの記録'}}",
   "const TX={ko:{c:'닫기',t:'지난 기록'},en:{c:'Close',t:'Records'},ja:{c:'閉じる',t:'これまでの記録'},zhs:{c:'关闭',t:'过往记录'},zht:{c:'關閉',t:'過往紀錄'}}")
rp("const LG=typeof LANG==='string'&&['en','ja'].includes(LANG)?LANG:'ko';", "const LG=typeof LANG==='string'&&['en','ja','zhs','zht'].includes(LANG)?LANG:'ko';")
rp("""    title:'聖杯が満ちる<em>夜</em>'}}[LG];""", """    title:'聖杯が満ちる<em>夜</em>'},
   zhs:{tap:'点击画面开始',enter:'开始',back:'标题画面',snd:'声音开关',set:'设置',hide:'隐藏UI',show:'显示UI',cont:'继续',
    age:n=>`${n}岁`,war:(y,d,h)=>`${y}年 · 圣杯战争第${d}天${h?' · '+h:''}`,year:y=>`${y}年`,
    sub:(a,b)=>`${a}段人生 · 化作星辰的英灵 ${b}`,first:'等待第一段人生的夜晚',newLife:'新的人生',bornDesc:'在某座城市、随机决定的家庭里，仅此一次的人生开始了。',
    scn:'剧本',scnSub:'改变圣杯战争走向的事件设置',bond:'羁绊召唤',bondSub:n=>`从契约过的${n}名从者中选择`,none:'不选择',grail:'由圣杯选择',sure:'必定',pct:n=>`约${n}%`,
    locked:'未解锁',lockedPc:'首次契约后解锁',lockHint:'与从者缔结契约并结束一段人生后解锁。选好那位从者，召唤时便能再次呼唤。',
    dex:'从者图鉴',lives:'往生记录',ach:'成就',sent:'派出的组',livesN:n=>`${n}段人生`,
    contracted:n=>`契约过的从者 ${n}名`,tip:'选好往生中契约过的从者，召唤时就能不用触媒而呼唤那位从者。',
    recent:'最近的羁绊召唤',recentSub:'按最近呼唤排序',all:'契约过的从者',nP:n=>`${n}名`,q:'按名字搜索',sort:'排序',sRecent:'最近同行',sP:'抵达几率',sName:'名字',
    sureOnly:'仅限必定',cls:'职阶',allCls:'全部',help:'羁绊召唤说明',close:'关闭',empty:'没有符合条件的从者。',lastLife:'上一段人生',ago:n=>`${n}段人生之前`,
    title:'圣杯满溢<em>之夜</em>'},
   zht:{tap:'點擊畫面開始',enter:'開始',back:'標題畫面',snd:'聲音開關',set:'設定',hide:'隱藏UI',show:'顯示UI',cont:'繼續',
    age:n=>`${n}歲`,war:(y,d,h)=>`${y}年 · 聖杯戰爭第${d}天${h?' · '+h:''}`,year:y=>`${y}年`,
    sub:(a,b)=>`${a}段人生 · 化作星辰的英靈 ${b}`,first:'等待第一段人生的夜晚',newLife:'新的人生',bornDesc:'在某座城市、隨機決定的家庭裡，僅此一次的人生開始了。',
    scn:'劇本',scnSub:'改變聖杯戰爭走向的事件設定',bond:'羈絆召喚',bondSub:n=>`從契約過的${n}名從者中選擇`,none:'不選擇',grail:'由聖杯選擇',sure:'必定',pct:n=>`約${n}%`,
    locked:'未解鎖',lockedPc:'首次契約後解鎖',lockHint:'與從者締結契約並結束一段人生後解鎖。選好那位從者，召喚時便能再次呼喚。',
    dex:'從者圖鑑',lives:'往生紀錄',ach:'成就',sent:'派出的組',livesN:n=>`${n}段人生`,
    contracted:n=>`契約過的從者 ${n}名`,tip:'選好往生中契約過的從者，召喚時就能不用觸媒而呼喚那位從者。',
    recent:'最近的羈絆召喚',recentSub:'按最近呼喚排序',all:'契約過的從者',nP:n=>`${n}名`,q:'按名字搜尋',sort:'排序',sRecent:'最近同行',sP:'抵達機率',sName:'名字',
    sureOnly:'僅限必定',cls:'職階',allCls:'全部',help:'羈絆召喚說明',close:'關閉',empty:'沒有符合條件的從者。',lastLife:'上一段人生',ago:n=>`${n}段人生之前`,
    title:'聖杯滿溢<em>之夜</em>'}}[LG];""")

if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
if ON: s = s.replace('const ZH_ON=false;', 'const ZH_ON=true;').replace('const ZO=false,', 'const ZO=true,')
open(P, 'w', encoding='utf-8').write(s)
print('적용 끝', P, '(공개)' if ON else '(숨김)')
