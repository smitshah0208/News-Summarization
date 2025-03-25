from response import NYTimesScraper
from sentiment_analyzer import SentimentAnalyzer
from topic_extractor import NewsTopicExtractor
from utils import get_sentiment_distribution, analyze_article_topics

# Example usage
company_name = "Tesla"
scraper = NYTimesScraper(company_name)
articles = scraper.get_articles()
sentiment_analyzer = SentimentAnalyzer(articles)
articles = sentiment_analyzer.analyze_articles()
news_topic_extractor = NewsTopicExtractor()
articles = news_topic_extractor.get_articles_with_topics(articles)

       



for article in articles:
    print(article)

dist = get_sentiment_distribution(articles)
print(dist)


ans = analyze_article_topics(articles)
print(ans)