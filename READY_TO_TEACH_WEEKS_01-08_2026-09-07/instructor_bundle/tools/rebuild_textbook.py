# /// script
# requires-python = ">=3.11"
# dependencies = ["python-docx==1.2.0"]
# ///
"""Rebuild only the eight-chapter classroom volume beside this tools folder."""
import hashlib
import json
import re
import textbook_engine as book


def sources():
    modules = [next(book.TEXTBOOK.glob(f'module_{n:02}_*.md')) for n in range(1, 9)]
    return [book.PUBLICATION / 'front_matter.md', book.PUBLICATION / 'parts/part_1.md',
            *modules[:3], book.PUBLICATION / 'parts/part_2.md', *modules[3:],
            book.PUBLICATION / 'back_matter.md']


def manifest():
    records = [{'path': str(p.relative_to(book.ROOT)),
                'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
               for p in sources()]
    outputs = [book.DOCX_PATH, book.PDF_PATH, book.HTML_PATH, book.EPUB_PATH]
    (book.EXPORTS / 'SOURCE_MANIFEST.json').write_text(json.dumps({
        'title': 'Operating Cloud Databases: Chapters 1-8',
        'status': 'unpublished classroom handoff', 'sources': records,
        'outputs': [{'path': p.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                    for p in outputs]}, indent=2) + '\n')


def check():
    text = book.HTML_PATH.read_text()
    chapters = re.findall(r'<h1[^>]*data-number="([0-9]+)"', text)
    assert chapters == [str(n) for n in range(1, 9)], chapters
    assert 'id="companion-materials"' in text
    assert '<math' in text and 'Listing 1.' in text
    assert all(p.stat().st_size > 10000 for p in
               [book.DOCX_PATH, book.PDF_PATH, book.HTML_PATH, book.EPUB_PATH])
    print('Eight-chapter Word, PDF, HTML, and EPUB volume built.')


book.source_order = sources
book.write_manifests = manifest
book.structural_checks = check
book.main()
