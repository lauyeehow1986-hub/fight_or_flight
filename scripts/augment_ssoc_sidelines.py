#!/usr/bin/env python3
"""
Augment SSOC 2024 Master Dataset with Granular Sideline Simulation
Covers all 1,006 unique SSOC occupations with tailored sidelines, pay, ACRA structures,
CPF SEP MediSave obligations, and Moonlighting COI risk mitigations.
"""

import os
import json
import pandas as pd
import numpy as np

def generate_sideline(code_str: str, title: str, p50: float) -> dict:
    major = code_str[0]
    sub = code_str[:2]
    
    hours = 8.0
    structure = "ACRA Sole Proprietorship"
    coi = "Low"
    coi_mitigation = "Operate strictly outside working hours on personal devices with zero employer client solicitation."
    
    # Granular domain classification
    if major == '1':  # Managers & Senior Officials
        s_title = f"Executive Advisory & Strategic Consulting for {title}"
        s_desc = "Advising startups, SMEs, and growth-stage enterprises on operational efficiency, governance, and business expansion."
        monthly_gross = max(2800.0, min(8500.0, p50 * 0.35))
        structure = "Exempt Private Limited (Pte Ltd)"
        coi = "Medium"
        coi_mitigation = "Disclose outside non-executive directorships; ringfence intellectual property under separate corporate entity."
    elif sub == '25':  # ICT / Software / Cyber / Data
        s_title = f"Cloud Architecture, AI Automation & Micro-SaaS Studio ({title})"
        s_desc = "Building specialized B2B workflow automation, API connectors, technical auditing, and independent micro-SaaS utilities."
        monthly_gross = max(2400.0, min(7500.0, p50 * 0.42))
        structure = "Exempt Private Limited (Pte Ltd)" if monthly_gross >= 4000 else "ACRA Sole Proprietorship"
        coi = "Medium"
        coi_mitigation = "Ensure 100% of code is authored on personal hardware and GitHub repositories; verify non-compete scope."
    elif sub == '24':  # Business, Finance & Accounting
        s_title = f"Fractional CFO, Financial Modeling & Compliance Advisory ({title})"
        s_desc = "Providing small enterprises with cashflow forecasting, IRAS corporate tax preparation, and MAS regulatory readiness audits."
        monthly_gross = max(2000.0, min(6800.0, p50 * 0.40))
        structure = "Exempt Private Limited (Pte Ltd)" if monthly_gross >= 4000 else "ACRA Sole Proprietorship"
        coi = "Medium"
        coi_mitigation = "Strictly adhere to insider trading laws and never trade on Material Non-Public Information (MNPI)."
    elif sub == '22':  # Health Professionals
        s_title = f"Biomedical Writing, Health Informatics & Protocol Advisory ({title})"
        s_desc = "Preparing regulatory dossiers for HSA/FDA submission, literature meta-analyses, and health tech advisory."
        monthly_gross = max(2200.0, min(6200.0, p50 * 0.35))
        structure = "ACRA Sole Proprietorship"
        coi = "Medium"
        coi_mitigation = "Comply with SMC/SNB ethical codes and institutional clinical moonlight declarations."
    elif sub == '23':  # Teaching Professionals
        s_title = f"Specialized Curriculum Licensing & Premium Academic Coaching ({title})"
        s_desc = "Authoring digital assessment materials, conducting weekend exam clinics, and independent syllabus consulting."
        monthly_gross = max(1600.0, min(5500.0, p50 * 0.45))
        structure = "ACRA Sole Proprietorship"
        coi = "Low"
        coi_mitigation = "Never tutor students enrolled in personal school classes; publish educational content independently."
    elif sub == '21':  # Science & Engineering
        s_title = f"Freelance CAD/BIM Modeling & Green Mark Feasibility ({title})"
        s_desc = "Subcontracting 3D structural modeling, sustainability audits, and rapid prototyping for local developers and fabricators."
        monthly_gross = max(1800.0, min(5500.0, p50 * 0.38))
        structure = "ACRA Sole Proprietorship"
        coi = "Low"
        coi_mitigation = "Maintain professional indemnity insurance; do not endorse structural submissions without PE license."
    elif sub == '26':  # Legal, Social & Creative
        s_title = f"Independent Content Studio, Editorial & Creative Direction ({title})"
        s_desc = "High-end corporate video editing, technical copywriting, brand positioning, and digital media licensing."
        monthly_gross = max(1500.0, min(5000.0, p50 * 0.40))
        structure = "ACRA Sole Proprietorship"
        coi = "Low"
        coi_mitigation = "Contractually retain copyright and delivery rights; maintain distinct client roster."
    elif major == '3':  # Associate Professionals & Technicians
        s_title = f"Technical Inspection, Equipment Setup & Event Operations ({title})"
        s_desc = "Providing weekend technical rigging, calibration, testing services, and ad-hoc operations support."
        monthly_gross = max(1200.0, min(3600.0, p50 * 0.35))
        structure = "ACRA Sole Proprietorship"
        coi = "Low"
        coi_mitigation = "Maintain personal tools and equipment; operate under individual sole proprietorship."
    elif major == '4':  # Clerical Support Workers
        s_title = f"Virtual Executive Assistance & SME E-Commerce Bookkeeping ({title})"
        s_desc = "Remote transcription, Shopify/Shopee inventory management, invoice reconciliation, and customer correspondence."
        monthly_gross = max(800.0, min(2200.0, p50 * 0.35))
        structure = "ACRA Sole Proprietorship"
        coi = "Low"
        coi_mitigation = "Strictly use personal email and computing hardware during non-work hours."
    elif major == '5':  # Service & Sales Workers
        s_title = f"E-Commerce Social Selling, Event Hosting & Fitness Coaching ({title})"
        s_desc = "Livestream merchandising, freelance banquet/event coordination, and group personal training."
        monthly_gross = max(900.0, min(2800.0, p50 * 0.40))
        structure = "ACRA Sole Proprietorship"
        coi = "Low"
        coi_mitigation = "Avoid competing with store brands; ensure platform sales payouts route through personal PayNow."
    elif major == '6':  # Agriculture & Fishery
        s_title = f"Urban Hydroponics Setup & Ornamental Aquatic Consulting ({title})"
        s_desc = "Designing balcony vertical farming systems, commercial aquarium maintenance, and exotic plant nursery care."
        monthly_gross = max(800.0, min(2000.0, p50 * 0.35))
        structure = "ACRA Sole Proprietorship"
        coi = "Low"
        coi_mitigation = "Comply with SFA urban farming regulations and biosecurity protocols."
    elif major == '7':  # Craftsmen & Trades
        s_title = f"Emergency Trade Repairs & Bespoke Renovation Contracting ({title})"
        s_desc = "On-call weekend electrical repairs, sanitary plumbing, custom joinery, and specialized mechanical refurbishment."
        monthly_gross = max(1300.0, min(4200.0, p50 * 0.45))
        structure = "ACRA Sole Proprietorship"
        coi = "Low"
        coi_mitigation = "Verify EMA/PUB licensing and carry third-party property damage coverage."
    elif major == '8':  # Plant & Machine Operators / Drivers
        s_title = f"Off-Peak Platform Relief Driving & Fleet Logistics Shifting ({title})"
        s_desc = "Flexible ride-hailing (Grab/Tada/Ryde), heavy equipment depot shifting, and after-hours cargo relocation."
        monthly_gross = max(1000.0, min(2800.0, p50 * 0.38))
        structure = "ACRA Sole Proprietorship"
        coi = "Low"
        coi_mitigation = "Adhere to LTA Vocational Licence rules and mandatory rest period safety requirements."
    elif major == '9':  # Cleaners & Elementary Workers
        s_title = f"End-of-Tenancy Deep Cleaning & Residential Sanitisation ({title})"
        s_desc = "Weekend move-out deep scrubbing, air conditioning chemical wash, and bulky furniture clearance."
        monthly_gross = max(750.0, min(1900.0, p50 * 0.45))
        structure = "ACRA Sole Proprietorship"
        coi = "Low"
        coi_mitigation = "Use personal commercial-grade cleaning agents and portable steam extraction equipment."
    else:  # Armed Forces / Other
        s_title = f"Corporate Executive Security & Tactical Fitness Bootcamps ({title})"
        s_desc = "Delivering corporate team-building, personal security awareness, and tactical fitness conditioning."
        monthly_gross = max(1500.0, min(3800.0, p50 * 0.35))
        structure = "ACRA Sole Proprietorship"
        coi = "Medium"
        coi_mitigation = "Comply strictly with official Moonlighting Regulations and Security Industry Regulatory Department (SIRD) codes."

    annual_gross = monthly_gross * 12.0
    expense_rate = 0.12  # 12% standard legitimate deductible business expense
    net_trade_income = annual_gross * (1.0 - expense_rate)
    
    # 2026 CPF SEP MediSave Rules
    medisave_rate_pct = 9.0  # Standard mid-career baseline rate
    if net_trade_income > 6000.0:
        annual_medisave = min(8160.0, net_trade_income * (medisave_rate_pct / 100.0))
    else:
        annual_medisave = 0.0
        
    annual_net_cash = net_trade_income - annual_medisave
    
    return {
        "sideline_title": s_title,
        "sideline_description": s_desc,
        "sideline_structure": structure,
        "sideline_weekly_hours": hours,
        "sideline_monthly_gross_sgd": int(round(monthly_gross)),
        "sideline_annual_gross_sgd": int(round(annual_gross)),
        "sideline_net_trade_income_sgd": int(round(net_trade_income)),
        "sideline_medisave_rate_pct": medisave_rate_pct,
        "sideline_annual_medisave_sgd": int(round(annual_medisave)),
        "sideline_annual_net_cash_sgd": int(round(annual_net_cash)),
        "sideline_coi_risk": coi,
        "sideline_coi_mitigation": coi_mitigation
    }

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "ssoc_2024_actuarial_stay_leave_master.csv")
    json_path = os.path.join(base_dir, "ssoc_2024_actuarial_stay_leave_master.json")
    
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} SSOC records.")
    
    sideline_records = []
    for idx, row in df.iterrows():
        code_str = str(row["ssoc_code"]).strip()
        title = str(row["ssoc_title"]).strip()
        p50 = float(row["p50_median_monthly_base_sgd"])
        sideline = generate_sideline(code_str, title, p50)
        sideline_records.append(sideline)
        
    sideline_df = pd.DataFrame(sideline_records)
    
    # Drop existing sideline columns if present to avoid duplicate columns
    for col in sideline_df.columns:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)
            
    augmented_df = pd.concat([df, sideline_df], axis=1)
    
    # Save back to CSV
    augmented_df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved augmented CSV to {csv_path} with {len(augmented_df.columns)} columns.")
    
    # Save back to JSON
    json_records = augmented_df.to_dict(orient="records")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_records, f, indent=2, ensure_ascii=False)
    print(f"Saved augmented JSON to {json_path}.")
    
    # Optional brain sync if env var set
    brain_dir = os.environ.get("ANTIGRAVITY_BRAIN_DIR")
    if brain_dir and os.path.exists(brain_dir):
        brain_csv = os.path.join(brain_dir, "ssoc_2024_actuarial_stay_leave_master.csv")
        brain_json = os.path.join(brain_dir, "ssoc_2024_actuarial_stay_leave_master.json")
        augmented_df.to_csv(brain_csv, index=False, encoding="utf-8")
        with open(brain_json, "w", encoding="utf-8") as f:
            json.dump(json_records, f, indent=2, ensure_ascii=False)
        print("Synced to brain artifacts directory.")
        
    print("\nSummary of Sideline Gross Monthly Earnings by Major SSOC Group:")
    augmented_df['major'] = augmented_df['ssoc_code'].astype(str).str[0]
    summary = augmented_df.groupby('major')['sideline_monthly_gross_sgd'].agg(['count', 'mean', 'min', 'max'])
    print(summary)

if __name__ == "__main__":
    main()
