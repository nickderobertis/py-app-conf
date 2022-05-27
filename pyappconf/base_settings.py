# Vendor Pydantic BaseSettings, changing only that it does not have BaseModel as a base,
# instead it is a pydantic dataclass.
import warnings
from pathlib import Path
from typing import Union, Optional, Any, Dict, AbstractSet, List, Tuple

import pydantic
from pydantic import Extra
from pydantic.env_settings import env_file_sentinel, InitSettingsSource, EnvSettingsSource, SecretsSettingsSource, \
    SettingsSourceCallable
from pydantic.fields import ModelField
from pydantic.typing import display_as_type
from pydantic.utils import deep_update, sequence_like


@pydantic.dataclasses.dataclass
class BaseSettings:
    """
    Base class for settings, allowing values to be overridden by environment variables.

    This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
    Heroku and any 12 factor app design.
    """

    def __init__(
        __pydantic_self__,
        _env_file: Union[Path, str, None] = env_file_sentinel,
        _env_file_encoding: Optional[str] = None,
        _secrets_dir: Union[Path, str, None] = None,
        **values: Any,
    ) -> None:
        # Uses something other than `self` the first arg to allow "self" as a settable attribute
        super().__init__(
            **__pydantic_self__._build_values(
                values, _env_file=_env_file, _env_file_encoding=_env_file_encoding, _secrets_dir=_secrets_dir
            )
        )

    def _build_values(
        self,
        init_kwargs: Dict[str, Any],
        _env_file: Union[Path, str, None] = None,
        _env_file_encoding: Optional[str] = None,
        _secrets_dir: Union[Path, str, None] = None,
    ) -> Dict[str, Any]:
        # Configure built-in sources
        init_settings = InitSettingsSource(init_kwargs=init_kwargs)
        env_settings = EnvSettingsSource(
            env_file=(_env_file if _env_file != env_file_sentinel else self.__config__.env_file),
            env_file_encoding=(
                _env_file_encoding if _env_file_encoding is not None else self.__config__.env_file_encoding
            ),
        )
        file_secret_settings = SecretsSettingsSource(secrets_dir=_secrets_dir or self.__config__.secrets_dir)
        # Provide a hook to set built-in sources priority and add / remove sources
        sources = self.__config__.customise_sources(
            init_settings=init_settings, env_settings=env_settings, file_secret_settings=file_secret_settings
        )
        if sources:
            return deep_update(*reversed([source(self) for source in sources]))
        else:
            # no one should mean to do this, but I think returning an empty dict is marginally preferable
            # to an informative error and much better than a confusing error
            return {}

    class Config(pydantic.BaseConfig):
        env_prefix = ''
        env_file = None
        env_file_encoding = None
        secrets_dir = None
        validate_all = True
        extra = Extra.forbid
        arbitrary_types_allowed = True
        case_sensitive = False

        @classmethod
        def prepare_field(cls, field: ModelField) -> None:
            env_names: Union[List[str], AbstractSet[str]]
            field_info_from_config = cls.get_field_info(field.name)

            env = field_info_from_config.get('env') or field.field_info.extra.get('env')
            if env is None:
                if field.has_alias:
                    warnings.warn(
                        'aliases are no longer used by BaseSettings to define which environment variables to read. '
                        'Instead use the "env" field setting. '
                        'See https://pydantic-docs.helpmanual.io/usage/settings/#environment-variable-names',
                        FutureWarning,
                    )
                env_names = {cls.env_prefix + field.name}
            elif isinstance(env, str):
                env_names = {env}
            elif isinstance(env, (set, frozenset)):
                env_names = env
            elif sequence_like(env):
                env_names = list(env)
            else:
                raise TypeError(f'invalid field env: {env!r} ({display_as_type(env)}); should be string, list or set')

            if not cls.case_sensitive:
                env_names = env_names.__class__(n.lower() for n in env_names)
            field.field_info.extra['env_names'] = env_names

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return init_settings, env_settings, file_secret_settings

