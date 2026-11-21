"""K7 동맹 결전 (4판) — 오리지널 작곡. 3판의 소리(16분 몰아침 · 낮은 E 지속 · 긴 음 선율 · 기타 벽)에 더해, 구성까지 참고곡(Unassailable Barricade)을 마디 단위로 재서 맞췄다(소리 · 선율 · 화성은 쓰지 않음).
참고곡의 한 바퀴(36마디, 112.35BPM, 약 78.5초, 도입 없이 첫 박부터 전원):
- 0~7마디 A1: E 중심, 마디마다 화음이 바뀌고 7마디째(끝)에서 A 위에 반음(G# · A#)이 얹혀 긴장
- 8~15마디 A2: A1 변주, 13마디째는 화음이 빠지고 북만 도드라지는 한 마디, 15마디째 다시 A 위 반음 긴장
- 16~23마디 B: E–F 프리지안, 저음 80~90% · 가장 어둡다(소리 중심 1.6~2.3kHz)
- 24~35마디 C(12마디): 북이 앞으로 나옴(화성 대 타격이 가장 낮음), 조금 작고 더 밝음, E 위에 D · G · B♭(♭V) · D# 같은 낯선 색이 번갈아
템포는 이음매를 샘플 단위로 맞추려고 112.36BPM(한 박 0.534초 = 25632샘플)."""
import sys
from eng import *
S = Song('kgally', 60e6 / 534000, intro=0, body=36, loop_off=2, lufs=-17.0)
A1_H = ['Em', 'D/E', 'Bsus', 'Em', 'Em', 'A/E', 'G', 'A']
A2_H = ['Em', 'D/E', 'Em', 'A7', 'Em', None, 'G', 'A']
B_H = ['E5', 'F', 'F', 'E5', 'E5', 'F', 'E', 'E5']
C_H = ['Em', 'Em7', 'Bb/E', 'G', 'Emaj7', 'Em7', 'Bb/E', 'Em', 'Em7', 'Bb/E', 'Em7', 'E']
A1_M = [('B4', W), ('A4', H), ('D5', H), ('E5', W), ('C#5', H), ('B4', H), ('G4', H), ('B4', H), ('C#5', W), ('D5', H), ('B4', H), ('E5', H), ('F5', H)]
A2_M = [('E5', W), ('F#5', H), ('D5', H), ('B4', W), ('C#5', H), ('G5', H), ('G5', W), (None, W), ('D5', H), ('B4', H), ('A4', H), ('A#4', H - E8), (None, E8)]
B_M = [('E3', W), ('F3', W), ('F3', H), ('E3', H), ('E3', W), ('B2', W), ('C3', W), ('E3', H), ('F3', H), ('E3', W - E8), (None, E8)]
C_HI = [('B5', W), ('A#5', W), ('B5', W), ('D#6', W - E8), (None, E8)]
KICK = [0, 2, 3, 6, 8, 10, 11, 14]

def drums(bar, kind, fill=False):
    b = bar * S.BAR
    if kind == 'half':
        for k in [0, 1, 3, 6, 7, 10, 11, 13, 14]: S.add('kit', b + k * S16, S16, 36, 114)
        S.add('kit', b + 8 * S16, S16, 38, 118)
    elif kind == 'break':   # 화음이 빠지고 북만: 탐탐 16분 한 마디
        for k in range(16): S.add('kit', b + k * S16, S16, [50, 48, 47, 45][k // 4], 92 + k * 2)
        for k in (0, 4, 8, 12): S.add('kit', b + k * S16, S16, 36, 112)
    elif kind == 'perc':   # C: 북이 앞으로 — 킥 · 스네어 · 탐탐이 16분으로 얽힘
        for k in (0, 3, 6, 8, 11, 14): S.add('kit', b + k * S16, S16, 36, 116)
        for k in (4, 12): S.add('kit', b + k * S16, S16, 38, 116)
        for k in (2, 7, 10, 15): S.add('kit', b + k * S16, S16, [47, 45, 48, 43][(k // 4) % 4], 98)
        for k in (5, 13): S.add('kit', b + k * S16, S16, 38, 70)
    else:
        for k in KICK: S.add('kit', b + k * S16, S16, 36, 112 if k % 4 == 0 else 100)
        for k in (4, 12): S.add('kit', b + k * S16, S16, 38, 112)
    if kind != 'half':
        for k in range(16): S.add('kit', b + k * S16, S16 // 2, 70, 80 if k % 2 == 0 else 66)
    hat = 42
    if kind == 'half':
        for k in range(0, 16, 2): S.add('kit', b + k * S16, S16 // 2, 42, 70)
    elif kind != 'break':
        for k in range(16): S.add('kit', b + k * S16, S16 // 2, 46 if (kind == 'perc' and k % 4 == 2) else hat, (100 if k % 2 == 0 else 84) + (10 if k % 4 == 0 else 0))
    if fill:
        for k in range(8): S.add('kit', b + (8 + k) * S16, S16, [48, 48, 47, 47, 45, 45, 43, 43][k], 100 + k * 2)
def gallop(bar, r, v, tr):
    for beat in range(4):
        for k, dv in ((0, 12), (2, 0), (3, 4)): S.add(tr, bar * S.BAR + beat * Q + k * S16, S16 * .9, r, v + dv)
def low(bar, root='E1', v=96, twist=False):
    r = nn(root); gallop(bar, r, v, 'ebass'); gallop(bar, r + 12, v - 8, 'low'); S.add('cb', bar * S.BAR, S.BAR * .99, r, 84)
    if twist:
        for k, n in ((12, 'D#2'), (13, 'E2'), (14, 'F2'), (15, 'D2')): S.add('ebass', bar * S.BAR + k * S16, S16 * .9, n, 104)
def wall(bar, ch, v=92, mute=True):
    r = tone(CH[ch][0], 2)
    if r < nn('D2'): r += 12
    for n in (r, r + 7, r + 12): S.add('gtr', bar * S.BAR, S.BAR * .99, n, v)
    if mute:
        for k in range(16): S.add('gtrm', bar * S.BAR + k * S16, S16 * .45, nn('E2'), 70 + (16 if k % 4 == 0 else 0) + (6 if k % 2 == 0 else 0))
def strings16(bar, n, v=70):
    for k in range(16): S.add('spicc', bar * S.BAR + k * S16, S16 * .7, nn(n) + (12 if k % 8 == 4 else 0), v + (12 if k % 4 == 0 else 0))
def drone(bar, nbars, notes, val=3.0): S.syn('drone', bar * S.BAR, nbars * S.BAR, val, notes=notes, cut=520, a=.02, r=.05)

def body(s):
    # A1 · A2 (16마디): 첫 박부터 전원, 마디마다 화음, 8마디 끝에서 A 위 반음 긴장
    for i, c in enumerate(A1_H + A2_H):
        b = s + i
        if c is None: drums(b, 'break'); low(b, 'E1', 90); continue
        drums(b, 'drive', fill=(i in (7, 15))); low(b, 'E1', 96, twist=(i in (3, 11))); wall(b, c, 90); strings16(b, 'E4' if i < 8 else 'B4', 70)
        drone(b, 1, ('E1', 'B1', 'E2', 'B2'))
        if i in (7, 15):   # A 위에 반음이 얹힌다(G# · A#)
            for n in ('G#4', 'A#4'): S.add('trem', b * S.BAR + H, H * .98, n, 84)
        if i % 4 == 0: S.add('kit', b * S.BAR, W, 49, 106)
    S.line('brass', s, A1_M, v=108); S.line('horn', s, A1_M, v=100, oct=-1); S.line('vln', s, A1_M, v=96)
    S.line('brass', s + 8, A2_M, v=110); S.line('horn', s + 8, A2_M, v=100, oct=-1); S.line('vln', s + 8, A2_M, v=96, oct=1)
    # B (8마디): E–F 프리지안, 가장 어둡고 무겁다
    s2 = s + 16
    for i, c in enumerate(B_H):
        b = s2 + i; drums(b, 'half', fill=(i == 7)); low(b, 'F1' if c == 'F' else 'E1', 104); wall(b, c, 100, mute=(i % 2 == 0))
        drone(b, 1, ('F1', 'C2', 'F2') if c == 'F' else ('E1', 'B1', 'E2'), 5.0)
        for x in ('E4', 'F4') if i % 2 == 0 else ('F4', 'G4'): S.add('trem', b * S.BAR, S.BAR * .99, x, 64)
        if i % 4 == 0: S.add('kit', b * S.BAR, W, 49, 96)
    S.line('trb', s2, B_M, v=114); S.line('brass', s2, B_M, v=104, oct=1)
    # C (12마디): 북이 앞으로, 금관은 16분 엇박으로 찌르고, 뒤 4마디만 높은 현악이 긴 음
    s3 = s2 + 8
    for i, c in enumerate(C_H):
        b = s3 + i; drums(b, 'perc', fill=(i == 11)); low(b, 'E1', 98, twist=(i in (3, 7))); wall(b, c, 86)
        strings16(b, 'E5' if i % 2 == 0 else 'D5', 74); drone(b, 1, ('E1', 'B1', 'E2', 'B2'), 2.6)
        r = tone(CH[c][0], 3)
        for k in (0, 3, 6, 10): S.add('brass', b * S.BAR + k * S16, S16 * .8, r, 104); S.add('brass', b * S.BAR + k * S16, S16 * .8, r + 7, 100)
        S.add('kit', b * S.BAR, W, 55 if i % 2 else 49, 104); S.add('kit', b * S.BAR + 2 * Q, Q, 57, 90)
    S.line('vln', s3 + 8, C_HI, v=104); S.line('horn', s3 + 8, C_HI, v=94, oct=-1)

body(0); body(S.body); body(2 * S.body)
PROG = {'low': 42, 'gtr': 30, 'gtrm': 29, 'ebass': 34, 'cb': 43, 'spicc': 45, 'trem': 44, 'vln': 48, 'horn': 60, 'brass': 61, 'trb': 57, 'kit': 'drum0'}
MIX = {'low': (.75, -.1), 'gtr': (.95, 0), 'gtrm': (.85, -.35), 'ebass': (.8, 0), 'cb': (.7, 0), 'spicc': (.8, .35), 'trem': (.85, .2), 'vln': (.95, .25),
       'horn': (.9, -.3), 'brass': (1.15, -.1), 'trb': (1.05, -.2), 'kit': (1.15, 0)}
J = S.render(sys.argv[1], PROG, MIX, bright={'vln': .7, 'spicc': .8, 'brass': .8, 'kit': 1.5, 'gtr': 1.0, 'gtrm': .8, 'trem': .6}, hpf=('vln', 'spicc', 'trem'),
             sub={'ebass': .3, 'cb': .25}, wet=.16)
preview(f'{sys.argv[1]}/kgally.mp3', J, f'{sys.argv[1]}/kgally_preview.mp3')
