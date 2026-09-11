# 뉴로시민 | Everyday Neuroscience Lab

> **운영 하네스 버전: v1.1.0** · GitHub Pages 공익 뇌과학 리터러시 아카이브

뇌과학을 시민의 일상 언어로 설명합니다. 배움, 집중, 기억, 수면, 감정, 습관, 관계, 디지털 환경을 다루되, 연구 근거를 우선하고 의료적 진단·치료를 단정하지 않습니다.

- **편집 원칙:** 연구 근거 우선 · 쉬운 설명 · 과장 없는 해석
- **공개 원칙:** 후보군·점수·선정 과정은 내부 편집용이며 게시글에는 노출하지 않음
- **배포:** GitHub Pages — https://ai4tenlab.github.io/everyday-neuroscience-lab/

## 매일 발행 하네스

```text
07:30 KST  주제·근거 브리핑
08:30 KST  본 발행: 연구 확인 → 글·GPT Image 썸네일 → GitHub Pages 검증
09:10 KST  Recovery Guard: 누락·이미지·라이브 URL·OG 메타 재검증, 필요 시 복구
```

발행은 승인된 **OpenAI Codex GPT Image** 경로로 16:9 인물 중심 썸네일을 생성합니다. 썸네일은 파일·포맷·해상도·비율 검사와 시각 검토를 통과해야 커밋됩니다.

## 검증 도구

```bash
# 생성된 썸네일 단독 검사
python3 scripts/validate_thumbnail.py assets/images/thumbnails/YYYY-MM-DD-slug.png

# 당일 포스트·라이브 URL·OG 이미지까지 통합 검사
python3 scripts/verify_daily_publication.py --date YYYY-MM-DD
```

정상 결과는 각각 `THUMBNAIL_VALIDATION=pass`, `DAILY_PUBLICATION_VERIFICATION=pass`입니다. 실패하면 발행 성공으로 처리하지 않습니다.

## 다른 Hermes 노드에서 복제하기

새 노드(예: 백주경 박사님 Hermes)는 아래 운영 문서를 기준으로 동일한 발행·복구 구조를 만들 수 있습니다.

- [Hermes 복제·운영 가이드](docs/HERMES_REPLICATION.md)
- [운영 변경 이력](docs/CHANGELOG.md)
- 실제 발행 기준: [`CRON_PROMPT.md`](CRON_PROMPT.md)

> 보안 원칙: 이 저장소에는 토큰·`.env`·인증 파일을 넣지 않습니다. 새 노드의 GitHub/Resend/OpenAI Codex 인증은 각 노드에서 별도로 설정합니다.
