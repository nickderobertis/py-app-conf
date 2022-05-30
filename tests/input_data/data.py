from pathlib import Path

from tests.fixtures.model import MyConfig, MyEnum, SubConfig

config = MyConfig(
    string="a",
    integer=5,
    custom=SubConfig(a="b", b=8.5),
    dictionary={"yeah": SubConfig(a="c", b=9.6)},
    str_list=["a", "b", "c"],
    int_tuple=(1, 2, 3),
    default_string="woo",
    default_custom=SubConfig(a="yeah", b=5.6),
    default_enum=MyEnum.ONE,
    default_enum_list=[MyEnum.ONE, MyEnum.TWO],
    file_path=Path("/a/b.txt"),
)
