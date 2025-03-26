def get_sentiment_distribution(articles):
    """
    Calculate the distribution of sentiment labels from a list of articles.
    
    Args:
        articles (list): A list of dictionaries representing articles, where each 
                        dictionary should contain a 'sentiment' key with values
                        'positive', 'negative', or 'neutral'.
    
    Returns:
        dict: A dictionary containing the count of each sentiment category:
              {'positive': int, 'negative': int, 'neutral': int}
    
    Example:
        >>> articles = [{'sentiment': 'positive'}, {'sentiment': 'neutral'}]
        >>> get_sentiment_distribution(articles)
        {'positive': 1, 'negative': 0, 'neutral': 1}
    """
    sentiment_distribution = {"positive": 0, "negative": 0, "neutral": 0}
    
    for article in articles:
        try:
            if isinstance(article, dict) and "sentiment" in article:
                sentiment = article["sentiment"].lower()  # Convert to lowercase for case-insensitive comparison
                if sentiment == "positive":
                    sentiment_distribution["positive"] += 1
                elif sentiment == "negative":
                    sentiment_distribution["negative"] += 1  # Fixed: should increment, not decrement
                else:
                    sentiment_distribution["neutral"] += 1
        except Exception as e:
            print(f"Error processing the article: {e}")
            continue  # Skip to next article if error occurs

    return sentiment_distribution

# def analyze_article_topics(articles):
#     """
#     Analyzes topics across multiple articles to find common and unique topics,
#     with case-insensitive comparison while preserving original case in results.
    
#     Args:
#         articles: List of dictionaries, each containing a 'topics' key with a list of words
        
#     Returns:
#         A dictionary with:
#         - 'common_words_across_all_topics': List of words common to all articles (original case from first article)
#         - 'unique_words_in_article_X': List of words unique to each article (X is index, original case preserved)
#     """
#     if not articles:
#         return {}
    
#     # Create a list of dictionaries with original topics and normalized (lowercase) versions
#     processed_articles = []
#     for article in articles:
#         if 'topics' not in article or not isinstance(article['topics'], list):
#             processed_articles.append({'original': [], 'normalized': set()})
#             continue
            
#         # Create mapping from normalized to original words (preserve first occurrence's case)
#         case_mapping = {}
#         normalized_topics = set()
        
#         for word in article['topics']:
#             normalized = word.lower()
#             if normalized not in case_mapping:
#                 case_mapping[normalized] = word
#             normalized_topics.add(normalized)
        
#         processed_articles.append({
#             'original': article['topics'],
#             'normalized': normalized_topics,
#             'case_mapping': case_mapping
#         })
    
#     # Get all normalized topic sets
#     normalized_sets = [article['normalized'] for article in processed_articles]
    
#     # Find common words across all articles (normalized)
#     common_normalized = set.intersection(*normalized_sets) if normalized_sets else set()
    
#     # Get original case for common words (using first article's case)
#     common_words = []
#     if common_normalized and processed_articles[0]['case_mapping']:
#         common_words = [processed_articles[0]['case_mapping'].get(word, word) 
#                         for word in common_normalized]
    
#     # Prepare the result dictionary
#     result = {
#         'common_words_across_all_topics': common_words
#     }
    
#     # Find unique words for each article
#     for i, article in enumerate(processed_articles):
#         # Get all other normalized topic sets
#         other_sets = normalized_sets[:i] + normalized_sets[i+1:]
        
#         # Find normalized words unique to this article
#         unique_normalized = article['normalized'] - set.union(*other_sets) if other_sets else article['normalized']
        
#         # Get original case for unique words
#         unique_words = []
#         if unique_normalized:
#             # For words that appear multiple times in the same article (with different case),
#             # we include all original occurrences to preserve all variations
#             original_topics = article['original']
#             unique_words = [word for word in original_topics 
#                           if word.lower() in unique_normalized]
        
#         result[f'unique_words_in_article_{i+1}'] = unique_words
    
#     return result

def analyze_article_topics_pairs(articles):
    """
    Analyzes topics across pairs of articles to find common and unique topics,
    with case-insensitive comparison while preserving original case in results.
    Returns a single list of common words across pairs.

    Args:
        articles: List of dictionaries, each containing a 'topics' key with a list of words

    Returns:
        A dictionary with:
        - 'common_words_across_pairs': List of words common to pairs of articles
        - 'unique_words_in_article_X': List of words unique to each article (X is index, original case preserved)
    """
    if not articles:
        return {}

    processed_articles = []
    for article in articles:
        if 'topics' not in article or not isinstance(article['topics'], list):
            processed_articles.append({'original': [], 'normalized': set(), 'case_mapping': {}})
            continue

        case_mapping = {}
        normalized_topics = set()

        for word in article['topics']:
            normalized = word.lower()
            if normalized not in case_mapping:
                case_mapping[normalized] = word
            normalized_topics.add(normalized)

        processed_articles.append({
            'original': article['topics'],
            'normalized': normalized_topics,
            'case_mapping': case_mapping
        })

    result = {
        'common_words_across_pairs': []
    }

    # Find common words for each pair of articles and flatten into a single list
    for i in range(0, len(processed_articles) - 1, 2):
        article1 = processed_articles[i]
        article2 = processed_articles[i + 1]

        common_normalized = article1['normalized'].intersection(article2['normalized'])

        if common_normalized:
            common_words = [article1['case_mapping'].get(word, word) for word in common_normalized]
            result['common_words_across_pairs'].extend(common_words)

    # Find unique words for each article
    for i, article in enumerate(processed_articles):
        other_sets = [processed_articles[j]['normalized'] for j in range(len(processed_articles)) if j != i]

        unique_normalized = article['normalized'] - set.union(*other_sets) if other_sets else article['normalized']

        unique_words = []
        if unique_normalized:
            original_topics = article['original']
            unique_words = [word for word in original_topics if word.lower() in unique_normalized]

        result[f'unique_words_in_article_{i+1}'] = unique_words

    return result