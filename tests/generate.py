"""
Generate test data for file output
"""
from pyappconf import AppConfig
from tests.config import (
    DATA_NAME,
    INPUT_DATA_DIR,
    JSON_PATH,
    JSON_WITH_SCHEMA_PATH,
    PY_CONFIG_PATH,
    RECURSIVE_CONFIG_1_PATH,
    RECURSIVE_CONFIG_ROOT_PATH,
    TOML_PATH,
    YAML_PATH,
    YAML_WITH_SCHEMA_PATH,
)
from tests.fixtures.model import get_model_object


def generate_basic_configs():
    conf = get_model_object()
    conf.to_json(out_path=JSON_PATH, json_kwargs=dict(indent=2))
    conf.to_yaml(out_path=YAML_PATH)
    conf.to_toml(out_path=TOML_PATH)
    conf.to_py_config(out_path=PY_CONFIG_PATH)


def generate_configs_with_schema():
    settings_with_schema = AppConfig(
        app_name="MyApp", schema_url="https://example.com/schema.json"
    )
    conf_with_schema = get_model_object(settings=settings_with_schema)
    conf_with_schema.to_json(out_path=JSON_WITH_SCHEMA_PATH, json_kwargs=dict(indent=2))
    conf_with_schema.to_yaml(out_path=YAML_WITH_SCHEMA_PATH)


def generate_recursive_configs():
    config_1 = get_model_object(string="loaded from 1")
    config_1.to_toml(RECURSIVE_CONFIG_1_PATH)
    config_recursive = get_model_object(string="loaded from recursive")
    config_recursive.to_toml(RECURSIVE_CONFIG_ROOT_PATH)


if __name__ == "__main__":
    generate_basic_configs()
    generate_configs_with_schema()
    generate_recursive_configs()
