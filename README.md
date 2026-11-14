# Singapore Quantitative Career Actuary & Stochastic Life-Path Engine (`fight_or_flight`)

🌐 **Live Interactive Web App (GitHub Pages)**: [https://lauyeehow1986-hub.github.io/fight_or_flight/](https://lauyeehow1986-hub.github.io/fight_or_flight/)

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

## Interactive Visualization & Stochastic Roadmap (`index.html`)
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
   - 2026 CPF Self-Employed Person (SEP) MediSave contribution (age-tiered 8%–10.5% on Net Trade Income up to S$102,000, capped at S$8,160–S$10,710/yr with S$6k–S$18k phase-in).
   - Net disposable annual cashflow.
   - Moonlighting Conflict of Interest (COI) risk level and concrete safe-harbor mitigation protocol.

### Summary Across Major SSOC Groups
| Major SSOC Group | Occs | Median Base ($P_{50}$) | Definite Leave Threshold | Required Counteroffer | Sideline Monthly Gross | Sideline Annual Net Cash |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1 - Managers & Senior Officials** | 82 | **S$7,772 / mo** | **+20.0%** | **S$9,930 / mo (+26.6%)** | **S$2,851 / mo** | **S$27,396 / yr** |
| **2 - Professionals** | 308 | **S$6,238 / mo** | **+22.0%** | **S$8,296 / mo (+28.1%)** | **S$2,420 / mo** | **S$23,255 / yr** |
| **3 - Associate Professionals & Technicians** | 216 | **S$3,958 / mo** | **+18.0%** | **S$4,812 / mo (+21.3%)** | **S$1,385 / mo** | **S$13,310 / yr** |
| **4 - Clerical Support Workers** | 60 | **S$3,100 / mo** | **+16.0%** | **S$3,635 / mo (+17.3%)** | **S$1,085 / mo** | **S$10,426 / yr** |
| **5 - Service & Sales Workers** | 86 | **S$2,803 / mo** | **+15.0%** | **S$3,235 / mo (+15.4%)** | **S$1,121 / mo** | **S$10,773 / yr** |
| **6 - Agricultural & Fishery Workers** | 11 | **S$2,142 / mo** | **+15.0%** | **S$2,460 / mo (+14.8%)** | **S$750 / mo** | **S$7,207 / yr** |
| **7 - Craftsmen & Related Trades Workers** | 94 | **S$2,571 / mo** | **+16.0%** | **S$3,077 / mo (+16.9%)** | **S$1,157 / mo** | **S$11,118 / yr** |
| **8 - Plant & Machine Operators & Drivers** | 79 | **S$2,440 / mo** | **+15.0%** | **S$2,851 / mo (+15.3%)** | **S$927 / mo** | **S$8,908 / yr** |
| **9 - Cleaners, Labourers & Elementary** | 65 | **S$1,816 / mo** | **+14.0%** | **S$2,064 / mo (+13.6%)** | **S$818 / mo** | **S$7,861 / yr** |
| **X - Armed Forces & Unclassified** | 5 | **S$6,500 / mo** | **+20.0%** | **S$8,063 / mo (+24.0%)** | **S$2,275 / mo** | **S$21,862 / yr** |

> **Salary Definition & Benchmark Comparison Caveat:**
> - **Basic Monthly Salary vs. MOM CLFS Gross Income:** `Median Base (P50)` above reports **monthly basic wages** (MOM OWS 2024 `mthly_basic_wage_50_pctile` + hierarchical peer medians), **excluding** annual bonuses/AWS and employer CPF. MOM's Comprehensive Labour Force Survey (CLFS) headline figures (e.g., `S$10,820` Managers, `S$8,363` Professionals, `S$4,735` Assoc Prof & Technicians; `S$5,775` all full-time employed residents) are **employment-weighted gross monthly incomes including 1/12th bonuses and 17% employer CPF**. Adding modeled bonuses and 17% employer CPF (up to the S$8,000 OW ceiling) to our dataset yields medians of **`S$11,117` / `S$9,078` / `S$5,330`**, aligned with CLFS.
> - **Equal-Weighted SSOC Codes vs. Worker Headcount:** The table takes medians across unique 5-digit SSOC codes (each occupation counts once) rather than weighting by headcount.
> - **Median (`P50`) vs. MOM COMPASS C1 Benchmarks:** MOM's Employment Pass COMPASS C1 schedules (`c1-salary-benchmarks-upcoming.pdf`) publish **65th and 90th percentile** local PMET fixed monthly salaries split by **sector × age (23–45+)**, not 50th-percentile all-age occupation medians.

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
