from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech_recognition as sr
import pyaudio
import requests
import nltk


# HTTP client configuration
base_url = 'http://localhost:9000/'


# speech to text
def speech_to_text():
    r = sr.Recognizer()
    r.non_speaking_duration = 0.3
    print('Listening.......')
    with sr.Microphone() as source:
        audio = r.listen(source)
        print('Finished audio recording')
        text = ''
        try:
            # request to google's speech recognition package to convert to text
            text = r.recognize_google(audio)
            print(text)
        except Exception as e:
            pass
    return text.lower()


# sentiment analysis
def sentiment_analysis_score(text):
    # Model 1
    # sentiment_result = TextBlob(text)  # takes the text and analyzes it
    # score = sentiment_result.sentiment.polarity  # polarity = numerical score

    # Model 2
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)["compound"]
    print(score)
    return score


# general flow
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
    

    # if (sentiment_score >= 0.25) and (sentiment_score <= 1):
    #     return "happiest"
    # elif (sentiment_score >= 0.01) and (sentiment_score < 0.25):
    #     return "happy"
    # elif (sentiment_score == 0.0):
    #     return "neutral"
    # elif (sentiment_score <= -0.01) and (sentiment_score > -0.25):
    #     return "mad"
    # elif (sentiment_score <= -0.25) and (sentiment_score == -1):
    #     return "maddest"

while True:
    text = speech_to_text()
    sentiment_score = sentiment_analysis_score(text)
    sentiment = get_sentiment(sentiment_score)
    print(sentiment)
    # Define the endpoint URL
    url = f'{base_url}'  # Replace with the actual endpoint URL

    # Define the payload data to send
    data = {'sentiment': sentiment}  # Replace with your desired data

    # Send the POST request

    response = requests.post(url, json=data)

    # Check the response
    if response.status_code == 200:
        print('Message sent successfully!')
    else:
        print('Failed to send message:', response.text)
