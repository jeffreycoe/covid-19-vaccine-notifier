from datetime import datetime
from providers.cvs import Cvs
from providers.riteaid import RiteAid

import boto3
import json
import os

def build_messages():
    print("Building notification message")
    messages = { 'email': '', 'sms': '' }
    time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    message = ''

    message += Cvs.build_message()
    message += RiteAid.build_message()

    messages['default'] = f"As of {time} UTC, the following stores have COVID-19 vaccine appointments:\n\n{message}"
    messages['email'] = f"As of {time} UTC, the following stores have COVID-19 vaccine appointments:\n\n{message}"

    return messages

def lambda_handler(event, context):
    print("Checking COVID-19 vaccine site availability")

    messages = build_messages()
    publish_notification(messages)

def publish_notification(messages):
    topic_arn = os.environ['SNS_TOPIC_ARN']
    sns = boto3.client('sns')

    print(f"Publishing SNS notification to {topic_arn}")
    sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(messages),
        MessageStructure="json",
        Subject="COVID-19 Vaccine Notification - Available Appointments"
    )
