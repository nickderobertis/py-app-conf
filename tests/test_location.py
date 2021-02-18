from pathlib import Path
from unittest.mock import patch

from pyappconf.model import BaseConfig
from tests.fixtures.model import model_object


@patch('sys.platform', 'linux')
def test_config_location_linux(model_object: BaseConfig):
    assert model_object._settings.config_location == Path('~').expanduser() / '.config' / 'MyApp' / 'config'

