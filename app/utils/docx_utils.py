import re
from typing import List, Tuple

from docx import Document


def extract_headings(doc: Document) -> List[Tuple[int, str]]:
    headings = []
    pattern = re.compile(r"^(\d+(?:\.\d+)*)(\s+.+)")

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        match = pattern.match(text)
        if match:
            level_str = match.group(1)
            level = level_str.count(".") + 1 if "." in level_str else 1
            headings.append((level, text))

    return headings


def append_document_content(target_doc: Document, source_doc: Document):
    for element in source_doc.element.body:
        target_doc.element.body.append(element)
