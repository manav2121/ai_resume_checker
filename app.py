from flask import Flask, request, jsonify
import pdfplumber
import re
import spacy

app = Flask(__name__)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_details(text):
    details = {}

    # Extract Name (First Capitalized Words)
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    details["name"] = names[0] if names else "Not Found"

    # Extract Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    details["email"] = email_match.group(0) if email_match else "Not Found"

    # Extract Phone Number
    phone_match = re.search(r"\+?\d[\d -]{8,}\d", text)
    details["phone"] = phone_match.group(0) if phone_match else "Not Found"

    # Extract LinkedIn Profile
    linkedin_match = re.search(r"https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+", text)
    details["linkedin"] = linkedin_match.group(0) if linkedin_match else "Not Found"

    # Extract GitHub Profile
    github_match = re.search(r"https?://(www\.)?github\.com/[a-zA-Z0-9_-]+", text)
    details["github"] = github_match.group(0) if github_match else "Not Found"

    # Extract Skills
    skills_list = ["Python", "JavaScript", "Machine Learning", "Data Science", "Django", "Flask", "React", "SQL"]
    found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    details["skills"] = found_skills if found_skills else ["Not Found"]

    return details

@app.route("/upload", methods=["POST"])
def upload_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    text = extract_text_from_pdf(file)
    analysis = extract_details(text)

    return jsonify({
        "message": "File processed successfully!",
        "analysis": analysis
    })

if __name__ == "__main__":
    app.run(debug=True)
