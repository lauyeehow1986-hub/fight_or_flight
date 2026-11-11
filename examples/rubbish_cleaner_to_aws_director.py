#!/usr/bin/env python3
"""
Case Study: 'Rubbish Cleaner' Grunt Worker to Director of Research at AWS
Demonstrates:
1. SCM Diagnosis: Frosty direct boss (LMX 2.0/7.0) vs. Great skip-level sponsor (4.5/5.0)
2. 6-layer CTMC + Merton/Kou Jump-Diffusion + 12-factor Hawkes Life Shocks under 1 Jan 2026 CPF Rules
3. 10/20/30-Year Median Net Worth, CVaR_95, and Bellman Indifference Counteroffer Solver
"""

import sys
import os
import json

# Add mcp_servers to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mcp_servers"))
from actuarial_math_engine import (
    compute_boss_promotion_scm,
    simulate_stay_leave_engine,
    generate_singapore_sidelines
)

def run_case_study():
    print("=" * 80)
    print("CASE STUDY: 'Rubbish Cleaner' (Age 28) -> Director of Research at AWS")
    print("=" * 80)

    # 1. Structural Causal Model (SCM) for Organizational Friction
    scm_out = compute_boss_promotion_scm(
        boss_lmx_score=2.0,            # Frosty direct boss
        skip_level_sponsorship=4.5,    # Great skip-level sponsor
        current_tenure_years=2.5,
        flight_risk_perception="Low",
        internal_visibility_score=5.0,
        performance_rating="Exceeds",
        years_in_current_band=2.0
    )
    print("\n--- 1. BOSS SCM DIAGNOSIS ---")
    print(f"Political Capital Score: {scm_out['political_capital_score']} / 100")
    print(f"Cog-Without-Flight-Risk Trap Index: {scm_out['cog_without_flight_risk_trap_index']}")
    print(f"Diagnosis: {scm_out['trap_diagnosis']}")
    print(f"Counteroffer 18-Month Attrition Hazard: {scm_out['counteroffer_18m_departure_hazard']}%")

    # 2. 6-Layer CTMC + Hawkes Simulation
    sim_out = simulate_stay_leave_engine(
        current_age=28,
        current_monthly_base=10000.0,
        current_annual_bonus=40000.0,
        current_annual_rsu=0.0,
        offer_monthly_base=26000.0,
        offer_annual_bonus=75000.0,
        offer_annual_rsu=220000.0,
        liquid_net_worth=120000.0,
        cpf_oa=60000.0,
        cpf_sa_ma=40000.0,
        housing_type="HDB_4Room",
        has_car=False,
        num_children=0,
        boss_lmx_score=2.0,
        time_horizons=[10, 20, 30],
        num_simulations=2000
    )

    print("\n--- 2. STOCHASTIC LIFE-PATH TRAJECTORY (1 JAN 2026 CPF RULES) ---")
    for h in ["10y", "20y", "30y"]:
        data = sim_out["horizon_projections"][h]
        print(f"\nHorizon: {h}")
        print(f"  STAY Median Net Worth:  S${data['stay_median_sgd']:>12,.0f} | CVaR_95 Downside: S${data['stay_cvar95_downside_sgd']:>12,.0f}")
        print(f"  LEAVE Median Net Worth: S${data['leave_median_sgd']:>12,.0f} | CVaR_95 Downside: S${data['leave_cvar95_downside_sgd']:>12,.0f}")
        print(f"  Net Worth Delta:        +S${data['median_delta_sgd']:>11,.0f} (+{data['median_delta_pct']}%)")

    # 3. Bellman Indifference Counteroffer
    bellman = sim_out["bellman_indifference_counteroffer"]
    print("\n--- 3. BELLMAN INDIFFERENCE COUNTEROFFER ---")
    print(f"Current Employer Total Guaranteed: S${bellman['current_total_guaranteed_annual_sgd']:,.0f}/yr")
    print(f"Required Monthly Base to Stay:     S${bellman['exact_indifference_monthly_base_sgd']:,.0f}/mo (+{bellman['minimum_raise_required_to_stay_pct']}%)")
    print(f"Required Annual Bonus to Stay:    S${bellman['exact_indifference_annual_bonus_sgd']:,.0f}")
    print(f"Required Total Annual to Stay:     S${bellman['exact_indifference_total_annual_sgd']:,.0f}/yr")
    print(f"Verdict: {bellman['strategic_verdict']}")

    # 4. Sidelines
    sidelines = generate_singapore_sidelines(
        primary_profession="Director of Research",
        skills=["Distributed Systems", "Cloud Architecture", "AI Infrastructure", "Python"],
        weekly_hours_available=8.0,
        current_employer_type="MNC"
    )
    print("\n--- 4. TOP COMPLIANT SIDELINES ---")
    for idx, s in enumerate(sidelines["top_3_recommended_sidelines"], 1):
        print(f"{idx}. {s['title']} ({s['recommended_structure']})")
        print(f"   Gross: S${s['projected_annual_gross_sgd']:,.0f} | Net Disposable: S${s['net_annual_disposable_sgd']:,.0f}")

if __name__ == "__main__":
    run_case_study()
