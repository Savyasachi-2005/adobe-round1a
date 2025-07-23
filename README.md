# 📝 PDF Outline Extractor

> **Adobe Hackathon 2025 – Round 1A**  
> *"Connecting the Dots"*

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20AMD64-red.svg)](https://www.linux.org/)

## 🎯 Overview

A **lightweight, CPU-only PDF outline extractor** built for the **Adobe India Hackathon (Round 1A)**. This universal solution processes a wide range of documents — including structured reports, academic papers, flyers, and scanned PDFs — and outputs clean, structured summaries with titles, headings, and page numbers.

### ✨ Key Features

- 🚀 **Fast Processing** - Processes 50-page PDFs in under 10 seconds
- 💾 **Lightweight** - Docker image optimized for size
- 🔒 **Offline First** - No internet or external services required
- ⚡ **CPU Only** - No GPU dependencies
- 🐧 **Linux AMD64** - Optimized for Linux systems
- 📦 **Docker Ready** - Easy deployment with containerization
- 🔍 **OCR Support** - Handles scanned/image-based PDFs with Tesseract
- 📊 **Multi-format Support** - Works with structured and unstructured PDFs

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **PDF Processing:** PyMuPDF + pdfplumber
- **OCR Engine:** Tesseract OCR + pytesseract
- **Image Processing:** pdf2image, Pillow
- **Container:** Docker with python:3.11-slim base
- **Platform:** Linux AMD64

---

## 📦 Input & Output

### Input
- PDF files (≤ 50 pages)
- Any standard PDF format (structured or scanned)
- Supports multilingual documents

### Output
```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Chapter 1: Introduction",
      "page": 1
    },
    {
      "level": "H2",
      "text": "1.1 Overview", 
      "page": 2
    },
    {
      "level": "H3",
      "text": "1.1.1 Background",
      "page": 3
    }
  ]
}
```

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Pull the image
docker pull savyasachi2005/pdf-outline-extractor:latest

# Run with volume mount
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output savyasachi2005/pdf-outline-extractor:latest

# Output JSON files will be created in your output/ directory
```

### Option 2: Local Python

```bash
# Clone the repository
git clone https://github.com/Savyasachi-2005/adobe-outline-extractor.git
cd adobe-outline-extractor

# Install dependencies
pip install -r requirements.txt

# Install system dependencies (Ubuntu/WSL)
sudo apt update && sudo apt install tesseract-ocr poppler-utils

# Run the extractor
python main.py
```

---

## 🔧 Installation

### Prerequisites
- Python 3.11+
- Docker (optional, for containerized deployment)
- Linux AMD64 system (recommended)

### Setup Instructions

#### 1. Clone the Repository
```bash
git clone https://github.com/Savyasachi-2005/adobe-outline-extractor.git
cd adobe-outline-extractor
```

#### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Install System Dependencies

**Ubuntu / WSL:**
```bash
sudo apt update
sudo apt install tesseract-ocr poppler-utils
```

**macOS (using Homebrew):**
```bash
brew install tesseract poppler
```

**Windows:**
- [Install Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Install Poppler for Windows](http://blog.alivate.com.au/poppler-windows/)
- Add both to your system `PATH`

---

## 📁 Project Structure

```
.
├── main.py             # Entry point script to process all PDFs
├── extractor.py        # Core logic for outline extraction (text + OCR fallback)
├── requirements.txt    # Required Python packages
├── Dockerfile          # Docker container configuration
├── input/              # Place your input .pdf files here
└── output/             # Extracted JSON files will be saved here
```

---

## 📖 Usage Examples

### Basic Usage
```bash
# Place PDFs in input/ folder and run
python main.py

# Output: JSON files created in output/ folder
```

### Docker Usage
```bash
# Build the image
docker build -t adobe-pdf-outline .

# Run with volume mounts
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output adobe-pdf-outline

# Batch processing - all PDFs in input/ folder will be processed
```

### API Usage
```python
from extractor import PDFOutlineExtractor

# Initialize extractor
extractor = PDFOutlineExtractor()

# Extract outline from PDF
outline = extractor.extract_outline('document.pdf')

# Save to JSON
import json
with open('outline.json', 'w') as f:
    json.dump(outline, f, indent=2)
```

---

## 🧠 How It Works

1. **PDF Analysis** - Uses PyMuPDF to extract structured text and metadata
2. **OCR Fallback** - Applies Tesseract OCR for scanned/image-based PDFs
3. **Heading Detection** - Analyzes text formatting using layout-based heuristics:
   - **Font Size Analysis** - Larger fonts indicate higher-level headings
   - **Line Positioning** - Spacing and alignment patterns
   - **Text Formatting** - Bold, uppercase, and style variations
4. **Structure Building** - Creates hierarchical outline (H1, H2, H3)
5. **JSON Output** - Generates clean, structured data with page numbers

---

## 📊 Performance Benchmarks

| Metric | Performance |
|--------|-------------|
| **50-page PDF Processing** | ≤ 10 seconds |
| **Model Size** | < 200 MB |
| **Memory Usage** | < 200 MB |
| **CPU Requirements** | Single core sufficient |
| **Offline Capability** | ✅ Full offline operation |
| **OCR Support** | ✅ Multilingual via Tesseract |

---

## 🐳 Docker Configuration

### Dockerfile
```dockerfile
FROM python:3.11-slim

RUN apt update && apt install -y tesseract-ocr poppler-utils

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

ENV INPUT_DIR=/app/input
ENV OUTPUT_DIR=/app/output

CMD ["python", "main.py"]
```

### Build and Run
```bash
# Build the Docker image
docker build -t adobe-pdf-outline .

# Run the container
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output adobe-pdf-outline
```

---

## 📋 Requirements

```
PyMuPDF>=1.23.0
pytesseract>=0.3.10
pdf2image>=3.1.0
Pillow>=10.0.0
numpy>=1.24.0
```

---

## ✅ Adobe Hackathon Constraints (Satisfied)

| Constraint | Support | Status |
|------------|---------|--------|
| CPU-only | ✅ Yes | No GPU dependencies |
| Model size < 200 MB | ✅ Yes | Lightweight libraries only |
| No Internet required | ✅ Yes | Fully offline operation |
| Execution ≤ 10s per PDF (50 pages) | ✅ Tested | Optimized processing |
| Multilingual / image PDFs | ✅ Supported | Via OCR integration |

---

## 🧪 Testing

### Sample Output
**Input File:** `TOPJUMP-PARTY-INVITATION-20161003-V01.pdf`  
**Output File:** `output/TOPJUMP-PARTY-INVITATION-20161003-V01.json`

```json
{
  "title": "HOPE To SEE You THERE!",
  "outline": [
    { "text": "ADDRESS:", "level": "H3", "page": 1 },
    { "text": "TOPJUMP", "level": "H3", "page": 1 },
    { "text": "3735 PARKWAY", "level": "H1", "page": 1 },
    { "text": "PIGEON FORGE, TN 37863", "level": "H3", "page": 1 },
    { "text": "RSVP: ----------------", "level": "H1", "page": 1 },
    { "text": "PLEASE VISIT TOPJUMP.COM TO FILL OUT WAIVER", "level": "H2", "page": 1 },
    { "text": "HOPE To SEE You THERE!", "level": "H1", "page": 1 },
    { "text": "WWW.TOPJUMP.COM", "level": "H2", "page": 1 }
  ]
}
```

---

## 🐛 Known Limitations

- Maximum 50 pages per PDF (Adobe constraint)
- Heading detection based on heuristic patterns
- OCR accuracy depends on image quality
- Optimized for Linux AMD64 platform

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ✉️ Contact

Feel free to raise an issue or drop a message if you have questions or feature requests. Good luck hacking! 🚀

---

*Built with ❤️ for Adobe Hackathon 2025*
