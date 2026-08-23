# Data

This folder is gitignored and not committed to the repository.

## Generating the data

Run the ingestion scripts in order from the project root:

1. `python src/ingestion/pubmed_client.py`  
   → generates data/raw/pubmed/pmids.json

2. `python src/ingestion/pubtator_client.py`  
   → generates data/raw/pubtator/annotations.json

3. `python src/ingestion/opentargets_client.py`  
   → generates data/raw/opentargets/associations.json

4. `python src/ingestion/clinicaltrials_client.py`  
   → generates data/raw/clinicaltrials/trials.json
