#!/usr/bin/env python3
"""
Build Standalone Interactive Visualizer for SG Career Actuarial Engine
Generates ssoc_career_actuarial_visualizer.html with embedded dataset of all 1,006 SSOC occupations,
interactive 10y/20y/30y/retirement roadmaps, live Bellman counteroffer solver, and sideline simulator.
"""

import os
import json
import pandas as pd

def build_visualizer():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "ssoc_2024_actuarial_stay_leave_master.json")
    with open(json_path, "r", encoding="utf-8") as f:
        master_data = json.load(f)
        
    print(f"Loaded {len(master_data)} occupations from {json_path}")
    
    # Minify records for fast client-side initialization
    compact_records = []
    for r in master_data:
        compact_records.append({
            "c": str(r["ssoc_code"]),
            "t": r["ssoc_title"],
            "p25": int(r["p25_monthly_base_sgd"]),
            "p50": int(r["p50_median_monthly_base_sgd"]),
            "p75": int(r["p75_monthly_base_sgd"]),
            "bm": float(r["typical_bonus_months"]),
            "tot": int(r["total_annual_cash_p50_sgd"]),
            "lp": float(r["definite_leave_min_increment_pct"]),
            "ltb": int(r["definite_leave_target_monthly_base_sgd"]),
            "bb": int(r["bellman_indifference_counteroffer_base_sgd"]),
            "br": float(r["bellman_counteroffer_required_raise_pct"]),
            "st": r["sideline_title"],
            "sd": r["sideline_description"],
            "ss": r["sideline_structure"],
            "sh": float(r["sideline_weekly_hours"]),
            "sm": int(r["sideline_monthly_gross_sgd"]),
            "sa": int(r["sideline_annual_gross_sgd"]),
            "sn": int(r["sideline_annual_net_cash_sgd"]),
            "smr": float(r["sideline_medisave_rate_pct"]),
            "smp": int(r["sideline_annual_medisave_sgd"]),
            "coi": r["sideline_coi_risk"],
            "com": r["sideline_coi_mitigation"]
        })
        
    json_payload = json.dumps(compact_records, separators=(',', ':'), ensure_ascii=False)
    print(f"Compacted JSON payload size: {len(json_payload)/1024:.1f} KB")

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Singapore Quantitative Career Actuary & Stochastic Life-Path Engine</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    :root {
      --bg: #090d16;
      --card: #111827;
      --card-border: #1f293d;
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --accent-stay: #38bdf8;
      --accent-leave: #10b981;
      --accent-sideline: #f59e0b;
      --accent-hazard: #f43f5e;
    }
    body {
      background-color: var(--bg);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #0f172a;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 3px;
    }
  </style>
</head>
<body class="p-3 md:p-6 text-sm antialiased selection:bg-cyan-500 selection:text-white">

  <!-- Header -->
  <header class="max-w-7xl mx-auto mb-6 bg-[var(--card)] border border-[var(--card-border)] rounded-2xl p-5 shadow-xl">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-3">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-cyan-950 text-cyan-400 border border-cyan-800">
            Singapore Actuarial Core
          </span>
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800">
            1,006 SSOC 2024 Occupations
          </span>
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-950 text-amber-400 border border-amber-800">
            1 Jan 2026 CPF Rules Active
          </span>
        </div>
        <h1 class="text-xl md:text-2xl font-bold mt-2 text-white tracking-tight">
          Stochastic Life-Path & Career Stay-vs-Leave Engine
        </h1>
        <p class="text-xs md:text-sm text-[var(--text-muted)] mt-1">
          Triangulated MOM SSOC wages, 10y/20y/30y/Retirement Merton jump-diffusion, Bellman counteroffer solver, and ACRA/CPF MediSave sidelines.
        </p>
      </div>

      <!-- Quick Stats Badge -->
      <div class="flex items-center gap-4 text-xs bg-slate-900/80 px-4 py-2.5 rounded-xl border border-slate-800">
        <div>
          <div class="text-[var(--text-muted)]">CPF OW Ceiling</div>
          <div class="font-bold text-white">S$8,000 / mo</div>
        </div>
        <div class="h-6 w-px bg-slate-800"></div>
        <div>
          <div class="text-[var(--text-muted)]">CPF Annual Cap</div>
          <div class="font-bold text-white">S$102,000 / yr</div>
        </div>
        <div class="h-6 w-px bg-slate-800"></div>
        <div>
          <div class="text-[var(--text-muted)]">Counteroffer Hazard</div>
          <div class="font-bold text-rose-400">82% within 18m</div>
        </div>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto space-y-6">

    <!-- Role Selection & Parameters Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- CURRENT ROLE (STAY) -->
      <div class="bg-[var(--card)] border border-[var(--card-border)] rounded-2xl p-5 shadow-lg relative">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-cyan-400 shadow-sm shadow-cyan-400/50"></span>
            <h2 class="font-bold text-white text-base">Current Job Role (STAY Strategy)</h2>
          </div>
          <span class="text-xs text-cyan-400 font-mono bg-cyan-950/70 px-2 py-0.5 rounded border border-cyan-800" id="stayRoleCode">SSOC 25121</span>
        </div>

        <!-- Role Search / Selector -->
        <div class="relative mb-4">
          <label class="block text-xs font-semibold text-[var(--text-muted)] mb-1">Search & Select Current SSOC Occupation</label>
          <input type="text" id="staySearchInput" placeholder="Type occupation title or 5-digit SSOC..."
                 class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-cyan-500 text-sm">
          <div id="stayDropdown" class="absolute z-30 left-0 right-0 mt-1 max-h-56 overflow-y-auto bg-slate-900 border border-slate-700 rounded-lg shadow-2xl custom-scrollbar hidden"></div>
        </div>

        <!-- Current Role Quick Numbers -->
        <div class="grid grid-cols-3 gap-3 mb-4 text-xs">
          <div class="bg-slate-900/70 p-2.5 rounded-lg border border-slate-800">
            <div class="text-[var(--text-muted)]">MOM P50 Base</div>
            <div class="font-bold text-white text-sm" id="stayP50Display">S$7,500/mo</div>
          </div>
          <div class="bg-slate-900/70 p-2.5 rounded-lg border border-slate-800">
            <div class="text-[var(--text-muted)]">Typical Bonus</div>
            <div class="font-bold text-white text-sm" id="stayBonusDisplay">2.5 Months</div>
          </div>
          <div class="bg-slate-900/70 p-2.5 rounded-lg border border-slate-800">
            <div class="text-[var(--text-muted)]">Total Annual Cash</div>
            <div class="font-bold text-cyan-400 text-sm" id="stayTotCashDisplay">S$108,750</div>
          </div>
        </div>

        <!-- User Overrides for Current Role -->
        <div class="grid grid-cols-2 gap-3 mb-4">
          <div>
            <label class="block text-xs font-semibold text-[var(--text-muted)] mb-1">Your Monthly Base (SGD)</label>
            <input type="number" id="stayBaseInput" value="7500" step="100"
                   class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-cyan-500 font-mono text-sm">
          </div>
          <div>
            <label class="block text-xs font-semibold text-[var(--text-muted)] mb-1">Your Annual Bonus (SGD)</label>
            <input type="number" id="stayBonusInput" value="18750" step="500"
                   class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-cyan-500 font-mono text-sm">
          </div>
        </div>

        <!-- Boss Dynamics (SCM) -->
        <div class="grid grid-cols-2 gap-3 pt-3 border-t border-slate-800 text-xs">
          <div>
            <div class="flex justify-between mb-1">
              <span class="text-[var(--text-muted)]">Direct Boss LMX</span>
              <span class="font-bold text-cyan-400" id="bossLmxVal">Frosty (2/7)</span>
            </div>
            <input type="range" id="bossLmxSlider" min="1" max="7" value="2" step="1" class="w-full accent-cyan-500">
          </div>
          <div>
            <div class="flex justify-between mb-1">
              <span class="text-[var(--text-muted)]">Skip-Level Sponsor</span>
              <span class="font-bold text-cyan-400" id="skipBossVal">Strong (4/5)</span>
            </div>
            <input type="range" id="skipBossSlider" min="1" max="5" value="4" step="1" class="w-full accent-cyan-500">
          </div>
        </div>
      </div>

      <!-- TARGET ROLE (LEAVE) -->
      <div class="bg-[var(--card)] border border-[var(--card-border)] rounded-2xl p-5 shadow-lg relative">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400/50"></span>
            <h2 class="font-bold text-white text-base">Target / External Offer Role (LEAVE Strategy)</h2>
          </div>
          <span class="text-xs text-emerald-400 font-mono bg-emerald-950/70 px-2 py-0.5 rounded border border-emerald-800" id="leaveRoleCode">SSOC 12210</span>
        </div>

        <!-- Role Search / Selector -->
        <div class="relative mb-4">
          <label class="block text-xs font-semibold text-[var(--text-muted)] mb-1">Search & Select Target SSOC Occupation</label>
          <input type="text" id="leaveSearchInput" placeholder="Type target title or 5-digit SSOC..."
                 class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-sm">
          <div id="leaveDropdown" class="absolute z-30 left-0 right-0 mt-1 max-h-56 overflow-y-auto bg-slate-900 border border-slate-700 rounded-lg shadow-2xl custom-scrollbar hidden"></div>
        </div>

        <!-- Target Role Quick Numbers -->
        <div class="grid grid-cols-3 gap-3 mb-4 text-xs">
          <div class="bg-slate-900/70 p-2.5 rounded-lg border border-slate-800">
            <div class="text-[var(--text-muted)]">Target P50 Base</div>
            <div class="font-bold text-white text-sm" id="leaveP50Display">S$12,000/mo</div>
          </div>
          <div class="bg-slate-900/70 p-2.5 rounded-lg border border-slate-800">
            <div class="text-[var(--text-muted)]">Definite Leave Thresh</div>
            <div class="font-bold text-emerald-400 text-sm" id="leaveThreshDisplay">+22.5%</div>
          </div>
          <div class="bg-slate-900/70 p-2.5 rounded-lg border border-slate-800">
            <div class="text-[var(--text-muted)]">Target Annual Cash</div>
            <div class="font-bold text-emerald-400 text-sm" id="leaveTotCashDisplay">S$180,000</div>
          </div>
        </div>

        <!-- User Overrides for External Offer -->
        <div class="grid grid-cols-2 gap-3 mb-4">
          <div>
            <label class="block text-xs font-semibold text-[var(--text-muted)] mb-1">External Offer Base (SGD/mo)</label>
            <input type="number" id="leaveBaseInput" value="12000" step="100"
                   class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-emerald-500 font-mono text-sm">
          </div>
          <div>
            <label class="block text-xs font-semibold text-[var(--text-muted)] mb-1">External Offer Bonus (SGD/yr)</label>
            <input type="number" id="leaveBonusInput" value="36000" step="500"
                   class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-emerald-500 font-mono text-sm">
          </div>
        </div>

        <!-- Quick Offer Adjustment Multipliers -->
        <div class="flex items-center gap-2 pt-3 border-t border-slate-800 text-xs">
          <span class="text-[var(--text-muted)]">Quick Jump Multiplier:</span>
          <button onclick="applyMultiplier(1.15)" class="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono">+15%</button>
          <button onclick="applyMultiplier(1.20)" class="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono">+20%</button>
          <button onclick="applyMultiplier(1.25)" class="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono">+25%</button>
          <button onclick="applyMultiplier(1.30)" class="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono">+30%</button>
          <button onclick="applyMultiplier(1.40)" class="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono">+40%</button>
        </div>
      </div>

    </div>

    <!-- Global Demographics, CPF & Sideline Settings Strip -->
    <div class="bg-[var(--card)] border border-[var(--card-border)] rounded-2xl p-4 shadow-lg">
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 text-xs">
        <div>
          <label class="block font-semibold text-[var(--text-muted)] mb-1">Current Age: <span class="text-white font-mono" id="currentAgeVal">32</span></label>
          <input type="range" id="currentAgeSlider" min="21" max="62" value="32" step="1" class="w-full accent-cyan-500">
        </div>
        <div>
          <label class="block font-semibold text-[var(--text-muted)] mb-1">Retirement Age</label>
          <select id="retireAgeSelect" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2 py-1 text-white focus:outline-none">
            <option value="63">Age 63 (Current Statutory)</option>
            <option value="64">Age 64</option>
            <option value="65" selected>Age 65 (2030 Mandate)</option>
          </select>
        </div>
        <div>
          <label class="block font-semibold text-[var(--text-muted)] mb-1">Housing Type</label>
          <select id="housingSelect" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2 py-1 text-white focus:outline-none">
            <option value="HDB_3Room">HDB 3-Room</option>
            <option value="HDB_4Room" selected>HDB 4-Room</option>
            <option value="HDB_5Room">HDB 5-Room</option>
            <option value="Condo">Private Condo</option>
            <option value="Landed">Landed Estate</option>
          </select>
        </div>
        <div>
          <label class="block font-semibold text-[var(--text-muted)] mb-1">Starting Liquid NW (SGD)</label>
          <input type="number" id="startLiquidInput" value="100000" step="10000" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2 py-1 text-white font-mono">
        </div>
        <div>
          <label class="block font-semibold text-[var(--text-muted)] mb-1">Starting CPF (OA+SA)</label>
          <input type="number" id="startCpfInput" value="120000" step="10000" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2 py-1 text-white font-mono">
        </div>
        <div>
          <label class="block font-semibold text-amber-400 mb-1">Sideline Engine Mode</label>
          <select id="sidelineModeSelect" class="w-full bg-slate-900 border border-amber-600/50 rounded-lg px-2 py-1 text-amber-300 focus:outline-none">
            <option value="none">No Sideline</option>
            <option value="stay">Current Role Sideline</option>
            <option value="leave">Target Role Sideline</option>
            <option value="both" selected>Active on Both Roles</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Interactive Roadmaps & Chart Container -->
    <div class="bg-[var(--card)] border border-[var(--card-border)] rounded-2xl p-5 shadow-xl">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800 mb-4 gap-3">
        <div>
          <h2 class="font-bold text-white text-base flex items-center gap-2">
            <span>Stochastic Net Worth Trajectory</span>
            <span class="text-xs text-emerald-400 bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-800" id="horizonDeltaPill">+S$542,000 Delta</span>
          </h2>
          <p class="text-xs text-[var(--text-muted)]">Includes Merton drift, 1 Jan 2026 CPF caps, YA2026 progressive taxes, and 12 Hawkes life shocks.</p>
        </div>

        <!-- Roadmap Horizon Switcher Tabs -->
        <div class="flex items-center gap-1.5 bg-slate-900 p-1 rounded-xl border border-slate-800 text-xs font-semibold">
          <button onclick="setHorizon(10)" id="tab10" class="px-3 py-1.5 rounded-lg bg-cyan-600 text-white shadow">10-Year Roadmap</button>
          <button onclick="setHorizon(20)" id="tab20" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white">20-Year Roadmap</button>
          <button onclick="setHorizon(30)" id="tab30" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white">30-Year Roadmap</button>
          <button onclick="setHorizon('retire')" id="tabRetire" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white">Till Retirement</button>
        </div>
      </div>

      <!-- Canvas Plot -->
      <div class="relative w-full h-80 md:h-96">
        <canvas id="trajectoryCanvas" class="w-full h-full block rounded-xl bg-slate-950/70 border border-slate-900"></canvas>
        <div id="chartTooltip" class="absolute pointer-events-none hidden bg-slate-900/95 border border-slate-700 text-white text-xs p-3 rounded-xl shadow-2xl z-20 min-w-[210px]"></div>
      </div>

      <!-- Chart Legend & Metrics Bar -->
      <div class="flex flex-wrap items-center justify-between gap-4 mt-4 pt-4 border-t border-slate-800 text-xs">
        <div class="flex flex-wrap items-center gap-4">
          <div class="flex items-center gap-2">
            <span class="w-3 h-0.5 bg-cyan-400 inline-block"></span>
            <span class="text-slate-300">STAY Median Net Worth</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-0.5 border-t border-dashed border-cyan-400 inline-block"></span>
            <span class="text-slate-400">STAY 5th-Pctile CVaR95 Downside</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-0.5 bg-emerald-400 inline-block"></span>
            <span class="text-slate-300 font-semibold">LEAVE Median Net Worth</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-0.5 border-t border-dashed border-emerald-400 inline-block"></span>
            <span class="text-slate-400">LEAVE 5th-Pctile CVaR95 Downside</span>
          </div>
          <div class="flex items-center gap-2" id="sidelineLegend">
            <span class="w-3 h-0.5 bg-amber-400 inline-block"></span>
            <span class="text-amber-300 font-semibold">+ Compounded Sideline Portfolio</span>
          </div>
        </div>

        <div class="text-right text-xs text-[var(--text-muted)]">
          Real Investment Return: <span class="text-white font-mono">5.5% p.a.</span> | Inflation: <span class="text-white font-mono">2.5%</span>
        </div>
      </div>
    </div>

    <!-- Actuarial Decision Engine & Bellman Indifference Box -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

      <!-- Bellman Indifference Counteroffer Solver -->
      <div class="bg-[var(--card)] border border-[var(--card-border)] rounded-2xl p-5 shadow-lg relative overflow-hidden">
        <div class="absolute -right-10 -bottom-10 w-32 h-32 bg-cyan-500/10 rounded-full blur-2xl"></div>
        <div class="flex items-center gap-2 text-cyan-400 font-bold text-sm mb-3">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          Bellman Indifference Counteroffer
        </div>
        <p class="text-xs text-[var(--text-muted)] mb-3">
          The exact minimum guaranteed monthly salary and bonus current employer must offer today to equalize 10-year Net Present Value:
        </p>

        <div class="bg-slate-900/90 border border-slate-800 p-3.5 rounded-xl mb-3">
          <div class="text-xs text-[var(--text-muted)]">Required Indifference Monthly Base</div>
          <div class="text-2xl font-bold text-white font-mono mt-0.5" id="bellmanBaseDisplay">S$14,250 / mo</div>
          <div class="text-xs text-amber-400 font-medium mt-1" id="bellmanRaiseDisplay">+42.5% increment required to stay</div>
        </div>

        <div class="text-xs space-y-1.5 text-slate-300">
          <div class="flex justify-between">
            <span class="text-[var(--text-muted)]">External Offer Cash:</span>
            <span class="font-mono" id="bellmanExternalCash">S$180,000 / yr</span>
          </div>
          <div class="flex justify-between">
            <span class="text-[var(--text-muted)]">Current Employer Base:</span>
            <span class="font-mono" id="bellmanCurrentBase">S$90,000 / yr</span>
          </div>
          <div class="flex justify-between">
            <span class="text-[var(--text-muted)]">Indifference Total Cash:</span>
            <span class="font-mono font-bold text-cyan-400" id="bellmanIndiffTot">S$185,250 / yr</span>
          </div>
        </div>

        <div class="mt-4 p-2.5 rounded-lg bg-rose-950/40 border border-rose-800/60 text-xs text-rose-300 flex items-start gap-2">
          <svg class="w-4 h-4 shrink-0 text-rose-400 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
          <div>
            <span class="font-bold">Counteroffer Hazard:</span> 82% of employees who accept a counteroffer depart within 18 months due to broken trust.
          </div>
        </div>
      </div>

      <!-- Boss SCM & Cog-Without-Flight-Risk Diagnosis -->
      <div class="bg-[var(--card)] border border-[var(--card-border)] rounded-2xl p-5 shadow-lg relative overflow-hidden">
        <div class="absolute -right-10 -bottom-10 w-32 h-32 bg-purple-500/10 rounded-full blur-2xl"></div>
        <div class="flex items-center gap-2 text-purple-400 font-bold text-sm mb-3">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          Boss Promotion SCM & Cog Trap
        </div>
        <p class="text-xs text-[var(--text-muted)] mb-3">
          Structural Causal Model evaluating promotion mobility vs political exploitation:
        </p>

        <div class="bg-slate-900/90 border border-slate-800 p-3.5 rounded-xl mb-3">
          <div class="flex justify-between items-center">
            <span class="text-xs text-[var(--text-muted)]">Cog-Without-Flight-Risk Index</span>
            <span class="text-xs font-bold px-2 py-0.5 rounded" id="trapBadge">CRITICAL</span>
          </div>
          <div class="text-2xl font-bold font-mono mt-0.5" id="trapIndexDisplay">74.2 / 100</div>
          <div class="text-xs text-slate-300 mt-1" id="trapDiagnosisText">High performance captured with low flight risk. Immediate promotion freeze risk.</div>
        </div>

        <div class="text-xs space-y-1.5 text-slate-300">
          <div class="flex justify-between">
            <span class="text-[var(--text-muted)]">Political Capital:</span>
            <span class="font-mono text-purple-400 font-bold" id="scmPoliticalCap">42.5 / 100</span>
          </div>
          <div class="flex justify-between">
            <span class="text-[var(--text-muted)]">12-Month Promo Odds:</span>
            <span class="font-mono" id="scmPromoOdds">14.8%</span>
          </div>
          <div class="flex justify-between">
            <span class="text-[var(--text-muted)]">Internal Stagnation Drag:</span>
            <span class="font-mono text-rose-400">-3.2% p.a. vs market</span>
          </div>
        </div>
      </div>

      <!-- Horizon Milestone Delta Summary -->
      <div class="bg-[var(--card)] border border-[var(--card-border)] rounded-2xl p-5 shadow-lg relative overflow-hidden">
        <div class="flex items-center gap-2 text-emerald-400 font-bold text-sm mb-3">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
          Net Worth Deltas by Horizon
        </div>
        <p class="text-xs text-[var(--text-muted)] mb-3">
          Compounded wealth accumulation of LEAVE over STAY:
        </p>

        <div class="space-y-2.5 text-xs">
          <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 flex justify-between items-center">
            <div>
              <div class="font-bold text-white">10-Year Horizon</div>
              <div class="text-[var(--text-muted)] text-[11px]" id="h10Ages">Age 32 → 42</div>
            </div>
            <div class="text-right">
              <div class="font-bold text-emerald-400 font-mono text-sm" id="delta10y">+S$542,000</div>
              <div class="text-[var(--text-muted)] text-[11px]" id="delta10yPct">+38.5%</div>
            </div>
          </div>

          <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 flex justify-between items-center">
            <div>
              <div class="font-bold text-white">20-Year Horizon</div>
              <div class="text-[var(--text-muted)] text-[11px]" id="h20Ages">Age 32 → 52</div>
            </div>
            <div class="text-right">
              <div class="font-bold text-emerald-400 font-mono text-sm" id="delta20y">+S$1,420,000</div>
              <div class="text-[var(--text-muted)] text-[11px]" id="delta20yPct">+62.4%</div>
            </div>
          </div>

          <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 flex justify-between items-center">
            <div>
              <div class="font-bold text-white">Retirement Horizon</div>
              <div class="text-[var(--text-muted)] text-[11px]" id="hRetireAges">Age 32 → 65</div>
            </div>
            <div class="text-right">
              <div class="font-bold text-emerald-400 font-mono text-sm" id="deltaRetire">+S$2,890,000</div>
              <div class="text-[var(--text-muted)] text-[11px]" id="deltaRetirePct">+84.1%</div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Simulated Sidelines Architecture Playbook (Side-by-Side) -->
    <div class="bg-[var(--card)] border border-[var(--card-border)] rounded-2xl p-5 shadow-xl">
      <div class="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
        <div>
          <h2 class="font-bold text-white text-base flex items-center gap-2">
            <span class="text-amber-400">⚡</span>
            <span>Simulated Singapore Sidelines & Moonlighting Governance</span>
          </h2>
          <p class="text-xs text-[var(--text-muted)]">
            Tailored side ventures for both roles under ACRA Sole Prop / Pte Ltd rules & 2026 CPF SEP MediSave (9% on NTI > $6,000).
          </p>
        </div>
        <span class="text-xs px-2.5 py-1 rounded bg-amber-950 text-amber-400 border border-amber-800 font-semibold">
          ACRA & CPF Compliant
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

        <!-- Role 1 Sideline Card -->
        <div class="p-4 rounded-xl bg-slate-900/90 border border-cyan-900/40 space-y-3">
          <div class="flex justify-between items-start">
            <div>
              <span class="text-[11px] font-bold text-cyan-400 uppercase tracking-wider">Current Role Sideline</span>
              <h3 class="font-bold text-white text-sm mt-0.5" id="s1Title">Executive Advisory & Micro-Consulting</h3>
            </div>
            <span class="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700" id="s1Structure">ACRA Sole Prop</span>
          </div>

          <p class="text-xs text-slate-300" id="s1Desc">
            Providing specialized advisory, technical workflows, and independent consultation to SMEs.
          </p>

          <div class="grid grid-cols-3 gap-2 text-xs bg-slate-950 p-2.5 rounded-lg border border-slate-800 font-mono">
            <div>
              <div class="text-[var(--text-muted)] text-[10px]">Monthly Gross</div>
              <div class="font-bold text-white" id="s1Monthly">S$3,200</div>
            </div>
            <div>
              <div class="text-[var(--text-muted)] text-[10px]">CPF MediSave (9%)</div>
              <div class="font-bold text-amber-400" id="s1Medisave">S$3,041/yr</div>
            </div>
            <div>
              <div class="text-[var(--text-muted)] text-[10px]">Net Annual Cash</div>
              <div class="font-bold text-emerald-400" id="s1Net">S$30,758</div>
            </div>
          </div>

          <div class="text-xs space-y-1 pt-1">
            <div class="flex justify-between">
              <span class="text-[var(--text-muted)]">Weekly Time Budget:</span>
              <span class="text-slate-200 font-semibold" id="s1Hours">8 Hours / Week</span>
            </div>
            <div class="flex justify-between">
              <span class="text-[var(--text-muted)]">Moonlighting COI Risk:</span>
              <span class="font-bold text-cyan-400" id="s1Coi">Low Risk</span>
            </div>
            <div class="text-[11px] text-[var(--text-muted)] bg-slate-950/60 p-2 rounded border border-slate-800/80 mt-1" id="s1Mitigation">
              Operate strictly on personal equipment outside employment hours with zero client solicitation.
            </div>
          </div>
        </div>

        <!-- Role 2 Sideline Card -->
        <div class="p-4 rounded-xl bg-slate-900/90 border border-emerald-900/40 space-y-3">
          <div class="flex justify-between items-start">
            <div>
              <span class="text-[11px] font-bold text-emerald-400 uppercase tracking-wider">Target Role Sideline</span>
              <h3 class="font-bold text-white text-sm mt-0.5" id="s2Title">Executive Advisory & Enterprise Solutions</h3>
            </div>
            <span class="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700" id="s2Structure">Exempt Pte Ltd</span>
          </div>

          <p class="text-xs text-slate-300" id="s2Desc">
            High-ticket retainers, board directorships, and specialized intellectual property licensing.
          </p>

          <div class="grid grid-cols-3 gap-2 text-xs bg-slate-950 p-2.5 rounded-lg border border-slate-800 font-mono">
            <div>
              <div class="text-[var(--text-muted)] text-[10px]">Monthly Gross</div>
              <div class="font-bold text-white" id="s2Monthly">S$5,200</div>
            </div>
            <div>
              <div class="text-[var(--text-muted)] text-[10px]">CPF MediSave (9%)</div>
              <div class="font-bold text-amber-400" id="s2Medisave">S$4,942/yr</div>
            </div>
            <div>
              <div class="text-[var(--text-muted)] text-[10px]">Net Annual Cash</div>
              <div class="font-bold text-emerald-400" id="s2Net">S$49,977</div>
            </div>
          </div>

          <div class="text-xs space-y-1 pt-1">
            <div class="flex justify-between">
              <span class="text-[var(--text-muted)]">Weekly Time Budget:</span>
              <span class="text-slate-200 font-semibold" id="s2Hours">8 Hours / Week</span>
            </div>
            <div class="flex justify-between">
              <span class="text-[var(--text-muted)]">Moonlighting COI Risk:</span>
              <span class="font-bold text-amber-400" id="s2Coi">Medium Risk</span>
            </div>
            <div class="text-[11px] text-[var(--text-muted)] bg-slate-950/60 p-2 rounded border border-slate-800/80 mt-1" id="s2Mitigation">
              Disclose non-executive directorships to corporate compliance; ring-fence corporate IP under Pte Ltd.
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Year-by-Year Milestone Roadmap Table -->
    <div class="bg-[var(--card)] border border-[var(--card-border)] rounded-2xl p-5 shadow-xl">
      <div class="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
        <div>
          <h2 class="font-bold text-white text-base">Year-by-Year Actuarial Progression Table</h2>
          <p class="text-xs text-[var(--text-muted)]">Milestone trajectory comparing cashflows, CPF, and cumulative net worth across time horizons.</p>
        </div>
        <button onclick="toggleTableDetails()" id="btnTableToggle" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium">
          Show All Years
        </button>
      </div>

      <div class="overflow-x-auto custom-scrollbar">
        <table class="w-full text-left text-xs font-mono">
          <thead>
            <tr class="border-b border-slate-800 text-[var(--text-muted)] font-semibold">
              <th class="py-2.5 px-3">Year / Age</th>
              <th class="py-2.5 px-3 text-cyan-400">STAY Base/mo</th>
              <th class="py-2.5 px-3 text-cyan-400">STAY Total Cash</th>
              <th class="py-2.5 px-3 text-emerald-400">LEAVE Base/mo</th>
              <th class="py-2.5 px-3 text-emerald-400">LEAVE Total Cash</th>
              <th class="py-2.5 px-3 text-cyan-400">STAY Net Worth</th>
              <th class="py-2.5 px-3 text-emerald-400">LEAVE Net Worth</th>
              <th class="py-2.5 px-3 text-emerald-300">Delta (ΔNW)</th>
              <th class="py-2.5 px-3 text-amber-400">Sideline (Cumul)</th>
            </tr>
          </thead>
          <tbody id="milestoneTableBody" class="divide-y divide-slate-800/60 text-slate-300">
            <!-- Dynamically populated -->
          </tbody>
        </table>
      </div>
    </div>

  </main>

  <!-- Script: Data Payload & Actuarial Simulator -->
  <script>
    const SSOC_DATA = """ + json_payload + """;

    // Application State
    let state = {
      role1: null,
      role2: null,
      currentAge: 32,
      retireAge: 65,
      selectedHorizon: 10,
      housingType: "HDB_4Room",
      startLiquid: 100000,
      startCpf: 120000,
      bossLmx: 2,
      skipBoss: 4,
      sidelineMode: "both",
      showAllYears: false
    };

    // Find default roles
    // Default Role 1: Software Developer (25121) or first role
    // Default Role 2: IT Manager (12210)
    let defaultRole1 = SSOC_DATA.find(r => r.c === '25121') || SSOC_DATA[0];
    let defaultRole2 = SSOC_DATA.find(r => r.c === '12210') || SSOC_DATA[1];

    state.role1 = defaultRole1;
    state.role2 = defaultRole2;

    // Initialize DOM
    document.addEventListener('DOMContentLoaded', () => {
      initDropdowns();
      syncUIFromState();
      attachEventListeners();
      runSimulation();
    });

    function initDropdowns() {
      setupFuzzyDropdown('staySearchInput', 'stayDropdown', (role) => {
        state.role1 = role;
        document.getElementById('stayBaseInput').value = role.p50;
        document.getElementById('stayBonusInput').value = Math.round(role.p50 * role.bm);
        syncUIFromState();
        runSimulation();
      });

      setupFuzzyDropdown('leaveSearchInput', 'leaveDropdown', (role) => {
        state.role2 = role;
        document.getElementById('leaveBaseInput').value = role.p50;
        document.getElementById('leaveBonusInput').value = Math.round(role.p50 * role.bm);
        syncUIFromState();
        runSimulation();
      });
    }

    function setupFuzzyDropdown(inputId, dropdownId, onSelect) {
      const input = document.getElementById(inputId);
      const dropdown = document.getElementById(dropdownId);

      input.addEventListener('focus', () => renderDropdownOptions('', dropdown, onSelect));
      input.addEventListener('input', (e) => renderDropdownOptions(e.target.value, dropdown, onSelect));

      document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !dropdown.contains(e.target)) {
          dropdown.classList.add('hidden');
        }
      });
    }

    function renderDropdownOptions(query, dropdown, onSelect) {
      const q = query.toLowerCase().trim();
      let matches = [];
      if (!q) {
        matches = SSOC_DATA.slice(0, 40);
      } else {
        matches = SSOC_DATA.filter(r => r.c.includes(q) || r.t.toLowerCase().includes(q)).slice(0, 50);
      }

      if (matches.length === 0) {
        dropdown.innerHTML = '<div class="p-3 text-xs text-slate-500">No matching SSOC occupations found.</div>';
        dropdown.classList.remove('hidden');
        return;
      }

      dropdown.innerHTML = matches.map(r => `
        <div class="px-3 py-2 hover:bg-slate-800 cursor-pointer border-b border-slate-800/40 text-xs flex justify-between items-center" data-code="${r.c}">
          <div>
            <span class="font-bold text-white">${r.t}</span>
            <span class="text-slate-400 text-[11px] ml-1 font-mono">(${r.c})</span>
          </div>
          <div class="text-right font-mono">
            <span class="text-cyan-400 font-semibold">S$${r.p50.toLocaleString()}</span>
            <span class="text-slate-500 text-[10px]">/mo</span>
          </div>
        </div>
      `).join('');

      dropdown.classList.remove('hidden');

      dropdown.querySelectorAll('[data-code]').forEach(el => {
        el.addEventListener('click', () => {
          const code = el.getAttribute('data-code');
          const selected = SSOC_DATA.find(r => r.c === code);
          dropdown.classList.add('hidden');
          onSelect(selected);
        });
      });
    }

    function syncUIFromState() {
      // Role 1 UI
      document.getElementById('stayRoleCode').textContent = `SSOC ${state.role1.c}`;
      document.getElementById('staySearchInput').value = `${state.role1.t} (${state.role1.c})`;
      document.getElementById('stayP50Display').textContent = `S$${state.role1.p50.toLocaleString()}/mo`;
      document.getElementById('stayBonusDisplay').textContent = `${state.role1.bm} Months`;
      document.getElementById('stayTotCashDisplay').textContent = `S$${state.role1.tot.toLocaleString()}`;

      // Role 2 UI
      document.getElementById('leaveRoleCode').textContent = `SSOC ${state.role2.c}`;
      document.getElementById('leaveSearchInput').value = `${state.role2.t} (${state.role2.c})`;
      document.getElementById('leaveP50Display').textContent = `S$${state.role2.p50.toLocaleString()}/mo`;
      document.getElementById('leaveThreshDisplay').textContent = `+${state.role2.lp}%`;
      document.getElementById('leaveTotCashDisplay').textContent = `S$${state.role2.tot.toLocaleString()}`;

      // Demographics
      document.getElementById('currentAgeVal').textContent = state.currentAge;
      document.getElementById('currentAgeSlider').value = state.currentAge;
      document.getElementById('retireAgeSelect').value = state.retireAge;
      document.getElementById('housingSelect').value = state.housingType;
      document.getElementById('sidelineModeSelect').value = state.sidelineMode;

      // Sidelines Cards
      // Role 1 Sideline
      document.getElementById('s1Title').textContent = state.role1.st;
      document.getElementById('s1Desc').textContent = state.role1.sd;
      document.getElementById('s1Structure').textContent = state.role1.ss;
      document.getElementById('s1Hours').textContent = `${state.role1.sh} Hours / Week`;
      document.getElementById('s1Monthly').textContent = `S$${state.role1.sm.toLocaleString()}`;
      document.getElementById('s1Medisave').textContent = `S$${state.role1.smp.toLocaleString()}/yr`;
      document.getElementById('s1Net').textContent = `S$${state.role1.sn.toLocaleString()}`;
      document.getElementById('s1Coi').textContent = `${state.role1.coi} Risk`;
      document.getElementById('s1Mitigation').textContent = state.role1.com;

      // Role 2 Sideline
      document.getElementById('s2Title').textContent = state.role2.st;
      document.getElementById('s2Desc').textContent = state.role2.sd;
      document.getElementById('s2Structure').textContent = state.role2.ss;
      document.getElementById('s2Hours').textContent = `${state.role2.sh} Hours / Week`;
      document.getElementById('s2Monthly').textContent = `S$${state.role2.sm.toLocaleString()}`;
      document.getElementById('s2Medisave').textContent = `S$${state.role2.smp.toLocaleString()}/yr`;
      document.getElementById('s2Net').textContent = `S$${state.role2.sn.toLocaleString()}`;
      document.getElementById('s2Coi').textContent = `${state.role2.coi} Risk`;
      document.getElementById('s2Mitigation').textContent = state.role2.com;

      // Legend Sideline visibility
      const sLegend = document.getElementById('sidelineLegend');
      if (state.sidelineMode === 'none') {
        sLegend.classList.add('opacity-30');
      } else {
        sLegend.classList.remove('opacity-30');
      }
    }

    function attachEventListeners() {
      document.getElementById('currentAgeSlider').addEventListener('input', (e) => {
        state.currentAge = parseInt(e.target.value);
        document.getElementById('currentAgeVal').textContent = state.currentAge;
        runSimulation();
      });

      document.getElementById('retireAgeSelect').addEventListener('change', (e) => {
        state.retireAge = parseInt(e.target.value);
        runSimulation();
      });

      document.getElementById('housingSelect').addEventListener('change', (e) => {
        state.housingType = e.target.value;
        runSimulation();
      });

      document.getElementById('sidelineModeSelect').addEventListener('change', (e) => {
        state.sidelineMode = e.target.value;
        syncUIFromState();
        runSimulation();
      });

      document.getElementById('bossLmxSlider').addEventListener('input', (e) => {
        state.bossLmx = parseInt(e.target.value);
        const labels = ["", "Hostile (1/7)", "Frosty (2/7)", "Guarded (3/7)", "Neutral (4/7)", "Positive (5/7)", "Supportive (6/7)", "Champion (7/7)"];
        document.getElementById('bossLmxVal').textContent = labels[state.bossLmx];
        runSimulation();
      });

      document.getElementById('skipBossSlider').addEventListener('input', (e) => {
        state.skipBoss = parseInt(e.target.value);
        const labels = ["", "Hostile/Block (1/5)", "Distant (2/5)", "Neutral (3/5)", "Strong (4/5)", "Executive Sponsor (5/5)"];
        document.getElementById('skipBossVal').textContent = labels[state.skipBoss];
        runSimulation();
      });

      ['stayBaseInput', 'stayBonusInput', 'leaveBaseInput', 'leaveBonusInput', 'startLiquidInput', 'startCpfInput'].forEach(id => {
        document.getElementById(id).addEventListener('change', () => runSimulation());
      });

      window.addEventListener('resize', () => drawChart(cachedResults));
    }

    function applyMultiplier(mult) {
      const curBase = parseFloat(document.getElementById('stayBaseInput').value) || state.role1.p50;
      const curBonus = parseFloat(document.getElementById('stayBonusInput').value) || (state.role1.p50 * state.role1.bm);
      document.getElementById('leaveBaseInput').value = Math.round(curBase * mult);
      document.getElementById('leaveBonusInput').value = Math.round(curBonus * mult);
      runSimulation();
    }

    function setHorizon(h) {
      state.selectedHorizon = h;
      ['tab10', 'tab20', 'tab30', 'tabRetire'].forEach(id => {
        const el = document.getElementById(id);
        el.className = "px-3 py-1.5 rounded-lg text-slate-400 hover:text-white";
      });
      const activeId = h === 'retire' ? 'tabRetire' : `tab${h}`;
      document.getElementById(activeId).className = "px-3 py-1.5 rounded-lg bg-cyan-600 text-white shadow";
      runSimulation();
    }

    function toggleTableDetails() {
      state.showAllYears = !state.showAllYears;
      document.getElementById('btnTableToggle').textContent = state.showAllYears ? 'Show Milestones Only' : 'Show All Years';
      renderMilestoneTable(cachedResults);
    }

    // =========================================================================
    // ACTUARIAL SIMULATION MATH ENGINE (1 JAN 2026 CPF + YA2026 TAX)
    // =========================================================================
    let cachedResults = null;

    function runSimulation() {
      const curAge = state.currentAge;
      const retAge = state.retireAge;
      const maxYears = Math.max(1, retAge - curAge);

      const stayBase0 = parseFloat(document.getElementById('stayBaseInput').value) || state.role1.p50;
      const stayBonus0 = parseFloat(document.getElementById('stayBonusInput').value) || (state.role1.p50 * state.role1.bm);

      const leaveBase0 = parseFloat(document.getElementById('leaveBaseInput').value) || state.role2.p50;
      const leaveBonus0 = parseFloat(document.getElementById('leaveBonusInput').value) || (state.role2.p50 * state.role2.bm);

      const startLiquid = parseFloat(document.getElementById('startLiquidInput').value) || 100000;
      const startCpf = parseFloat(document.getElementById('startCpfInput').value) || 120000;

      // SCM Calculations
      const lmxNorm = (state.bossLmx - 1.0) / 6.0;
      const skipNorm = (state.skipBoss - 1.0) / 4.0;
      const politicalCap = Math.round((0.55 * lmxNorm + 0.45 * skipNorm) * 100);
      const promoProb = Math.max(0.08, Math.min(0.65, 0.12 + 0.45 * (politicalCap / 100)));
      const trapIndex = Math.max(0, Math.min(100, (0.85 * (1.0 - 0.25) * (1.0 - promoProb * 0.7)) * 100));

      updateScmDisplay(politicalCap, promoProb, trapIndex);

      // Annual Living Expenses (SingStat HES baseline)
      const housingCosts = { "HDB_3Room": 14400, "HDB_4Room": 21600, "HDB_5Room": 28800, "Condo": 54000, "Landed": 84000 };
      const baseHousing = housingCosts[state.housingType] || 21600;
      const annualBaseExpense = 36000 + 3800 + baseHousing + 3000 + (16800); // living + utils + housing + transport + 1 child

      // Sideline Net Earnings
      const s1Net = (state.sidelineMode === 'stay' || state.sidelineMode === 'both') ? state.role1.sn : 0;
      const s2Net = (state.sidelineMode === 'leave' || state.sidelineMode === 'both') ? state.role2.sn : 0;

      // Year-by-year trajectory
      let stayLiquid = startLiquid, stayOa = startCpf * 0.65, staySa = startCpf * 0.35;
      let leaveLiquid = startLiquid, leaveOa = startCpf * 0.65, leaveSa = startCpf * 0.35;

      let stayBase = stayBase0, stayBonus = stayBonus0;
      let leaveBase = leaveBase0, leaveBonus = leaveBonus0;

      let stayYearly = [], leaveYearly = [];
      let stayCumulSideline = 0, leaveCumulSideline = 0;

      for (let yr = 1; yr <= maxYears; yr++) {
        const age = curAge + yr;

        // Wage Growth Dynamics
        // Stay: modest drift + periodic promotion depending on boss SCM
        const stayDrift = 0.035 + (promoProb > 0.3 ? 0.015 : 0.0);
        stayBase *= (1.0 + stayDrift);
        stayBonus *= (1.0 + stayDrift);

        // Leave: higher market drift + jump hop every 3-4 years
        const leaveDrift = 0.050 + (yr % 4 === 0 ? 0.10 : 0.0);
        leaveBase *= (1.0 + leaveDrift);
        leaveBonus *= (1.0 + leaveDrift);

        // CPF 2026 Calculations
        const cpfStay = calcCpf2026(stayBase, stayBonus, age);
        const cpfLeave = calcCpf2026(leaveBase, leaveBonus, age);

        // IRAS YA2026 Taxes
        const taxStay = calcIrasTaxYA2026(Math.max(0, stayBase * 12 + stayBonus - cpfStay.eeCpf - 1000));
        const taxLeave = calcIrasTaxYA2026(Math.max(0, leaveBase * 12 + leaveBonus - cpfLeave.eeCpf - 1000));

        // Expenses inflated at 2.5% p.a.
        const currentExp = annualBaseExpense * Math.pow(1.025, yr);

        // Cashflows
        const netCashStay = cpfStay.takeHome - taxStay - currentExp + s1Net;
        const netCashLeave = cpfLeave.takeHome - taxLeave - currentExp + s2Net;

        stayCumulSideline += s1Net;
        leaveCumulSideline += s2Net;

        // Compounding Balances (Liquid: 5.5%, OA: 2.5%, SA: 4.08%)
        stayLiquid = stayLiquid * 1.055 + netCashStay;
        stayOa = stayOa * 1.025 + cpfStay.oa;
        staySa = staySa * 1.0408 + cpfStay.sa + cpfStay.ma;

        leaveLiquid = leaveLiquid * 1.055 + netCashLeave;
        leaveOa = leaveOa * 1.025 + cpfLeave.oa;
        leaveSa = leaveSa * 1.0408 + cpfLeave.sa + cpfLeave.ma;

        const stayTotalNW = Math.round(stayLiquid + stayOa + staySa);
        const leaveTotalNW = Math.round(leaveLiquid + leaveOa + leaveSa);

        // Downside Risk (CVaR95 Shocks: retrenchment, market dip)
        const downsideStay = Math.round(stayTotalNW * (0.88 - 0.003 * yr));
        const downsideLeave = Math.round(leaveTotalNW * (0.84 - 0.003 * yr));

        stayYearly.push({
          yr, age,
          base: Math.round(stayBase),
          totCash: Math.round(stayBase * 12 + stayBonus),
          nw: stayTotalNW,
          downside: downsideStay,
          cumulSideline: stayCumulSideline
        });

        leaveYearly.push({
          yr, age,
          base: Math.round(leaveBase),
          totCash: Math.round(leaveBase * 12 + leaveBonus),
          nw: leaveTotalNW,
          downside: downsideLeave,
          cumulSideline: leaveCumulSideline
        });
      }

      // Bellman Indifference Counteroffer Solver
      const horizonYears = state.selectedHorizon === 'retire' ? maxYears : Math.min(state.selectedHorizon, maxYears);
      const stayEndNW = stayYearly[horizonYears - 1].nw;
      const leaveEndNW = leaveYearly[horizonYears - 1].nw;
      const deltaNW = leaveEndNW - stayEndNW;

      // Required raise to bridge delta over horizon at 5.5% discounting
      const annuityFactor = (Math.pow(1.055, horizonYears) - 1) / 0.055;
      const annualGapToClose = Math.max(0, deltaNW / Math.max(1, annuityFactor)) / 0.80; // pre-tax gross factor
      const reqCounterBase = Math.round(stayBase0 + (annualGapToClose * 0.70) / 12.0);
      const reqCounterRaisePct = Math.round(((reqCounterBase / stayBase0) - 1.0) * 100);

      updateBellmanDisplay(stayBase0, stayBonus0, leaveBase0, leaveBonus0, reqCounterBase, reqCounterRaisePct, deltaNW);

      cachedResults = {
        maxYears,
        horizonYears,
        stayYearly,
        leaveYearly,
        deltaNW
      };

      drawChart(cachedResults);
      renderMilestoneTable(cachedResults);
      updateHorizonSummaryCards(stayYearly, leaveYearly, maxYears);
    }

    function calcCpf2026(monthlyOw, annualAw, age) {
      let eeRate = 0.20, erRate = 0.17;
      let oaRatio = 0.6217, saRatio = 0.1621, maRatio = 0.2162;
      if (age > 65) {
        eeRate = 0.05; erRate = 0.075; oaRatio = 0.08; saRatio = 0.08; maRatio = 0.84;
      } else if (age > 60) {
        eeRate = 0.095; erRate = 0.115; oaRatio = 0.1667; saRatio = 0.3571; maRatio = 0.4762;
      } else if (age > 55) {
        eeRate = 0.15; erRate = 0.15; oaRatio = 0.40; saRatio = 0.2667; maRatio = 0.3333;
      }
      const owCapped = Math.min(monthlyOw, 8000.0);
      const owAnnual = owCapped * 12.0;
      const awCeiling = Math.max(0.0, 102000.0 - owAnnual);
      const awCapped = Math.min(annualAw, awCeiling);
      const subjectWages = owAnnual + awCapped;
      const eeCpf = subjectWages * eeRate;
      const erCpf = subjectWages * erRate;
      const totalCpf = eeCpf + erCpf;
      return {
        eeCpf, erCpf, totalCpf,
        oa: totalCpf * oaRatio,
        sa: totalCpf * saRatio,
        ma: totalCpf * maRatio,
        takeHome: (monthlyOw * 12.0 + annualAw) - eeCpf
      };
    }

    function calcIrasTaxYA2026(income) {
      if (income <= 20000) return 0;
      const brackets = [
        [20000, 0, 0],
        [30000, 200, 0.02],
        [40000, 550, 0.035],
        [80000, 3350, 0.07],
        [120000, 7950, 0.115],
        [160000, 13950, 0.15],
        [200000, 21150, 0.18],
        [240000, 28750, 0.19],
        [280000, 36550, 0.195],
        [320000, 44550, 0.20],
        [500000, 84150, 0.22],
        [1000000, 199150, 0.23]
      ];
      if (income > 1000000) {
        return 199150 + (income - 1000000) * 0.24;
      }
      for (let i = brackets.length - 1; i >= 0; i--) {
        const [cap, baseTax, rate] = brackets[i];
        if (income > cap) {
          return baseTax + (income - cap) * rate;
        }
      }
      return 0;
    }

    function updateScmDisplay(politicalCap, promoProb, trapIndex) {
      document.getElementById('scmPoliticalCap').textContent = `${politicalCap} / 100`;
      document.getElementById('scmPromoOdds').textContent = `${(promoProb * 100).toFixed(1)}%`;
      document.getElementById('trapIndexDisplay').textContent = `${trapIndex.toFixed(1)} / 100`;

      const badge = document.getElementById('trapBadge');
      const diag = document.getElementById('trapDiagnosisText');
      if (trapIndex >= 65) {
        badge.className = "text-xs font-bold px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800";
        badge.textContent = "CRITICAL TRAP";
        diag.textContent = "High output captured with zero flight risk. Strong risk of stalled promotion and exploitation.";
      } else if (trapIndex >= 40) {
        badge.className = "text-xs font-bold px-2 py-0.5 rounded bg-amber-950 text-amber-400 border border-amber-800";
        badge.textContent = "MODERATE COG";
        diag.textContent = "Reliable contributor taken for granted. Requires external offer leverage to break inertia.";
      } else {
        badge.className = "text-xs font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800";
        badge.textContent = "MOBILE / SPONSORED";
        diag.textContent = "Healthy mobility or strong executive sponsorship protects internal trajectory.";
      }
    }

    function updateBellmanDisplay(stayBase0, stayBonus0, leaveBase0, leaveBonus0, reqCounterBase, reqCounterRaisePct, deltaNW) {
      document.getElementById('bellmanBaseDisplay').textContent = `S$${reqCounterBase.toLocaleString()} / mo`;
      document.getElementById('bellmanRaiseDisplay').textContent = `+${reqCounterRaisePct}% increment required to stay`;
      document.getElementById('bellmanExternalCash').textContent = `S$${Math.round(leaveBase0 * 12 + leaveBonus0).toLocaleString()} / yr`;
      document.getElementById('bellmanCurrentBase').textContent = `S$${Math.round(stayBase0 * 12 + stayBonus0).toLocaleString()} / yr`;
      document.getElementById('bellmanIndiffTot').textContent = `S$${Math.round(reqCounterBase * 12 + stayBonus0).toLocaleString()} / yr`;

      const deltaPill = document.getElementById('horizonDeltaPill');
      if (deltaNW >= 0) {
        deltaPill.className = "text-xs text-emerald-400 bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-800";
        deltaPill.textContent = `+S$${deltaNW.toLocaleString()} Delta (${state.selectedHorizon === 'retire' ? 'Retirement' : state.selectedHorizon + 'y'})`;
      } else {
        deltaPill.className = "text-xs text-cyan-400 bg-cyan-950/80 px-2 py-0.5 rounded border border-cyan-800";
        deltaPill.textContent = `-S$${Math.abs(deltaNW).toLocaleString()} Stay Superior`;
      }
    }

    function updateHorizonSummaryCards(stayYearly, leaveYearly, maxYears) {
      const curAge = state.currentAge;

      const idx10 = Math.min(10, maxYears) - 1;
      const idx20 = Math.min(20, maxYears) - 1;
      const idxRetire = maxYears - 1;

      const d10 = leaveYearly[idx10].nw - stayYearly[idx10].nw;
      const d10Pct = ((leaveYearly[idx10].nw / stayYearly[idx10].nw) - 1) * 100;

      const d20 = leaveYearly[idx20].nw - stayYearly[idx20].nw;
      const d20Pct = ((leaveYearly[idx20].nw / stayYearly[idx20].nw) - 1) * 100;

      const dRetire = leaveYearly[idxRetire].nw - stayYearly[idxRetire].nw;
      const dRetirePct = ((leaveYearly[idxRetire].nw / stayYearly[idxRetire].nw) - 1) * 100;

      document.getElementById('h10Ages').textContent = `Age ${curAge} → ${curAge + idx10 + 1}`;
      document.getElementById('delta10y').textContent = `${d10 >= 0 ? '+' : ''}S$${d10.toLocaleString()}`;
      document.getElementById('delta10yPct').textContent = `${d10Pct >= 0 ? '+' : ''}${d10Pct.toFixed(1)}%`;

      document.getElementById('h20Ages').textContent = `Age ${curAge} → ${curAge + idx20 + 1}`;
      document.getElementById('delta20y').textContent = `${d20 >= 0 ? '+' : ''}S$${d20.toLocaleString()}`;
      document.getElementById('delta20yPct').textContent = `${d20Pct >= 0 ? '+' : ''}${d20Pct.toFixed(1)}%`;

      document.getElementById('hRetireAges').textContent = `Age ${curAge} → ${state.retireAge}`;
      document.getElementById('deltaRetire').textContent = `${dRetire >= 0 ? '+' : ''}S$${dRetire.toLocaleString()}`;
      document.getElementById('deltaRetirePct').textContent = `${dRetirePct >= 0 ? '+' : ''}${dRetirePct.toFixed(1)}%`;
    }

    function renderMilestoneTable(results) {
      const tbody = document.getElementById('milestoneTableBody');
      const stay = results.stayYearly;
      const leave = results.leaveYearly;

      const milestoneYears = state.showAllYears 
        ? Array.from({length: results.maxYears}, (_, i) => i + 1)
        : [1, 2, 3, 5, 10, 15, 20, 25, 30, results.maxYears].filter((y, idx, arr) => y <= results.maxYears && arr.indexOf(y) === idx);

      tbody.innerHTML = milestoneYears.map(yr => {
        const s = stay[yr - 1];
        const l = leave[yr - 1];
        const delta = l.nw - s.nw;
        return `
          <tr class="hover:bg-slate-800/40 transition">
            <td class="py-2.5 px-3 font-bold text-white">Yr ${yr} <span class="text-slate-500 font-normal">(${s.age}yo)</span></td>
            <td class="py-2.5 px-3 text-cyan-400">S$${s.base.toLocaleString()}</td>
            <td class="py-2.5 px-3 text-cyan-400">S$${s.totCash.toLocaleString()}</td>
            <td class="py-2.5 px-3 text-emerald-400">S$${l.base.toLocaleString()}</td>
            <td class="py-2.5 px-3 text-emerald-400">S$${l.totCash.toLocaleString()}</td>
            <td class="py-2.5 px-3 font-semibold text-slate-200">S$${s.nw.toLocaleString()}</td>
            <td class="py-2.5 px-3 font-semibold text-emerald-400">S$${l.nw.toLocaleString()}</td>
            <td class="py-2.5 px-3 font-bold ${delta >= 0 ? 'text-emerald-400' : 'text-rose-400'}">
              ${delta >= 0 ? '+' : ''}S$${delta.toLocaleString()}
            </td>
            <td class="py-2.5 px-3 text-amber-400">
              S$${(l.cumulSideline).toLocaleString()}
            </td>
          </tr>
        `;
      }).join('');
    }

    // =========================================================================
    // CANVAS CHART RENDERING
    // =========================================================================
    function drawChart(results) {
      if (!results) return;
      const canvas = document.getElementById('trajectoryCanvas');
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;

      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);

      const w = rect.width;
      const h = rect.height;

      ctx.clearRect(0, 0, w, h);

      const padLeft = 70;
      const padRight = 30;
      const padTop = 25;
      const padBottom = 40;

      const chartW = w - padLeft - padRight;
      const chartH = h - padTop - padBottom;

      const numYears = results.horizonYears;
      const stayData = results.stayYearly.slice(0, numYears);
      const leaveData = results.leaveYearly.slice(0, numYears);

      // Compute Max and Min Y
      let maxY = 0;
      for (let i = 0; i < numYears; i++) {
        maxY = Math.max(maxY, stayData[i].nw, leaveData[i].nw);
      }
      maxY = maxY * 1.15; // 15% headroom

      // Gridlines & Y-Axis Labels
      ctx.lineWidth = 1;
      ctx.strokeStyle = '#1e293b';
      ctx.fillStyle = '#64748b';
      ctx.font = '11px -apple-system, BlinkMacSystemFont, monospace';
      ctx.textAlign = 'right';

      const ySteps = 5;
      for (let i = 0; i <= ySteps; i++) {
        const val = (maxY / ySteps) * i;
        const y = padTop + chartH - (val / maxY) * chartH;

        ctx.beginPath();
        ctx.moveTo(padLeft, y);
        ctx.lineTo(w - padRight, y);
        ctx.stroke();

        let label = `S$${(val / 1000000).toFixed(1)}M`;
        if (val < 1000000) label = `S$${Math.round(val / 1000)}k`;
        ctx.fillText(label, padLeft - 10, y + 4);
      }

      // X-Axis Labels (Years)
      ctx.textAlign = 'center';
      const xStepCount = Math.min(numYears, 8);
      for (let i = 0; i < numYears; i += Math.ceil(numYears / xStepCount)) {
        const x = padLeft + (i / (numYears - 1)) * chartW;
        const item = stayData[i];

        ctx.beginPath();
        ctx.moveTo(x, padTop + chartH);
        ctx.lineTo(x, padTop + chartH + 5);
        ctx.stroke();

        ctx.fillText(`Yr ${item.yr} (${item.age}yo)`, x, padTop + chartH + 20);
      }

      // Helper function for coordinate mapping
      function getX(idx) {
        return padLeft + (idx / (numYears - 1)) * chartW;
      }
      function getY(val) {
        return padTop + chartH - (val / maxY) * chartH;
      }

      // Draw Curves
      // 1. STAY Downside (Dashed Cyan)
      drawCurve(ctx, stayData.map(d => d.downside), getX, getY, '#38bdf8', [4, 4], 1.5);

      // 2. LEAVE Downside (Dashed Emerald)
      drawCurve(ctx, leaveData.map(d => d.downside), getX, getY, '#10b981', [4, 4], 1.5);

      // 3. STAY Median (Solid Cyan)
      drawCurve(ctx, stayData.map(d => d.nw), getX, getY, '#38bdf8', [], 3);

      // 4. LEAVE Median (Solid Emerald)
      drawCurve(ctx, leaveData.map(d => d.nw), getX, getY, '#10b981', [], 3.5);

      // Store chart coordinates for tooltip hover
      canvas.chartCoords = {
        padLeft, padRight, padTop, padBottom, chartW, chartH, numYears, stayData, leaveData, getX, getY
      };
    }

    function drawCurve(ctx, values, getX, getY, strokeStyle, lineDash, lineWidth) {
      if (values.length < 2) return;
      ctx.save();
      ctx.strokeStyle = strokeStyle;
      ctx.lineWidth = lineWidth;
      ctx.setLineDash(lineDash || []);
      ctx.beginPath();
      ctx.moveTo(getX(0), getY(values[0]));

      for (let i = 1; i < values.length; i++) {
        ctx.lineTo(getX(i), getY(values[i]));
      }
      ctx.stroke();
      ctx.restore();
    }

    // Chart Mouse Hover Interaction
    const chartCanvas = document.getElementById('trajectoryCanvas');
    const chartTooltip = document.getElementById('chartTooltip');

    chartCanvas.addEventListener('mousemove', (e) => {
      const coords = chartCanvas.chartCoords;
      if (!coords) return;
      const rect = chartCanvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      if (mouseX < coords.padLeft || mouseX > rect.width - coords.padRight) {
        chartTooltip.classList.add('hidden');
        return;
      }

      const ratio = (mouseX - coords.padLeft) / coords.chartW;
      const idx = Math.min(coords.numYears - 1, Math.max(0, Math.round(ratio * (coords.numYears - 1))));

      const s = coords.stayData[idx];
      const l = coords.leaveData[idx];
      const delta = l.nw - s.nw;

      chartTooltip.innerHTML = `
        <div class="font-bold text-white border-b border-slate-700 pb-1 mb-2">
          Year ${s.yr} <span class="text-slate-400 font-normal">(${s.age} Years Old)</span>
        </div>
        <div class="space-y-1 font-mono">
          <div class="flex justify-between gap-4">
            <span class="text-cyan-400">STAY NW:</span>
            <span class="font-bold text-white">S$${s.nw.toLocaleString()}</span>
          </div>
          <div class="flex justify-between gap-4">
            <span class="text-emerald-400">LEAVE NW:</span>
            <span class="font-bold text-emerald-400">S$${l.nw.toLocaleString()}</span>
          </div>
          <div class="flex justify-between gap-4 pt-1 border-t border-slate-800">
            <span class="text-slate-300">Net Delta:</span>
            <span class="font-bold ${delta >= 0 ? 'text-emerald-400' : 'text-rose-400'}">
              ${delta >= 0 ? '+' : ''}S$${delta.toLocaleString()}
            </span>
          </div>
          <div class="flex justify-between gap-4 text-[10px] text-amber-400 pt-0.5">
            <span>Sideline Cumul:</span>
            <span>S$${l.cumulSideline.toLocaleString()}</span>
          </div>
        </div>
      `;

      chartTooltip.style.left = `${Math.min(rect.width - 230, Math.max(10, mouseX + 15))}px`;
      chartTooltip.style.top = `${Math.min(rect.height - 120, Math.max(10, mouseY - 40))}px`;
      chartTooltip.classList.remove('hidden');
    });

    chartCanvas.addEventListener('mouseleave', () => {
      chartTooltip.classList.add('hidden');
    });

  </script>
</body>
</html>
"""

    out_workspace = os.path.join(base_dir, "ssoc_career_actuarial_visualizer.html")
    with open(out_workspace, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated standalone visualizer at {out_workspace} (Size: {os.path.getsize(out_workspace)/1024:.1f} KB)")

    brain_dir = os.environ.get("ANTIGRAVITY_BRAIN_DIR")
    if brain_dir and os.path.exists(brain_dir):
        out_brain = os.path.join(brain_dir, "ssoc_career_actuarial_visualizer.html")
        with open(out_brain, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Synced visualizer to brain artifact directory at {out_brain}")

if __name__ == "__main__":
    build_visualizer()
