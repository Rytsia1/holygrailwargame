"""K1 검귀 결투 (마스터 대 서번트) 배경음악 — 오리지널 작곡.
참고곡에서 잰 것은 큰 성격뿐: 약 160BPM 4/4 · 8분음 몰아침, E♭ 단조에 ♭II(F♭)가 섞인 일본 음계 색, 150Hz 아래 몫이 큼(무거운 북 · 저음),
3kHz 위가 적은 어두운 소리, 곡 내내 세기 폭이 좁음, 한가운데 저음만 남는 짧은 숨 고르기. 선율 · 화성 · 리듬은 새로 썼다.
구성(마디, 1마디 1.5초): 도입 8 | 본문 56 = A 16 · B 16 · 숨 8 · A' 16. 본문을 두 번 그려 두 번째와 같은 자리로 되감는다.
사용: python3 k1.py <작업 폴더>"""
import sys, os, subprocess, wave, json
import numpy as np, mido
from scipy.signal import fftconvolve, butter, sosfilt

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
SR = 48000; BPM = 160; TPB = 960                 # 한 박 0.375초 = 18000샘플, 1틱 = 18.75샘플
BAR = 4 * TPB; SPT = SR * 60 / BPM / TPB          # 틱당 샘플
SF = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
INTRO, BODY = 8, 56
NB = INTRO + BODY * 2 + 2                          # 도입 + 본문 2회 + 꼬리 2마디
E8, Q, H, DQ, W = TPB // 2, TPB, TPB * 2, TPB * 3 // 2, TPB * 4

def nn(s):   # 'Eb4' → MIDI 번호 (Cb · Fb 허용)
    names = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    p = names[s[0]]; i = 1
    while i < len(s) and s[i] in 'b#': p += -1 if s[i] == 'b' else 1; i += 1
    return p + 12 * (int(s[i:]) + 1)

# ---------- 악보 ----------
T = {}   # 이름 → [(tick, dur, note, vel)]
def add(tr, t, d, n, v):
    T.setdefault(tr, []).append((int(t), int(d), n if isinstance(n, int) else nn(n), int(v)))
def line(tr, bar, seq, v=90, oct=0, leg=.95):   # seq: [(음, 길이틱)] 음 None = 쉼
    t = bar * BAR
    for n, d in seq:
        if n is not None:
            for m in (n if isinstance(n, (list, tuple)) else [n]):
                add(tr, t, d * leg, (nn(m) if isinstance(m, str) else m) + 12 * oct, v)
        t += d
    return t

# 화성(2마디 단위 근음 · 화음 음)
CH = {'Ebm': ['Eb', 'Gb', 'Bb'], 'Cb': ['Cb', 'Eb', 'Gb'], 'Abm': ['Ab', 'Cb', 'Eb'], 'Fb': ['Fb', 'Ab', 'Cb'], 'Bb': ['Bb', 'D', 'F'], 'Bbsus': ['Bb', 'Eb', 'F'],
      'Db': ['Db', 'F', 'Ab'], 'Gb': ['Gb', 'Bb', 'Db'], 'Bbm': ['Bb', 'Db', 'F']}
def tone(name, octv): return nn(name + str(octv))

# 주제(본성 속 진심): 한 음에 머물다 F♭(♭II)을 거쳐 미끄러져 내려온다
MOTIF = [('Bb4', DQ * 2), ('Cb5', E8), ('Bb4', E8), ('Ab4', Q), ('Gb4', Q), ('Fb4', Q), ('Eb4', Q)]
A_MEL = MOTIF + [('Gb4', DQ), ('Ab4', E8), ('Bb4', Q), ('Db5', Q), ('Cb5', H), ('Bb4', H),
                 ('Eb5', DQ), ('Db5', E8), ('Cb5', Q), ('Bb4', Q), ('Ab4', Q), ('Cb5', Q), ('Bb4', H),
                 ('Gb4', Q), ('F4', Q), ('Gb4', Q), ('Ab4', Q), ('Bb4', H + Q), (None, Q),
                 ('Eb5', DQ * 2), ('Fb5', E8), ('Eb5', E8), ('Db5', Q), ('Cb5', Q), ('Bb4', Q), ('Ab4', Q),
                 ('Gb4', Q), ('Ab4', Q), ('Bb4', Q), ('Cb5', Q), ('Db5', H), ('Cb5', Q), ('Bb4', Q),
                 ('Ab4', DQ), ('Gb4', E8), ('Fb4', Q), ('Gb4', Q), ('Ab4', Q), ('Bb4', Q), ('Cb5', Q), ('Db5', Q),
                 ('Eb5', H), ('Fb4', Q), ('Eb4', Q), ('Eb4', W - E8), (None, E8)]
A_HAR = ['Ebm', 'Cb', 'Abm', 'Bbsus', 'Ebm', 'Db', 'Cb', 'Ebm']
B_MEL = [('Cb5', H), ('Db5', Q), ('Eb5', Q), ('Gb5', H + Q), ('F5', Q),
         ('Eb5', Q), ('Db5', Q), ('Cb5', Q), ('Db5', Q), ('Bb4', W),
         ('Ab4', Q), ('Bb4', Q), ('Cb5', Q), ('Db5', Q), ('Eb5', H), ('Gb5', H),
         ('F5', DQ), ('Eb5', E8), ('Db5', Q), ('F5', Q), ('Eb5', W),
         ('Cb5', H), ('Db5', Q), ('Eb5', Q), ('Gb5', H + Q), ('Ab5', Q),
         ('Bb5', DQ), ('Ab5', E8), ('Gb5', Q), ('F5', Q), ('Gb5', H), ('Db5', H),
         ('Eb5', Q), ('F5', Q), ('Gb5', Q), ('Ab5', Q), ('Gb5', H), ('F5', H),
         ('F5', H), ('Eb5', Q), ('D5', Q), ('F5', W - E8), (None, E8)]
B_HAR = ['Cb', 'Gb', 'Abm', 'Ebm', 'Cb', 'Db', 'Abm', 'Bb']   # 2마디씩 · 둘째 8마디는 아래에서 조금 바꿈
B_HAR2 = ['Cb', 'Db', 'Bbm', 'Cb', 'Abm', 'Fb', 'Bbsus', 'Bb']

def harm_seq(lst):   # 1마디 단위 화성 목록(2마디씩 펼침)
    out = []
    for c in lst: out += [c, c]
    return out

def bass_bar(tr, bar, ch, v=96, oct=1, alt=False):   # 8분 몰아침: 3+3+2 강세, 강세 자리에서 옥타브 위로
    r = tone(CH[ch][0], oct)
    if r > nn('F2'): r -= 12
    pat = [r, r, r + 12, r, r, r + 12, r + 10 if not alt else r + 1, r + 12] if ch == 'Ebm' else [r, r, r + 12, r, r, r + 12, r + 7, r + 12]
    for i, n in enumerate(pat):
        add(tr, bar * BAR + i * E8, E8 * .8, n, v + (16 if i in (0, 3, 6) else 0))

KOTO_SCALE = ['Eb', 'Fb', 'Ab', 'Bb', 'Cb']
def koto_bar(tr, bar, ch, v=72, hi=False):   # 16분 뜯기: 화음 음과 일본 음계 음을 섞어 오르내림
    c = [tone(x, 4 + (1 if hi else 0)) for x in CH[ch]]
    c = sorted(set(m if m < nn('Eb5') + (12 if hi else 0) else m - 12 for m in c))
    s = sorted(tone(x, 4 + (1 if hi else 0)) for x in KOTO_SCALE)
    pat = [c[0], c[1], c[2], c[2], s[1], c[0], c[2], s[3], c[0] + 12, c[2], c[1], s[1] + 12, c[2], c[1], c[0], s[4]]
    for i, n in enumerate(pat):
        add(tr, bar * BAR + i * (Q // 4), Q // 4 * 1.6, n, v + (10 if i % 4 == 0 else 0))

def strings_pad(tr, bar, ch, d=BAR, v=70, octs=(3, 4)):
    for o in octs:
        for x in CH[ch]: add(tr, bar * BAR, d * .98, tone(x, o), v)

def drums_main(bar, fill=False, light=False):   # 태고 3+3+2 · 큰북 · 스네어
    b = bar * BAR
    for i in (0, 3, 6):
        add('taiko', b + i * E8, E8, nn('C3') if i == 0 else nn('G2'), 118 if i == 0 else 100)
        add('kit', b + i * E8, E8, 36, 110 if i == 0 else 92)
    if not light:
        for p in (Q, 3 * Q): add('kit', b + p, E8, 38, 70)
        for i in range(8): add('kit', b + i * E8, E8 // 2, 42, 68 + (14 if i % 2 == 0 else 0))
    if fill:
        for i in range(8): add('kit', b + 2 * Q + i * (Q // 4), Q // 4, [50, 50, 48, 48, 47, 47, 45, 45][i], 84 + i * 4)
        add('taiko', b + 3 * Q + E8, E8, nn('C3'), 120)

def timp(bar, root, v=100):
    add('timp', bar * BAR, Q, tone(root, 2), v); add('timp', bar * BAR + 3 * E8, E8, tone(root, 2), v - 20)

def crash(bar, v=96): add('kit', bar * BAR, W, 49, v)

def roll(bar, beats=4, v0=50, v1=110):   # 스네어 16분 연타 크레셴도
    n = beats * 4
    for i in range(n): add('kit', bar * BAR + (4 - beats) * Q + i * Q // 4, Q // 4, 38, v0 + (v1 - v0) * i / max(1, n - 1))

SY = []   # 합성 층: (종류, 시작 틱, 길이 틱, 값)

# ----- 도입 (마디 0~7) -----
def intro():
    for b in range(8):
        if b < 4:
            add('taiko', b * BAR, Q, nn('C3'), 96); SY.append(('boom', b * BAR, Q, .6))
            if b % 2 == 1: add('taiko', b * BAR + 3 * E8, E8, nn('G2'), 90); add('taiko', b * BAR + 6 * E8, E8, nn('G2'), 96)
        else:
            drums_main(b, light=True)
            bass_bar('bass', b, 'Ebm', v=84 + (b - 4) * 4)
    SY.append(('drone', 0, 8 * BAR, 0))
    line('shaku', 0, MOTIF, v=96)                         # 퉁소 소리가 주제를 홀로
    line('shaku', 2, [('Eb5', DQ * 2), ('Fb5', E8), ('Eb5', E8), ('Db5', Q), ('Cb5', Q), ('Bb4', H)], v=92)
    for b in range(4, 8): add('trem', b * BAR, BAR * .98, nn('Eb3'), 60 + (b - 4) * 10); add('trem', b * BAR, BAR * .98, nn('Bb3'), 56 + (b - 4) * 10)
    for b in range(6, 8): koto_bar('koto', b, 'Ebm', v=60 + (b - 6) * 8)
    line('horn', 4, [(['Eb3', 'Bb3'], W * 2), (['Fb3', 'Cb4'], W), (['Eb3', 'Bb3', 'Gb4'], W - E8)], v=78)
    SY.append(('riser', 6 * BAR, 2 * BAR, 0)); roll(7, 4, 40, 112)

# ----- 본문 (시작 마디 s) -----
def body(s):
    hA = harm_seq(A_HAR)
    # A (16마디): 저음 몰아침 · 고토 · 호른 + 현악 선율
    for i in range(16):
        b = s + i; c = hA[i]
        bass_bar('bass', b, c, v=92, alt=(i % 4 == 3)); bass_bar('cello', b, c, v=80, oct=2)
        koto_bar('koto', b, c, v=70)
        drums_main(b, fill=(i in (7, 15)))
        if i % 2 == 0: timp(b, CH[c][0]); SY.append(('boom', b * BAR, Q, .8))
        strings_pad('pad', b, c, v=56)
    crash(s, 100); crash(s + 8, 92)
    line('horn', s, A_MEL, v=96)
    line('vln', s, A_MEL, v=84, oct=1)
    # B (16마디): 현악 16분 · 합창 · 높은 선율, 금관이 엇박으로 찌름
    hB = harm_seq(B_HAR)
    s2 = s + 16
    for i in range(16):
        b = s2 + i; c = hB[i]
        bass_bar('bass', b, c, v=90); bass_bar('cello', b, c, v=74, oct=2)
        r = [tone(x, 4) for x in CH[c]]
        for k in range(16): add('spicc', b * BAR + k * Q // 4, Q // 4 * .7, [r[0], r[1], r[2], r[1]][k % 4] + (12 if k >= 8 else 0), 66 + (12 if k % 4 == 0 else 0))
        for x in CH[c]: add('choir', b * BAR, BAR * .98, tone(x, 4), 74)
        drums_main(b, fill=(i in (7, 15)))
        for k in (1, 5): add('brass', b * BAR + k * E8 + (Q if k == 5 else 0), E8 * .9, tone(CH[c][0], 3), 108); add('brass', b * BAR + k * E8 + (Q if k == 5 else 0), E8 * .9, tone(CH[c][2], 3), 104)
        if i % 2 == 0: timp(b, CH[c][0], 92)
    crash(s2, 100); crash(s2 + 8, 96)
    line('vln', s2, B_MEL, v=104, oct=0); line('horn', s2, B_MEL, v=92, oct=-1)
    roll(s2 + 15, 4, 50, 118)
    # 숨 고르기 (8마디): 저음 지속 · 심장 같은 태고 · 퉁소가 주제를 느리게, 마지막 2마디에서 다시 차오름
    s3 = s2 + 16
    SY.append(('drone', s3 * BAR, 8 * BAR, 1))
    for i in range(8):
        b = s3 + i
        add('taiko', b * BAR, Q, nn('C3'), 84); add('taiko', b * BAR + E8 * 3 // 2, E8, nn('C3'), 62)
        SY.append(('boom', b * BAR, Q, .5)); SY.append(('heart', b * BAR, Q, 0))
        add('cb', b * BAR, BAR * .98, nn('Eb2'), 74); add('cb', b * BAR, BAR * .98, nn('Eb1') + 12 * 0, 60)
        if i >= 6: drums_main(b, light=(i == 6)); bass_bar('bass', b, 'Ebm', v=82 + (i - 6) * 8)
    line('shaku', s3, [('Bb4', W), ('Cb5', H), ('Bb4', H), ('Ab4', H), ('Gb4', H), ('Fb4', H), ('Eb4', H + W)], v=90)
    for i in (2, 3, 4, 5): koto_bar('koto', s3 + i, 'Ebm' if i % 2 == 0 else 'Fb', v=50)
    for x in ('Eb', 'Bb'): add('trem', (s3 + 4) * BAR, 4 * BAR * .98, tone(x, 3), 58)
    SY.append(('riser', (s3 + 6) * BAR, 2 * BAR, 0)); roll(s3 + 7, 4, 44, 118)
    # A' (16마디): 전원 · 합창과 금관이 주제를 옥타브로
    s4 = s3 + 8
    for i in range(16):
        b = s4 + i; c = hA[i]
        bass_bar('bass', b, c, v=96, alt=(i % 4 == 3)); bass_bar('cello', b, c, v=84, oct=2)
        koto_bar('koto', b, c, v=70, hi=True)
        r = [tone(x, 4) for x in CH[c]]
        for k in range(16): add('spicc', b * BAR + k * Q // 4, Q // 4 * .7, [r[0], r[2], r[1], r[2]][k % 4], 60 + (10 if k % 4 == 0 else 0))
        drums_main(b, fill=(i in (7,)))
        if i % 2 == 0: timp(b, CH[c][0], 104); SY.append(('boom', b * BAR, Q, 1.0))
        strings_pad('pad', b, c, v=60)
        for x in CH[c]: add('choir', b * BAR, BAR * .98, tone(x, 4), 66)
    crash(s4, 108); crash(s4 + 8, 100)
    line('brass', s4, A_MEL, v=100); line('horn', s4, A_MEL, v=96, oct=-1); line('vln', s4, A_MEL, v=90, oct=1)
    # 마지막 마디는 짧게 끊어 되감을 때 앞 소리가 끌리지 않게(이끎음 · 긴 울림 없음)

intro()
body(INTRO); body(INTRO + BODY)
# 꼬리 2마디: 본문 첫 2마디와 같게 (파일 끝 0.5초 꼬리용)
body_tail = INTRO + 2 * BODY

# ---------- 사람 손맛: 본문 안 자리로 씨앗을 정해 두 회차가 똑같게 ----------
def human(tr, ev):
    out = []
    for t, d, n, v in ev:
        bar = t // BAR; pos = bar - INTRO
        key = (bar if pos < 0 else INTRO + pos % BODY) * 100000 + (t % BAR) * 7 + n * 13 + hash(tr) % 997
        r = np.random.default_rng(abs(key) % (2 ** 32))
        if tr not in ('kit', 'taiko', 'timp'): t2 = t + int(round(r.uniform(-1, 1) * 2)) * 8   # ±16틱(약 6ms)
        else: t2 = t
        out.append((max(0, t2), d, n, int(np.clip(v + r.integers(-6, 7), 1, 127))))
    return out

PROG = {'shaku': 77, 'koto': 107, 'bass': 43, 'cello': 42, 'cb': 43, 'pad': 49, 'trem': 44, 'spicc': 45, 'vln': 48, 'horn': 60, 'brass': 61, 'choir': 52,
        'timp': 47, 'taiko': 116, 'kit': 'drum'}
def write_mid(tr, ev, path):
    mf = mido.MidiFile(ticks_per_beat=TPB); trk = mido.MidiTrack(); mf.tracks.append(trk)
    trk.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(BPM)))
    chn = 9 if PROG[tr] == 'drum' else 0
    if chn == 0: trk.append(mido.Message('program_change', program=PROG[tr], channel=0))
    else: trk.append(mido.Message('program_change', program=48, channel=9))   # 오케스트라 세트
    trk.append(mido.Message('control_change', control=91, value=0, channel=chn)); trk.append(mido.Message('control_change', control=93, value=0, channel=chn))
    E = []
    for t, d, n, v in ev:
        E.append((t, 1, n, v)); E.append((t + max(10, d), 0, n, 0))
    E.sort(key=lambda e: (e[0], e[1]))
    last = 0
    for t, on, n, v in E:
        trk.append(mido.Message('note_on' if on else 'note_off', note=int(np.clip(n, 0, 127)), velocity=v, channel=chn, time=t - last)); last = t
    mf.save(path)

def rd(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').reshape(-1, 2).T.astype(float) / 32768; return x
N = int(NB * BAR * SPT) + SR * 4
stems = {}
for tr, ev in T.items():
    mp = os.path.join(OUT, f'{tr}.mid'); wp = os.path.join(OUT, f'{tr}.wav')
    write_mid(tr, human(tr, ev), mp)
    subprocess.run(['fluidsynth', '-ni', '-g', '0.6', '-R', '0', '-C', '0', '-r', str(SR), '-F', wp, SF, mp], capture_output=True)
    x = rd(wp); y = np.zeros((2, N)); y[:, :min(N, x.shape[1])] = x[:, :N]; stems[tr] = y

# ---------- 합성 층 ----------
rng = np.random.default_rng(5)
def env(n, a, r): e = np.ones(n); A = int(a * SR); R = int(r * SR); e[:A] = np.linspace(0, 1, A); e[-R:] *= np.linspace(1, 0, R); return e
syn = np.zeros((2, N))
def put(x, t, g=1., pan=0.):
    i = int(round(t * SPT)); n = min(len(x), N - i)
    if n <= 0: return
    syn[0, i:i + n] += x[:n] * g * (1 - pan) ** .5; syn[1, i:i + n] += x[:n] * g * (1 + pan) ** .5
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
for k, t, d, val in SY:
    if k == 'boom':
        L = int(.9 * SR); tt = np.arange(L) / SR
        x = np.sin(2 * np.pi * 46 * tt * (1 + .9 * np.exp(-tt / .04))) * np.exp(-tt / .28)
        put(x, t, .28 * val)
    elif k == 'heart':
        L = int(.5 * SR); tt = np.arange(L) / SR
        x = np.sin(2 * np.pi * 52 * tt) * np.exp(-tt / .09); x2 = np.sin(2 * np.pi * 46 * tt) * np.exp(-tt / .08)
        put(x, t, .22); put(x2, t + 0.16 / (60 / BPM / TPB), .16)
    elif k == 'drone':
        L = int(d * SPT); tt = np.arange(L) / SR; x = np.zeros(L)
        for f, g in ((nn('Eb1'), 1), (nn('Bb1'), .5), (nn('Eb2'), .35)):
            hz = 440 * 2 ** ((f - 69) / 12)
            for dt in (-.15, 0, .15):
                ph = (np.cumsum(np.full(L, hz * 2 ** (dt / 12))) / SR) % 1; x += g * (2 * ph - 1) / 3
        x = lp(lp(x, 260), 260) * env(L, 1.2, 1.0); put(x, t, .14 if val == 0 else .12)
    elif k == 'riser':
        L = int(d * SPT); tt = np.arange(L) / SR; u = tt / tt[-1]
        nz = np.random.default_rng(11).standard_normal(L)
        out = np.zeros(L); seg = 2400
        for j in range(0, L, seg):
            f = 300 + 5000 * u[j] ** 2; out[j:j + seg] = sosfilt(butter(2, [f * .7, f * 1.3], 'band', fs=SR, output='sos'), nz[j:j + seg])
        put(out * u ** 2 * .5, t, .5)

# ---------- 섞기 ----------
MIX = {'bass': (.72, 0), 'cello': (.7, -.25), 'cb': (.55, 0), 'koto': (1.05, .35), 'shaku': (1.25, -.1), 'pad': (.5, 0), 'trem': (1.0, .1), 'spicc': (.95, .3),
       'vln': (1.05, .25), 'horn': (1.1, -.3), 'brass': (1.05, -.15), 'choir': (.75, 0), 'timp': (.75, -.1), 'taiko': (.78, .05), 'kit': (.75, 0)}
BRIGHT = {'vln': .9, 'spicc': .8, 'brass': .7, 'horn': .5, 'koto': .6, 'choir': .5, 'shaku': .4, 'kit': 1.2, 'trem': .5}
mix = np.zeros((2, N))
for tr, y in stems.items():
    g, pan = MIX[tr]
    if tr in ('vln', 'choir', 'pad', 'spicc'): y = np.vstack([hp(y[0], 120), hp(y[1], 120)])
    if tr in BRIGHT: k = BRIGHT[tr]; y = np.vstack([y[c] + k * hp(hp(y[c], 2500), 2500) for c in range(2)])
    mix[0] += y[0] * g * (1 - pan) ** .5; mix[1] += y[1] * g * (1 + pan) ** .5
mix += syn
# 합성 잔향(늘 같은 결과): 약 2.2초
L = int(2.2 * SR); tt = np.arange(L) / SR; out = np.zeros_like(mix)
for c in range(2):
    ir = np.random.default_rng(100 + c).standard_normal(L) * np.exp(-tt / (2.2 / 6.9)); ir = lp(ir, 6000); ir[:int(.02 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
    wet = fftconvolve(hp(mix[c], 180), ir)[:N]; out[c] = mix[c] + .22 * wet
mix = out
# 반복 지점: 본문 시작 3초(2마디) 뒤부터 본문 길이만큼
LS = (INTRO + 2) * BAR * SPT / SR; LE = LS + BODY * BAR * SPT / SR
a, b = int(LS * SR), int(LE * SR)
seg1, seg2 = mix[:, a:a + SR * 6], mix[:, b:b + SR * 6]
sim = (seg1 * seg2).sum() / np.sqrt((seg1 ** 2).sum() * (seg2 ** 2).sum())
end = b + int(.5 * SR); Y = mix[:, :end]
# 크기: 전투곡과 같은 −17.4 LUFS
w = os.path.join(OUT, 'k1.wav'); Y = Y / (np.abs(Y).max() + 1e-9) * .95
ww = wave.open(w, 'wb'); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(SR); ww.writeframes((np.clip(Y.T, -1, 1) * 32767).astype('<i2').tobytes()); ww.close()
I = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', w, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float([l for l in I.split('\n') if l.strip().startswith('I:')][-1].split()[1]); G = -17.4 - I
subprocess.run(['ffmpeg', '-hide_banner', '-y', '-loglevel', 'error', '-i', w, '-af', f'volume={G}dB,alimiter=limit=0.89:level=false:attack=2:release=60', '-ar', '48000', '-b:a', '160k', os.path.join(OUT, 'kgduel.mp3')])
json.dump({'d': round(end / SR, 3), 'ls': round(LS, 3), 'le': round(LE, 3), 'seam': round(float(sim), 4)}, open(os.path.join(OUT, 'kgduel.json'), 'w'))
print('len', round(end / SR, 2), 'loop', round(LS, 3), round(LE, 3), 'seam', round(float(sim), 4), 'gain', round(G, 1))
