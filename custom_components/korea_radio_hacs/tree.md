# Korea Radio Project Structure

```
\korea_radio_hacs
├── custom_components/
│   └── korea_radio_hacs/
│       ├── translations/
│       │   └── ko.json          # 한국어 번역 파일
│       ├── __init__.py          # 통합 구성요소 진입점
│       ├── api.py               # API 클라이언트 및 URL 생성 로직
│       ├── config_flow.py       # UI 설정 흐름 (설정 및 재구성)
│       ├── const.py             # 상수 및 채널 매핑
│       ├── manifest.json        # 통합 구성요소 메타데이터
│       ├── media_source.py      # 미디어 브라우저 구현
│       ├── services.yaml        # 서비스 정의
│       ├── strings.json         # 기본 현지화 문자열
│       └── tree.md              # 프로젝트 구조
├── hacs.json                    # HACS 설정 파일
├── LICENSE                      # MIT 라이센스
└── README.md                    # 사용자 가이드
```
