from flask import Flask, render_template, request
from transformers import pipeline
from dotenv import load_dotenv
import os

from scrapers.twitter_scraper import fetch_twitter_replies
from scrapers.youtube_scraper import fetch_youtube_comments

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
#print("YouTube API Key:", YOUTUBE_API_KEY)

app = Flask(__name__)

# Sentiment classifier using your chosen model
classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

def analyze_sentiments(comments):
    #print(f"Analyzing {len(comments)} comments")  # Debug print
    #if not comments:
    #    return {'positive': 0, 'neutral': 0, 'negative': 0}
    results = classifier(comments)
    #print(f"Sample classification results: {results[:3]}")  # Debug print

    sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
    #print("classifier results: ", results)
    for r in results:
        label = r['label']
        print(f"Processing label: {label}")
        if label == 'LABEL_0':  # Negative
            sentiment_counts['negative'] += 1
        elif label == 'LABEL_1':  # Neutral
            sentiment_counts['neutral'] += 1
        elif label == 'LABEL_2':  # Positive
            sentiment_counts['positive'] += 1
        else:
            print("Unknown label:", label)

    #print("Sentiment counts:", sentiment_counts)
    return sentiment_counts

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        url = request.form.get("url")
        comments = []

        if not url:
            error = "Please enter a URL."
            return render_template("index.html", error=error)

        try:
            if "twitter.com" in url:
                comments = fetch_twitter_replies(url, max_comments=500)
            elif "youtube.com" in url or "youtu.be" in url:
                comments = fetch_youtube_comments(url, max_comments=500, api_key=YOUTUBE_API_KEY)
            else:
                error = "Unsupported URL. Please enter a Twitter or YouTube URL."
                return render_template("index.html", error=error)

            # Debug print statements
            print(f"Fetched {len(comments)} comments from URL")
            print("First 5 comments:", comments[:5])

            if not comments:
                error = "No comments found for this post."
                return render_template("index.html", error=error)

            result = analyze_sentiments(comments)

        except Exception as e:
            error = f"Error fetching or analyzing comments: {str(e)}"

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
