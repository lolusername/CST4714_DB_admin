#!/usr/bin/env python3
"""Render and pixel-compare two matching sets of weekly PDF handouts."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require_tool(name: str) -> str:
    executable = shutil.which(name)
    if executable is None:
        raise SystemExit(f"Required command is unavailable: {name}")
    return executable


def render(pdf: Path, destination: Path, pdftoppm: str) -> list[Path]:
    destination.mkdir(parents=True)
    prefix = destination / "page"
    result = subprocess.run(
        [pdftoppm, "-png", "-r", "96", str(pdf), str(prefix)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Could not render {pdf}: {result.stderr.strip()}")
    return sorted(destination.glob("page-*.png"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", nargs="?", type=Path, default=ROOT)
    args = parser.parse_args()

    reference_input = args.reference.resolve()
    candidate_input = args.candidate.resolve()
    pdftoppm = require_tool("pdftoppm")
    compare = require_tool("compare")
    pairs: list[tuple[Path, Path, Path]] = []
    if reference_input.is_file() and candidate_input.is_file():
        pairs.append((reference_input, candidate_input, Path(candidate_input.name)))
    elif reference_input.is_dir() and candidate_input.is_dir():
        candidates = sorted(candidate_input.glob("week_*/*.pdf"))
        if len(candidates) != 15:
            raise SystemExit(f"Expected 15 candidate PDFs, found {len(candidates)}")
        for candidate in candidates:
            relative = candidate.relative_to(candidate_input)
            reference = reference_input / relative
            if not reference.is_file():
                raise SystemExit(f"Missing reference PDF: {reference}")
            pairs.append((reference, candidate, relative))
    else:
        raise SystemExit("Reference and candidate must both be PDF files or directories")

    compared_pages = 0
    changed_pages: list[str] = []
    with tempfile.TemporaryDirectory(prefix="cst4714-pdf-compare-") as temp:
        temp_root = Path(temp)
        for reference, candidate, relative in pairs:
            key = relative.parent.name if relative.parent.name else candidate.stem
            reference_pages = render(
                reference,
                temp_root / "reference" / key,
                pdftoppm,
            )
            candidate_pages = render(
                candidate,
                temp_root / "candidate" / key,
                pdftoppm,
            )
            if len(reference_pages) != len(candidate_pages):
                raise SystemExit(
                    f"Page-count mismatch for {relative}: "
                    f"{len(reference_pages)} != {len(candidate_pages)}"
                )

            for page_number, (before, after) in enumerate(
                zip(reference_pages, candidate_pages, strict=True),
                start=1,
            ):
                result = subprocess.run(
                    [compare, "-metric", "AE", str(before), str(after), "null:"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                metric = result.stderr.strip()
                if result.returncode not in {0, 1}:
                    raise RuntimeError(
                        f"Image comparison failed for {relative} page {page_number}: "
                        f"{metric}"
                    )
                try:
                    absolute_error = float(metric.split()[0])
                except (IndexError, ValueError) as exc:
                    raise RuntimeError(
                        f"Unexpected comparison metric for {relative} page "
                        f"{page_number}: {metric}"
                    ) from exc
                if absolute_error != 0:
                    changed_pages.append(f"{relative} page {page_number}: AE={metric}")
                compared_pages += 1

    if changed_pages:
        print("PDF render comparison: FAIL")
        for changed in changed_pages:
            print(f"- {changed}")
        raise SystemExit(1)
    print(
        f"PDF render comparison: PASS ({compared_pages} pages are pixel-identical at 96 DPI)"
    )


if __name__ == "__main__":
    main()
