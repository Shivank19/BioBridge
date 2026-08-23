"""
test_pubtator_client.py

Tests for the PubTator ingestion client.
Uses mocking for API calls and tmp_path for file operations.
extract_paper_data is a pure function so it needs no mocking —
we just pass in controlled input and check the output.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from ingestion.pubtator_client import (
    load_pmids,
    batch_pmids,
    fetch_annotations,
    extract_paper_data,
    save_annotations
)


# ── HELPERS ───────────────────────────────────────────────────────────────────
# A fake raw paper dict that looks exactly like what PubTator returns.
# We define it once here and reuse it across multiple tests rather than
# duplicating the same structure everywhere.

def make_raw_paper(pmid="12345678", include_abstract=True):
    """
    Builds a minimal PubTator-style paper dict for testing.
    Set include_abstract=False to simulate a paper with no abstract passage.
    """
    passages = [
        {
            "infons": {"type": "title"},
            "text": "Role of IL-15 in Celiac Disease",
            "annotations": []
        }
    ]
    if include_abstract:
        passages.append({
            "infons": {"type": "abstract"},
            "text": "Tofacitinib inhibits JAK1 and has been studied in celiac disease.",
            "annotations": [
                {
                    "id": "1",
                    "infons": {
                        "type": "Chemical",
                        "identifier": "MESH:C479163",
                        "name": "Tofacitinib"
                    },
                    "text": "Tofacitinib",
                    "locations": [{"offset": 0, "length": 11}]
                },
                {
                    "id": "2",
                    "infons": {
                        "type": "Gene",
                        "identifier": "3716",
                        "name": "JAK1"
                    },
                    "text": "JAK1",
                    "locations": [{"offset": 20, "length": 4}]
                }
            ]
        })
    return {"id": pmid, "passages": passages}


# ── SECTION 1: load_pmids ─────────────────────────────────────────────────────
# load_pmids reads a JSON file from disk and returns a list.
# We use tmp_path to create a real temporary file — no mocking needed
# because there is no network call, just file IO.

def test_load_pmids_returns_list(tmp_path):
    """
    Tests that load_pmids reads a JSON file and returns the correct list.
    """
    pmids = ["12345678", "87654321", "11111111"]
    filepath = tmp_path / "pmids.json"
    filepath.write_text(json.dumps(pmids))

    result = load_pmids(filepath)

    assert result == pmids, "load_pmids did not return the correct PMID list"


def test_load_pmids_returns_empty_list(tmp_path):
    """
    Tests that load_pmids handles an empty list file without crashing.
    """
    filepath = tmp_path / "pmids.json"
    filepath.write_text(json.dumps([]))

    result = load_pmids(filepath)

    assert result == [], "load_pmids should return empty list for empty file"


def test_load_pmids_raises_on_missing_file(tmp_path):
    """
    Tests that load_pmids raises FileNotFoundError if the file does not exist.
    This matters because if pubmed_client never ran, pubtator_client should
    fail clearly rather than silently producing no output.
    """
    filepath = tmp_path / "does_not_exist.json"

    with pytest.raises(FileNotFoundError):
        load_pmids(filepath)


# ── SECTION 2: batch_pmids ────────────────────────────────────────────────────
# batch_pmids is a pure function — no IO, no network.
# We just check the output shape and content directly.

def test_batch_pmids_even_split():
    """
    300 PMIDs with batch size 100 should produce exactly 3 batches of 100.
    """
    pmids = [str(i) for i in range(300)]
    batches = batch_pmids(pmids, batch_size=100)

    assert len(batches) == 3, "Should produce 3 batches for 300 PMIDs"
    assert all(len(b) == 100 for b in batches), "Each batch should have 100 PMIDs"


def test_batch_pmids_uneven_split():
    """
    250 PMIDs with batch size 100 should produce 3 batches: 100, 100, 50.
    The last batch is smaller — this is expected and must not be dropped.
    """
    pmids = [str(i) for i in range(250)]
    batches = batch_pmids(pmids, batch_size=100)

    assert len(batches) == 3, "Should produce 3 batches for 250 PMIDs"
    assert len(batches[0]) == 100, "First batch should have 100 PMIDs"
    assert len(batches[1]) == 100, "Second batch should have 100 PMIDs"
    assert len(batches[2]) == 50, "Third batch should have 50 PMIDs"


def test_batch_pmids_preserves_all_pmids():
    """
    The total number of PMIDs across all batches must equal the input count.
    Nothing should be lost or duplicated during batching.
    """
    pmids = [str(i) for i in range(275)]
    batches = batch_pmids(pmids, batch_size=100)

    all_pmids = [pmid for batch in batches for pmid in batch]

    assert len(all_pmids) == 275, "Batching should not lose or duplicate PMIDs"
    assert all_pmids == pmids, "Batching should preserve order"


def test_batch_pmids_smaller_than_batch_size():
    """
    If there are fewer PMIDs than the batch size, should return one batch.
    """
    pmids = ["1", "2", "3"]
    batches = batch_pmids(pmids, batch_size=100)

    assert len(batches) == 1, "Should return one batch when PMIDs < batch_size"
    assert batches[0] == pmids, "The single batch should contain all PMIDs"


# ── SECTION 3: fetch_annotations ─────────────────────────────────────────────
# fetch_annotations makes a real HTTP request, so we mock requests.get.
# The mock returns a fake response object with a controlled json() return value.

def test_fetch_annotations_returns_paper_list():
    """
    Tests that fetch_annotations extracts the PubTator3 list from the response
    and returns it. The PubTator3 key is where the papers live in the response.
    """
    fake_paper = make_raw_paper("12345678")
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"PubTator3": [fake_paper]}

    with patch("ingestion.pubtator_client.requests.get", return_value=mock_response):
        result = fetch_annotations(
            pmids_batch=["12345678"],
            base_url="https://fake-pubtator-url.com"
        )

    assert isinstance(result, list), "fetch_annotations should return a list"
    assert len(result) == 1, "Should return one paper for one PMID"
    assert result[0]["id"] == "12345678", "Paper ID should match the requested PMID"


def test_fetch_annotations_returns_empty_list_when_no_results():
    """
    Tests that fetch_annotations returns an empty list when PubTator3 key
    is missing or empty — not a crash.
    """
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}

    with patch("ingestion.pubtator_client.requests.get", return_value=mock_response):
        result = fetch_annotations(
            pmids_batch=["99999999"],
            base_url="https://fake-pubtator-url.com"
        )

    assert result == [], "Should return empty list when PubTator3 key is missing"


def test_fetch_annotations_raises_on_api_failure():
    """
    Tests that fetch_annotations raises when the API returns an error status.
    """
    import requests as req

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = req.HTTPError("500 Server Error")

    with patch("ingestion.pubtator_client.requests.get", return_value=mock_response):
        with pytest.raises(req.HTTPError):
            fetch_annotations(
                pmids_batch=["12345678"],
                base_url="https://fake-pubtator-url.com"
            )


# ── SECTION 4: extract_paper_data ────────────────────────────────────────────
# extract_paper_data is a pure function — no IO, no network, no mocking.
# We pass in controlled dicts and check the output.
# This section tests the most important logic in the file.

def test_extract_paper_data_returns_correct_structure():
    """
    Tests that extract_paper_data returns a dict with all required keys.
    """
    raw = make_raw_paper("12345678", include_abstract=True)
    result = extract_paper_data(raw)

    assert "pmid" in result, "Result should have 'pmid' key"
    assert "title" in result, "Result should have 'title' key"
    assert "abstract" in result, "Result should have 'abstract' key"
    assert "annotations" in result, "Result should have 'annotations' key"


def test_extract_paper_data_correct_values():
    """
    Tests that extract_paper_data extracts the right values from each passage.
    """
    raw = make_raw_paper("12345678", include_abstract=True)
    result = extract_paper_data(raw)

    assert result["pmid"] == "12345678", "PMID should match paper id"
    assert result["title"] == "Role of IL-15 in Celiac Disease", "Title should match title passage"
    assert "Tofacitinib" in result["abstract"], "Abstract should contain expected text"
    assert len(result["annotations"]) == 2, "Should extract 2 annotations from abstract"


def test_extract_paper_data_annotations_have_correct_fields():
    """
    Tests that each annotation in the result has the fields downstream
    code will expect: type, name, identifier, text.
    """
    raw = make_raw_paper("12345678", include_abstract=True)
    result = extract_paper_data(raw)

    for annotation in result["annotations"]:
        assert "infons" in annotation, "Each annotation should have infons"
        infons = annotation["infons"]
        assert "type" in infons, "infons should have type"
        assert "identifier" in infons, "infons should have identifier"
        assert "name" in infons, "infons should have name"


def test_extract_paper_data_fallback_when_no_abstract():
    """
    Tests that extract_paper_data returns a safe fallback dict when the
    abstract passage is missing, rather than crashing with a KeyError.
    This happens for some papers that only have a title in PubTator.
    """
    raw = make_raw_paper("99999999", include_abstract=False)
    result = extract_paper_data(raw)

    # Should not crash — should return safe empty values
    assert result["pmid"] == "99999999", "PMID should still be present in fallback"
    assert result["title"] == "", "Title should be empty string in fallback"
    assert result["abstract"] == "", "Abstract should be empty string in fallback"
    assert result["annotations"] == [], "Annotations should be empty list in fallback"


# ── SECTION 5: save_annotations ──────────────────────────────────────────────

def test_save_annotations_creates_file(tmp_path):
    """
    Tests that save_annotations creates the output file.
    """
    papers = [
        {"pmid": "123", "title": "Test", "abstract": "Test abstract", "annotations": []},
        {"pmid": "456", "title": "Test 2", "abstract": "Test abstract 2", "annotations": []}
    ]
    filepath = tmp_path / "pubtator" / "annotations.json"

    save_annotations(papers, filepath)

    assert filepath.exists(), "save_annotations should create the output file"


def test_save_annotations_content_matches(tmp_path):
    """
    Tests that the saved file content exactly matches what was passed in.
    """
    papers = [
        {"pmid": "123", "title": "Test", "abstract": "Test abstract", "annotations": []},
    ]
    filepath = tmp_path / "annotations.json"

    save_annotations(papers, filepath)

    with open(filepath, "r") as f:
        loaded = json.load(f)

    assert loaded == papers, "Saved content should match original paper list"


def test_save_annotations_creates_parent_directories(tmp_path):
    """
    Tests that save_annotations creates intermediate directories automatically.
    """
    filepath = tmp_path / "a" / "b" / "c" / "annotations.json"

    save_annotations([], filepath)

    assert filepath.exists(), "save_annotations should create all parent directories"