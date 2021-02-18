from pathlib import Path
from typing import Optional, Union, Dict, Any

from pydantic import BaseSettings, validator, BaseModel
import yaml
import toml
import json
import appdirs


def _output_if_necessary(content: str, out_path: Optional[Union[str, Path]] = None):
    if out_path is not None:
        out_path = Path(out_path)
        out_path.write_text(content)


class AppConfigSettings(BaseModel):
    app_name: str = ""
    app_author: str = ""

    @validator("app_name", "app_author")
    def name_must_be_set(cls, v):
        if not v:
            raise ValueError("must be set")
        return v


class BaseConfig(BaseSettings):
    def yaml(
        self,
        out_path: Optional[Union[str, Path]] = None,
        yaml_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        if yaml_kwargs is None:
            yaml_kwargs = {}
        data = self.dict(**kwargs)
        yaml_str = yaml.safe_dump(data, **yaml_kwargs)
        _output_if_necessary(yaml_str, out_path)
        return yaml_str

    @classmethod
    def parse_yaml(cls, in_path: Union[str, Path]) -> "BaseConfig":
        data = yaml.safe_load(Path(in_path).read_text())
        return cls.parse_obj(data)

    def toml(
        self,
        out_path: Optional[Union[str, Path]] = None,
        toml_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        if toml_kwargs is None:
            toml_kwargs = {}
        data = self.dict(**kwargs)
        toml_str = toml.dumps(data, **toml_kwargs)
        _output_if_necessary(toml_str, out_path)
        return toml_str

    @classmethod
    def parse_toml(cls, in_path: Union[str, Path]) -> "BaseConfig":
        data = toml.load(in_path)
        return cls.parse_obj(data)

    @classmethod
    def parse_json(cls, in_path: Union[str, Path]) -> "BaseConfig":
        data = json.loads(Path(in_path).read_text())
        return cls.parse_obj(data)