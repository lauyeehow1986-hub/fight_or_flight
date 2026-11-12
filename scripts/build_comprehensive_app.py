import os
import json
import zipfile
import xml.etree.ElementTree as ET
import re

def calibrate_title_pay(code: str, title: str, p25: float, p50: float, p75: float):
    t_lower = title.lower()

    # 1. Constitutional, Apex Political & Judiciary (Official Singapore Gazetted Benchmarks)
    if code == '11110':
        if 'prime minister' in t_lower:
            return 110000, 15.0, 'STAT', 'Official Singapore Gazetted Benchmark: Prime Minister (S$2.2M/yr benchmark)'
        elif 'minister of state' in t_lower:
            return 38000, 6.0, 'STAT', 'Official Singapore Gazetted Benchmark: Minister of State (S$770k/yr benchmark)'
        elif 'minister' in t_lower and 'secretary' not in t_lower:
            return 55000, 7.0, 'STAT', 'Official Singapore White Paper Benchmark: Cabinet Minister MR4 (S$1.1M/yr benchmark)'
        elif 'attorney general' in t_lower and 'deputy' not in t_lower:
            return 70000, 7.0, 'STAT', 'Official Singapore Judicial & Legal Service Gazetted Benchmark'
        elif 'deputy attorney general' in t_lower:
            return 45000, 6.0, 'STAT', 'Official Singapore Judicial & Legal Service Gazetted Benchmark'
        elif 'speaker' in t_lower:
            return 45000, 6.0, 'STAT', 'Official Singapore Statutory Benchmark: Speaker of Parliament'
        elif 'parliamentary secretary' in t_lower:
            return 28000, 5.0, 'STAT', 'Official Singapore Gazetted Benchmark: Parliamentary Secretary'
        elif 'legislator' in t_lower or 'member of parliament' in t_lower or 'parliamentarian' in t_lower:
            return 16041, 1.0, 'STAT', 'Official Statutory MP Allowance: S$192,500/yr (Parliamentary Allowances Act Cap. 219)'
        elif 'solicitor general' in t_lower:
            return 50000, 6.0, 'STAT', 'Official Singapore Judicial & Legal Service Gazetted Benchmark'

    if code == '11121':
        if 'permanent secretary' in t_lower or 'auditor general' in t_lower:
            return 55000, 6.0, 'STAT', 'Official Singapore Public Service Division Apex Administrative Service Benchmark'
        elif 'commissioner' in t_lower and 'deputy' not in t_lower:
            return 38000, 5.0, 'STAT', 'Official Singapore Civil Service Commissioner Benchmark'
        elif 'deputy commissioner' in t_lower or 'deputy secretary' in t_lower:
            return 28000, 4.5, 'STAT', 'Official Singapore Civil Service Deputy Secretary Benchmark'
        elif 'ambassador' in t_lower or 'high commissioner' in t_lower:
            return 32000, 4.5, 'STAT', 'Official Singapore MFA Senior Diplomatic Benchmark'
        elif 'director-general' in t_lower:
            return 35000, 5.0, 'STAT', 'Official Singapore Civil Service Director-General Benchmark'

    if code == '26120':
        if 'chief justice' in t_lower:
            return 75000, 8.0, 'STAT', 'Official Singapore Statutory Benchmark: Chief Justice (Judges Remuneration Act)'
        elif 'judge of appeal' in t_lower:
            return 58000, 7.0, 'STAT', 'Official Singapore Statutory Benchmark: Judge of Appeal'
        elif 'high court judge' in t_lower:
            return 48000, 6.5, 'STAT', 'Official Singapore Statutory Benchmark: High Court Judge'
        elif 'judicial commissioner' in t_lower:
            return 36000, 5.5, 'STAT', 'Official Singapore Statutory Benchmark: Judicial Commissioner'
        elif 'district court judge' in t_lower or 'presiding judge' in t_lower:
            return 26000, 4.5, 'STAT', 'Official Singapore Statutory Benchmark: District Court Judge'
        elif 'magistrate' in t_lower or 'registrar' in t_lower:
            return 18000, 4.0, 'STAT', 'Official Singapore Statutory Benchmark: Magistrate / Registrar'

    # 2. Medical & Dental Hierarchy (Singapore Public Healthcare Clusters: MOH, SingHealth, NUHS, NHG)
    if code.startswith('221') or code.startswith('226'):
        if re.search(r'\bsenior consultant\b', t_lower):
            return int(round(max(p75 * 1.30, 28000))), 4.0, 'SEN', 'Hospital Apex Specialist: Senior Consultant Tier'
        elif re.search(r'\bconsultant\b', t_lower) and not re.search(r'\b(associate|assistant)\b', t_lower):
            return int(round(max(p50 * 1.15, 20000))), 3.5, 'SEN', 'Hospital Specialist: Consultant Tier'
        elif re.search(r'\bassociate consultant\b', t_lower):
            return int(round(max(p25 * 1.05, 15000))), 3.0, 'SEN', 'Hospital Sub-Specialist: Associate Consultant Tier'
        elif re.search(r'\bregistrar\b', t_lower):
            return int(round(max(p25 * 0.75, 10500))), 2.5, 'SEN', 'Advanced Specialist Trainee / Registrar Tier'
        elif re.search(r'\bmedical officer\b', t_lower):
            return int(round(max(p25 * 0.55, 7500))), 2.0, 'SEN', 'Hospital Post-HO: Medical Officer Tier'
        elif re.search(r'\b(resident physician|resident)\b', t_lower) and 'senior' not in t_lower:
            return int(round(max(p25 * 0.65, 8500))), 2.0, 'SEN', 'Hospital Residency Programme Medical Resident'
        elif re.search(r'\bhouse officer\b', t_lower):
            return 5200, 1.5, 'SEN', 'Hospital PGY-1 Trainee: House Officer Tier'

    # 3. Aviation Hierarchy (Civil Aviation Authority of Singapore & Commercial Airlines)
    if code.startswith('2172'):
        if re.search(r'\b(captain|commander|line captain)\b', t_lower):
            return int(round(max(p75 * 1.25, 24000))), 3.5, 'SEN', 'Commercial Aviation: Airline Captain / Commander'
        elif re.search(r'\b(first officer|senior first officer)\b', t_lower):
            return int(round(p50 * 0.95)), 2.5, 'SEN', 'Commercial Aviation: First Officer Tier'
        elif re.search(r'\bsecond officer\b', t_lower):
            return int(round(p25 * 0.70)), 2.0, 'SEN', 'Commercial Aviation: Second Officer / Cruise Relief'
        elif re.search(r'\bcadet\b', t_lower):
            return 3800, 1.0, 'SEN', 'Commercial Aviation: Cadet Pilot Trainee'

    # 4. Academic & University Faculty (NUS, NTU, SMU, SUTD)
    if code == '23111':
        if re.search(r'\b(distinguished professor|provost|dean)\b', t_lower):
            return 32000, 4.0, 'SEN', 'University Leadership / Distinguished Chair Professor'
        elif re.search(r'\bprofessor\b', t_lower) and not re.search(r'\b(associate|assistant|adjunct)\b', t_lower):
            return int(round(p75 * 1.15)), 3.5, 'SEN', 'University Faculty: Tenured Full Professor'
        elif re.search(r'\bassociate professor\b', t_lower):
            return int(round(p50 * 1.10)), 3.0, 'SEN', 'University Faculty: Associate Professor'
        elif re.search(r'\bassistant professor\b', t_lower):
            return int(round(p25 * 1.10)), 2.5, 'SEN', 'University Faculty: Tenure-Track Assistant Professor'
        elif re.search(r'\b(lecturer|senior lecturer)\b', t_lower):
            return int(round(p25 * 0.85)), 2.0, 'SEN', 'University Faculty: Teaching Lecturer / Fellow'

    # 4b. Statistics & Quantitative Science Sub-Specialty Domain Calibration (SSOC 21221)
    if code == '21221':
        if 'finance' in t_lower or 'financial' in t_lower or 'quant' in t_lower:
            return 12500, 3.8, 'SEN', 'Actuarially Calibrated Domain: Finance Statistician (Quant Modeling & Derivatives Risk)'
        elif 'biostatistician' in t_lower:
            return 9800, 2.8, 'SEN', 'Actuarially Calibrated Domain: Biostatistician (Clinical Trial Protocol & CDISC Regulatory Submissions)'
        elif 'bioinformatics' in t_lower:
            return 9650, 2.6, 'SEN', 'Actuarially Calibrated Domain: Bioinformatics Specialist (Genomics & High-Throughput Omics)'
        elif 'biometrician' in t_lower:
            return 9200, 2.4, 'SEN', 'Actuarially Calibrated Domain: Biometrician (Biological & Agricultural Systems Modeling)'
        elif 'economics' in t_lower or 'econometric' in t_lower:
            return 8500, 2.6, 'SEN', 'Actuarially Calibrated Domain: Economics Statistician (Econometric & Macro Policy Modeling)'
        elif 'health' in t_lower or 'epidemiol' in t_lower:
            return 7800, 2.5, 'SEN', 'Actuarially Calibrated Domain: Health Statistician (Public Healthcare & Population Surveillance)'
        elif 'demographer' in t_lower:
            return 7600, 2.4, 'SEN', 'Actuarially Calibrated Domain: Demographer (Population Projections & Vital Statistics)'
        elif 'education' in t_lower:
            return 7200, 2.2, 'SEN', 'Actuarially Calibrated Domain: Education Statistician (Psychometrics & Assessment Analytics)'
        elif 'research officer' in t_lower:
            return 6800, 2.0, 'SEN', 'Actuarially Calibrated Domain: Research Officer (Statistical Data Modeling)'
        elif 'survey' in t_lower or 'polling' in t_lower:
            return 5600, 1.8, 'SEN', 'Actuarially Calibrated Domain: Survey Statistician (Sampling Operations & Survey Fieldwork)'
        elif re.search(r'\b(assistant|junior)\b', t_lower):
            return 4800, 1.5, 'SEN', 'Actuarially Calibrated Domain: Assistant / Junior Statistician'
        else:
            return 8350, 2.2, 'BASE', 'Principal Profession Benchmark: Statistician (Parent SSOC 21221 Median Anchor)'

    # 4c. Mathematics & Cryptography Domain Calibration (SSOC 21211)
    if code == '21211':
        if 'cryptanalyst' in t_lower or 'cipher' in t_lower:
            return 11500, 3.2, 'SEN', 'Actuarially Calibrated Domain: Cryptanalyst / Cipher Specialist (Cybersecurity & Defense Math)'
        elif 'applied' in t_lower:
            return 9800, 2.8, 'SEN', 'Actuarially Calibrated Domain: Applied Mathematics Scientist'
        elif 'algebraist' in t_lower or 'geometrician' in t_lower:
            return 8800, 2.5, 'SEN', 'Actuarially Calibrated Domain: Pure Mathematics Researcher'

    # 5. Entry-level / Junior / Trainee keywords (Evaluate early to prevent false senior matches)
    if re.search(r'\b(pupil|intern\b|apprentice|trainee\b|assistant nurse|cadet)\b', t_lower):
        return int(round(p25 * 0.70)), 1.0, 'SEN', 'Actuarially Calibrated Seniority: Intern / Trainee Entry Tier (0.70x P25)'

    # 6. Assistant / Sub-ordinate prefixes (Avoid false positive C-suite/VP match on "Assistant Vice President")
    if re.search(r'\bassistant\s+vice[\s-]president\b', t_lower) or re.search(r'\bavp\b', t_lower):
        return int(round(p50 * 1.10)), 2.5, 'SEN', 'Banking & Corporate Hierarchy: Assistant Vice President (AVP)'

    # 7. Tier 1: C-Suite / Apex / Founder / Managing Director / Chairman / Senior Partner
    if re.search(r'\b(chief executive|ceo|chief financial|cfo|chief technology|cto|chief operating|coo|chief information|cio|chief risk|cro|chief data|chief digital|chief security|ciso|chief audit|chief legal|chief medical|chief commercial|chief revenue|chief investment|chief compliance|chief people|chief strategy|managing director|chairman|president\b|senior partner|general secretary)\b', t_lower):
        return int(round(max(p75 * 1.35, p50 * 1.70))), 4.0, 'SEN', 'Actuarially Calibrated Seniority: C-Suite / Apex Tier (1.70x P50 / 1.35x P75)'

    # 8. Tier 2: Director / Executive Director / Senior VP / Head of Department / Partner
    if re.search(r'\b(director|vice-president|vice president|vp\b|svp\b|evp\b|head of\b|head,\b|site director|general manager|partner\b|senior official|financial controller|general counsel)\b', t_lower):
        return int(round(max(p75 * 1.05, p50 * 1.30))), 3.5, 'SEN', 'Actuarially Calibrated Seniority: Director / VP / Senior Official Tier (1.30x P50)'

    # 9. Tier 3: Senior Manager / Assistant Director / Lead / Principal / Superintendent / Architect
    if re.search(r'\b(senior manager|lead\b|principal\b|assistant director|superintendent|chief engineer|senior fellow|fellow\b|master craftsman|architect\b|senior associate)\b', t_lower):
        return int(round(p75 * 0.95)), 3.0, 'SEN', 'Actuarially Calibrated Seniority: Senior Manager / Principal / Lead Tier (0.95x P75)'

    # 10. Tier 4: Manager / Senior Specialist / Senior Engineer / Senior Analyst / Consultant
    if re.search(r'\b(manager\b|senior engineer|senior specialist|senior analyst|senior consultant|senior developer)\b', t_lower):
        return int(round(p50 * 1.05)), 2.5, 'SEN', 'Actuarially Calibrated Seniority: Manager / Senior Specialist Tier (1.05x P50)'

    # 11. Tier 5: Specialist / Engineer / Analyst / Officer / Mid-Level
    if re.search(r'\b(administrator|assistant manager|deputy|specialist|consultant|engineer|analyst|developer|designer|officer|physician|accountant|doctor)\b', t_lower):
        return int(round(p25 + (p50 - p25) * 0.60)), 2.0, 'SEN', 'Actuarially Calibrated Seniority: Specialist / Officer Tier (P25 + 0.60 IQR)'

    # 12. Tier 6: Junior / Associate / Assistant / Aide
    if re.search(r'\b(assistant|associate|junior|aide|helper|attendant)\b', t_lower):
        return int(round(p25 * 0.85)), 1.5, 'SEN', 'Actuarially Calibrated Seniority: Junior / Assistant Tier (0.85x P25)'

    return int(p50), 2.2, 'BASE', 'Parent SSOC Broad Group Median'

def extract_all_titles(xlsx_path, master_lookup):
    print(f"Extracting titles from {xlsx_path}...")
    with zipfile.ZipFile(xlsx_path, 'r') as z:
        with z.open('xl/sharedStrings.xml') as f:
            tree = ET.parse(f)
            shared_strings = [elem.text for elem in tree.getroot().iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')]

        with z.open('xl/worksheets/sheet1.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            rows = list(root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'))

    titles_index = []
    for r in rows:
        cells = r.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c')
        row_vals = []
        for c in cells:
            val = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
            t = c.get('t')
            if val is not None and val.text:
                if t == 's':
                    row_vals.append(shared_strings[int(val.text)])
                else:
                    row_vals.append(val.text)
            else:
                row_vals.append('')

        if len(row_vals) >= 2:
            code = row_vals[0].strip()
            title = row_vals[1].strip()
            ttype = row_vals[2].strip() if len(row_vals) > 2 else ''
            if len(code) == 5 and (code.isdigit() or code.startswith('X')):
                t_flag = 'P' if 'Principal' in ttype else ('S' if 'SFw' in ttype else 'A')

                # Fetch baseline SSOC wage bounds
                parent_stats = master_lookup.get(code, {'p25': 4000, 'p50': 6000, 'p75': 9000})
                calibrated_base, calibrated_bm, calib_type, calib_note = calibrate_title_pay(
                    code, title, parent_stats['p25'], parent_stats['p50'], parent_stats['p75']
                )
                titles_index.append([title, code, t_flag, calibrated_base, calibrated_bm, calib_type, calib_note])

    print(f"Extracted and calibrated {len(titles_index)} total job title records.")
    return titles_index

def build_app():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "ssoc_2024_actuarial_stay_leave_master.json")
    template_path = os.path.join(base_dir, "src", "template.html")

    with open(json_path, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    mcf_path = os.path.join(base_dir, "data_mcf_2026_ssoc_summary.json")
    mcf_benchmarks = {}
    if os.path.exists(mcf_path):
        with open(mcf_path, "r", encoding="utf-8") as f:
            mcf_payload = json.load(f)
            mcf_benchmarks = mcf_payload.get("ssoc_benchmarks", {})
        print(f"Loaded MyCareersFuture benchmarks for {len(mcf_benchmarks)} SSOC codes ({mcf_payload.get('total_unique_postings', 0):,} live postings).")

    master_lookup = {}
    for r in master_data:
        code = str(r["ssoc_code"]).strip()
        master_lookup[code] = {
            "p25": int(r["p25_monthly_base_sgd"]),
            "p50": int(r["p50_median_monthly_base_sgd"]),
            "p75": int(r["p75_monthly_base_sgd"])
        }

    # Locate uploaded SSOC alphabetical index XLSX dynamically
    xlsx_candidate = os.environ.get("SSOC_XLSX_PATH", "")
    if not xlsx_candidate or not os.path.exists(xlsx_candidate):
        brain_dir = os.environ.get("ANTIGRAVITY_BRAIN_DIR", "")
        if brain_dir:
            xlsx_candidate = os.path.join(brain_dir, ".user_uploaded", "media_1794407090567_96dd581d.xlsx")
    if not xlsx_candidate or not os.path.exists(xlsx_candidate):
        user_home = os.path.expanduser("~")
        candidate = os.path.join(user_home, ".gemini", "antigravity", "brain", "7a5d928d-4122-4057-8c85-27fea2ce18e0", ".user_uploaded", "media_1794407090567_96dd581d.xlsx")
        if os.path.exists(candidate):
            xlsx_candidate = candidate
        else:
            xlsx_candidate = os.path.join(base_dir, "ssoc2024-alphabetical-index.xlsx")

    titles_index = extract_all_titles(xlsx_candidate, master_lookup)

    # Build full SSOC dictionary
    ssoc_dict = {}
    for r in master_data:
        code = str(r["ssoc_code"]).strip()
        ssoc_dict[code] = {
            "c": code,
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
            "hz": float(r["counteroffer_18m_hazard_rate"]),
            "src": r.get("wage_data_source_tier", "ACTUARIALLY_IMPUTED"),
            "cite": r.get("wage_citation", "Singapore Career Actuarial Engine Benchmark"),
            "rb25": r.get("official_reported_p25_sgd"),
            "rb50": r.get("official_reported_p50_sgd"),
            "rb75": r.get("official_reported_p75_sgd"),
            "rg50": r.get("official_reported_gross_p50_sgd")
        }
        mcf_row = mcf_benchmarks.get(code)
        if mcf_row and mcf_row.get("vacancies", 0) > 0:
            ssoc_dict[code]["mcf"] = [
                int(mcf_row.get("vacancies", 0)),
                int(mcf_row.get("salary_samples", 0)),
                int(mcf_row.get("p25_min_sgd", 0)),
                int(mcf_row.get("p50_offer_sgd", 0)),
                int(mcf_row.get("p75_max_sgd", 0)),
                float(mcf_row.get("avg_apps_per_vacancy", 0.0)),
                float(mcf_row.get("perm_share_pct", 0.0))
            ]

    lookup_json = json.dumps(ssoc_dict, separators=(',', ':'), ensure_ascii=False)
    titles_json = json.dumps(titles_index, separators=(',', ':'), ensure_ascii=False)

    print(f"Total payload size: {(len(lookup_json) + len(titles_json)) / 1024:.1f} KB")

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    output_html = template.replace('/*__LOOKUP_JSON__*/', lookup_json).replace('/*__TITLES_JSON__*/', titles_json)

    out_path = os.path.join(base_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output_html)

    print(f"Generated comprehensive visualizer at {out_path} ({len(output_html) / 1024:.1f} KB)")

if __name__ == "__main__":
    build_app()
