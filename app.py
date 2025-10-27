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
            # Add AI-generated comment to the extracted amount results
            amounts["comment"] = comment
            result = amounts
    return render_template("index.html", result=result)

def extract_text(pdf):
    """Extract all text content from the PDF"""
    text = ""
    with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_amounts_only(text):
    """Extract only monetary amounts"""
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
    """Simple AI-based comment generator with 20 examples"""
    examples = [
        "This invoice includes consulting and support services.",
        "This invoice is for monthly subscription billing.",
        "This invoice contains hardware purchase and shipping fees.",
        "This invoice details software licensing charges.",
        "This invoice covers cloud service subscription fees.",
        "This invoice is for website development and maintenance.",
        "This invoice lists training and onboarding services.",
        "This invoice records office supplies and stationery purchase.",
        "This invoice is for marketing and advertising services.",
        "This invoice details IT support and troubleshooting fees.",
        "This invoice covers subscription to productivity tools.",
        "This invoice is for graphic design and creative services.",
        "This invoice records travel and accommodation expenses.",
        "This invoice details consulting for project management.",
        "This invoice lists subscription fees for SaaS tools.",
        "This invoice covers customer support and helpdesk services.",
        "This invoice is for event organization and coordination.",
        "This invoice details cloud hosting and server maintenance fees.",
        "This invoice lists legal and compliance consulting fees.",
        "This invoice is for research and data analysis services."
    ]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(examples + [text])
    sims = cosine_similarity(X[-1:], X[:-1]).flatten()
    return examples[sims.argmax()]

if __name__ == "__main__":
    app.run(debug=True)
