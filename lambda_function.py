from datetime import datetime
from providers.cvs import Cvs
from providers.riteaid import RiteAid
from providers.walgreens import Walgreens

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
    message += Walgreens.build_message()

    message += "\nNote: The available appointments above are not guaranteed and eligibility must be verified."

    messages['default'] = f"As of {time} UTC, the following stores have COVID-19 vaccine appointments:\n\n{message}"
    messages['email'] = f"As of {time} UTC, the following stores have COVID-19 vaccine appointments:\n\n{message}"

    return messages

def skip_publish_notification():
    availability = [Cvs.availability, RiteAid.availability, Walgreens.availability]
    skip_publish = all(entry == False for entry in availability)

    return skip_publish

def lambda_handler(event, context):
    print("Checking COVID-19 vaccine site availability")

    messages = build_messages()
    skip_publish = skip_publish_notification()

    if skip_publish == True:
        print(f"Skipping publishing message to SNS topic as no stores have vaccine appointment availability.")
    else:
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
