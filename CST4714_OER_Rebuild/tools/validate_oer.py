#!/usr/bin/env python3
"""Validate the public CST4714 OER package with only the Python standard library."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import struct
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEEK_RE = re.compile(r"week_(\d{2})$")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
URL_RE = re.compile(r"https?://[^\s<>\"'\\\]\)]+")
SLIDE_SECTION_RE = re.compile(r"^## Slide (\d+):[^\n]*\n", re.MULTILINE)
NON_LINK_URI_PREFIXES = (
    "http://purl.org/dc/",
    "http://schemas.openxmlformats.org/",
    "http://www.idpf.org/",
    "http://www.w3.org/2001/XMLSchema-instance",
)
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}
CORE_NS = {
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
}
EPUB_NS = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "opf": "http://www.idpf.org/2007/opf",
}
WORD_NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if condition:
            self.passes.append(message)
        else:
            self.errors.append(message)

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_prose(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def check_structure(report: Report) -> None:
    weeks = sorted(path for path in ROOT.glob("week_*") if path.is_dir())
    expected_weeks = [ROOT / f"week_{number:02d}" for number in range(1, 16)]
    report.require(weeks == expected_weeks, "15 weekly directories are present")

    modules = sorted((ROOT / "textbook").glob("module_*.md"))
    labs = sorted(ROOT.glob("week_*/lab_*.md"))
    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    dataset_dirs = sorted(path for path in (ROOT / "datasets").iterdir() if path.is_dir())
    assessment_files = sorted(path for path in (ROOT / "assessments").glob("*.md"))

    report.require(len(modules) == 15, "15 open-text modules are present")
    report.require(len(labs) == 25, "25 individual lab files are present")
    report.require(len(notebooks) == 6, "6 educational notebooks are present")
    report.require(len(dataset_dirs) == 3, "3 reusable data packages are present")
    report.require(len(assessment_files) == 6, "6 assessment resources are present")

    required_root_files = {
        "README.md",
        "OER_CATALOG.md",
        "FREE_EXTERNAL_RESOURCES.md",
        "ATTRIBUTIONS.md",
        "LICENSE.md",
        "CITATION.cff",
        "course_map.md",
        "syllabus.md",
        "midterm_project.md",
        "final_project.md",
        "RELEASE_CHECKLIST.md",
        "RELEASE_NOTES.md",
    }
    for name in sorted(required_root_files):
        report.require((ROOT / name).is_file(), f"required package file exists: {name}")

    report.require(
        (ROOT / "fellowship/CURRENTNESS_PEDAGOGY_QA_AUDIT.md").is_file(),
        "currentness and pedagogy audit record exists",
    )
    accessibility_report = (
        ROOT / "fellowship/STANDALONE_HTML_ACCESSIBILITY_QA.md"
    )
    report.require(
        accessibility_report.is_file(),
        "standalone HTML accessibility QA record exists",
    )
    if accessibility_report.is_file():
        accessibility_text = read_text(accessibility_report)
        fellowship_index = read_text(ROOT / "fellowship/README.md")
        report.require(
            "Representative Safari keyboard result: PASS" in accessibility_text
            and "Screen-reader test: NOT RUN" in accessibility_text
            and "STANDALONE_HTML_ACCESSIBILITY_QA.md" in fellowship_index,
            "accessibility record distinguishes completed and pending checks",
        )

    format_report = ROOT / "fellowship/PUBLICATION_FORMAT_QA.md"
    report.require(
        format_report.is_file(),
        "publication-format QA record exists",
    )
    if format_report.is_file():
        format_text = read_text(format_report)
        fellowship_index = read_text(ROOT / "fellowship/README.md")
        report.require(
            "EPUBCheck 5.3.0 result: PASS" in format_text
            and "0 fatals / 0 errors / 0 warnings / 0 infos" in format_text
            and "PDF handout accessibility claim: NOT MADE" in format_text
            and "Screen-reader test: NOT RUN" in format_text
            and "PUBLICATION_FORMAT_QA.md" in fellowship_index,
            "publication-format record distinguishes conformance from external review",
        )

    unwanted = [
        path
        for path in ROOT.rglob("*")
        if path.name == "__pycache__"
        or path.suffix == ".pyc"
        or path.name.endswith(".inspect.ndjson")
        or "deck_builder" in path.name.lower()
        or "slide_generator" in path.name.lower()
        or "answer_key" in path.name.lower()
        or "cheat_sheet" in path.name.lower()
    ]
    report.require(
        not unwanted,
        "no cache, inspection, slide-builder, answer-key, or cheat-sheet files are public",
    )
    for path in unwanted:
        report.fail(f"remove non-release artifact: {relative(path)}")


def check_markdown_links(report: Report) -> None:
    checked = 0
    for source in sorted(ROOT.rglob("*.md")):
        text = read_text(source)
        for match in MARKDOWN_LINK_RE.finditer(text):
            raw_target = match.group(1).strip()
            if raw_target.startswith("<") and ">" in raw_target:
                target = raw_target[1 : raw_target.index(">")]
            else:
                target = raw_target.split(maxsplit=1)[0]
            target = target.strip()
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            decoded = urllib.parse.unquote(target.split("#", 1)[0].split("?", 1)[0])
            destination = (source.parent / decoded).resolve()
            checked += 1
            if not destination.exists():
                report.fail(
                    f"broken relative link in {relative(source)}: {target}"
                )
    report.require(checked > 100, f"checked {checked} relative Markdown links")


def check_json_csv_and_notebooks(report: Report) -> None:
    json_files = sorted(
        path for path in ROOT.rglob("*.json") if path.suffix != ".ipynb"
    )
    for path in json_files:
        try:
            json.loads(read_text(path))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            report.fail(f"invalid JSON in {relative(path)}: {exc}")
    report.require(bool(json_files), f"parsed {len(json_files)} JSON data files")

    csv_files = sorted(ROOT.rglob("*.csv"))
    total_rows = 0
    for path in csv_files:
        try:
            with path.open(newline="", encoding="utf-8-sig") as handle:
                reader = csv.DictReader(handle)
                rows = list(reader)
            if not reader.fieldnames or any(not field for field in reader.fieldnames):
                report.fail(f"missing or empty CSV header in {relative(path)}")
            if not rows:
                report.fail(f"CSV has no data rows: {relative(path)}")
            if any(None in row for row in rows):
                report.fail(f"CSV row has more fields than its header: {relative(path)}")
            total_rows += len(rows)
        except (csv.Error, UnicodeDecodeError) as exc:
            report.fail(f"invalid CSV in {relative(path)}: {exc}")
    report.require(len(csv_files) == 6, f"parsed {len(csv_files)} CSV files")
    report.require(total_rows == 137, f"validated {total_rows} CSV data rows")

    kev_path = ROOT / "datasets/cisa_kev_sample/kev_sample.json"
    if kev_path.exists():
        kev = json.loads(read_text(kev_path))
        report.require(
            kev.get("count") == 75 and len(kev.get("vulnerabilities", [])) == 75,
            "CISA teaching snapshot contains its documented 75 records",
        )

    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    notebook_code: dict[str, str] = {}
    for path in notebooks:
        try:
            notebook = json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            report.fail(f"invalid notebook JSON in {relative(path)}: {exc}")
            continue
        cells = notebook.get("cells", [])
        report.require(bool(cells), f"notebook has cells: {path.name}")
        errors = [
            output
            for cell in cells
            for output in cell.get("outputs", [])
            if output.get("output_type") == "error"
        ]
        if errors:
            report.fail(f"notebook contains saved error output: {relative(path)}")
        source_text = "\n".join(
            "".join(cell.get("source", [])) for cell in cells
        )
        report.require(
            "colab.research.google.com" in source_text,
            f"notebook has an Open in Colab link: {path.name}",
        )
        code_text = "\n".join(
            "".join(cell.get("source", []))
            for cell in cells
            if cell.get("cell_type") == "code"
        )
        notebook_code[path.name] = code_text
        if re.search(r"tlsInsecure\s*=\s*True", code_text, re.IGNORECASE):
            report.fail(f"unsafe tlsInsecure=True in {relative(path)}")
        if re.search(r"sslmode\s*=\s*['\"]?disable", code_text, re.IGNORECASE):
            report.fail(f"unsafe sslmode=disable in {relative(path)}")

    disabled_markers = {
        "02_postgres_transactions_locks.ipynb": "USE_CLOUD = False",
        "04_atlas_mql_modeling.ipynb": "USE_ATLAS = False",
        "05_mongodb_logical_recovery.ipynb": "USE_ATLAS = False",
        "06_public_data_capacity_integration.ipynb": "LOAD_ATLAS = False",
    }
    report.require(
        all(marker in notebook_code.get(name, "") for name, marker in disabled_markers.items())
        and "LOAD_POSTGRES = False"
        in notebook_code.get("06_public_data_capacity_integration.ipynb", ""),
        "all optional cloud notebook paths default to disabled",
    )
    cloud_notebooks = [
        notebook_code.get(name, "")
        for name in disabled_markers
    ]
    report.require(
        all("getpass(" in code for code in cloud_notebooks),
        "cloud notebooks request connection secrets at runtime",
    )
    atlas_notebooks = [
        notebook_code.get(name, "")
        for name in [
            "04_atlas_mql_modeling.ipynb",
            "05_mongodb_logical_recovery.ipynb",
            "06_public_data_capacity_integration.ipynb",
        ]
    ]
    report.require(
        all(
            'ServerApi("1", strict=True, deprecation_errors=True)' in code
            and "serverSelectionTimeoutMS=" in code
            and "timeoutMS=" in code
            and '.admin.command("ping")' in code
            for code in atlas_notebooks
        ),
        "Atlas notebook paths use Stable API, bounded waits, and ping",
    )
    postgres_notebooks = [
        notebook_code.get("02_postgres_transactions_locks.ipynb", ""),
        notebook_code.get("06_public_data_capacity_integration.ipynb", ""),
    ]
    report.require(
        all(
            "conninfo_to_dict" in code
            and "connect_timeout=10" in code
            and '{"require", "verify-ca", "verify-full"}' in code
            for code in postgres_notebooks
        ),
        "PostgreSQL notebook paths require encrypted transport and bounded connects",
    )
    report.require(
        "DROP SCHEMA IF EXISTS lock_lab CASCADE"
        in postgres_notebooks[0]
        and "session_a.close()" in postgres_notebooks[0]
        and 'delete_many({"course_fixture": "cst4714"})' in atlas_notebooks[0]
        and "client.drop_database(SOURCE_DB)" in atlas_notebooks[1]
        and 'delete_many({"cveID": {"$in": fixture_ids}})' in atlas_notebooks[2]
        and "DROP SCHEMA IF EXISTS cst4714_oer CASCADE" in atlas_notebooks[2],
        "cloud notebook cleanup is bounded to disposable course artifacts",
    )


def check_publication(report: Report) -> None:
    version = "1.0.0-rc.1"
    publication = ROOT / "publication"
    exports = publication / "exports"
    stem = f"operating_cloud_databases_v{version}"
    html = exports / f"{stem}.html"
    epub = exports / f"{stem}.epub"
    docx = exports / f"{stem}.docx"
    cover = publication / "cover.png"
    manifest = exports / "SHA256SUMS.txt"

    required = [
        publication / "README.md",
        publication / "book_metadata.yaml",
        publication / "front_matter.md",
        publication / "back_matter.md",
        publication / "operating_cloud_databases.css",
        publication / "cover.svg",
        cover,
        html,
        epub,
        docx,
        manifest,
    ]
    for path in required:
        report.require(path.is_file(), f"publication artifact exists: {relative(path)}")
    if not all(path.is_file() for path in [cover, html, epub, docx, manifest]):
        return

    html_text = read_text(html)
    report.require(
        all(f"Module {number}:" in html_text for number in range(1, 16)),
        "standalone HTML contains all 15 modules",
    )
    report.require(
        "About This Book" in html_text
        and "License, Attribution, and Reuse" in html_text,
        "standalone HTML contains publication front and back matter",
    )
    report.require(
        html_text.count('<nav id="TOC"') == 1
        and html_text.count('<main id="main-content" tabindex="-1">') == 1
        and html_text.count("</main>") == 1
        and '<a class="skip-link" href="#main-content">Skip to main content</a>'
        in html_text
        and html_text.index('<nav id="TOC"')
        < html_text.index('<main id="main-content" tabindex="-1">'),
        "standalone HTML contains semantic navigation and main content",
    )
    report.require(
        '<link rel="stylesheet"' not in html_text
        and ".skip-link" in html_text
        and "--teal-dark:" in html_text,
        "standalone HTML embeds the authored stylesheet",
    )
    report.require(
        bool(re.search(r'<html\b[^>]*\blang="en-US"', html_text))
        and "<title>Operating Cloud Databases</title>" in html_text,
        "standalone HTML identifies its language and title",
    )
    html_ids = re.findall(r'\sid="([^"]+)"', html_text)
    fragment_targets = re.findall(r'href="#([^"]+)"', html_text)
    report.require(
        len(html_ids) == len(set(html_ids)),
        "standalone HTML identifiers are unique",
    )
    report.require(
        not (set(fragment_targets) - set(html_ids)),
        "standalone HTML fragment links resolve to local targets",
    )

    for path, label in [(epub, "EPUB"), (docx, "Word import")]:
        try:
            with zipfile.ZipFile(path) as archive:
                bad_member = archive.testzip()
            report.require(bad_member is None, f"{label} archive passes integrity check")
        except zipfile.BadZipFile as exc:
            report.fail(f"invalid {label} archive: {exc}")

    try:
        with zipfile.ZipFile(epub) as archive:
            first_member = archive.infolist()[0]
            report.require(
                first_member.filename == "mimetype"
                and first_member.compress_type == zipfile.ZIP_STORED
                and archive.read("mimetype") == b"application/epub+zip",
                "EPUB starts with the required uncompressed mimetype entry",
            )
            epub_xml_names = [
                name
                for name in archive.namelist()
                if Path(name).suffix.lower() in {".xml", ".xhtml", ".opf", ".ncx"}
            ]
            epub_xml_valid = True
            for name in epub_xml_names:
                try:
                    ET.fromstring(archive.read(name))
                except ET.ParseError:
                    epub_xml_valid = False
                    break
            report.require(epub_xml_valid, "all EPUB XML and XHTML files are well formed")

            package = ET.fromstring(archive.read("EPUB/content.opf"))
            title = package.findtext(".//dc:title", namespaces=EPUB_NS)
            language = package.findtext(".//dc:language", namespaces=EPUB_NS)
            published = package.findtext(".//dc:date", namespaces=EPUB_NS)
            report.require(
                title == "Operating Cloud Databases"
                and language == "en-US"
                and published == "2026-08-09",
                "EPUB metadata identifies the candidate title, language, and date",
            )
            chapter_ids = {
                item.attrib.get("id")
                for item in package.findall(".//opf:manifest/opf:item", EPUB_NS)
                if re.fullmatch(r"text/ch\d{3}\.xhtml", item.attrib.get("href", ""))
            }
            spine_ids = {
                item.attrib.get("idref")
                for item in package.findall(".//opf:spine/opf:itemref", EPUB_NS)
            }
            report.require(
                len(chapter_ids) == 17 and chapter_ids <= spine_ids,
                "EPUB manifest and reading order contain all 17 book sections",
            )
    except (KeyError, zipfile.BadZipFile, ET.ParseError) as exc:
        report.fail(f"EPUB structure could not be inspected: {exc}")

    try:
        with zipfile.ZipFile(docx) as archive:
            word_xml_names = [
                name
                for name in archive.namelist()
                if Path(name).suffix.lower() in {".xml", ".rels"}
            ]
            word_xml_valid = True
            for name in word_xml_names:
                try:
                    ET.fromstring(archive.read(name))
                except ET.ParseError:
                    word_xml_valid = False
                    break
            report.require(
                word_xml_valid,
                "all Word import XML and relationship files are well formed",
            )
            document = ET.fromstring(archive.read("word/document.xml"))
            heading_ones = document.findall(
                ".//w:pStyle[@w:val='Heading1']", WORD_NS
            )
            report.require(
                len(heading_ones) == 17,
                "Word import contains one Heading 1 for each of 17 book sections",
            )
    except (KeyError, zipfile.BadZipFile, ET.ParseError) as exc:
        report.fail(f"Word import structure could not be inspected: {exc}")

    with cover.open("rb") as image:
        header = image.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        report.fail("publication cover is not a PNG")
    else:
        width, height = struct.unpack(">II", header[16:24])
        report.require(
            (width, height) == (1600, 2560),
            "publication cover has the expected 1600 x 2560 dimensions",
        )

    expected_hashes: dict[str, str] = {}
    for line in read_text(manifest).splitlines():
        if not line.strip():
            continue
        checksum, filename = line.split(maxsplit=1)
        expected_hashes[filename.strip()] = checksum
    for path in [html, epub, docx]:
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        report.require(
            expected_hashes.get(path.name) == actual,
            f"checksum matches publication artifact: {path.name}",
        )

    report.require(
        "version: \"1.0.0-rc.1\"" in read_text(publication / "book_metadata.yaml")
        and "Version 1.0.0-rc.1" in read_text(publication / "cover.svg"),
        "publication metadata and cover identify the candidate version",
    )

    metadata_text = read_text(publication / "book_metadata.yaml")
    catalog_text = read_text(ROOT / "OER_CATALOG.md")
    metadata_date_match = re.search(
        r'^date:\s*"(\d{4}-\d{2}-\d{2})"', metadata_text, re.MULTILINE
    )
    catalog_date_match = re.search(
        r"^- \*\*Inventory date:\*\* ([A-Za-z]+ \d{1,2}, \d{4})$",
        catalog_text,
        re.MULTILINE,
    )
    dates_match = False
    if metadata_date_match and catalog_date_match:
        try:
            catalog_date = datetime.strptime(
                catalog_date_match.group(1), "%B %d, %Y"
            ).date().isoformat()
            dates_match = metadata_date_match.group(1) == catalog_date
        except ValueError:
            dates_match = False
    report.require(
        dates_match,
        "publication date matches the authoritative OER inventory date",
    )


def extract_note_text(xml_bytes: bytes) -> str:
    root = ET.fromstring(xml_bytes)
    for shape in root.findall(".//p:sp", NS):
        if shape.find(".//p:ph[@type='body']", NS) is None:
            continue
        paragraphs: list[str] = []
        for paragraph in shape.findall(".//a:p", NS):
            value = "".join(
                node.text or "" for node in paragraph.findall(".//a:t", NS)
            ).strip()
            if value:
                paragraphs.append(value)
        return "\n\n".join(paragraphs)
    return ""


def transcript_sections(text: str) -> dict[int, str]:
    matches = list(SLIDE_SECTION_RE.finditer(text))
    sections: dict[int, str] = {}
    license_position = text.find("\n## License")
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        if license_position != -1 and license_position < end:
            end = license_position
        sections[int(match.group(1))] = text[match.end() : end].strip()
    return sections


def pdf_page_count(path: Path) -> int | None:
    executable = shutil.which("pdfinfo")
    if not executable:
        return None
    result = subprocess.run(
        [executable, str(path)], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        return -1
    match = re.search(r"^Pages:\s+(\d+)", result.stdout, re.MULTILINE)
    return int(match.group(1)) if match else -1


def pdf_text(path: Path) -> str | None:
    executable = shutil.which("pdftotext")
    if not executable:
        return None
    result = subprocess.run(
        [executable, "-layout", str(path), "-"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else ""


def pdf_metadata(path: Path) -> dict[str, str] | None:
    executable = shutil.which("pdfinfo")
    if not executable:
        return None
    result = subprocess.run(
        [executable, str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return {}
    metadata: dict[str, str] = {}
    for line in result.stdout.splitlines():
        key, separator, value = line.partition(":")
        if separator:
            metadata[key.strip()] = value.strip()
    return metadata


def pdf_catalog(path: Path) -> str | None:
    executable = shutil.which("mutool")
    if not executable:
        return None
    result = subprocess.run(
        [executable, "show", "-g", str(path), "trailer/Root"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else ""


def expected_deck_title(transcript: Path) -> str:
    first_line = read_text(transcript).splitlines()[0]
    match = re.fullmatch(r"# (Week \d+: .+) - Spoken Transcript", first_line)
    return match.group(1) if match else ""


def check_decks(report: Report) -> None:
    forbidden_directions = re.compile(
        r"\b(?:use this slide|use this as (?:a|the) transition|tell students|"
        r"ask students|teaching note|speaker note|remind students|"
        r"pause here|focus (?:your|the) (?:attention|discussion))\b",
        re.IGNORECASE,
    )
    decks = sorted(ROOT.glob("week_*/*.pptx"))
    report.require(len(decks) == 15, "15 student PowerPoint decks are present")
    total_slides = 0

    for deck in decks:
        week_match = WEEK_RE.match(deck.parent.name)
        if not week_match:
            report.fail(f"deck is outside a numbered week: {relative(deck)}")
            continue
        week = int(week_match.group(1))
        transcript = deck.with_name(f"{deck.stem}_transcript.md")
        pdf = deck.with_suffix(".pdf")
        report.require(transcript.exists(), f"matching transcript exists: {transcript.name}")
        report.require(pdf.exists(), f"matching PDF exists: {pdf.name}")
        if not transcript.exists():
            continue
        expected_title = expected_deck_title(transcript)
        report.require(
            bool(expected_title),
            f"Week {week} transcript supplies the canonical presentation title",
        )

        with zipfile.ZipFile(deck) as archive:
            names = archive.namelist()
            slide_numbers = sorted(
                int(match.group(1))
                for name in names
                if (match := re.fullmatch(r"ppt/slides/slide(\d+)\.xml", name))
            )
            note_numbers = sorted(
                int(match.group(1))
                for name in names
                if (
                    match := re.fullmatch(
                        r"ppt/notesSlides/notesSlide(\d+)\.xml", name
                    )
                )
            )
            total_slides += len(slide_numbers)
            report.require(
                slide_numbers == note_numbers,
                f"Week {week} has one speaker-note script per slide",
            )
            note_scripts = {
                number: extract_note_text(
                    archive.read(f"ppt/notesSlides/notesSlide{number}.xml")
                )
                for number in note_numbers
            }
            try:
                core = ET.fromstring(archive.read("docProps/core.xml"))
            except (KeyError, ET.ParseError):
                core = None

        report.require(core is not None, f"Week {week} deck has valid core metadata")
        if core is not None:
            report.require(
                core.findtext("dc:title", default="", namespaces=CORE_NS)
                == expected_title
                and core.findtext("dc:creator", default="", namespaces=CORE_NS)
                == "Atilio Barreda"
                and core.findtext("dc:language", default="", namespaces=CORE_NS)
                == "en-US"
                and core.findtext("cp:contentStatus", default="", namespaces=CORE_NS)
                == "Release Candidate",
                f"Week {week} deck metadata identifies its title, author, language, and status",
            )

        sections = transcript_sections(read_text(transcript))
        report.require(
            sorted(sections) == slide_numbers,
            f"Week {week} transcript has one section per slide",
        )
        for number in slide_numbers:
            note = note_scripts.get(number, "")
            transcript_text = sections.get(number, "")
            if normalize_prose(note) != normalize_prose(transcript_text):
                report.fail(
                    f"Week {week} slide {number} notes do not match the transcript"
                )
            word_count = len(re.findall(r"\b[\w'-]+\b", note))
            if word_count < 45:
                report.fail(
                    f"Week {week} slide {number} notes are too short for a complete script "
                    f"({word_count} words)"
                )
            if forbidden_directions.search(note):
                report.fail(
                    f"Week {week} slide {number} notes contain teaching directions rather "
                    "than spoken prose"
                )

        if pdf.exists():
            report.require(pdf.stat().st_size > 20_000, f"PDF is nontrivial: {pdf.name}")
            pages = pdf_page_count(pdf)
            if pages is None:
                report.warn("pdfinfo is unavailable; PDF page counts were not checked")
            else:
                report.require(
                    pages == len(slide_numbers),
                    f"Week {week} PDF page count matches the deck",
                )
            extracted = pdf_text(pdf)
            if extracted is None:
                report.warn("pdftotext is unavailable; PDF text extraction was not checked")
            else:
                report.require(
                    len(extracted.split()) >= len(slide_numbers) * 20,
                    f"Week {week} PDF contains extractable instructional text",
                )
                if "\ufffd" in extracted:
                    report.fail(f"Week {week} PDF contains replacement glyphs")
            metadata = pdf_metadata(pdf)
            if metadata is None:
                report.warn("pdfinfo is unavailable; PDF tag metadata was not checked")
            else:
                report.require(
                    metadata.get("Tagged", "").lower() == "yes",
                    f"Week {week} PDF reports a tagged structure",
                )
                report.require(
                    metadata.get("Encrypted", "").lower() == "no",
                    f"Week {week} PDF is not encrypted",
                )
                report.require(
                    metadata.get("Title", "") == expected_title
                    and metadata.get("Author", "") == "Atilio Barreda",
                    f"Week {week} PDF metadata identifies its title and author",
                )
            catalog = pdf_catalog(pdf)
            if catalog is None:
                report.warn("mutool is unavailable; PDF catalog structure was not checked")
            else:
                report.require(
                    "/StructTreeRoot" in catalog
                    and "/Marked true" in catalog
                    and "/Lang(en-US)" in catalog
                    and "/DisplayDocTitle true" in catalog,
                    f"Week {week} PDF catalog exposes structure, language, and title display",
                )

    report.require(total_slides == 214, f"validated all {total_slides} authored slides")


def check_labs_and_assignments(report: Report) -> None:
    labs = sorted(ROOT.glob("week_*/lab_*.md"))
    for lab in labs:
        text = read_text(lab)
        report.require(
            bool(re.search(r"\bindividual(?:ly| work| project)\b", text, re.IGNORECASE)),
            f"lab states the individual-work rule: {relative(lab)}",
        )
        report.require(
            bool(re.search(r"^## (?:\d+\. )?Submit One Thing", text, re.MULTILINE)),
            f"lab has one explicit submission section: {relative(lab)}",
        )

    weekly_readmes = sorted(ROOT.glob("week_*/README.md"))
    duplicate_final_headings = re.compile(
        r"^## (?:Required Evidence|Required Deliverables|Submission Package|Final Project Rubric)",
        re.MULTILINE,
    )
    for path in weekly_readmes:
        weekly_text = read_text(path)
        if duplicate_final_headings.search(weekly_text):
            report.fail(f"weekly guide redefines final-project deliverables: {relative(path)}")
        optional_headings = re.findall(
            r"^## Optional Industry Extension:", weekly_text, re.MULTILINE
        )
        report.require(
            len(optional_headings) == 1,
            f"weekly guide has exactly one optional industry extension: {relative(path)}",
        )
        report.require(
            "This activity is optional, ungraded, and does not add a submission."
            in weekly_text,
            f"optional extension does not change required workload: {relative(path)}",
        )

    final_text = read_text(ROOT / "final_project.md")
    report.require(
        "This is an individual project." in final_text,
        "canonical final project is explicitly individual",
    )
    report.require(
        "GitHub is encouraged" in final_text and "not required" in final_text,
        "canonical final does not require a public GitHub repository",
    )
    report.require(
        "read-only instructor access" in final_text,
        "canonical final provides an approved cloud-access verification path",
    )

    week_10 = read_text(ROOT / "week_10/README.md")
    live_slug = "modeling-data-relationships"
    student_slug = "relational-to-document-model"
    report.require(
        live_slug in week_10 and student_slug in week_10,
        "Week 10 links distinct instructor-live and individual MongoDB activities",
    )
    report.require(
        "intentionally different" in week_10,
        "Week 10 explicitly explains why the two MongoDB activities differ",
    )

    response = read_text(ROOT / "week_11/lab_02_sort_and_case_response.md")
    report.require(
        "1XeG3VDtdsA" in response
        and "200-300 words" in response
        and "Brightspace" in response
        and "Do not create or upload a Markdown file" in response,
        "Week 11 case response is one short Brightspace text assignment",
    )


def check_oer_boundary(report: Report) -> None:
    catalog = normalize_prose(read_text(ROOT / "OER_CATALOG.md"))
    external = read_text(ROOT / "FREE_EXTERNAL_RESOURCES.md")
    fellowship = read_text(ROOT / "fellowship/README.md")
    readme = read_text(ROOT / "README.md")
    citation = read_text(ROOT / "CITATION.cff")

    report.require(
        "authoritative inventory of course OER" in catalog
        and "not itself the course content" in catalog,
        "OER catalog identifies itself as the authoritative created-artifact inventory",
    )
    report.require(
        "free access is not the same as an open license" in external.lower()
        and "not counted" in external.lower(),
        "free external resources are not claimed as created OER",
    )
    report.require(
        "deliberately separate" in fellowship
        and "Catalog of created OER" in fellowship,
        "fellowship planning is explicitly separate from created OER evidence",
    )
    report.require(
        not (ROOT / "fellowship/OER_CATALOG.md").exists(),
        "the authoritative OER catalog is not duplicated inside the fellowship plan",
    )
    report.require(
        "PDF handout" in readme
        and "Every PDF reports tagged structure" in readme
        and "tag-tree inspection found insufficient semantics" in readme
        and "convenience handouts" in readme,
        "the package describes PDFs accurately and identifies the transcript alternative",
    )
    report.require(
        "version: 1.0.0-rc.1" in citation
        and "https://github.com/lolusername/CST4714_DB_admin" in citation,
        "citation metadata identifies the actual repository and candidate version",
    )


def check_secrets(report: Report) -> None:
    token_patterns = {
        "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
        "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "JWT-like secret": re.compile(r"\beyJ[A-Za-z0-9_-]{60,}\.[A-Za-z0-9_-]{20,}"),
    }
    credential_uri = re.compile(
        r"(?:mongodb(?:\+srv)?|postgres(?:ql)?)://"
        r"([^:\s/@<>]+):([^@\s/<>]+)@",
        re.IGNORECASE,
    )
    placeholder_terms = {
        "user",
        "username",
        "password",
        "example",
        "placeholder",
        "redacted",
        "your_user",
        "your_password",
    }
    extensions = {
        ".md",
        ".py",
        ".sql",
        ".ipynb",
        ".json",
        ".csv",
        ".yml",
        ".yaml",
        ".cff",
        ".html",
        ".css",
        ".svg",
    }
    for path in sorted(file for file in ROOT.rglob("*") if file.suffix in extensions):
        if path.resolve() == Path(__file__).resolve():
            continue
        text = read_text(path)
        for label, pattern in token_patterns.items():
            if pattern.search(text):
                report.fail(f"possible {label} in {relative(path)}")
        for match in credential_uri.finditer(text):
            user = match.group(1).lower()
            password = match.group(2).lower()
            combined = f"{user} {password}"
            if not any(term in combined for term in placeholder_terms) and "${" not in match.group(0):
                report.fail(f"possible credential-bearing URI in {relative(path)}")
    report.require(
        not any("possible " in error for error in report.errors),
        "no credential or token pattern was detected",
    )


def collect_urls() -> list[str]:
    urls: set[str] = set()
    extensions = {".md", ".ipynb", ".py", ".json", ".yml", ".yaml", ".cff"}
    for path in (file for file in ROOT.rglob("*") if file.suffix in extensions):
        if path.resolve() == Path(__file__).resolve():
            continue
        for value in URL_RE.findall(read_text(path)):
            cleaned = value.rstrip("\\\"').,;]}")
            if cleaned and not cleaned.startswith(NON_LINK_URI_PREFIXES):
                urls.add(cleaned)
    return sorted(urls)


def fetch_url(url: str) -> tuple[str, int | None, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "CST4714-OER-link-check/1.0",
            "Range": "bytes=0-1024",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            response.read(1)
            return url, response.status, ""
    except urllib.error.HTTPError as exc:
        return url, exc.code, str(exc.reason)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return url, None, str(exc)


def check_external_urls(report: Report) -> None:
    urls = collect_urls()
    report.require(bool(urls), f"collected {len(urls)} unique external URLs")
    definite_failures: list[str] = []
    access_warnings: list[str] = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(fetch_url, url) for url in urls]
        for future in as_completed(futures):
            url, status, detail = future.result()
            if status in {404, 410}:
                definite_failures.append(f"{status} {url}")
            elif status is None or status >= 400:
                access_warnings.append(f"{status or 'network'} {url} ({detail})")
    for item in sorted(definite_failures):
        report.fail(f"external URL failed: {item}")
    for item in sorted(access_warnings):
        report.warn(f"external URL requires manual review: {item}")
    report.require(
        not definite_failures,
        f"checked {len(urls)} external URLs with no definite 404/410 response",
    )


def print_report(report: Report) -> int:
    print(f"CST4714 OER validation: {len(report.passes)} checks passed")
    if report.warnings:
        print(f"\nWarnings ({len(report.warnings)}):")
        for warning in sorted(set(report.warnings)):
            print(f"- {warning}")
    if report.errors:
        print(f"\nErrors ({len(report.errors)}):")
        for error in sorted(set(report.errors)):
            print(f"- {error}")
        return 1
    print("\nResult: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-urls",
        action="store_true",
        help="also make live requests to every external URL",
    )
    args = parser.parse_args()

    report = Report()
    check_structure(report)
    check_markdown_links(report)
    check_json_csv_and_notebooks(report)
    check_publication(report)
    check_decks(report)
    check_labs_and_assignments(report)
    check_oer_boundary(report)
    check_secrets(report)
    if args.check_urls:
        check_external_urls(report)
    return print_report(report)


if __name__ == "__main__":
    sys.exit(main())
