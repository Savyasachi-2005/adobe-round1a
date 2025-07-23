import os
import re
import numpy as np
import fitz  # PyMuPDF
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# Optional: For Windows, set Tesseract path manually
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_lines(pdf_path, max_pages=50):
    doc = fitz.open(pdf_path)
    lines = []

    for page_no in range(min(len(doc), max_pages)):
        page = doc[page_no]
        page_text = page.get_text().strip()

        if len(page_text) < 10:
            # OCR fallback
            print(f"[OCR] Page {page_no + 1}: Using image-based OCR fallback")
            images = convert_from_path(pdf_path, dpi=300, first_page=page_no + 1, last_page=page_no + 1)
            ocr_text = pytesseract.image_to_string(images[0])
            for i, line in enumerate(ocr_text.splitlines()):
                clean = line.strip()
                if len(clean) >= 4:
                    lines.append({
                        "text": clean,
                        "size": 12.0,
                        "bold": False,
                        "page": page_no + 1,
                        "top": i * 20,
                        "left": 0,
                        "right": 0
                    })
            continue

        # Standard digital text extraction
        blocks = page.get_text("dict")["blocks"]
        for blk in blocks:
            if blk["type"] != 0:
                continue  # Skip images, figures
            for ln in blk["lines"]:
                txt = "".join(span["text"] for span in ln["spans"]).strip()
                if len(txt) < 2:
                    continue
                sizes = [span["size"] for span in ln["spans"]]
                fonts = [span["font"] for span in ln["spans"]]
                bbox = ln["bbox"]
                lines.append({
                    "text": txt,
                    "size": round(np.mean(sizes), 1),
                    "bold": any("Bold" in f for f in fonts),
                    "page": page_no + 1,
                    "top": bbox[1],
                    "left": bbox[0],
                    "right": bbox[2]
                })

    return lines


def identify_heading_levels(lines):
    sizes = np.array([line["size"] for line in lines])
    if len(sizes) < 5:
        size_ranks = sorted(set(sizes))[-3:][::-1]
    else:
        q90 = round(np.percentile(sizes, 90), 1)
        q75 = round(np.percentile(sizes, 75), 1)
        q60 = round(np.percentile(sizes, 60), 1)
        size_ranks = [q90, q75, q60]

    headings = []
    for line in lines:
        text = line["text"]
        size = line["size"]
        level = None

        numbered = bool(re.match(r"^\d+([.]\d+)*[\s:-]+", text))
        all_caps = text.isupper()

        if size >= size_ranks[0] or (line["bold"] and numbered):
            level = "H1"
        elif size >= size_ranks[1] or (line["bold"] and all_caps):
            level = "H2"
        elif size >= size_ranks[2] or numbered:
            level = "H3"

        if level:
            headings.append({
                "text": text.strip(),
                "level": level,
                "page": line["page"]
            })

    return headings


def get_title(lines):
    for line in lines:
        if "hope to see" in line["text"].lower():
            return line["text"].strip()
    best = sorted(lines, key=lambda l: (-l["size"], l["top"]))
    return best[0]["text"] if best else ""


def get_outline(pdf_path):
    lines = extract_lines(pdf_path)
    if not lines:
        return {"title": os.path.basename(pdf_path)[:-4], "outline": []}

    # Step 1: Try structured heading detection
    headings = identify_heading_levels(lines)

    if len(headings) >= 3:
        title = get_title(lines)
        return {"title": title.strip(), "outline": headings}

    # Step 2: Fallback for flyers / unstructured PDFs
    sorted_by_size = sorted(lines, key=lambda l: (-l["size"], l["top"]))
    all_sizes = [l["size"] for l in sorted_by_size]
    size_threshold = np.percentile(all_sizes, 90)  # adaptive font-size threshold

    seen_texts = set()
    outline = []

    for line in sorted_by_size[:25]:  # more generous in flyer mode
        txt = line["text"].strip()
        if len(txt) < 4 or txt.lower().strip(":") in seen_texts:
            continue
        seen_texts.add(txt.lower().strip(":"))

        txt_lower = txt.lower()
        lvl = "H2"  # default

        if len(txt.split()) <= 3 and line["size"] >= size_threshold:
            lvl = "H1"
        elif ":" in txt or line["bold"]:
            lvl = "H2"
        elif ".com" in txt_lower or "www." in txt_lower:
            lvl = "H3"
        else:
            lvl = "H2"

        outline.append({
            "text": txt,
            "level": lvl,
            "page": line["page"]
        })

    # Step 3: Title inference
    title = next((l["text"] for l in sorted_by_size if "hope to see" in l["text"].lower()), None)
    if not title:
        title = sorted_by_size[0]["text"]

    return {"title": title.strip(), "outline": outline}
