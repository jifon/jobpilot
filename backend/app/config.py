from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str = ""
    model_fast: str = "claude-haiku-4-5"
    model_smart: str = "claude-sonnet-5"
    database_url: str = "sqlite:///./data/jobpilot.db"
    prefilter_min_score: int = 30


settings = Settings()
