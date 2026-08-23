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

def load_pmids(filepath: Path) -> list[str]:
    with open(filepath, "r") as f:
        pmids = json.load(f)
    return pmids

def batch_pmids(pmids: list[str], batch_size: int) -> list[list[str]]:
    return [pmids[i:i + batch_size] for i in range(0, len(pmids), batch_size)]

def fetch_annotations(pmids_batch: list[str], base_url: str) -> list[dict]:
    #Joins the batch into a comma-separated string. Calls the PubTator API. Returns the list of raw paper objects from the response. Has try/except with raise_for_status() exactly like pubmed_client did.
    
    pmid_req = ",".join(pmids_batch)

    try:
        response = requests.get(base_url, params={"pmids": pmid_req})
        response.raise_for_status()
        return response.json().get("PubTator3", [])
    except requests.RequestException as e:
        logger.error("PubTator API request failed: %s", e)
        raise

def extract_paper_data(raw_paper: dict) -> dict:
    # Takes one raw paper object from the API response. Loops through the passages list to find the title passage and the abstract passage. From the abstract passage extracts the text and the annotations list. Returns the clean dict structure shown above. This is a pure function — no API calls, no file reading, just data transformation.

    title_passage = next((p for p in raw_paper["passages"] if p["infons"]["type"] == "title"), None)
    abstract_passage = next((p for p in raw_paper["passages"] if p["infons"]["type"] == "abstract"), None)

    if not title_passage or not abstract_passage:
        return {
            "pmid": raw_paper["id"],
            "title": "",
            "abstract": "",
            "annotations": [],
        }

    return {
        "pmid": raw_paper["id"],
        "title": title_passage["text"],
        "abstract": abstract_passage["text"],
        "annotations": abstract_passage.get("annotations", [])
    }

def save_annotations(papers: list[dict], filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(papers, f)



def run_client() -> None:
     # Orchestrates everything:
        # Load PMIDs from disk
        # Split into batches
        # Loop through batches, calling fetch_annotations then extract_paper_data for each paper in each batch
        # Sleep 0.4 seconds between batches
        # Collect all results into one list
        # Save to data/raw/pubtator/annotations.json
    
    data_path = PROJECT_ROOT / "data" / "raw" / "pubmed" / "pmids.json"

    pmids = load_pmids(data_path)

    batch_size = 100

    batches = batch_pmids(pmids, batch_size)

    logger.info("Loaded %d PMIDs, splitting into %d batches", len(pmids), len(batches))

    base_url = get_data_sources()['pubtator']['base_url'] + "publications/export/biocjson"

    annotations = []

    for i, batch in enumerate(batches):
        raw_papers = fetch_annotations(batch, base_url)
        papers = [extract_paper_data(raw_paper) for raw_paper in raw_papers]
        annotations.extend(papers)
        time.sleep(0.4)
        logger.info("Batch %d/%d done. Total papers collected: %d", i+1, len(batches), len(annotations))

    save_annotations(annotations, PROJECT_ROOT / "data" / "raw" / "pubtator" / "annotations.json")
    logger.info("Saved %d annotated papers to disk", len(annotations))

if __name__ == "__main__":
    run_client()