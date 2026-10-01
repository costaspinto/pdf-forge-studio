# PDF Forge Studio

**Offline-first PDF utility for Windows — compress, merge, split, rotate, convert, and inspect PDFs with a native desktop interface.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-2C2C2C)
![PDF Engine](https://img.shields.io/badge/PDF-PyMuPDF-6B4FBB)
![Image Processing](https://img.shields.io/badge/Images-Pillow-8A2BE2)
![Privacy](https://img.shields.io/badge/Processing-Local--Only-2E7D32)
![License](https://img.shields.io/badge/License-MIT-green)
![alt text](image.png)
> **PDF Forge Studio** is a local Windows desktop application designed for practical PDF workflows where documents should remain on the user's machine.

![alt text](image-2.png)

## Overview
PDF Forge Studio provides a focused set of common PDF operations through a simple desktop UI:

- PDF compression with selectable quality profiles
- PDF merging
- PDF splitting
- Page extraction
- Page rotation
- PDF-to-PNG conversion
- Images-to-PDF conversion
- PDF metadata / document information
- Automatic backups before compression
- Unique output filenames to avoid accidental overwrites
- Progress reporting and operation status
- Local error logging

The application does **not** upload documents to a remote server or require a cloud account for PDF processing.

---

## Key Features

### PDF Compression

Four predefined compression profiles balance file size and visual quality:

| Profile | Target DPI | JPEG Quality | Intended Use |
|---|---:|---:|---|
| High | 200 | 90 | Higher visual quality |
| Medium | 150 | 80 | General document sharing |
| Small | 120 | 70 | Smaller attachments |
| Very Small | 100 | 60 | Aggressive size reduction |

Compression reports the original size, resulting size, and percentage reduction.

> Compression results depend on the source PDF. Text/vector-heavy PDFs may behave differently from scanned/image-heavy PDFs.

### PDF Management

- **Merge** multiple PDF files into one document
- **Split** a PDF into individual page files
- **Extract** selected pages such as `1,3,5-7`
- **Rotate** pages by 90°, 180°, or 270°
- **PDF → PNG** page rendering
- **Images → PDF** document creation
- **PDF Info** for basic document metadata

### File Safety

The application is designed to reduce accidental data loss:

- Creates backups before compression
- Uses unique output filenames
- Keeps generated files in dedicated application folders
- Logs application errors locally
- Does not overwrite source files during normal operations

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Desktop GUI | Tkinter |
| PDF processing | PyMuPDF |
| Image processing | Pillow |
| Packaging / execution | Windows CMD + Python |
| Storage | Local Windows filesystem |

### Why these technologies?

**Python** provides a mature ecosystem for document and image processing.

**Tkinter** keeps the desktop application lightweight and avoids requiring a separate GUI framework.

**PyMuPDF** provides fast PDF parsing, rendering, page manipulation, and document operations.

**Pillow** handles image conversion and encoding required by image/PDF workflows.

---

## Architecture

```text
                    PDF Forge Studio
                           │
                    Tkinter Desktop UI
                           │
              ┌────────────┴────────────┐
              │                         │
        PDF Operations            Image Operations
              │                         │
          PyMuPDF                    Pillow
              │                         │
              └────────────┬────────────┘
                           │
                  Local Windows Filesystem
                           │
              ┌────────────┼────────────┐
              │            │            │
           Output       Backups        Logs
```

The application follows a local-first processing model:

```text
User selects file
       ↓
GUI validates input
       ↓
PDF/image operation
       ↓
Temporary processing in memory/filesystem
       ↓
Output generated with unique name
       ↓
Status + result reported to user
```

---

## Project Structure

```text
pdf-forge-studio/
│
├── PDF_Forge_Studio.py
├── Install_PDF_Forge_Studio.cmd
├── Run_PDF_Forge_Studio.cmd
├── README.md
├── READ_BEFORE_INSTALL.txt
├── .gitignore
└── LICENSE
```

Runtime-generated directories are intentionally excluded from Git:

```text
Downloads/
└── PDF_Forge_Studio/
    ├── Output/
    ├── Backups/
    └── Logs/
```

---

## Requirements

- Windows 10 or Windows 11
- Python 3.10+
- PyMuPDF
- Pillow

Python dependencies:

```text
pymupdf
pillow
```

The included installer can install the required Python dependencies.

---

## Installation

### Option 1 — Installer

Keep these files together:

```text
PDF_Forge_Studio.py
Install_PDF_Forge_Studio.cmd
Run_PDF_Forge_Studio.cmd
```

Then run:

```text
Install_PDF_Forge_Studio.cmd
```

The installer checks for Python and installs the required dependencies.

### Option 2 — Manual Setup

Install dependencies:

```bash
python -m pip install pymupdf pillow
```

Run:

```bash
python PDF_Forge_Studio.py
```

---

## Output Locations

The application stores its working data under:

```text
%USERPROFILE%\Downloads\PDF_Forge_Studio\
```

Typical structure:

```text
PDF_Forge_Studio/
├── Output/
├── Backups/
└── Logs/
```

The application log is:

```text
Logs\pdf_forge.log
```

---

## Example Page Selection Syntax

The page extraction feature accepts ranges such as:

```text
1
```

```text
1,3,5
```

```text
1-5
```

```text
1,3,5-7
```

This allows users to extract non-contiguous pages without manually splitting the entire document.

---

## Privacy Model

PDF Forge Studio is designed around local processing.

### No cloud upload

Documents are processed on the local Windows machine.

### No account required

The application does not require a user account or remote API for its core PDF functionality.

### No document analytics

The application does not intentionally transmit document contents to an external analytics service.

> Users should still review any third-party Python packages and their own operating-system security configuration before deploying the application in sensitive environments.

---

## Security Considerations

PDF files can contain malicious or malformed content. PDF Forge Studio relies on PyMuPDF for PDF parsing and rendering.

Recommended practices:

- Keep Python and dependencies updated.
- Process untrusted PDFs in an appropriately secured environment.
- Do not run the application with unnecessary administrative privileges.
- Keep Windows Defender / endpoint protection enabled.
- Do not disable Windows security controls to run the application.

The project intentionally does not implement mechanisms to bypass Windows security protections such as Smart App Control.

---

## Error Handling

Startup and runtime errors are written to:

```text
%USERPROFILE%\Downloads\PDF_Forge_Studio\Logs\pdf_forge.log
```

When reporting a bug, include:

1. Windows version
2. Python version
3. Operation being performed
4. Relevant log traceback
5. Input PDF characteristics, if relevant

Do **not** upload confidential documents when reporting an issue.

---

## Development

Clone the repository:

```bash
git clone https://github.com/costaspinto/pdf-forge-studio.git
cd pdf-forge-studio
```

Install dependencies:

```bash
python -m pip install pymupdf pillow
```

Run the application:

```bash
python PDF_Forge_Studio.py
```

Basic syntax validation:

```bash
python -m py_compile PDF_Forge_Studio.py
```

---

## Roadmap

Potential future improvements include:

- Drag-and-drop PDF support
- Thumbnail page previews
- Batch compression
- Custom DPI / JPEG quality controls
- PDF page reordering
- Password-protected PDF support
- PDF/A validation
- OCR integration
- Native Windows executable packaging
- Automated test coverage
- CI validation through GitHub Actions
- Application code signing and release automation

---

## Engineering Notes

This project demonstrates practical desktop application engineering across:

- Python application development
- GUI design
- PDF document processing
- Image processing
- File-system management
- Input validation
- Error handling
- Logging
- Backup and recovery considerations
- Windows installation workflows
- Dependency management
- Privacy-conscious local processing

The project is intentionally structured as a lightweight desktop utility rather than a web application so that document processing can remain local.

---

## License

This project is released under the **MIT License**.

See [`LICENSE`](LICENSE) for the complete license text.

---

## Author

**Costas Pinto**

AI/ML Engineer | Generative AI | LLMs | RAG | Python

GitHub: https://github.com/costaspinto

Portfolio: https://costas-portfolio-ai.vercel.app/

LinkedIn: https://www.linkedin.com/in/costaspinto/

---

## Disclaimer

PDF Forge Studio is provided as a software project for general document-processing purposes.

Always keep the original document when performing destructive or lossy operations such as compression or page manipulation.
