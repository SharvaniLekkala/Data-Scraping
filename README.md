# Content Scraping and Reliability Assessment System

This system handles the automated collection and evaluation of data from diverse digital platforms. It was designed to pull information from standard blogs, YouTube transcripts, and PubMed research articles, transforming raw web data into structured, actionable JSON. Aside from mere extraction, the pipeline incorporates a trust-assessment engine that scores the reliability of each source based on its origin and content markers.

## Operational Flow

The pipeline executes in three primary phases:

1. **Extraction**: Targeted scripts navigate the specific architecture of each platform. We use standard HTML parsing for blogs, a combination of metadata and transcript APIs for YouTube, and direct XML fetching for PubMed research.
2. **Analysis**: Once recovered, raw text is sent through two utility layers. The first segments long articles into manageable chunks of approximately 100 words. The second maps the text against a broad taxonomy dictionary to assign relevant topic tags automatically.
3. **Evaluation**: Every source is passed through a scoring module. This algorithm generates a normalized 0-1 reliability score by examining the author's credentials, the site's domain authority, and the presence of critical health disclaimers.

## Directory Structure

* scraper/: Source-specific scripts for YouTube, PubMed, and general blogs.
* scoring/: The logic engine for the trust-scoring algorithm.
* utils/: Text processing tools for chunking and topic mapping.
* output/: The storage location for the final consolidated dataset.

## Usage

Ensure all dependencies are available:
pip install -r requirements.txt

Start the orchestration script:
python main.py

The final result will be written to output/scraped_data.json.
