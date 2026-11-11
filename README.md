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

## SSOC 2024 Comprehensive Actuarial Valuation Master Dataset
The project contains full actuarial valuations for **all 1,006 unique 5-digit SSOC occupations** in Singapore:
- `ssoc_2024_actuarial_stay_leave_master.csv`
- `ssoc_2024_actuarial_stay_leave_master.json`

### Computed Actuarial Metrics per Occupation
- **Baseline Monthly Base Salary**: 25th percentile ($P_{25}$), Median ($P_{50}$), 75th percentile ($P_{75}$).
- **Annual Bonus Months**: Actuarially modeled based on SSOC major group industry benchmarks (1.2 to 3.8 months).
- **Total Annual Cash Baseline**: Total annual gross earnings under current role.
- **Definite Leave Increment Threshold (%)**: The minimum percentage increment in total annual cash required to justify departure, factoring in switching costs, probation risk (15%), culture risk (20%), and tenure loss.
- **Target Leave Base Salary (SGD/month)**: Recommended minimum monthly base pay to demand when receiving an external job offer.
- **Bellman Indifference Counteroffer (SGD/month)**: Minimum monthly base salary required from current employer to stay, pricing in the empirical **82% 18-month counteroffer departure hazard** and stunted internal wage drift.

### Summary Across Major SSOC Groups
| Major SSOC Group | Total Occupations | Median Base ($P_{50}$) | Definite Leave Threshold | Required Counteroffer |
| :--- | :--- | :--- | :--- | :--- |
| **1 - Managers & Senior Officials** | 82 | S$11,076 / mo | **+21.4%** | **S$14,310 / mo (+29.2%)** |
| **2 - Professionals** | 308 | S$9,316 / mo | **+22.6%** | **S$12,120 / mo (+30.1%)** |
| **3 - Associate Professionals & Technicians** | 216 | S$4,388 / mo | **+18.5%** | **S$5,358 / mo (+22.1%)** |
| **4 - Clerical Support Workers** | 60 | S$3,117 / mo | **+16.0%** | **S$3,656 / mo (+17.3%)** |
| **5 - Service & Sales Workers** | 86 | S$2,937 / mo | **+15.6%** | **S$3,416 / mo (+16.3%)** |
| **6 - Agricultural & Fishery Workers** | 11 | S$2,600 / mo | **+15.0%** | **S$2,985 / mo (+14.8%)** |
| **7 - Craftsmen & Related Trades Workers** | 94 | S$3,391 / mo | **+16.4%** | **S$3,981 / mo (+17.4%)** |
| **8 - Plant & Machine Operators & Assemblers** | 79 | S$3,234 / mo | **+15.3%** | **S$3,742 / mo (+15.7%)** |
| **9 - Cleaners, Labourers & Related Workers** | 65 | S$1,968 / mo | **+14.0%** | **S$2,236 / mo (+13.6%)** |
| **X - Workers Not Elsewhere Classified / Armed Forces**| 5 | S$6,500 / mo | **+20.0%** | **S$8,060 / mo (+24.0%)** |

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
