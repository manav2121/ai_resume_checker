from flask import Flask, request, jsonify
from flask_cors import CORS  # Allow frontend communication
import os
import nltk
import pdfplumber  # Alternative to PyMuPDF

# Ensure NLTK is ready
nltk.download('punkt')

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests

# Set up the upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Function to extract text from a PDF using pdfplumber
def extract_text_from_pdf(pdf_path):
    try:
        text = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)

        extracted_text = "\n".join(text).strip()
        if not extracted_text:
            return "Error: No text found in the PDF"
        return extracted_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# Function to analyze the resume text
def analyze_resume(text):
    words = nltk.word_tokenize(text.lower())  # Tokenize text
    total_words = len(words)

    # Keywords to match (modify as needed)
    keywords = ["python", "flask", "machine learning", "data science", "API", "resume"]
    matched_keywords = [kw for kw in keywords if kw in words]

    return {
        "word_count": total_words,
        "matched_keywords": matched_keywords,
        "keyword_match_score": round((len(matched_keywords) / len(keywords)) * 100, 2)
    }

@app.route("/")
def home():
    return jsonify({"message": "Resume Analysis API is running!"})

@app.route("/upload", methods=["POST"])
def upload_file():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "Empty file name"}), 400

    # Save the uploaded file
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Extract text from the PDF
    resume_text = extract_text_from_pdf(file_path)
    if resume_text.startswith("Error"):
        return jsonify({"error": resume_text}), 500  # Handle errors

    # Analyze resume text
    analysis_result = analyze_resume(resume_text)

    return jsonify({
        "filename": file.filename,
        "message": "Analysis successful",
        "analysis": analysis_result
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
