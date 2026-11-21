"""검귀 배경음악 공통 엔진 (K1에서 떼어 냄): 악보 → 악기별 MIDI → FluidR3 렌더 → 합성 층 · 섞기 · 합성 잔향 → 반복 지점 · 크기 맞춤.
본문을 두 번 그려 둘째 회차와 같은 자리로 되감는다(사람 손맛은 본문 안 자리로 씨앗을 정해 두 회차가 똑같다)."""
import os, subprocess, wave, json, zlib
import numpy as np, mido
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000; TPB = 960
SF = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
E8, Q, H, DQ, W = TPB // 2, TPB, TPB * 2, TPB * 3 // 2, TPB * 4
S16 = TPB // 4

def nn(s):
    if isinstance(s, int): return s
    names = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    p = names[s[0]]; i = 1
    while i < len(s) and s[i] in 'b#': p += -1 if s[i] == 'b' else 1; i += 1
    return p + 12 * (int(s[i:]) + 1)

CH = {'Ebm': ['Eb', 'Gb', 'Bb'], 'Cb': ['Cb', 'Eb', 'Gb'], 'Abm': ['Ab', 'Cb', 'Eb'], 'Fb': ['Fb', 'Ab', 'Cb'], 'Bb': ['Bb', 'D', 'F'], 'Bbsus': ['Bb', 'Eb', 'F'],
      'Db': ['Db', 'F', 'Ab'], 'Gb': ['Gb', 'Bb', 'Db'], 'Bbm': ['Bb', 'Db', 'F'],
      'Gm': ['G', 'Bb', 'D'], 'Eb': ['Eb', 'G', 'Bb'], 'Cm': ['C', 'Eb', 'G'], 'Ab': ['Ab', 'C', 'Eb'], 'Abmaj7': ['Ab', 'C', 'G'], 'D': ['D', 'F#', 'A'], 'Dsus': ['D', 'G', 'A'],
      'F': ['F', 'A', 'C'], 'Fm': ['F', 'Ab', 'C'], 'G': ['G', 'B', 'D'], 'Gsus': ['G', 'C', 'D'], 'Bbmaj': ['Bb', 'D', 'F'], 'Gm/Bb': ['Bb', 'D', 'G'], 'Ebmaj7': ['Eb', 'G', 'D'],
      'Bm': ['B', 'D', 'F#'], 'Gmaj7': ['G', 'B', 'F#'], 'D/F#': ['F#', 'A', 'D'], 'Em': ['E', 'G', 'B'], 'Cmaj7': ['C', 'E', 'B'], 'F#sus': ['F#', 'B', 'C#'], 'F#m': ['F#', 'A', 'C#'], 'Bm/D': ['D', 'F#', 'B'],
      'Dm': ['D', 'F', 'A'], 'C': ['C', 'E', 'G'], 'A': ['A', 'C#', 'E'], 'Am': ['A', 'C', 'E'], 'Ebm': ['Eb', 'Gb', 'Bb'], 'B': ['B', 'D#', 'F#'], 'E': ['E', 'G#', 'B'], 'E5': ['E', 'B', 'E'], 'D/E': ['D', 'F#', 'A'], 'Bsus': ['B', 'E', 'F#'], 'A/E': ['A', 'C#', 'E'], 'A7': ['A', 'C#', 'G'], 'Bb/E': ['Bb', 'D', 'F'], 'Em7': ['E', 'G', 'D'], 'Emaj7': ['E', 'G#', 'D#'], 'Bb/D': ['D', 'F', 'Bb'], 'Eb/G': ['G', 'Bb', 'Eb'], 'Eb/Bb': ['Bb', 'Eb', 'G'], 'G7': ['G', 'B', 'F'], 'Bbsus4': ['Bb', 'Eb', 'F'], 'Bdim': ['B', 'D', 'F'], 'Dbmaj': ['Db', 'F', 'Ab']}
def tone(name, octv): return nn(name + str(octv))

class Song:
    def __init__(s, name, bpm, intro, body, loop_off=2, tail=2, lufs=-18.0):
        s.name, s.bpm, s.intro, s.body, s.loop_off, s.tail, s.lufs = name, bpm, intro, body, loop_off, tail, lufs
        s.BAR = 4 * TPB; s.SPT = SR * 60 / bpm / TPB; s.T = {}; s.SY = []
    def add(s, tr, t, d, n, v): s.T.setdefault(tr, []).append((int(t), int(d), nn(n), int(max(1, min(127, v)))))
    def line(s, tr, bar, seq, v=90, oct=0, leg=.95):
        t = bar * s.BAR
        for n, d in seq:
            if n is not None:
                for m in (n if isinstance(n, (list, tuple)) else [n]): s.add(tr, t, d * leg, nn(m) + 12 * oct, v)
            t += d
        return t
    def chord(s, tr, bar, ch, d=None, v=70, octs=(3, 4)):
        for o in octs:
            for x in CH[ch]: s.add(tr, bar * s.BAR, (d or s.BAR) * .98, tone(x, o), v)
    def syn(s, kind, t, d, val=1.0, **kw): s.SY.append((kind, t, d, val, kw))

    def human(s, tr, ev, steady=('kit', 'taiko', 'timp')):
        out = []
        for t, d, n, v in ev:
            bar = t // s.BAR; pos = bar - s.intro
            key = (bar if pos < 0 else s.intro + pos % s.body) * 100000 + (t % s.BAR) * 7 + n * 13 + zlib.crc32(tr.encode()) % 997
            r = np.random.default_rng(key % (2 ** 32))
            t2 = t if tr in steady else t + int(round(r.uniform(-1, 1) * 2)) * 8
            out.append((max(0, t2), d, n, int(np.clip(v + r.integers(-6, 7), 1, 127))))
        return out

    def render(s, out, prog, mix, bright={}, hpf=(), drone=('Eb1', 'Bb1', 'Eb2'), wet=.22, revsec=2.2, sub={}, lpf={}):
        os.makedirs(out, exist_ok=True); BAR, SPT = s.BAR, s.SPT
        NB = s.intro + s.body * 2 + s.tail; N = int(NB * BAR * SPT) + SR * 5
        stems = {}
        for tr, ev in s.T.items():
            mp = os.path.join(out, f'{tr}.mid'); wp = os.path.join(out, f'{tr}.wav')
            mf = mido.MidiFile(ticks_per_beat=TPB); trk = mido.MidiTrack(); mf.tracks.append(trk)
            trk.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(s.bpm)))
            chn = 9 if str(prog[tr]).startswith('drum') else 0
            trk.append(mido.Message('program_change', program=(0 if prog[tr] == 'drum0' else 48) if chn == 9 else prog[tr], channel=chn))
            trk.append(mido.Message('control_change', control=91, value=0, channel=chn)); trk.append(mido.Message('control_change', control=93, value=0, channel=chn))
            E = []
            for t, d, n, v in s.human(tr, ev): E.append((t, 1, n, v)); E.append((t + max(10, d), 0, n, 0))
            E.sort(key=lambda e: (e[0], e[1])); last = 0
            for t, on, n, v in E:
                trk.append(mido.Message('note_on' if on else 'note_off', note=int(np.clip(n, 0, 127)), velocity=v, channel=chn, time=t - last)); last = t
            mf.save(mp)
            subprocess.run(['fluidsynth', '-ni', '-g', '0.6', '-R', '0', '-C', '0', '-r', str(SR), '-F', wp, SF, mp], capture_output=True)
            w = wave.open(wp); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').reshape(-1, 2).T.astype(float) / 32768
            y = np.zeros((2, N)); y[:, :min(N, x.shape[1])] = x[:, :N]; stems[tr] = y; os.remove(wp)
        lp = lambda x, f: sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
        hp = lambda x, f: sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
        syn = np.zeros((2, N))
        def put(x, t, g=1., pan=0.):
            i = int(round(t * SPT)); n = min(len(x), N - i)
            if n > 0: syn[0, i:i + n] += x[:n] * g * (1 - pan) ** .5; syn[1, i:i + n] += x[:n] * g * (1 + pan) ** .5
        def env(n, a, r):
            e = np.ones(n); A = int(a * SR); R = int(r * SR); e[:A] = np.linspace(0, 1, A); e[-R:] *= np.linspace(1, 0, R); return e
        for k, t, d, val, kw in s.SY:
            if k == 'boom':
                L = int(.9 * SR); tt = np.arange(L) / SR; f0 = kw.get('f', 46)
                put(np.sin(2 * np.pi * f0 * tt * (1 + .9 * np.exp(-tt / .04))) * np.exp(-tt / .28), t, .28 * val)
            elif k == 'heart':
                L = int(.5 * SR); tt = np.arange(L) / SR
                put(np.sin(2 * np.pi * 52 * tt) * np.exp(-tt / .09), t, .22 * val); put(np.sin(2 * np.pi * 46 * tt) * np.exp(-tt / .08), t + .16 / (60 / s.bpm / TPB), .16 * val)
            elif k == 'drone':
                L = int(d * SPT); x = np.zeros(L)
                for f, g in zip(kw.get('notes', drone), (1, .5, .35, .25)):
                    hz = 440 * 2 ** ((nn(f) - 69) / 12)
                    for dt in (-.15, 0, .15):
                        ph = (np.cumsum(np.full(L, hz * 2 ** (dt / 12))) / SR) % 1; x += g * (2 * ph - 1) / 3
                put(lp(lp(x, kw.get('cut', 260)), kw.get('cut', 260)) * env(L, kw.get('a', 1.2), kw.get('r', 1.0)), t, .14 * val)
            elif k == 'riser':
                L = int(d * SPT); u = np.arange(L) / max(1, L - 1); nz = np.random.default_rng(11).standard_normal(L); o = np.zeros(L)
                for j in range(0, L, 2400):
                    f = 300 + 5000 * u[j] ** 2; o[j:j + 2400] = sosfilt(butter(2, [f * .7, f * 1.3], 'band', fs=SR, output='sos'), nz[j:j + 2400])
                put(o * u ** 2 * .5, t, .5 * val)
            elif k == 'chime':   # 맑은 유리 종 (높은 사인 + 배음)
                L = int(2.5 * SR); tt = np.arange(L) / SR; hz = 440 * 2 ** ((nn(kw['n']) - 69) / 12)
                x = (np.sin(2 * np.pi * hz * tt) + .3 * np.sin(2 * np.pi * hz * 2.76 * tt) * np.exp(-tt / .3)) * np.exp(-tt / .9)
                put(x, t, .08 * val, kw.get('pan', 0))
        for tr, g in sub.items():   # 저음 받침: 악기 음의 바탕음을 사인으로 겹친다(GM 콘트라베이스의 150Hz 아래가 약해서)
            for t, d, n, v in s.human(tr, s.T.get(tr, [])):
                L = int(d * SPT) + int(.08 * SR); hz = 440 * 2 ** ((n - 69) / 12)
                while hz > 110: hz /= 2
                tt = np.arange(L) / SR; e = np.minimum(1, tt / .012) * np.minimum(1, (L / SR - tt) / .08)
                put(np.sin(2 * np.pi * hz * tt) * e * (v / 127) ** 1.5, t, g)
        mixd = np.zeros((2, N))
        for tr, y in stems.items():
            g, pan = mix[tr]
            if tr in hpf: y = np.vstack([hp(y[c], 120) for c in range(2)])
            if tr in lpf: y = np.vstack([lp(y[c], lpf[tr]) for c in range(2)])
            if tr in bright: kb = bright[tr]; y = np.vstack([y[c] + kb * hp(hp(y[c], 2500), 2500) for c in range(2)])
            mixd[0] += y[0] * g * (1 - pan) ** .5; mixd[1] += y[1] * g * (1 + pan) ** .5
        mixd += syn
        L = int(revsec * SR); tt = np.arange(L) / SR; o = np.zeros_like(mixd)
        for c in range(2):
            ir = np.random.default_rng(100 + c).standard_normal(L) * np.exp(-tt / (revsec / 6.9)); ir = lp(ir, 6000); ir[:int(.02 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
            o[c] = mixd[c] + wet * fftconvolve(hp(mixd[c], 180), ir)[:N]
        mixd = o
        LS = (s.intro + s.loop_off) * BAR * SPT / SR; LE = LS + s.body * BAR * SPT / SR
        a, b = int(round(LS * SR)), int(round(LE * SR))
        s1, s2 = mixd[:, a:a + SR * 6], mixd[:, b:b + SR * 6]
        sim = (s1 * s2).sum() / np.sqrt((s1 ** 2).sum() * (s2 ** 2).sum())
        end = b + int(.5 * SR); Y = mixd[:, :end]; Y = Y / (np.abs(Y).max() + 1e-9) * .95
        w = os.path.join(out, s.name + '.wav')
        ww = wave.open(w, 'wb'); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(SR); ww.writeframes((np.clip(Y.T, -1, 1) * 32767).astype('<i2').tobytes()); ww.close()
        I = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', w, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
        I = float([l for l in I.split('\n') if l.strip().startswith('I:')][-1].split()[1]); G = s.lufs - I
        subprocess.run(['ffmpeg', '-hide_banner', '-y', '-loglevel', 'error', '-i', w, '-af', f'volume={G}dB,alimiter=limit=0.89:level=false:attack=2:release=60', '-ar', '48000', '-b:a', '160k', os.path.join(out, s.name + '.mp3')])
        os.remove(w)
        J = {'d': round(end / SR, 3), 'ls': round(LS, 3), 'le': round(LE, 3), 'seam': round(float(sim), 4)}
        json.dump(J, open(os.path.join(out, s.name + '.json'), 'w')); print(s.name, J, 'gain', round(G, 1))
        return J

def preview(mp3, J, out):   # 게임처럼 반복 구간을 한 번 더 돌린 미리듣기
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp3, '-f', 's16le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True).stdout
    X = np.frombuffer(raw, '<i2').reshape(-1, 2).T.astype(float); sh = max(0, X.shape[1] - int(round(J['d'] * SR)))
    a, b = int(J['ls'] * SR) + sh, int(J['le'] * SR) + sh
    Y = np.concatenate([X[:, :b], X[:, a:b], X[:, a:a + SR * 6]], axis=1); Y[:, -SR * 6:] *= np.linspace(1, 0, SR * 6)
    w = out + '.wav'; ww = wave.open(w, 'wb'); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(SR); ww.writeframes(Y.T.astype('<i2').tobytes()); ww.close()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', w, '-b:a', '160k', out]); os.remove(w)
