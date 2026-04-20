#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract "作业1" Python code from a Word document or a zip of Word documents.

Supported inputs:
- .docx (OOXML): parses word/document.xml
- .doc (Word 2003 XML / WordML): parses as XML text if possible
- .zip: walks contained files and extracts from each .docx/.doc

Heuristics:
- Prefer code that contains `def calcArea` (assignment requirement)
- Otherwise, return the longest code-like block (lines containing common python tokens)

Output:
- JSON to stdout with per-file extracted code and a suggested filename.

This script is meant to be used by grade_rectangles.py.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import zipfile
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET


PY_HINT_RE = re.compile(
    r"\b(def|import|from|return|for|while|if|elif|else|with|open\(|csv\.|reader\(|append\()\b"
)


def _xml_text_with_breaks(root: ET.Element) -> str:
    """Collect visible text from OOXML/WordML XML, keeping rough line breaks.

    Important: In Word 2003 XML/WordML, it's common to see <w:t>text<w:br/>more</w:t>.
    In such cases, the "more" part becomes the .tail of the <w:br/> node.
    We must collect both .text and .tail.
    """
    out: List[str] = []

    for el in root.iter():
        tag = el.tag

        if tag.endswith("}t") and el.text:
            out.append(el.text)

        if tag.endswith("}tab"):
            out.append("\t")
            if el.tail:
                out.append(el.tail)

        if tag.endswith("}br") or tag.endswith("}cr"):
            out.append("\n")
            if el.tail:
                out.append(el.tail)

        if tag.endswith("}p"):
            out.append("\n")
            if el.tail:
                out.append(el.tail)

    text = "".join(out)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def extract_text_from_docx_bytes(data: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    return _xml_text_with_breaks(root)


def extract_text_from_wordml_bytes(data: bytes) -> str:
    # Word 2003 XML (.doc saved as WordML) is plain XML
    root = ET.fromstring(data)
    return _xml_text_with_breaks(root)


def split_code_blocks(text: str) -> List[str]:
    lines = [ln.rstrip() for ln in text.split("\n")]

    blocks: List[List[str]] = []
    cur: List[str] = []

    def flush():
        nonlocal cur
        if cur:
            blocks.append(cur)
            cur = []

    STOP_PREFIXES = ("正确答案", "教师批语", "题目得分", "作业批语")

    for ln in lines:
        raw = ln.rstrip("\n")
        stripped = raw.strip()

        # Stop markers (even if the line is indented in the original document)
        if stripped.startswith(STOP_PREFIXES):
            flush()
            continue

        # Remove common Word prompt prefixes like "学生答案：" / "答案：" while preserving indentation.
        ln2 = re.sub(r"^(\s*)(学生答案|答案|作业答案)\s*：\s*", r"\1", raw)
        stripped2 = ln2.strip()

        is_code_like = bool(PY_HINT_RE.search(stripped2))
        is_blank = (stripped2 == "")
        is_continuation = (cur and (raw.startswith(" ") or raw.startswith("\t")) and (is_code_like or is_blank))

        if is_code_like or is_continuation:
            cur.append(ln2)
        else:
            if cur and is_blank:
                cur.append("")
            else:
                flush()
    flush()

    return ["\n".join(b).strip("\n") for b in blocks if "\n".join(b).strip()]


def pick_best_code(text: str) -> Tuple[Optional[str], Dict[str, int]]:
    # First try a direct substring window for the specific assignment function.
    m = re.search(r"\bimport\s+csv\b", text)
    m2 = re.search(r"\bdef\s+calcArea\s*\(", text)
    if m2:
        start = m.start() if m and m.start() < m2.start() else max(0, m2.start() - 200)
        # stop at common markers or end
        stops = ["正确答案", "教师批语", "题目得分", "作业批语"]
        end = len(text)
        for s in stops:
            idx = text.find(s, m2.start())
            if idx != -1:
                end = min(end, idx)
        snippet = text[start:end].strip()
        # Ensure the snippet actually contains code.
        if "def calcArea" in snippet:
            return snippet, {"blocks": 0, "picked": 0, "method": 1}

    blocks = split_code_blocks(text)
    meta = {"blocks": len(blocks)}
    if not blocks:
        return None, meta

    for b in sorted(blocks, key=len, reverse=True):
        if "def calcArea" in b:
            meta["picked"] = 1
            return b, meta

    meta["picked"] = 2
    return max(blocks, key=len), meta


@dataclass
class Extracted:
    source_name: str
    code: Optional[str]
    meta: Dict[str, int]


def extract_from_file(path: str) -> Extracted:
    name = os.path.basename(path)
    with open(path, "rb") as f:
        data = f.read()

    text: str
    if name.lower().endswith(".docx"):
        text = extract_text_from_docx_bytes(data)
    elif name.lower().endswith(".doc"):
        # best-effort: treat as WordML XML
        text = extract_text_from_wordml_bytes(data)
    else:
        raise ValueError(f"Unsupported file: {name}")

    code, meta = pick_best_code(text)
    return Extracted(source_name=name, code=code, meta=meta)


def extract_from_zip(path: str) -> List[Extracted]:
    extracted: List[Extracted] = []
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            lower = info.filename.lower()
            if not (lower.endswith(".docx") or lower.endswith(".doc")):
                continue
            data = z.read(info.filename)
            try:
                if lower.endswith(".docx"):
                    text = extract_text_from_docx_bytes(data)
                else:
                    text = extract_text_from_wordml_bytes(data)
                code, meta = pick_best_code(text)
                extracted.append(Extracted(source_name=info.filename, code=code, meta=meta))
            except Exception:
                extracted.append(Extracted(source_name=info.filename, code=None, meta={"error": 1}))
    return extracted


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help=".docx/.doc/.zip")
    args = ap.parse_args()

    p = args.input
    if p.lower().endswith(".zip"):
        items = extract_from_zip(p)
    else:
        items = [extract_from_file(p)]

    out = []
    for it in items:
        out.append({"source": it.source_name, "code": it.code, "meta": it.meta})

    print(json.dumps({"items": out}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
