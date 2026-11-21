"""테스트용 HTML 한 장 만들기: 로비 하늘 · 초상화를 파일 안에 넣어, 내려받아 바로 열어도 그림이 나오게 한다.
--sound를 붙이면 소리 파일(assets/sound/*.mp3)도 모두 파일 안에 넣는다(풀사운드, 파일이 100MB 넘게 커짐).
테스트 조절판(test_panel.js)도 이 파일에만 넣는다: 전투 보정 · 마스터 스탯 · 서번트 상태 · 서번트 · 위기 고정 · 빠른 배속.
사용: python3 dev/mktest.py public/index.html dev/build/test.html"""
import sys, os, base64, re, json
args = [a for a in sys.argv[1:] if not a.startswith('--')]; SOUND = '--sound' in sys.argv
src, out = args[0], args[1]
A = os.path.join(os.path.dirname(os.path.abspath(src)), 'assets')
s = open(src, encoding='utf-8').read(); miss = []
du = lambda p: 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
# 얼굴 모음(CSS)
n = len(re.findall(r"url\(assets/portraits/faces72\.webp(\?v=\d+)?\)", s))
s = re.sub(r"url\(assets/portraits/faces72\.webp(\?v=\d+)?\)", 'url(' + du(os.path.join(A, 'portraits', 'faces72.webp')) + ')', s)
if not n: miss.append('faces72')
# 일러스트 초상화
P = {f[:-5]: du(os.path.join(A, 'portraits', f)) for f in os.listdir(os.path.join(A, 'portraits')) if f.endswith('.webp') and f != 'faces72.webp'}
o = "--img:url(assets/portraits/${id}.webp)"
if o in s: s = s.replace(o, "--img:url(${(window.__PORT||{})[id]||'assets/portraits/'+id+'.webp'})")
else: miss.append('portrait tpl')
# 로비 하늘
L = {f[:-5]: du(os.path.join(A, 'lobby', f)) for f in os.listdir(os.path.join(A, 'lobby')) if f.endswith('.webp')}
o = "im.src='assets/lobby/'+B.f+'.webp'"
if o in s: s = s.replace(o, "im.src=(window.__LOBBY||{})[B.f]||'assets/lobby/'+B.f+'.webp'")
else: miss.append('lobby')
pre = '<script>window.__PORT=' + json.dumps(P) + ';window.__LOBBY=' + json.dumps(L) + ';</script>\n'
s = s.replace('<body>\n', '<body>\n' + pre, 1)
# 테스트 조절판: 내 판정 보정 자리를 엔진에 하나 열고, 조절판 스크립트를 맨 끝에 붙인다
o = "+npFxP(b,'me'); b.judged=false;"
if s.count(o) == 1: s = s.replace(o, "+npFxP(b,'me')+((globalThis.__TEST&&globalThis.__TEST.pow)||0); if(globalThis.__TEST&&globalThis.__TEST.hook) globalThis.__TEST.hook(w,e); b.judged=false;")
else: miss.append('judge hook')
TP = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_panel.js'), encoding='utf-8').read()
# 번역기가 켜지기 전에 실행되도록 화면 스크립트 앞에 둔다(뒤에 붙이면 번역기가 스크립트 글자까지 옮기려다 멈춘다)
k = s.index('(() => {\nconst $=s=>document.querySelector(s);'); a = s.rindex('<script>', 0, k)
s = s[:a] + '<script>\n' + TP + '\n</script>\n' + s[a:]
# 캡처하기(11-14): 파일 하나로 열 때는 assets/js를 못 읽으므로 html2canvas를 파일 안에 넣는다
H2 = os.path.join(os.path.dirname(os.path.abspath(src)), 'assets', 'js', 'html2canvas.min.js')
if os.path.exists(H2):
    a = s.rindex('<script>', 0, s.index('(() => {\nconst $=s=>document.querySelector(s);'))
    s = s[:a] + '<script>\n' + open(H2, encoding='utf-8').read() + '\n</script>\n' + s[a:]
else: miss.append('html2canvas')
# 검귀 루트 바로 들어가기(조절판 단추): 전쟁 중 상태에서 성향을 깊게 하고 본성 속 진심을 시작한다
o = '  return {cn,ACH:'
if s.count(o) == 1: s = s.replace(o, "  globalThis.__KGT={start:(k,R)=>{ const w=S&&S.war; if(!w||S.phase!=='war'||!w.heroAlive) return '성배전쟁 중(서번트가 살아 있을 때)에만 쓸 수 있습니다'; if(w.kg) return '이미 검귀 루트 중입니다'; S.aff=S.aff||{}; S.aff[k]=Math.max(9,S.aff[k]||0); w.queue=[]; S.pending=null; w.ended=false; kgStart(k,null,[]); if(w.kg&&R>=0) w.kg.R=Math.max(0,Math.min(100,R)); return ''; }};\n" + o)
else: miss.append('kg hook')
# 풀사운드: 소리를 data URL로 넣고, 소리를 읽는 자리에서 먼저 그것을 쓴다
if SOUND:
    SD = os.path.join(A, 'sound'); M = {}
    for f in sorted(os.listdir(SD)):
        if f.endswith('.mp3'): M[f[:-4]] = 'data:audio/mpeg;base64,' + base64.b64encode(open(os.path.join(SD, f), 'rb').read()).decode()
    o = "fetch('assets/sound/'+k+'.mp3')"
    n = s.count(o)
    if n: s = s.replace(o, "fetch((window.__SND||{})[k]||'assets/sound/'+k+'.mp3')")
    else: miss.append('sound fetch')
    s = s.replace('<body>\n', '<body>\n<script>window.__SND=' + json.dumps(M) + ';</script>\n', 1)
    print('sound files', len(M), 'fetch sites', n)
open(out, 'w', encoding='utf-8').write(s)
print('test miss', miss, 'portraits', len(P), 'lobby', len(L), 'MB', round(len(s.encode()) / 1e6, 1))
