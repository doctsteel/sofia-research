from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import speech_recognition as sr
import os
from io import BytesIO
import analyser

app = Flask(__name__)
cors = CORS(app)


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/test', methods=['POST'])
@cross_origin()
def sentiment_analysis():
    print("REQUEST RECEIVED. STARTING PROCESSING.")
    try:
        if "audio" not in request.files:
            return jsonify({'error': 'no audio file received.'}), 400
        audio_file = request.files['audio']
        text = analyser.speech_to_text(audio_file);
        sentiment_score = analyser.sentiment_analysis_score(text)
        sentiment = analyser.get_sentiment(sentiment_score)
        analyser.send_email(text, sentiment)
        # You can process or save the audio file here
        return jsonify({"message": "OK", "text": text})
    except Exception as e:
        return jsonify({"message": "Error analysing audio", "error": str(e)}), 500




