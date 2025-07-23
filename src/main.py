import os
import json
from extractor import get_outline

INPUT_DIR = os.getenv("INPUT_DIR", "INPUT")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

def process_all() -> None:
    # Use list comprehension with os.scandir for faster file discovery
    try:
        pdf_files = [f.name for f in os.scandir(INPUT_DIR) if f.name.lower().endswith(".pdf")]
    except FileNotFoundError:
        print("No PDF files found in", INPUT_DIR)
        return

    if not pdf_files:
        print("No PDF files found in", INPUT_DIR)
        return

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for pdf_name in pdf_files:
        in_path = os.path.join(INPUT_DIR, pdf_name)
        out_path = os.path.join(OUTPUT_DIR, pdf_name[:-4] + ".json")  # Faster string slice
        print(f"Processing {pdf_name} ...")
        
        data = get_outline(in_path)
        
        # Optimized JSON writing
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, separators=(',', ':'))
        
        print(f"Saved {out_path}")

if __name__ == "__main__":
    process_all()