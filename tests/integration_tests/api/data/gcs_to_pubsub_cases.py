import base64
import json
from datetime import datetime

attributes = {
    "bucketId": "career_forger_email_bucket",
    "eventTime": "2023-07-31T15:01:06.058022Z",
    "eventType": "OBJECT_FINALIZE",
    "notificationConfig": "config",
    "objectGeneration": "1234",
    "objectId": f"test/processed/2024/05/31/test_file.eml",
    "payloadFormat": "JSON_API_V1",
}

valid_gcs_to_pubsub_data = {
    "message": {
        "data": {
            "kind": "storage#object",
            "id": "career_forger_email_bucket/email_test/Re_ Career Forger v1.0 Test.eml/1234567890123456",
            "selfLink": "dummy_link",
            "name": "email_test/Re_ Career Forger v1.0 Test.eml",
            "bucket": "career_forger_email_bucket",
            "contentType": "text/plain",
            "generation": "1234",
            "metageneration": "1",
            "timeCreated": str(datetime.now()),
            "updated": str(datetime.now()),
            "storageClass": "STANDARD",
            "timeStorageClassUpdated": str(datetime.now()),
            "size": "20",
            "md5Hash": "hash",
            "mediaLink": "dummy_link",
            "crc32c": "dummy",
            "etag": "dummy_etag"
        },
        "message_id": "test_message_id",
        "publish_time": "2023-07-31T15:01:06.058022+01:00",
        "attributes": attributes
    }
}

invalid_test_missing_name = {
    "message": {
        "data": {
            "kind": "storage_object",
            "id": "career_forger_email_bucket/email_test/Re_ Career Forger v1.0 Test.eml/1234567890123456",
            "selfLink": "dummy_link",
            "bucket": "career_forger_email_bucket",
            "generation": "1234",
            "metageneration": "1",
            "contentType": "text/plain",
            "timeCreated": str(datetime.now()),
            "updated": str(datetime.now()),
            "storageClass": "STANDARD",
            "timeStorageClassUpdated": str(datetime.now()),
            "size": "20",
            "md5Hash": "hash",
            "mediaLink": "dummy_link",
            "crc32c": "dummy",
            "etag": "dummy_etag"
        },
        "message_id": "test_message_id",
        "publish_time": "2023-07-31T15:01:06.058022+01:00",
        "attributes": attributes,
    }
}

invalid_test_missing_name_bytes = {
    "message": {
        "data": "eyJidWNrZXQiOiAiY2FyZWVyX2Zvcmdlcl9lbWFpbF9idWNrZXQifQ==",
        "message_id": "test_message_id",
        "publish_time": "2023-07-31T15:01:06.058022+01:00",
        "attributes": attributes,
    }
}

invalid_test_non_dict_data = {
    "message": {
        "data": [{"a": "b"}],
        "message_id": "test_message_id",
        "publish_time": "2023-07-31T15:01:06.058022+01:00",
        "attributes": attributes,
    }
}

invalid_test_missing_message_id = {
    "message": {
        "data": {
            "name": "email_test/Re_ Career Forger v1.0 Test.eml",
            "bucket": "career_forger_email_bucket",
        },
        "publish_time": "2023-07-31T15:01:06.058022+01:00",
        "attributes": attributes,
    }
}

test_content = """Hi Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec maximus suscipit odio, quis dictum velit. Pellentesque id urna a massa lobortis varius. Ut consectetur elementum sapien nec bibendum. Pellentesque a accumsan diam. Morbi sit amet congue felis. Morbi sagittis est justo, eget consequat est rutrum eget. Morbi nec orci lacinia augue pulvinar consectetur. Morbi auctor nec elit non aliquet. In maximus dignissim risus, ac tempor dui placerat non. Donec quis velit velit. Proin tempor sem mauris. Vivamus ac porta urna, ut feugiat nisi. Aliquam sed nibh mauris. Integer condimentum felis sit amet libero euismod rutrum. Nulla neque ante, scelerisque vitae augue ornare, vulputate egestas leo. Sed vehicula et ex eget facilisis. Maecenas egestas sapien ut facilisis venenatis. Proin nec lorem ac urna dictum feugiat id quis arcu. Sed ornare nulla sit amet odio accumsan malesuada. Ut ultrices lacus eget nisi vulputate, ac viverra sapien bibendum. Curabitur nunc lacus, venenatis id augue porttitor, tempus viverra sapien. Integer et dictum dui, in lacinia dui. Cras viverra gravida malesuada. Nam nec augue lorem. Nam sit amet massa at magna tempus porttitor. Praesent est tellus, lobortis sit amet leo quis, lacinia interdum enim. Maecenas imperdiet risus et velit feugiat facilisis. Curabitur at velit quis nunc suscipit ullamcorper. Cras pharetra nisi vel purus imperdiet, nec condimentum ligula faucibus. Morbi bibendum dolor ipsum, ac lobortis sapien pretium sit amet. Morbi id venenatis massa. Duis porttitor urna a scelerisque gravida. Ut quis risus velit. Maecenas nec mattis turpis. Proin ullamcorper dui sed aliquet auctor. Vivamus tristique, neque in rhoncus viverra, tortor felis finibus nisl, ac feugiat dolor elit a dui. In hac habitasse platea dictumst. Morbi vitae ante pharetra, iaculis nisl ac, maximus sem. Nullam nec bibendum enim. Duis eleifend, ex venenatis commodo convallis, arcu eros facilisis felis, eu tristique ante lacus semper elit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. In eleifend congue arcu, eu ullamcorper nisi suscipit nec. Donec ac augue metus. Etiam fermentum lectus porta finibus sodales. Pellentesque ut sagittis nisl, eget suscipit lectus. Nulla non est eget est euismod viverra. Praesent blandit massa sed viverra eleifend. Duis ornare massa velit, quis sodales justo semper vitae. Proin quis vehicula velit. Donec sit amet nisl et arcu consequat fermentum ut ornare mauris. Interdum et malesuada fames ac ante ipsum primis in faucibus. Fusce neque neque, fringilla et consequat ac, eleifend at mauris. Kind Regards Bashir Ali Data Engineer Advanced Analytics, Data Platforms"""

valid_response = {"date_sent": "Sat, 8 Jun 2024 11:26:36 +0000",
                  "sender": "Bashir Ali <Bashir.Ali@virginmediao2.co.uk>",
                  "recipient": "Bashir Ali <Bashir.Ali@virginmediao2.co.uk>",
                  "title": "Career Forger v1.0 Test",
                  "content_type": "text/plain",
                  "content": test_content}
