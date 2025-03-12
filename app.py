from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

def extract_text_from_pdf(file_content):
    """Extract text from the uploaded PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def analyze_resume(file_content):
    """Analyze the resume and extract details dynamically."""
    parsed_text = extract_text_from_pdf(file_content)
    
    # Debugging: Print extracted text
    print(f"Extracted Text: {parsed_text[:500]}")  # First 500 characters

    # Simple mock analysis (Replace this with AI-based processing if needed)
    analysis_result = {
        "education": "Unknown",
        "experience": [],
        "skills": []
    }

    if "Bachelor" in parsed_text:
        analysis_result["education"] = "Bachelor's in Computer Science"
    if "Software Engineer" in parsed_text:
        analysis_result["experience"].append("Software Engineer at XYZ")
    if "Python" in parsed_text:
        analysis_result["skills"].append("Python")
    if "Machine Learning" in parsed_text:
        analysis_result["skills"].append("Machine Learning")
    
    return analysis_result

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload and return the extracted resume analysis."""
    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]
    
    # Read the file content
    file_content = file.read()
    
    # Debugging: Print file details
    print(f"Received file: {file.filename}")
    print(f"File Content (First 500 chars): {file_content[:500]}")

    # Analyze the resume
    analysis_result = analyze_resume(file_content)

    return jsonify({
        "message": "File uploaded successfully!",
        "filename": file.filename,
        "analysis": analysis_result
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
