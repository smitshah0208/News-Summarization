# AI News Summarizer with Text-to-Speech

**Introduction:** 
This application provides AI-powered news summarization with text-to-speech capabilities, delivering concise and accessible summaries of company-related news.

## Features

* **News Summarization:** Generates concise summaries of news articles.
* **News Article Retrieval:** Fetches news articles from the New York Times based on a company name.
* **News Article Summarization:** Fetches the news summary related to the articles from the New York Times.
* **Sentiment Analysis:** Analyzes the sentiment of each article (positive, negative, neutral).
* **Topic Extraction:** Extracts key topics from each article.
* **Comparative Sentiment Score:** Provides an overview of the overall sentiment distribution.
* **Coverage Differences:** Compares articles and highlights differences in coverage.
* **Topic Overlap:** Analyzes the common and unique topics across articles.
* **Final Sentiment Analysis:** Provides a summary of the overall sentiment and potential market impact.
* **Audio Summary:** Generates an audio summary of the final sentiment analysis.
* **User-friendly Streamlit interface.**

## Technologies Used

* **FastAPI:** For the backend API.
* **Streamlit:** For the frontend user interface.
* **Docker:** For containerization.
* **Python:** Programming language.
* **New York Times API:** For news article data.
* **Hugging Face Spaces:** For deployment.
* **python-dotenv:** for .env file management.


## Prerequisites

* Docker Desktop installed.
* Hugging Face account.
* Gemini API key.

## Key Features & Workflow:

```mermaid
graph LR
    A[Scrape News] --> B{Summarization & Analysis};
    B --> C[Display Summary Insights Generation];
    C --> D[Final Sentiment using Audio];