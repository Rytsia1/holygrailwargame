"""K3 나흘 · 밤 — 오리지널 작곡. 참고곡(Severing the World)에서 잰 큰 성격만: 120BPM, C 단조(자연 단음계, ♭II는 가끔),
가운데가 반쯤 쉬는 길(하프타임) 북 · 16분 잔북, 앞 32초 몰아침 → 16초 가볍게 빠짐(저음 없음) → 32초 A♭ 중심의 무거운 구간(150Hz 아래 약 70%) → 낮게 돌아옴, 반복 88초.
주제(본성 속 진심)를 C 단조로: G–A♭–G–F–E♭–D♭–C.
구성(1마디 2초): 도입 4 | 본문 44 = A 16 · B 8 · C 16 · D 4"""
import sys
from eng import *
S = Song('kgnight', 120, intro=4, body=44, loop_off=2, lufs=-18.0)
A_H = ['Cm', 'Cm', 'Ab', 'Ab', 'Fm', 'Fm', 'Gsus', 'G'] * 2
C_H = ['Ab', 'Ab', 'Eb', 'Eb', 'Fm', 'Fm', 'G', 'G', 'Ab', 'Ab', 'Eb', 'Eb', 'Db', 'Db', 'G', 'G']
MOT = [('G4', DQ * 2), ('Ab4', E8), ('G4', E8), ('F4', Q), ('Eb4', Q), ('Db4', Q), ('C4', Q)]
A_M = MOT + [('Eb4', DQ), ('F4', E8), ('G4', Q), ('Bb4', Q), ('Ab4', H), ('G4', H),
             ('C5', DQ * 2), ('Db5', E8), ('C5', E8), ('Bb4', Q), ('Ab4', Q), ('G4', Q), ('F4', Q), ('Eb4', Q), ('F4', Q), ('G4', Q), ('Ab4', Q), ('G4', W),
             ('G4', DQ * 2), ('Ab4', E8), ('G4', E8), ('F4', Q), ('Eb4', Q), ('Db4', Q), ('C4', Q), ('C5', DQ), ('Bb4', E8), ('Ab4', Q), ('G4', Q), ('F4', H), ('Eb4', H),
             ('Ab4', Q), ('Bb4', Q), ('C5', Q), ('Eb5', Q), ('D5', H), ('C5', H), ('Bb4', Q), ('Ab4', Q), ('G4', Q), ('F4', Q), ('G4', W - E8), (None, E8)]
C_M = [('Eb5', H), ('C5', Q), ('Eb5', Q), ('Db5', DQ), ('C5', E8), ('C5', H), ('C5', Q), ('Bb4', Q), ('G4', Q), ('C5', Q), ('Bb4', W),
       ('Eb5', H), ('F5', Q), ('G5', Q), ('F5', DQ), ('Eb5', E8), ('Eb5', H), ('D5', Q), ('C5', Q), ('B4', Q), ('D5', Q), ('G4', W),
       ('Eb5', H), ('C5', Q), ('Eb5', Q), ('Db5', DQ), ('C5', E8), ('C5', H), ('C5', Q), ('Bb4', Q), ('G4', Q), ('C5', Q), ('Bb4', W),
       ('F5', H), ('Eb5', Q), ('Db5', Q), ('C5', H), ('Bb4', Q), ('Ab4', Q), ('G4', Q), ('Ab4', Q), ('B4', Q), ('D5', Q), ('G4', W - E8), (None, E8)]

def bass(bar, ch, v=90):   # 8분 · 엇박 강세: 1 · 2& · 3& · 4&
    r = tone(CH[ch][0], 2)
    if r > nn('F2'): r -= 12
    for i, (p, n) in enumerate([(0, r), (1, r), (3, r + 12), (4, r), (5, r + 7), (7, r + 12)]):
        S.add('bass', bar * S.BAR + p * E8, E8 * .85, n, v + (14 if p in (0, 3, 5) else 0))
def drums(bar, fill=False, heavy=False):
    b = bar * S.BAR
    for p, n, v in ((0, 'C3', 112), (5, 'G2', 96)): S.add('taiko', b + p * E8, E8, n, v + (8 if heavy else 0))
    S.add('kit', b, E8, 36, 104); S.add('kit', b + 5 * E8, E8, 36, 90); S.add('kit', b + 2 * Q, E8, 38, 92)
    for i in range(16): S.add('kit', b + i * S16, S16 // 2, 42, 52 + (12 if i % 4 == 0 else 0) + (6 if i % 2 == 0 else 0))
    if heavy: S.syn('boom', b, Q, .8); S.add('timp', b, Q, 'C2' if False else 'G2', 96)
    if fill:
        for i in range(8): S.add('kit', b + 2 * Q + i * S16, S16, [50, 50, 48, 48, 47, 47, 45, 45][i], 84 + i * 4)
def koto8(bar, ch, v=66):
    ns = sorted(tone(x, 4) for x in CH[ch]); pat = [ns[0], ns[2], ns[1] + 12, ns[2], ns[0] + 12, ns[2], ns[1], ns[2]]
    for i, n in enumerate(pat): S.add('koto', bar * S.BAR + i * E8, E8 * 1.5, n, v + (10 if i % 4 == 0 else 0))

def intro():
    S.syn('drone', 0, 4 * S.BAR, 1, notes=('C1', 'G1', 'C2'))
    for i in range(4):
        S.add('taiko', i * S.BAR, Q, 'C3', 90 + i * 6); S.syn('boom', i * S.BAR, Q, .6)
        if i >= 2: S.add('taiko', i * S.BAR + 5 * E8, E8, 'G2', 80)
    S.line('shaku', 0, [('G4', W), ('Ab4', H), ('G4', H)], v=88)
    for i in (2, 3): koto8(i, 'Cm', 50 + (i - 2) * 10)
    S.syn('riser', 2 * S.BAR, 2 * S.BAR, .8)
    for k in range(16): S.add('kit', 3 * S.BAR + k * S16, S16, 38, 40 + k * 4)

def body(s):
    for i in range(16):   # A
        b = s + i; c = A_H[i // 2 * 2 % 16] if False else A_H[i // 2]
        bass(b, c); S.add('cello', b * S.BAR, S.BAR * .98, tone(CH[c][0], 2), 70); koto8(b, c, 62)
        drums(b, fill=(i in (7, 15))); S.chord('pad', b, c, v=56, octs=(3, 4))
    S.add('kit', s * S.BAR, W, 49, 100); S.add('kit', (s + 8) * S.BAR, W, 49, 92)
    S.line('shaku', s, A_M[:25], v=96); S.line('vln', s + 8, A_M[25:], v=104); S.line('horn', s + 8, A_M[25:], v=96, oct=-1)
    s2 = s + 16   # B: 저음이 빠지고 가볍게
    for i in range(8):
        b = s2 + i; c = ['Cm', 'Ab', 'Fm', 'G'][i // 2]
        koto8(b, c, 86); S.chord('pad', b, c, v=84, octs=(4, 5)); S.chord('trem', b, c, v=80, octs=(3, 4)); S.chord('choir', b, c, v=58, octs=(4,)); S.syn('heart', b * S.BAR, Q, 1.0); S.add('cello', b * S.BAR, S.BAR * .98, tone(CH[c][0], 3), 62)
        S.add('kit', b * S.BAR + 2 * Q, E8, 42, 50)
    S.line('cele', s2, [('G5', DQ * 2), ('Ab5', E8), ('G5', E8), ('F5', Q), ('Eb5', Q), ('Db5', Q), ('C5', Q), (None, W * 2),
                        ('C6', DQ * 2), ('Db6', E8), ('C6', E8), ('Bb5', Q), ('Ab5', Q), ('G5', H), (None, W)], v=86)
    S.line('vln', s2 + 4, [('Eb5', W), ('C5', W), ('Ab4', W), ('B4', W - E8), (None, E8)], v=78)
    for k in range(16): S.add('kit', (s2 + 7) * S.BAR + k * S16, S16, 38, 44 + k * 4)
    S.syn('riser', (s2 + 6) * S.BAR, 2 * S.BAR, .8)
    s3 = s2 + 8   # C: A♭ 중심의 무거운 구간
    for i in range(16):
        b = s3 + i; c = C_H[i]
        bass(b, c, 98); S.add('cello', b * S.BAR, S.BAR * .98, tone(CH[c][0], 2), 80); S.add('cb', b * S.BAR, S.BAR * .98, tone(CH[c][0], 1) if CH[c][0] not in ('Eb', 'Db') else tone(CH[c][0], 2) - 12, 84)
        drums(b, fill=(i in (7, 15)), heavy=(i % 2 == 0)); S.chord('choir', b, c, v=74, octs=(4,))
        r = [tone(x, 4) for x in CH[c]]
        for k in range(16): S.add('spicc', b * S.BAR + k * S16, S16 * .7, [r[0], r[1], r[2], r[1]][k % 4] + (12 if k >= 8 else 0), 62 + (12 if k % 4 == 0 else 0))
    S.add('kit', s3 * S.BAR, W, 49, 108); S.add('kit', (s3 + 8) * S.BAR, W, 49, 100)
    S.line('brass', s3, C_M, v=100); S.line('trb', s3, C_M, v=92, oct=-1); S.line('vln', s3 + 8, C_M[len(C_M) // 2:], v=88, oct=1)
    s4 = s3 + 16  # D: 낮게 돌아옴
    S.syn('drone', s4 * S.BAR, 4 * S.BAR, 1, notes=('C1', 'G1', 'C2'))
    for i in range(4):
        b = s4 + i; S.add('taiko', b * S.BAR, Q, 'C3', 96); S.add('taiko', b * S.BAR + 5 * E8, E8, 'G2', 82); S.syn('boom', b * S.BAR, Q, .7)
        S.add('cb', b * S.BAR, S.BAR * .98, 'G1', 70)
    S.line('shaku', s4, [('Ab4', W), ('G4', W), (None, W * 2)], v=86)
    for i in (2, 3): koto8(s4 + i, 'G', 52 + (i - 2) * 10)
    S.syn('riser', (s4 + 2) * S.BAR, 2 * S.BAR, .9)
    for k in range(16): S.add('kit', (s4 + 3) * S.BAR + k * S16, S16, 38, 44 + k * 4)

intro(); body(S.intro); body(S.intro + S.body); body(S.intro + 2 * S.body)
PROG = {'trem': 44, 'bass': 43, 'cello': 42, 'cb': 43, 'koto': 107, 'pad': 49, 'shaku': 77, 'vln': 48, 'horn': 60, 'brass': 61, 'trb': 57, 'choir': 52, 'spicc': 45, 'cele': 8,
        'timp': 47, 'taiko': 116, 'kit': 'drum'}
MIX = {'trem': (.9, .1), 'bass': (.8, 0), 'cello': (.55, -.2), 'cb': (.8, 0), 'koto': (.95, .35), 'pad': (.55, 0), 'shaku': (1.2, -.1), 'vln': (1.0, .2), 'horn': (.9, -.3), 'brass': (1.15, -.15),
       'trb': (1.1, -.2), 'choir': (.75, 0), 'spicc': (.85, .3), 'cele': (.9, .2), 'timp': (.75, -.1), 'taiko': (.8, .05), 'kit': (.75, 0)}
J = S.render(sys.argv[1], PROG, MIX, sub={'bass': .22, 'cb': .26, 'trb': .1}, bright={'vln': .8, 'spicc': .7, 'brass': .6, 'koto': .5, 'kit': 1.0, 'shaku': .3, 'cele': .3}, hpf=('vln', 'choir', 'pad', 'spicc'), drone=('C1', 'G1', 'C2'))
preview(f'{sys.argv[1]}/kgnight.mp3', J, f'{sys.argv[1]}/kgnight_preview.mp3')
