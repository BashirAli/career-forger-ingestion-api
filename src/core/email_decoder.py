import email.charset
from email.parser import BytesParser
import email


class CustomParser(BytesParser):
    def __init__(self, fallback_encoding='latin1'):
        super().__init__()
        self._custom_decoder = CustomDecoder(fallback_encoding=fallback_encoding)

    @property
    def custom_decoder(self):
        return self._custom_decoder


class CustomDecoder(email.charset.Charset):
    def __init__(self, fallback_encoding='latin1'):
        super().__init__()
        self.fallback_encoding = fallback_encoding

    def body_decode(self, s):
        try:
            return s.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return s.decode(self.fallback_encoding)
            except Exception as e:
                raise ValueError("Failed to decode body") from e
        except Exception as e:
            raise ValueError("Failed to decode body") from e
