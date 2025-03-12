from flask import Flask, request, jsonify
import pdfplumber
import os

app = Flask(__name__)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        extracted_text = extract_text_from_pdf(file_path)
        print("Extracted Text:", extracted_text)  # Debugging

        # Placeholder for text processing and analysis
        analysis = {
            "education": "Bachelor's in Computer Science" if "computer" in extracted_text.lower() else "Not found",
            "experience": ["Software Engineer", "Intern"] if "intern" in extracted_text.lower() else [],
            "skills": ["Python", "JavaScript", "Machine Learning"] if "python" in extracted_text.lower() else []
        }

        print("Final Analysis:", analysis)  # Debugging
        return jsonify({"analysis": analysis})

if __name__ == "__main__":
    app.run(debug=True)
