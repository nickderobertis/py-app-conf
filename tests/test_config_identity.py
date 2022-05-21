from dataclasses import dataclass

from pyappconf import BaseConfig, AppConfig


def test_base_config_is_consistent():
    """
    It turns out pydantic.BaseModel seems to create new instance of the passed
    fields rather than using the same instance. This can cause issues with modifying
    fields and then calling save and expecting it to work, if the fields are being modified
    outside of the model directly. pydantic dataclasses do not suffer from this issue,
    so this test is to confirm that the issue is not present after switching to the dataclasses version.
    """

    @dataclass
    class SubModel:
        a: str

    class RootModel(BaseConfig):
        sub_model: SubModel
        _settings: AppConfig = AppConfig(app_name="MyApp")

    sub_model = SubModel(a="a")
    model = RootModel(sub_model=sub_model)
    sub_model.a = "b"
    assert model.sub_model.a == "b"
    assert model.sub_model is sub_model
