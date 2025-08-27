import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_from_web():
#    extract simple data -> headlines
    try:
        # website
        url = "https://news.ycombinator.com"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())
        
        # Extract headlines (first 5)
        headlines = []
        for item in soup.select('.titleline a')[:5]:
            headlines.append(item.text)
            # print(item.text)
        
        # Create DataFrame
        df = pd.DataFrame({
            'headline': headlines,
            'source': 'Hacker News',
            'scraped_at': pd.Timestamp.now()
        })
        
        print("Successfully extracted data from web")
        return df
        
    except Exception as e:
        print(f"Error extracting web data: {e}")
        return pd.DataFrame({
            'headline': ['Sample Headline 1', 'Sample Headline 2', 'Sample Headline 3'],
            'source': 'Sample Source',
            'scraped_at': pd.Timestamp.now()
        })