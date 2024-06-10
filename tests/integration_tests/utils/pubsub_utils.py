import json
from typing import List

from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1

from configuration.env import settings


class PubSubUtils:
    """PubSub emulator interaction"""

    def __init__(self):
        self.project_id = settings.gcp_project_id
        self.publisher = pubsub_v1.PublisherClient()

    def create_temp_topic(self, topic_name: str):
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        self.publisher.create_topic(request={"name": topic_path})
        return topic_path

    def delete_temp_topic(self, topic_path):
        self.publisher.delete_topic(request={"topic": topic_path})

    def create_temp_sub(self, topic_path, subscription_name):
        with pubsub_v1.SubscriberClient() as subscriber:
            subscription_path = subscriber.subscription_path(
                self.project_id, subscription_name
            )
            try:
                subscriber.create_subscription(
                    request={"name": subscription_path, "topic": topic_path}
                )
            except AlreadyExists:
                pass

        return subscription_path

    def create_temp_push_sub(
        self, topic_path: str, subscription_name: str, endpoint: str
    ):
        with pubsub_v1.SubscriberClient() as subscriber:
            subscription_path = subscriber.subscription_path(
                self.project_id, subscription_name
            )
            try:
                subscriber.create_subscription(
                    request={
                        "name": subscription_path,
                        "topic": topic_path,
                        "push_config": {"push_endpoint": endpoint},
                    }
                )
            except AlreadyExists:
                pass

        return subscription_path

    @staticmethod
    def delete_temp_sub(subscription_path: str = None):
        with pubsub_v1.SubscriberClient() as subscriber:
            subscriber.delete_subscription(request={"subscription": subscription_path})

    @staticmethod
    def pull_msgs(subscription_path: str) -> list:
        with pubsub_v1.SubscriberClient() as subscriber:
            response = subscriber.pull(
                request={"subscription": subscription_path, "max_messages": 5},
                timeout=5,
            )
            messages = [
                msg.message.data.decode("utf-8") for msg in response.received_messages
            ]
            if len(messages) > 0:
                ack_ids = [msg.ack_id for msg in response.received_messages]
                subscriber.acknowledge(
                    request={
                        "subscription": subscription_path,
                        "ack_ids": ack_ids,
                    }
                )
        return messages

    def ack_msgs(self, messages: list, subscription_id: str):
        ack_ids = [msg.ack_id for msg in messages]
        subscription_path = pubsub_v1.SubscriberClient.subscription_path(
            self.project_id, subscription_id
        )
        with pubsub_v1.SubscriberClient() as subscriber:
            subscriber.acknowledge(
                request={
                    "subscription": subscription_path,
                    "ack_ids": ack_ids,
                }
            )

    def publish_msgs(self, topic_path: str, messages: List[dict]):
        for msg in messages:
            body = json.dumps(msg).encode("utf-8")
            self.publisher.publish(topic=topic_path, data=body)
