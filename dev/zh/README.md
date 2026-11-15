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
