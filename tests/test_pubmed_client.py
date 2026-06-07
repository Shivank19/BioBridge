"""
test_pubmed_client.py

Tests for the PubMed ingestion client.
Uses mocking to avoid making real API calls during testing.
Mocking means we replace the actual requests.get call with a
fake that returns a controlled response we define ourselves.
This makes tests fast, reliable, and free of network dependency.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from ingestion.pubmed_client import fetch_pmids, save_pmids


# ── SECTION 1: fetch_pmids ────────────────────────────────────────────────────
# unittest.mock.patch temporarily replaces a real function with a fake.
# @patch("ingestion.pubmed_client.requests.get") means:
# "inside pubmed_client.py, replace requests.get with a MagicMock."
# The mock is passed into the test as the first argument (mock_get).

def test_fetch_pmids_returns_list(tmp_path):
    """
    Tests that fetch_pmids returns a list of strings when the
    API responds successfully.
    """
    # Build a fake response object that looks like what requests.get returns
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "esearchresult": {
            "count": "2",
            "idlist": ["12345678", "87654321"]
        }
    }
    # raise_for_status should do nothing (no error)
    mock_response.raise_for_status.return_value = None

    with patch("ingestion.pubmed_client.requests.get", return_value=mock_response):
        result = fetch_pmids(
            query="celiac disease",
            max_results=10,
            email="test@test.com",
            base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/",
            tool="test_tool"
        )

    assert isinstance(result, list), "fetch_pmids should return a list"
    assert result == ["12345678", "87654321"], "fetch_pmids returned wrong PMIDs"


def test_fetch_pmids_returns_empty_list_when_no_results():
    """
    Tests that fetch_pmids handles zero results gracefully
    rather than crashing.
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "esearchresult": {
            "count": "0",
            "idlist": []
        }
    }
    mock_response.raise_for_status.return_value = None

    with patch("ingestion.pubmed_client.requests.get", return_value=mock_response):
        result = fetch_pmids(
            query="zzznotarealquery",
            max_results=10,
            email="test@test.com",
            base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/",
            tool="test_tool"
        )

    assert result == [], "fetch_pmids should return empty list when no results"


def test_fetch_pmids_raises_on_api_failure():
    """
    Tests that fetch_pmids raises an exception when the API
    call fails, rather than silently returning bad data.
    """
    import requests as req

    mock_response = MagicMock()
    # raise_for_status raises HTTPError on 4xx/5xx responses
    mock_response.raise_for_status.side_effect = req.HTTPError("404 Not Found")

    with patch("ingestion.pubmed_client.requests.get", return_value=mock_response):
        with pytest.raises(req.HTTPError):
            fetch_pmids(
                query="celiac disease",
                max_results=10,
                email="test@test.com",
                base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/",
                tool="test_tool"
            )


# ── SECTION 2: save_pmids ─────────────────────────────────────────────────────
# tmp_path is a pytest built-in fixture.
# It gives you a temporary directory that is automatically
# created before the test and deleted after. Perfect for
# testing file writing without touching your real data folder.

def test_save_pmids_creates_file(tmp_path):
    """
    Tests that save_pmids creates a JSON file at the given path.
    """
    pmids = ["12345678", "87654321", "11111111"]
    filepath = tmp_path / "pubmed" / "pmids.json"

    save_pmids(pmids, filepath)

    assert filepath.exists(), "save_pmids should create the file"


def test_save_pmids_creates_parent_directories(tmp_path):
    """
    Tests that save_pmids creates intermediate directories
    if they do not exist yet.
    """
    pmids = ["12345678"]
    # deeply nested path that does not exist
    filepath = tmp_path / "a" / "b" / "c" / "pmids.json"

    save_pmids(pmids, filepath)

    assert filepath.exists(), (
        "save_pmids should create all parent directories automatically"
    )


def test_save_pmids_content_is_valid_json(tmp_path):
    """
    Tests that the file written by save_pmids contains valid
    JSON and that the content matches what was passed in.
    """
    pmids = ["12345678", "87654321"]
    filepath = tmp_path / "pmids.json"

    save_pmids(pmids, filepath)

    with open(filepath, "r") as f:
        loaded = json.load(f)

    assert loaded == pmids, (
        "Content of saved JSON file does not match original PMID list"
    )


def test_save_pmids_handles_empty_list(tmp_path):
    """
    Tests that save_pmids handles an empty list without crashing.
    An empty result is valid — it just means no PMIDs were found.
    """
    filepath = tmp_path / "pmids.json"
    save_pmids([], filepath)

    with open(filepath, "r") as f:
        loaded = json.load(f)

    assert loaded == [], "save_pmids should save an empty list as valid JSON"