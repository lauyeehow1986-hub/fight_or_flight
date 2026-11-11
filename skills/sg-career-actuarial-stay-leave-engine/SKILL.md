---
name: sg-career-actuarial-stay-leave-engine
description: Actuarial, continuous-time semi-Markov (CTMC), and Hawkes jump-diffusion quantitative life-path simulation engine for Singapore residents. Triangulates MOM occupational wages (SSOC), live MyCareersFuture v2 FCF salary ranges, SingStat TableBuilder (M182171, 18035 HES), Adzuna SG histograms, and multi-portal benchmarks (JobStreet, eFinancialCareers, Glints, NodeFlair). Simulates 10/20/30-year stay-vs-leave trajectories under 1 Jan 2026 CPF statutory rules (S$8,000 monthly OW ceiling, S$102,000 annual ceiling), IRAS YA2026 personal income and AV property taxes, 9% GST, and 12 Hawkes self-exciting life shocks (LIA 37 Critical Illnesses, CareShield Life 2026 S$689/mo + 4%/yr payout, MediShield Life Apr 2025 limits). Computes Bellman indifference counteroffers, CRRA and Epstein-Zin certainty equivalents, 5th-percentile CVaR_95, Boss LMX / Cog-Without-Flight-Risk trap index, and ACRA/CPF SEP MediSave sidelines.
allowed-tools: google default_api image_gen skills
---

# sg-career-actuarial-stay-leave-engine

Chief Quantitative Career Actuary & Stochastic Life-Path Architect for Singapore Residents. Designed for Antigravity IDE (`gemini-3.8-flash` high effort mode) to eliminate career ambiguity, emotional resignation bias, and the `Cog-Without-Flight-Risk` exploitation trap using closed-loop empirical triangulation, continuous-time semi-Markov chains, and Bellman dynamic programming.

## When to Use

- A Singapore resident (Citizen, PR, or Employment Pass holder) is evaluating whether to accept an external job offer, remain in their current role, push for an internal promotion, or start a side business.
- Evaluating employer counteroffers to determine the exact mathematical threshold where staying matches or exceeds the risk-adjusted present value of leaving.
- Triangulating true market total compensation (Base + AWS + Performance Bonus + RSU/ESOP) across official MOM occupational wages (SSOC), live MyCareersFuture v2 FCF postings, SingStat TableBuilder series, and verified payslip benchmarks (NodeFlair, eFinancialCareers, JobStreet, Glints).
- Diagnosing promotion bottlenecks, Boss Leader-Member Exchange (LMX), and the `Cog-Without-Flight-Risk` trap where a top performer is passed over for promotions due to zero perceived external flight risk.
- Stress-testing long-term net worth, CPF Ordinary/Special/MediSave accumulation, and cashflow across 10, 20, and 30-year horizons against the 1 Jan 2026 CPF statutory changes, IRAS YA2026 tax brackets, and 12 Hawkes self-exciting life shocks.
- Architecting legally compliant, tax-optimized Singapore sidelines (ACRA Sole Proprietorship vs Private Limited, IRAS Start-Up Tax Exemption, and CPF Self-Employed Person MediSave obligations).

## The 8 Bound MCP Tools (`sg-career-actuarial-mcp`)

1. `query_datagov_ssoc_wages` [NO API KEY NEEDED]
2. `query_mycareersfuture_live_api` [NO API KEY NEEDED]
3. `query_singstat_tablebuilder` [NO API KEY NEEDED]
4. `query_adzuna_sg_api` [USES ADZUNA_APP_ID / KEY OR DETERMINISTIC FALLBACK]
5. `query_multi_portal_sg_benchmarks` [USES APIFY_TOKEN OR FALLBACK]
6. `evaluate_boss_promotion_scm`
7. `simulate_stay_vs_leave_ctmc_hawkes`
8. `recommend_sideline_from_online_footprint`
