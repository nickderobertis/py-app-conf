"""
Generate test data for file output
"""
from tests.config import INPUT_DATA_DIR, DATA_NAME, JSON_PATH, YAML_PATH, TOML_PATH
from tests.fixtures.model import get_model_object

if __name__ == "__main__":
    conf = get_model_object()
    json_str = conf.json(indent=2)
    JSON_PATH.write_text(json_str)
    conf.yaml(out_path=YAML_PATH)
    conf.toml(out_path=TOML_PATH)
