import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
import re

def scrape_youtube(url):
    video_id = url.split("v=")[-1].split("&")[0]
    author = "Unknown Channel"
    date = "2023-01-01"
    title = "YouTube Video"
    description = ""
    
    try:
        ydl_opts = {'quiet': True, 'skip_download': True, 'extract_flat': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        author = info.get('uploader', author)
        dl_date = info.get('upload_date') 
        if dl_date and len(dl_date) == 8:
            date = f"{dl_date[0:4]}-{dl_date[4:6]}-{dl_date[6:8]}"
        description = info.get('description', '')
        title = info.get('title', title)
    except Exception as e:
        print(f"yt-dlp failed, falling back to basic requests: {e}")
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            title_tag = soup.find("meta", property="og:title")
            if title_tag: title = title_tag["content"]
            author_tag = soup.find("link", itemprop="name")
            if author_tag: author = author_tag["content"]
            date_tag = soup.find("meta", itemprop="uploadDate")
            if date_tag: date = date_tag["content"][:10]
        except Exception as e2:
            print(f"Fallback also failed: {e2}")

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t['text'] for t in transcript])
        text = description + "\n" + transcript_text
    except Exception as e:
        print(f"Could not fetch transcript for {url}: {e}")
        text = description + "\nTranscript unavailable."
        
    return {
        "source_url": url,
        "source_type": "youtube",
        "author": author,
        "published_date": date,
        "title": title,
        "text": text,
        "language": "en",
        "region": "global"
    }
