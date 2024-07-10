# helpers/ai_helpers.py

from textblob import TextBlob

def analyze_sentiment(text):
    # Example: Perform sentiment analysis using TextBlob
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score
