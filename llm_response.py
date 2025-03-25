import openai
import json
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def compare_two_articles(article1, article2, openai_api_key):
    """
    Generates a comparison between two articles using OpenAI's GPT-4o mini model.
    
    Args:
        article1 (dict): Dictionary with 'summary' key for the first article
        article2 (dict): Dictionary with 'summary' key for the second article
        openai_api_key (str): Your OpenAI API key
    
    Returns:
        dict: Comparison and impact analysis as a dictionary
    """
    # Configure the OpenAI API client
    openai.api_key = openai_api_key
    
    # Construct the prompt
    prompt = f"""
    Compare these two articles and provide ONE clear comparison with impact analysis:
    
    ARTICLE 1: {article1.get('summary', '')}
    ARTICLE 2: {article2.get('summary', '')}
    
    Respond with exactly ONE JSON object containing:
    1. "Comparison" - Key difference between the articles
    2. "Impact" - Practical consequence of this difference
    
    Use this exact format:
    {{
        "Comparison": "Concise contrast of main focuses",
        "Impact": "Analysis of how this difference matters"
    }}
    """
    
    try:
        # Call the OpenAI API with GPT-4o mini
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Specify the GPT-4o mini model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides precise, structured comparisons."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}  # Ensure JSON response
        )
        
        # Extract and parse the JSON response
        comparison_json = response.choices[0].message.content
        return json.loads(comparison_json)
    
    except openai.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        return None
    except json.JSONDecodeError:
        print("Failed to parse JSON response")
        return None
