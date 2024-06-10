import datetime
import logging
from unittest.mock import MagicMock, patch
import json
from core.email_parser import EmailParser
import pytest
from conftest import DEST_BLOB_NAME
from configuration.env import settings
from api.data.gcs_to_pubsub_cases import valid_response
parser = EmailParser()


def test_read_from_emulator(gcs_utils, upload_test_file):
    # read the test file sent to test bucket
    input_file_from_emulator = gcs_utils.read_file(
        bucket_name=settings.email_bucket,
        source_blob_name=DEST_BLOB_NAME,
    )

    formatted_email = parser.parse_email(gcs_email_as_bytes=input_file_from_emulator)

    assert all(key in ["date_sent", "sender", "recipient", "title", "content_type", "content"] for key in
               formatted_email.keys())
    assert all(value not in ("", None) for value in formatted_email.values())

    assert formatted_email == valid_response
