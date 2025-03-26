import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

class CoverageComparison:

    def __init__(self, api_key):
        """
        Initialize the CoverageComparison class.
        
        Args:
            api_key (str, optional): Gemini API key. If not provided, will try to load from environment.
        """
        self.api_key = api_key

    def compare_two_articles(self, i, article1, article2, gemini_api_key):
        """
        Generates a precise one-line comparison between two articles using Google's Gemini Flash model.
        
        Args:
            article1 (dict): Dictionary with 'title' and 'summary' keys
            article2 (dict): Dictionary with 'title' and 'summary' keys
            gemini_api_key (str): Your Gemini API key
        
        Returns:
            dict: {"Comparison": "one-line", "Impact": "one-line"}
        """
        client = genai.Client(api_key=self.api_key)
        
        prompt = f"""Compare these articles and respond in JSON format :

        Article {i} - Title: {article1.get('title','')}
        Summary: {article1.get('summary','')}

        Article {i+1} - Title: {article2.get('title','')}
        Summary: {article2.get('summary','')}

        Provide:
        1. "Comparison": One sentence highlighting key difference
        2. "Impact": One sentence on practical consequence

        Note: It should strictly avoid any other extra words like "JSON", etc.

        Format exactly like this:
        {{
            "Comparison": "Your one-line comparison here",
            "Impact": "Your one-line impact here"
        }}"""
        
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",  # Using the faster Flash model
                contents=[prompt],
                
            )
            
            
            # Extract the text and remove any markdown code block formatting
            response_text = response.text.strip('`json\n').strip('`').strip()

            # Parse the JSON response
            result = json.loads(response_text) 

            return {
                "Comparison": " ".join(result["Comparison"].split()),
                "Impact": " ".join(result["Impact"].split())
            }
        except json.JSONDecodeError as je:
            print(f"JSON Parsing Error: {je}")
            # print(f"Received response: {response.text}")
            return {
                "Comparison": "Parsing error",
                "Impact": "Unable to parse response"
            }
        except Exception as e:
            print(f"API Error: {e}")
            return {
                "Comparison": "Comparison unavailable",
                "Impact": "Impact analysis failed"
            }

    def get_analysis_across_all(self, articles):
        """
        Generates article comparisons across all the articles in pairs.
        Args:
            articles (list): List of dictionaries of articles with 'title' and 'summary' keys
            gemini_api_key (str): Your Gemini API key

        Returns:
            list: List of dictionaries, each with "Comparison" and "Impact" keys.
        """
        comparison_list = []
        if len(articles) < 2:
            return comparison_list # return empty list if less than 2 articles.

        for i in range(0, len(articles) - 1, 2):
            try:
                ans_dict = self.compare_two_articles(i + 1, articles[i], articles[i + 1], self.api_key)
                comparison_list.append(ans_dict)
            except IndexError: # handle the case where there is an odd number of articles.
                print("Odd number of articles, last one will be ignored")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        return comparison_list
    
    def get_final_sentiment_analysis(self, comparisons):
        """
        Generates a final sentiment analysis based on the impact of all article comparisons.
        
        Args:
            comparisons (list): List of dictionaries, each with "Comparison" and "Impact" keys.
        
        Returns:
            dict: {"Final Sentiment Analysis": "Two-line sentiment analysis"}
        """
        client = genai.Client(api_key=self.api_key)
        
        impacts = [comp["Impact"] for comp in comparisons]
        impacts_str = "\n".join(impacts)

        prompt = f"""Analyze the following impacts from news coverage and provide a final sentiment analysis in two lines:

        {impacts_str}

        Specifically address:
        1. Whether the overall news coverage is positive or negative.
        2. The overall impact on the company's market growth.

        Respond in JSON format:
        {{
            "Final Sentiment Analysis": "Your two-line analysis here"
        }}

        Note: It should strictly avoid any other extra words like "JSON", etc."""

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt],
            )
            response_text = response.text.strip('`json\n').strip('`').strip()
            result = json.loads(response_text)
            return {"Final Sentiment Analysis": " ".join(result["Final Sentiment Analysis"].split())}
        except json.JSONDecodeError as je:
            print(f"JSON Parsing Error: {je}")
            # print(f"Received response: {response.text}")
            return {"Final Sentiment Analysis": "Parsing error"}
        except Exception as e:
            print(f"API Error: {e}")
            return {"Final Sentiment Analysis": "Analysis failed"}
        
    def get_all_analysis(self, articles):
        """
        Generates all comparison analysis and the final sentiment analysis.
        
        Args:
            articles (list): List of dictionaries of articles with 'title' and 'summary' keys.
        
        Returns:
            tuple: (comparison_list, final_sentiment)
        """
        comparison_list = self.get_analysis_across_all(articles)
        final_sentiment = self.get_final_sentiment_analysis(comparison_list)
        return comparison_list, final_sentiment