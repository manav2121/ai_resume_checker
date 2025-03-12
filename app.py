from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import os

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from frontend

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return "Welcome to the Resume Analyzer API. Use /upload to upload resumes."

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)
    
    # Extract text from the PDF
    extracted_text = extract_text_from_pdf(file_path)
    
    # Perform analysis (dummy example for now)
    analysis_result = analyze_resume(extracted_text)
    
    return jsonify({
        "message": "File uploaded successfully!",
        "filename": file.filename,
        "analysis": analysis_result
    })

def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with open(pdf_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return str(e)

def analyze_resume(text):
    # Dummy analysis - replace with actual NLP processing
    return {
        "education": "Bachelor's in Computer Science" if "computer science" in text.lower() else "Unknown",
        "experience": ["Software Engineer at XYZ"] if "software engineer" in text.lower() else [],
        "skills": ["Python", "Machine Learning"] if "python" in text.lower() else ["Unknown"]
    }

if __name__ == "__main__":
    app.run(debug=True)
