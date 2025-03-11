import os
import shutil
from flask import Flask, request, jsonify
from .resume_scanner import extract_text_from_pdf, calculate_similarity

app = Flask(__name__)

# Ensure temp directory exists
TEMP_FOLDER = "temp"
os.makedirs(TEMP_FOLDER, exist_ok=True)

# Define the job description
job_description = "Looking for a Python developer with experience in machine learning, AI, and SQL."

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the uploaded file temporarily
    file_path = os.path.join(TEMP_FOLDER, file.filename)
    file.save(file_path)
    
    try:
        # Extract text from the resume
        resume_text = extract_text_from_pdf(file_path)
        
        # Calculate similarity score
        similarity_score = calculate_similarity(resume_text, job_description)
        
        # Remove the temporary file after processing
        os.remove(file_path)
        
        return jsonify({"resume_match_score": round(similarity_score, 2)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ensure the app runs on the correct port for deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get PORT from environment variable
    app.run(host="0.0.0.0", port=port)  # Bind to all network interfaces
