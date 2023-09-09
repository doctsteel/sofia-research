import speech_recognition as sr
from flask import jsonify
from vaderSentiment import SentimentIntensityAnalyzer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import os

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'jose.alves2+donotreply@gmail.com'
SMTP_PASSWORD = os.environ["EMAILPASSWORD"]
RECIPIENT_EMAIL = 'sofia.frostnoffs@post.runi.ac.il'

def speech_to_text(audio):
    r = sr.Recognizer()
    text = ''
    with sr.AudioFile(audio) as source:
        try:
            print(source)
            audio_data = r.record(source)
            # request to google's speech recognition package to convert to text
            text = r.recognize_google(audio_data)
            print("Google Speech Recognition thinks you said " + text)
        except sr.UnknownValueError:
            return jsonify({'error': 'Unable to recognize speech'}), 400
        except sr.RequestErro as e:
            return jsonify({'error': f"Speech recognition request failed: {e}"}), 500

        return text.lower()

def sentiment_analysis_score(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)["compound"]
    print(score)
    return score

def get_sentiment(sentiment_score):
    if (sentiment_score >= 0.5) and (sentiment_score <= 1):
        return "happiest"
    if (sentiment_score > 0) and (sentiment_score < 0.5):
        return "happy"
    elif (sentiment_score == 0):
        return "neutral"
    elif (sentiment_score >= -0.5) and (sentiment_score < -0.1):
        return "mad"
    elif (sentiment_score >= -1) and (sentiment_score < -0.5):
        return "maddest"
    
def send_email(text, analysis):
    try:
        # Create a text file with the recognized speech
        with open('recognized_text.txt', 'w') as text_file:
            text_file.write(text + " ")
            text_file.write(analysis)
            text_file.write(" "+ datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        # Create an email message
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = 'Speech to Text Conversion '+ datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Attach the text file to the email
        with open('recognized_text.txt', 'rb') as file:
            part = MIMEApplication(file.read(), Name='recognized_text.txt')
        part['Content-Disposition'] = f'attachment; filename=recognized_text.txt'
        msg.attach(part)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, RECIPIENT_EMAIL, msg.as_string())

        return True
    except Exception as e:
        return str(e)
