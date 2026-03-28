"""Application configuration bindings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    app_name: str = "SQB Payment Reference Python App"
    app_env: str = "dev"
    app_debug: bool = False

    sqb_base_url: str = "https://vsi-api.shouqianba.com"
    sqb_vendor_sn: str = Field(default="", description="Vendor serial number")
    sqb_vendor_key: str = Field(default="", description="Vendor signing key")
    sqb_callback_public_key: str = Field(default="", description="SQB callback RSA public key")
    sqb_timeout_seconds: float = Field(default=10.0, description="SQB HTTP timeout in seconds")
    sqb_use_stub_transport: bool = Field(
        default=True,
        description="Use local stub transport instead of real HTTP requests",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
