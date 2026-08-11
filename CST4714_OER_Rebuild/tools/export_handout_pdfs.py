#!/usr/bin/env python3
"""Export tagged PDF handouts from the 15 canonical PowerPoint decks."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MACOS_SOFFICE = Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")


def soffice_path() -> str:
    executable = shutil.which("soffice")
    if executable:
        return executable
    if MACOS_SOFFICE.is_file():
        return str(MACOS_SOFFICE)
    raise SystemExit("LibreOffice is required to export PDF handouts")


def main() -> None:
    decks = sorted(ROOT.glob("week_*/*.pptx"))
    if len(decks) != 15:
        raise SystemExit(f"Expected 15 decks, found {len(decks)}")

    filter_options = {
        "UseTaggedPDF": {"type": "boolean", "value": "true"},
        "ExportNotes": {"type": "boolean", "value": "false"},
        "ExportBookmarks": {"type": "boolean", "value": "true"},
    }
    conversion = "pdf:impress_pdf_Export:" + json.dumps(
        filter_options,
        separators=(",", ":"),
    )

    with tempfile.TemporaryDirectory(prefix="cst4714-pdf-export-") as temp:
        temp_root = Path(temp)
        output = temp_root / "output"
        profile = temp_root / "profile"
        output.mkdir()
        profile.mkdir()
        command = [
            soffice_path(),
            "--headless",
            f"-env:UserInstallation={profile.as_uri()}",
            "--convert-to",
            conversion,
            "--outdir",
            str(output),
            *(str(deck) for deck in decks),
        ]
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise SystemExit(result.stdout + result.stderr)

        for deck in decks:
            generated = output / f"{deck.stem}.pdf"
            if not generated.is_file() or generated.read_bytes()[:5] != b"%PDF-":
                raise SystemExit(f"LibreOffice did not create a valid PDF for {deck}")
            destination = deck.with_suffix(".pdf")
            shutil.copyfile(generated, destination)
            print(f"exported: {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
