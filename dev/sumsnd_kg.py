"""검귀 루트 연출 소리 (11-21). 모두 직접 합성 (악기 · 다른 곡의 소리 없음).
- j_kg_in      본성 속 진심 진입 (11.6초 · 11-22 1.35배로 늘림): 금빛 울림과 화음 → 손을 거두면 뚝 끊기고 높은 음 하나 → 글자마다 긁힘 → 방울 '톡' · 낮은 쿵 → 낮은 종 넷(나흘)
- j_kg_back_a  등 뒤의 칼 · 눈치채지 못함 (6초): 따뜻한 화음 → 정적 · 칼빛 '칭' → '쉭' → 둔한 '퍽' 뒤 무음 → 멀리서 잔이 깨짐
- j_kg_back_b  령주로 멈춰라 (6.6초): ... '쉭'이 되감기듯 멎음 → 령주의 저음 · 떨리는 화음
- j_kg_back_c  알면서 그대로 둔다 (6.2초): 화음이 끝까지 이어지다 '쉭' 뒤 함께 가라앉음
- j_kg_back_h  동맹 앞에서 등 뒤의 칼이 먼저 닿음 (4초): '쉭' → 무겁게 베임 (쓰러지지 않음)
- j_kg_day1~4  날 카드 (2.9초) · j_kg_full_r/g 잔이 가득 참 (4.8초) · j_kg_duel 결투 시작 (5.6초)
- j_kg_mr 대마력이 령주를 버팀 (5.8초) · j_kg_ally 동맹이 등을 돌림 (5.4초)
- j_end_kgF · j_end_kgS · j_end_kgT 결말 전용 장면 효과(11-22부터 곡 없이 — 결말 연출 동안 다음 곡이 천천히 들어온다) · j_end_kgN 나머지 검귀 결말의 짧은 효과
사용: python3 sumsnd_kg.py <출력 폴더> [이름,이름]"""
import sys, os, subprocess, numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
SR = 48000; rng = np.random.default_rng(21)
OUT = sys.argv[1]
def T(d): return np.arange(int(d * SR)) / SR
def buf(d): return np.zeros((2, int(d * SR)))
def put(B, x, at, pan=0., g=1.):
    i = int(at * SR); n = min(len(x), B.shape[1] - i)
    if n <= 0: return
    B[0, i:i + n] += x[:n] * g * np.sqrt(.5 * (1 - pan)); B[1, i:i + n] += x[:n] * g * np.sqrt(.5 * (1 + pan))
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def noise(d): return rng.standard_normal(int(d * SR))
def adsr(d, a, r):
    x = T(d); return np.minimum(1, x / max(a, 1e-4)) * np.clip((d - x) / max(r, 1e-4), 0, 1)
def tone(f, d, a=.01, r=None, kind='sine'):
    x = T(d); ph = 2 * np.pi * f * x
    y = np.sin(ph) if kind == 'sine' else (2 / np.pi) * np.arcsin(np.sin(ph))
    return y * adsr(d, a, r if r is not None else d * .6)
def glide(f0, f1, d, a=.005, r=None):
    x = T(d); f = f0 * (f1 / f0) ** (x / d); return np.sin(2 * np.pi * np.cumsum(f) / SR) * adsr(d, a, r if r is not None else d * .9)
def bell(f, d):
    x = T(d); m = 1.6 * np.exp(-x / (d * .3)); return np.sin(2 * np.pi * f * x + m * np.sin(2 * np.pi * f * 2.76 * x)) * np.exp(-x / (d * .32))
def pad(freqs, d, a, r, bright=2400):
    x = T(d); y = np.zeros(len(x))
    for f in freqs:
        for k in (-1, 0, 1):
            y += np.sin(2 * np.pi * f * (1 + .003 * k) * x + rng.random() * 6) * .33
    return lp(y, bright) * adsr(d, a, r) / len(freqs)
def whoosh(d, lo, hi, g=1.):
    n = int(d * SR); s = noise(d); y = np.zeros(n); seg = 1200; u = np.linspace(0, 1, n)
    for k in range(0, n, seg): f = lo * (hi / lo) ** u[k]; y[k:k + seg] = bp(s[k:k + seg], f * .7, min(f * 1.4, 20000), 1)
    return y * np.sin(np.pi * u) ** 1.2 * g
def thump(f=60, d=.5): x = T(d); return np.sin(2 * np.pi * f * x * (1 + .7 * np.exp(-x / .03))) * np.exp(-x / (d * .35))
def scratch(d=.07):
    return bp(noise(d), 2600, 6200) * np.exp(-T(d) / .02)
def glass(d=1.2):
    y = np.zeros(int(d * SR))
    for k in range(9):
        at = rng.uniform(0, .45); f = rng.uniform(2300, 5200); s = bell(f, rng.uniform(.18, .4)) * rng.uniform(.3, 1)
        i = int(at * SR); n = min(len(s), len(y) - i); y[i:i + n] += s[:n]
    y += hp(noise(d), 3000) * np.exp(-T(d) / .12) * .5
    return y
def reverb(B, sec=2.4, wet=.32):
    n = int(sec * SR); x = np.arange(n) / SR; out = np.zeros_like(B)
    for c in range(2):
        ir = rng.standard_normal(n) * np.exp(-x / (sec / 6.9)); ir = lp(ir, 7000); ir /= np.sqrt((ir ** 2).sum()); out[c] = B[c] + wet * fftconvolve(B[c], ir)[:B.shape[1]]
    return out
def save(name, B, lufs=-16.5):
    import wave
    B = B / (np.abs(B).max() + 1e-9) * .89; w = os.path.join(OUT, name + '.wav')
    ww = wave.open(w, 'wb'); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(SR); ww.writeframes((np.clip(B.T, -1, 1) * 32767).astype('<i2').tobytes()); ww.close()
    I = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', w, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float([l for l in I.split('\n') if l.strip().startswith('I:')][-1].split()[1]); G = lufs - I
    subprocess.run(['ffmpeg', '-hide_banner', '-y', '-loglevel', 'error', '-i', w, '-af', f'volume={G}dB,alimiter=limit=0.89:level=false:attack=2:release=60', '-ar', '48000', '-b:a', '160k', os.path.join(OUT, name + '.mp3')]); os.remove(w); print(name, round(B.shape[1] / SR, 2))

GOLD = [659.25, 783.99, 987.77]
def kg_in():   # 11-22: 화면을 1.35배 느리게 풀어서 소리도 같은 비율로 늘림(K). 마지막 장면은 누를 때까지 멈춰 있고, 그동안 낮은 울림이 길게 남는다
    K = 1.35; d = 8.6 * K + 3.0; B = buf(d)
    put(B, tone(55, 1.75 * K, .5, .08), 0, 0, .5); put(B, tone(82.41, 1.65 * K, .6, .08), .1 * K, 0, .3)
    put(B, pad(GOLD, 1.5 * K, .35, .1), .3 * K, 0, .22)
    for k in range(8): put(B, bell(GOLD[k % 3] * 2, .5), (.4 + k * .13) * K, rng.uniform(-.6, .6), .03)
    put(B, tone(1318.5, 3.0 * K, .02, 2.8 * K), 1.65 * K, .1, .05)
    put(B, lp(noise(.5), 300) * np.exp(-T(.5) / .15), 1.6 * K, 0, .25)
    for i in range(14): put(B, scratch(), (2.65 + i * .085) * K + rng.uniform(-.01, .01), rng.uniform(-.3, .3), .35)
    put(B, glide(1180, 520, .35 * K, .003, .33 * K), 4.98 * K, 0, .28); put(B, lp(noise(.5), 900) * np.exp(-T(.5) / .15), 5.0 * K, 0, .06)
    put(B, thump(58, .6), 5.3 * K, 0, .5)
    for i, f in enumerate([196, 174.61, 164.81, 146.83]): put(B, bell(f, 2.6), (6.1 + i * .32) * K, (i - 1.5) * .25, .3)
    put(B, tone(41.2, 2.4 * K + 3.0, .8, 3.0), 6.0 * K, 0, .35)
    return reverb(B)
WARM = [261.63, 329.63, 392.0]
def back(v):
    d = {'a': 6.0, 'b': 6.6, 'c': 6.2, 'h': 4.0}[v]; B = buf(d)
    pd = 3.5 if v == 'c' else 1.45
    put(B, pad(WARM + [523.25], pd, .5, min(.6, pd * .3)), 0, 0, .26); put(B, tone(130.81, pd, .6, min(.6, pd * .3)), 0, 0, .16)
    put(B, bell(3150, .9), 1.55, .7, .12); put(B, bell(4730, .5), 1.56, .7, .05)     # 칼빛 '칭'
    S0 = 2.05 if v == 'b' else 1.93
    put(B, whoosh(.32, 500, 5200, 1), S0 - .02, .4, .55)
    if v == 'a':
        put(B, thump(62, .4), 2.2, 0, .9); put(B, lp(noise(.12), 500) * np.exp(-T(.12) / .04), 2.2, 0, .4)
        put(B, glass(1.4), 3.7, -.1, .22)
    if v == 'h':
        put(B, thump(70, .5), 2.18, 0, .9); put(B, bp(noise(.4), 400, 2600) * np.exp(-T(.4) / .08), 2.18, 0, .45)
        put(B, tone(110, 1.4, .02, 1.2), 2.2, 0, .2)
    if v == 'b':
        x = T(.5); put(B, np.sin(2 * np.pi * np.cumsum(880 * (110 / 880) ** (x / .5)) / SR) * adsr(.5, .01, .45) * .5, 2.05, 0, .3)   # 되감기듯 멎음
        put(B, thump(49, 2.2), 2.12, 0, .9); put(B, lp(noise(.6), 220) * np.exp(-T(.6) / .2), 2.12, 0, .5)
        put(B, pad([523.25, 622.25, 783.99], 2.0, .05, 1.6, 3600), 2.15, 0, .18)
        put(B, tone(98, 2.6, .6, 1.6), 2.6, 0, .2)
    if v == 'c':
        put(B, lp(noise(1.2), 700) * np.exp(-T(1.2) / .5), 2.3, 0, .12)
    return reverb(B, 2.2, .3)

def kg_day(d):   # 날 카드: 낮은 울림 · 차오르는 물소리 · 종 하나(날마다 한 음씩 낮아짐). 11-22: 화면과 함께 1.5배로 늘림
    K = 1.5; L = 2.9 * K + .4; B = buf(L)
    put(B, tone(49, 2.4 * K, .3 * K, 1.0 * K), 0, 0, .35)
    x = T(1.0 * K); sw = bp(noise(1.0 * K), 250, 1400) * np.minimum(1, x / (.5 * K)) * np.clip((1 * K - x) / (.3 * K), 0, 1); put(B, sw, .4 * K, 0, .12)
    put(B, bell([220, 196, 174.61, 164.81][d - 1], 2.6), 1.3 * K, 0, .38)
    return reverb(B, 2.0, .3)
def kg_full(v):  # 잔이 가득 참: 부푸는 울림 → 붉게 넘침(쿵 · 흘러내림) / 금빛으로 풀림
    L = 4.8; B = buf(L)
    put(B, tone(41.2, 2.0, 1.2, .3), 0, 0, .4)
    x = T(1.5); put(B, bp(noise(1.5), 200, 1400) * np.minimum(1, x / 1.2), .2, 0, .08)
    if v == 'r':
        put(B, thump(55, 1.4), 1.6, 0, .9); put(B, bp(noise(.9), 300, 900) * np.exp(-T(.9) / .3), 1.6, 0, .3)
        put(B, pad([138.59, 164.81, 207.65], 2.4, .05, 1.8, 1400), 1.62, 0, .3)
        for k in range(12): put(B, bell(rng.uniform(900, 1800), .4), 1.7 + k * .12, rng.uniform(-.6, .6), .04)
    else:
        for i, f in enumerate([523.25, 659.25, 783.99, 1046.5]): put(B, tone(f, 2.6, .05, 2.0), 1.6 + i * .05, (i - 1.5) * .2, .09)
        put(B, bell(1046.5, 2.0), 1.62, 0, .12)
    return reverb(B, 2.4, .32)
def kg_duel():  # 결투 시작: 잔의 울림 → 돌아서는 '스릉' → '칭' · 낮은 쿵 → 어두운 화음
    L = 5.6; B = buf(L)
    put(B, tone(55, 1.2, .4, .4), 0, 0, .35); put(B, pad([261.63, 329.63, 392.0], 1.0, .3, .4), .2, 0, .15)
    put(B, whoosh(.5, 1800, 5200, 1), 1.1, .3, .35)
    x = T(.45); put(B, np.sin(2 * np.pi * np.cumsum(220 * (2 ** (x / .45))) / SR) * adsr(.45, .02, .3) * .3, 1.15, .3, .3)
    put(B, bell(3150, .9), 1.85, .5, .14); put(B, thump(52, 1.4), 1.9, 0, .85); put(B, lp(noise(.3), 400) * np.exp(-T(.3) / .08), 1.9, 0, .3)
    put(B, pad([146.83, 174.61, 220.0], 3.2, .3, 2.0, 1200), 2.0, 0, .25)
    return reverb(B, 2.2, .3)

def kg_mr():  # 대마력이 령주를 버팀: 령주가 달아오름 → 막이 켜짐 → 길항(갈리는 웅웅거림이 높고 거칠어짐) → 밀어냄(터짐 · 쿵)
    L = 5.8; B = buf(L)
    put(B, glide(98, 196, .9, .5, .2), .3, 0, .25); put(B, pad([523.25, 622.25], .6, .3, .2, 3000), .5, 0, .12)
    x = T(.6); put(B, bp(noise(.6), 400, 3000) * np.minimum(1, x / .4) * np.clip((.6 - x) / .1, 0, 1), .95, 0, .3)
    put(B, bell(2093, 1.0), 1.45, .2, .2); put(B, bell(2637, .8), 1.46, .2, .12)
    x = T(1.4); f = 70 * (150 / 70) ** (x / 1.4)
    saw = lambda ff: (2 * ((np.cumsum(ff) / SR) % 1) - 1)
    grind = (saw(f) + saw(f * 1.04)) * .5 * (1 + .5 * np.sin(2 * np.pi * 11 * x)) * np.minimum(1, x / .2) * np.clip((1.4 - x) / .1, 0, 1)
    put(B, lp(grind, 1800), 1.5, 0, .35); put(B, bp(noise(1.4), 600, 2600) * np.minimum(1, x / .6), 1.5, 0, .12)
    for i in range(9): put(B, bell(rng.uniform(1400, 3000), .15), 1.6 + i * .13, rng.uniform(-.5, .5), .05)
    put(B, hp(noise(.7), 2400) * np.exp(-T(.7) / .15), 2.85, 0, .35); put(B, glass(1.0), 2.86, 0, .25)
    put(B, thump(56, 1.4), 2.85, 0, .9); put(B, tone(1760, 1.6, .002, 1.5), 2.86, 0, .07)
    return reverb(B, 2.4, .32)
def kg_ally():  # 동맹이 등을 돌림: 잔의 울림 · 떨리는 실 → '툭' 끊어짐 · 줄이 튕김 → 낮은 쿵 · 어두운 화음
    L = 5.4; B = buf(L)
    put(B, tone(55, 1.6, .4, .4), 0, 0, .3); put(B, tone(1760, 1.2, .3, .2) + tone(1777.6, 1.2, .3, .2), .3, 0, .05)
    x = T(.45); put(B, np.sin(2 * np.pi * np.cumsum(1760 * (1 + .08 * x / .45) * (1 + .01 * np.sin(2 * np.pi * 40 * x))) / SR) * adsr(.45, .05, .1), 1.2, 0, .1)
    put(B, bp(noise(.12), 1500, 4000) * np.exp(-T(.12) / .03), 1.62, 0, .7)
    put(B, glide(330, 110, .6, .002, .55), 1.63, -.4, .2); put(B, glide(294, 98, .6, .002, .55), 1.65, .4, .17)
    put(B, thump(52, 1.4), 1.9, 0, .8); put(B, pad([146.83, 174.61, 207.65], 2.8, .3, 2.0, 1200), 2.0, 0, .25)
    return reverb(B, 2.2, .3)

def rd(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 's16le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, '<i2').reshape(-1, 2).T.astype(float) / 32768
def with_song(B, song, at, g=1.):   # 결말 전용 장면의 효과 뒤에 결말 곡을 붙인다 (전사 j_end_dead와 같은 방식)
    m = rd(os.path.join(OUT, song + '.mp3')); m = m / (np.abs(m).max() + 1e-9) * np.abs(B).max() * g
    n = max(B.shape[1], int(at * SR) + m.shape[1]); out = np.zeros((2, n)); out[:, :B.shape[1]] += B; i = int(at * SR); out[:, i:i + m.shape[1]] += m; return out
def end_kgF():  # 등 뒤의 칼 (결말): 붉은 잔의 울림 → '슥' 칼이 가름 · 금속음 → 잔이 깨짐 · 쿵 → 심장 둘 → 멎음 → 결말 곡(c)
    d = 5.0; B = buf(d)
    put(B, pad([138.59, 164.81, 207.65], 1.5, .5, .25, 900), 0, 0, .3); put(B, tone(49, 1.5, .5, .3), 0, 0, .3)
    put(B, whoosh(.22, 1500, 7000, 1), 1.34, .3, .6); put(B, bell(3520, .5), 1.45, .2, .1); put(B, bell(5280, .3), 1.46, .2, .04)
    put(B, glass(1.2), 1.62, 0, .35); put(B, thump(60, 1.0), 1.6, 0, .9); put(B, lp(noise(.6), 900) * np.exp(-T(.6) / .15), 1.62, 0, .25)
    for i, b in enumerate((2.6, 3.15)): put(B, thump(52, .25), b, 0, .8 - .3 * i); put(B, thump(46, .22), b + .14, 0, .55 - .2 * i)
    put(B, tone(880, 1.5, .05, 1.3), 3.7, 0, .03)
    return reverb(B, 2.2, .3)
def end_kgS():  # 막아선 칼 (결말): 낮은 바람 → 잦아듦 → 작게 금 가는 소리 · 맑은 종 → 칼날의 희미한 쇳소리 → 마지막 화음이 잦아든다
    d = 7.6; B = buf(d)   # 11-22: 5초에서 화음 · 종 · 잔향이 '툭' 끊기던 것 → 끝까지 울리고 2초에 걸쳐 잦아들게
    put(B, lp(noise(3.2), 450) * adsr(3.2, .6, 1.4), 0, 0, .35); put(B, tone(44, 2.6, .8, 1.2), 0, 0, .3)
    put(B, bp(noise(.35), 2400, 3800) * np.exp(-T(.35) / .08), 2.5, .1, .25); put(B, bell(1318.5, 2.4), 2.55, -.2, .14); put(B, bell(1975.5, 2.2), 2.63, .2, .1); put(B, bell(659.25, 3.0), 2.7, 0, .12)
    put(B, tone(2637, .9, .05, .8) + tone(2652, .9, .05, .8), 3.15, -.3, .03)
    put(B, pad([196.0, 293.66, 392.0], 2.6, .6, 1.8, 1400), 3.4, 0, .2)
    B = reverb(B, 2.4, .32); n = int(2.0 * SR); B[:, -n:] *= .5 * (1 + np.cos(np.pi * np.arange(n) / n)); return B
def end_kgT():  # 둘이 이긴 세계 (결말): 잔의 울림 → 깊게 차오름 · 불이 하나씩 꺼지는 작은 소리 → 거의 무음 · 작은 종 하나 → 결말 곡(a)
    d = 5.2; B = buf(d)
    put(B, tone(55, 1.4, .4, .4), 0, 0, .3); put(B, pad([220.0, 277.18, 329.63], 1.3, .4, .3, 1200), .1, 0, .2)
    put(B, glide(40, 30, 1.8, .5, 1.2), 1.15, 0, .7); put(B, lp(noise(1.7), 700) * adsr(1.7, .6, 1.0), 1.15, 0, .3); put(B, pad([146.83, 174.61, 220.0], 1.6, .5, 1.0, 900), 1.2, 0, .15)
    for i in range(10): put(B, hp(noise(.01), 2500) * np.exp(-T(.01) / .003), 1.4 + i * .14 + rng.uniform(-.03, .03), rng.uniform(-.8, .8), .12)
    put(B, bell(1975.5, 2.6), 3.9, 0, .06)
    return reverb(B, 2.4, .3)

def end_kgN():   # 11-22: 빌린 장면을 쓰는 검귀 결말(kgM · kgB · kgP · kgP2 · kgX)의 짧은 효과. 곡 없이 — 뒤의 에필로그 곡이 천천히 들어온다
    d = 6.0; B = buf(d)
    put(B, tone(55, 2.6, .8, 1.6), 0, 0, .32); put(B, pad([233.08, 311.13, 392.0], 2.8, 1.0, 1.6, 1400), .2, 0, .14)
    put(B, bell(622.25, 2.8), 1.2, -.2, .09); put(B, bell(466.16, 3.0), 1.9, .2, .08); put(B, bell(392.0, 3.2), 2.7, 0, .07)
    return reverb(B, 2.6, .32)
os.makedirs(OUT, exist_ok=True)
F = {'j_end_kgN': end_kgN, 'j_end_kgF': end_kgF, 'j_end_kgS': end_kgS, 'j_end_kgT': end_kgT, 'j_kg_mr': kg_mr, 'j_kg_ally': kg_ally, 'j_kg_day1': lambda: kg_day(1), 'j_kg_day2': lambda: kg_day(2), 'j_kg_day3': lambda: kg_day(3), 'j_kg_day4': lambda: kg_day(4), 'j_kg_full_r': lambda: kg_full('r'), 'j_kg_full_g': lambda: kg_full('g'), 'j_kg_duel': kg_duel, 'j_kg_in': kg_in, 'j_kg_back_a': lambda: back('a'), 'j_kg_back_b': lambda: back('b'), 'j_kg_back_c': lambda: back('c'), 'j_kg_back_h': lambda: back('h')}
ONLY = sys.argv[2].split(',') if len(sys.argv) > 2 else list(F)
for n in ONLY: save(n, F[n]())
