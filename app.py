from flask import Flask, request, render_template
import fitz
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from db_examples import ExampleDB

app = Flask(__name__)
db = ExampleDB()  # Create an instance from the module

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        pdf_file = request.files.get("pdf")
        if pdf_file:
            # Extract text from the uploaded PDF
            text = extract_text(pdf_file)
            # Extract monetary amounts
            amounts = extract_amounts_only(text)
            # Generate AI-based comment using DB examples
            comment = generate_ai_comment(text)
            amounts["comment"] = comment
            result = amounts
    return render_template("index.html", result=result)

def extract_text(pdf):
    """Extract all text from the given PDF file"""
    text = ""
    with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_amounts_only(text):
    """Extract only monetary amounts from the text"""
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
    """
    Retrieve example sentences from the DB and return the most similar example
    using TF-IDF cosine similarity.
    """
    examples_rows = db.list_all(limit=500)  # Fetch required number of examples
    examples = [r["text"] for r in examples_rows]
    if not examples:
        return "No examples found in the database."

    # Compute TF-IDF similarity
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(examples + [text])
    sims = cosine_similarity(X[-1:], X[:-1]).flatten()
    best_idx = int(sims.argmax())
    return examples[best_idx]

if __name__ == "__main__":
    # Run the Flask application
    app.run(debug=True)
