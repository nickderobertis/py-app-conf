from enum import Enum
from pathlib import Path
from typing import Any, Sequence

import black
from pydantic import BaseModel
from pydantic.fields import ModelField


def pydantic_model_to_python_config_file(
    model: BaseModel, imports: Sequence[str]
) -> str:
    """
    Generate a python config file from a pydantic model.

    :param model: The pydantic model.
    :return: The python config file.
    """
    unformatted = _pydantic_model_to_python_config_file(model, imports)
    # Format the python config file with black.
    formatted = _format_python_config_file(unformatted)
    return formatted


def _format_python_config_file(unformatted: str) -> str:
    """
    Format a python config file.

    :param unformatted: The python config file.
    :return: The formatted python config file.
    """
    return black.format_str(unformatted, mode=black.FileMode(line_length=80))


def _pydantic_model_to_python_config_file(
    model: BaseModel, imports: Sequence[str]
) -> str:
    """
    Generate a python config file from a pydantic model.

    :param model: The pydantic model.
    :return: The python config file.
    """
    imports_str = "\n".join(imports)
    name = model.__class__.__name__
    return (
        f"""
{imports_str}

config = {name}({_build_attributes(model)})
""".strip()
        + "\n"
    )


def _build_attributes(model: BaseModel) -> str:
    """
    Build the attribute definition of a pydantic model.

    :param model: The pydantic model.
    :return: The attributes of the model.
    """
    attributes = ""
    for field_name, field in model.__fields__.items():
        field: ModelField
        value = getattr(model, field_name)
        attributes += f"    {field_name} = {_build_attribute_value(value)},\n"
    return attributes


def _build_attribute_value(value: Any) -> str:
    """
    Build the attribute value of a pydantic model.

    :param value: The value of the attribute.
    :return: The value of the attribute.
    """
    if isinstance(value, (str, Path)):
        return f'"{value}"'
    elif isinstance(value, Enum):
        return f'"{value.value}"'
    elif isinstance(value, BaseModel):
        return repr(value)
    elif isinstance(value, list):
        return f"[{', '.join(_build_attribute_value(v) for v in value)}]"
    elif isinstance(value, tuple):
        return f"({', '.join(_build_attribute_value(v) for v in value)})"
    elif isinstance(value, dict):
        return f"{{{', '.join(f'{_build_attribute_value(k)}: {_build_attribute_value(v)}' for k, v in value.items())}}}"
    else:
        return str(value)
