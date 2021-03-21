from common.http_request import HttpRequest
from common.location import Location
from datetime import datetime

import json
import os

class Walgreens:
    availability = False
    search_radius = os.environ['SEARCH_RADIUS']
    zip_code = os.environ['ZIP_CODE']

    @classmethod
    def build_message(cls):
        print("Building message for Walgreens")
        available = cls.vaccine_availability()
        message = ''

        if available == True:
            message += f"Walgreens stores near {cls.zip_code} have vaccine appointments available!\n\n"
            message += "Walgreens Appointment Scheduler: https://www.walgreens.com/findcare/vaccination/covid-19/location-screening\n\n"
        else:
            message += f"No Walgreens stores have available COVID-19 vaccine appointments near {cls.zip_code}.\n\n"

        return message

    @classmethod
    def vaccine_availability(cls):
        print("Retrieving Walgreens COVID-19 vaccine appointment availablity data")
        session = HttpRequest.session()
        session = cls._csrf_token(session)
        location = Location.latitude_longitude_from_address(cls.zip_code)
        headers = {
            "Referer": "https://www.walgreens.com/findcare/vaccination/covid-19/location-screening"
        }
        body = {
            "serviceId": "99",
            "position": {
                "latitude": float(location['latitude']),
                "longitude": float(location['longitude'])
            },
            "appointmentAvailability": {
                "startDateTime": datetime.now().strftime('%Y-%m-%d')
            },
            "radius": 25
        }
        url = "https://www.walgreens.com/hcschedulersvc/svc/v1/immunizationLocations/availability"
        resp = HttpRequest.post(url, headers, body, session)

        if resp.ok != True:
            print(f"Failed to connect to Walgreens. HTTP Response Code: {resp.status_code} Body: {resp.json()}")
            return False

        data = resp.json()

        if data['appointmentsAvailable'] == True:
            print(f"Found available appointments at Walgreens!")
            cls.availability = True
            return True
        else:
            print(f"No Walgreens stores have available appointments near {cls.zip_code}.")
            return False

    @classmethod
    def _csrf_token(cls, session):
        headers = {}
        url = "https://www.walgreens.com/browse/v1/csrf"
        resp = HttpRequest.get(url, headers, session)
        data = resp.json()

        session.headers.update({ data['csrfHeaderName']: data['csrfToken'] })

        return session
