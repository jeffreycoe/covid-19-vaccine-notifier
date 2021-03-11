from datetime import datetime
from providers.cvs import Cvs
from providers.riteaid import RiteAid

import boto3
import json
import os

def build_messages(stores):
    print("Building notification message")
    messages = { 'email': '', 'sms': '' }
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    stores_text = ''

    for store, locations in stores.items():
        if store == 'CVS':
            if len(locations) == 0:
                stores_text += "\nNo CVS stores have available COVID-19 vaccine appointments.\n"
            else:
                stores_text += "\nCVS Stores:\n\n"

                for location in locations:
                    stores_text += f"{location}\n"

                stores_text += "\nCVS Appointment Scheduler: https://www.cvs.com/immunizations/covid-19-vaccine\n\n"

        if store == 'Rite Aid':
            if len(locations) == 0:
                stores_text += "\nNo Rite Aid stores have available COVID-19 vaccine appointments.\n"
            else:
                stores_text += "\nRite Aid Stores:\n\n"

                for location in locations:
                    stores_text += f"Store Number: {location['store_number']}\n"\
                                 + f"Address: {location['address']}\n"\
                                 + f"Phone Number: {location['phone_number']}\n\n"

                stores_text += "Rite Aid Appointment Scheduler: https://www.riteaid.com/pharmacy/covid-qualifier\n\n"

    messages['default'] = f"As of {time}, the following stores have COVID-19 vaccine appointments:\n\n{stores_text}"
    messages['email'] = f"As of {time}, the following stores have COVID-19 vaccine appointments:\n\n{stores_text}"
    messages['sms'] = f"COVID-19 Vaccine Sites Available:\n{stores_text}"

    return messages

def lambda_handler(event, context):
    print("Checking COVID-19 vaccine site availability")

    stores = vaccine_availability()

    if stores['availability'] == True:
        messages = build_messages(stores)
        publish_notification(messages)
    else:
        print("No stores were found with available COVID-19 vaccine.")

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

def vaccine_availability():
    stores = {}
    stores['availability'] = False
    stores['CVS'] = Cvs.vaccine_availability()
    stores['Rite Aid'] = RiteAid.vaccine_availability()

    for store in stores:
        if store == 'availability':
            continue

        if len(stores[store]) > 0:
            stores['availability'] = True

    return stores
