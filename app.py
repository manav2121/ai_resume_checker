from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from parser import extract_resume_text
from analysis import analyze_resume
from database import save_to_mongo

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Parse resume
    resume_text = extract_resume_text(filepath)
    
    # Analyze resume
    analysis_result = analyze_resume(resume_text)

    # Save to database
    save_to_mongo(filename, analysis_result)

    return jsonify({"filename": filename, "analysis": analysis_result})

if __name__ == "__main__":
    app.run(debug=True)
