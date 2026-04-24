import requests
import xml.etree.ElementTree as ET

def scrape_pubmed(url):
    try:
        if 'pubmed.ncbi.nlm.nih.gov' not in url:
            return None
            
        pmid = [part for part in url.split('/') if part.isdigit()]
        if not pmid:
            return None
        pmid = pmid[0]
        
        api_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        article = root.find('.//Article')
        
        if article is None:
            return None
            
        title_tag = article.find('.//ArticleTitle')
        title = title_tag.text if title_tag is not None else ""
        
        abstract_tag = article.find('.//AbstractText')
        text = abstract_tag.text if abstract_tag is not None else ""
        
        authors = []
        author_list = article.find('.//AuthorList')
        if author_list is not None:
            for author_node in author_list.findall('Author'):
                last_name = author_node.find('LastName')
                first_name = author_node.find('ForeName')
                if last_name is not None and first_name is not None:
                    authors.append(f"{first_name.text} {last_name.text}")
        author_str = ", ".join(authors) if authors else "Unknown Authors"
        
        journal_tag = article.find('.//Journal/Title')
        journal = journal_tag.text if journal_tag is not None else "Unknown Journal"

        pub_date = article.find('.//Journal/JournalIssue/PubDate')
        year = pub_date.find('Year').text if pub_date is not None and pub_date.find('Year') is not None else "2020"
        date = f"{year}-01-01" 
            
        return {
            "source_url": url,
            "source_type": "pubmed",
            "author": author_str,
            "published_date": date,
            "journal": journal,
            "title": title,
            "text": text,
            "language": "en",
            "region": "global",
            "citation_count": 45 # mock value
        }
    except Exception as e:
        print(f"Error scraping pubmed {url}: {e}")
        return None
