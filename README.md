# Invoice-AI

A Flask-based PDF and text file analyzer.  
It uses **PyMuPDF (fitz)** and **scikit-learn** for text feature extraction,  
and manages example sentences via **SQLite** for natural language analysis.

---

## Setup Guide

### 1️ Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate

###2️ Install Dependencies
pip install -r requirements.txt

requirements.txt example:

Flask==3.0.2
gunicorn==21.2.0
PyPDF2==3.0.1
PyMuPDF==1.24.9
torch>=2.5.0,<3.0.0
transformers==4.26.1
sentencepiece==0.1.99
safetensors==0.6.2
tokenizers==0.12.1
requests>=2.32.5
scikit-learn==1.5.2

###3️ Initialize Example Database
python init_examples.py

You should see:

[OK] 20 examples have been registered in the database.

This will create examples.db and store all example sentences from the txt file.

You can later update the txt file and re-run init_examples.py to refresh the DB.

###4 Run Flask App (Optional)
python wrapper.py


Then open http://127.0.0.1:5000
 in your browser
to confirm that the application works correctly.

### Build to EXE (Windows)

Since .exe, build/, and dist/ directories are ignored by .gitignore, you can rebuild the executable locally using the following command:

Note for Windows CMD:
If you split the PyInstaller command across multiple lines using ^, Windows may display More? indicating it expects more input.
To avoid this, either put the command in one line or make sure the last line does not end with ^.

One-line example:

pyinstaller --onefile --noconsole --add-data "templates;templates" --add-data "static;static" --hidden-import sklearn --hidden-import torch --collect-all torch --collect-all sklearn wrapper.py

If you want to include optional modules like tensorboard to remove PyInstaller warnings, install them first:

pip install tensorboard

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
├── init_examples.py
├── db_examples.py
├── requirements.txt
├── templates/
├── static/
├── examples/
│   └── sample.txt
├── examples.db        # after initialization
├── README.md
└── .gitignore

### Development Info

Python: 3.10.11

Framework: Flask

Build Tool: PyInstaller

Recommended OS: Windows 10 / 11