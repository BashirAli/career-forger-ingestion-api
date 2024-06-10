import pytest
from unittest.mock import patch
from email import message_from_bytes
from core.email_parser import EmailParser
from error.custom_exceptions import ManualDLQError


def test_successful_parse_email():
    email_parser = EmailParser()
    result = email_parser.parse_email(
        b'From: sender@example.com\nTo: recipient@example.com\nDate: Thu, 1 Apr 2021 12:00:00 +0000\nSubject: Test Email\n\nThis is the body of the email.'
    )

    expected_result = {
        'date_sent': 'Thu, 1 Apr 2021 12:00:00 +0000',
        'sender': 'sender@example.com',
        'recipient': 'recipient@example.com',
        'title': 'Test Email',
        'content_type': 'text/plain',
        'content': 'This is the body of the email.'
    }

    assert result == expected_result


def test_missing_metadata():

    email_parser = EmailParser()
    actual_result = email_parser.parse_email(
        b'From: sender@example.com\n\nThis is the body of the email.'
    )
    expected_result = {
        'date_sent': '',
        'sender': 'sender@example.com',
        'recipient': '',
        'title': '',
        'content_type': 'text/plain',
        'content': 'This is the body of the email.'
    }

    assert expected_result == actual_result


@patch.object(EmailParser, 'parse_email')
def test_invalid_email_bytes(mock_parse_email):
    mock_parse_email.side_effect = Exception("Invalid bytes")

    email_parser = EmailParser()

    with pytest.raises(Exception) as ex:
        email_parser.parse_email(b'Invalid bytes')

    assert str(ex.value) == "Invalid bytes"


def test_clean_text():
    assert EmailParser._clean_text("Hello\nWorld\r") == "Hello World"
    assert EmailParser._clean_text("Hello \x96 World") == "Hello World"
    assert EmailParser._clean_text("email@example.com") == ""
    assert EmailParser._clean_text("--\nSignature") == ""
    assert EmailParser._clean_text("Content <mailto:> More content") == "Content"
    assert EmailParser._clean_text("Content ________________________ More content") == "Content"
    assert EmailParser._clean_text("") == ""


def test_extract_email_metadata():
    msg = message_from_bytes(
        b'From: sender@example.com\nTo: recipient@example.com\nDate: Thu, 1 Apr 2021 12:00:00 +0000\nSubject: Re: Test Email\n\nThis is the body of the email.'
    )
    expected_metadata = {
        'date_sent': 'Thu, 1 Apr 2021 12:00:00 +0000',
        'sender': 'sender@example.com',
        'recipient': 'recipient@example.com',
        'title': 'Test Email'
    }
    assert EmailParser._extract_email_metadata(msg) == expected_metadata

### TODO ADD DLQ ERROR LOGGING AND CATCHING
### TODO ADD EXCEPTION IN GET_TOP_REPLY IF ITS EMPTY