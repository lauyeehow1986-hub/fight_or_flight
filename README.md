# Singapore Quantitative Career Actuary & Stochastic Life-Path Engine (`fight_or_flight`)

Antigravity Skill: `sg-career-actuarial-stay-leave-engine`  
FastMCP Server: `sg-career-actuarial-mcp`

---

## Capabilities
1. **MOM Resident Occupational Wages by 5-digit SSOC** (`query_datagov_ssoc_wages`)
2. **Live MyCareersFuture v2 FCF-mandated salary bands & applicant-to-vacancy ratios** (`query_mycareersfuture_live_api`)
3. **SingStat TableBuilder M182171 & 18035 Household Expenditure Survey** (`query_singstat_tablebuilder`)
4. **Adzuna Singapore parametric salary histograms & 12-month wage drift** (`query_adzuna_sg_api`)
5. **Multi-portal benchmarks**: JobStreet, eFinancialCareers, Glints, NodeFlair (`query_multi_portal_sg_benchmarks`)
6. **Structural Causal Model (SCM) for Boss LMX, Skip-Level Sponsorship & Cog-Without-Flight-Risk trap** (`evaluate_boss_promotion_scm`)
7. **6-layer CTMC + Merton/Kou Jump-Diffusion + 12-factor Hawkes Life Shocks** (`simulate_stay_vs_leave_ctmc_hawkes`)
8. **ACRA Sole Prop / Pte Ltd, CPF Self-Employed MediSave (8%-10.5%), and Moonlighting COI Governance** (`recommend_sideline_from_online_footprint`)

---

## Interactive Visualization & Stochastic Roadmap (`ssoc_career_actuarial_visualizer.html`)
The project includes a standalone, offline-capable interactive HTML5/Canvas visualization dashboard:
- **Interactive Role Matching**: Live searchable autocomplete across all 1,006 SSOC 2024 occupations for both Current Role (STAY) and Target Role (LEAVE).
- **Multi-Horizon Trajectory Engine**: Live toggle between **10-Year**, **20-Year**, **30-Year**, and **Till Retirement (e.g. Age X → 65)** roadmaps.
- **Dynamic Stochastic Canvas Chart**: Real-time rendering of median net worth paths, 5th-percentile downside CVaR95 risk bands, and compounded sideline portfolio growth.
- **Live Bellman Counteroffer Solver**: Dynamically calculates the exact monthly salary and bonus increment required from current employer to achieve financial indifference with an external hop.
- **Boss LMX & Cog-Without-Flight-Risk Diagnosis**: Live Structural Causal Model (SCM) measuring political capital, 12-month promotion odds, and exploitation trap index.
- **Year-by-Year Milestone Table**: Complete tabular cashflow, CPF Ordinary/Special account accumulation, and net worth progression.

---

## SSOC 2024 Comprehensive Actuarial Valuation & Sideline Master Dataset
The master dataset (`ssoc_2024_actuarial_stay_leave_master.csv` & `.json`) covers **all 1,006 unique 5-digit SSOC occupations** with:
1. **Occupational Wage Baseline**: $P_{25}, P_{50}, P_{75}$, modeled bonus months, total annual cash.
2. **Mobility Hurdle Rates**: Definite leave increment threshold (%), target external base salary, and Bellman indifference counteroffer.
3. **Simulated Sideline Playbook**:
   - Tailored side business title & operational model.
   - ACRA Legal Structure (Sole Proprietorship vs Exempt Private Limited with SUTE tax exemption).
   - Weekly time budget (8 hrs/week baseline).
   - Monthly & Annual Gross Revenue.
   - 2026 CPF Self-Employed Person (SEP) MediSave contribution (9% on Net Trade Income > S$6,000, capped at S$8,160).
   - Net disposable annual cashflow.
   - Moonlighting Conflict of Interest (COI) risk level and concrete safe-harbor mitigation protocol.

### Summary Across Major SSOC Groups
| Major SSOC Group | Occs | Median Base ($P_{50}$) | Definite Leave Threshold | Required Counteroffer | Sideline Monthly Gross | Sideline Annual Net Cash |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1 - Managers & Senior Officials** | 82 | **S$11,076 / mo** | **+21.4%** | **S$14,310 / mo (+29.2%)** | **S$3,996 / mo** | **S$38,410 / yr** |
| **2 - Professionals** | 308 | **S$9,316 / mo** | **+22.6%** | **S$12,120 / mo (+30.1%)** | **S$3,527 / mo** | **S$33,896 / yr** |
| **3 - Associate Professionals & Technicians** | 216 | **S$4,388 / mo** | **+18.5%** | **S$5,358 / mo (+22.1%)** | **S$1,536 / mo** | **S$14,757 / yr** |
| **4 - Clerical Support Workers** | 60 | **S$3,117 / mo** | **+16.0%** | **S$3,656 / mo (+17.3%)** | **S$1,091 / mo** | **S$10,481 / yr** |
| **5 - Service & Sales Workers** | 86 | **S$2,937 / mo** | **+15.6%** | **S$3,416 / mo (+16.3%)** | **S$1,175 / mo** | **S$11,289 / yr** |
| **6 - Agricultural & Fishery Workers** | 11 | **S$2,600 / mo** | **+15.0%** | **S$2,985 / mo (+14.8%)** | **S$910 / mo** | **S$8,743 / yr** |
| **7 - Craftsmen & Related Trades Workers** | 94 | **S$3,391 / mo** | **+16.4%** | **S$3,981 / mo (+17.4%)** | **S$1,526 / mo** | **S$14,663 / yr** |
| **8 - Plant & Machine Operators & Drivers** | 79 | **S$3,234 / mo** | **+15.3%** | **S$3,742 / mo (+15.7%)** | **S$1,229 / mo** | **S$11,808 / yr** |
| **9 - Cleaners, Labourers & Elementary** | 65 | **S$1,968 / mo** | **+14.0%** | **S$2,236 / mo (+13.6%)** | **S$886 / mo** | **S$8,515 / yr** |
| **X - Armed Forces & Unclassified** | 5 | **S$6,500 / mo** | **+20.0%** | **S$8,060 / mo (+24.0%)** | **S$2,275 / mo** | **S$21,858 / yr** |

---

## Statutory & Economic Parameters Enforced
- **CPF Statutory Ceilings (1 Jan 2026)**: S$8,000 monthly Ordinary Wage (OW) ceiling; S$102,000 annual wage ceiling.
- **IRAS YA2026 Tax Schedules**: Progressive resident tax brackets up to 24% marginal rate.
- **Goods & Services Tax (GST)**: 9% statutory rate.
- **Hawkes Life Shocks**: LIA 37 critical illness, MediShield Life Apr 2025 claim limits, CareShield Life 2026 S$689/mo payout.
- **Counteroffer Hazard Rule**: Internal counteroffers must carry a **1.25x - 1.65x risk surcharge** over external offers to offset post-counteroffer loyalty erosion and replacement risks.

---

## Installation & Setup

### 1. Antigravity Skill
Clone or copy the skill directory into your local Antigravity skills configuration:
```bash
# Target location:
~/.gemini/config/skills/sg-career-actuarial-stay-leave-engine
```

### 2. FastMCP Server Registration
Add the server entry to your Antigravity MCP configuration (`~/.gemini/config/mcp_config.json`):
```json
{
  "mcpServers": {
    "sg-career-actuarial-mcp": {
      "command": "python",
      "args": [
        "mcp_servers/sg_career_actuarial_mcp.py"
      ],
      "env": {}
    }
  }
}
```
*(Note: Replace `mcp_servers/sg_career_actuarial_mcp.py` with the absolute path to `mcp_servers/sg_career_actuarial_mcp.py` on your machine if running outside the repository root).*
