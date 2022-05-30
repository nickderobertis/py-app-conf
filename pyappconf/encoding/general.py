from pyappconf.constants import PY10

if PY10:
    from typing import Protocol
else:
    from typing_extensions import Protocol  # type: ignore


class HasStr(Protocol):
    def __str__(self) -> str:
        ...
