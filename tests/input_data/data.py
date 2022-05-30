import datetime
from pathlib import Path
from uuid import UUID

from tests.fixtures.model import MyConfig, MyEnum, SubModel

config = MyConfig(
    string="a",
    integer=5,
    custom=SubModel(a="b", b=8.5),
    dictionary={"yeah": SubModel(a="c", b=9.6)},
    str_list=["a", "b", "c"],
    int_tuple=(1, 2, 3),
    uuid=UUID("826032aa-465a-4692-b9b4-c81819197ed0"),
    date=datetime.date(2020, 1, 1),
    time=datetime.datetime(2020, 1, 1, 12, 0),
    default_string="woo",
    default_custom=SubModel(a="yeah", b=5.6),
    default_enum=MyEnum.ONE,
    default_enum_list=[MyEnum.ONE, MyEnum.TWO],
    default_uuid_list=[
        UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
    ],
    default_time_with_tz=datetime.datetime(
        2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc
    ),
    default_time_list=[
        datetime.datetime(
            2022,
            1,
            1,
            0,
            0,
            tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=60)),
        ),
        datetime.datetime(
            2022,
            1,
            2,
            0,
            0,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=86340)),
        ),
    ],
    default_date_list=[datetime.date(2022, 1, 1), datetime.date(2022, 1, 2)],
    file_path=Path("/a/b.txt"),
)
