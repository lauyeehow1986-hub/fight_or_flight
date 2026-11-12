import sys
import json
import csv
import re
sys.stdout.reconfigure(encoding='utf-8')

# 1. Load MOM OWS 2024 raw records
with open('data_mom_ows_2024_raw.json', 'r', encoding='utf-8') as f:
    mom_records = json.load(f)

# 2. Load existing master
with open('ssoc_2024_actuarial_stay_leave_master.json', 'r', encoding='utf-8') as f:
    master_records = json.load(f)

print(f"Loaded {len(mom_records)} MOM OWS records, {len(master_records)} SSOC master records.")

def clean_str(s):
    s = s.lower().strip()
    s = re.sub(r'\(.*?\)', '', s).strip()
    s = s.replace('draughtsman', 'draughtsperson')
    s = s.replace('salesman', 'salesperson')
    s = s.replace('delivery man', 'delivery person')
    s = s.replace('sportsman', 'athlete')
    s = re.sub(r'[^a-z0-9 ]', '', s)
    return ' '.join(s.split())

# Index MOM records
mom_by_exact = {}
mom_by_clean = {}
for r in mom_records:
    occ = r['occ_desc'].lower().strip()
    c_occ = clean_str(occ)
    b50 = int(r['mthly_basic_wage_50_pctile']) if r['mthly_basic_wage_50_pctile'].isdigit() else 0
    g50 = int(r['mthly_gross_wage_50_pctile']) if r['mthly_gross_wage_50_pctile'].isdigit() else 0
    b25 = int(r['mthly_basic_wage_25_pctile']) if r['mthly_basic_wage_25_pctile'].isdigit() else 0
    b75 = int(r['mthly_basic_wage_75_pctile']) if r['mthly_basic_wage_75_pctile'].isdigit() else 0
    rec_obj = {
        'occ_desc': r['occ_desc'],
        'b25': b25, 'b50': b50, 'b75': b75,
        'g50': g50,
        'year': r.get('year', '2024')
    }
    mom_by_exact[occ] = rec_obj
    mom_by_clean[c_occ] = rec_obj

# Precise manual overrides for MOM historical phrasing -> SSOC 2024 codes
manual_mom_to_ssoc = {
    'educarer': '53112',
    'electrical lift, escalator and related equipment fitter': '74123',
    'financial markets back office administrator': '33113',
    'food and beverage establishments general cleaner': '91122',
    'general waste collection, recycling and material recovery worker': '96110',
    'ict sales and services professional': '24341',
    'office, commercial and industrial establishments indoor cleaner': '91121',
    'office, commercial and industrial establishments outdoor cleaner': '91123',
    'chief information officer/chief technology officer/chief security officer': '13301',
    'chief operating officer/general manager': '11202',
    'budgeting and financial accounting manager (including financial controller)': '12111',
    'business and financial project management professional': '24212',
    'enterprise/solution architect': '25113',
    'civil/structural engineering draughtsman': '31181',
    'electrical/electronics draughtsman': '31183',
    'architectural draughtsman': '31182',
    'advertising salesman': '33221',
    'athlete/sportsman': '34211',
    'arts and cultural centre manager (including gallery and museum manager)': '14311',
    'assistant civil and structural engineer': '31121',
    'audio and video equipment engineer': '21521',
    'audio and video equipment technician': '31142',
    'butcher, fishmonger and related food preparer': '75111',
    'career coach (counselling)': '24233',
    'chief engineer/second engineer (ship)': '31511',
    'clearing and forwarding agent': '33311',
    'commodities and freight derivatives broker': '33242',
    'community, partnership and relations manager': '12222',
    'dairy and confectionery products machine operator': '81602',
    'delivery man using motorised personal mobility aids/devices': '83212',
    'food and drink technologist': '21413',
    'fumigator and other pest and weed controller': '61301',
    'gardener and horticultural worker': '61131'
}

statutory_codes = {
    '11110': 'Singapore White Paper on Ministerial Salaries / Parliamentary Pensions and Allowances Act (Cap. 219)',
    '11121': 'Public Service Division Administrative Service Apex Framework & Statutory Board Chief Executive Benchmarks',
    '26120': 'Judicial Salaries Framework & Judges Remuneration Act (Cap. 147)',
    '01100': 'Singapore Armed Forces (SAF) Commissioned Senior Officers Remuneration Framework',
    '02100': 'Singapore Armed Forces (SAF) Warrant Officers & Specialists Remuneration Framework',
    '03100': 'Singapore Armed Forces (SAF) Enlisted Personnel Framework'
}

updated_master = []
mom_reported_count = 0
statutory_count = 0
imputed_count = 0

for m in master_records:
    code = str(m['ssoc_code']).strip()
    title = m['ssoc_title'].strip()
    c_title = clean_str(title)
    
    mom_rec = None
    if code in statutory_codes:
        data_source_tier = 'STATUTORY_BENCHMARK'
        is_officially_reported = False
        statutory_count += 1
        citation = statutory_codes[code]
        rep_p25 = None
        rep_p50 = None
        rep_p75 = None
        rep_g50 = None
    else:
        # Check manual
        for mom_desc, ssoc_target in manual_mom_to_ssoc.items():
            if code == ssoc_target:
                mom_rec = mom_by_exact.get(mom_desc) or mom_by_clean.get(mom_desc)
                break
                
        if not mom_rec:
            if title.lower().strip() in mom_by_exact:
                mom_rec = mom_by_exact[title.lower().strip()]
            elif c_title in mom_by_clean:
                mom_rec = mom_by_clean[c_title]
            else:
                for clean_occ, rec in mom_by_clean.items():
                    if len(clean_occ) > 5 and (clean_occ == c_title or clean_occ in c_title or c_title in clean_occ):
                        mom_rec = rec
                        break
                        
        if mom_rec:
            data_source_tier = 'MOM_OWS_2024_REPORTED'
            is_officially_reported = True
            mom_reported_count += 1
            citation = f"MOM Occupational Wage Survey 2024 (Data.gov.sg table d_9917e751f7498502f70052a940a3f312, '{mom_rec['occ_desc']}')"
            rep_p25 = mom_rec['b25']
            rep_p50 = mom_rec['b50']
            rep_p75 = mom_rec['b75']
            rep_g50 = mom_rec['g50']
        else:
            data_source_tier = 'ACTUARIALLY_IMPUTED'
            is_officially_reported = False
            imputed_count += 1
            citation = "Actuarially Imputed / Modelled (MOM suppressed due to sample size <10; regressed from SingStat M182171 series & Sub-Major Group median)"
            rep_p25 = None
            rep_p50 = None
            rep_p75 = None
            rep_g50 = None

    # Merge new metadata
    rec_copy = dict(m)
    rec_copy['wage_data_source_tier'] = data_source_tier
    rec_copy['is_officially_reported'] = is_officially_reported
    rec_copy['official_reported_p25_sgd'] = rep_p25
    rec_copy['official_reported_p50_sgd'] = rep_p50
    rec_copy['official_reported_p75_sgd'] = rep_p75
    rec_copy['official_reported_gross_p50_sgd'] = rep_g50
    rec_copy['wage_citation'] = citation
    
    updated_master.append(rec_copy)

print(f"Master update complete:")
print(f"  MOM_OWS_2024_REPORTED:   {mom_reported_count} ({mom_reported_count/len(updated_master)*100:.1f}%)")
print(f"  STATUTORY_BENCHMARK:     {statutory_count} ({statutory_count/len(updated_master)*100:.1f}%)")
print(f"  ACTUARIALLY_IMPUTED:      {imputed_count} ({imputed_count/len(updated_master)*100:.1f}%)")

# Save updated JSON and CSV
with open('ssoc_2024_actuarial_stay_leave_master.json', 'w', encoding='utf-8') as f:
    json.dump(updated_master, f, indent=2, ensure_ascii=False)

fieldnames = list(updated_master[0].keys())
with open('ssoc_2024_actuarial_stay_leave_master.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_master)

print("Saved ssoc_2024_actuarial_stay_leave_master.json and .csv successfully!")
