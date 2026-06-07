import yaml
from pathlib import Path

# This gets the project root by going up two levels from this
# test file: tests/test_project_structure.py -> tests/ -> project root
PROJECT_ROOT = Path(__file__).parent.parent

# ── TEST 1: Config files exist ────────────────────────────────

def test_config_files_exist():
    """
    Checks that all four config YAML files are present.
    If any is missing, the test fails and tells you which one.
    """
    expected_configs = [
        "configs/disease_scope.yaml",
        "configs/data_sources.yaml",
        "configs/graph_schema.yaml",
        "configs/ranking.yaml",
    ]

    for config_path in expected_configs:
        full_path = PROJECT_ROOT / config_path
        assert full_path.exists(), (
            f"Missing config file: {config_path}. "
            f"Expected it at {full_path}"
        )

# ── TEST 2: Config files are valid YAML and not empty ────────

def test_config_files_are_valid_yaml():
    """
    Opens each config file and parses it.
    Fails if the YAML syntax is broken or the file is empty.
    """
    config_files = [
        "configs/disease_scope.yaml",
        "configs/data_sources.yaml",
        "configs/graph_schema.yaml",
        "configs/ranking.yaml",
    ]

    for config_path in config_files:
        full_path = PROJECT_ROOT / config_path
        with open(full_path, "r") as f:
            content = yaml.safe_load(f)

        assert content is not None, (
            f"{config_path} is empty. It must contain valid YAML."
        )
        assert isinstance(content, dict), (
            f"{config_path} did not parse into a dictionary. "
            f"Check the YAML structure."
        )

# ── TEST 3: Required keys exist in each config ────────────────

def test_disease_scope_has_required_keys():
    """
    Checks that disease_scope.yaml has the keys the system
    depends on. If a key is missing, downstream code will fail
    with a confusing KeyError. Better to catch it here.
    """
    full_path = PROJECT_ROOT / "configs/disease_scope.yaml"
    with open(full_path, "r") as f:
        config = yaml.safe_load(f)

    required_keys = ["primary_disease", "sanity_check_candidates"]
    for key in required_keys:
        assert key in config, (
            f"disease_scope.yaml is missing required key: '{key}'"
        )

def test_data_sources_has_required_keys():
    """
    Checks that data_sources.yaml defines all four sources
    the ingestion layer will try to use.
    """
    full_path = PROJECT_ROOT / "configs/data_sources.yaml"
    with open(full_path, "r") as f:
        config = yaml.safe_load(f)

    required_keys = ["pubmed", "open_targets", "pubtator", "clinicaltrials"]
    for key in required_keys:
        assert key in config, (
            f"data_sources.yaml is missing required key: '{key}'"
        )

def test_graph_schema_has_required_keys():
    """
    Checks that graph_schema.yaml defines node types, edge types,
    and provenance fields. These are what graph_schema.py will
    be built from, so they must all be present.
    """
    full_path = PROJECT_ROOT / "configs/graph_schema.yaml"
    with open(full_path, "r") as f:
        config = yaml.safe_load(f)

    required_keys = ["node_types", "edge_types", "edge_provenance_fields"]
    for key in required_keys:
        assert key in config, (
            f"graph_schema.yaml is missing required key: '{key}'"
        )

def test_ranking_has_required_keys():
    """
    Checks that ranking.yaml defines a version, active scorers,
    and a top_k value. The ranking layer reads all three at startup.
    """
    full_path = PROJECT_ROOT / "configs/ranking.yaml"
    with open(full_path, "r") as f:
        config = yaml.safe_load(f)

    required_keys = ["version", "active_scorers", "top_k_candidates"]
    for key in required_keys:
        assert key in config, (
            f"ranking.yaml is missing required key: '{key}'"
        )

# ── TEST 4: Core folder structure exists ─────────────────────

def test_core_folders_exist():
    """
    Checks that the key source folders exist.
    If someone clones the repo and a folder is missing,
    imports will fail with confusing errors. This catches it early.
    """
    expected_folders = [
        "src/ingestion",
        "src/preprocessing",
        "src/entity_extraction",
        "src/normalization",
        "src/graph",
        "src/ranking",
        "src/explanations",
        "src/evaluation",
        "src/api",
        "src/utils",
        "src/ml/embeddings",
        "src/ml/gnn",
        "data/raw",
        "data/interim",
        "data/processed",
        "data/sample",
        "app",
        "scripts",
        "notebooks",
        "models",
        "reports",
        "docs/adr",
        "tests",
    ]

    for folder_path in expected_folders:
        full_path = PROJECT_ROOT / folder_path
        assert full_path.is_dir(), (
            f"Missing expected folder: {folder_path}. "
            f"Create it with a .gitkeep file inside."
        )