"""설정 창 켜기/끄기 스위치(11-15): 소리 · 익명 통계 · 다른 플레이어의 조 · 시작/격돌/령주 연출.
- 판 단추 → 줄 전체가 눌리는 스위치 줄(아이콘 · 이름 · 오른쪽 스위치)
- 이름은 단추 글자('소리 · 꺼짐')에서 마지막 ' · ' 앞을 data-n으로 옮겨 보여 준다(글자는 감추되 남겨 두어 스크린 리더가 그대로 읽음)
- 스위치 그림은 게임 안 사운드 스위치와 같은 모양(켜짐 파란 바탕 · 금빛 손잡이)
사용: python3 ig10_apply.py <game.html>"""
import sys
CSS = r'''
/* ---- 설정 창 스위치 (ig10_apply) ---- */
/* 설정 창: 켜기/끄기를 스위치 줄로 */
:root{--swOn:url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20width%3D%2742%27%20height%3D%2724%27%20viewBox%3D%270%200%2042%2024%27%3E%3Cdefs%3E%3ClinearGradient%20id%3D%27t%27%20x1%3D%270%27%20y1%3D%270%27%20x2%3D%270%27%20y2%3D%271%27%3E%3Cstop%20offset%3D%270%27%20stop-color%3D%27%232a3a78%27%2F%3E%3Cstop%20offset%3D%271%27%20stop-color%3D%27%2317224d%27%2F%3E%3C%2FlinearGradient%3E%3ClinearGradient%20id%3D%27k%27%20x1%3D%270%27%20y1%3D%270%27%20x2%3D%271%27%20y2%3D%271%27%3E%3Cstop%20offset%3D%270%27%20stop-color%3D%27%23f6e8bf%27%2F%3E%3Cstop%20offset%3D%271%27%20stop-color%3D%27%23c2a062%27%2F%3E%3C%2FlinearGradient%3E%3C%2Fdefs%3E%3Crect%20x%3D%27.75%27%20y%3D%27.75%27%20width%3D%2740.5%27%20height%3D%2722.5%27%20rx%3D%2711.25%27%20fill%3D%27url%28%23t%29%27%20stroke%3D%27%23d8bd7c%27%20stroke-width%3D%271.2%27%2F%3E%3Ccircle%20cx%3D%2730%27%20cy%3D%2712%27%20r%3D%278%27%20fill%3D%27url%28%23k%29%27%2F%3E%3C%2Fsvg%3E");--swOff:url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20width%3D%2742%27%20height%3D%2724%27%20viewBox%3D%270%200%2042%2024%27%3E%3Crect%20x%3D%27.75%27%20y%3D%27.75%27%20width%3D%2740.5%27%20height%3D%2722.5%27%20rx%3D%2711.25%27%20fill%3D%27%23090c17%27%20stroke%3D%27%235a554c%27%20stroke-width%3D%271.2%27%2F%3E%3Ccircle%20cx%3D%2712%27%20cy%3D%2712%27%20r%3D%278%27%20fill%3D%27%236f6a5f%27%2F%3E%3C%2Fsvg%3E")}
.dlg:not(#dlg) .set-sec .pn-btn.st{display:flex!important;width:100%;box-sizing:border-box;border:0!important;border-image:none!important;background:var(--swOn) right 2px center/42px 24px no-repeat!important;filter:none!important;border-radius:0!important;padding:4px 52px 4px 2px!important;margin-bottom:8px;min-height:34px;font-size:0!important;color:#e8d3a0!important;gap:10px}
.dlg:not(#dlg) .set-sec .pn-btn.st[aria-pressed=false]{background-image:var(--swOff)!important;color:#8f8878!important}
.dlg:not(#dlg) .set-sec .pn-btn.st::before{width:15px;height:15px;background:currentColor!important}
.dlg:not(#dlg) .set-sec .pn-btn.st::after{content:attr(data-n);font:700 14.5px/1.4 var(--lbF);color:#ece3cc;letter-spacing:.02em;text-align:left}
.dlg:not(#dlg) .set-sec .pn-btn.st[aria-pressed=false]::after{color:#a39c8a}
.dlg:not(#dlg) .set-sec .pn-btn.st:hover::after{color:#f3e8cb}
.dlg:not(#dlg) .set-sec .pn-btn.st:focus-visible{outline:1px solid rgba(216,189,124,.6);outline-offset:3px}
'''
JS = r'''
<script>/* 설정 창 스위치 이름 (ig10_apply) */
(()=>{ const up=b=>{ const t=b.textContent, i=t.lastIndexOf(' · '), n=i>0?t.slice(0,i):t; if(b.dataset.n!==n) b.dataset.n=n; };
 document.querySelectorAll('.set-sec .pn-btn.st').forEach(b=>{ up(b); new MutationObserver(()=>up(b)).observe(b,{childList:true,characterData:true,subtree:true}); }); })();
</script>
'''
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read()
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    i = s.rindex('</body>'); s = s[:i] + JS + s[i:]
    print('ig10 ok')
    open(P, 'w', encoding='utf-8').write(s)
