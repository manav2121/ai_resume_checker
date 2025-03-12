from flask_cors import CORS
from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, origins=["https://earnest-chimera-848a94.netlify.app"])


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)
    
    # Simulated resume processing result
    analysis_result = {
        "skills": ["Python", "Machine Learning", "Web Development"],
        "experience": ["Software Engineer at XYZ", "Intern at ABC"],
        "education": "Bachelor's in Computer Science"
    }
    
    response_data = {
        "message": "File uploaded successfully!",
        "filename": filename,
        "analysis": analysis_result
    }
    
    print("Response to frontend:", response_data)  # Debugging log
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
