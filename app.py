from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)
app.config["DEBUG"] = True  # Enable debug mode

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return "Flask app is running!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    return jsonify({"message": "File uploaded successfully", "filename": file.filename})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT from Render, default to 5000
    app.run(host='0.0.0.0', port=port)

