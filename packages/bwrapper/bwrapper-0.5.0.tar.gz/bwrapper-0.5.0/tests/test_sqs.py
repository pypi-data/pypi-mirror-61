import json
from typing import Dict, List

import pytest

from bwrapper.sqs import GenericSqsMessage, SqsMessage


def test_all():
    class JobMessage(SqsMessage):
        class MessageAttributes:
            job_id: str

        class MessageBody:
            uuid: str
            request: Dict

    job = JobMessage.from_sqs_dict({
        "MessageAttributes": {
            "job_id": {
                "DataType": "string",
                "StringValue": "123-456",
            },
        },
        "Body": json.dumps({  # It is "Body" in the payload as returned by AWS, but it's MessageBody in the request.
            "uuid": "1234-1234-1234-1234",
            "request": {
                "version": "JobRequest-1.0",
                "command": "bwrapper.providers.test.succeed",
            },
        }),
    })

    assert job.MessageAttributes.job_id == "123-456"
    assert job.MessageBody.uuid == "1234-1234-1234-1234"
    assert job.MessageBody.request["version"] == "JobRequest-1.0"
    assert job.MessageBody.request["command"] == "bwrapper.providers.test.succeed"

    sqs_dict = job.to_sqs_dict()
    assert sqs_dict["MessageAttributes"] == {
        "sqs_message_type": {
            "DataType": "String",
            "StringValue": "JobMessage",
        },
        "sqs_body_type": {
            "DataType": "String",
            "StringValue": "json",
        },
        "job_id": {
            "DataType": "String",
            "StringValue": "123-456",
        },
    }
    assert json.loads(sqs_dict["MessageBody"]) == {
        "uuid": "1234-1234-1234-1234",
        "request": {
            "version": "JobRequest-1.0",
            "command": "bwrapper.providers.test.succeed",
        },
    }

    # Make sure can write too
    job.MessageAttributes.job_id = "987-654"
    job.MessageBody.uuid = "8888-8888-8888-8888"
    job.MessageBody.request["command_params"] = {"period": "today"}

    assert job.MessageAttributes.job_id == "987-654"
    assert job.MessageBody.uuid == "8888-8888-8888-8888"

    sqs_dict = job.to_sqs_dict()
    assert sqs_dict["MessageAttributes"] == {
        "sqs_body_type": {
            "DataType": "String",
            "StringValue": "json",
        },
        "sqs_message_type": {
            "DataType": "String",
            "StringValue": "JobMessage",
        },
        "job_id": {
            "DataType": "String",
            "StringValue": "987-654",
        },
    }
    assert json.loads(sqs_dict["MessageBody"]) == {
        "uuid": "8888-8888-8888-8888",
        "request": {
            "version": "JobRequest-1.0",
            "command": "bwrapper.providers.test.succeed",
            "command_params": {
                "period": "today",
            },
        },
    }

    job2 = JobMessage()
    job2.MessageBody.uuid = "5555-5555"
    assert job2.MessageBody.uuid == "5555-5555"


def test_message_body_and_message_attributes_definitions_are_optional():
    class Message1(SqsMessage):
        pass

    class Message2(SqsMessage):
        class MessageBody:
            pass

    class Message3(SqsMessage):
        class MessageAttributes:
            pass

    Message1()
    Message2()
    Message3()


def test_message_attributes_from_dict():
    class Tx(SqsMessage):
        class MessageAttributes:
            currency: str
            amount: int

    tx: Tx = Tx(attributes={"currency": "GBP", "amount": 123})
    assert tx.MessageAttributes.currency == "GBP"
    assert tx.MessageAttributes.amount == 123


def test_message_body_from_dict():
    class Log(SqsMessage):
        class MessageBody:
            account: Dict
            transactions: List

    log: Log = Log(body={"account": {"name": "First"}, "transactions": [{"amount": 11}, {"amount": 20}]})
    assert log.MessageBody.account["name"] == "First"
    assert log.MessageBody.transactions[1]["amount"] == 20


def test_serialised_message_attributes_include_message_type():
    class Greeting(SqsMessage):
        class MessageAttributes:
            message: str

    greeting = Greeting(attributes={"message": "hello"})
    assert greeting.MessageAttributes.message == "hello"
    assert greeting.MessageAttributes.sqs_message_type == "Greeting"


def test_sqs_message_type_is_always_set():
    assert GenericSqsMessage().MessageAttributes.sqs_message_type == "GenericSqsMessage"
    assert GenericSqsMessage().to_sqs_dict()["MessageAttributes"]["sqs_message_type"] == {
        "DataType": "String",
        "StringValue": "GenericSqsMessage",
    }


def test_generic_sqs_message_accepts_anything():
    assert GenericSqsMessage.MessageAttributes._definition.accepts_anything
    assert GenericSqsMessage.MessageBody._definition.accepts_anything

    message = GenericSqsMessage(attributes={"a": 12, "b": "23"}, body={"c": 34, "d": "45"})
    assert message.MessageAttributes._accepts_anything
    assert message.MessageBody._accepts_anything

    assert message.MessageAttributes.a == 12
    assert message.MessageAttributes.b == "23"
    assert message.MessageBody.c == 34
    assert message.MessageBody.d == "45"


def test_generic_sqs_message_with_unknown_fields_doesnt_raise_exception():
    class Message(GenericSqsMessage):
        class MessageAttributes:
            message: str

    raw = {
        "MessageId": "9ac265aa-c50d-4846-a980-8b98e451627f",
        "ReceiptHandle": "blablabla",
        "MD5OfBody": "blablabla", "Body": "{}",
        "MD5OfMessageAttributes": "blablabla",
        "MessageAttributes": {
            "message": {"StringValue": "Hello", "DataType": "String"},
            "name": {"StringValue": "world", "DataType": "String"}
        }
    }

    message = Message.from_sqs_dict(raw)
    assert message.MessageAttributes.sqs_body_type == "json"
    assert message.MessageAttributes.message == "Hello"
    assert message.MessageAttributes.name == "world"

    dct = message.to_sqs_dict()
    assert dct["MessageAttributes"] == {
        "sqs_message_type": {"StringValue": "Message", "DataType": "String"},
        "sqs_body_type": {"StringValue": "json", "DataType": "String"},
        "message": {"StringValue": "Hello", "DataType": "String"},
        "name": {"StringValue": "world", "DataType": "String"}
    }
    assert dct["MessageBody"] == "{}"

    assert message.extract_body() == {}
    assert message.extract_attributes() == {
        "message": "Hello",
        "name": "world",
    }


def test_unknown_fields_passed_as_attributes_or_body_raises_exception():
    # See also test_unknown_fields_dont_raise_exception

    class Message(SqsMessage):
        class MessageBody:
            subject: str

        class MessageAttributes:
            message: str

    with pytest.raises(AttributeError):
        Message(attributes={"title": "This is the title"})

    with pytest.raises(AttributeError):
        Message(body={"body": "This is the body"})


def test_int_and_bool_message_attributes():
    class Message(SqsMessage):
        class MessageAttributes:
            timeout: int
            validate: bool

    message = Message(attributes={"timeout": "123", "validate": 0})
    assert message.MessageAttributes.timeout == 123
    assert message.MessageAttributes.validate is False

    raw = {
        "MessageId": "9ac265aa-c50d-4846-a980-8b98e451627f",
        "ReceiptHandle": "blablabla",
        "MD5OfBody": "blablabla", "Body": "{}",
        "MD5OfMessageAttributes": "blablabla",
        "MessageAttributes": {
            "timeout": {"StringValue": "123", "DataType": "String"},
            "validate": {"StringValue": "True", "DataType": "String"},
        }
    }
    message = Message.from_sqs_dict(raw)
    assert message.MessageAttributes.timeout == 123
    assert message.MessageAttributes.validate is True


def test_plain_string_as_message_body():
    message = SqsMessage(body="Hello world!")
    assert message.MessageBody.sqs_body == "Hello world!"
    assert message.body == "Hello world!"

    message.body = "Bye world!"
    assert message.body == "Bye world!"
    assert message.MessageBody.sqs_body == "Bye world!"

    assert message.to_sqs_dict()["MessageBody"] == "Bye world!"

    message.body = None
    assert message.body is None
    assert "MessageBody" not in message.to_sqs_dict()


def test_extract_sns_message():
    message = GenericSqsMessage.from_sqs_dict({
        "MessageId": "9f843e3f-3141-42af-813a-75cd9c5132ea",
        "ReceiptHandle": "blablabla",
        "MD5OfBody": "deadbeefbaddadabbabeefbaaa",
        "Body": '{\n  "Type" : "Notification",\n  "MessageId" : "d9ba645b-6783-53be-b6b1-32e42aae84eb",\n  "TopicArn" : "arn:aws:sns:eu-west-1:account-id:topic-name",\n  "Subject" : "Are you listening?",\n  "Message" : "Hello again",\n  "Timestamp" : "2020-02-13T13:11:09.354Z",\n  "SignatureVersion" : "1",\n  "Signature" : "blablabla",\n  "SigningCertURL" : "https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-234523452345234523452345.pem",\n  "UnsubscribeURL" : "https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-1:account-id:topic-name:beefdeafbaddadabbadeadbee10"\n}'  # noqa
    })

    notif = message.extract_sns_notification()
    assert notif.topic_arn == "arn:aws:sns:eu-west-1:account-id:topic-name"
    assert notif.subject == "Are you listening?"
    assert notif.message == "Hello again"
