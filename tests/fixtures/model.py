from typing import Type, Dict, List, Tuple

import pytest

from pyappconf.model import BaseConfig


def get_model_classes() -> Tuple[Type[BaseConfig], Type[BaseConfig]]:
    class SubConfig(BaseConfig):
        a: str
        b: float

    class MyConfig(BaseConfig):
        string: str
        integer: int
        custom: SubConfig
        dictionary: Dict[str, SubConfig]
        str_list: List[str]
        int_tuple: Tuple[int, ...]

        default_string: str = "woo"
        default_custom: SubConfig = SubConfig(a="yeah", b=5.6)

    return MyConfig, SubConfig


def get_model_object(**kwargs) -> BaseConfig:
    MyConfig, SubConfig = get_model_classes()
    conf = MyConfig(
        string="a",
        integer=5,
        custom=SubConfig(a="b", b=8.5),
        dictionary={"yeah": SubConfig(a="c", b=9.6)},
        str_list=["a", "b", "c"],
        int_tuple=(1, 2, 3),
    )
    return conf


@pytest.fixture(scope="session")
def model_classes() -> Tuple[Type[BaseConfig], Type[BaseConfig]]:
    return get_model_classes()


@pytest.fixture(scope="session")
def model_object() -> BaseConfig:
    return get_model_object()
