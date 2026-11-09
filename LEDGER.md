# 수치 장부 — 원고에 쓰는 숫자와 출처 (2026-11-01)

> 원고의 모든 숫자는 여기 있어야 한다. 상태: **확인**(메인 세션이 파일에서 직접 재계산·대조) / **에이전트**(서브에이전트가 파일에서 읽음, 메인 미대조) / **정정**(초안 값과 달랐음).
> 경로 기준: `paper/access2026/harness/`.

## Exp9 — study30_rag_cq_scaling (MAIN 4조건, shard 클러스터 BCa 95%, B = 10,000)
출처: `study30_rag_cq_scaling/analysis/results_{tag}_{ds}_main.json` → `contrasts.<key>.{delta, ci95, n_shards}`

| 대비 | qwen T-REx | gemma T-REx | gemma 2Wiki | qwen 2Wiki | 상태 |
|---|---|---|---|---|---|
| n shards (대비) | 33 | 26 | 20 | 24 | 확인 |
| K_acc B4−G (`Kacc_B4-G`) | +.035 [+.007, +.068] | +.056 [+.020, +.098] | +.109 [+.041, +.159] | +.062 [+.003, +.104] | 확인 |
| cov B4−G (`cov_B4-G`) | +.003 [−.011, +.021] | +.010 [+.001, +.023] | +.092 [+.055, +.154] | +.099 [+.069, +.132] | 확인 |
| H B4−G (`H2_B4-G`) | +.003 [−.022, +.026] | +.006 [−.022, +.036] | +.006 [−.037, +.056] | −.036 [−.089, +.010] | 확인 |
| K_acc A4−G (`Kacc_A4-G`) | +.047 [+.016, +.080] | +.050 [+.017, +.082] | +.106 [+.025, +.172] | +.016 [−.047, +.057] | 에이전트 |
| cov A4−G | +.019 [+.008, +.039] | +.006 [−.002, +.020] | +.095 [+.059, +.156] | +.120 [+.088, +.156] | 에이전트 |
| H A4−G (`H1_A4-G`) | +.009 [−.028, +.042] | +.003 [−.022, +.026] | −.009 [−.047, +.034] | −.091 [−.138, −.055] | 에이전트(qwen 2Wiki 확인) |
| prec B4−G (`H3_prec_B4-G`) | .000 [−.052, +.050] | −.005 [−.052, +.038] | +.049 [+.008, +.094] | −.040 [−.090, +.007] | 에이전트 |
| prec A4−G | −.124 [−.180, −.078] | −.012 [−.048, +.024] | +.033 [−.006, +.071] | −.122 [−.170, −.064] | 에이전트 |
| K_acc B4−E4B (진단 파일) | +.003 [−.042, +.036] | +.019 [−.012, +.055] | +.025 [−.031, +.066] | −.042 [−.107, −.003] | 에이전트 |
| F2 B4−G (D32 사전 지정) | — | — | — | +.013 [−.021, +.039] | 확인 |

실패 셀: qwen T-REx 0/363, gemma T-REx 78/363 (21.5%), gemma 2Wiki 47/264 (17.8%), qwen 2Wiki 0/264 (에이전트).
절대값(G / B4): K_acc qwen T-REx .395/.431, gemma T-REx .268/.332, gemma 2Wiki .441/.550, qwen 2Wiki .537/.599; V qwen T-REx .529, gemma T-REx .454, gemma 2Wiki .344, qwen 2Wiki .521 (에이전트, 일부 확인).
토큰(M, 유닛 평균 합계 기준 아님 — 셀 평균): A4 ≈ 2.8–3.8 × G, B4 ≈ G (에이전트).
근거 확인 루프 첫 시도 탈락률: qwen T-REx 6.88%, gemma T-REx 4.70%, gemma 2Wiki 2.72%, qwen 2Wiki 2.61%; 최종 탈락 0.17–0.74% (에이전트).
설계: G 40 CQ; A4 160 CQ @4× 예산; B4 160 CQ @1×; C4 40 CQ @4×; E4B 160 CQ @1×, 근거 확인 끔. 예산 B = 유닛별 D arm 토큰, 0.95·k·B에서 정지. Hybrid = KG 사실 ≤ 30 + 상위 3청크, V = 상위 5청크(code/s30_qa.py 확인). 정밀도 = 셀당 40사실, 교차 계열 판정. 2Wiki 24 shard × 16 보류 질문, T-REx 33 shard(보류 507문항), seed 1 (에이전트).
iText2KG T-REx: qwen 14,065 facts, cov_p .047, prec .700; gemma 6,272, .053, .805; G cov_p qwen .221, gemma .136 (에이전트+이전 세션 확인).

## Exp1–Exp6 (study19–25a) — 에이전트 전 항목 CONFIRMED (results.json 기준)
지표가 스터디마다 다르다: Exp2·Exp3 = 근거 재현율, Exp4·Exp5 = grounded QA(정답 ∧ 근거), Exp1 = gold ASK 통과(Brick TTL 렌더 코퍼스). 한 사다리로 나란히 놓지 않는다.
| 항목 | 값 | 출처 |
|---|---|---|
| Exp4 G − L0 (grounded QA) | +.0906 [.0469, .1375] (양측, 사후 secondary), 40 shard × 8문항 = 320/arm | study24 results.json `/secondary/G-L0` |
| Exp4 GR − L0 | +.0969 [.0406, .150] | `/H1_GR_vs_L0` |
| Exp4 실패 귀속 | round-0 실패 676 중 질의 쪽 526 (77.8%: query_error 453, entity_mismatch 73), KG 쪽 22.0% | `/operating_point/checks` |
| Exp4 GR − GR-null / GR − GR-exec | +.0188 / .000 | `/secondary` |
| Exp4 judge "2" | 정밀도 .943–.977, 재현율 .723–.857, κ .744–.868 (단일 Qwen, 사람 검증 없음) | `/judge_validity` |
| Exp4 비용 | G 162,723 tok vs GR 481,017 (33.8%), 평가 42.5%; G 1차 .475 vs GR .481 (98.8%) | `/cost` |
| Exp5 G − L0 | +.0964 [.0521, .1484], 24 shard × seed 2, 768/arm | study25 results.json `/secondary/G-L0` |
| Exp5 H1 GR2 − GR2-null | −.0026, 단측 [−.0365, +.0313] → not improved (δ .05) | `/H1_GR2_vs_GR2null` |
| Exp5 GR2 − G | +.0130 [−.0078, +.0365] | `/secondary/GR2-G` |
| Exp5 QA ~ 커버리지 | G−L0 QA .096 / cov .102; S-budget2−G .074 / .086; GR2−G .013 / .019 | `/structure_contrasts` |
| Exp2 A0 → A1 | 재현율 .093 → .377; CQ 12.0 → 85.8; 속성 14.76 → 23.46 | study22 REPORT_ko.md:51–52; study22b results.json `/tbox_sizes` |
| Exp2 A1 − A2s′ (같은 CQ 수 일괄) | +.0115 [−.0347, +.0566] (crossed) | study22 `/contrasts/C1_A1-A2s` |
| Exp2 진단 선택 | 5,744/5,760 (99.72%)이 미커버 청크 | study22 REPORT |
| Exp2b U-ext 반복 전 TBox | −.2011 [−.2505, −.1508], 0/24 shard 승 | study22b `/q1/U0_minus_U1` |
| Exp3 (test n = 400) | B-prior .425, MIPROv2 .363, GEPA .356; 트리플 맞춤 B-prior .411 > GEPA .337 > MIPROv2 .255 > B0 .181; M-CQ − B0 +.142 (단측 [.121, .163]), 맞춤 +.073 | study23 `/arm_means`, `/hypotheses_fixed_sequence/H1` |
| Exp6 오류 유형 (비정확 gold 1,336/2,196) | 누락 87.3%, 엔티티 분리 7.2%, 오값 5.5% | study25a `/headline_q1_A1` |
| Exp6 SHACL | 탐지 0.15% [0, 0.37%], 리프트 1.04 [0.81, 1.28], 정확 사실 오경보 25.1%; ΔAUC +.006 [−.003, +.015]; 핵심 질문 AUC .48/.47 | `/q3_L0_judge_outcome`, `/extension_s24/qa_ext` |
| Exp1 C1 A1 − A0 | +.214 [.162, .271], n = 35 — 구성상 양수(PLAN §0.1)이므로 효과 크기 헤드라인으로 쓰지 않는다; A2s .362 > A1 .257 | study19 `/contrasts/C1` |
## Exp8 — study27_ours_final (2Wiki, 30 shard × seed 2 = 60유닛, 비교군당 보류 질문 960)
| 항목 | 값 | 출처 | 상태 |
|---|---|---|---|
| 시드 QA(gc) 상승 | L0 +.1469, LOOP +.0938, Ours +.0927, U-ext +.0448 [+.0073, +.0875] | post_review/results_postreview.json `contrasts.*.gc` | 에이전트(U-ext 확인) |
| 시드 포함률 | dev gold **근거** 관계의 98.36% (n = 1,216 근거); 질문 단위 95.8%; 관계 22종 | results.json `seed_audit` | 확인(98.36) |
| Ours − U-ext+seed | gc +.0031 [−.0312, +.0354]; cov_primary +.0061 [−.0055, +.0187]; 예산형 재현율 pr_b +.0396 [+.0165, +.0618]; CQ-40 통과율 +.1353 [+.1069, +.1631] | results_postreview.json | 확인 |
| 토큰 | U-ext+seed 105,866 vs Ours 837,655 (12.6%) | `arm_means.*.tok_total` | 에이전트 |
| Ours−seed − U-ext | cov −.0759 [−.1007, −.0497]; gc −.0448 [−.0740, −.0104] | results_postreview.json | 에이전트 |
| H1 Ours − LOOP+seed (Qwen) | cov_primary +.0556 [.0421, .0701] (단측 BCa); 예산형 −.0873; gc +.0073 [−.0281, +.0333] | results.json `primary.H1` | 에이전트 |
| H2 Ours − L0+seed | cov +.1403 [.1208, .1594]; 예산형 −.0831; gc +.0656 | results.json | 에이전트 |
| QA 천장·비용 | Ours−passes gc .6073 @ 0.277M; Ours .6062 @ 0.838M; LOOP+seed .5990 @ 0.878M; U-ext+seed .6031 @ 0.106M | arm_means | 에이전트 |
| 조기 종료(v2, 탐색, 기술 CI) | 54/60유닛, 토큰 −21.5%, Δcov −.0031 [−.0068, −.0016] | es_results.json `versions.v2` | 에이전트 |

## 복제 — replic_gemma (Gemma, Nemotron)
| 항목 | 값 | 출처 | 상태 |
|---|---|---|---|
| s27 H1 Ours − LOOP+seed **cov_primary** | Gemma +.0924 [.0763, .1136] (n = 60); Nemotron +.1311 [.0892, .1683] (n = 41); Qwen +.056 | gemma_repair_main.json `primary.H1`; nemotron_repair_main.json | 확인(Gemma) |
| 사실 수 맞춤(부피 보간) H1 | Gemma +.003 [−.006, +.011] (p .23, 30 shard); Nemotron +.003 [−.005, +.013] | gemma_repair_vs_old.md:39,64; replication_final_summary.md:13 (Nemotron은 요약 인용) | 확인(Gemma, 파일 문면) |
| 같은 방향 재현 | s19 C1 Gemma +.421 [.336, .507]; s24 H1 Gemma +.131 [.078, .184]; s21 Gemma +5.5pp | RESEARCH_LOG…:67–75 | 에이전트 |
| s25 H1 | Qwen −.003; Gemma +.0146 [−.031, +.065]; Nemotron −.007 [−.019, .000] | RESEARCH_LOG | 에이전트 |
| T-REx (Gemma, n = 27) | H1 +.0156 [−.0093, +.0441]; H2 +.0273 [−.0040, +.0576], not established | gemma_trex_main.json | 에이전트 |
주의: 부피 맞춤 +.003은 **재현율**이며 QA가 아니다. 원 Qwen의 부피 보간값은 장부에 없음 → 원고에 "원 모델에서도"라고 쓰지 않는다.

## Exp7 — study26 (스모크 12유닛, 진입 조건에서 종료)
③ R − G: 3x +0.78pp, 5x +2.47pp; EVAL − R5c +0.28pp, 양측 95% [−3.1, +4.2]; 표적 적중 EVAL 8.9% vs R_c 9.7–10.1% (기저 7.1–7.6%); 미커버 97건 중 누락 81–89%; 수정 계층 G 대비 +1.8–2.5pp (에이전트, REPORT_ko.md / results_smoke_5x.json).

## R1 추가 (메인 확인, 2026-11-01)
- Exp8 비교군 평균(post_review/results_postreview.json `arm_means`; gc / cov_primary / pr_b / 토큰 / 사실 수): U-ext .5583/.8737/.5124/100,039/1,704; U-ext+seed .6031/.8946/.6037/105,866/1,472; L0 .3937/.6460/.6088/130,989/725; L0+seed .5406/.7605/.7264/107,850/687; LOOP .5052/.7680/.6177/1,061,185/1,134; LOOP+seed .5990/.8451/.7305/878,308/980; Ours .6062/.9007/.6433/837,655/1,435; Ours−seed .5135/.7978/.5622/838,162/1,418; Ours−expand .5865/.8241/.6529/836,653/1,191; Ours−passes .6073/.8542/.7422/277,341/972. (확인)
- Exp8 H1 cov_primary 구간: **양측** ci95 [.0421, .0701], 단측 하한 lo1 .0441 (results.json `primary.H1.cov_primary`) (확인)
- Exp4 GR − GR-null: +.0188 [−.0156, +.0531], 단측 하한 −.0094, 판정 inconclusive(operating_point_failed) (study24 results.json `H3_GR_vs_GRnull`) (확인)
- Exp2 A1 − A2s′ 원 BCa [−.025, .049], crossed [−.0347, +.0566] (에이전트)
- 복제 범위(RESEARCH_LOG:65–76): Gemma = s19, s20, s21, s24, s25, s26(사후 main), s27, s28 T-REx; Nemotron = s25, s27, s28(n=12) (s19·s21·s24는 무효/floor 표기). s22·s22b·s23 미복제. Gemma T-REx(Exp8 설계) H1 +.0156 [−.0093, +.0441], H2 +.0273 [−.0040, +.0576] not established. (확인: 로그 문면)
- Exp9 C4 − G K_acc (arm 평균 차, 구간 없음): qwen T-REx +1.5, gemma T-REx −0.5, gemma 2Wiki +1.0, qwen 2Wiki 0.0 pt (확인: 셀 평균 .4101−.3953 등)
- Exp9 A4/G 토큰비(셀 평균): qwen T-REx 2.84, gemma T-REx 1.86, gemma 2Wiki 3.82, qwen 2Wiki 3.99 → "1.9–4.0배" (확인)
- Exp9 1차 지표 = Hybrid QA(H_acc), 사전 등록(study30 PLAN §8–10) (에이전트); 진단 83–88% / 16–23% (analysis/hybrid_diag_20261101*.md, 이전 세션 확인)
- 설계 상수: 시드 관계 22종; L0 TBox ≤ 36속성; LOOP 라운드당 CQ +20, K=3 (study27 PLAN §4–5, 확인); T-REx 482문서(dev 96/holdout 386), 관계 14종, 질의 626(holdout 507) (study28 README, 에이전트); shard 8문항(Exp4) / 16문항(Exp5·Exp8·Exp9) (확인)
- 부피 보간 방법: 스냅샷 곡선(사실 수, 재현율)에서 두 비교군의 겹치는 사실 수 구간을 20점 선형 보간, shard BCa (study27 PLAN §6, 확인)

## R2 추가 (메인 확인)
- Exp7 진입 조건 ③: 균등 무작위 R − G ≥ 3pp(사전 등록, primary 커버리지) (study26 REPORT_ko.md:13, NEW_PAPER_PLAN §3 C5) (확인)
- 질문 제외: Exp4는 Exp2·Exp3 질문 제외, Exp5는 Exp2–Exp4 제외, Exp8은 Exp2–Exp7(study22–26) 질문 ID 전부 제외, Exp9 2Wiki는 study22–27 제외(qid 충돌 0) (study27 PLAN §3, study30 D26; 확인)
- CQ-40: (shard, seed)마다 중립 프롬프트(시드 없음)로 무작위 40청크에서 생성한 새 CQ 40개, 어떤 루프에도 쓰지 않음; 최종 KG마다 SPARQL을 3회 새로 생성; 통과 = 결과 행 ≤ 20 ∧ 기대 답 span이 결과에 있음 ∧ judge 점수 2; 통과율 = 3회 평균 (study27 PLAN §7, 확인)

## R3 추가 (메인 확인, 원 파일)
- **Exp8 Qwen 부피 보간 H1(cov_primary)**: +.0112 [+.0048, +.0191] (study27 results.json `primary.H1.volume_interp`) → 사실 수를 맞추면 세 모델 모두 0.3–1.1pt (확인)
- Exp8 H1 예산형 재현율: −.087 [−.106, −.068]; H2 −.083 (study27 REPORT_ko.md:91) (확인)
- Exp4 게이트 수용률 98.3% (flag gate_acceptance_out_of_range) (study24 results.json `operating_point.checks.acceptance_rate`) (확인)
- Exp5 GR2 − G 구간 상한 +.0365 → 3.7pt (반올림 정정)
- Exp3 +14.2 / +7.3은 MIPROv2(M-CQ) − B0 (확인)
- Exp6 상태 수(Exp2 그래프, gold 2,196): 정확 860, 오값 74, 누락 1,166, 분리 96. 정렬이 속성명 규칙·거친 관계 클래스에 의존하므로 누락이 과대 분류됐을 수 있음(REPORT §한계). 다른 5개 비교군 누락 비율 78–98% (study25a REPORT_ko.md:12–23,47) (확인)
- 복제 표(RESEARCH_LOG:65–76, 확인=로그 문면): Gemma s19 C1 +.421 [.336,.507]; s20 NOT_DISTINGUISHABLE; s21 +5.5pp [+2.0,+9.5]; s24 H1 +.131 [.078,.184]; s25 H1 +.0146 [−.031,+.065] not improved; s26 사후 main −.0092 [−.029,+.009] inconclusive; s27 H1 +.0924 [.076,.114], H2 +.1021 [.021,.161]; T-REx H1 +.0156 [−.009,+.044], H2 +.0273 [−.004,+.058] not established. Nemotron: s25 −.007 [−.019,.000]; s27 H1 +.1311 [.089,.168] (n=41), H2 +.1673 [.118,.209]; T-REx n=12 H1 +.0117 [−.006,+.041] not established. s19·s21·s24 Nemotron 무효/floor.
- Exp9 근거 확인(grounding) 루프: CQ 생성 → 임베딩 → 상위 5청크 검색으로 출처 근거 확인 → 실패 시 최대 3회 재생성 (study30 PLAN, 이전 세션 확인)
- 시드 포함률 98.36%의 분모: Exp8 본실행 평가 질문 480개(2Wiki dev 분할)의 gold 근거 1,216건 (study27 results.json seed_audit; 확인)

## R4 추가 (메인 확인)
- Exp9 1차 지표 = Hybrid QA: 등록 H1 `H-acc(A4) − H-acc(G) > 0`, H2 `B4 − G > 0` (study30 PLAN.md:84) (확인). cov_primary = study27 정의의 무예산 근거 재현율, 2차 (PLAN.md:69) (확인)
- Exp9 C4 − G K_acc: results JSON에 대비 없음(구간 미계산) (확인, contrasts 키 목록)
- Exp9 확장 arm: 모델별 토큰 예산 초과 뒤 저자 결정으로 결과에서 제외, 결과 미계산 (study30 DEVIATIONS D34·D35, 확인)
- Hybrid 진단 기권: qwen T-REx B4에서 벡터 단독 정답을 Hybrid가 놓친 48건 중 15건이 기권 (hybrid_diag_20261101.md 표 `via H-abstain`) (확인). "대체로 unknown"이라고 쓰지 않는다.
- 예산형 재현율 한도: 질문마다 출처 문장당 트리플 2개(M_q = ceil(2.0 × 출처 문장 수)), 초과분은 초기하 기대값으로 감점 (study27 scorer_2wiki.py RHO_DEFAULT = 2.0) (확인)
- F2 정의: 벡터 단독 답이 기권이면 KG 단독 답, 아니면 벡터 단독 답 (hybrid_diag md L6) (확인)
- Exp8 평가 질문: 480개 × seed 2 = 비교군당 채점 960건 (study27 PLAN §3) (확인)
- Exp7: Qwen은 진입 조건에서 종료(본실행 없음); Gemma 복제에서는 진입 조건 통과 후 사후 본실행 −0.9 [−2.9, +0.9] inconclusive (로그) (확인)
- 등록 상태: Exp2 A1 − A2s′ = 사전 등록 1차 대비(Holm 3개 중 하나, δ .05) (study22 REPORT_ko.md:42,61) (확인). Exp8 시드 효과(+seed − 무시드) = 가설검정 없이 CI만 내는 기술 대비 (study27 PLAN §2 "어블레이션·U-ext·… 시드 없는 기준선 대비는 CI만") (확인)

## R5 추가 (메인 확인)
- Exp8 시드 효과 gc(기술 대비, CI만): L0+seed − L0 +.1469 [.1094, .1844]; LOOP+seed − LOOP +.0938 [.0635, .1219]; Ours − Ours−seed +.0927 [.0604, .1208]; U-ext+seed − U-ext +.0448 [.0073, .0875] (results_postreview.json, 확인)
- Exp9 K_acc·cov = 2차 지표(등록 가설 H1–H5는 H-acc·정밀도) (study30 PLAN §7–8, 확인)
- Exp9 Hybrid 진단(사후): (1c) 160 CQs/1× 에서 40 CQs/1× 대비 KG 단독으로 새로 맞힌 문항 중 Hybrid(160/1×)도 맞힌 비율 = qwen T-REx 38/46 (.826), gemma T-REx 30/34 (.882), gemma 2Wiki 48/56 (.857); (b) 벡터 단독 정답 중 Hybrid가 틀린 비율 16–23% (arm별) (hybrid_diag_20261101.md, 확인)
- 복제 모델명: Gemma-4-26B-A4B-it, Nemotron-3.5-Lightning-30B-A3B (RESEARCH_LOG:19–21, 확인)
- Exp4 평가 토큰 42.5% = GR 총 토큰 481,017 중 평가 204,540 (확인)
- bootstrap B = 10,000: Exp8(study27 PLAN §2), Exp9 확인. 다른 실험은 각 PLAN 값 — 원고에는 "Exp8·Exp9에서 10,000" 으로만 씀

## R6 추가 (메인 확인)
- 시드와 평가 질문 비겹침: Exp8 질문 576개 중 2Wiki train과 qid 겹침 0, 정규화 질문문 일치 0 (study27 PLAN §3) (확인)
- Exp2 A1 − A2s′ 판정: inconclusive; 24 shard × seed 3 (study22 REPORT_ko.md:49,61; 큐레이션 기록) (확인)
- Exp9 source check: 40 CQs/1×(G) 와 160 CQs/1×(B4) 모두 켬, E4B만 끔 (study30 PLAN §6 "루프 OFF(E)") (확인)
- 판정자 모델: Exp4·Exp8 내부 CQ 평가·CQ-40 판정 = 빌더와 같은 Qwen 계열(Qwen3.8-Flash-Next); Exp9 정밀도 = 교차 계열(Qwen 그래프는 Gemma가, Gemma 그래프는 Qwen이 판정) (study27 PLAN §7, study30 agent 추출) (확인)
- Exp4 실패 범주 원문: query_error 453, entity_mismatch 73 → 원고 "query errors and entity mismatches"
- Gemma 복제의 G−L0 값은 장부에 없음(GR−L0 +.131만 있음)

## R7 추가 — 서론 사례 (메인 확인, 원 예측 파일)
- Exp8, shard main10, seed 20261101, qid 8d2587f2…: "What is the cause of death of director of film Wedding Bills?" 정답 Parkinson. 근거: (Wedding Bills, director, Erle C. Kenton), (Erle C. Kenton, cause of death, Parkinson) — 출처 문장 "He was born in Norborne, Missouri and died in Glendale, California from Parkinson's disease."
- L0 답 "unknown"; L0 검색 사실에 (Wedding Bills, director, Erle C. Kenton) 있음, Kenton의 사인 트리플 없음 (Kenton 속성: birthYear, nationality, birthPlace, burialPlace). L0+seed 답 "Parkinson's disease", 근거 트리플 (Erle C. Kenton, causeOfDeath, Parkinson's disease). "cause of death"는 시드 22종에 포함. (predictions/main/main10/s20261101/L0.json, L0plusseed.json; 확인)
- 같은 조건에서 L0 오답·L0+seed 정답(gc)인 개방형 문항 40개 (에이전트 집계, 단일 shard-seed 아님 — 전체 집계 기준)
- 임베딩 Qwen3-Embedding-0.6B (last-token): study30 D23, Exp9에만 해당 (확인, 이전 세션)
- 시드 제시 방식: 관계명만, 알파벳순, 빈도·비율 없음 (study27 PLAN §3, 확인)

## R8 추가 — 사후 동등성 분석 (review/analyses/equivalence.md, LLM 0, 다중비교 미보정; 에이전트 계산, 저장 per-shard 값 재평균으로 delta 일치 확인)
- 90% CI(TOST): Exp9 hybrid 160 vs 40 CQs at 1×: qwen T-REx [−1.8, 2.3] (MDE80 3.1); gemma T-REx [−1.7, 3.1] (3.7); gemma 2Wiki [−3.4, 4.7] (6.1); qwen 2Wiki [−8.1, 0.3] (6.4) — 동등 아님(하락 방향 불확실)
- Exp8 combined − U-ext+seed gc: 90% [−2.6, 3.0], MDE80 4.2 → ±3pt 경계, ±5pt 배제
- Exp8 combined − LOOP+seed gc: 90% [−2.2, 2.9], MDE80 3.9
- Exp5 GR2 − GR2-null: 90% [−3.7, 3.1], MDE80 3.4 < 등록 마진 5

## R9 추가 — 사후 시드 정렬 분석 (review/analyses/seed_alignment.md; analyze27 부트스트랩 재사용, 게시값과 일치 확인; LLM 0)
시드 효과(시드 − 무시드), 95% BCa, 30 shard: 
- L0: cov_primary +.114 [.093,.145]; cov_agnostic +.097 [.076,.129]; correct(관계·근거 무관) +.138 [.105,.172]
- LOOP: cov_primary +.077; cov_agnostic +.050 [.029,.069]; correct +.079 [.048,.107]
- Ours: cov_primary +.103; cov_agnostic +.068 [.051,.086]; correct +.070 [.040,.097]
- U-ext: cov_primary +.021 [.010,.035]; cov_agnostic +.006 [−.007,.023]; correct +.030 [.000,.066]
읽기: L0/LOOP/Ours에서는 정렬 무관 지표에서도 하한 > 0 (cov_agnostic이 primary의 65–85%; L0 .097/.114=85%, LOOP .050/.077=65%, Ours .068/.103=66% — R11에서 64→65 정정, 원고 표기 "65 to 85%"). U-ext에서는 정렬 무관 지표에서 사라짐.
- Exp3 B-prior = 관계 이름과 비율을 준 고정 지시문 (NEW_PAPER_PLAN §3 C2; study27 PLAN §1 "관계명 주입"); Exp8 시드 = 관계 이름만, 빈도·비율 없음 (확인)

## R10 synonym seed (study32 B1) — 사전 등록 확인 실험 (원 파일에서 직접 읽음, 2026-11-01; LLM 호출 사전 해시 고정)
출처: `study32_reviewer_checks/b1_b4/b1/results.json` (경로 기준 `paper/access2026/harness/`), 설계 `study32_reviewer_checks/b1_b4/PLAN.md` §2, 편차 `DEVIATIONS.md` D1(스모크 게이트 방법 교체, 고정 파일 무변경)·D2(사후 어휘 진단 코드 추가). 원고에는 내부 코드(study32, B1, D1)를 쓰지 않는다.
설계: Qwen, 2Wiki, Exp8 harness; `n_units` 60, `n_shards` 30, 실행 시드 20261031·20261101 (`seeds`), 실패 셀 0 (`arms.*.failed_cells`); 시드 22개 관계명을 어간이 겹치지 않는 동의어구로 치환; 시드 없음·원 시드 arm은 저장된 Exp8 arm 재사용(PLAN §1: 같은 가중치·요청 설정, 다른 서버 인스턴스). 단위 = 점(pp), 소수 첫째 자리.
| 원고 값 | 값 | JSON 키 경로 |
|---|---|---|
| H1 L0+synonym seed − L0, answer correct | +15.4 [11.3, 19.5] (0.15417; [0.1125, 0.19479]) | `primary.H1.correct.{delta,ci95}` |
| H1 Holm p / 판정 | 0.0002 / improved | `primary.H1.p_holm`, `primary.H1.verdict` |
| H1 class-free recall (cov_agnostic) | +12.4 [9.2, 16.0] | `primary.H1.cov_agnostic.{delta,ci95}` |
| H2 U-ext+synonym seed − U-ext, answer correct | +1.6 [−1.4, 4.2]; Holm p 0.15558; not established | `primary.H2.correct.{delta,ci95}`, `primary.H2.p_holm`, `primary.H2.verdict` |
| H2 class-free recall | +0.4 [−0.5, 1.5] | `primary.H2.cov_agnostic.{delta,ci95}` |
| 2차 L0: synonym − no seed, grounded QA (gc) | +15.8 [11.5, 20.3] | `secondary.L0.synseed_minus_base.gc.{delta,ci95}` |
| 2차 L0: synonym − original seed, answer correct | +1.7 [−2.0, 5.0] | `secondary.L0.synseed_minus_seed.correct.{delta,ci95}` |
| 2차 U-ext: synonym − original seed, answer correct | −1.5 [−4.2, 1.4] | `secondary.U-ext.synseed_minus_seed.correct.{delta,ci95}` |
| 2차 L0: synonym − original seed, 클래스 정렬 recall (cov_primary) | −13.7 [−19.6, −8.4] | `secondary.L0.synseed_minus_seed.cov_primary.{delta,ci95}` |
| 2차 U-ext: synonym − original seed, cov_primary | −10.1 [−11.8, −8.8] | `secondary.U-ext.synseed_minus_seed.cov_primary.{delta,ci95}` |
| 원 시드의 U-ext 효과(answer correct, 기존 R9와 동일 값) | +3.0 [0.0, 6.6] | `secondary.U-ext.seed_minus_base_reference.correct.{delta,ci95}` |
| 사후(비등록): 동의어 어간을 가진 사실 비율, L0 | 원 시드 6.2% → 동의어 시드 47.0% | `b1/vocab_posthoc.json` `L0plusseed.syn_stem_share` .0623 → `L0plussynseed.syn_stem_share` .4701 |
| 사후(비등록): 같은 비율, U-ext | 6.2% → 30.6% | `U-extplusseed.syn_stem_share` .0619 → `U-extplussynseed.syn_stem_share` .3061 |
읽기: L0 시드 효과는 이름 정렬이 아니라 추출 효과다(이름 정렬 recall은 떨어지는데 QA는 유지). H2 U-ext는 원 시드 효과 자체가 작아(+3.0) 확립되지 않음. 동의어-원 시드 차이는 두 구간 모두 0 포함.

## R11 study32 B2·B3 — 사전 등록 확인 실험 (원 파일 `study32_reviewer_checks/b2_b3/results.json`에서 main이 직접 읽음, 2026-11-02; DEVIATIONS D1–D3)
Qwen 그래프(Exp8 보관 상태, 30 shard × run seed 2), shard-cluster BCa B=10,000.
| 항목 | 값 | 키 |
|---|---|---|
| B2 사실 precision (Gemma 판정, 교차 계열, pass 1), 결합(Ours) | .716 [.686, .741] | `B2.arms.Ours` |
| 〃 U-ext+seed | .925 [.913, .938] | `B2.arms.U-ext+seed` |
| 〃 LOOP+seed | .802 [.785, .819] | `B2.arms.LOOP+seed` |
| 〃 L0+seed | .874 [.856, .890] | `B2.arms.L0+seed` |
| B2 등록 대비 U-ext+seed − Ours (비열등 마진 −5pt) | +20.9 [18.0, 24.3], 단측 하한 18.5 → non-inferior | `B2.contrast_Uextseed_minus_Ours` |
| B2 판정 반복 일치율 | .90 (Ours) – .94 (U-ext+seed) | `mean_pass_agreement` |
| B3 vector QA (V, 그래프 없음) | .502 [.460, .544] | `B3.V` |
| B3 hybrid QA (H) L0 / L0+seed / Ours / U-ext+seed / LOOP+seed | .600 / .692 / .603 / .585 / .671 | `B3.arms.*.H_acc_shard_mean` |
| B3 H − V (서술, 모든 arm 구간 0 제외) | L0 +9.8 [4.3, 14.6]; L0+seed +19.0 [14.7, 22.5]; Ours +10.1 [5.3, 14.2]; U-ext+seed +8.3 [2.2, 13.9]; LOOP+seed +16.9 [12.2, 21.0] | `B3.arms.*.H_minus_V` |
| B3 H(Ours) − H(L0) | +0.3 [−4.2, 3.9] (서술) | `B3.contrast_H_Ours_minus_H_L0` |
| B3 H(U-ext+seed) − H(Ours) | −1.8 [−5.1, 1.8] (서술) | `B3.contrast_H_Uextseed_minus_H_Ours` |
상태: B2 대비 1개는 등록(결정 규칙: 비열등), B3 7개 구간은 등록된 서술(가설 검정 아님). 실패 셀 0. 토큰 Gemma 3.37M, Qwen 4.87M.

## R12 study32 B4 — Qwen on T-REx, Exp8 arms (원 파일 `study32_reviewer_checks/b1_b4/b4/results.json`, main이 직접 읽음 2026-11-02)
33 holdout shard × run seed 1 (20261031), shard-cluster BCa B=10,000, 실패 셀 0. seed = 2Wiki 관계 어휘(T-REx 전용 아님). 1-hop gold.
| 항목 | 값 | 키 |
|---|---|---|
| arm 평균 gc (grounded QA) | L0+seed .290; LOOP+seed .346; Ours .371; U-ext+seed .421 | `arms.*.gc.mean` |
| arm 평균 cov_primary | L0+seed .173; LOOP+seed .189; Ours .228; U-ext+seed .184 | `arms.*.cov_primary.mean` |
| arm 평균 토큰/unit | L0+seed 22.7k; LOOP+seed 310k; Ours 298k; U-ext+seed 19.1k | `arms.*.tok_total.mean` |
| 예산 일치 Ours/LOOP+seed 토큰 | .961 (.950–.979), 33/33 band 내 | `ours_over_loopseed_tokens` |
| 등록 TOST(±3pt) Ours − U-ext+seed, gc | −5.0, 90% [−8.1, −1.1], p_TOST .816 → 동등 아님(U-ext+seed가 높음) | `registered_Ours_minus_Uextseed.gc` |
| 〃 cov_primary | +4.4, 90% [+3.0, +6.0], p_TOST .953 → 동등 아님(Ours가 높음) | `….cov_primary` |
| 등록 라벨 | "equivalence not established on at least one measure" | `….label` |
| 2차 Ours − LOOP+seed (95%) | gc +2.4 [−0.8, 6.1]; cov_primary +3.9 [2.4, 5.8] | `secondary.LOOP+seed` |
| 2차 Ours − L0+seed (95%) | gc +8.1 [5.2, 12.4]; cov_primary +5.5 [3.8, 7.7] | `secondary.L0+seed` |
파생(승인 필요): U-ext+seed 토큰은 Ours의 약 1/15(19.1k vs 298k) — 원고에는 두 값을 그대로 쓰고 비율은 저자 승인 후.

## R13 사후 분석 — 커버리지 대비와 교차 모델 seed 효과 (review/analyses/coverage_crossmodel.{py,json}, LLM 0; main이 Qwen seed 효과 재현값을 장부 R9/line 118과 대조, 2026-11-02)
(applied to LEDGER R13 by main 2026-11-02)
All labeled post hoc; B = 10,000, seed 20261031; source `paper/cq_dissection/review/analyses/coverage_crossmodel.json`.
| item | value | key |
|---|---|---|
| Qwen U-ext − L0 gc | +.1646 [+.1062, +.2167] | `qwen.A["U-ext - L0"].gc` |
| Qwen U-ext − L0 correct | +.2146 [+.1562, +.2729] | `qwen.A["U-ext - L0"].correct` |
| Qwen U-ext − L0 cov_primary | +.2277 [+.1987, +.2583] | `qwen.A["U-ext - L0"].cov_primary` |
| Qwen U-ext − L0 n_facts Δ | +979 [+904, +1,053] (1,704 vs 725) | `qwen.A["U-ext - L0"].n_facts`, `qwen.arm_means` |
| Qwen U-ext+seed − L0+seed gc / correct / cov_primary | +.0625 [+.0260, +.0938] / +.1073 [+.0729, +.1406] / +.1341 [+.1105, +.1568] | `qwen.A["U-ext+seed - L0+seed"]` |
| Qwen U-ext+seed − L0+seed n_facts Δ | +785 [+711, +843] (1,472 vs 687) | same |
| Volume-matched U-ext vs L0 | not feasible (1 snapshot/arm) | `qwen.snapshot_counts` |
| Gemma seed effect gc: L0 / LOOP / Ours | +.0740 [+.0333, +.1125] / +.0750 [+.0125, +.1500] / +.0927 [+.0573, +.1292] | `gemma.seed_effect.*.gc.itt` |
| Gemma seed effect correct: L0 / LOOP / Ours | +.0729 [+.0271, +.1177] / +.0604 [−.0073, +.1385] / +.0521 [+.0208, +.0781] | `gemma.seed_effect.*.correct.itt` |
| Nemotron seed effect gc: L0 / LOOP / Ours | +.0013 [.0000, +.0037] / −.0075 [−.0288, −.0013] / +.0125 [−.0037, +.0275] (floor) | `nemotron.seed_effect.*.gc.itt` |
| Nemotron seed effect correct: L0 / LOOP / Ours | +.0013 [−.0088, +.0088] / −.0213 [−.0437, −.0013] / +.0100 [−.0387, +.0325] | `nemotron.seed_effect.*.correct.itt` |
| Qwen U-ext+seed − U-ext correct | +.0302 [+.0000, +.0656] (new; gc +.0448 already in ledger) | `qwen.seed_effect["U-ext+seed - U-ext"].correct` |
주의: Nemotron은 모든 arm gc ≤ .047 바닥 → 정보 없음(효과 없음의 증거 아님). U-ext vs L0 사실 수 맞춤 비교는 불가(arm당 스냅샷 1개).

## R14 study32 B9 — volume-matched coverage (사전 등록, `study32_reviewer_checks/b9_volume/results.json`, main이 직접 읽음 2026-11-02)
Qwen 2Wiki Exp8, 30 shard × 2 run seed, 실패 0, 토큰 0.88M. 저장된 U-ext(±seed) 그래프에서 사실을 균일 무작위로 L0(±seed)와 같은 개수만큼 추출(sha256 seeded) 후 같은 QA 답변기·채점기.
| 항목 | 값 | 키 |
|---|---|---|
| H1 U-ext@L0size − L0, gc | −28.2 [−33.2, −23.4] (95%), Holm p 1.0 → not improved | `registered.H1.gc` |
| H2 U-ext+seed@L0+seed-size − L0+seed, gc | −39.1 [−44.1, −34.2] (95%), Holm p 1.0 → not improved | `registered.H2.gc` |
| 사실 수 맞춘 arm 평균 gc | U-ext@L0size .111; U-ext+seed@L0+seed-size .150 (L0 .394, L0+seed .541) | `arms.*.gc.mean` |
| 사실 수 맞춘 arm cov_primary | .380 / .430 (L0 .646, L0+seed .760) | `arms.*.cov_primary.mean` |
| 청크 점유율(≥1 사실, 서술) | L0 .950; U-ext@L0size .930; U-ext .998; U-ext+seed@L0+seed-size .922 | `arms.*.chunk_share.mean` |
| 참조: 전체 볼륨 U-ext − L0 gc | +16.5 [10.6, 21.7] (R13 재현) | `reference_full_volume` |
| 볼륨 효과 U-ext@L0size − U-ext, gc | −44.7 [−49.1, −40.7] | `volume_effect` |
읽기: 같은 사실 수에서 CQ 기반 single pass(L0)가 무작위 open-extraction 부분집합보다 훨씬 높음 → U-ext의 +16.5는 사실 볼륨에서 옴. 표집기는 균일 무작위(선별 아님).

## R15 study32 B5·B6 — 같은 인스턴스 재실행 + 코퍼스 유도 seed (사전 등록, `study32_reviewer_checks/b5_b6/results.json`, main이 H1–H6 직접 읽음 2026-11-02)
Qwen 2Wiki Exp8, 30 shard × 2 run seed (60 unit), 실패 0/60 전 arm, 지표 `correct`(answer correctness), shard-cluster BCa B=10,000, Holm 6개. 토큰 main 34.8M + smoke 2.55M = 37.4M (D1 cap 62M). 유도 seed: 코퍼스 300 청크에서 LLM이 22개 관계 이름 유도(정답 미사용), 36k 토큰.
| 항목 | 값 | 키 |
|---|---|---|
| H1 L0+seed − L0 (재실행) | +15.1 [10.5, 19.5], Holm p .0007 → improved | `registered.H1.correct` |
| H2 U-ext+seed − U-ext (재실행) | +3.0 [0.2, 5.6], Holm p .063 → not established | `registered.H2.correct` |
| H3 L0+synseed − L0+seed (양측) | +2.0 [−1.5, 5.3] → did not differ detectably | `registered.H3.correct` |
| H4 U-ext+synseed − U-ext+seed (양측) | −1.3 [−4.4, 1.6] → did not differ detectably | `registered.H4.correct` |
| H5 L0+indseed − L0 (유도 seed) | +16.3 [11.6, 20.2], Holm p .001 → improved | `registered.H5.correct` |
| H6 U-ext+indseed − U-ext (유도 seed) | +3.4 [0.4, 6.7], Holm p .063 → not established | `registered.H6.correct` |
| arm 평균 correct / n_facts | L0 .417/679; L0+seed .568/702; L0+indseed .579/889; U-ext .646/1,698; U-ext+seed .676/1,471; U-ext+indseed .680/1,484 | `arms` (에이전트 보고, REPORT.md) |
| 재실행 − 저장 correct (B5 판독) | L0 −1.7 [−6.2, 1.7]; L0+seed −0.3; U-ext −0.2; U-ext+seed −0.2 (모두 0 포함) | REPORT.md |
| 보조(라벨 없음) indseed − seed | L0 +1.2 [−2.5, 4.2]; U-ext +0.4 [−1.6, 2.2] | REPORT.md |
| post hoc 유도 seed의 정답 관계 일치 | strict 10/23 (증거 가중 62.2%), lenient 13/23 (72.0%); 원 seed 19/23 (98.4%) | `posthoc_gold_match.json` |
읽기: 정답 관계를 보지 않고 코퍼스에서 유도한 seed도 single pass에 +16.3 (원 seed +15.1과 구간 겹침). 재실행 값은 저장 arm과 구간 내 일치 → 앞선 비교는 서버 인스턴스 차이로 설명되지 않음. 주의: arm 평균·보조·post hoc 행은 에이전트 보고에서 옮김(H1–H6만 main 직접 확인).

## R16 study32 B7 — seed 커버리지 용량-반응 (사전 등록, `study32_reviewer_checks/b7_coverage/results.json`, main이 H1·H2·arm 평균 직접 읽음 2026-11-02)
Qwen 2Wiki Exp8, L0 + 원 seed 22개 이름의 중첩 부분집합 6/11/17개(random.Random(20261104)), 30 shard × 2 run seed, 실패 0, 지표 `correct`, BCa B=10,000, Holm 2개. 참조 arm L0·L0+seed = R15 재실행. 토큰 21.3M (cap 30M). 분석 interpreter `-I` 없이 실행(DEVIATIONS; numpy user site).
| 항목 | 값 | 키 |
|---|---|---|
| H1 seed 비율 기울기 (+100%당, x=0/.25/.5/.75/1) | +21.1 [17.0, 25.2], Holm p .0001 → improved | `registered.H1.correct` |
| H2 L0+seed50 − L0 | +10.5 [5.5, 14.5], Holm p .0003 → improved | `registered.H2.correct` |
| arm 평균 correct / n_facts | L0 .417/679; seed25 .325/546; seed50 .522/605; seed75 .550/624; seed100 .568/702 | `arms.*` |
| 보조(라벨 없음) seed25 − L0 / seed75 − L0 | −9.2 [−14.7, −4.9] / +13.3 [8.2, 18.2] | `secondary` (에이전트 보고) |
| 보조 seed75 − seed100 | −1.8 [−5.6, 2.2] | `secondary` (에이전트 보고) |
| gold evidence 가중 커버리지(lenient) | 0 / 27.5 / 57.3 / 86.2 / 98.4 % | `gold_coverage_descriptive` (에이전트 보고) |
읽기: 기울기는 등록 기준 improved, 그러나 단조 아님(seed25가 L0보다 낮음, post hoc 관찰). 중첩 부분집합 1회 추출 → 용량과 포함 이름이 교란.

## R17 study32 B8 — 외부 기준선 iText2KG 1.1.0 (사전 등록, 출력은 모두 descriptive·라벨 없음; `study32_reviewer_checks/b8_external/results.json`, main이 직접 읽음 2026-11-02)
Qwen 2Wiki Exp8 하네스, 60/60 unit, 실패 0, 유실 청크 5/9,002, 기본 설정·청크 단위·seed 없음(스키마 옵션 없음). 토큰 31.8M (cap 35M). DEVIATIONS D1(시간 추정), D2(분석 `-I` 없이).
| 팔 | gc | correct | n_facts | tokens/unit |
|---|---|---|---|---|
| iText2KG | .430 [.393, .470] | .549 [.503, .596] | 1,899 | 478.8k |
| U-ext+seed (저장) | .603 | .678 | 1,472 | 105.9k |
| U-ext+seed (같은 인스턴스 재실행) | .589 | .676 | 1,471 | 105.7k |
| Combined/Ours (저장) | .606 | .655 | 1,435 | 837.7k |
| U-ext (저장) | .558 | .648 | 1,704 | 100.0k |
| L0 (저장) | .394 | .433 | 725 | 131.0k |
| 대비 iText2KG − (gc / correct, 95%) | 값 |
|---|---|
| − U-ext+seed (저장) | −17.3 [−21.0, −13.9] / −12.9 [−16.3, −10.0] |
| − U-ext+seed (재실행) | −15.8 [−19.1, −12.6] / −12.7 [−16.3, −9.6] |
| − Combined (저장) | −17.6 [−20.8, −14.1] / −10.6 [−14.1, −7.5] |
| − U-ext (저장) | −12.8 [−16.5, −8.7] / −9.9 [−13.3, −5.8] |
| − L0 (저장) | +3.7 [−1.5, 9.3] / +11.6 [5.6, 18.2] |
읽기: 이 하네스·기본 설정에서 iText2KG는 사실 1,899개(가장 많음)를 쓰고도 seeded extraction보다 grounded QA 17.3점 낮고, 토큰은 4.5배(파생값—원고 사용 금지, 478.8k vs 105.9k로 표기). PLAN 사전 단서: 문서 단위 시스템을 청크 단위 기본값으로 사용 → "defaults on this harness".

## R18 study32 B10 — T-REx: seed 없는 arm + T-REx 코퍼스 유도 seed (사전 등록, `study32_reviewer_checks/b10_trex_seed/results.json`, main이 직접 읽음 2026-11-02)
Qwen, T-REx holdout 33 shard × seed 20261031 (507문항, 1-hop), 실패 0, 토큰 5.18M (cap 25M). 유도 seed: T-REx 코퍼스 300/386 청크, 22개 이름(2Wiki seed와 정확 일치 4개). gc 1차·correct 2차, 단측, BCa B=10,000, Holm {H1,H2}. 분석 `-I` 없이(D1).
| 항목 | 값 | 키 |
|---|---|---|
| H1 L0+trexseed − L0, gc | +13.3 [8.0, 23.1] → improved (correct +12.5 improved) | `registered_primary_gc.H1.contrast` |
| H2 U-ext+trexseed − U-ext, gc | +0.5 [−2.5, 2.9] → not established | `registered_primary_gc.H2.contrast` |
| arm 평균 gc / correct / n_facts / tokens·unit | L0 .241/.253/111/24.2k; L0+trexseed .374/.378/145/24.4k; U-ext .424/.447/390/22.3k; U-ext+trexseed .428/.449/333/20.3k | `arms` (토큰은 에이전트 보고) |
| 기술(저장 B4 arm, 2Wiki seed) | Combined .371/.373/261/298.1k; U-ext+trexseed − Combined gc +5.8 [0.8, 10.3], correct +7.6 [3.0, 12.6] | `descriptive.Uext_trexseed_minus_Combined_stored` |
읽기: T-REx에서도 코퍼스 유도 seed가 single pass를 +13.3 올림(registered, improved). seed 없는 추출(U-ext)은 이미 높아 seed 이득 미검출. 유도 seed + 넓은 추출이 Combined(2Wiki seed, 298k 토큰)보다 gc +5.8 높음(기술, 저장 arm과 혼합 비교).

## R19 study32 B11 — 같은 사실 수에서 비무작위(휴리스틱) 선택 + 6/22 사후 분석 (사전 등록, `study32_reviewer_checks/b11_selection/results.json`, `results_b7_posthoc.json`, main이 직접 읽음 2026-11-03)
Qwen, 2Wiki 30 shard × 2 seed = 60 unit, 실패 0, LLM 무사용 선택기(S1 entity centrality, S2 relation frequency; S3 LLM ranking은 비용 cap으로 미실행, 동결 전 결정). 저장 U-ext / U-ext+seed 그래프를 L0 / L0+seed와 같은 사실 수로 잘라 동일 QA. gc 1차, 단측, BCa B=10,000, Holm {H1..H4}. 분석 `-I` 없이(D1). 토큰 대장 2.02M (cap 5M, 에이전트 보고).
| 항목 | 값 | 키 |
|---|---|---|
| H1 U-ext@L0크기 S1(centrality) − L0, gc | −14.4 [−19.5, −9.5] → not improved | `registered.H1` |
| H2 U-ext@L0크기 S2(relation freq) − L0, gc | +8.0 [2.7, 13.3] → improved (correct +7.9) | `registered.H2` |
| H3 U-ext+seed@L0+seed크기 S1 − L0+seed, gc | −25.8 [−30.5, −20.5] → not improved (correct −23.2) | `registered.H3` |
| H4 U-ext+seed@L0+seed크기 S2 − L0+seed, gc | −16.6 [−22.1, −11.4] → not improved (correct −13.5) | `registered.H4` |
| 2차(동일 인스턴스 rerun 기준) H1r..H4r | −12.2 / +10.2 / −25.4 / −16.1, 라벨 동일 | `secondary_vs_b5_rerun` |
| arm 평균 gc / correct / n_facts | S1A .250/.319/725; S2A .474/.513/725; S1B .282/.339/687; S2B .375/.435/687; L0 .394/.433/725; L0+seed .541/.571/687 | `arms` |
| 기술: 휴리스틱 − 무작위 부분집합(B9) gc | S1A +13.9 [10.4, 17.9]; S2A +36.3 [30.5, 42.1]; S1B +13.2 [9.4, 15.9]; S2B +22.5 [19.0, 25.7] | `selector_minus_b9_random_descriptive` |
| 사후(6/22, B7 데이터, 무검정) | seed25 − L0: n_facts 679→546; seed 6개 이름에 든 사실 비율 6.5%→51.4% (lenient); distinct relation 33.0→16.0; top relation share .165→.252; correct −9.2 [−14.7, −4.9]; 질문 유형별 correct: bridge-comparison −18.3 [−29.6, −8.8], inference −12.1 [−21.7, −3.8], comparison +2.1 [−6.7, 11.3] | `results_b7_posthoc.json` |
읽기(PLAN reading rule): 휴리스틱에 따라 다름. seed가 있으면 CQ-guided L0+seed가 두 비-CQ 선택 모두보다 같은 사실 수에서 높음(16.6, 25.8점). seed 없이는 relation-frequency 선택이 L0보다 8.0 높음. 무작위 부분집합은 휴리스틱보다 13–36점 낮음. 6/22: 부분 seed가 추출을 6개 관계로 몰아 관계 종류가 절반으로 줄고, bridge-comparison·inference 질문이 떨어짐(사후, 기술).

## R20 study32 B13 — T-REx 두 번째 run seed 반복 (사전 등록, `study32_reviewer_checks/b13_trex_seed2/results.json`, main이 직접 읽음 2026-11-03)
Qwen, T-REx holdout 33 shard × seed 20261105, B10과 코드 동일·유도 seed 동일(해시 일치), 실패 0, non-ok HTTP 0/6160, 토큰 5.08M (cap 12M). gc 1차·correct 2차, 단측, BCa B=10,000, Holm {H1,H2}. 분석 `-I` 없이(사전 기록). D4: pooled 뷰 버그로 분석 코드 수정(등록 절은 영향 없음, 결과 공개 전, 해시 `MANIFEST_analysis_postfix.sha256`).
| 항목 | 값 | 키 |
|---|---|---|
| H1 L0+trexseed − L0, gc (seed 20261105 단독) | +14.1 [9.1, 23.4] → improved (correct +13.5 [8.2, 22.7] improved) | `registered_primary_gc.H1` |
| H2 U-ext+trexseed − U-ext, gc | +0.6 [−2.7, 4.1] → not established (correct −0.3) | `registered_primary_gc.H2` |
| 2-seed pooled (66 unit, descriptive) | H1 gc +13.7 [9.8, 23.9], correct +13.0 [9.0, 23.0]; H2 gc +0.6 [−2.3, 3.1] | `pooled_descriptive.contrasts` |
| arm 평균 gc / correct / n_facts (seed 20261105) | L0 .243/.258/108; L0+trexseed .385/.393/146; U-ext .420/.446/386; U-ext+trexseed .427/.443/330 | `arms` |
읽기: B10의 T-REx seed 효과(+13.3)가 새 run seed에서 +14.1로 재현(registered, improved); 두 seed 합산 +13.7.

## R21 study32 B12 — 두 번째 외부 베이스라인 EDC (clear-nus/edc @02aad17e, Self Canonicalization, 사전 등록·descriptive only, `study32_reviewer_checks/b12_external2/results.json`, main이 직접 읽음 2026-11-03)
60/60 unit (30 shard × seeds 20261031/20261101), failed 0, dropped 0. 토큰 ledger 40.46M (저자 승인 cap 50M, 원래 40M; D-cap50). 엔진 = kgexp-qwen38-pro6000(B8과 동일). 라벨 없음(PLAN §3 descriptive).
| 항목 | 값 (shard-cluster BCa 95%, B=10,000) | 출처 키 |
|---|---|---|
| EDC 평균 gc / correct / n_facts / tok per unit | .445 [.398, .493] / .629 [.583, .676] / 1,357.7 / 618.4k | `arms.EDC` |
| 참조 arm gc / correct / n_facts / tok | U-ext+seed(stored) .603/.678/1,472.3/105.9k; Combined(stored) .606/.655/1,434.8/837.7k; U-ext .558/.648/1,704.5/100.0k; L0 .394/.433/725.2/131.0k | `arms` |
| U-ext+seed − EDC, gc | +15.8 [12.3, 19.3] (correct +4.9 [2.5, 7.7]); EDC가 unit당 5.8배 토큰(618.4k vs 105.9k) | `contrasts_EDC_minus.U-ext+seed-stored` (부호 반전) |
| Combined − EDC, gc | +16.1 [12.4, 20.1] (correct +2.6 [−0.5, 5.9]) | `contrasts_EDC_minus.Ours-stored` |
| U-ext − EDC, gc | +11.4 [7.5, 15.2] (correct +1.9 [−1.8, 5.2]) | `contrasts_EDC_minus.U-ext-stored` |
| EDC − L0, gc | +5.1 [0.5, 10.0] (correct +19.6 [14.8, 24.7]) | `contrasts_EDC_minus.L0-stored` |
| same-instance rerun U-ext+seed(b5b6) − EDC, gc | +14.4 [11.3, 17.6] (correct +4.7 [2.0, 7.7]) | `contrasts_EDC_minus.U-ext+seed-b5b6` |
읽기(descriptive): 스키마를 스스로 유도·정규화하는 EDC는 L0보다 높았지만, 22-name seed를 준 seeded extraction이 grounded QA에서 15.8점 높았고 토큰은 1/5.8. 두 run seed 모두 같은 방향(per_seed −.150/−.167).

## R22 — B17 chunk retrieval vs graph (2Wiki Exp8 units, 60 units / 30 shards, none failed; 2026-11-03)
Source: paper/access2026/harness/study32_reviewer_checks/b17_rag/results_P.json (registered, pro6000 own engine) and results_H.json (replication, H100, W4A16 kernel, descriptive). Labels on shard clusters (n=30, DEVIATIONS D-cluster, set before any main result). RAG-k = top-5 chunks by embedding (k=5 frozen after smoke so the answer-prompt median matches the graph arm: 791 vs 794 tokens); RAG-k+seed = same + the 22-name seed as hint; full-context arm dropped before main (cap, D1). Primary = answer correctness (`correct`); gc for RAG is computed on retrieved text and is not one-to-one comparable.
- Part P arm means (correct): U-ext+seed (fresh) .669; RAG-k .515; RAG-k+seed .500. gc: U-ext+seed .592; RAG gc-on-text .460 / .454. Tokens per unit: U-ext+seed write 105.8k + answer 22.6k; RAG-k answer 14.3k; RAG-k+seed 15.7k.
- H1 U-ext+seed − RAG-k (correct): +15.4 [10.6, 19.8] (shard clusters), Holm p .00024 → improved.
- H2 U-ext+seed − RAG-k+seed (correct): +16.9 [11.1, 22.3] → improved.
- Part H (replication): U-ext+seed .678, RAG-k .508, RAG-k+seed .502; H1 +17.0 [10.6, 22.5], H2 +17.6 [11.0, 23.8].
- Fresh U-ext+seed vs stored (.678 correct, .603 gc): close (descriptive). Interim (24 units) H1 point +17.7 passed the futility rule.

## R23 study32 B19 — T-REx equal-fact-count comparison (사전 등록, `study32_reviewer_checks/b19_volume_trex/results.json`, main이 H1/H2 gc·Holm·라벨 직접 확인 2026-11-03)
Qwen, T-REx holdout 33 shard × run seed 20261031 (507문항, 1-hop), 실패 0, non-ok HTTP 0/2,567, 토큰 0.753M (cap 6M). 저장된 B4 U-ext+seed / B10 U-ext 그래프에서 사실을 균일 무작위(sha256 seeded)로 L0+seed / L0와 같은 개수만큼 추출(33/33 unit 개수 일치) 후 같은 QA 답변기·코드 채점기. 비교 arm = 저장 B4 L0+seed / B10 L0(같은 엔진 인스턴스, 컨테이너 시작 시각 동일). gc 1차, 단측 BCa B=10,000, Holm {H1,H2}. D = single pass − 무작위 부분집합. 40% 중단 규칙(A1 14/33 shard, 점추정 +3.8) 미발동. 분석 `-I` 없이.
| 항목 | 값 | 키 |
|---|---|---|
| H1 L0+seed − U-ext+seed@L0+seed-size, gc | +7.4 [2.9, 12.8] (95%), one-sided lo1 +3.5, Holm p .0010 → improved (correct +6.3 [1.6, 12.0]) | `main.registered.H1` |
| H2 L0 − U-ext@L0size, gc | +6.6 [−5.8, 12.2], lo1 −3.1, Holm p .113 → not established (correct +6.1 [−6.3, 11.4]) | `main.registered.H2` |
| arm 평균 gc / correct / n_facts | L0+seed .290/.294/111; U-ext+seed@L0+seed-size .215/.232/111; U-ext+seed(저장) .421/.439/316; L0 .241/.253/111; U-ext@L0size .174/.192/111; U-ext(저장) .424/.447/390 | `main.arms` |
| 2차 H1r / H2r (같은 인스턴스 rerun 기준) | +7.8 [3.2, 13.1] improved / +7.0 [−5.5, 12.7] not established | `main.secondary_vs_b19_rerun` |
| 2차 H3 (run seed 20261105, L0 − U-ext@L0size) | +5.2 [−6.5, 10.9], p .161 → not established | `rep.registered_secondary_H3` |
| 참조: 전체 볼륨 U-ext+seed − L0+seed / U-ext − L0, gc | +13.1 [9.0, 17.3] / +18.3 [12.6, 27.4] | `main.reference_full_volume` |
| 볼륨 효과 A1 − U-ext+seed / A2 − U-ext, gc | −20.6 [−25.2, −15.9] / −24.9 [−29.6, −20.0] | `main.volume_effect` |
| 청크 점유율(≥1 사실, 서술) | L0+seed .977; A1 .992; L0 .992; A2 .982; 저장 full arm 1.000 | `main.arms.*.chunk_share` |
읽기: 시드가 있을 때 CQ 기반 single pass는 같은 사실 수에서 무작위 부분집합보다 T-REx에서도 높음(+7.4, 2Wiki의 +39.1보다 작은 격차). 시드 없는 arm은 점추정 비슷(+6.6)하나 구간이 0 포함(not established), 두 번째 run seed도 동일(+5.2). U-ext의 full-volume 이점(+13~18)은 L0 크기로 자르면 사라짐 → 볼륨 효과. 한계: 균일 무작위 부분집합(선별 아님), 1-hop 단일 관계 질문, seed = 2Wiki 관계 목록, 단일 모델 계열, run seed 1개(주 family).

## R24 study32 B15 — 세 번째 외부 베이스라인 AutoSchemaKG (atlas-rag 0.0.5.post1, released defaults, 사전 등록·descriptive only, `study32_reviewer_checks/b15_external3/exp/results.json`, main이 직접 읽음 2026-11-04)
Qwen, 2Wiki Exp8 단위 중 run seed 20261031의 30 shard(D1: 두 번째 seed 제외, 대체 없음), 실패 셀 0, 토큰 51.35M(cap 60M, D2/D3). 같은 청크·같은 KG-only 답변기·코드 채점기. 비교 arm = 저장 Exp8 arm(다른 엔진 인스턴스). 중단 규칙(24/30 시점 U-ext+seed − AutoSchemaKG gc 점추정 +0.518 > 0) 미발동. 독립 감사(sonnet, read-only): GENUINE — provenance·매핑 결함 없음; primary arm은 공유 60-fact 검색 상한에 has_concept·이벤트 edge가 차서(문맥 99% 잘림) 불리 → 비교 가능 arm은 ER. cov_primary가 L0과 같은 .6299는 우연(합 302.35 동일, 문항별 불일치).
| 항목 | 값 | 키 |
|---|---|---|
| AutoSchemaKG-ER (엔티티-관계 triple만) gc / correct / n_facts | .2125 [.175, .252] / .446 [.396, .490] / 1,256.6 | `arms.AutoSchemaKG-ER` |
| AutoSchemaKG (전체 edge) gc / correct / n_facts | .096 [.073, .121] / .233 [.200, .260] / 18,360 | `arms.AutoSchemaKG` |
| 토큰/단위 (두 변형 공통 추출) | 1,557.8k (참조: U-ext+seed 105.9k, Ours 836.9k) | `tokens_per_unit` |
| ER − U-ext+seed(저장), gc / correct | −39.2 [−44.0, −34.4] / −23.3 [−27.5, −20.0] | `contrasts_new_minus_ref.AutoSchemaKG-ER.U-ext+seed-stored` |
| ER − Ours(저장), gc / correct | −41.9 [−46.3, −38.3] / −23.1 [−27.3, −19.0] | `…AutoSchemaKG-ER.Ours-stored` |
| ER − U-ext(저장), gc / correct | −34.6 [−38.5, −30.8] / −20.2 [−23.8, −16.7] | `…AutoSchemaKG-ER.U-ext-stored` |
| ER − L0(저장), gc / correct | −19.2 [−26.0, −13.1] / +2.1 [−5.0, 9.4] | `…AutoSchemaKG-ER.L0-stored` |
| 전체 − U-ext+seed(저장), gc / correct | −50.8 [−54.8, −46.9] / −44.6 [−49.0, −40.6] | `…AutoSchemaKG.U-ext+seed-stored` |
| 30 shard 위 저장 arm 평균 gc / correct | U-ext+seed .604/.679; Ours .631/.677; U-ext .558/.648; L0 .404/.425 | `arms.*-stored` |
읽기: released-default AutoSchemaKG는 엔티티-관계 triple만 써도 seeded extraction보다 gc 39.2점 낮고 토큰은 1,557.8k vs 105.9k. 한계: seed 1개 30 shard, 저장 arm은 다른 인스턴스, 추출 T 0.7(패키지 기본)·thinking off, 공유 60-fact 검색 상한.

## R25 study32 B20 — class-free gc 재분석 (사후, LLM 호출 0, 저장 예측·상태만; `study32_reviewer_checks/b20_classfree/results.json`; main이 s27_score.py:14-35,74-85와 results.json diag·contrasts 직접 확인 2026-11-04)
리뷰어 비판("gc는 관계 CLASS가 맞는 gold 근거 사실이 검색돼야 grounded → 시드 arm 구조적 유리")의 전제 점검. 코드 확인: gc = correct AND grounded(`s27_score.primary_item`); 선택형(comparison, bridge_comparison) grounded = 모든 gold 근거가 `ev_hits`로 hit(주어·목적어 쌍 일치 + 인용 청크에 근거 포함, 관계 무관; 일반 술어만 제외), 개방형(compositional, inference) grounded = gold 답 문자열이 검색 사실의 주어/목적어에 있음. 관계 CLASS(`pred_class`/`REL_CLASS`)는 `cov_primary`에만 쓰임. 저장 예측의 `qa.retrieved`(60-fact 상한)로 재계산, 검색 재실행 없음. shard-cluster BCa 95% B=10,000. 단위 = 점(pp).

| 항목 | 값 | 키 |
|---|---|---|
| 재현(sanity) gc / correct | 12개 arm 전부 저장값과 소수 셋째 자리 일치(U-ext .558, U-ext+seed .603, Ours .606, L0 .394, EDC .445, iText2KG .430, AutoSchemaKG-ER .2125, AutoSchemaKG .096 등); L0+seed − L0 gc +14.7 | `arms.*` |
| gc_free − gc 불일치 문항 | 0 (12개 arm 모두; 일반 술어 제외도 제거한 상태) | `arms.*.n_unit_questions_mismatch_free_vs_gc` |
| gc_class(관계 CLASS 필수, 구성 변형) − gc | 전 arm −0.0~−1.2 pp (Ours 0, U-ext+seed −.4, iText2KG −.9, EDC −.4, ER −.8, AutoSchemaKG −1.25) | `arms.*.gc_class` |
| U-ext+seed − iText2KG gc / gc_free / gc_class | +17.3 [13.6, 20.8] / +17.3 / +17.8 | `contrasts."U-ext+seed - iText2KG"` |
| U-ext+seed − EDC gc / gc_free / gc_class | +15.8 [12.1, 19.1] / +15.8 / +15.8 | `contrasts."U-ext+seed - EDC"` |
| U-ext+seed − AutoSchemaKG-ER gc / gc_class (30 shard) | +39.2 [34.0, 43.8] / +39.6 | `contrasts."U-ext+seed - AutoSchemaKG-ER"` |
| U-ext+seed − AutoSchemaKG gc / gc_class (30 shard) | +50.8 [46.7, 54.4] / +51.7 | `contrasts."U-ext+seed - AutoSchemaKG"` |
| Ours − iText2KG / EDC / ER / AutoSchemaKG gc (= gc_free) | +17.6 [13.9, 20.6] / +16.1 [12.2, 19.8] / +41.9 [37.9, 45.6] / +53.5 [49.4, 57.5] | `contrasts."Ours - *"` |
| 선택형 gold 근거 중 검색에 쌍+청크 hit가 있는 비율 | seed arm 88–90% (U-ext+seed 88.5, Ours 90.0) vs EDC 75.6, iText2KG 81.0, ER 57.7, AutoSchemaKG 48.9 | `diag.*` |
| 그 hit 근거 중 술어 CLASS가 gold와 일치 | seed 99.2–99.3%, EDC 98.6, iText2KG 97.4, ER 95.1, AutoSchemaKG 90.3; 전부 미분류(None=other/unknown) 0.6–1.5% (seed/EDC/iText2KG), ER 4.7, AutoSchemaKG 9.4 | `diag.*.share_*` |
| 검색 60-fact 문맥 중 CLASS None 비율 | U-ext+seed 30.2, Ours 16.4, EDC 34.4, iText2KG 50.6, ER 59.9, AutoSchemaKG 91.3 | `diag.*.share_retrieved_class_none` |
한계: 진단은 선택형만(개방형 gc는 관계 기준이 없음); gc_class는 새로 만든 가상 지표(저장값 아님); AutoSchemaKG는 30 shard·seed 1개(b15 D1); 저장 arm은 다른 엔진 인스턴스·같은 모델 계열; cov_primary/cov_agnostic은 재계산하지 않음. 해석: 외부 추출기와의 gc 격차는 CLASS 매핑이 아니라 검색에 근거 쌍이 오르는 비율 차이로 설명되며, CLASS를 요구하면 격차는 같거나 최대 1.2pp 커진다.
주의: 원고의 기존 대비 구간(R21 등)은 원래 분석값을 유지(이 재분석의 BCa 구간은 재표집 seed 차이로 ±0.2 다를 수 있음). 원고에서 쓸 값: gc_class 변화 ≤1.2점, 근거 쌍 검색 도달률 U-ext+seed 88.5% / Ours 90.0% / iText2KG 81.0% / EDC 75.6% / ER 57.7%.

## R26 study32 B22 — 2Wiki 모델 자체 지식 기준선 (descriptive arm CBown, `study32_reviewer_checks/b22_closedbook/results.json` `corpora.wiki`, main이 직접 읽음 2026-11-04)
Qwen, 2Wiki Exp8 60 units(30 shard 군집), 같은 QA 답변기 모델·디코딩, 사실 문맥 없이 study27 own-knowledge 프롬프트로 답함, 코드 채점 answer correctness. 실패 0. 등록 arm(사실만 쓰라는 프롬프트, 빈 문맥)은 전부 "unknown"→0점이라 기계적이므로 원고에 쓰지 않음. T-REx 부분은 원고·LEDGER 미사용(저자 규칙, 실험노트만).
| 항목 | 값 | 키 |
|---|---|---|
| 자체 지식 answer correctness | .325 [.294, .354] (기권 44.4%) | `arm_means.CBown` |
| U-ext+seed − 자체 지식 | +35.3 [30.1, 40.1] | `descriptive_stored_minus_CBown.U-ext+seed` |
| Ours(결합) − 자체 지식 | +33.0 [28.4, 37.8] | `….Ours` |
| U-ext − 자체 지식 | +32.3 [27.3, 38.1] | `….U-ext` |
| L0+seed − 자체 지식 | +24.6 [19.6, 29.7] | `….L0+seed` |
| L0 − 자체 지식 | +10.8 [4.6, 16.8] | `….L0` |

## R27 study32 B25 — 사후 재분석 5건 (LLM 호출 0, 저장 상태·예측만; `study32_reviewer_checks/b25_reanalysis/results_task{12,2,3}.json`; main이 results.json task2 arms·contrasts 직접 확인 2026-11-04)
(1) 엔티티 링킹 민감도: QA 검색(`s27_kg.retrieve`)의 정확 n-gram 링커를 저장 그래프 위에서 완화 링커로 재계산(정답 재생성 없음, 답과 무관한 진단만). 완화 = 토큰집합 동일 / difflib 비율 ≥ .9(숫자·로마숫자 토큰 일치 필수) / 포함(상한). shard-cluster BCa 95%, B=10,000, 60 유닛(AutoSchemaKG 30).

| 항목 | 값 | 키 |
|---|---|---|
| 재현(sanity) | 정확 링커가 저장 `qa.retrieved` 목록을 960/960(U-ext+seed, Ours, L0)·958(U-ext)·959(iText2KG, EDC)·480/480(AutoSchemaKG, -ER) 재현; 풀링 reach가 b20 diag와 일치(88.5/90.0/75.6/81.0/57.7/48.9) | `repro`, `pooled.*.exact` |
| 근거 도달률(choice gold 근거 중 쌍+청크 hit) 정확 → fuzzy .9 | U-ext+seed 88.5→88.5, Ours 90.1→90.2, U-ext 86.0→86.1, L0 65.7→65.7, iText2KG 80.9→80.9, EDC 75.6→75.9, ER 57.8→57.9, AutoSchemaKG 49.0→48.5 | `arms.*.ev_reach__{exact,fuzzy}` |
| fuzzy−정확 reach / choice grounded | reach +0.1(전 arm; EDC +0.3 [0.1, 0.7]만 0 제외); grounded 0.0~+0.4(iText2KG −0.4) | `arms.*.*__fuzzy-exact` |
| 포함 링커(상한) − 정확 reach | 전 arm −2.0~−4.3 (씨드 arm −3.5~−4.3, 외부 −2.0~−3.2): 시드 추가가 60 사실 상한에서 관련 사실을 밀어냄 | `*__contain-exact` |
| U-ext+seed − 외부 reach, 정확 / fuzzy | iText2KG +7.6 [5.2, 10.1] / +7.6; EDC +12.8 [9.7, 16.6] / +12.6; ER +30.8 / +30.8; AutoSchemaKG +39.6 / +40.2 | `contrasts."U-ext+seed - *"` |
| 같은 격차, choice grounded | iText2KG +17.3 / +17.7; EDC +25.6 / +25.2; ER +57.9 / +57.9 | 동일 |
| 열린 질문 답 문자열이 검색 사실에 있는 비율 fuzzy−정확 | −0.4~+1.2 (EDC +1.2 [−0.6, 3.3]) | `arms.*.open_ans_present__fuzzy-exact` |
해석: 링크율 98~100%이고 완화 링커는 어느 arm도 0.4pp 넘게 움직이지 않아 외부 추출기 격차를 설명하지 못한다. 한계: 답 재생성 없음(링커가 LLM 답에 미치는 영향은 미측정), 임계값 .9 한 값, 공통 토큰 없는 다중 토큰 오타 변형은 미검사, 저장 arm은 다른 엔진 인스턴스.

(2) U-ext+seed − Ours(2Wiki Exp8, 60 유닛): gc −0.3 [−3.9, 2.8](반대 방향 Ours − U-ext+seed +0.3 [−3.0, 3.6]; 논문 +0.3 [−3.1, 3.5]와 BCa 방향·재표본 차이만큼 다름); answer correct +2.3 [−0.2, 4.4](Ours − U-ext+seed −2.3 [−4.6, 0.0]). 평균 gc .603 / .606, correct .678 / .655. `results_task2.json contrasts`.

(3) 시드 비율 표(L0 answer correct, 60 유닛): K=0 .417 [.366, .474]; 6 .325 [.274, .383] (−9.2 [−14.7, −4.9]); 11 .522 [.481, .554] (+10.5 [5.5, 14.5]); 17 .550 [.500, .592] (+13.3 [8.2, 18.2]); 22 .568 [.521, .613] (+15.1 [10.5, 19.5]); 22 induced .579 [.533, .620] (+16.3 [11.6, 20.2]). 출처: K=0, 22, induced = b5_b6 재실행 인스턴스(컨테이너 시작 2026-10-29T04:51Z), K=6/11/17 = b7_coverage(같은 인스턴스, S7 통과; 인스턴스 동일성은 컨테이너 가동 시각으로 추정). 저장 Exp7(다른 인스턴스) L0 .433 / L0+seed .571, 차이 +13.8 [10.5, 17.2]. 재계산 평균은 b7 results.json과 소수 5자리 일치. `results_task3.json`.

(4) Gemma "combined +9.3 [5.7, 12.9]": Gemma 값이 맞다(복사 아님). `replic_gemma/analysis/gemma_repair_main.json descriptive["Ours - Ours-seed (seed)"].gc` = +.0927 [.0573, .1292], 30 shard·60 유닛, Ours·Ours-seed 각 7/60 셀 실패(ITT). Qwen은 `study27_ours_final/results.json` 같은 키 +.0927 [.0604, .1208]: 점추정만 우연히 같고(둘 다 89/960) 구간·시드별 값이 다르다. 수리 전 gemma_main.json은 +6.8 [2.0, 9.9]. 

(5) Exp1: .257 = A1(진단 반복, K=5), .362 = A2s(비적응 일괄 생성, 같은 CQ 수, 탐색적 arm), A0 = .043, A2 .181, A3 .248. +21.4 [16.2, 27.1] = C1 = A1 − A0(반복 없음 대비; 구성상 양수), 단일 일괄과의 대비가 아니다. A1 − A2s = −10.5 [−19.5, −1.4](탐색적). 부록 문장이 두 비교를 섞는다. `study19_e1_cq_closed_loop/results.json arm_table, contrasts C1/C6`.
원고 사용 규칙: 기존 원고 구간(+0.3 [−3.1, 3.5] 등)은 유지; 새로 쓸 수 있는 값 = 링커 완화 시 reach 변화 ≤0.3점, U-ext+seed − Ours answer correctness +2.3 [−0.2, 4.4], Table 4 구간(task3), Exp1 arm 정체(.257 반복 A1, .362 단일 배치 A2s, +21.4 = A1 − A0).

## R28 study32 B23 — T-REx seed induced only outside the evaluation shards (사전 등록, `study32_reviewer_checks/b23_inductive_seed/results.json`, main이 results.json registered_primary_gc.H1·arms 직접 확인 2026-11-04)
Qwen(H100 엔진), T-REx main 33 shard x run seed 20261031 (507문항), 실패 0 (33/33 unit x 2 arm), 토큰 2.523M (cap 15M; main 2.395M, smoke 0.128M, 유도 0.024M). 시드 = b10 유도 코드 그대로, 풀만 main에 없는 도메인 dev 96 청크(7 배치; b10은 300 청크/20 배치), 이름 22개, 풀-main 겹침 0(id/text/title), 문항 미열람. 비교 arm = 저장 b10 L0 / U-ext (pro6000 엔진; 엔진 인스턴스 혼재). gc 1차, 단측 BCa B=10,000, Holm {H1,H2}. 40% 중단 규칙(14/33 shard, 점추정 +7.6) 미발동. 분석 `-I` 없이.
| 항목 | 값 | 키 |
|---|---|---|
| 시드(22) | author, award, based on, birth date, cast member, cause of death, child, creator, death date, developer, director, genre, influenced by, instance of, language, location, member of, nationality, occupation, publication date, publisher, spouse | `induced_seed.names` |
| 이름 겹침 | transductive T-REx 시드와 15/22 (Jaccard .517); 2Wiki 시드와 6/22 (cause of death, child, director, occupation, publication date, spouse; Jaccard .158) | `induced_seed.exact_overlap_*` |
| H1 L0+indseed − L0, gc | +7.4 [3.9, 11.4], lo1 +4.4, Holm p .0001, cov_agnostic +15.3 → improved (correct +6.8 [3.0, 10.9], p .0004) | `registered_primary_gc.H1` |
| H2 U-ext+indseed − U-ext, gc | −2.4 [−5.2, +0.4], lo1 −4.8, hi1 −0.09, Holm p .956 → not improved (correct −1.8 [−4.7, +1.1], not established) | `registered_primary_gc.H2` |
| arm 평균 gc / correct / n_facts | L0 .241/.253/111; L0+indseed .315/.321/149; L0+trexseed(전이) .374/.378/145; U-ext .424/.447/390; U-ext+indseed .399/.429/328; U-ext+trexseed .428/.449/333 | `arms` |
| 서술: indseed − 전이 시드 | L0 gc −5.9 [−16.6, −1.5]; U-ext gc −2.9 [−5.5, −0.5]; 전이 L0 효과 +13.3 대비 약 56% | `descriptive` |
읽기: main shard 밖 문서로만 유도한 시드도 L0 single pass를 올린다(b10과 같은 패턴: L0 개선, U-ext 개선 없음). 전이 시드 대비 이득은 작다(풀이 작아 효과 감소가 풀 크기 때문인지 전이성 때문인지는 이 설계로 분리 불가). 한계: 유도 1회, 풀 96청크, dev는 같은 T-REx 도메인(shard 밖이나 도메인 밖 아님), 기준 arm은 다른 엔진 인스턴스(pro6000), 질문문이 관계명을 포함해 gc와 coverage가 가까움, run seed 1개, 동일 모델 계열 생성·답변·판정.
원고 사용 규칙: H1(+7.4 [3.9, 11.4], Holm p .0001, improved)과 시드 출처(평가 shard 밖 dev 청크 96개에서 유도, 질문 미열람, transductive T-REx 시드와 15/22, 2Wiki 시드와 6/22 이름 일치)를 쓴다. H2는 기존 R18과 같은 패턴(U-ext는 시드로 이득 없음)이라 한 구절로만; 전이 시드 대비 비율(56%) 같은 파생 수치는 쓰지 않는다.

## R29 study32 B24 — equal-fact-count check vs strong question-agnostic selectors (사전 등록, `study32_reviewer_checks/b24_selector/results.json`, main이 results.json registered.H1·H2·arms 직접 확인 2026-11-04)
2WikiMultihopQA 30 shard x run seed 20261031/20261101 = 60 unit, 실패 0, 토큰 3.04M (cap 25M). 저장 U-ext+seed 그래프에서 L0+seed와 같은 사실 수(60/60 일치)를 (SCH) 2-hop 경로 수 최대화 greedy(LLM 없음), (SLM) Qwen 0-9 정보성 점수 상위로 선택 후 같은 QA 답변기·코드 채점기. gc 1차, 단측 BCa B=10,000, Holm {H1,H2}. 40% 중단 look(24 unit) +26.8 통과. 중간에 로컬 재부팅으로 일시중지 후 재개(D2, 결과 미열람).
| 항목 | 값 | 키 |
|---|---|---|
| H1 L0+seed − SCH, gc | +25.0 [19.8, 30.1], lo1 +20.5, Holm p .0002 → improved | `registered.H1` |
| H2 L0+seed − SLM, gc | +14.3 [8.9, 19.3], lo1 +9.8, Holm p .0002 → improved | `registered.H2` |
| arm 평균 gc/correct/n_facts | L0+seed .541/.571/687; SCH .291/.340/687; SLM .398/.450/687; U-ext+seed .603/.678/1472 | `arms` |
| SCH − SLM, gc (기술) | −10.7 [−15.8, −5.6] | `SCH_minus_SLM_descriptive` |
| 참조: b9 무작위 / b11 S1 / S2 gc | .150 / .282 / .375 (L0+seed 대비 +39.1 / +25.8 / +16.6) | `L0plusseed_minus_comparators_descriptive` |
한계: 구체적 선택기 2종(최선 아님), SCH는 허브 쏠림, SLM은 같은 Qwen 계열·청크 내 맥락만·점수 7-8 쏠림, 두 seed 독립 아님, 비교 저장 예측은 다른 서버 창, SPARQL/CQ-40 지표 없음.
원고 사용 규칙: H1·H2(+25.0, +14.3, 둘 다 improved)를 쓴다. 한계 문장(선택기 2종, SLM 같은 계열)은 원고에 한계 절로 넣지 않고 선택기 정의 서술(질문·gold·CQ 미열람, 같은 사실 수)로만 반영. SCH − SLM 같은 선택기 간 비교와 파생값은 쓰지 않는다.

## R30 study32 B28 — CQ-guided selection and chunk-balanced selection at equal fact count (pre-registered, `study32_reviewer_checks/b28_cq_selection/results.json`, main이 results.json registered.H1·H2·arms 직접 확인 2026-11-04)
Qwen3.8-Flash-Next on the H100 engine, 2Wiki 30 shards x seeds 20261031/20261101 (60 units, 16 held-out questions each), 0 failed cells, 0.883M tokens (cap 5M). Stored U-ext+seed graph subsampled to L0+seed's fact count (60/60 equal) by S-cq (BM25 vs the unit's own 40 stored CQs, max over CQs) or S-bal (chunk round-robin); same QA answerer and code scorer. Comparison arm = stored L0+seed (pro6000 engine). gc primary, one-sided shard-cluster BCa B=10,000, Holm {H1,H2}.
| item | value | key |
|---|---|---|
| H1 L0+seed − S-cq, gc | +33.3 [28.3, 37.7], lo1 +29.2, Holm p .0004 -> improved (correct +30.2 [25.0, 35.3]) | `registered.H1` |
| H2 L0+seed − S-bal, gc | +37.2 [31.6, 41.4], lo1 +32.5, Holm p .0005 -> improved (correct +30.5 [24.8, 35.4]) | `registered.H2` |
| arm gc | L0+seed .541; S-cq .207; S-bal .169; full U-ext+seed .603; b9 random .150 | `arms` |
| S-cq − S-bal (descr.) | gc +3.9 [0.7, 6.8], correct +0.3 [-2.1, 2.8] | `SCQ_minus_SBAL_descriptive` |
Caveat: engine differs between selector arms (H100) and stored L0+seed (pro6000); S-cq is one lexical selector. Futility look at 24 units passed (+38.0).
원고 사용 규칙: H1·H2(CQ 기반 추출 − CQ 선택 +33.3 [28.3, 37.7], − 청크 균형 선택 +37.2 [31.6, 41.4], 둘 다 registered improved)와 선택기 정의를 쓴다. 엔진 차이(저장 L0+seed = pro6000, 선택기 arm = H100)는 설계 서술에 한 문장으로 사실대로 적는다(한계 절 아님). S-cq vs S-bal 등 선택기 간 비교, 파생 수치는 쓰지 않는다.

## R31 study32 B21 — public extractor with the same 22-name relation seed (사전 등록, `study32_reviewer_checks/b21_seeded_externals/results.json`, main이 results.json registered.H1·H2·arms 직접 확인 2026-11-04)
2WikiMultihopQA 30 shard x run seed 20261031 = 30 unit, 실패 0(손실 청크 1/4,501), 토큰 31.8M(cap 해제). EDC(Target Alignment, 목표 스키마 = 시드 관계명 22개, 정의 = 이름 그대로)를 같은 청크·엔진·답변기·채점기로 실행. gc 1차, 단측 BCa B=10,000, Holm {H1,H2}. 12 unit look +0.031 통과. 12 unit 이후 로컬 GPU 요청으로 서빙 인스턴스 교체(units 0-11 / 12-29 서로 다른 인스턴스), 저장 참조(EDC b12, U-ext+seed 등)는 다른 인스턴스.
| 항목 | 값 | 키 |
|---|---|---|
| H1 EDC+seed − EDC, gc | +0.4 [−2.7, +2.9]pt, lo1 −2.3, Holm p .468 → not established | `registered.H1` |
| H2 U-ext+seed − EDC+seed, gc | +14.6 [10.4, 18.5], lo1 +11.0, Holm p .0003 → improved (correct +6.7 [2.9, 10.4]) | `registered.H2` |
| arm 평균 gc/correct/n_facts | EDC+seed .458/.613/824; EDC .454/.633/1356; U-ext+seed .604/.679/1470; Ours .631/.677/1420; U-ext .558/.648/1705; L0 .404/.425/689 | `arms` |
| 추출 진단 | OIE 41,080 중 정렬로 39% 폐기, 유지 25,017; 청크당 9.4 호출 | `extraction` |
한계: 시드가 EDC에서는 최종 정규화에만 쓰임(OIE 힌트 없음, 미정렬 삼중항 폐기), 정의는 관계명뿐(D0), 서버 인스턴스 교체 및 저장 참조는 다른 인스턴스, 같은 Qwen 계열, run seed 1개, iText2KG는 시드 주입 불가(미해결).
원고 사용 규칙: H1(EDC에 같은 22개 관계 목록을 target schema로 줌: +0.4 [−2.7, 2.9] gc, registered not established)과 H2(U-ext+seed − EDC+list +14.6 [10.4, 18.5] gc, registered improved, Holm p .0003), arm 평균(EDC+list .458/.613, EDC .454/.633, 사실 수 824 vs 1,356, 토큰/unit 791k)을 쓴다. 서버 인스턴스가 0–11 단위 이후 바뀐 사실과 저장 참조 arm이 다른 인스턴스라는 사실은 설계 서술 한 문장으로 적는다. 이름만 target definition으로 준 점(EDC 설정)을 서술에 사실대로 포함. 파생 수치 금지.

## R32 study32 B29 - hybrid QA with fact cap 60 (사전 등록, `study32_reviewer_checks/b29_hybrid60/results.json`, main이 results.json registered.H1·H2·arms 직접 확인 2026-11-06)
2Wiki Exp8 저장 그래프, 30 shard x 2 seed (60 unit, 480문항), 5 arm 전부 완료, 실패 0, 토큰 4.97M. B3 hybrid 코드에서 그래프 사실 상한만 30 -> 60 (H_FACTS 한 줄), H100 엔진. 1차 correct, 단측 BCa B=10,000, Holm {H1,H2}. **주의(D4)**: 중단 후 H100 컨테이너를 autotune 비활성으로 재생성; L0+seed 후반부와 L0는 새 인스턴스, 나머지는 옛 인스턴스(결과 열람 전 기록).
| 항목 | 값 | 키 |
|---|---|---|
| H1 U-ext+seed hybrid60 - hybrid30 | +12.4 [9.3, 15.3], lo1 +9.8, Holm p .0002 -> improved | `registered.H1` |
| H2 Combined hybrid60 - hybrid30 | +9.6 [7.2, 11.7], lo1 +7.6, Holm p .0002 -> improved | `registered.H2` |
| arm 평균 hybrid60 / hybrid30 | LOOP+seed .725/.671; L0+seed .716/.692; U-ext+seed .709/.585; Combined .699/.603; L0 .626/.600 (V .502) | `arms` |
| 쌍별(hybrid60, 기술) | Combined - LOOP -2.6 [-5.6, -0.4]; Combined - L0+seed -1.7 [-5.3, 0.9]; U-ext+seed - L0+seed -0.6 [-4.5, 2.6]; U-ext+seed - Combined +1.0 [-1.1, 3.2]; L0 대비 모든 arm +7.3 ~ +9.9 | `pairwise_H60` |
| 엔진 대조(동일 프롬프트 부분집합, H60-H30) | Combined +0.6, U-ext+seed +0.8, LOOP +0.4, L0+seed -0.2, L0 +0.6 (모두 0 포함) | `arms.*.identical_prompt_subset` |
| 상한 30 도달 문항 비율 | Combined 64%, U-ext+seed 70%, LOOP 39%, L0+seed 19%, L0 18% | `arms.*.share_questions_cap30_binding` |
읽기: 상한 30이 사실이 많은 그래프를 불리하게 했다(hybrid30 순위 L0+seed > LOOP > Combined > L0 > U-ext -> hybrid60에서는 LOOP/L0+seed/U-ext/Combined가 2.6점 이내, L0만 7~10점 아래). 한계: 저장 hybrid30은 pro6000, hybrid60은 H100 두 인스턴스(D4), 단일 답변기 계열, 쌍별 다중비교 보정 없음.
원고 사용 규칙: 하이브리드 QA(그래프 사실 상한 60, 5 arm 전부) 평균 LOOP+seed .725, L0+seed .716, U-ext+seed .709, Combined .699, L0 .626 (저장 상한 30: .671/.692/.585/.603/.600; 벡터 전용 .502)와 등록 H1(U-ext+seed 상한 60−30 +12.4 [9.3, 15.3], improved)·H2(Combined +9.6 [7.2, 11.7], improved)를 쓴다. 상한 30 순서 역전이 사실 상한 영향이라는 서술은 이 수치로만(해석 단정 금지). 서버 인스턴스 변경과 autotune 해제는 설계 서술에 한 문장. 파생 수치 금지.

## R33 study32 B27 — 2Wiki list induced only outside the evaluation shards (사전 등록, `study32_reviewer_checks/b27_2wiki_outside_list/results.json`, main이 results.json registered.H1·H2·arms 직접 확인 2026-11-06)
Qwen(H100 엔진), 2Wiki main 30 shard x run seed 20261031 (480문항), 실패 0 (30/30 unit x 2 arm), 토큰 7.981M (main 7.448M, smoke 0.533M, 유도 0.040M; cap 8M은 D4에서 1e9로 해제, 8M 미도달). 목록 = b5_b6 유도 코드 그대로, 풀만 main shard에 없는 비-main 2Wiki 청크 6,136개(id 0 / text 3,519 / title 37 / 중복 329 제거)에서 300 청크 표본, 이름 22개, 풀·표본-main 겹침 0, 문항 미열람. 비교 arm = 저장 b5_b6 L0 / U-ext (pro6000 엔진; 엔진 인스턴스 혼재). gc 1차, 단측 BCa B=10,000, Holm {H1,H2}. 40% 중단 규칙(12/30 shard, 점추정 +0.2135) 미발동. 중간 일시중지·H100 컨테이너 재생성(autotune off, 새 서빙 인스턴스)은 DEVIATIONS D4와 PLAN caveat (x)에 사전 기재.
| 항목 | 값 | 키 |
|---|---|---|
| 목록(22) | based on, birth date, birth place, cast member, child, death date, death place, director, employer, genre, location, member of, nationality, occupation, parent, producer, publication date, release year, sibling, spouse, title, writer | `induced_seed.names` |
| 이름 겹침 | 전이 목록과 18/22 (Jaccard .692; 새 목록에만 location, producer, writer); 원 훈련 split 목록과 5/22 (child, director, occupation, publication date, spouse; Jaccard .128) | `induced_seed.exact_overlap_*` |
| H1 L0+outlist − L0, gc | +15.8 [9.6, 21.9], lo1 +10.4, Holm p .00024, cov_agnostic +11.9 → improved (correct +14.4 [8.1, 20.6], p .00016) | `registered_primary_gc.H1` |
| H2 U-ext+outlist − U-ext, gc | +3.1 [0.0, 6.5], lo1 +0.6, Holm p .026, cov_agnostic +0.5 → improved(경계) (correct +1.7 [−1.0, +4.2], p .148, not established) | `registered_primary_gc.H2` |
| arm 평균 gc / correct / n_facts | L0 .383/.429/672; L0+전이 .531/.575/919; L0+outlist .542/.573/846; U-ext .558/.642/1,698; U-ext+전이 .606/.681/1,484; U-ext+outlist .590/.658/1,492 | `arms` |
| 서술: outlist − 전이 목록 | L0 gc +1.0 [−4.0, +5.8]; U-ext gc −1.7 [−4.4, +0.6], correct −2.3 [−4.4, −0.6]; 전이 효과 L0 +14.8, U-ext +4.8 대비 L0 약 107%, U-ext 약 65%(점추정) | `descriptive` |
읽기: main shard 밖 문서로만 유도한 목록도 single pass의 gc를 올린다(L0 큼, U-ext 작고 경계). L0 효과는 전이 목록과 같은 크기라 평가 shard 텍스트 접근이 필요하지 않다. U-ext의 +3.1은 엔진 인스턴스 차이(논문 내 재실행 최대 약 1.6점)와 같은 자릿수이고 correct·cov_agnostic은 확립되지 않았다. 한계: 유도 1회, 풀은 shard 밖이나 corpus 밖 아님(같은 2Wiki 도메인), 기준 arm은 다른 엔진 인스턴스(pro6000), phase A/B가 서로 다른 H100 인스턴스, 질문문이 관계명을 포함해 gc와 coverage가 가까움, run seed 1개(원 b5_b6는 2개), 동일 모델 계열 생성·답변·판정, 인간 검증 없음. AI 생성 초안; 저자 검토·재현 전 사용 금지.
원고 사용 규칙: 2Wiki 평가 shard 밖 청크(풀 6,136, 표본 300)에서 질문 없이 유도한 목록(22개; transductive 목록과 18/22, 훈련 split 목록과 5/22 이름 일치): 단일 패스 H1 +15.8 [9.6, 21.9] gc, registered improved(Holm p .0002); 전체 추출 H2 +3.1 [0.0, 6.5] improved이나 경계선(correct +1.7 [−1.0, 4.2] not established) — 원고에는 H1과 목록 출처를 쓰고 H2는 구간 그대로 한 구절로만(과장 금지). 서버 인스턴스 변경(0–11 단위 이후, autotune 해제)은 설계 서술 한 문장. 서술 비교(외부 − transductive 목록)·파생 비율(약 65%)은 쓰지 않는다.
