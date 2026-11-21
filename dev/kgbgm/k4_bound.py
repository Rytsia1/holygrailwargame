"""K4 묶인 잔 에필로그 — 오리지널 작곡. 참고곡(An Unending Path)에서 잰 큰 성격만: 약 66BPM(여기서는 반복 이음매를 샘플 단위로 맞추려고 64BPM), B 단조, 독주 악기 하나(북 없음 · 150Hz 아래 거의 없음),
어두운 가운데 음역(중심 약 1.2kHz), 숨처럼 크게 부풀었다 잦아드는 세기(약 10dB 폭), 빈 박이 많음.
주제(본성 속 진심)를 B 단조로: F#–G–F#–E–D–C–(B). 이 곡에서는 끝내 B까지 내려오지 않고 C(♭II)에서 멈춘 채 빈 마디로 넘어간다.
구성(1마디 3.75초): 도입 2 | 본문 16 = A 8 · B 8"""
import sys
from eng import *
S = Song('kgbound', 64, intro=2, body=16, loop_off=1, lufs=-18.5)
A_H = ['Bm', 'Gmaj7', 'D/F#', 'Em', 'Bm', 'Cmaj7', 'Em', 'F#sus']
B_H = ['Gmaj7', 'F#m', 'Em', 'Bm/D', 'Cmaj7', 'Bm', 'Em', 'Cmaj7']
A_M = [(None, Q), ('F#5', H + Q), ('G5', E8), ('F#5', DQ), (None, H), ('E5', Q), ('D5', Q), ('C#5', H), ('B4', W),
       (None, Q), ('F#5', H), ('A5', Q), ('G5', DQ), ('F#5', E8), ('E5', H), ('D5', Q), ('C5', Q), ('B4', H), (None, W)]
B_M = [('B5', H), ('A5', Q), ('F#5', Q), ('A5', DQ), ('F#5', E8), ('E5', H), ('G5', Q), ('F#5', Q), ('E5', Q), ('D5', Q), ('F#5', W),
       (None, Q), ('F#5', Q), ('G5', Q), ('F#5', Q), ('E5', H), ('D5', H), ('E5', Q), ('D5', Q), ('C5', H), (None, W)]

def lh(bar, ch, v=46):   # 왼손: 1박 바탕음 · 2박 반 5도 · 4박 3도, 다음 마디까지 울리게 길게 둔다(페달 대신)
    r = tone(CH[ch][0], 3); f = tone(CH[ch][2], 3); t3 = tone(CH[ch][1], 4)
    if f < r: f += 12
    if t3 < f: t3 += 12
    for p, n, dv in ((0, r, 6), (Q + E8, f, 0), (3 * Q, t3, -4)): S.add('pno', bar * S.BAR + p, S.BAR - p + Q, n, v + dv)

def intro():
    S.add('pno', 0, W, 'B4', 44); S.add('pno', Q + E8, W, 'F#4', 36); S.add('pno', 3 * Q, W, 'D4', 34)
    S.add('pno', S.BAR + Q, W, 'C5', 38); S.add('pno', S.BAR + 3 * Q, W, 'B3', 30)

def body(s):
    dynA = [44, 46, 48, 46, 52, 58, 52, 40]; dynB = [56, 60, 62, 58, 50, 46, 42, 36]
    for i, c in enumerate(A_H): lh(s + i, c, dynA[i])
    for i, c in enumerate(B_H): lh(s + 8 + i, c, dynB[i])
    t = s * S.BAR; k = 0
    for n, d in A_M:
        if n: S.add('pno', t, d * 1.5, n, dynA[min(7, (t - s * S.BAR) // S.BAR)] + 14)
        t += d
    t = (s + 8) * S.BAR
    for n, d in B_M:
        if n: S.add('pno', t, d * 1.5, n, dynB[min(7, (t - (s + 8) * S.BAR) // S.BAR)] + 14)
        t += d
    for b, n in ((s + 3, 'B5'), (s + 11, 'F#6')): S.add('pno', b * S.BAR + 3 * Q + E8, H, n, 30)   # 멀리서 한 음

intro(); body(S.intro); body(S.intro + S.body); body(S.intro + 2 * S.body)
J = S.render(sys.argv[1], {'pno': 0}, {'pno': (1.0, 0)}, wet=.34, revsec=3.0, lpf={'pno': 2600})
preview(f'{sys.argv[1]}/kgbound.mp3', J, f'{sys.argv[1]}/kgbound_preview.mp3')
