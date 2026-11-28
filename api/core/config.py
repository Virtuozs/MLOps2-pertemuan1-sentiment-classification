from functools import lru_cache
from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


# api/config.toml, found relative to this file so it works from any working directory.
CONFIG_FILE = Path(__file__).resolve().parents[1] / "config.toml"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file=CONFIG_FILE,
        extra="ignore",
        protected_namespaces=("settings_",),
    )

    # Empty means "no key configured": every request is rejected (fail closed).
    api_key: str = ""
    model_path: Path = Path("models/best_model/model.joblib")
    model_info_path: Path = Path("models/best_model/model_info.json")
    model_name: str = "sentiment-sgd-tfidf"
    # Used by `python -m api`. 0.0.0.0 listens on all network interfaces.
    host: str = "0.0.0.0"
    port: int = 8000

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings, env_settings, TomlConfigSettingsSource(settings_cls))


@lru_cache
def get_settings() -> Settings:
    return Settings()
