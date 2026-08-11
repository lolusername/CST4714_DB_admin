#!/usr/bin/env python3
"""Set accurate, deterministic core metadata in every authored PowerPoint deck."""

from __future__ import annotations

import os
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHOR = "Atilio Barreda"
SUBJECT = "CST 4714 Database Administration"
KEYWORDS = "database administration; PostgreSQL; MongoDB; cloud databases; OER"
MODIFIED = "2026-08-09T00:00:00Z"

NS = {
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

ET.register_namespace("", NS["cp"])
ET.register_namespace("dc", NS["dc"])
ET.register_namespace("dcterms", NS["dcterms"])
ET.register_namespace("xsi", NS["xsi"])


def transcript_title(deck: Path) -> tuple[int, str]:
    transcript = deck.with_name(f"{deck.stem}_transcript.md")
    first_line = transcript.read_text(encoding="utf-8").splitlines()[0]
    match = re.fullmatch(
        r"# Week (\d+): (.+) - Spoken Transcript",
        first_line,
    )
    if match is None:
        raise ValueError(f"Unexpected transcript title: {transcript}")
    return int(match.group(1)), f"Week {match.group(1)}: {match.group(2)}"


def set_text(root: ET.Element, namespace: str, name: str, value: str) -> ET.Element:
    tag = f"{{{NS[namespace]}}}{name}"
    element = root.find(tag)
    if element is None:
        element = ET.SubElement(root, tag)
    element.text = value
    return element


def updated_core_xml(core_xml: bytes, week: int, title: str) -> bytes:
    root = ET.fromstring(core_xml.lstrip(b"\xef\xbb\xbf"))
    set_text(root, "dc", "creator", AUTHOR)
    set_text(root, "cp", "lastModifiedBy", AUTHOR)
    set_text(root, "dc", "title", title)
    set_text(root, "dc", "subject", SUBJECT)
    set_text(
        root,
        "dc",
        "description",
        f"Week {week} presentation for Operating Cloud Databases.",
    )
    set_text(root, "dc", "language", "en-US")
    set_text(root, "cp", "keywords", KEYWORDS)
    set_text(root, "cp", "category", "Open Educational Resource")
    set_text(root, "cp", "contentStatus", "Release Candidate")
    modified = set_text(root, "dcterms", "modified", MODIFIED)
    modified.set(f"{{{NS['xsi']}}}type", "dcterms:W3CDTF")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def update_deck(deck: Path) -> bool:
    week, title = transcript_title(deck)
    temp_path = deck.with_suffix(".pptx.tmp")
    try:
        with zipfile.ZipFile(deck) as source:
            source.testzip()
            original = source.read("docProps/core.xml")
            replacement = updated_core_xml(original, week, title)
            if replacement == original:
                return False

            with zipfile.ZipFile(temp_path, "w") as destination:
                destination.comment = source.comment
                for info in source.infolist():
                    data = (
                        replacement
                        if info.filename == "docProps/core.xml"
                        else source.read(info.filename)
                    )
                    destination.writestr(info, data)

        with zipfile.ZipFile(temp_path) as candidate:
            if candidate.testzip() is not None:
                raise ValueError(f"Corrupt rewritten archive: {deck}")
            ET.fromstring(candidate.read("docProps/core.xml"))
        os.replace(temp_path, deck)
        return True
    finally:
        temp_path.unlink(missing_ok=True)


def main() -> None:
    decks = sorted(ROOT.glob("week_*/*.pptx"))
    if len(decks) != 15:
        raise SystemExit(f"Expected 15 decks, found {len(decks)}")
    for deck in decks:
        state = "updated" if update_deck(deck) else "unchanged"
        print(f"{state}: {deck.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
