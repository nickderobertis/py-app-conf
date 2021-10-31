from pathlib import Path

TEST_DIR = Path(__file__).parent
INPUT_DATA_DIR = TEST_DIR / 'input_data'
GENERATED_DATA_DIR = TEST_DIR / 'generated_data'

DATA_NAME = 'data'
JSON_PATH = INPUT_DATA_DIR / (DATA_NAME + '.json')
YAML_PATH = INPUT_DATA_DIR / (DATA_NAME + '.yaml')
TOML_PATH = INPUT_DATA_DIR / (DATA_NAME + '.toml')
NON_EXISTENT_NAME = 'woo'
NON_EXISTENT_IN_PATH = INPUT_DATA_DIR / NON_EXISTENT_NAME
NON_EXISTENT_INPUT_JSON_PATH = INPUT_DATA_DIR / (NON_EXISTENT_NAME + '.json')
CUSTOM_CONFIG_IN_PATH = INPUT_DATA_DIR / DATA_NAME
ENV_PATH = GENERATED_DATA_DIR / '.env'
RECURSIVE_INPUT_FOLDER = INPUT_DATA_DIR / "recursive"

if not INPUT_DATA_DIR.exists():
    INPUT_DATA_DIR.mkdir()
if not GENERATED_DATA_DIR.exists():
    GENERATED_DATA_DIR.mkdir()