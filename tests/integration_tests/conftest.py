import logging

import pytest
from fastapi.testclient import TestClient
import json
from configuration.env import settings
from main import app

from utils.cloud_storage_utils import CloudStorageUtils
from utils.pubsub_utils import PubSubUtils

TEST_EMAIL_FILE_PATH = "/home/appuser/tests/integration_tests/api/data/Re_ Career Forger v1.0 Test.eml"

DEST_BLOB_NAME = "email_test/Re_ Career Forger v1.0 Test.eml"


@pytest.fixture
def upload_test_file(gcs_utils):
    with open(TEST_EMAIL_FILE_PATH, "r") as f:
        test_file = f.read()
    gcs_utils.upload_file_from_buffer(
        bucket=settings.email_bucket,
        file_name=DEST_BLOB_NAME,
        string_data=test_file,
    )

    return test_file


@pytest.fixture
def gcs_utils():
    return CloudStorageUtils()


@pytest.fixture
def pubsub_utils():
    return PubSubUtils()


@pytest.fixture()
def pubsub_testing_dlq_topic(pubsub_utils):
    # Create a new Pub/Sub topic for testing
    topic_path = pubsub_utils.create_temp_topic(settings.dlq_topic)
    yield topic_path

    # Clean up the topic after testing
    pubsub_utils.delete_temp_topic(topic_path)


@pytest.fixture
def pubsub_testing_dlq_subscription(pubsub_utils, pubsub_testing_dlq_topic):
    # Create a new Pub/Sub subscription for testing
    subscription_path = pubsub_utils.create_temp_sub(
        topic_path=pubsub_testing_dlq_topic, subscription_name="dlq_dummy_subscription"
    )
    yield subscription_path

    # Clean up the subscription after testing
    pubsub_utils.delete_temp_sub(subscription_path)


@pytest.fixture()
def pubsub_testing_topic(pubsub_utils):
    # Create a new Pub/Sub topic for testing
    topic_path = pubsub_utils.create_temp_topic(settings.pubsub_publish_topic_id)
    yield topic_path

    # Clean up the topic after testing
    pubsub_utils.delete_temp_topic(topic_path)


@pytest.fixture
def pubsub_testing_subscription(pubsub_utils, pubsub_testing_topic):
    # Create a new Pub/Sub subscription for testing
    subscription_path = pubsub_utils.create_temp_sub(
        topic_path=pubsub_testing_topic, subscription_name="dummy_subscription"
    )
    yield subscription_path

    # Clean up the subscription after testing
    pubsub_utils.delete_temp_sub(subscription_path)


@pytest.fixture(scope="function")
def api_client(request):
    """Generate an API test client

    Need to parametrize with a ScheduleModeEnum member, eg:
       @pytest.mark.parametrize("api_client", [ScheduleModeEnum.ALWAYS_ON], indirect=True)
    """

    yield TestClient(app)
