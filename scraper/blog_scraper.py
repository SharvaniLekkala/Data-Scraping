import requests
from bs4 import BeautifulSoup
import re

def scrape_blog(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else ""
        
        date_meta = soup.find('meta', {'property': 'article:published_time'})
        date = date_meta['content'] if date_meta else ""
        if not date:
            # Fallback for date
            date_meta2 = soup.find('meta', {'name': 'pubdate'})
            date = date_meta2['content'] if date_meta2 else "2023-01-01" # Mock if missing
            
        author_meta = soup.find('meta', {'name': 'author'})
        author = author_meta['content'] if author_meta else ""
        if not author:
            # Try to find a rel="author" link
            a_tag = soup.find('a', rel="author")
            author = a_tag.get_text() if a_tag else "Editorial Team"
            
        for unwanted in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            unwanted.decompose()
            
        paragraphs = soup.find_all('p')
        text = "\n".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 20])
        
        return {
            "source_url": url,
            "source_type": "blog",
            "author": author,
            "published_date": date,
            "title": title,
            "text": text,
            "language": "en", 
            "region": "global"
        }
    except Exception as e:
        print(f"Error scraping blog {url}: {e}")
        return None
