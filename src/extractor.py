import os
import re
import pdfplumber

def get_outline(pdf_path: str):
    outline = []
    with pdfplumber.open(pdf_path) as doc:
        # Collect every char with font info
        chars = []
        for p_num, page in enumerate(doc.pages, 1):
            for ch in page.chars:
                chars.append(
                    dict(
                        text=ch.get("text", ""),
                        font=ch.get("fontname", ""),
                        size=float(ch.get("size", 12)),
                        top=float(ch.get("top", 0)),
                        page=p_num,
                    )
                )

        if not chars:
            return {"title": os.path.basename(pdf_path).split(".")[0], "outline": []}

        # Build lines (group by y-coordinate)
        lines = {}
        for ch in chars:
            y = int(ch["top"])
            lines.setdefault(y, []).append(ch)
        line_list = []
        for y in sorted(lines):
            txt = "".join(c["text"] for c in lines[y]).strip()
            if not txt:
                continue
            sizes = [c["size"] for c in lines[y]]
            fonts = [c["font"] for c in lines[y]]
            avg_size = sum(sizes) / len(sizes)
            bold = any("Bold" in f for f in fonts)
            line_list.append(
                {
                    "text": txt,
                    "size": avg_size,
                    "bold": bold,
                    "page": lines[y][0]["page"],
                }
            )

        # Global average (ignore extreme outliers)
        all_sizes = [l["size"] for l in line_list]
        global_avg = sum(all_sizes) / len(all_sizes)

        # Determine level
        def level(l):
            sz = l["size"]
            txt = l["text"]
            if sz > global_avg + 4 or l["bold"]:
                if re.match(r"^\d+\s+[A-Z]", txt) or txt.isupper():
                    return "H1"
                return "H2"
            if sz > global_avg + 1 or re.match(r"^\d+\.\d+", txt):
                return "H3"
            return None

        # Keep headings, ordered top-to-bottom
        headings = [l for l in line_list if level(l)]
        for h in headings:
            outline.append(
                {"level": level(h), "text": h["text"], "page": h["page"]}
            )

    # Title = first H1 or fallback
    h1s = [o["text"] for o in outline if o["level"] == "H1"]
    title = h1s[0] if h1s else os.path.basename(pdf_path).split(".")[0]

    return {"title": title, "outline": outline}