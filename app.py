from flask import Flask, request, jsonify
from resume_scanner import extract_text_from_pdf, calculate_similarity

app = Flask(__name__)

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
    file_path = f"temp/{file.filename}"
    file.save(file_path)
    
    # Extract text from the resume
    resume_text = extract_text_from_pdf(file_path)
    
    # Calculate similarity score
    similarity_score = calculate_similarity(resume_text, job_description)
    
    return jsonify({
        "resume_match_score": round(similarity_score, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
