import pytest
from unittest.mock import patch

from core.email_decoder import CustomParser, CustomDecoder


@pytest.fixture
def custom_decoder():
    return CustomDecoder(fallback_encoding='latin1')


@pytest.fixture
def custom_parser():
    return CustomParser(fallback_encoding='latin1')


def test_body_decode_utf8(custom_decoder):
    result = custom_decoder.body_decode(b'test')
    assert result == 'test'


def test_body_decode_fallback(custom_decoder):
    result = custom_decoder.body_decode(b't\xebst')
    assert result == 'tëst'


def test_body_decode_invalid_utf8(custom_decoder):
    result = custom_decoder.body_decode(b'\x80')
    assert result == '\x80'


@patch("core.email_decoder.CustomDecoder.body_decode")
def test_body_decode_exception(mock_body_decode, custom_decoder):
    mock_body_decode.side_effect = ValueError("Failed to decode body")
    with pytest.raises(ValueError) as ve:
        custom_decoder.body_decode(None)

    assert str(ve.value) == "Failed to decode body"


def test_custom_decoder_property(custom_parser):
    assert isinstance(custom_parser.custom_decoder, CustomDecoder)
