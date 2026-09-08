"""Build versioned public-data teaching fixtures.

The script downloads public source data, selects documented fields, and writes a
small classroom snapshot. It does not contain credentials or student data.
"""

from __future__ import annotations

import csv
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
CISA_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


def build_cisa_kev_sample(limit: int = 75) -> None:
    request = Request(CISA_URL, headers={"User-Agent": "CST4714-OER-dataset-builder/1.0"})
    with urlopen(request, timeout=30) as response:
        source = json.load(response)

    selected_fields = (
        "cveID",
        "vendorProject",
        "product",
        "vulnerabilityName",
        "dateAdded",
        "dueDate",
        "knownRansomwareCampaignUse",
        "cwes",
    )
    records = [
        {field: item.get(field) for field in selected_fields}
        for item in source["vulnerabilities"][:limit]
    ]

    output_dir = ROOT / "datasets" / "cisa_kev_sample"
    output_dir.mkdir(parents=True, exist_ok=True)

    snapshot = {
        "title": source.get("title"),
        "catalogVersion": source.get("catalogVersion"),
        "sourceDateReleased": source.get("dateReleased"),
        "retrievedAt": datetime.now(timezone.utc).isoformat(),
        "sourceUrl": CISA_URL,
        "selection": f"first {len(records)} source records; documented fields only",
        "count": len(records),
        "vulnerabilities": records,
    }
    (output_dir / "kev_sample.json").write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    with (output_dir / "kev_sample.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=selected_fields, lineterminator="\n")
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["cwes"] = "|".join(record.get("cwes") or [])
            writer.writerow(row)


def main() -> None:
    build_cisa_kev_sample()


if __name__ == "__main__":
    main()
