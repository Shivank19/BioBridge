"""
test_config.py

Tests that config.py correctly loads all four YAML files
and that each returns a dict with the expected top-level keys.

These tests are important because every other module depends
on config.py. A silent failure here would cause confusing
errors deep in the pipeline.
"""

import pytest
from utils.config import (
    load_config,
    get_disease_scope,
    get_data_sources,
    get_graph_schema,
    get_ranking_config
)


# ── SECTION 1: Core loader works ─────────────────────────────────────────────
# Tests the load_config function directly before testing
# the convenience wrappers built on top of it.

def test_load_config_returns_dict():
    # load_config should return a Python dict for any valid YAML file
    result = load_config("disease_scope.yaml")
    assert isinstance(result, dict), (
        "load_config should return a dict but returned "
        f"{type(result).__name__}"
    )

def test_load_config_raises_on_missing_file():
    # pytest.raises is how you test that a function raises an exception.
    # the code inside the `with` block should raise FileNotFoundError.
    # if it does not raise, the test fails.
    with pytest.raises(FileNotFoundError):
        load_config("this_file_does_not_exist.yaml")

def test_load_config_raises_on_wrong_filename_type():
    # passing something that clearly does not exist should fail cleanly
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent_config.yaml")


# ── SECTION 2: Convenience functions return dicts ────────────────────────────
# Each convenience function wraps load_config for one specific file.
# These tests prove they all return dicts, not None, not lists.

def test_get_disease_scope_returns_dict():
    result = get_disease_scope()
    assert isinstance(result, dict), (
        "get_disease_scope should return a dict"
    )

def test_get_data_sources_returns_dict():
    result = get_data_sources()
    assert isinstance(result, dict), (
        "get_data_sources should return a dict"
    )

def test_get_graph_schema_returns_dict():
    result = get_graph_schema()
    assert isinstance(result, dict), (
        "get_graph_schema should return a dict"
    )

def test_get_ranking_config_returns_dict():
    result = get_ranking_config()
    assert isinstance(result, dict), (
        "get_ranking_config should return a dict"
    )


# ── SECTION 3: Expected top-level keys exist ─────────────────────────────────
# These tests check that the keys your code will actually use
# exist in the returned dict. If a key is missing, every module
# that depends on it will fail with a confusing KeyError.
# Better to catch it here.

def test_disease_scope_has_expected_keys():
    config = get_disease_scope()
    assert "primary_disease" in config, (
        "disease_scope.yaml missing key: 'primary_disease'"
    )
    assert "sanity_check_candidates" in config, (
        "disease_scope.yaml missing key: 'sanity_check_candidates'"
    )

def test_data_sources_has_expected_keys():
    config = get_data_sources()
    for key in ["pubmed", "open_targets", "pubtator", "clinicaltrials"]:
        assert key in config, (
            f"data_sources.yaml missing key: '{key}'"
        )

def test_graph_schema_has_expected_keys():
    config = get_graph_schema()
    for key in ["node_types", "edge_types", "edge_provenance_fields"]:
        assert key in config, (
            f"graph_schema.yaml missing key: '{key}'"
        )

def test_ranking_config_has_expected_keys():
    config = get_ranking_config()
    for key in ["version", "active_scorers", "top_k_candidates"]:
        assert key in config, (
            f"ranking.yaml missing key: '{key}'"
        )


# ── SECTION 4: Spot-check specific values ────────────────────────────────────
# These tests check that specific values in the config are what
# we expect. They act as a contract — if someone changes the config
# in a way that breaks the system, these tests fail and warn them.

def test_disease_scope_primary_disease_is_celiac():
    config = get_disease_scope()
    disease = config["primary_disease"]
    assert disease["name"] == "Celiac Disease", (
        "primary_disease name should be 'Celiac Disease'"
    )
    assert disease["mondo_id"] == "MONDO:0005130", (
        "primary_disease mondo_id should be 'MONDO:0005130'"
    )

def test_ranking_top_k_is_integer():
    config = get_ranking_config()
    top_k = config["top_k_candidates"]
    assert isinstance(top_k, int), (
        f"top_k_candidates should be an int but is {type(top_k).__name__}"
    )
    assert top_k > 0, (
        "top_k_candidates should be a positive integer"
    )

def test_data_sources_pubmed_has_base_url():
    config = get_data_sources()
    pubmed = config["pubmed"]
    assert "base_url" in pubmed, (
        "pubmed config missing 'base_url'"
    )
    assert pubmed["base_url"].startswith("https://"), (
        "pubmed base_url should start with https://"
    )

def test_sanity_check_candidates_are_present():
    config = get_disease_scope()
    candidates = config["sanity_check_candidates"]
    # extract just the names from the list of candidate dicts
    names = [c["name"] for c in candidates]
    assert "Larazotide" in names, "Larazotide should be a sanity check candidate"
    assert "AMG 714" in names, "AMG 714 should be a sanity check candidate"
    assert "Tofacitinib" in names, "Tofacitinib should be a sanity check candidate"