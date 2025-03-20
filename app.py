from flask import Flask, request, jsonify
import os
import nltk
import pdfplumber  # Alternative to PyMuPDF

# Ensure NLTK is ready
nltk.download('punkt')

app = Flask(__name__)

# Set up the upload folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Function to extract text from a PDF using pdfplumber
def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()
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
        "keyword_match_score": (len(matched_keywords) / len(keywords)) * 100
    }

@app.route("/")
def home():
    return "Resume Analysis API is running!"

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
    if "Error" in resume_text:
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
