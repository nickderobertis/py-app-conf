from pyappconf.py_config.generate import pydantic_model_to_python_config_file
from tests.config import PYDANTIC_PY_CONFIG_PATH
from tests.fixtures.pydantic_model import (
    PYTHON_FORMAT_IMPORT,
    MyModel,
    python_format_specific_model_object,
)


def test_pydantic_model_to_config_file(python_format_specific_model_object: MyModel):
    config_str = pydantic_model_to_python_config_file(
        python_format_specific_model_object,
        [PYTHON_FORMAT_IMPORT],
    )
    assert config_str == PYDANTIC_PY_CONFIG_PATH.read_text()
