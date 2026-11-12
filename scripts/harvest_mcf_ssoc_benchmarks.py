import concurrent.futures
import datetime
import json
import os
import statistics
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict

BASE_URL = "https://api.mycareersfuture.gov.sg/v2/jobs"
PAGE_LIMIT = 100
MAX_WORKERS = 10
OUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data_mcf_2026_ssoc_summary.json",
)


def fetch_page(page: int, retries: int = 4) -> dict:
    url = f"{BASE_URL}?limit={PAGE_LIMIT}&page={page}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            if attempt == retries - 1:
                raise RuntimeError(f"Failed page {page} after {retries} attempts: {exc}") from exc
            time.sleep(0.5 * (2 ** attempt))
    return {}


def quantile(sorted_vals, q: float) -> int:
    if not sorted_vals:
        return 0
    if len(sorted_vals) == 1:
        return int(round(sorted_vals[0]))
    pos = q * (len(sorted_vals) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(sorted_vals) - 1)
    frac = pos - lo
    return int(round(sorted_vals[lo] + frac * (sorted_vals[hi] - sorted_vals[lo])))


def main():
    t_start = time.time()
    first = fetch_page(0)
    total_postings = int(first.get("total", 0))
    total_pages = (total_postings + PAGE_LIMIT - 1) // PAGE_LIMIT
    print(f"MCF live total: {total_postings:,} postings across {total_pages} pages.")

    all_results = list(first.get("results", []))
    remaining_pages = list(range(1, total_pages))

    failed_pages = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_page = {executor.submit(fetch_page, p): p for p in remaining_pages}
        done_count = 1
        for fut in concurrent.futures.as_completed(future_to_page):
            p = future_to_page[fut]
            done_count += 1
            try:
                data = fut.result()
                all_results.extend(data.get("results", []))
            except Exception as exc:
                failed_pages.append((p, str(exc)))
            if done_count % 100 == 0 or done_count == total_pages:
                print(f"Fetched {done_count}/{total_pages} pages ({len(all_results):,} jobs)...")

    if failed_pages:
        print(f"Warning: {len(failed_pages)} pages failed: {failed_pages[:5]}")

    seen_uuids = set()
    salary_types = Counter()
    rejected_reasons = Counter()

    by_ssoc = defaultdict(
        lambda: {
            "vacancies": 0,
            "apps_sum": 0,
            "perm_count": 0,
            "contract_count": 0,
            "mins": [],
            "maxs": [],
            "offers": [],
        }
    )

    for job in all_results:
        jid = job.get("uuid") or (job.get("metadata") or {}).get("jobPostId")
        if jid:
            if jid in seen_uuids:
                rejected_reasons["duplicate"] += 1
                continue
            seen_uuids.add(jid)

        ssoc = str(job.get("ssocCode") or "").strip()
        if len(ssoc) != 5:
            rejected_reasons["invalid_ssoc"] += 1
            continue

        meta = job.get("metadata") or {}
        apps = meta.get("totalNumberJobApplication")
        emp_types = [(e.get("employmentType") or "").lower() for e in (job.get("employmentTypes") or [])]

        bucket = by_ssoc[ssoc]
        bucket["vacancies"] += 1
        if isinstance(apps, (int, float)):
            bucket["apps_sum"] += int(apps)
        if any("permanent" in et or "full time" in et for et in emp_types):
            bucket["perm_count"] += 1
        elif any("contract" in et or "temporary" in et for et in emp_types):
            bucket["contract_count"] += 1

        if meta.get("isHideSalary"):
            rejected_reasons["hidden_salary"] += 1
            continue

        sal = job.get("salary") or {}
        smin = sal.get("minimum")
        smax = sal.get("maximum")
        stype = ((sal.get("type") or {}).get("salaryType") or "").strip()
        salary_types[stype] += 1

        if not isinstance(smin, (int, float)) or not isinstance(smax, (int, float)):
            rejected_reasons["missing_bounds"] += 1
            continue
        if smin <= 0 or smax < smin:
            rejected_reasons["invalid_bounds"] += 1
            continue

        if stype == "Monthly":
            m_min, m_max = float(smin), float(smax)
        elif stype == "Annually":
            m_min, m_max = float(smin) / 12.0, float(smax) / 12.0
        else:
            rejected_reasons[f"non_monthly_type:{stype}"] += 1
            continue

        # Sanity bounds and FCF compliance-padding filter (reject extreme >2.5x dummy spread or <$500/mo or >$200k/mo)
        if m_min < 500 or m_max > 200000:
            rejected_reasons["out_of_range_monthly"] += 1
            continue
        if m_max / m_min > 2.5:
            rejected_reasons["fcf_wide_band_gt_2.5x"] += 1
            continue

        # Conservative FCF clearing offer estimate: 40th percentile within [min, max]
        est_offer = m_min + 0.40 * (m_max - m_min)
        bucket["mins"].append(m_min)
        bucket["maxs"].append(m_max)
        bucket["offers"].append(est_offer)

    ssoc_summary = {}
    for ssoc, b in sorted(by_ssoc.items()):
        n_sal = len(b["offers"])
        vac = b["vacancies"]
        avg_apps = round(b["apps_sum"] / vac, 1) if vac > 0 else 0.0
        mins_s = sorted(b["mins"])
        maxs_s = sorted(b["maxs"])
        offers_s = sorted(b["offers"])
        entry = {
            "vacancies": vac,
            "salary_samples": n_sal,
            "avg_apps_per_vacancy": avg_apps,
            "perm_share_pct": round(100.0 * b["perm_count"] / vac, 1) if vac > 0 else 0.0,
        }
        if n_sal > 0:
            entry["p25_min_sgd"] = quantile(mins_s, 0.25)
            entry["p50_offer_sgd"] = int(round(statistics.median(offers_s)))
            entry["p75_max_sgd"] = quantile(maxs_s, 0.75)
        ssoc_summary[ssoc] = entry

    payload = {
        "harvest_timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": "MyCareersFuture v2 API (https://api.mycareersfuture.gov.sg/v2/jobs)",
        "total_unique_postings": len(seen_uuids),
        "ssoc_codes_with_postings": len(ssoc_summary),
        "ssoc_codes_with_clean_salaries": sum(1 for v in ssoc_summary.values() if v["salary_samples"] >= 1),
        "salary_type_distribution": dict(salary_types),
        "filter_stats": dict(rejected_reasons),
        "methodology": "Excludes hidden salaries, non-Monthly/Annual units, bounds <S$500 or >S$200k, and wide FCF compliance padding bands (max/min > 2.5x). Clearing estimate = min + 0.40*(max - min).",
        "ssoc_benchmarks": ssoc_summary,
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    elapsed = time.time() - t_start
    print(f"Done in {elapsed:.1f}s -> wrote {OUT_PATH}")
    print(f"Unique postings: {len(seen_uuids):,}")
    print(f"SSOC codes with postings: {len(ssoc_summary):,} (clean salary samples: {payload['ssoc_codes_with_clean_salaries']:,})")
    print(f"Salary types: {dict(salary_types)}")
    print(f"Filtered out: {dict(rejected_reasons)}")


if __name__ == "__main__":
    main()
