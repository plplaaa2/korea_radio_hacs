# 📻 Korea Radio HACS Integration (v3.0.0)

Home Assistant에서 대한민국 라디오를 편리하게 제어하기 위한 커스텀 통합 구성요소입니다. 이 구성요소는 **Korea Radio Add-on** 또는 호환되는 API 서버와 연동되어 작동합니다.

## 🚀 주요 특징

- **미디어 브라우저 지원**: HA의 '미디어' 메뉴에서 라디오 채널을 직접 탐색하고 재생할 수 있습니다. (New!)
- **동적 연동**: 서버 정보를 기반으로 실시간 스트리밍 주소를 생성합니다.
- **최신 표준**: 최신 Home Assistant 개발 가이드를 준수하며, 로직이 캡슐화되어 유지보수가 용이합니다.
- **간편한 설정**: UI를 통해 서버 주소와 토큰을 입력하는 것만으로 설정을 마칠 수 있습니다.
- **하위 호환성**: 기존에 사용하던 서비스(`play_radio`)와 채널 이름들을 그대로 사용할 수 있습니다.

## 🛠 설치 방법

### 수동 설치
1. 이 저장소의 `korea_radio` 폴더를 다운로드합니다.
2. Home Assistant의 `config/custom_components/` 디렉토리 안에 `korea_radio` 폴더를 통째로 복사합니다.
3. Home Assistant를 재시작합니다.

## ⚙️ 설정 방법

1. HA 메인 화면에서 **설정 > 기기 및 서비스**로 이동합니다.
2. 우측 하단의 **통합 구성요소 추가** 버튼을 누릅니다.
3. **Korea Radio**를 검색하여 선택합니다.
4. 다음 정보를 입력합니다:
   - **Host**: 라디오 애드온 서버 주소 (예: `http://192.168.1.100:3005`)
   - **Token**: 애드온 설정에서 지정한 보안 토큰 (기본값: `homeassistant`)

## 📻 사용 방법

### 1. 미디어 브라우저 (추천)
Home Assistant 왼쪽 메뉴의 **미디어** 항목을 클릭한 후, **Korea Radio**를 선택하면 등록된 모든 라디오 채널을 한눈에 보고 즉시 재생할 수 있습니다.

### 2. 서비스 호출 (`korea_radio.play_radio`)
기존 방식인 서비스 호출을 통해서도 라디오를 재생할 수 있습니다.

| 필드 | 필수 | 설명 | 예시 |
| :--- | :---: | :--- | :--- |
| `entity_id` | Yes | 재생할 미디어 플레이어 엔티티 ID | `media_player.living_room_speaker` |
| `channel` | Yes | 재생할 채널 키 (대소문자 무관) | `KBSCoolFM`, `sbs_power`, `ebs` |

## 📝 기여 및 라이센스
이 프로젝트는 [miumida/korea_radio](https://github.com/miumida/korea_radio) 프로젝트의 아이디어에서 영감을 받아 현대적인 구조로 재작성되었습니다.

이 프로젝트는 **MIT License**를 따릅니다.
