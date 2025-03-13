from flask import Flask, render_template, request, jsonify
import os
from analysis import analyze_resume  # Make sure analysis.py exists

app = Flask(__name__)

# Serve Homepage
@app.route("/")
def home():
    return render_template("index.html")  # Ensure index.html is in the "templates/" folder

# Handle Resume Upload and Analysis
@app.route("/upload", methods=["POST"])
def upload():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save file temporarily
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)  # Ensure the folder exists
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    # Analyze resume
    try:
        result = analyze_resume(file_path)
        return jsonify({"message": "Resume processed successfully", "analysis": result})
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
