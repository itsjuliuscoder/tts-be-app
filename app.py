from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS # type: ignore
import os
from utils import extract_text 

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return jsonify({
        "appname": "Text to Speech API",
        "version": "1.0.0",
        "description": "This is a simple text-to-speech API. Upload a file and specify the language to generate a speech.",
        "endpoint": {
            "upload": "/upload"
        }
    }), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    language = request.form['language']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Extract text from the file
    text = extract_text(filepath)
    if not text: 
        return {"error": "No text found in the file"}, 400
    
    # Generate speech
    tts = gTTS(text, lang=language)
    output_path = os.path.join(UPLOAD_FOLDER, 'output.mp3')
    tts.save(output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use PORT from environment
    app.run(host="0.0.0.0", port=port) 