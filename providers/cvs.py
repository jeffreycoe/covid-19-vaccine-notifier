from common.http import Http

import json
import os

class Cvs:
    state = os.environ['STATE']

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
        resp = Http.get(url, headers)
        data = json.loads(resp.data.decode('utf-8'))['responsePayloadData']['data'][cls.state]
        return data
