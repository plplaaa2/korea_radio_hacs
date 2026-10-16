Home Assistant에서 대한민국 라디오를 편리하게 제어하기 위한 커스텀 통합 구성요소입니다. 이 구성요소는 **Korea Radio Add-on** 또는 호환되는 API 서버와 연동되어 작동합니다.

현재 버전은 **1.1.2**이며, Home Assistant **2026.10.0 이상**이 필요합니다.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/plplaaa2)

> [!IMPORTANT]
> **필수 애드온 설치:** 이 통합 구성요소를 사용하려면 먼저 아래 애드온이 설치되어 있어야 합니다.
> 
> [plplaaa2/korea_radio_addon: Korea Radio Home Assistant Addon](https://github.com/plplaaa2/korea_radio_addon)

- **Assist 도구 제공**: 도구 호출을 지원하는 LLM 대화 에이전트에서 Korea Radio 채널 재생을 요청할 수 있습니다.
- **미디어 브라우저 지원**: HA의 '미디어' 메뉴에서 라디오 채널을 탐색하고 재생할 수 있습니다.
- **동적 연동**: Home Assistant서버 정보를 기반으로 실시간 스트리밍 주소를 생성합니다. (Add-on 일때 한함)
- **최신 표준**: 최신 Home Assistant 개발 가이드를 준수하며, 로직이 캡슐화되어 유지보수가 용이합니다.
- **간편한 설정**: UI를 통해 서버 주소와 토큰을 입력하는 것만으로 설정을 마칠 수 있습니다.

### 자동설치 (권장)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=plplaaa2&repository=https%3A%2F%2Fgithub.com%2Fplplaaa2%2Fkorea_radio_hacs&category=integrate)

위 버튼을 누른 후 저장소 추가 후 HACS에서 Korea radio hacs를 검색하여 다운로드 합니다.

### 수동 설치
1. HACS에서 저장소를 추가 합니다.
   ```https://github.com/plplaaa2/korea_radio_hacs```
2. HACS에서 Korea radio hacs를 검색하여 다운로드 합니다.
3. Home Assistant를 재시작합니다.

1. HA 메인 화면에서 **설정 > 기기 및 서비스**로 이동합니다.
2. 우측 하단의 **통합 구성요소 추가** 버튼을 누릅니다.
3. **Korea Radio**를 검색하여 선택합니다.
4. 다음 정보를 입력합니다:
   - **Host**: 라디오 애드온 서버 주소 (예: `http://192.168.1.100:3005`)
   - **Token**: 애드온 설정에서 지정한 보안 토큰 (기본값: `homeassistant`)
   - **radio_port**: 라디오 애드온 설정에서 설정한 Addon 포트 (기본값: `3005`)
- **Playback Host (선택)**: 미디어 플레이어가 HA의 API 서버 주소로 접근할 수 없을 때, 플레이어에서 접근 가능한 애드온 호스트 주소를 입력합니다 (예: `http://192.168.1.50`). 포트는 입력하지 말고 `radio_port`에 설정하세요. 비워 두면 Host와 같은 주소를 사용합니다.

설정 과정에서 라디오 API 연결과 토큰을 확인합니다. 서버가 응답하지 않거나 토큰이 틀리면 설정 화면에 오류가 표시됩니다. 이미 등록한 동일 서버와 라디오 포트는 중복 등록할 수 없습니다.

연결 문제가 있으면 애드온이 실행 중인지, 입력한 호스트 및 라디오 포트가 맞는지, 애드온과 통합 구성요소의 토큰이 같은지 확인하세요. 기본 라디오 포트는 `3005`입니다.

미디어 브라우저, `play_radio` 서비스, Assist 재생 요청에 지정된 플레이어가 재생 호스트를 사용할 수 있어야 합니다. 해당 플레이어가 애드온 호스트와 포트에 네트워크로 연결할 수 있는지도 확인하세요.

### 제거
1. **설정 > 기기 및 서비스 > 통합 구성요소**에서 Korea Radio를 선택합니다.
2. 메뉴에서 **삭제**를 눌러 통합 구성요소를 제거합니다.
3. HACS의 **통합 구성요소** 화면에서 Korea Radio를 제거하고 Home Assistant를 재시작합니다.
4. 필수 애드온도 더 이상 사용하지 않는 경우 애드온 저장소에서 별도로 제거합니다.

### Assist 음성 제어
Korea Radio는 Home Assistant의 Assist 도구 목록에 **Korea Radio** 도구를 제공합니다. Assist에 사용할 미디어 플레이어를 노출하고, 도구 호출을 지원하는 LLM 대화 에이전트를 선택하세요. 예를 들어 “거실 스피커에서 KBS Cool FM 틀어줘”라고 요청할 수 있습니다.

Assist의 표시 이름은 **Korea Radio**이며 내부 도구 식별자는 `korea_radio_hacs__play_radio`입니다. 채널 키와 Assist에 노출된 미디어 플레이어 엔티티를 전달받아 재생합니다. 지원 채널은 `services.yaml`의 `play_radio` 목록을 따릅니다. LLM 도구 플랫폼은 Home Assistant 2026.10 이상이 필요합니다.

### 미디어 브라우저
가장 쉽고 직관적인 방법입니다. 별도의 설정 없이 HA UI에서 바로 채널을 선택할 수 있습니다.

1. Home Assistant 사이드바에서 **미디어(Media)** 메뉴를 클릭합니다.
2. 미디어 소스 목록에서 **Korea Radio**를 선택합니다.
3. 표시되는 라디오 채널 목록에서 원하는 채널을 클릭합니다.

### 서비스 호출 (`korea_radio_hacs.play_radio`)
자동화(Automation)나 대시보드 버튼에서 특정 채널을 재생하고 싶을 때 사용합니다.

| 필드 | 필수 | 설명 | 예시 |
| :--- | :---: | :--- | :--- |
| `entity_id` | Yes | 재생할 미디어 플레이어 엔티티 ID | `media_player.living_room_speaker` |
| `channel` | Yes | 재생할 채널 키 (대소문자 무관) | `KBSCoolFM`, `sbs_power`, `mbc_fm` |

**YAML 예제:**
```yaml
action: korea_radio_hacs.play_radio
data:
  entity_id: media_player.google_home_mini
  channel: KBSCoolFM
```

이 프로젝트는 [miumida/korea_radio](https://github.com/miumida/korea_radio) 프로젝트의 아이디어에서 영감을 받아 현대적인 구조로 재작성되었습니다.

이 프로젝트는 **MIT License**를 따릅니다.
