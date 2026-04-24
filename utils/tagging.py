import re

TOPIC_KEYWORDS = {
    "AI": ["ai", "artificial intelligence", "machine learning", "deep learning", "neural network", "generative ai", "llm"],
    "data scraping": ["scraping", "crawler", "extraction", "data mining", "beautifulsoup", "spider"],
    "technology": ["tech", "software", "hardware", "internet", "web", "gadget", "cybersecurity", "blockchain"],
    "healthcare": ["health", "medicine", "healthcare", "medical", "patient", "clinical", "hospital", "disease", "treatment"],
    "genetics": ["crispr", "gene", "dna", "rna", "genome", "mutation", "genetic", "biotech"],
    "science": ["research", "study", "scientist", "analysis", "laboratory", "experiment"],
    "space & astronomy": ["space", "astronomy", "telescope", "nasa", "galaxy", "universe", "planet", "orbit", "apollo", "astronaut"],
    "physics & math": ["physics", "quantum", "mathematics", "calculus", "equations", "relativity", "algebra"],
    "environment": ["climate change", "global warming", "environment", "sustainability", "carbon", "pollution", "ecology", "weather"],
    "sports": ["badminton", "shuttlecock", "racket", "olympics", "tournament", "player", "court", "sport", "football", "basketball"],
    "nutrition": ["diet", "nutrition", "calories", "food", "metabolism", "fasting", "protein", "vitamins", "mediterranean"],
    "history": ["history", "ancient", "war", "century", "historical", "civilization", "empire"],
    "finance": ["finance", "economy", "money", "investing", "stocks", "wall street", "banking", "currency", "inflation"]
}

def generate_topic_tags(text):
    if not text:
        return []
    
    text_lower = text.lower()
    tags = set()
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                tags.add(topic)
                break
                
    return list(tags)
