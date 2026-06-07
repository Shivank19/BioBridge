import os
from pathlib import Path
from dotenv import load_dotenv
import logging
from utils.config import get_data_sources
import json
import requests
import time


PROJECT_ROOT = Path(__file__).parent.parent.parent

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()


def fetch_pmids(query: str, max_results: int, email: str, base_url: str, tool: str) -> list[str]:
    
    try:
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "tool": tool,
            "email": email
        }
        response = requests.get(base_url + "esearch.fcgi", params=params)

        response.raise_for_status()

        response_json = response.json()
        
        pmids = response_json['esearchresult']['idlist']
        logger.info(f"Found {response_json['esearchresult']['count']} results. Fetching PMIDs: {pmids}")

    except requests.RequestException as e:
        logger.error("PubMed API request failed: %s", e)
        raise
       
    return pmids

def save_pmids(pmids: list[str], filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(pmids, f)

def run_client() -> None:
    data_sources = get_data_sources()
    # print(data_sources)
    base_url = data_sources['pubmed']['base_url']
    queries = data_sources['pubmed']['queries']
    max_abstracts = data_sources['pubmed']['max_abstracts']
    email = os.getenv("NCBI_EMAIL")
    if not email:
        raise ValueError(
            "NCBI_EMAIL not set. Add it to your .env file: NCBI_EMAIL=your@email.com"
        )
    tool = os.getenv("NCBI_TOOL", "biobridge")

    disease_query = " OR ".join(queries)

    pmids = fetch_pmids(disease_query, max_abstracts, email, base_url, tool)

    time.sleep(0.5)

    data_path = PROJECT_ROOT / "data" / "raw" / "pubmed" / "pmids.json"

    save_pmids(pmids, data_path)


if __name__ == "__main__":
    run_client()