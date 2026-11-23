"""11-23 커뮤니티 버그 묶음
① 새벽 서번트 한 줄: 「상처를 숨기려 하는 것을 보았다」가 다치지 않은 첫날 밤에도 나오던 것 → 서번트 체력이 80 아래일 때만
② 본성 속 진심 ② · ③(곁에 서번트가 남은 세계): 에필로그 서번트 카드가 「그 겨울의 서번트 · 떠남」으로 나오던 것
③ 휴대폰 브라우저의 강제 다크 모드가 이미 어두운 화면을 다시 뒤집어 능력치 막대가 안 보이던 것 → 이 페이지는 원래 어둡다고 알린다
사용: python3 fix1123_apply.py <game.html>"""
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read(); miss = []
def rp(o, n):
    global s
    if s.count(o) != 1: miss.append((o[:70], s.count(o))); return
    s = s.replace(o, n)
if 'fix1123' in s: print('이미 적용됨'); sys.exit(0)
rp("sayV(h,'dawn'),`새벽녘 ${h.name}${J(h.name,이)} 상처를 숨기려 하는 것을 보았다.`])",
   "sayV(h,'dawn'),...(w.hp<80?[`새벽녘 ${h.name}${J(h.name,이)} 상처를 숨기려 하는 것을 보았다.`]:[])])   /* fix1123 ① */")
rp("gone:done&&!stayHome(),", "gone:done&&!stayHome()&&!kgSide(),   /* fix1123 ② */")
rp('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
   '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><meta name="color-scheme" content="dark"><!-- fix1123 ③ -->')
# ④ 어머니가 세상을 떠난 뒤에도 「동생이 태어났다」가 나오던 것 (커뮤니티 제보: 홀아버지 집안인데 한 해 뒤 동생이 생김)
rp("c:()=>S.fam.sib&&S.origin!=='noble2'&&!S.once.c_sib,", "c:()=>S.fam.sib&&S.origin!=='noble2'&&!S.once.c_sib&&!!(S.fam.mother&&S.fam.mother.alive),   /* fix1123 ④ */")
if miss:
    for x in miss: print('못 찾음', x)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(s)
print('fix1123 적용')
