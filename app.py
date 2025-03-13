from flask import Flask, render_template, request, jsonify
import os
import nltk
import language_tool_python
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Configure file upload folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

# Initialize NLP tools
nltk.download("punkt")
tool = language_tool_python.LanguageToolPublicAPI("en-US")


def allowed_file(filename):
    """Check if the uploaded file has a valid extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_resume():
    """Handle resume file upload and analysis."""
    if "resume" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only PDF, DOC, and DOCX allowed"}), 400

    # Save file securely
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Resume analysis (Mock Data - Replace with AI/ML Processing)
    analysis_result = {
        "skills_detected": ["Python", "Machine Learning", "Flask"],
        "experience_level": "3+ years",
        "grammar_issues": tool.check("This are an example of incorrect sentence."),
        "readability_score": 8.5,  # Simulated readability score
    }

    return jsonify(analysis_result)


if __name__ == "__main__":
    app.run(debug=True)
