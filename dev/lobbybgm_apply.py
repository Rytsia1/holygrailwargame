"""로비 배경음악 5곡 (11-15)
- 예전 로비 곡(title) 한 곡을 새로 지은 다섯 곡으로 바꾼다. 로비 화면으로 들어올 때마다 한 곡을 무작위로 고르고,
  바로 앞에 나온 곡은 다시 고르지 않는다. 로비에 머무는 동안은 같은 곡이 계속 반복된다.
  lobby1 봄밤의서약 · lobby2 남은온기 · lobby3 마지막빛 · lobby4 꿈의가장자리 · lobby5 밤의맹세
  (멜로디 · 화성은 새로 썼고, 템포 · 구성 · 세기 흐름 · 악기 짜임만 참고곡에서 재서 맞췄다. 파일은 assets/sound/lobby1~5.mp3, −18 LUFS · 160kbps)
- 반복 지점(ls · le)은 렌더할 때 잰 값. lobby1만 머리 8마디(약 21.5초)가 있고 나머지는 처음 4.5~5초 뒤부터가 반복 구간.
사용: python3 lobbybgm_apply.py <game.html>"""
import sys
M = {   # 키: (wav 길이, 반복 시작, 반복 끝)
    'lobby1': (101.972, 26.208, 101.472),
    'lobby2': (92.244, 4.512, 91.744),
    'lobby3': (85.908, 5.024, 85.408),
    'lobby4': (90.932, 5.024, 90.432),
    'lobby5': (97.864, 4.82, 97.364),
}
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp('"title":{"d":124.21,"ls":10.558,"le":123.71},',
       ''.join('"%s":{"d":%s,"ls":%s,"le":%s},' % (k, d, a, b) for k, (d, a, b) in M.items()))
    rp("function sndScene(){\n  if(!$('#ending').classList.contains('hidden')) return Snd.endKey()||'end_b';\n  if(!$('#intro').classList.contains('hidden')) return 'title';",
       "// 로비 곡: 로비로 들어올 때마다 한 곡을 무작위로(바로 앞 곡은 빼고), 머무는 동안은 그대로\n"
       "const LB_KEYS=['lobby1','lobby2','lobby3','lobby4','lobby5']; let lbK=null, lbLast=null;\n"
       "function lobbyBgm(){ if(!lbK){ const c=LB_KEYS.filter(k=>k!==lbLast); lbK=c[Math.floor(Math.random()*c.length)]; lbLast=lbK; } return lbK; }\n"
       "function sndScene(){\n  if($('#intro').classList.contains('hidden')) lbK=null;\n"
       "  if(!$('#ending').classList.contains('hidden')) return Snd.endKey()||'end_b';\n  if(!$('#intro').classList.contains('hidden')) return lobbyBgm();")
    print('lobbybgm miss', miss)
    if miss: sys.exit(1)
    open(P, 'w', encoding='utf-8').write(s)
