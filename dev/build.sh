#!/bin/sh
# v1.16 main(ac19f71)의 public/index.html에서 작업을 차례로 다시 쌓는다: sh dev/build.sh
# (11-14: main을 v2.00으로 합친 뒤로는 main이 이미 다 쌓인 파일이므로, 바탕은 v1.16 커밋으로 고정한다)
set -e
cd "$(dirname "$0")"
git show ac19f71:public/index.html > base.html
mkdir -p build; cp base.html build/game.html
python3 al_apply.py build/game.html            # ⓪ 속성·취향
python3 inject3.py batch3 3차 build/game.html   # ① BB·멜트릴리스·패션립
python3 cls_apply.py build/game.html           # ① 새 클래스 셋
python3 inject3.py batch4 4차 build/game.html   # ③ 스즈카 고젠 · 타마모 캣
python3 inject3.py batch5 5차 build/game.html   # 에미야[얼터]
python3 extras4.py build/game.html             # ③ 성향 말투 · 마성 · 매료 마안 · 낮잠
python3 bx_patch.py build/game.html            # ② 비스트 위기
python3 bxe_apply.py build/game.html           # ② 키아라 패배 뒤 에필로그
python3 rel_apply.py build/game.html          # ④ 관계 대사 · 짝 대사
python3 faces_apply.py build/game.html         # ④ 얼굴 135칸
python3 sw_apply.py build/game.html            # ⑤ 에필로그 애정 전환
python3 moon_apply.py build/game.html          # BB · 멜트 · 립 전용 소환 길
python3 sfx_apply.py build/game.html           # 소환 연출: 문 캔서 · 얼터 에고
python3 sfx_bb.py build/game.html              # 소환 연출: BB 전용(가로채는 소환)
python3 kiara_bgm_apply.py build/game.html       # 키아라 · BB 전투 배경음악
python3 ea_apply.py build/game.html              # 에미야[얼터]: 보구 특례 · 키아라 관계 대사
python3 fix1112_apply.py build/game.html         # 11-12 문의: 교회 의뢰 보상 · 죽마고우 → 지기
python3 alex_apply.py build/game.html            # 이스칸다르의 소원: 수육
python3 epi2_apply.py build/game.html            # 에필로그 시간 흐름: 일 · 달 · 해 구간
python3 bxach_apply.py build/game.html           # 비스트 위기 업적 17개 (11-13) · 선배와 후배 (11-14)
python3 ach_order_apply.py build/game.html       # 업적 화면: 업데이트된 순서 · 분류 순서 고정 (11-13)
python3 reg1113_apply.py build/game.html         # 갈림길 · 재촉 · 쉼 대사를 서번트 말투에 맞게 (11-13)
python3 bxscn_apply.py build/game.html           # 비스트 위기 화면 표시 · 시나리오 분리 (11-13)
python3 cxui_apply.py build/game.html            # 후반 위기 현판 (11-13)
python3 bxnun_apply.py build/game.html           # 비스트 위기: 수녀(키아라)의 소원 · 대사 · 이벤트 (11-13)
python3 epi1113_apply.py build/game.html          # 에필로그: 비스트 생의 검은 성배 사건 · 단꿈 생의 일상 사건 거르기 (11-13)
python3 bxabs_apply.py build/game.html           # 비스트: 봉인 중 흡수도 단서로 (11-13 · A안)
python3 cxmsg_apply.py build/game.html           # 비스트 유닛: 전투 종료 메시지 · 적 카드 · 정보창 문구 (11-13)
python3 fitchip_apply.py build/game.html          # 궁합 어긋남 칩: 서번트가 좋게 본 뒤에는 이어지는 문구로 (11-13 · A안)
python3 bxnote_apply.py build/game.html           # 비스트: 봉인 1~2일 뒤 BB의 쪽지 (11-13)
python3 bxally_apply.py build/game.html           # 키아라전: 동행(BB·멜트·립)과 호위를 카드·대사·행동 묘사로 (11-13)
python3 bxbye_apply.py build/game.html            # 키아라 처치 뒤 「새벽의 작별」 · 닫기 연출 (11-14)
python3 epi1114_apply.py build/game.html          # 에필로그: 키아라 결말에 안 맞는 사건 정리 (11-14)
python3 bxrec_apply.py build/game.html            # 기록 화면: 비스트 결말 문구 (11-14)
python3 bxui_apply.py build/game.html             # 기록 화면: 비스트 결말 카드 꾸밈 · 지난 생 분류 · 수녀 조 줄 (11-14)
python3 cap_apply.py build/game.html             # 결과 화면: 조 목록 초상화 · 캡처하기 (11-14)
python3 fix1113_apply.py build/game.html         # 11-13 문의: 인질 구출전 대화 · 인질 날 결투장 겹침
python3 lobby_apply.py build/game.html            # 로비 새 배경 · 새 배치 (11-13)
python3 lbsnd_apply.py build/game.html           # 로비 소리 아이콘: 켜지면 금색 (11-14)
python3 lbbond_apply.py build/game.html          # 로비: 인연 소환을 펼쳐도 태어나기 칸이 늘어나지 않게 (11-14)
python3 allyev_apply.py build/game.html          # 문의: 이미 동맹인 조가 동맹을 다시 걸어오던 것 (11-14)
python3 infox_apply.py build/game.html           # 정보 창 닫기 버튼을 아래에 띄움 (11-14)
python3 lbrec_apply.py build/game.html            # 로비: 기록 화면을 배경 위에 펼침 (A안 · 11-13)
python3 lb2_apply.py build/game.html              # 로비 두 단계 · 고풍 스타일 · 인연 소환 목록 (11-14)
python3 lbpop_apply.py build/game.html            # 로비에서 여는 팝업 · 기록 화면 고풍 스타일 (11-14)
python3 help_apply.py build/game.html             # 도움말: 소제목 + 한 문장씩 · 문장 다듬기 (11-14)
python3 ig1_apply.py build/game.html              # 게임 UI 1단계: 창 · 공통 부품 · 소리 스위치 (11-15)
python3 ig2_apply.py build/game.html              # 게임 UI 2단계: 화면 틀 (11-15)
python3 ig3_apply.py build/game.html              # 게임 UI 3단계: 기록 피드 (11-15)
python3 ig4_apply.py build/game.html              # 게임 UI 4단계: 상태 패널 (11-15)
python3 ig5_apply.py build/game.html              # 게임 UI 5단계: 선택 팝업 (11-15)
python3 ig6_apply.py build/game.html              # 게임 UI 6단계: 전투 · 위기 (11-15)
python3 ig7_apply.py build/game.html              # 게임 UI 7단계: 태어나기 (11-15)
python3 ig8_apply.py build/game.html              # 게임 UI 8단계: 결과 화면 (11-15)
python3 ig9_apply.py build/game.html              # 게임 UI 9단계: 알림 · 캡처 창 · 보낸 조 창 (11-15)
python3 ig10_apply.py build/game.html             # 설정 창 켜기/끄기 스위치 (11-15)
python3 lbstart_apply.py build/game.html          # 로비 시작 화면: 키보드로 넘겨도 소리를 깨움 (11-15)
python3 bug1115_apply.py build/game.html          # 11-15 커뮤니티 버그 제보 9건 (직장 연락 · 아줌마 · 강연 · 아이 각인 · 형제 대사 · 남은 령주 · 교회 청산 · 대화로 끝난 밤 · 마안 효과)
python3 relpick_apply.py build/game.html          # 인연 1단계에서 애정 · 우정 고르기 · 같은 성별 애정 · 아이 사건 출산 제외 (11-15)
python3 relopen_apply.py build/game.html          # 연애 가능으로: 멀린 · 솔로몬 · 시바의 여왕 (애정 대사 90줄 · 영어 · 일본어) (11-15)
python3 solhuman_apply.py build/game.html         # 사람이 된 솔로몬: 곁에 남는 조건 · 재능 선택지 11곳 · 재능 사건 6개 (11-15)
python3 lobbybgm_apply.py build/game.html         # 로비 배경음악 5곡: 로비로 들어올 때마다 무작위 1곡(바로 앞 곡 제외) · 예전 title 곡 대신 (11-15)
python3 lobbyfb_apply.py build/game.html          # 로비 피드백: 첫 배경음악 4초에 걸쳐 커짐 · 입장 단추(가운데) · ✕를 창 안으로 · 톱니바퀴 · 로비 단추 소리 (11-15)
python3 uifix_apply.py build/game.html            # UI 최신화 남은 곳: 기술 사건 설명 상자를 새 창 장식으로 (11-15)
python3 raidintel_apply.py build/game.html         # 저격 · 암습을 막아 내며 얻은 단서로는 상대 마스터의 소원을 알 수 없음(거처는 그대로) (11-15)
python3 wishsrc_apply.py build/game.html          # 소원은 만나거나 전해 들었을 때만: 산책 · 뒤밟기 · 흔적 · 정찰 · 공격은 거처만, 멀리서 본 싸움 등은 아무것도 (11-15)
python3 bxsent_apply.py build/game.html           # 수녀의 서번트가 센티넬이 될 때 이미 알던 진명 · 보구를 이어받음 (11-15)
python3 loading_apply.py build/game.html          # 로딩 화면: 성배에 금빛이 차오름 (11-13)
python3 bxfx_apply.py build/game.html            # 비스트 연출 ①~⑥: 봉인 · 빈 자리 · 강림 · 키아라 입장 · 단독현현 · 결말 (11-12 시안 → 11-13 연결)
python3 bxfx2_apply.py build/game.html           # 비스트 연출 ⑦~⑪: KP · 해방 · 봉인이 갈라짐 · 토벌령 · 격돌 (11-13 연결)
python3 pnver_apply.py build/game.html            # 패치 노트 버전 번호 v1.00~ (11-14)
python3 pn117_apply.py build/game.html            # 패치 노트 v2.00 (11-14)
