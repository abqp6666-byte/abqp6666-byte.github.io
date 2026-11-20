# 오늘도 바쁜 AI 사무실 · AI Office Tycoon

도트(픽셀아트) AI 사무실 경영 타이쿤. 안드로이드 APK 로 설치하거나 브라우저에서 바로 플레이할 수 있습니다.
**인터넷 없이 100% 동작**합니다 (CDN·외부 폰트·외부 이미지 의존 0).

| | |
|---|---|
| 웹 (바로 플레이) | https://abqp6666-byte.github.io/ai-office-tycoon/ |
| APK 다운로드 | [Releases](https://github.com/abqp6666-byte/abqp6666-byte.github.io/releases/latest) |

## 게임 소개

대표님(CEO) 자리에 앉아 AI 직원들이 올리는 결재만 눌러 주면 되는 사무실 경영 게임입니다.
직원들은 자기 책상에서 일하다가 보고서를 들고 대표님 책상과 회의실로 걸어 다니고, 머리 위에 말풍선을 띄웁니다.

### 플레이

- **결재함** — AI 직원이 올리는 결재/문의/돌발 카드 38종. 선택지마다 보상(₩·XP)이 다릅니다.
- **직원** — 최대 12명 채용 (CS 미소, QUOTE 계상, REPORT 차곡, DATA 소리, BOOKING 두리, DOCS 영수, COST 다온, PR 새봄, DEV 하나, DESIGN 마루, LEGAL 누리, HR 민서). 레벨업으로 초당 수익 상승.
- **시설** — 회의실 확장 / 에스프레소 머신 / AI 서버랙 / 황금 명패 / 공기청정기. 사면 오피스 맵에 실제로 그려지고 전체 수익 배율이 오릅니다.
- **할 일** — 결재·채용·업그레이드·누적 수익 등 미션. 다 채우면 다음 라운드가 열립니다.
- **빠른 결재 / 2배 부스트** — 손맛용 즉시 처리와 30초 부스트.
- **자동 저장 + 오프라인 정산** — 앱을 꺼도 직원이 번 돈을 최대 8시간까지 정산해 줍니다.

## 구조

```
index.html                          게임 원본 (HTML+CSS+JS 단일 파일, 오프라인 번들)
app/                                Android WebView 프로젝트 (Gradle)
  src/main/assets/www/              빌드 시 ../index.html 이 자동 복사됨
  src/main/java/com/howgrow/aioffice/MainActivity.java
  src/main/res/mipmap-*/            런처 아이콘 (픽셀아트 로봇)
art/icon-512.png                    큰 아이콘 이미지
tools/make_icon.py                  아이콘 생성 스크립트
.github/workflows/build-apk.yml     (단독 저장소용) APK 빌드 + Release 업로드
```

## 빌드

```bash
# APK (Gradle 8.9+, JDK 17, Android SDK 34)
gradle assembleDebug
# → app/build/outputs/apk/debug/app-debug.apk

# 아이콘 다시 만들기
python3 tools/make_icon.py
```

`main` 에 푸시하면 GitHub Actions(`.github/workflows/build-apk.yml`)가 APK 를 빌드해 Release 에 `ai-office-tycoon.apk` 로 올립니다.

## 라이선스

개인 프로젝트 · 자유롭게 즐겨 주세요.
