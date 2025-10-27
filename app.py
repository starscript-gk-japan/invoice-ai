from flask import Flask, request, render_template
import fitz  # PyMuPDF
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        pdf_file = request.files.get("pdf")
        if pdf_file:
            text = extract_text(pdf_file)
            amounts = extract_amounts_only(text)
            comment = generate_ai_comment(text)
            # Add AI-generated comment to the extracted amounts
            amounts["comment"] = comment
            result = amounts
    return render_template("index.html", result=result)

def extract_text(pdf):
    """Extract all text from a PDF"""
    text = ""
    with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_amounts_only(text):
    """Extract only the monetary amounts"""
    amounts = re.findall(r"\$[0-9,]+\.\d{2}", text)

    line_items = amounts[:-3] if len(amounts) > 3 else []
    subtotal = amounts[-3] if len(amounts) >= 3 else "N/A"
    tax = amounts[-2] if len(amounts) >= 2 else "N/A"
    total = amounts[-1] if len(amounts) >= 1 else "N/A"

    return {
        "Line Item Amounts": line_items,
        "Subtotal": subtotal,
        "Sales Tax": tax,
        "Total": total
    }

def generate_ai_comment(text):
    """Simple AI comment generator"""
    examples = [
        "This invoice includes consulting and support services.",
        "This invoice is for monthly subscription billing.",
        "This invoice contains hardware purchase and shipping fees."
    ]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(examples + [text])
    sims = cosine_similarity(X[-1:], X[:-1]).flatten()
    return examples[sims.argmax()]

if __name__ == "__main__":
    app.run(debug=True)
