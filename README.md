# Invoice-AI

A Flask-based PDF text extraction and analysis tool.  
It uses **PyMuPDF (fitz)** and **scikit-learn** for natural language processing to automatically analyze invoice documents.

---

## Setup Guide

### 1️ Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate

###2️ Install Dependencies
pip install -r requirements.txt

###3️ Run Flask App (Optional)
python wrapper.py


Then open http://127.0.0.1:5000
 in your browser
to confirm that the application works correctly.

### Build to EXE (Windows)

Since .exe, build/, and dist/ directories are ignored by .gitignore,
you can rebuild the executable locally using the following command:

pyinstaller --onefile ^
--noconsole ^
--add-data "templates;templates" ^
--add-data "static;static" ^
--hidden-import sklearn ^
--hidden-import torch ^
--collect-all torch ^
--collect-all sklearn ^
wrapper.py

### Output

After building, the executable file will be generated at:

dist/wrapper.exe


Simply double-click wrapper.exe to start the application.
After a few seconds, your browser will automatically open.

### Notes

The .exe, build/, and dist/ folders are excluded from Git tracking.

Run pyinstaller as a normal user (not as administrator).

If you want to rebuild cleanly, delete the following before rebuilding:

rmdir /s /q build
rmdir /s /q dist
del wrapper.spec

### Project Structure
invoice-ai/
├── app.py
├── wrapper.py
├── requirements.txt
├── templates/
├── static/
├── README.md
└── .gitignore

### Development Info

Python: 3.10.11

Framework: Flask

Build Tool: PyInstaller

Recommended OS: Windows 10 / 11