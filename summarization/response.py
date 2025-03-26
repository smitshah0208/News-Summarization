import requests
from bs4 import BeautifulSoup

class NYTimesScraper:
    def __init__(self, company_name):
        """
        Initializes the NYTimesScraper with the company name to search for.

        Args:
            company_name (str): The name of the company to search for.
        """
        self.company_name = company_name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

    def fetch_nytimes_search_results(self):
        """
        Fetches search results from the New York Times website for the given company name.

        Returns:
            requests.Response: The HTTP response from the NYTimes search URL.
        """
        # Construct the search URL
        search_url = f"https://www.nytimes.com/search?dropmab=false&lang=en&query={self.company_name}&sections=Business%7Cnyt%3A%2F%2Fsection%2F0415b2b0-513a-5e78-80da-21ab770cb753&sort=best&types=article"

        try:
            # Make the HTTP GET request
            response = requests.get(search_url, headers=self.headers, timeout=15)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching search results: {e}")
            return None

    def extract_article_info(self, url_response):
        """
        Extracts all the relevant information about the articles from the URL response.

        Args:
            url_response (requests.Response): The HTTP response from the NYTimes search URL.

        Returns:
            list: A list of dictionaries containing article information.
        """
        articles = []
        soup = BeautifulSoup(url_response.text, "html.parser")

        # Find all <a> tags that contain article information
        for a_tag in soup.find_all("a", href=True):
            try:
                # Extract the link
                link = a_tag["href"]

                # Extract the title
                title_tag = a_tag.find("h4", class_="css-nsjm9t")
                title = title_tag.get_text(strip=True) if title_tag else None

                # Only proceed if the title is available (assume it's an article)
                if title:
                    # Extract summary
                    summary_tag = a_tag.find("p", class_="css-e5tzus")
                    summary = summary_tag.get_text(strip=True) if summary_tag else None

                    # Extract source
                    source_tag = a_tag.find("span", class_="css-chk81a")
                    source = source_tag.get_text(strip=True) if source_tag else None

                    # Extract author
                    author_tag = a_tag.find("p", class_="css-1engk30")
                    author = author_tag.get_text(strip=True) if author_tag else None

                    # Extract and format timestamp
                    timestamp_span = a_tag.find("span", class_="css-1t2tqhf")
                    timestamp = None
                    if timestamp_span and timestamp_span.next_sibling:
                        timestamp = timestamp_span.next_sibling.strip()
                        if timestamp:
                            timestamp = ", ".join(timestamp.split(",")[:2])  # Format timestamp

                    # Add article info to the list
                    articles.append({
                        'link': link,
                        'title': title,
                        'source': source,
                        'author': author,
                        'timestamp': timestamp,
                        'summary': summary
                    })
            except Exception as e:
                print(f"Error processing an article: {e}")

        return articles

    def get_articles(self):
        """
        Fetches search results and extracts article information.

        Returns:
            list: A list of dictionaries containing article information.
        """
        # Fetch search results
        search_response = self.fetch_nytimes_search_results()
        if search_response:
            # Extract article information
            articles = self.extract_article_info(search_response)
            return articles
        else:
            print("Failed to fetch search results.")
            return []

