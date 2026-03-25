from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Ad Analytics Pipeline"
    mode: str = "demo"

    # AWS
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    s3_bucket: str = "ad-analytics-docs"

    # Meta Ads
    meta_access_token: str = ""
    meta_ad_account_id: str = ""

    # Google Ads
    google_ads_developer_token: str = ""
    google_ads_customer_id: str = ""

    # GA4
    ga4_property_id: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
