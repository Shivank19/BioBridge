import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

def load_config(filename):
    try:
        with open(PROJECT_ROOT / "configs" /filename) as f:
            content = yaml.safe_load(f)
            if not isinstance(content, dict):
                raise ValueError(f"{filename} is empty or not a valid YAML dictionary")
            return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {filename}")
    except yaml.YAMLError as e:
        raise ValueError(f"Could not parse {filename}: {e}")
    

def get_disease_scope():
    return load_config("disease_scope.yaml")
    

def get_data_sources():
    return load_config("data_sources.yaml")

def get_graph_schema():
    return load_config("graph_schema.yaml")

def get_ranking_config():
    return load_config("ranking.yaml")