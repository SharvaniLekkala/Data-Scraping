import os
import json
from scraper.blog_scraper import scrape_blog
from scraper.youtube_scraper import scrape_youtube
from scraper.pubmed_scraper import scrape_pubmed
from utils.chunking import chunk_text
from utils.tagging import generate_topic_tags
from scoring.trust_score import calculate_trust_score
from langdetect import detect

URLS = [
    # 3 Blogs 
    "https://news.mit.edu/2023/explained-generative-ai-1109",
    "https://en.wikipedia.org/wiki/Climate_change",
    "https://en.wikipedia.org/wiki/James_Webb_Space_Telescope",
    
    # 2 YouTube 
    "https://www.youtube.com/watch?v=F1Hq8eVOMHs",
    "https://www.youtube.com/watch?v=wY6UyatwVTA",
    
    # 1 PubMed 
    "https://pubmed.ncbi.nlm.nih.gov/30531559/" 
]

def process_url(url):
    print(f"Scraping: {url}")
    if "youtube.com" in url or "youtu.be" in url:
        raw_data = scrape_youtube(url)
    elif "pubmed.ncbi.nlm.nih.gov" in url:
        raw_data = scrape_pubmed(url)
    else:
        raw_data = scrape_blog(url)
        
    if not raw_data:
        print(f"Returned no data for {url}")
        return None
        
    text = raw_data.pop('text', '')
    
    # Auto-detect language
    try:
        raw_data['language'] = detect(text[:1000]) if text else "en"
    except:
        raw_data['language'] = "en"

    raw_data['topic_tags'] = generate_topic_tags(text)
    raw_data['content_chunks'] = chunk_text(text, max_words_per_chunk=100)
    raw_data['trust_score'] = calculate_trust_score(raw_data)
    
    # Enforce strict 9-field schema as per requirements
    schema_fields = [
        "source_url", "source_type", "author", "published_date", 
        "language", "region", "topic_tags", "trust_score", "content_chunks"
    ]
    sanitized_data = {field: raw_data.get(field, "") for field in schema_fields}
    
    return sanitized_data

def main():
    print("Starting scraping pipeline...")
    all_results = []
    count = 0
    for url in URLS:
        try:
            data = process_url(url)
            if data:
                all_results.append(data)
                count += 1
        except Exception as e:
            print(f"Failed to process {url}: {e}")
            
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_file = os.path.join(output_dir, "scraped_data.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully scraped {count} sources. Saved to {output_file}")

if __name__ == "__main__":
    main()
