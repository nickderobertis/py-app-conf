import json
from pathlib import Path
from typing import Any
from uuid import UUID


class ExtendedJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (Path, UUID)):
            return str(o)

        return json.JSONEncoder.default(self, o)
