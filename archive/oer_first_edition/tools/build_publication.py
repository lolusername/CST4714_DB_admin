#!/usr/bin/env python3
"""Build portable publication formats from the canonical Markdown modules."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLICATION = ROOT / "publication"
EXPORTS = PUBLICATION / "exports"
VERSION = "1.0.0-rc.1"
STEM = f"operating_cloud_databases_v{VERSION}"


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_html_landmarks(path: Path) -> None:
    """Add explicit landmarks that Pandoc's default HTML template omits."""
    text = path.read_text(encoding="utf-8")
    main_marker = '<main id="main-content" tabindex="-1">'
    if main_marker not in text:
        body_marker = "<body>"
        nav_marker = "</nav>"
        body_end_marker = "</body>"
        if not all(
            marker in text for marker in (body_marker, nav_marker, body_end_marker)
        ):
            raise RuntimeError("Pandoc HTML is missing the expected body or TOC markers")

        text = text.replace(
            body_marker,
            body_marker
            + '\n<a class="skip-link" href="#main-content">Skip to main content</a>',
            1,
        )
        nav_end = text.index(nav_marker) + len(nav_marker)
        text = text[:nav_end] + f"\n{main_marker}" + text[nav_end:]
        text = text.replace(body_end_marker, "</main>\n" + body_end_marker, 1)

    # Pandoc's embedded highlighting CSS contains trailing spaces by default.
    text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    if shutil.which("pandoc") is None:
        raise SystemExit("pandoc is required to build publication formats")

    EXPORTS.mkdir(parents=True, exist_ok=True)
    modules = sorted((ROOT / "textbook").glob("module_*.md"))
    sources = [PUBLICATION / "front_matter.md", *modules, PUBLICATION / "back_matter.md"]
    source_args = [str(path.relative_to(ROOT)) for path in sources]
    metadata = str((PUBLICATION / "book_metadata.yaml").relative_to(ROOT))
    css = str((PUBLICATION / "operating_cloud_databases.css").relative_to(ROOT))
    cover = str((PUBLICATION / "cover.png").relative_to(ROOT))

    if shutil.which("magick") is not None:
        run(
            [
                "magick",
                str((PUBLICATION / "cover.svg").relative_to(ROOT)),
                "-alpha",
                "off",
                "-depth",
                "8",
                "-strip",
                "-define",
                "png:exclude-chunk=date,time",
                cover,
            ]
        )
    elif not (PUBLICATION / "cover.png").exists():
        raise SystemExit("ImageMagick is required to render publication/cover.png")

    common = [
        "pandoc",
        *source_args,
        "--from=gfm",
        f"--metadata-file={metadata}",
        "--toc",
        "--toc-depth=2",
        "--number-sections",
    ]

    html = EXPORTS / f"{STEM}.html"
    run(
        [
            *common,
            "--standalone",
            "--embed-resources",
            "--section-divs",
            f"--css={css}",
            f"--output={html.relative_to(ROOT)}",
        ]
    )
    add_html_landmarks(html)

    epub = EXPORTS / f"{STEM}.epub"
    run(
        [
            *common,
            f"--css={css}",
            f"--epub-cover-image={cover}",
            f"--output={epub.relative_to(ROOT)}",
        ]
    )

    docx = EXPORTS / f"{STEM}.docx"
    run([*common, f"--output={docx.relative_to(ROOT)}"])

    manifest = EXPORTS / "SHA256SUMS.txt"
    artifacts = [html, epub, docx]
    manifest.write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in artifacts),
        encoding="utf-8",
    )

    for path in [*artifacts, manifest]:
        print(f"built {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
