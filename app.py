from flask import Flask, request, jsonify
import os
import nltk

# Ensure 'punkt' tokenizer is available
nltk.download('punkt')

app = Flask(__name__)

# Create an "uploads" folder if it doesn't exist
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return "Welcome to Resume Analysis API!"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "Empty file name"}), 400

    # Save the file
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Process the file (Example: Read the content)
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
        return jsonify({"message": "Upload successful", "filename": file.filename}), 200
    except Exception as e:
        return jsonify({"error": f"File processing failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
