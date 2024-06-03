from pydantic_model.api_model import Message


class DeadLetterQueueError(Exception):
    """Custom Exception for manual DLQ

    Args:
        Exception ([type]): [description]
    """

    def __init__(
        self, original_message: Message, error_description: str, error_stage: str
    ):
        self.original_message = original_message
        self.error_description = error_description
        self.error_stage = error_stage


class SendToReprocessError(Exception):
    """Custom exception to reprocess a message

    Args:
        Exception ([type]): [description]
    """

    def __init__(self, original_message, error_description, error_stage):
        self.original_message = original_message
        self.error_description = error_description
        self.error_stage = error_stage


class MessageDecodeError(Exception):
    """Custom Exception for pubsub decode validation

    Args:
        Exception ([type]): [description]
    """
class MessageValidationError(Exception):
    """Custom Exception for pubsub data validation

    Args:
        Exception ([type]): [description]
    """

class PubsubPublishException(Exception):
    """Custom Exception for PubSub Publish Exceptions

    Args:
        Exception ([type]): [description]
    """
class DatastoreGenericError(Exception):
    """Custom Exception for generic issues when data fetched from Datastore

    Args:
        Exception ([type]): [description]
    """


class DatastoreNotFoundException(Exception):
    """Custom Exception for data not found when fetched from Datastore

        Args:
            Exception ([type]): [description]
        """

class ModelValidationError(Exception):
    """Custom Exception for Pydantic Model Validation

    Args:
        Exception ([type]): [description]
    """



class DatastoreMultiResultException(Exception):
    """Custom Exception for multiple entities fetched from Datastore

    Args:
        Exception ([type]): [description]
    """


class InternalAPIException(Exception):
    """Custom Exception for Internal api exceptions

    Args:
        Exception ([type]): [description]
    """