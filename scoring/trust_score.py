import math
from datetime import datetime
import re

def parse_date(date_str):
    if not date_str:
        return None
    try:
        from dateutil.parser import parse
        return parse(date_str, fuzzy=True)
    except:
        return None

def calculate_trust_score(item_data):
    """
    Trust Score = f(author_credibility, citation_count, domain_authority, recency, medical_disclaimer_presence)
    Returns: float between 0.0 and 1.0
    """
    score = 0.0
    
    # 1. Author Credibility (0.0 to 1.0)
    author = item_data.get('author', '')
    fake_authors = ['admin', 'user', 'guest', 'author', 'editorial team']
    author_credibility = 0.5 
    if author and author.lower() not in fake_authors:
        if len(author.split(', ')) > 1 or "organization" in author.lower() or "institute" in author.lower() or "inc" in author.lower():
            author_credibility = 0.9
        else:
            author_credibility = 0.8
    elif not author:
        author_credibility = 0.2
    else:
        author_credibility = 0.1
        
    # 2. Domain Authority (0.0 to 1.0)
    url = item_data.get('source_url', '')
    domain_authority = 0.5
    if '.gov' in url or '.edu' in url or 'nih.gov' in url:
        domain_authority = 1.0
    elif 'youtube.com' in url or 'youtu.be' in url:
        domain_authority = 0.7
    elif '.org' in url:
        domain_authority = 0.8
    elif url: 
        domain_authority = 0.5
    else:
        domain_authority = 0.1
        
    if 'seo' in url.lower() or 'cheap' in url.lower():
        domain_authority *= 0.2
        
    # 3. Citation Count (defaulting to 0 for non-academic)
    citations = item_data.get('citation_count', 0)
    if citations is None: citations = 0
    citation_score = min(1.0, math.log1p(citations) / math.log1p(100))
    if item_data.get('source_type') != 'pubmed':
        citation_score = 0.5
        
    # 4. Recency
    published_date_str = item_data.get('published_date', '')
    parsed_date = parse_date(published_date_str)
    recency = 0.5
    if parsed_date:
        parsed_date = parsed_date.replace(tzinfo=None)
        age_days = (datetime.now() - parsed_date).days
        if age_days < 0: age_days = 0
        recency = max(0.1, 1.0 - (age_days / 3650.0))
        
    # 5. Medical Disclaimer Presence
    content_text = " ".join(item_data.get('content_chunks', []))
    disclaimer_keywords = ['not medical advice', 'consult your physician', 'medical disclaimer', 'informational purposes only']
    has_disclaimer = any(keyword in content_text.lower() for keyword in disclaimer_keywords)
    
    is_healthcare = 'healthcare' in item_data.get('topic_tags', []) or 'health' in item_data.get('topic_tags', [])
    medical_disclaimer_presence = 0.5
    
    if has_disclaimer:
        medical_disclaimer_presence = 1.0
    elif is_healthcare and item_data.get('source_type') != 'pubmed':
        medical_disclaimer_presence = 0.1

    weights = {
        'author_credibility': 0.25,
        'domain_authority': 0.25,
        'citation_count': 0.15,
        'recency': 0.15,
        'medical_disclaimer_presence': 0.20
    }
    
    final_score = (
        author_credibility * weights['author_credibility'] +
        domain_authority * weights['domain_authority'] +
        citation_score * weights['citation_count'] +
        recency * weights['recency'] +
        medical_disclaimer_presence * weights['medical_disclaimer_presence']
    )
    
    return round(final_score, 2)
