"""Application configuration bindings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    app_name: str = "SQB Payment Reference Python App"
    app_env: str = "dev"
    app_debug: bool = False

    sqb_base_url: str = "https://api.shouqianba.com"
    sqb_vendor_sn: str = Field(default="", description="Vendor serial number")
    sqb_vendor_key: str = Field(default="", description="Vendor signing key")
    sqb_access_token: str = Field(default="", description="SQB access token")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
