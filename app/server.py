from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def sentiment_analysis():
    print("Welcome to sentiment analysis")
    data = request.json
    # Perform sentiment analysis on the received data
    # Replace this with your actual sentiment analysis logic
    sentiment_score = 0.5  # Example sentiment score

    return "200"

if __name__ == '__main__':
    app.run(host='localhost', port=9000, debug=True)