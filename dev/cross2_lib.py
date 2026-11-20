# 11-20: 갈림길 추가(61장면) 공통 도구
# 사건 JS 안의 문자열은 ⟦한국어¦영어¦일본어¦간체¦번체⟧로 적는다. 빌드할 때 한국어 문자열로 바뀌고 번역은 따로 모인다.
import re
TOK = re.compile(r'⟦(.*?)⟧', re.S)

def compile_js(src, tr):
    def rep(m):
        parts = m.group(1).split('¦')
        if len(parts) != 5: raise ValueError('번역 칸이 5개가 아님: ' + m.group(1)[:60])
        ko = parts[0]
        tr.append(tuple(parts))
        return "'" + ko.replace('\\', '\\\\').replace("'", "\\'") + "'"
    return TOK.sub(rep, src)
