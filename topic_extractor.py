import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Download necessary NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class NewsTopicExtractor:
    def __init__(self):
        # Load spaCy English model
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            print("Downloading spaCy English model...")
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load('en_core_web_sm')
        
        # Stop words to filter out
        self.stop_words = set(stopwords.words('english'))
    
    def extract_topics(self, summary, num_topics=3):
        """
        Extract topics from a news summary
        
        Args:
            summary (str): News summary text
            num_topics (int): Number of topics to extract
        
        Returns:
            list: Extracted topics
        """
        # Process the summary with spaCy
        doc = self.nlp(summary)
        
        # Extract named entities and nouns as potential topics
        potential_topics = []
        
        # Add named entities
        potential_topics.extend([ent.text for ent in doc.ents 
                                 if ent.label_ in ['ORG', 'PERSON', 'GPE', 'PRODUCT']])
        
        # Add important nouns and proper nouns
        potential_topics.extend([token.text for token in doc 
                                 if token.pos_ in ['PROPN', 'NOUN'] 
                                 and token.text.lower() not in self.stop_words
                                 and len(token.text) > 2])
        
        # Remove duplicates while preserving order
        topics = list(dict.fromkeys(potential_topics))
        
        # If not enough topics, use TF-IDF to extract more
        if len(topics) < num_topics:
            vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
            tfidf_matrix = vectorizer.fit_transform([summary])
            feature_names = vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            # Get top TF-IDF terms
            top_indices = tfidf_scores.argsort()[-num_topics:][::-1]
            tfidf_topics = [feature_names[i] for i in top_indices]
            
            topics.extend(tfidf_topics)
        
        # Ensure unique topics and limit to num_topics
        topics = list(dict.fromkeys(topics))[:num_topics]
        
        # Capitalize topics
        topics = [topic.capitalize() for topic in topics]
        
        return topics
    
    def get_articles_with_topics(self, articles):
        processed_articles = []
        for article in articles:
            try:
                # Create a copy of the article dictionary to avoid modifying the original
                processed_article = article.copy()
                if isinstance(processed_article, dict) and "summary" in processed_article:
                    topic_list = self.extract_topics(processed_article["summary"])
                    processed_article["topics"] = topic_list
                processed_articles.append(processed_article)
            except Exception as e:
                print(f"Error processing the article: {e}")
                # If there's an error, still add the original article
                processed_articles.append(article)

        return processed_articles

