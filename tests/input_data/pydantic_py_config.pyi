import datetime
from pathlib import Path
from typing import Callable, List, Mapping, Optional, Tuple
from uuid import UUID

from pydantic import BaseModel

from tests.fixtures.pydantic_model import (
    MyEnum,
    PythonFormatSpecificModel,
    SubModel,
    default_func,
    required_callable,
)

class PythonFormatSpecificModel(BaseModel):
    string: str = "a"
    integer: int = 5
    custom: SubModel = SubModel(a="b", b=8.5)
    dictionary: Mapping[str, SubModel] = {"yeah": SubModel(a="c", b=9.6)}
    str_list: List[str] = ["a", "b", "c"]
    int_tuple: Tuple[int, ...] = (1, 2, 3)
    uuid: UUID = UUID("826032aa-465a-4692-b9b4-c81819197ed0")
    date: date = datetime.date(2020, 1, 1)
    time: datetime = datetime.datetime(2020, 1, 1, 12, 0)
    optional_required_string: Optional[str] = "optional_required_string"
    default_string: str = "woo"
    default_custom: SubModel = SubModel(a="yeah", b=5.6)
    default_enum: MyEnum = MyEnum.ONE
    default_enum_list: List[MyEnum] = [MyEnum.ONE, MyEnum.TWO]
    default_uuid_list: List[UUID] = [
        UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
    ]
    default_time_with_tz: datetime = datetime.datetime(
        2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc
    )
    default_time_list: List[datetime] = [
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
    ]
    default_date_list: List[date] = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
    ]
    file_path: Path = Path("/a/b.txt")
    default_optional_string: Optional[str] = "default_optional_string"
    func: Callable[[], str] = required_callable
    optional_func: Callable[[], str] = default_func

config: PythonFormatSpecificModel
