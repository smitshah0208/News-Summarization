import nltk
nltk.download("vader_lexicon")
from nltk.sentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    """
    A class to perform sentiment analysis on a list of articles using VADER.
    """

    def __init__(self, articles):
        """
        Initializes the SentimentAnalyzer with a list of articles.

        Args:
            articles (list): A list of dictionaries containing article details.
        """
        self.articles = articles
        self.sia = SentimentIntensityAnalyzer()  # Initialize VADER sentiment analyzer

    def analyze_sentiment(self, text):
        """
        Analyzes the sentiment of the given text using VADER.

        Args:
            text (str): The text to analyze.

        Returns:
            str: The sentiment label ("positive", "negative", or "neutral").
        """
        if not text:
            return "neutral"  # Return neutral if text is empty

        # Get sentiment scores
        sentiment_scores = self.sia.polarity_scores(text)

        # Determine sentiment based on compound score
        if sentiment_scores["compound"] >= 0.25:
            return "positive"
        elif sentiment_scores["compound"] <= -0.25:
            return "negative"
        else:
            return "neutral"

    def analyze_articles(self):
        """
        Performs sentiment analysis on all articles in the list.

        Returns:
            list: A list of dictionaries with added sentiment analysis results.
        """
        for article in self.articles:
            sentiment = self.analyze_sentiment(article.get("summary"))
            article["sentiment"] = sentiment  # Add sentiment to the article dictionary

        return self.articles