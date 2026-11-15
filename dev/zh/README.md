# 중국어 간체(zhs) · 번체(zht) 번역 작업

결정(11-16, 사용자): 간체 · 번체를 각각 한국어 원문에서 따로 번역 / 중국어권 FGO 공식 표기 / 전부 끝난 뒤 한 번에 공개.

## 파일
- `src.jsonl` 원문 목록: 사전(I18N_DICT, k=d) + 틀(I18N_TPL, k=t). id · 한국어 · 영어 · 일본어. `extract`로 다시 뽑아도 id는 유지.
- `done.json` 번역 결과: { 한국어 원문: [간체, 번체] }. 원문이 키라서 패치로 문장이 바뀌면 그 문장만 다시 번역 대상이 된다.
- `out/NNNNN.txt` 묶음별 번역 원본(형식: `#id` / `S: 간체` / `T: 번체`, 줄바꿈은 \n). `ingest`로 검사 후 done.json에 들어감.
- `official/names.json` 공식 이름표(일본어 → [간체, 번체, 종류]). 출처 chaldea-center/chaldea-data.
- `glossary.md` 용어 · 문장 부호 · 문체 규칙.

## 흐름
1. `python3 dev/zh/zhtool.py next 6000` → 다음 묶음(K 한국어 · J 일본어 · = 공식 이름 힌트)
2. 번역해서 `dev/zh/out/<첫 id>.txt`로 저장 → `python3 dev/zh/zhtool.py ingest dev/zh/out/<첫 id>.txt`
3. 문제가 나온 항목만 고쳐 다시 ingest. `stats`로 진행 확인. 몇 묶음마다 wip에 커밋.
4. 전부 끝나면 zh_apply.py(엔진: LANGS · 글꼴 · 문장 부호 · 패턴 · 화면 안 문구 · 사람 이름)로 게임에 넣고 언어 창에 켠다.

## 엔진에서 따로 옮길 것 (사전 밖)
- I18N_PAT(66) · I18N_NAMES(286, 사람 이름 조각) · I18N_CHIP · I18N_ATTR · CX_TR · TR_POS/TR_NEG · STAY_TR
- `{en:'…',ja:'…'}[LANG]` 꼴 화면 문구 약 124곳, `LANG==='ja'` 분기 20곳(문장 부호 · 이름 잇기 · 따옴표)

## 게임에 넣기 (11-16)
- `python3 dev/zh/zh_apply.py public/index.html` — 처음 한 번은 엔진을 고치고, 그다음부터는 사전 파일(`public/assets/i18n/zhs.js` · `zht.js`)만 다시 만든다. build.sh 맨 끝에도 들어 있다.
- 사전은 게임 파일 밖에 둔다(각 4.5MB). 로딩 화면 스크립트가 언어가 zhs · zht일 때만 불러온다. 사전에 없는 문장은 영어로 보인다.
- 엔진 밖 표: `zh_data.py`(사람 이름 286 · 숫자 틀 66 · 판정 칩 55). 화면 문구(로딩 · 제목 · 계절 · 출신 장면 · 이름 짓기 · 언어 창 · 로비)는 zh_apply.py 안에 있다.
- 공개 전: `ZH_ON=false` — 언어 창에 없고 브라우저 언어로 고르지 않는다. 주소 뒤 `?lang=zhs` · `?lang=zht`로만 켜진다(다시 `?lang=ko`로 돌아감).
- 공개: `python3 dev/zh/zh_apply.py public/index.html --on` (언어 창에 简体中文 · 繁體中文, 중국어 브라우저는 자동 선택).
- 패치로 문장이 늘면: `zhtool.py extract` → `next` → 번역 → `ingest` → zh_apply.py 다시 실행.
- 중국어만의 엔진 처리: 문장 부호 뒤 띄어쓰기 지움 · 앞에 끼워 넣는 말이 중국어에서 문장 가운데로 가는 틀은 한 문장만 받고 앞 문장은 따로 옮김 · 서양 이름은 `·`로 잇고 한·중·일 이름은 붙여 씀 · 대명사 자리 {n:he}는 他/她.
