from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple, Type

import pytest
from pydantic import BaseModel, Field

from pyappconf.model import AppConfig, BaseConfig, ConfigFormats
from tests.config import ENV_PATH, GENERATED_DATA_DIR
from tests.fixtures.pydantic_model import MyModel, SubModel


class MyEnum(str, Enum):
    ONE = "one"
    TWO = "two"


class MyConfig(MyModel, BaseConfig):
    _settings: AppConfig = AppConfig(
        app_name="MyApp",
        py_config_imports=[
            "from tests.fixtures.model import MyConfig, SubModel, MyEnum"
        ],
    )

    class Config:
        env_prefix = "MYAPP_"
        env_file = ENV_PATH


class MyConfigPyFormat(MyConfig):
    _settings = AppConfig(
        app_name="MyApp",
        custom_config_folder=GENERATED_DATA_DIR,
        default_format=ConfigFormats.PY,
        py_config_imports=[
            "from tests.fixtures.model import MyConfigPyFormat, SubModel, MyEnum"
        ],
    )


def get_model_classes() -> Tuple[Type[BaseConfig], Type[BaseModel]]:
    return MyConfig, SubModel


def get_model_class_with_defaults() -> Type[BaseConfig]:
    class MyDefaultConfig(BaseConfig):
        a: str = "a"
        b: int = 2

        _settings: AppConfig = AppConfig(app_name="MyApp")

        class Config:
            env_prefix = "MYAPP_"
            env_file = ENV_PATH

    return MyDefaultConfig


def get_model_object(
    exclude_keys: Optional[Sequence[str]] = None, **kwargs
) -> BaseConfig:
    MyConfig, SubModel = get_model_classes()

    all_kwargs = dict(
        string="a",
        integer=5,
        custom=SubModel(a="b", b=8.5),
        dictionary={"yeah": SubModel(a="c", b=9.6)},
        str_list=["a", "b", "c"],
        int_tuple=(1, 2, 3),
    )
    if exclude_keys is not None:
        all_kwargs = {
            key: value for key, value in all_kwargs.items() if key not in exclude_keys
        }
    all_kwargs.update(kwargs)

    # conf = MyConfig(**{'myapp_' + key: value for key, value in all_kwargs.items()})
    conf = MyConfig(**all_kwargs)
    return conf


def get_model_object_with_defaults() -> BaseConfig:
    MyDefaultConfig = get_model_class_with_defaults()
    return MyDefaultConfig()


@pytest.fixture(scope="session")
def model_classes() -> Tuple[Type[BaseConfig], Type[BaseModel]]:
    return get_model_classes()


@pytest.fixture(scope="session")
def model_class_with_defaults() -> Type[BaseConfig]:
    return get_model_class_with_defaults()


@pytest.fixture(scope="session")
def model_object() -> BaseConfig:
    return get_model_object()


@pytest.fixture(scope="session")
def model_object_with_defaults() -> BaseConfig:
    return get_model_object_with_defaults()
