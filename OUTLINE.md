# 새 분석 논문 — 개요와 주장–근거 지도 (2026-11-01, AI 초안)

> 이 폴더는 새 분석 논문 전용이다. access2026(IEEE Access) 원고와 문장·표·그림을 공유하지 않는다. 폴더 대응은 `../access2026/harness/STUDY_INDEX_TWO_PAPERS.md`.
> 저자 지시: 사람이 쓴 것처럼, 읽기 쉽게, 과장 없이 주장마다 근거가 붙게. 별도 "지침"·"한계" 절은 두지 않는다. 초록은 긍정 프레이밍.

## 작업 제목
What Makes LLM-Built Knowledge Graphs Answer Held-out Questions? A Pre-registered Dissection of Competency-Question-Driven Curation

## 한 문장
CQ 기반 KG 큐레이션 파이프라인의 품질은 관계 스키마, 그다음 CQ가 덮는 범위에서 나오고, 평가-수정 반복의 이득은 추출된 사실의 양으로 설명된다.

## 글쓰기 원칙
- 결과 절은 지렛대가 큰 순서. 각 절 첫 문장이 그 절의 결론과 숫자다.
- 숫자는 `LEDGER.md`에 출처(file:key)가 있는 것만 쓴다. 효과는 점추정 + 95% CI + n.
- 판정 어휘는 사전 등록 문면 그대로(improved / not improved / inconclusive). "효과 없음"은 쓰지 않는다. 검정 못 한 것은 "검정하지 않았다".
- 문장 25단어 안팎, 한 문단 한 생각, 수동태·메타 문장("In this section we…") 최소.
- 연구 내부 번호(study22, D33)는 본문에 쓰지 않는다. 본문은 Exp 번호, 부록 표에 폴더 대응.

## 절 구성
1. Introduction — 문제(바텀업 KG, CQ로 조종·점검), 질문(무엇이 보류 질문 답변력을 만드나), 접근(사전 등록·하나씩 바꾸기·큐레이션 CQ/보류 질문 분리), 결과 네 줄, 기여.
2. Related Work — CQ 기반 온톨로지 공학과 LLM, 텍스트→KG 파이프라인, 반복 자기수정/프롬프트 최적화, KG-RAG. access2026은 측정 도구로 인용.
3. Pipeline and Components — 단계 ①–⑧과 실험에서 켜고 끄는 다섯 요소(스키마 시드, CQ 범위·수, 평가-수정 루프, 형식 제약, 생성 예산).
4. Experimental Design — 데이터(2Wiki 문항별 코퍼스, T-REx 영화 도메인; Brick은 부록), 큐레이션 CQ와 보류 질문 분리, 지표(근거 재현율 무예산/예산형, grounded QA, KG-only QA, Hybrid QA, 커버리지, 정밀도), 모델(Qwen3.8-Flash-Next 주, Gemma·Nemotron 복제), 사전 등록·통계(shard 클러스터 BCa, Holm, 3값 판정, 조작 확인, 계산량 맞춤 대조).
5. Results
   5.1 Schema is the largest lever (Exp8 seed 효과, Exp3 B-prior)
   5.2 Coverage comes next (Exp2/2b/4/5 G−L0; Exp9 CQ 수 × 예산: B4 vs G, A4, C4 — 4조건)
   5.3 What evaluate-and-repair adds (Exp4 실패 귀속, Exp5 미검출, Exp7 검정 불가, Exp8 부피 분해 + 복제)
   5.4 Errors are omissions (Exp6)
   5.5 Cost, and what CQs add over plain extraction (Exp8 U-ext+seed, CQ-40, 예산형 재현율, 조기 종료)
   5.6 Hybrid retrieval-augmented QA (Exp9 H null, 진단, 사전 지정 융합 결과) — 사실대로, 짧게
6. Discussion — 결과가 그리는 그림(한 문단씩): 어디서 품질이 오나, CQ의 역할(커버리지 도구 + 수용 시험), 측정상 교훈(부피·예산).
7. Conclusion
Appendix — 스터디 폴더 대응표, 사전 등록·편차 요약, 프롬프트, 추가 표.

## 실험 번호(본문) ↔ 폴더
| 본문 | 폴더 | 역할 |
|---|---|---|
| Exp1 | study19 | 폐루프 첫 검증(Brick, 부록) |
| Exp2 | study22 (+22b) | 2Wiki 루프 vs 일괄, TBox 경로 |
| Exp3 | study23 | CQ 생성 최적화 vs 스키마 사전 |
| Exp4 | study24 | CQ→SPARQL→judge 루프 |
| Exp5 | study25 | 신호 정리 루프 |
| Exp6 | study25a | 오류 유형·SHACL |
| Exp7 | study26 | 용량-반응(진입 조건 종료) |
| Exp8 | study27 | 결합 파이프라인·어블레이션·U-ext+seed |
| Exp9 | study30_rag_cq_scaling | CQ 수 × 예산, Hybrid RAG, 2모델 × 2데이터 |
| Rep | replic_gemma, study28 | Gemma·Nemotron 복제, T-REx 데이터 |
