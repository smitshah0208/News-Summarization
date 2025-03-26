from summarization.response import NYTimesScraper
from summarization.sentiment_analyzer import SentimentAnalyzer
from summarization.topic_extractor import NewsTopicExtractor
from summarization.llm_response import CoverageComparison
from utils import get_sentiment_distribution,analyze_article_topics_pairs
from summarization.text_speech import TextToSpeechConverter
from fastapi import FastAPI,HTTPException, APIRouter
from typing import Dict,Any,List

import os
from dotenv import load_dotenv
load_dotenv()

news_report_router = APIRouter()

gemini_api_key = os.getenv("GEMINI_API_KEY")

def get_report(company_name: str,api_key = gemini_api_key)->Dict[str, Any]:
    scraper = NYTimesScraper(company_name)
    articles = scraper.get_articles()
    sentiment_analyzer = SentimentAnalyzer(articles)
    articles = sentiment_analyzer.analyze_articles()
    news_topic_extractor = NewsTopicExtractor()
    articles = news_topic_extractor.get_articles_with_topics(articles)
    sentiment_distribution = get_sentiment_distribution(articles)
    coverage = CoverageComparison(api_key)
    coverage_differences, final_sentiment = coverage.get_all_analysis(articles)
    topic_overlap = analyze_article_topics_pairs(articles)
    converter = TextToSpeechConverter()
    audio_file_path = converter.convert_english_to_hindi_audio(final_sentiment["Final Sentiment Analysis"])

    # Modified articles list to include only title, summary, sentiment, and topics
    simplified_articles = []
    for article in articles:
        simplified_articles.append({
            "Title": article.get("title"),
            "Summary": article.get("summary"),
            "Sentiment": article.get("sentiment"),
            "Topics": article.get("topics")
        })

    result = {
        "Company": company_name,
        "Articles": simplified_articles,  # Using the simplified articles list
        "Comparative Sentiment Score": sentiment_distribution,
        "Coverage Differences": coverage_differences,
        "Topic Overlap": topic_overlap,
        "Final Sentiment Analysis": final_sentiment["Final Sentiment Analysis"],
        "Audio": audio_file_path
    }

    return result
       
@news_report_router.get("/report/{company_name}")
async def generate_report(company_name: str) -> Dict[str,Any]:
    try:
        report = get_report(company_name)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
