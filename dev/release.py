"""11-22: 공개 파일 만들기 — dev/build/game.html → public/index.html (예전의 cp를 대신한다)
- 영어 · 일본어 번역 사전(I18N_DICT, 약 8.8MB)과 문장 틀(I18N_TPL, 약 2.4MB, 11-22 밤)을 게임 파일에서 떼어 public/assets/i18n/en.js · ja.js로 둔다.
  로딩 화면 스크립트가 고른 언어의 사전만 받는다: 영어 · 중국어(없는 문장은 영어로) → en.js, 일본어 → ja.js, 한국어 → 받지 않음
- 주소에 내용 해시(?v=)를 붙여, 사전이 바뀌면 새로 받고 아니면 캐시를 쓴다
- dev/build/game.html은 그대로 둔다(시험 스크립트가 사전을 그 파일에서 읽는다)
사용: python3 dev/release.py"""
import os, json, hashlib, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(R, 'dev/build/game.html'), encoding='utf-8').read()
a = s.find('const I18N_DICT='); b = s.find(';\n', a)
if a < 0 or s.count('const I18N_DICT=') != 1: sys.exit('I18N_DICT 못 찾음')
D = json.loads(s[a + len('const I18N_DICT='):b])
assert set(D) == {'en', 'ja'}, D.keys()
# 문장 틀(I18N_TPL, 약 2.4MB)도 같은 파일로
ta = s.find('const I18N_TPL='); tb = s.find(';\n', ta)
if ta < 0 or s.count('const I18N_TPL=') != 1: sys.exit('I18N_TPL 못 찾음')
TP = json.loads(s[ta + len('const I18N_TPL='):tb])
assert set(TP) == {'en', 'ja'}, TP.keys()
ver = {}
for lg, var in (('en', 'I18N_EN'), ('ja', 'I18N_JA')):
    body = ('/* 성배가 차는 밤 — ' + ('영어' if lg == 'en' else '일본어') + ' 사전 · 문장 틀 (dev/release.py가 game.html에서 떼어 냄) */\nwindow.' + var + '=' + json.dumps(D[lg], ensure_ascii=False, separators=(',', ':')) + ';\n'
            + 'window.' + var + '_T=' + json.dumps(TP[lg], ensure_ascii=False, separators=(',', ':')) + ';\n')
    open(os.path.join(R, 'public/assets/i18n', lg + '.js'), 'w', encoding='utf-8').write(body)
    ver[lg] = hashlib.md5(body.encode('utf-8')).hexdigest()[:8]
    print(lg, len(D[lg]), '줄', f'{len(body.encode())/1e6:.1f}MB', ver[lg])
s = s[:ta] + "const I18N_TPL={en:(typeof window!=='undefined'&&window.I18N_EN_T)||[],ja:(typeof window!=='undefined'&&window.I18N_JA_T)||[]};   // 문장 틀은 assets/i18n/en.js · ja.js (dev/release.py)" + s[tb:]
a = s.find('const I18N_DICT='); b = s.find(';\n', a)
s = s[:a] + "const I18N_DICT={en:(typeof window!=='undefined'&&window.I18N_EN)||{},ja:(typeof window!=='undefined'&&window.I18N_JA)||{}};   // 사전은 assets/i18n/en.js · ja.js (dev/release.py)" + s[b:]
o = " if(L==='zhs'||L==='zht') document.write("
if s.count(o) != 1: sys.exit('로딩 스크립트 자리 못 찾음')
s = s.replace(o, " if(L==='en'||L==='zhs'||L==='zht') document.write('<script src=\"assets/i18n/en.js?v=" + ver['en'] + "\"><\\/script>');"
                 " if(L==='ja') document.write('<script src=\"assets/i18n/ja.js?v=" + ver['ja'] + "\"><\\/script>');\n" + o)
open(os.path.join(R, 'public/index.html'), 'w', encoding='utf-8').write(s)
print('public/index.html', f'{len(s.encode())/1e6:.1f}MB')
