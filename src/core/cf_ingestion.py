from __future__ import annotations

from service.logger import CustomLoggerAdapter
from helper.utils import read_validate_message_data
from core.email_parser import EmailParser
from configuration.env import settings
from gcp.gcs import GoogleCloudStorage
from gcp.pubsub import PubSubPublisher
import logging
import pendulum

logger = CustomLoggerAdapter(logging.getLogger(__name__), None)


class CareerForgerIngestion:
    def __init__(self):
        self._gcs_client = GoogleCloudStorage(project_id=settings.gcp_project_id)
        self._email_client = EmailParser()
        self._pubsub_client = PubSubPublisher(project_id=settings.gcp_project_id,
                                              topic=settings.pubsub_publish_topic_id)

    def process(self, message):
        # 1. validate pubsub as gcs event
        gcs_pubsub_event = read_validate_message_data(message)
        # 2. read gcs file
        email_data = self._gcs_client.read_gcs_file_to_bytes(
            bucket_name=gcs_pubsub_event.bucket,
            source_blob_name=gcs_pubsub_event.name
        )
        logger.info(msg=f"Processing Email: {gcs_pubsub_event.name} from GCS")
        # 3. transform + clean data in file + redact PII
        formatted_email = self._email_client.parse_email(email_data)
        logger.info(f"Email formatted. Not logging in case of PII")

        # 4. push to pubsub
        self._pubsub_client.publish(data=formatted_email, source_publish_time=str(pendulum.now("Europe/London")))
