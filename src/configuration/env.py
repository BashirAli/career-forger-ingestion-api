from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gcp_project_id: str = Field(..., alias="GCP_PROJECT_ID")
    api_name: str = "career-forger-ingestion-api"
    is_test_env: Optional[bool] = Field(
        default=False, alias="IS_TEST_ENV"
    )
    email_bucket: str = Field(..., alias="SOURCE_BUCKET")  # "career_forger_email_bucket"
    pubsub_publish_topic_id: str = "career_forger_transformed.topic"
    dlq_topic: str = "career_forger_dlq.topic"


settings = Settings()
