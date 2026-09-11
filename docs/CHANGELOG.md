# 뉴로시민 운영 하네스 변경 이력

이 문서는 **콘텐츠 변경 이력**이 아니라, 재현 가능한 발행·검증·복구 운영 장치의 버전 이력입니다.

## v1.1.0 — 2026-09-11 KST

### 배경

9월 7일에는 추론 사용 한도(`HTTP 429`)가 발생했고, 9월 8~10일에는 이전 고정 모델 `gpt-5.5`의 접근 불가(`HTTP 404`)로 발행이 멈췄습니다. 9월 11일에는 전역 모델 변경 뒤 비고정 크론의 비용 방지 정책이 실행을 건너뛰었습니다.

### 개선

- 뉴로시민 **07:30 브리핑**과 **08:30 발행** 크론을 `openai-codex / gpt-5.6-terra`로 명시적으로 고정했다.
- 승인된 OpenAI Codex GPT Image 경로만 썸네일 생성에 사용하도록 `CRON_PROMPT.md`를 보강했다.
- `scripts/validate_thumbnail.py`를 추가해 파일 존재·손상·포맷·최소 해상도·16:9 비율을 fail-closed로 확인한다.
- 매일 **09:10 KST Recovery Guard**를 추가해 당일 포스트, 썸네일, 라이브 URL, OG/Twitter 메타, 이메일 상태를 재검증하고 누락 시 복구한다.
- `scripts/verify_daily_publication.py`를 추가해 다른 노드에서도 로컬·라이브 검증을 재현할 수 있게 했다.
- 브리핑(07:30) → 발행(08:30) → 복구(09:10) 일정과 문서 표현을 일치시켰다.

### 검증 기준

발행 완료는 아래를 모두 충족할 때만 인정한다.

1. 당일 `_posts/YYYY-MM-DD-*.md`가 정확히 1개
2. `THUMBNAIL_VALIDATION=pass`
3. 로컬 Jekyll 빌드 성공
4. 라이브 포스트와 이미지 HTTP 200
5. `.post-thumbnail`, `og:image`, `twitter:card=summary_large_image`, JSON-LD 확인
6. `LIVE_URL_VERIFIED=yes` 및 이메일 가드 상태 확인

## v1.0.0 — 초기 운영

- GitHub Pages 기반 일일 뇌과학 리터러시 포스팅
- 연구 근거·AEO/GEO 구조·16:9 인물 중심 썸네일·라이브 검증을 기본 운영 기준으로 채택
