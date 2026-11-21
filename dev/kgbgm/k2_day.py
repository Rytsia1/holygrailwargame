"""K2 나흘 · 낮 — 오리지널 작곡. 참고곡(Carrying the Dawn)에서 잰 큰 성격만: 느린 약 64BPM, G 단조 · 곡 내내 G 지속음, ♭II(A♭)가 가끔 섞임,
북이 거의 없는 긴 소리 위주(화성 대 타격 15~20dB), 어두운 소리(중심 1~1.5kHz), 크게 부풀었다 가라앉는 세기, 반복 약 74초.
주제(본성 속 진심)를 G 단조로: D–E♭–D–C–B♭–A(첫째)/A♭(둘째)–G. 첫째는 A로 밝게, 둘째는 A♭으로 어긋나게.
구성(1마디 3.75초): 도입 4 | 본문 20 = A 8 · B 8 · C 4"""
import sys
from eng import *
S = Song('kgday', 64, intro=4, body=20, loop_off=1, lufs=-18.0)
A_H = ['Gm', 'Ebmaj7', 'Gm/Bb', 'Cm', 'Gm', 'Abmaj7', 'Eb', 'Dsus']
B_H = ['Eb', 'Bbmaj', 'Cm', 'Gm', 'Eb', 'F', 'Ab', 'D']
C_H = ['Gm', 'Abmaj7', 'Gm', 'Dsus']
A_M = [('D5', DQ * 2), ('Eb5', E8), ('D5', E8), ('C5', Q), ('Bb4', Q), ('A4', Q), ('G4', Q), ('Bb4', DQ), ('C5', E8), ('D5', H), ('F5', Q), ('Eb5', Q), ('D5', H),
       ('D5', DQ * 2), ('Eb5', E8), ('D5', E8), ('C5', Q), ('Bb4', Q), ('Ab4', Q), ('G4', Q), ('Eb5', H), ('D5', Q), ('C5', Q), ('D5', W - E8), (None, E8)]
B_M = [('G5', H), ('F5', Q), ('Eb5', Q), ('D5', W), ('Eb5', Q), ('F5', Q), ('G5', Q), ('Bb5', Q), ('A5', H), ('G5', H),
       ('G5', H), ('F5', Q), ('Eb5', Q), ('F5', H), ('C5', H), ('Eb5', Q), ('D5', Q), ('C5', Q), ('Ab4', Q), ('D5', W - E8), (None, E8)]

def harp(bar, ch, v=60, up=True):   # 8분 펼침화음: 아래에서 위로 갔다 내려옴
    ns = [tone(CH[ch][0], 3)] + [tone(x, 4) for x in CH[ch]] + [tone(CH[ch][0], 5)]
    ns = sorted(ns); pat = ns + ns[-2:0:-1]
    for i in range(8): S.add('harp', bar * S.BAR + i * E8, E8 * 2.5, pat[i % len(pat)], v + (8 if i == 0 else 0))
def pedal(bar, v=62, d=None):
    S.add('cb', bar * S.BAR, (d or S.BAR) * .99, 'G1', v); S.add('cello', bar * S.BAR, (d or S.BAR) * .99, 'G2', v - 6)

def intro():
    S.syn('drone', 0, 4 * S.BAR, .8, notes=('G1', 'D2', 'G2'))
    for i, c in enumerate(['Gm', 'Gm', 'Ebmaj7', 'Dsus']):
        pedal(i, 50 + i * 4); harp(i, c, 44 + i * 5)
    S.line('shaku', 0, [('D5', W), ('Eb5', H), ('D5', H)], v=78)
    S.line('pad', 2, [(['G3', 'D4', 'Bb4'], W), (['A3', 'D4', 'G4'], W - E8)], v=50)

def body(s):
    S.syn('drone', s * S.BAR, 16 * S.BAR, .25, notes=('G1', 'D2', 'G2'), a=2.0, r=2.5)
    for i, c in enumerate(A_H):
        b = s + i; pedal(b, 66); harp(b, c, 62); S.chord('pad', b, c, v=52, octs=(4,))
        if i in (3, 7): S.add('koto', b * S.BAR + 3 * Q, Q, tone(CH[c][0], 5), 66); S.add('koto', b * S.BAR + 3 * Q + E8, Q, tone(CH[c][2], 5), 60)
    S.line('flute', s, A_M[:13], v=84); S.line('oboe', s + 4, A_M[13:], v=82)
    S.line('clar', s + 4, [('Bb3', W), ('C4', W), ('Bb3', W), ('A3', W - E8), (None, E8)], v=60)
    s2 = s + 8
    for i, c in enumerate(B_H):
        b = s2 + i; pedal(b, 80 + (8 if i >= 4 else 0)); harp(b, c, 72)
        S.chord('pad', b, c, v=66 + i * 2, octs=(3, 4)); S.chord('choir', b, c, v=54 + i * 3, octs=(4,))
        if i % 4 == 0: S.add('taiko', b * S.BAR, Q, 'C3', 70); S.syn('boom', b * S.BAR, Q, .5)
        S.add('timp', b * S.BAR, H, tone(CH[c][0], 2), 60 + i * 3)
    S.line('vln', s2, B_M, v=98); S.line('horn', s2, [(n if n is None else n[:-1] + str(int(n[-1]) - 1), d) for n, d in B_M], v=70)
    for k in range(16): S.add('timp', (s2 + 7) * S.BAR + k * S16, S16, 'D2', 50 + k * 3)   # 넷째 마디 끝 소용돌이
    s3 = s2 + 8
    S.syn('drone', s3 * S.BAR, 4 * S.BAR, .9, notes=('G1', 'D2', 'G2'))
    for i, c in enumerate(C_H):
        b = s3 + i; pedal(b, 56); S.chord('pad', b, c, v=44, octs=(4,))
        if i < 2: harp(b, c, 46)
    S.line('cele', s3, [('D6', DQ * 2), ('Eb6', E8), ('D6', E8), ('C6', Q), ('Bb5', Q), ('Ab5', Q), ('G5', Q + H), (None, H)], v=66)
    for i, n in enumerate(['G6', 'D6', 'Bb5']): S.syn('chime', (s3 + 2) * S.BAR + i * DQ, Q, .9, n=n, pan=(i - 1) * .4)

intro(); body(S.intro); body(S.intro + S.body); body(S.intro + 2 * S.body)
PROG = {'cb': 43, 'cello': 42, 'harp': 46, 'pad': 49, 'shaku': 77, 'flute': 73, 'oboe': 68, 'clar': 71, 'koto': 107, 'vln': 48, 'horn': 60, 'choir': 52, 'timp': 47, 'taiko': 116, 'cele': 8}
MIX = {'cb': (.75, 0), 'cello': (.6, -.2), 'harp': (.9, .3), 'pad': (.55, 0), 'shaku': (1.1, -.1), 'flute': (1.0, -.15), 'oboe': (.95, .15), 'clar': (.6, -.3), 'koto': (.8, .35),
       'vln': (1.0, .2), 'horn': (.85, -.3), 'choir': (.6, 0), 'timp': (.7, -.1), 'taiko': (.6, 0), 'cele': (.8, .2)}
J = S.render(sys.argv[1], PROG, MIX, sub={'cb': .13}, bright={'vln': .6, 'harp': .4, 'flute': .3, 'cele': .3}, hpf=('vln', 'choir', 'pad'), wet=.3, revsec=2.8)
preview(f'{sys.argv[1]}/kgday.mp3', J, f'{sys.argv[1]}/kgday_preview.mp3')
