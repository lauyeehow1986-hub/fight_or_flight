import csv
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOM_RAW_PATH = ROOT / "data_mom_ows_2024_raw.json"
MASTER_JSON_PATH = ROOT / "ssoc_2024_actuarial_stay_leave_master.json"
MASTER_CSV_PATH = ROOT / "ssoc_2024_actuarial_stay_leave_master.csv"

MOM_CITATION_PREFIX = "MOM Occupational Wage Survey 2024 (Data.gov.sg table d_9917e751f7498502f70052a940a3f312"

# Explicit, human-verified 1-to-1 SSOC 2024 <-> MOM OWS 2024 mappings where wording differs
# without using loose substring matching.
VERIFIED_SSOC_TO_MOM = {
    "11203": "chief operating officer/general manager",
    "13301": "chief information officer/chief technology officer/chief security officer",
    "13304": "ict service manager",
    "13410": "pre-school education manager",
    "13441": "social service manager",
    "13493": "media and broadcasting manager",
    "14330": "arts and cultural centre manager (including gallery and museum manager)",
    "21454": "food and drink technologist",
    "21531": "media and broadcasting engineer",
    "21662": "multimedia artist and animator",
    "21711": "chief engineer/second engineer (ship)",
    "22693": "medical diagnostic radiographer",
    "24154": "commodities and freight derivatives broker",
    "24320": "public relations/corporate communications professional",
    "24333": "ict sales and services professional",
    "24351": "commodities trader (excluding oil and bunker)",
    "25112": "ict business process consultant/business analyst",
    "25113": "enterprise/solution architect",
    "25123": "multimedia (including games) developer",
    "25151": "ict quality assurance specialist",
    "25152": "ict auditor",
    "25211": "database administrator",
    "25212": "database architect",
    "25220": "network, servers and computer systems administrator",
    "31001": "assistant civil and structural engineer",
    "31161": "chemical engineering technician",
    "31163": "chemical engineering technician (petrochemicals)",
    "31181": "mechanical draughtsman",
    "31182": "electrical/electronics draughtsman",
    "31183": "civil/structural engineering draughtsman",
    "33160": "financial markets back office administrator",
    "34210": "athlete/sportsman",
    "35220": "telecommunications technician",
    "51942": "keeper/trainer in zoological, bird and aquatic parks",
    "61131": "landscape and plant nursery supervisor",
    "61133": "gardener and horticultural worker",
    "75440": "fumigator and other pest and weed controller",
    "83211": "motorcycle delivery man",
    "83212": "delivery man using motorised personal mobility aids/devices",
    "91131": "office, commercial and industrial establishments indoor cleaner",
    "91132": "office, commercial and industrial establishments outdoor cleaner",
    "91133": "office, commercial and industrial establishments multi-skilled cleaner cum machine operator",
    "91151": "food and beverage establishments general cleaner",
    "96101": "general waste collection, recycling and material recovery worker",
    "96261": "building caretaker/watchman",
}

# Codes with explicit, documented market-reality adjustments where MOM establishment survey
# pools junior/field headcount underneath the statutory/generic SSOC title.
PRESERVE_CALIBRATED_BASE = {"21221"}

MAJOR_GROUP_CITATIONS = {
    "1": "SSOC Major Group 1 (Managers & Senior Officials) Cross-Sectional Imputation from MOM OWS 2024 Peer Benchmarks",
    "2": "SSOC Major Group 2 (Professionals) Cross-Sectional Imputation from MOM OWS 2024 Peer Benchmarks",
    "3": "SSOC Major Group 3 (Associate Professionals & Technicians) Cross-Sectional Imputation from MOM OWS 2024 Peer Benchmarks",
    "4": "SSOC Major Group 4 (Clerical Support Workers) Cross-Sectional Imputation from MOM OWS 2024 Peer Benchmarks",
    "5": "SSOC Major Group 5 (Service & Sales Workers) Cross-Sectional Imputation from MOM OWS 2024 Peer Benchmarks",
    "6": "SSOC Major Group 6 (Agricultural & Fishery Workers) Cross-Sectional Imputation from MOM OWS 2024 Peer Benchmarks",
    "7": "SSOC Major Group 7 (Craftsmen & Related Trades Workers) Cross-Sectional Imputation from MOM OWS 2024 Peer Benchmarks",
    "8": "SSOC Major Group 8 (Plant & Machine Operators & Assemblers) Cross-Sectional Imputation from MOM OWS 2024 Peer Benchmarks",
    "9": "SSOC Major Group 9 (Cleaners, Labourers & Related Workers) Cross-Sectional Imputation from MOM OWS 2024 Peer Benchmarks",
}


def norm_keep_parens(s: str) -> str:
    s = s.lower().strip()
    s = s.replace("pre-school", "preschool")
    s = s.replace("information and communications technology (ict)", "ict")
    s = s.replace("information and communications technology", "ict")
    s = s.replace("human resource (hr)", "human resource")
    s = s.replace("public relations (pr)", "public relations")
    s = s.replace("chief operating officer (coo)", "chief operating officer")
    s = s.replace("chief executive officer (ceo)", "chief executive officer")
    s = s.replace("food and beverage (f&b)", "food and beverage")
    s = s.replace("research and development (r&d)", "research and development")
    s = s.replace("(it)", "")
    s = s.replace("draughtsman", "draughtsperson")
    s = s.replace("salesman", "salesperson")
    s = s.replace("delivery man", "delivery person")
    s = s.replace("sportsman", "athlete")
    s = s.replace("except", "excluding")
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    tokens = [t for t in s.split() if t not in {"and", "the"}]
    return " ".join(tokens)


def norm_no_parens(s: str) -> str:
    s = re.sub(r"\((?:e\.g\.|including|excluding|except)[^)]*\)", "", s.lower().strip())
    return norm_keep_parens(s)


def recompute_dependent_fields(row: dict, old_p50: float) -> None:
    p50 = float(row["p50_median_monthly_base_sgd"])
    bonus_m = float(row.get("typical_bonus_months", 2.0))
    leave_inc = float(row.get("definite_leave_min_increment_pct", 20.0))

    row["total_annual_cash_p50_sgd"] = round(p50 * (12.0 + bonus_m))
    target_base = round(p50 * (1.0 + leave_inc / 100.0))
    row["definite_leave_target_monthly_base_sgd"] = target_base
    row["definite_leave_target_annual_cash_sgd"] = round(target_base * (12.0 + bonus_m))

    if old_p50 > 0 and old_p50 != p50:
        scale = p50 / old_p50
        if row.get("bellman_indifference_counteroffer_base_sgd") is not None:
            row["bellman_indifference_counteroffer_base_sgd"] = round(
                row["bellman_indifference_counteroffer_base_sgd"] * scale
            )
        if row.get("bellman_indifference_total_annual_sgd") is not None:
            row["bellman_indifference_total_annual_sgd"] = round(
                row["bellman_indifference_total_annual_sgd"] * scale
            )
        if row.get("sideline_monthly_gross_sgd") is not None:
            sl_m = round(row["sideline_monthly_gross_sgd"] * scale)
            sl_a = sl_m * 12
            row["sideline_monthly_gross_sgd"] = sl_m
            row["sideline_annual_gross_sgd"] = sl_a
            nti = round(sl_a * 0.88)
            row["sideline_net_trade_income_sgd"] = nti
            ms_rate = float(row.get("sideline_medisave_rate_pct", 9.0)) / 100.0
            max_cap = round(102000 * ms_rate)
            ms_amt = round(min(max_cap, nti * ms_rate)) if nti > 6000 else 0
            row["sideline_annual_medisave_sgd"] = ms_amt
            row["sideline_annual_net_cash_sgd"] = nti - ms_amt


def main() -> None:
    mom_raw = json.loads(MOM_RAW_PATH.read_text(encoding="utf-8"))
    master = json.loads(MASTER_JSON_PATH.read_text(encoding="utf-8"))

    mom_by_exact = {}
    mom_by_keep = {}
    mom_by_noparen = {}
    for rec in mom_raw:
        occ_lower = rec["occ_desc"].lower().strip()
        mom_by_exact[occ_lower] = rec
        mom_by_keep.setdefault(norm_keep_parens(occ_lower), []).append(rec)
        mom_by_noparen.setdefault(norm_no_parens(occ_lower), []).append(rec)

    matched_count = 0
    unmatched_imputations = 0
    statutory_count = 0
    used_mom_ids = set()
    mom_peer_rows = []
    old_p50_map = {}

    # Pass 1: Assign authoritative STATUTORY_BENCHMARK and MOM_OWS_2024_REPORTED rows
    for row in master:
        code = str(row["ssoc_code"])
        title = str(row["ssoc_title"])
        t_lower = title.lower().strip()
        old_p50_map[code] = float(row["p50_median_monthly_base_sgd"])

        if row.get("wage_data_source_tier") == "STATUTORY_BENCHMARK":
            statutory_count += 1
            continue

        matched_rec = None
        is_nec = "n.e.c." in t_lower

        if code in VERIFIED_SSOC_TO_MOM:
            matched_rec = mom_by_exact.get(VERIFIED_SSOC_TO_MOM[code])
            if matched_rec is None:
                raise KeyError(f"Manual mapping target missing in MOM raw for {code}: {VERIFIED_SSOC_TO_MOM[code]}")
        elif not is_nec:
            if t_lower in mom_by_exact:
                matched_rec = mom_by_exact[t_lower]
            else:
                k_hits = mom_by_keep.get(norm_keep_parens(t_lower), [])
                if len(k_hits) == 1:
                    matched_rec = k_hits[0]
                else:
                    np_hits = mom_by_noparen.get(norm_no_parens(t_lower), [])
                    if len(np_hits) == 1 and "n.e.c." not in np_hits[0]["occ_desc"].lower():
                        matched_rec = np_hits[0]

        if matched_rec is not None:
            matched_count += 1
            used_mom_ids.add(matched_rec["_id"])
            rb25 = int(round(float(matched_rec["mthly_basic_wage_25_pctile"])))
            rb50 = int(round(float(matched_rec["mthly_basic_wage_50_pctile"])))
            rb75 = int(round(float(matched_rec["mthly_basic_wage_75_pctile"])))
            rg50 = int(round(float(matched_rec["mthly_gross_wage_50_pctile"])))

            row["wage_data_source_tier"] = "MOM_OWS_2024_REPORTED"
            row["is_officially_reported"] = True
            row["official_reported_p25_sgd"] = rb25
            row["official_reported_p50_sgd"] = rb50
            row["official_reported_p75_sgd"] = rb75
            row["official_reported_gross_p50_sgd"] = rg50
            row["wage_citation"] = f"{MOM_CITATION_PREFIX}, '{matched_rec['occ_desc']}')"

            if code not in PRESERVE_CALIBRATED_BASE:
                row["p25_monthly_base_sgd"] = rb25
                row["p50_median_monthly_base_sgd"] = rb50
                row["p75_monthly_base_sgd"] = rb75

            mom_peer_rows.append(row)
        else:
            row["wage_data_source_tier"] = "ACTUARIALLY_IMPUTED"
            row["is_officially_reported"] = False
            row["official_reported_p25_sgd"] = None
            row["official_reported_p50_sgd"] = None
            row["official_reported_p75_sgd"] = None
            row["official_reported_gross_p50_sgd"] = None

    # Pass 2: Hierarchical MOM OWS 2024 peer imputation for all ACTUARIALLY_IMPUTED codes
    # Lookup hierarchy: 4-digit (n>=1) -> 3-digit (n>=2) -> 3-digit (n>=1) -> 2-digit (n>=1) -> 1-digit (n>=1)
    for row in master:
        code = str(row["ssoc_code"])
        if row.get("wage_data_source_tier") == "ACTUARIALLY_IMPUTED":
            unmatched_imputations += 1
            chosen_peers = []
            chosen_k = None
            for k, min_n in ((4, 1), (3, 2), (3, 1), (2, 1), (1, 1)):
                peers = [p for p in mom_peer_rows if str(p["ssoc_code"])[:k] == code[:k]]
                if len(peers) >= min_n:
                    chosen_peers = peers
                    chosen_k = k
                    break

            if chosen_peers:
                row["p25_monthly_base_sgd"] = round(
                    statistics.median(p["official_reported_p25_sgd"] for p in chosen_peers)
                )
                row["p50_median_monthly_base_sgd"] = round(
                    statistics.median(p["official_reported_p50_sgd"] for p in chosen_peers)
                )
                row["p75_monthly_base_sgd"] = round(
                    statistics.median(p["official_reported_p75_sgd"] for p in chosen_peers)
                )
                row["wage_citation"] = (
                    f"SSOC {chosen_k}-Digit Peer Group ({code[:chosen_k]}*, n={len(chosen_peers)}) "
                    f"Hierarchical Median Imputation from MOM OWS 2024"
                )
            else:
                row["wage_citation"] = MAJOR_GROUP_CITATIONS.get(
                    code[:1],
                    "SSOC 2024 Actuarial Cross-Sectional Imputation (Armed Forces / Unclassified)",
                )

        recompute_dependent_fields(row, old_p50_map[code])

    MASTER_JSON_PATH.write_text(json.dumps(master, indent=2), encoding="utf-8")
    fieldnames = list(master[0].keys())
    with MASTER_CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(master)

    update_readme_summary(master)

    print(
        f"Updated {len(master)} SSOC records: "
        f"MOM_OWS_2024_REPORTED={matched_count} ({len(used_mom_ids)} unique MOM rows), "
        f"STATUTORY_BENCHMARK={statutory_count}, "
        f"ACTUARIALLY_IMPUTED={unmatched_imputations}"
    )


def update_readme_summary(master: list) -> None:
    readme_path = ROOT / "README.md"
    if not readme_path.exists():
        return

    group_labels = [
        ("1", "**1 - Managers & Senior Officials**"),
        ("2", "**2 - Professionals**"),
        ("3", "**3 - Associate Professionals & Technicians**"),
        ("4", "**4 - Clerical Support Workers**"),
        ("5", "**5 - Service & Sales Workers**"),
        ("6", "**6 - Agricultural & Fishery Workers**"),
        ("7", "**7 - Craftsmen & Related Trades Workers**"),
        ("8", "**8 - Plant & Machine Operators & Drivers**"),
        ("9", "**9 - Cleaners, Labourers & Elementary**"),
        ("X", "**X - Armed Forces & Unclassified**"),
    ]
    lines = [
        "### Summary Across Major SSOC Groups",
        "| Major SSOC Group | Occs | Median Base ($P_{50}$) | Definite Leave Threshold | Required Counteroffer | Sideline Monthly Gross | Sideline Annual Net Cash |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for g, label in group_labels:
        rows = [r for r in master if str(r["ssoc_code"])[:1] == g]
        if not rows:
            continue
        med_p50 = round(statistics.median(r["p50_median_monthly_base_sgd"] for r in rows))
        med_leave = statistics.median(r["definite_leave_min_increment_pct"] for r in rows)
        med_co_base = round(statistics.median(r["bellman_indifference_counteroffer_base_sgd"] for r in rows))
        med_co_pct = statistics.median(r["bellman_counteroffer_required_raise_pct"] for r in rows)
        med_sl_mo = round(statistics.median(r["sideline_monthly_gross_sgd"] for r in rows))
        med_sl_net = round(statistics.median(r["sideline_annual_net_cash_sgd"] for r in rows))
        lines.append(
            f"| {label} | {len(rows)} | **S${med_p50:,} / mo** | **+{med_leave:.1f}%** | "
            f"**S${med_co_base:,} / mo (+{med_co_pct:.1f}%)** | **S${med_sl_mo:,} / mo** | **S${med_sl_net:,} / yr** |"
        )

    new_block = "\n".join(lines)
    raw = readme_path.read_bytes()
    has_crlf = b"\r\n" in raw
    text = raw.decode("utf-8").replace("\r\n", "\n")
    text = re.sub(
        r"### Summary Across Major SSOC Groups\n(?:\|.*\n)+",
        new_block + "\n",
        text,
        count=1,
    )
    text = text.replace(
        "(`ssoc_career_actuarial_visualizer.html`)",
        "(`index.html`)",
    ).replace(
        "2026 CPF Self-Employed Person (SEP) MediSave contribution (9% on Net Trade Income > S$6,000, capped at S$8,160).",
        "2026 CPF Self-Employed Person (SEP) MediSave contribution (age-tiered 8%–10.5% on Net Trade Income up to S$102,000, capped at S$8,160–S$10,710/yr with S$6k–S$18k phase-in).",
    )
    readme_path.write_bytes((text.replace("\n", "\r\n") if has_crlf else text).encode("utf-8"))
    print("Synced README.md Summary Across Major SSOC Groups with true dataset medians:\n" + new_block)


if __name__ == "__main__":
    main()
