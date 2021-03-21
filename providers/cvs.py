from common.http_request import HttpRequest

import json
import os

class Cvs:
    state = os.environ['STATE']

    @classmethod
    def build_message(cls):
        print("Building message for CVS")
        stores = cls.vaccine_availability()
        message = ''

        if len(stores) == 0:
            message += "No CVS stores have available COVID-19 vaccine appointments.\n\n"
            return message

        message += "CVS Stores:\n\n"

        for store in stores:
            message += f"{store}\n"

        message += "\nCVS Appointment Scheduler: https://www.cvs.com/immunizations/covid-19-vaccine\n\n"

        return message

    @classmethod
    def vaccine_availability(cls):
        print(f"Retrieving CVS COVID-19 vaccine appointment availablity data in {cls.state}")
        appts = []
        stores = cls._stores()

        for store in stores:
            city = store['city']
            state = store['state']
            status = store['status'].lower()

            if status == 'available':
                print(f"Found CVS store with available appointments in {city}, {state}!")
                appts.append(f"{city}, {state}")

        if len(appts) == 0:
            print(f"No CVS stores have available appointments in {cls.state}.")

        return appts

    @classmethod
    def _stores(cls):
        headers = {
            "Referer": "https://www.cvs.com/immunizations/covid-19-vaccine"
        }
        url = f"https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{cls.state}.json"
        resp = HttpRequest.get(url, headers)
        data = resp.json()['responsePayloadData']['data'][cls.state]
        return data
