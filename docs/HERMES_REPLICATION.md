# Hermes 복제·운영 가이드 — 뉴로시민 v1.1.0

이 문서는 백주경 박사님 Hermes처럼 **별도 노드가 이 저장소만 기준으로 뉴로시민의 발행·이미지·검증·복구 구조를 재현**하기 위한 안전한 운영 명세입니다.

## 1. 복제 범위와 보안 경계

복제 대상은 아래의 공개 운영 자산입니다.

- `CRON_PROMPT.md`: 글쓰기·팩트 검증·발행 기준
- `scripts/validate_thumbnail.py`: 생성 이미지 fail-closed 검사
- `scripts/verify_daily_publication.py`: 당일 게시물의 로컬·라이브 검사
- 이 문서와 `docs/CHANGELOG.md`

다음은 저장소에 넣거나 다른 노드와 복사하지 않습니다.

- `.env`, API 키, GitHub 토큰, OAuth 파일, Resend 키
- Hermes `auth.json`, 세션 DB, 개인 대화 로그
- 수신자 개인정보·이메일 전송 마커

## 2. 새 노드 준비

```bash
git clone https://github.com/ai4tenlab/everyday-neuroscience-lab.git
cd everyday-neuroscience-lab
bundle install
hermes auth add openai-codex
hermes config check
gh auth status
```

필수 조건:

- GitHub 저장소 push 권한과 GitHub Pages 배포 권한
- OpenAI Codex 인증 및 Hermes `image_gen` 도구 활성화
- Python 3 + Pillow (`python3 -c 'from PIL import Image'`)
- 뉴스레터를 쓸 경우 해당 노드에만 Resend 자격증명을 별도 설정

`hermes config check`에서 비밀값을 채팅·로그·Git 저장소에 출력하지 않습니다.

## 3. 필수 Hermes 도구·스킬

### 도구

```text
web, terminal, file, browser, image_gen
```

### 스킬

```text
fact-check-research
universal-brand-blog-authority
aeo-geo-korean-natural-writing
github-workflow
k-drama-blog-thumbnail
```

## 4. 크론 3단계 구성

시간대는 **KST**로 설정합니다. 모델은 전역 기본값에 맡기지 말고 현재 사용 가능한 승인 모델로 명시적으로 고정합니다.

| 시각 | 역할 | 실패 시 행동 |
|---|---|---|
| 07:30 | 연구 후보 브리핑 | 발행 크론이 직접 신뢰 가능한 출처를 다시 찾음 |
| 08:30 | 본 발행 | 발행 실패를 보고하고 중복 게시 금지 |
| 09:10 | Recovery Guard | 누락·이미지·라이브 검증 실패 시 1회 복구 시도 |

### 본 발행 크론

- Workdir: 이 저장소 루트
- Prompt: `CRON_PROMPT.md`를 먼저 읽고 그대로 수행
- 모델: `openai-codex / gpt-5.6-terra` 또는 노드에서 검증한 동등한 승인 모델
- 필수 toolset: `web, terminal, file, browser, image_gen`

### Recovery Guard 프롬프트

아래 내용을 별도의 09:10 KST 크론으로 등록합니다.

```text
Use KST. First git pull --rebase origin main. Run:
python3 scripts/verify_daily_publication.py --date YYYY-MM-DD

If it prints DAILY_PUBLICATION_VERIFICATION=pass, respond exactly [SILENT].
If it fails because today's post is absent or any image/live metadata validation fails,
read and execute CRON_PROMPT.md to recover exactly one post. Use only the approved
Hermes image_generate OpenAI Codex GPT Image route. Validate the copied thumbnail
with scripts/validate_thumbnail.py, commit/push, then rerun the daily verifier.
Never duplicate a post, use a placeholder image, or claim success without a passing
live verifier. Report only a compact actionable failure if recovery cannot complete.
```

## 5. 발행 성공의 정의

아래 명령이 성공하고, 라이브 검증까지 통과해야 합니다.

```bash
bundle exec jekyll build
python3 scripts/verify_daily_publication.py --date YYYY-MM-DD
git diff --check
git status --short
```

이미지 생성 도구가 반환한 경로를 실제 `assets/images/thumbnails/YYYY-MM-DD-slug.png`로 복사한 뒤에만 다음 검사를 수행합니다.

```bash
python3 scripts/validate_thumbnail.py assets/images/thumbnails/YYYY-MM-DD-slug.png
```

`THUMBNAIL_VALIDATION=pass`가 아니면 발행하지 않습니다.

## 6. 장애 대응 순서

1. `hermes cron list`에서 브리핑·발행·Recovery Guard가 enabled인지 확인한다.
2. 해당 작업의 **model/provider가 명시적으로 고정**돼 있는지 확인한다.
3. 실패 로그에서 `429`, `404`, 모델 드리프트, 이미지 검증, Git push, Pages 배포, 이메일 가드를 구분한다.
4. 모델 오류면 인증된 현재 모델로만 재고정한다. 무승인 제공자로 우회하지 않는다.
5. `scripts/verify_daily_publication.py --date YYYY-MM-DD`를 실행해 실제 결손 상태를 확정한다.
6. Recovery Guard를 1회 수동 실행한다. 당일 글이 이미 있으면 절대 중복 발행하지 않는다.
7. 복구 후 라이브 URL과 이미지 HTTP 200, OG/Twitter 메타를 다시 확인한다.
8. 같은 유형의 장애가 재발하면 이 문서와 `docs/CHANGELOG.md`를 새 버전으로 갱신한다.

## 7. 비보장 사항

이 하네스는 모델 변경·이미지 실패·배포 지연·누락 게시를 조기에 막고 복구하도록 설계됐지만, 외부 제공자 장애, 인증 만료, GitHub/Resend 장애를 100% 제거할 수는 없습니다. 대신 실패를 숨기지 않고 **fail-closed 검증과 09:10 Recovery Guard**가 조기에 감지·복구·보고합니다.
