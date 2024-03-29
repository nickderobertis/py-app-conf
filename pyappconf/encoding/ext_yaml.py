from enum import Enum
from pathlib import Path, PosixPath
from uuid import UUID

from yaml.emitter import Emitter
from yaml.representer import SafeRepresenter
from yaml.resolver import Resolver
from yaml.serializer import Serializer

from pyappconf.encoding.general import HasStr


def _represent_hasstr(obj, value: HasStr):
    from yaml.representer import SafeRepresenter

    return SafeRepresenter.represent_str(obj, str(value))


def _represent_enum(obj, value: Enum):
    from yaml.representer import SafeRepresenter

    return SafeRepresenter.represent_str(obj, value.value)


def _represent_uuid(obj, value: UUID):
    from yaml.representer import SafeRepresenter

    return SafeRepresenter.represent_str(obj, str(value))


class CustomRepresenter(SafeRepresenter):
    pass


CustomRepresenter.add_representer(Path, _represent_hasstr)
CustomRepresenter.add_representer(PosixPath, _represent_hasstr)
CustomRepresenter.add_multi_representer(Enum, _represent_enum)
CustomRepresenter.add_multi_representer(UUID, _represent_uuid)


class CustomDumper(Emitter, Serializer, CustomRepresenter, Resolver):
    def __init__(
        self,
        stream,
        default_style=None,
        default_flow_style=False,
        canonical=None,
        indent=None,
        width=None,
        allow_unicode=None,
        line_break=None,
        encoding=None,
        explicit_start=None,
        explicit_end=None,
        version=None,
        tags=None,
        sort_keys=True,
    ):
        Emitter.__init__(
            self,
            stream,
            canonical=canonical,
            indent=indent,
            width=width,
            allow_unicode=allow_unicode,
            line_break=line_break,
        )
        Serializer.__init__(
            self,
            encoding=encoding,
            explicit_start=explicit_start,
            explicit_end=explicit_end,
            version=version,
            tags=tags,
        )
        CustomRepresenter.__init__(
            self,
            default_style=default_style,
            default_flow_style=default_flow_style,
            sort_keys=sort_keys,
        )
        Resolver.__init__(self)
