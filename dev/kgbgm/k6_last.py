"""K6 마지막 밤 — 오리지널 작곡. K3(나흘 · 밤)의 재료(120BPM · C 단조 · 주제 G–A♭–G–F–E♭–D♭–C)를 더 조이고 낮춘 판.
잔이 가득 찬 뒤 령주 창 · 결심까지의 짧은 시간: 밝은 고토 · 높은 선율을 빼고, 낮은 C 지속음 · 반음으로 조이는 첼로 8분(C–D♭–C–B) · 심장 박동 · 시계 같은 똑딱임.
주제는 퉁소가 낮은 음역(G3)에서 느리게. 뒤로 갈수록 반음 뭉치(G–A♭) 현악 떨림과 북이 조이다가, 마지막 두 마디에서 지속음만 남아 처음으로 돌아간다.
구성(1마디 2초): 도입 2 | 본문 24 = a 8 · b 8 · c 8"""
import sys
from eng import *
S = Song('kglast', 120, intro=2, body=24, loop_off=2, lufs=-18.5)
B_H = ['Cm', 'Dbmaj', 'Cm', 'Bdim', 'Cm', 'Dbmaj', 'Ab', 'G']
MOT = [('G3', DQ * 2), ('Ab3', E8), ('G3', E8), ('F3', Q), ('Eb3', Q), ('Db3', Q), ('C3', Q)]

def ost(bar, v=74, root='C'):   # 첼로 8분: 반음으로 조인다
    r = tone(root, 2) if root != 'C' else nn('C3')
    for i, d in enumerate([0, 0, 1, 0, 0, 0, -1, 0]): S.add('cello', bar * S.BAR + i * E8, E8 * .55, r + d, v + (12 if i in (0, 4) else 0))
def tick(bar, v=46):
    for i in range(8): S.add('kit', bar * S.BAR + i * E8, E8 // 2, 76 if i % 2 == 0 else 77, v + (8 if i % 2 == 0 else 0))
def heart(bar, val=1.0):
    for k in (0, 2): S.syn('heart', bar * S.BAR + k * Q, Q, val)

def intro():
    S.syn('drone', 0, 2 * S.BAR, .9, notes=('C1', 'G1', 'C2'), cut=300, a=1.5, r=.1)
    for b in range(2): heart(b, .6 + b * .2); tick(b, 34 + b * 6)

def body(s):
    S.syn('drone', s * S.BAR, 24 * S.BAR, .9, notes=('C1', 'G1', 'C2'), cut=300, a=.05, r=.05)
    for i in range(8):   # a: 첼로 조임 · 심장 · 똑딱 · 낮은 퉁소
        b = s + i; ost(b, 70); heart(b, .8); tick(b, 44)
        S.add('cb', b * S.BAR, S.BAR * .99, 'C2', 60)
        if i % 2 == 0: S.add('taiko', b * S.BAR, Q, 'C3', 76)
    S.line('shaku', s, MOT + [(None, W * 2)] + MOT[:3] + [('F3', H), ('G3', H), (None, W)], v=84)
    for i, c in enumerate(B_H):   # b: 화음이 반음으로 비틀리고 낮은 금관이 부푼다
        b = s + 8 + i; ost(b, 78, root='C' if c in ('Cm', 'Bdim') else CH[c][0]); heart(b, .9); tick(b, 50)
        S.add('cb', b * S.BAR, S.BAR * .99, tone(CH[c][0], 1) + (12 if CH[c][0] in ('Db', 'B') else 0), 70)
        for x in CH[c]: S.add('trb', b * S.BAR + E8, S.BAR * .9, tone(x, 3), 62 + i * 3)
        S.add('taiko', b * S.BAR, Q, 'C3', 86); S.add('taiko', b * S.BAR + 5 * E8, E8, 'G2', 70)
        for k in range(16): S.add('kit', b * S.BAR + k * S16, S16 // 2, 38, 30 + (k % 4 == 0) * 10)
    S.line('horn', s + 8, [('G3', W), ('Ab3', W), ('G3', W), ('F3', W), ('Eb3', W), ('F3', W), ('Eb3', H), ('C3', H), ('D3', W - E8), (None, E8)], v=74)
    for i in range(8):   # c: 가장 조인다 → 마지막 두 마디는 지속음만
        b = s + 16 + i
        if i < 6:
            ost(b, 86); heart(b, 1.0); tick(b, 56)
            for x in ('G5', 'Ab5'): S.add('trem', b * S.BAR, S.BAR * .99, x, 58 + i * 5)
            for x in ('C4', 'Db4'): S.add('trem', b * S.BAR, S.BAR * .99, x, 54 + i * 4)
            for k in range(8): S.add('taiko', b * S.BAR + k * E8, E8, 'C3' if k % 4 == 0 else 'G2', 70 + i * 5 + (12 if k % 4 == 0 else 0))
            S.add('cb', b * S.BAR, S.BAR * .99, 'C2', 76); S.syn('boom', b * S.BAR, Q, .5 + i * .06)
        else:
            heart(b, .7 - (i - 6) * .2); tick(b, 40 - (i - 6) * 6)
    S.line('shaku', s + 16, [('G4', W), ('Ab4', W), ('G4', H), ('F4', H), ('Eb4', H), ('Db4', H), ('C4', W * 2), (None, W * 2 - E8), (None, E8)], v=90)
    S.syn('riser', (s + 14) * S.BAR, 2 * S.BAR, .6)

intro(); body(S.intro); body(S.intro + S.body); body(S.intro + 2 * S.body)
PROG = {'cello': 42, 'cb': 43, 'trb': 57, 'horn': 60, 'trem': 44, 'shaku': 77, 'taiko': 116, 'kit': 'drum'}
MIX = {'cello': (.95, -.15), 'cb': (.8, 0), 'trb': (.85, -.2), 'horn': (.9, -.3), 'trem': (.8, .2), 'shaku': (1.15, .1), 'taiko': (.75, 0), 'kit': (.7, .15)}
J = S.render(sys.argv[1], PROG, MIX, bright={'trem': .4}, hpf=('trem',), sub={'cb': .22}, drone=('C1', 'G1', 'C2'), wet=.26, revsec=2.6)
preview(f'{sys.argv[1]}/kglast.mp3', J, f'{sys.argv[1]}/kglast_preview.mp3')
