import logging
import re

from configuration.logger_config import logger_config
from core.email_decoder import CustomParser
from error.custom_exceptions import ManualDLQError
from pydantic_model.api_model import ErrorEnum
from service.logger import CustomLoggerAdapter

logger = CustomLoggerAdapter(logging.getLogger(__name__), None)


class EmailParser:
    def __init__(self):
        self._custom_parser = CustomParser(fallback_encoding='latin1')

    def parse_email(self, gcs_email_as_bytes):
        try:
            msg = self._custom_parser.parsebytes(gcs_email_as_bytes)
            root_info = self._extract_email_metadata(msg)
            email_messages = self.get_top_reply_only(msg, root_info['recipient'].split('<')[0])
            return {**root_info, **email_messages}
        except Exception as e:
            error_value = f"Cannot process {gcs_email_as_bytes}\n Error: {e}"
            logger.error(error_value)
            raise ManualDLQError(
                original_request=logger_config.context.get().get("original_request"),
                error_desc=str(e),
                error_stage=ErrorEnum.EMAIL_PARSE,
            )

    def get_top_reply_only(self, msg, original_sender):
        def decode_email_content(part):
            """Process a single part of the email message."""
            content_decoded = {
                'content_type': part.get_content_type(),
                'content': self._custom_parser.custom_decoder.body_decode(part.get_payload(decode=True))
            }
            return content_decoded

        for msg_part in msg.walk():
            if msg_part.is_multipart() or msg_part.get_content_type() != 'text/plain':
                continue
            msg_content = decode_email_content(msg_part)
            content = msg_content['content']
            if original_sender in content:
                content = content.split(f'From: {original_sender}', 1)[0]

            msg_content['content'] = self._clean_text(content)

        return msg_content

    @staticmethod
    def _clean_text(text):
        # Replace newline and carriage return characters with a space
        for to_remove in ['\n', '\r', '\x96']:
            cleaned_text = text.replace(to_remove, " ")
        cleaned_text = ' '.join(cleaned_text.split())

        # Remove email signatures and email addresses
        cleaned_text = re.sub(r'\[cid:.*?]|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|--\s+.*$', '', cleaned_text)

        # Remove everything after "<mailto:>" or "________________________"
        cleaned_text = re.split(r'<mailto:>|________________________', cleaned_text)[0]

        return cleaned_text.strip()


    @staticmethod
    def _extract_email_metadata(msg):
        """Extract relevant email information for the root message."""
        return {
            'date_sent': msg['Date'] if msg['Date'] is not None else '',
            'sender': msg['From'] if msg['From'] is not None else '',
            'recipient': msg['To'] if msg['To'] is not None else '',
            'title': msg['Subject'].replace("Re: ", "") if msg['Subject'] is not None else ''
        }
