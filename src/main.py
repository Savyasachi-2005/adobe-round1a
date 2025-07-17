import os
import json
from extractor import get_outline

INPUT_DIR  = os.getenv("INPUT_DIR",  "INPUT")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

def process_all() -> None:
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("No PDF files found in", INPUT_DIR)
        return

    for pdf_name in pdf_files:
        in_path  = os.path.join(INPUT_DIR, pdf_name)
        out_path = os.path.join(OUTPUT_DIR, pdf_name.replace(".pdf", ".json"))
        print(f"Processing {pdf_name} ...")
        data = get_outline(in_path)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved {out_path}")

if __name__ == "__main__":
    process_all()