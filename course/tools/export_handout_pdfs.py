#!/usr/bin/env python3
"""Export tagged PDF handouts from the 15 canonical PowerPoint decks."""

from __future__ import annotations

import json
import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def soffice_path() -> str:
    explicit = os.environ.get("SOFFICE")
    if explicit:
        if not Path(explicit).is_file():
            raise SystemExit(f"SOFFICE does not name a file: {explicit}")
        return explicit
    executable = shutil.which("soffice")
    if executable:
        return executable
    raise SystemExit("Set SOFFICE to a headless LibreOffice executable to export handouts")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deck", action="append", type=Path)
    args = parser.parse_args()
    decks = [path.resolve() for path in args.deck] if args.deck else sorted(ROOT.glob("weeks/week_*/*.pptx"))
    if not args.deck and len(decks) != 15:
        raise SystemExit(f"Expected 15 decks, found {len(decks)}")

    filter_options = {
        "UseTaggedPDF": {"type": "boolean", "value": "true"},
        "ExportNotes": {"type": "boolean", "value": "false"},
        "ExportBookmarks": {"type": "boolean", "value": "true"},
        "DisplayPDFDocumentTitle": {"type": "boolean", "value": "true"},
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
        environment = os.environ.copy()
        # The bundled macOS converter needs an explicit system-font configuration.
        fontconfig = Path("/opt/homebrew/etc/fonts/fonts.conf")
        if "FONTCONFIG_FILE" not in environment and fontconfig.is_file():
            environment["FONTCONFIG_FILE"] = str(fontconfig)
            environment["FONTCONFIG_PATH"] = str(fontconfig.parent)
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            env=environment,
        )
        if result.returncode != 0:
            raise SystemExit(result.stdout + result.stderr)

        for deck in decks:
            generated = output / f"{deck.stem}.pdf"
            if not generated.is_file() or generated.read_bytes()[:5] != b"%PDF-":
                raise SystemExit(f"LibreOffice did not create a valid PDF for {deck}")
            destination = deck.with_suffix(".pdf")
            shutil.copyfile(generated, destination)
            print(f"exported: {destination}")


if __name__ == "__main__":
    main()
