"""K5 검귀 엔딩 곡 — 오리지널 작곡. 참고곡(Distant Bonds, 사무라이 렘넌트 OST의 끝 곡)에서 잰 큰 성격만:
55BPM(여기서는 이음매를 샘플 단위로 맞추려고 55.05BPM = 한 박 1.09초), C 단조, 앞 6마디(들어옴 2 + 첫 진술 4) 뒤 25마디가 한 바퀴:
고요 4(북 없음, −20dB) → 쌓임 4 → 오름 3(북이 들어옴) → 넘어감 1 → 절정 8(가장 큼 −14dB · 화음이 C–B♭–A♭–B♭ 식으로 돎) → 마무리 1 → 첫 진술 다시 4.
주제(본성 속 진심)를 C 단조로 진술하고(G–A♭–G–F–E♭–D♭–C), 절정에서는 게임 엔딩 곡의 조인 E♭ 장조로 풀렸다가, 마무리에서 다시 C 단조로 돌아온다.
구성(1마디 약 4.36초): 도입 6 | 본문 25"""
import sys
from eng import *
S = Song('kgend', 60e6 / 1090000, intro=6, body=25, loop_off=1, lufs=-18.0)
OPEN_H = ['Cm', 'Fm', 'Cm', 'G']
OPEN_M = [('G4', DQ * 2), ('Ab4', E8), ('G4', E8), ('F4', Q), ('Eb4', Q), ('Db4', Q), ('C4', Q), ('Eb4', DQ), ('F4', E8), ('G4', H), ('D4', H), ('B3', H - E8), (None, E8)]
Q_H = ['Ab', 'Eb/G', 'Fm', 'G7']
Q_M = [('C5', H), ('Eb5', H), ('Bb4', W), ('Ab4', H), ('C5', Q), ('F5', Q), ('D5', H), ('B4', H - E8), (None, E8)]
B_H = ['Cm', 'Eb/Bb', 'Ab', 'G']
B_M = [('G4', Q), ('C5', Q), ('Eb5', Q), ('D5', Q), ('Eb5', H), ('Bb4', H), ('C5', DQ), ('Bb4', E8), ('Ab4', Q), ('C5', Q), ('B4', W - E8), (None, E8)]
R_H = ['Ab', 'Fm', 'G', 'Bbsus4']
R_M = [('C5', H), ('Eb5', H), ('F5', H), ('Ab5', H), ('G5', H), ('F5', H), ('F5', H), ('Eb5', Q), ('D5', Q)]
C_H = ['Eb', 'Bb/D', 'Cm', 'Ab', 'Fm', 'Eb/G', 'Ab', 'Bb']
C_M = [('G5', DQ), ('F5', E8), ('Eb5', H), ('F5', DQ), ('Eb5', E8), ('D5', H), ('Eb5', Q), ('G5', Q), ('C6', Q), ('Bb5', Q), ('Ab5', H), ('Eb5', H),
       ('F5', DQ), ('G5', E8), ('Ab5', H), ('G5', DQ), ('F5', E8), ('Eb5', Q), ('G5', Q), ('Ab5', Q), ('Bb5', Q), ('C6', Q), ('Ab5', Q), ('Bb5', W - E8), (None, E8)]
K_M = [('G5', DQ * 2), ('Ab5', E8), ('G5', E8)]

def pno(bar, ch, v=52, up=True):   # 8분 펼침화음(한 박 1.09초라 느긋하게)
    ns = [tone(CH[ch][0], 2 if tone(CH[ch][0], 2) >= nn('F2') else 3)] + sorted(tone(x, 4) for x in CH[ch])
    pat = [ns[0], ns[0] + 7, ns[1], ns[2], ns[3], ns[2], ns[1], ns[0] + 12]
    for i, n in enumerate(pat): S.add('pno', bar * S.BAR + i * E8, (S.BAR - i * E8) * .9 if i == 0 else E8 * 3, n, v + (8 if i == 0 else 0))
def strings(bar, ch, v=56, octs=(3, 4)): S.chord('str', bar, ch, v=v, octs=octs)
def low(bar, ch, v=64):
    r = tone(CH[ch][0], 2)
    if r > nn('F2'): r -= 12
    S.add('cb', bar * S.BAR, S.BAR * .99, r, v + 10); S.add('cello', bar * S.BAR, S.BAR * .99, r + 12, v + 4)
    S.syn('drone', bar * S.BAR, 1 * S.BAR, .9 * v / 80, notes=(r, r + 7, r + 12), cut=300, a=.15, r=.2)
def pulse(bar, v=70, every=2):   # 낮은 북: 박마다 / 두 박마다
    for k in range(0, 4, every): S.add('taiko', bar * S.BAR + k * Q, Q, 'C3' if k == 0 else 'G2', v - (0 if k == 0 else 12))

def intro():
    for i in range(2):   # 들어옴: 낮은 C와 피아노 한 줄
        S.add('cb', i * S.BAR, S.BAR * .99, 'C2', 50 + i * 6); S.add('pno', i * S.BAR, W, 'C4', 40 + i * 6); S.add('pno', i * S.BAR + H, W, 'G4', 36 + i * 6)
        S.chord('str', i, 'Cm', v=36 + i * 8, octs=(4,))
    for i, c in enumerate(OPEN_H):   # 첫 진술: 퉁소가 주제를
        b = 2 + i; pno(b, c, 66); strings(b, c, 70); low(b, c, 74); pulse(b, 78)
        if i == 0: S.add('timp', b * S.BAR, Q, 'C2', 80)
    S.line('shaku', 2, OPEN_M, v=104)

def body(s):
    for i, c in enumerate(Q_H):   # 고요: 피아노와 플루트만
        b = s + i; pno(b, c, 62); strings(b, c, 48, octs=(4,)); low(b, c, 56)
    S.line('flute', s, Q_M, v=88)
    for i, c in enumerate(B_H):   # 쌓임: 현악 · 첼로 대선율
        b = s + 4 + i; pno(b, c, 62); strings(b, c, 62 + i * 4); low(b, c, 66 + i * 2); pulse(b, 62 + i * 4)
    S.line('flute', s + 4, B_M, v=96); S.line('cello', s + 4, [('Eb3', W), ('G3', W), ('C3', W), ('D3', W - E8), (None, E8)], v=60)
    for i, c in enumerate(R_H):   # 오름(3) + 넘어감(1): 북이 들어오고 현악이 올라간다
        b = s + 8 + i; pno(b, c, 60); strings(b, c, 68 + i * 4); low(b, c, 70 + i * 3)
        S.add('taiko', b * S.BAR, Q, 'C3', 70 + i * 8); S.syn('boom', b * S.BAR, Q, .35 + i * .1)
        S.add('timp', b * S.BAR, H, tone(CH[c][0], 2), 70 + i * 6)
        if i == 3:
            for k in range(16): S.add('timp', b * S.BAR + k * S16, S16, 'Bb1', 56 + k * 4)
            S.add('kit', b * S.BAR + H, H, 49, 70)
    S.line('vln', s + 8, R_M, v=84); S.line('horn', s + 8, R_M, v=72, oct=-1)
    S.syn('riser', (s + 10) * S.BAR, 2 * S.BAR, .6)
    for i, c in enumerate(C_H):   # 절정: E♭ 장조로 풀림 · 전원
        b = s + 12 + i; strings(b, c, 76, octs=(3, 4)); low(b, c, 84); S.chord('choir', b, c, v=70, octs=(4,))
        for k in range(4): S.add('pno', b * S.BAR + k * Q, Q * 1.6, tone(CH[c][0], 3), 58); S.add('pno', b * S.BAR + k * Q, Q * 1.6, tone(CH[c][0], 4), 54)
        pulse(b, 100, every=1); S.add('taiko', b * S.BAR + 2 * Q + E8, E8, 'G2', 82); S.syn('boom', b * S.BAR, Q, .6)
        S.add('timp', b * S.BAR, H, tone(CH[c][0], 2) if tone(CH[c][0], 2) >= nn('F2') else tone(CH[c][0], 3), 88)
        if i in (0, 4): S.add('kit', b * S.BAR, W, 49, 92)
        if i in (3, 7):
            for k in range(8): S.add('kit', b * S.BAR + H + k * S16 * 2, S16 * 2, 38, 50 + k * 6)
    S.line('vln', s + 12, C_M, v=100); S.line('horn', s + 12, C_M, v=92, oct=-1); S.line('flute', s + 12, C_M, v=78)
    b = s + 20   # 마무리: 다시 C 단조, 주제 첫마디만 높게 남는다
    strings(b, 'Cm', 62); low(b, 'Cm', 66); pno(b, 'Cm', 52); S.line('vln', b, K_M, v=80)
    for i, c in enumerate(OPEN_H):   # 첫 진술 다시(퉁소)
        bb = s + 21 + i; pno(bb, c, 64 - i * 2); strings(bb, c, 66 - i * 3); low(bb, c, 72 - i * 3); pulse(bb, 74 - i * 3)
    S.line('shaku', s + 21, OPEN_M, v=100)

intro(); body(S.intro); body(S.intro + S.body); body(S.intro + 2 * S.body)
PROG = {'pno': 0, 'str': 49, 'cb': 43, 'cello': 42, 'shaku': 77, 'flute': 73, 'vln': 48, 'horn': 60, 'choir': 52, 'timp': 47, 'taiko': 116, 'kit': 'drum'}
MIX = {'pno': (.85, .1), 'str': (.65, 0), 'cb': (.75, 0), 'cello': (.6, -.2), 'shaku': (1.15, -.1), 'flute': (1.0, -.15), 'vln': (1.0, .2), 'horn': (.85, -.3),
       'choir': (.6, 0), 'timp': (.7, -.1), 'taiko': (.6, 0), 'kit': (.6, 0)}
J = S.render(sys.argv[1], PROG, MIX, bright={'vln': .6, 'flute': .3}, hpf=('vln', 'choir', 'str'), sub={'cb': .26}, wet=.3, revsec=2.8, lpf={'pno': 3500})
preview(f'{sys.argv[1]}/kgend.mp3', J, f'{sys.argv[1]}/kgend_preview.mp3')
