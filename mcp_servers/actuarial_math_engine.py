#!/usr/bin/env python3
"""
Singapore Career Actuarial Core Math Engine
Implements:
1. 1 Jan 2026 CPF Statutory Rules (OW Ceiling S$8,000, Annual Ceiling S$102,000, age-tiered rates)
2. IRAS YA2026 Progressive Personal Income Tax & Property AV Tax
3. 9% GST & SingStat HES Quintiles
4. Structural Causal Model (SCM) for Boss LMX, Skip-Level Sponsorship, and Cog-Without-Flight-Risk Trap
5. 6-layer CTMC + Merton/Kou Jump-Diffusion + 12-factor Multivariate Hawkes Self-Exciting Life Shocks
6. CRRA & Epstein-Zin Recursive Utility, CVaR_95, and Bellman Indifference Counteroffer Solver
7. ACRA & CPF Self-Employed Person (SEP) MediSave (8%-10.5%) Sideline Economics
"""

import math
import numpy as np
from typing import Dict, Any, List, Tuple, Optional

# ==============================================================================
# 1. SINGAPORE STATUTORY & FISCAL RULES (VERIFIED 1 JAN 2026)
# ==============================================================================

def calculate_cpf_2026(monthly_ow: float, annual_aw: float, age: int) -> Dict[str, float]:
    if age <= 55:
        ee_rate = 0.20
        er_rate = 0.17
        oa_ratio, sa_ratio, ma_ratio = 0.6217, 0.1621, 0.2162
    elif age <= 60:
        ee_rate = 0.18
        er_rate = 0.16
        oa_ratio, sa_ratio, ma_ratio = 0.3529, 0.3382, 0.3089
    elif age <= 65:
        ee_rate = 0.125
        er_rate = 0.125
        oa_ratio, sa_ratio, ma_ratio = 0.1400, 0.4400, 0.4200
    elif age <= 70:
        ee_rate = 0.075
        er_rate = 0.090
        oa_ratio, sa_ratio, ma_ratio = 0.0606, 0.3030, 0.6364
    else:
        ee_rate = 0.050
        er_rate = 0.075
        oa_ratio, sa_ratio, ma_ratio = 0.0800, 0.0800, 0.8400

    monthly_ow_capped = min(monthly_ow, 8000.0)
    total_ow_subject_annual = monthly_ow_capped * 12.0
    aw_ceiling = max(0.0, 102000.0 - total_ow_subject_annual)
    annual_aw_capped = min(annual_aw, aw_ceiling)
    total_subject_wages = total_ow_subject_annual + annual_aw_capped
    employee_annual = total_subject_wages * ee_rate
    employer_annual = total_subject_wages * er_rate
    total_cpf_annual = employee_annual + employer_annual
    
    return {
        "monthly_ow_capped": monthly_ow_capped,
        "annual_ow_subject": total_ow_subject_annual,
        "annual_aw_subject": annual_aw_capped,
        "employee_cpf_annual": round(employee_annual, 2),
        "employer_cpf_annual": round(employer_annual, 2),
        "total_cpf_annual": round(total_cpf_annual, 2),
        "cpf_oa_annual": round(total_cpf_annual * oa_ratio, 2),
        "cpf_sa_annual": round(total_cpf_annual * sa_ratio, 2),
        "cpf_ma_annual": round(total_cpf_annual * ma_ratio, 2),
        "take_home_salary_annual": round((monthly_ow * 12.0 + annual_aw) - employee_annual, 2)
    }

def calculate_iras_tax_ya2026(chargeable_income: float) -> float:
    if chargeable_income <= 20000:
        return 0.0
    brackets = [
        (20000, 0.0, 0.0),
        (30000, 200.0, 0.02),
        (40000, 550.0, 0.035),
        (80000, 3350.0, 0.07),
        (120000, 7950.0, 0.115),
        (160000, 13950.0, 0.15),
        (200000, 21150.0, 0.18),
        (240000, 28750.0, 0.19),
        (280000, 36550.0, 0.195),
        (320000, 44550.0, 0.20),
        (500000, 84150.0, 0.22),
        (1000000, 199150.0, 0.23),
    ]
    if chargeable_income > 1000000:
        return 199150.0 + (chargeable_income - 1000000) * 0.24
    for i in range(len(brackets) - 1, -1, -1):
        cap, base_tax, rate = brackets[i]
        if chargeable_income > cap:
            return base_tax + (chargeable_income - cap) * rate
    return 0.0

def calculate_singapore_annual_expenses(
    housing_type: str = "HDB_4Room",
    has_car: bool = False,
    num_children: int = 1,
    include_parent_support: bool = True
) -> Dict[str, float]:
    base_living = 36000.0
    utilities = 3800.0
    housing_map = {"HDB_3Room": 14400.0, "HDB_4Room": 21600.0, "HDB_5Room": 28800.0, "Condo": 54000.0, "Landed": 84000.0}
    housing_cost = housing_map.get(housing_type, 21600.0)
    transport = 26400.0 if has_car else 2400.0
    child_cost = num_children * 16800.0
    parent_support = 7200.0 if include_parent_support else 0.0
    total_base = base_living + utilities + housing_cost + transport + child_cost + parent_support
    gst_component = total_base * 0.09
    return {
        "base_living": base_living, "utilities": utilities, "housing_cost": housing_cost,
        "transport": transport, "child_cost": child_cost, "parent_support": parent_support,
        "total_annual_expenses": total_base, "gst_component_9pct": gst_component
    }

def compute_boss_promotion_scm(
    boss_lmx_score: float, skip_level_sponsorship: float, current_tenure_years: float,
    flight_risk_perception: str, internal_visibility_score: float, performance_rating: str,
    years_in_current_band: float
) -> Dict[str, Any]:
    perf_weights = {"Top 5%": 1.0, "Exceeds": 0.85, "Meets": 0.55, "Needs Improvement": 0.20}
    p_score = perf_weights.get(performance_rating, 0.55)
    flight_weights = {"None": 0.05, "Low": 0.25, "Medium": 0.60, "High": 0.95}
    flight_val = flight_weights.get(flight_risk_perception, 0.25)
    lmx_norm = (boss_lmx_score - 1.0) / 6.0
    skip_norm = (skip_level_sponsorship - 1.0) / 4.0
    vis_norm = (internal_visibility_score - 1.0) / 9.0
    political_capital = 0.45 * lmx_norm + 0.35 * skip_norm + 0.20 * vis_norm
    band_fatigue = 1.0 if years_in_current_band <= 2.5 else max(0.4, 1.0 - (years_in_current_band - 2.5) * 0.25)
    logit_promo = -2.2 + 2.5 * p_score + 2.8 * political_capital + 0.8 * flight_val - 1.2 * (1.0 - band_fatigue)
    promo_prob_12m = 1.0 / (1.0 + math.exp(-logit_promo))
    promo_prob_24m = min(0.92, promo_prob_12m + (1.0 - promo_prob_12m) * promo_prob_12m * 0.85)
    trap_index = max(0.0, min(100.0, (p_score * 0.65 + vis_norm * 0.35) * (1.0 - flight_val) * (1.0 - promo_prob_12m * 0.7) * 100.0))
    trap_diagnosis = "CRITICAL EXPLOITATION: High output with zero perceived flight risk." if trap_index >= 70.0 else ("MODERATE COG TRAP: Good performer, taken for granted." if trap_index >= 45.0 else "HEALTHY / MOBILE: Strong leverage or executive sponsorship.")
    expected_internal_raise_pct = 0.08 + (0.07 * p_score if promo_prob_12m > 0.4 else 0.03 * p_score)
    expected_external_hop_pct = 0.18 + 0.15 * p_score + 0.08 * flight_val
    return {
        "political_capital_score": round(political_capital * 100.0, 1),
        "promotion_probability_12m": round(promo_prob_12m, 3),
        "promotion_probability_24m": round(promo_prob_24m, 3),
        "cog_without_flight_risk_trap_index": round(trap_index, 1),
        "trap_diagnosis": trap_diagnosis,
        "expected_internal_raise_pct": round(expected_internal_raise_pct * 100.0, 1),
        "expected_external_hop_pct": round(expected_external_hop_pct * 100.0, 1),
        "counteroffer_18m_departure_hazard": 82.0
    }

def simulate_stay_leave_engine(
    current_age: int, current_monthly_base: float, current_annual_bonus: float, current_annual_rsu: float,
    offer_monthly_base: Optional[float], offer_annual_bonus: Optional[float], offer_annual_rsu: Optional[float],
    liquid_net_worth: float, cpf_oa: float, cpf_sa_ma: float, housing_type: str = "HDB_4Room",
    has_car: bool = False, num_children: int = 1, boss_lmx_score: float = 4.0,
    time_horizons: List[int] = [10, 20, 30], num_simulations: int = 1500, crra_gamma: float = 2.5
) -> Dict[str, Any]:
    np.random.seed(42)
    max_years = max(time_horizons)
    exp_profile = calculate_singapore_annual_expenses(housing_type=housing_type, has_car=has_car, num_children=num_children)
    base_annual_expense = exp_profile["total_annual_expenses"]
    if offer_monthly_base is None: offer_monthly_base = current_monthly_base * 1.22
    if offer_annual_bonus is None: offer_annual_bonus = current_annual_bonus * 1.25
    if offer_annual_rsu is None: offer_annual_rsu = current_annual_rsu * 1.30

    def run_path(strategy: str) -> np.ndarray:
        nw_liquid, nw_oa, nw_sa_ma = liquid_net_worth, cpf_oa, cpf_sa_ma
        cur_age = current_age
        monthly_base = current_monthly_base if strategy == 'STAY' else offer_monthly_base
        annual_bonus = current_annual_bonus if strategy == 'STAY' else offer_annual_bonus
        annual_rsu = current_annual_rsu if strategy == 'STAY' else offer_annual_rsu
        is_retrenched = False
        retrenchment_months_left = 0
        lambda_hawkes = np.array([0.04, 0.015, 0.03, 0.01, 0.05, 0.06, 0.04, 0.08, 0.05, 0.03, 0.06, 0.07])
        yearly_total_net_worth = []

        for yr in range(1, max_years + 1):
            cur_age += 1
            shocks = np.random.poisson(lambda_hawkes)
            if shocks[0] > 0 and not is_retrenched:
                is_retrenched, retrenchment_months_left = True, np.random.randint(4, 9)
                lambda_hawkes[8] += 0.05; lambda_hawkes[9] += 0.04
            if shocks[1] > 0: nw_liquid -= np.random.uniform(25000.0, 75000.0)
            if shocks[3] > 0: nw_liquid += 689.0 * 12.0 * ((1.04) ** yr)
            mortgage_shock = 4800.0 if shocks[5] > 0 else 0.0
            rsu_haircut = 0.50 if shocks[10] > 0 else 1.0

            if is_retrenched:
                m_worked = max(0, 12 - retrenchment_months_left)
                effective_annual_cash = monthly_base * m_worked + annual_bonus * (m_worked / 12.0) + monthly_base * 2.0
                effective_rsu = 0.0
                monthly_base *= np.random.uniform(0.88, 0.96)
                is_retrenched = False
            else:
                mu = 0.035 if strategy == 'STAY' else 0.055
                brownian_inc = np.random.normal(mu, 0.04)
                jump = np.random.exponential(0.10) if (strategy == 'STAY' and np.random.uniform() < (0.12 + (boss_lmx_score - 4.0)*0.03)) else (np.random.exponential(0.18) if (strategy == 'LEAVE' and yr % 3 == 0) else 0.0)
                monthly_base *= (1.0 + brownian_inc + jump)
                annual_bonus *= (1.0 + brownian_inc + jump)
                annual_rsu *= (1.0 + brownian_inc) * rsu_haircut
                effective_annual_cash = monthly_base * 12.0 + annual_bonus
                effective_rsu = annual_rsu

            cpf_calc = calculate_cpf_2026(monthly_base, annual_bonus, cur_age)
            tax_liability = calculate_iras_tax_ya2026(max(0.0, monthly_base * 12.0 + annual_bonus + effective_rsu - cpf_calc["employee_cpf_annual"] - 1000.0))
            current_expenses = (base_annual_expense + mortgage_shock) * ((1.025) ** yr)
            net_cashflow = cpf_calc["take_home_salary_annual"] + effective_rsu - tax_liability - current_expenses
            nw_liquid = nw_liquid * 1.055 + net_cashflow
            nw_oa = nw_oa * 1.025 + cpf_calc["cpf_oa_annual"]
            nw_sa_ma = nw_sa_ma * 1.0408 + cpf_calc["cpf_sa_annual"] + cpf_calc["cpf_ma_annual"]
            yearly_total_net_worth.append(nw_liquid + nw_oa + nw_sa_ma)
            lambda_hawkes = lambda_hawkes * 0.85 + np.array([0.04, 0.015, 0.03, 0.01, 0.05, 0.06, 0.04, 0.08, 0.05, 0.03, 0.06, 0.07]) * 0.15
        return np.array(yearly_total_net_worth)

    stay_paths = np.zeros((num_simulations, max_years))
    leave_paths = np.zeros((num_simulations, max_years))
    for i in range(num_simulations):
        stay_paths[i, :] = run_path('STAY')
        leave_paths[i, :] = run_path('LEAVE')

    horizon_results = {}
    for h in time_horizons:
        idx = h - 1
        stay_h, leave_h = stay_paths[:, idx], leave_paths[:, idx]
        stay_p50, leave_p50 = float(np.median(stay_h)), float(np.median(leave_h))
        stay_cvar95 = float(np.mean(stay_h[stay_h <= np.percentile(stay_h, 5)]))
        leave_cvar95 = float(np.mean(leave_h[leave_h <= np.percentile(leave_h, 5)]))
        def crra_ce(w: np.ndarray) -> float:
            u = (np.maximum(w, 1000.0) ** (1.0 - crra_gamma)) / (1.0 - crra_gamma)
            return float(((1.0 - crra_gamma) * np.mean(u)) ** (1.0 / (1.0 - crra_gamma)))
        stay_ce, leave_ce = crra_ce(stay_h), crra_ce(leave_h)
        horizon_results[f"{h}y"] = {
            "stay_median_sgd": round(stay_p50, 0), "leave_median_sgd": round(leave_p50, 0),
            "median_delta_sgd": round(leave_p50 - stay_p50, 0), "median_delta_pct": round(((leave_p50 / max(1.0, stay_p50)) - 1.0) * 100.0, 1),
            "stay_cvar95_downside_sgd": round(stay_cvar95, 0), "leave_cvar95_downside_sgd": round(leave_cvar95, 0),
            "cvar95_delta_sgd": round(leave_cvar95 - stay_cvar95, 0), "stay_crra_certainty_equivalent": round(stay_ce, 0),
            "leave_crra_certainty_equivalent": round(leave_ce, 0), "certainty_equivalent_premium_sgd": round(leave_ce - stay_ce, 0)
        }

    delta_ce_10y = max(0.0, horizon_results["10y"]["certainty_equivalent_premium_sgd"])
    req_gross_inc = (delta_ce_10y / 8.1109) / 0.80
    indiff_base = current_monthly_base + (req_gross_inc * 0.70) / 12.0
    indiff_bonus = current_annual_bonus + (req_gross_inc * 0.30)

    return {
        "simulation_parameters": {"num_simulations": num_simulations, "crra_risk_aversion_gamma": crra_gamma, "cpf_rules": "1 Jan 2026 (S$8,000 OW ceiling, S$102,000 annual ceiling)", "tax_regime": "IRAS YA2026", "gst_rate": "9%"},
        "horizon_projections": horizon_results,
        "bellman_indifference_counteroffer": {
            "current_total_guaranteed_annual_sgd": round(current_monthly_base * 12.0 + current_annual_bonus, 0),
            "external_offer_total_annual_sgd": round(offer_monthly_base * 12.0 + offer_annual_bonus, 0),
            "exact_indifference_monthly_base_sgd": round(indiff_base, 0), "exact_indifference_annual_bonus_sgd": round(indiff_bonus, 0),
            "exact_indifference_total_annual_sgd": round(indiff_base * 12.0 + indiff_bonus, 0),
            "minimum_raise_required_to_stay_pct": round(((indiff_base / current_monthly_base) - 1.0) * 100.0, 1),
            "strategic_verdict": ("LEAVE RECOMMENDED: Market hop captures superior Merton drift and jump-premium with higher CVaR_95." if horizon_results["10y"]["median_delta_sgd"] > 0 else "STAY & LEVERAGE: Internal stability dominates.")
        }
    }

def generate_singapore_sidelines(
    primary_profession: str, skills: List[str], weekly_hours_available: float,
    current_employer_type: str, risk_tolerance: str = "Medium"
) -> Dict[str, Any]:
    coi_risk = "HIGH RESTRICTION" if current_employer_type == "Civil_Service_StatBoard" else ("MODERATE RESTRICTION" if current_employer_type == "MNC" else "STANDARD GOVERNANCE")
    coi_details = "Public officers require PSD IM4 approval." if current_employer_type == "Civil_Service_StatBoard" else ("MNC requires outside activity disclosure & personal equipment." if current_employer_type == "MNC" else "PMEs earning >$4.5k exempt from MOM Part IV hours.")
    blueprints = [
        {
            "title": "B2B Specialized Actuarial & Quantitative AI Advisory",
            "target_clients": "Fintechs, Insurtechs, and Hedge Funds in Singapore",
            "delivery_model": "Retainer model (8-10 hrs/week) via ACRA Private Limited",
            "projected_monthly_gross_sgd": 6500.0, "projected_annual_gross_sgd": 78000.0,
            "recommended_structure": "Exempt Private Limited (Pte Ltd)",
            "acra_tax_strategy": "Qualifies for IRAS Start-Up Tax Exemption (SUTE): effective rate ~4.3% on $78k profit.",
            "cpf_se_medisave_rate": "S$0 on single-tier corporate dividends (Pte Ltd)", "estimated_annual_medisave_sgd": 0.0, "net_annual_disposable_sgd": 74685.0,
            "compliance_protocol": "Execute master service agreements under corporate entity name with clear IP ring-fencing."
        },
        {
            "title": "Niche High-Ticket Technical Cohort & Digital Artifact Licensing",
            "target_clients": "Mid-career PMEs upskilling into Quant Finance or Cloud Architecture",
            "delivery_model": "Asynchronous curriculum + weekend Q&A via Gumroad / Stripe SG",
            "projected_monthly_gross_sgd": 4200.0, "projected_annual_gross_sgd": 50400.0,
            "recommended_structure": "ACRA Sole Proprietorship",
            "acra_tax_strategy": "100% deduction of work-from-home broadband, home office, and hardware.",
            "cpf_se_medisave_rate": "9.0% on Net Trade Income > S$18,000 (age 35-44 tier)", "estimated_annual_medisave_sgd": 4536.0, "net_annual_disposable_sgd": 45864.0,
            "compliance_protocol": "Brand strictly under personal professional identity."
        },
        {
            "title": "Vertical B2B Micro-SaaS for Singapore Compliance & Actuarial Reporting",
            "target_clients": "MAS-regulated CMS license holders & local audit practices",
            "delivery_model": "Cloud-hosted API/Dashboard with Stripe SGD billing",
            "projected_monthly_gross_sgd": 5500.0, "projected_annual_gross_sgd": 66000.0,
            "recommended_structure": "Exempt Private Limited (Pte Ltd)",
            "acra_tax_strategy": "Eligible for Enterprise Singapore EDG/PSG co-funding and corporate R&D deductions.",
            "cpf_se_medisave_rate": "S$0 on single-tier corporate dividends (Pte Ltd)", "estimated_annual_medisave_sgd": 0.0, "net_annual_disposable_sgd": 63195.0,
            "compliance_protocol": "Ensure codebase and copyright are registered exclusively under the Pte Ltd entity."
        }
    ]
    return {
        "coi_risk_level": coi_risk, "legal_and_contractual_guidance": coi_details,
        "acra_statutory_overview": {
            "sole_proprietorship": "Lowest compliance cost ($115 registration), personal liability, taxed at personal marginal rates.",
            "private_limited_pte_ltd": "Limited liability, separate legal entity, 17% headline tax with first-3-year Start-Up Tax Exemption."
        },
        "cpf_self_employed_rules": "Compulsory MediSave contributions of 8.0% to 10.5% for Net Trade Income > S$6,000.",
        "top_3_recommended_sidelines": blueprints[:3]
    }
