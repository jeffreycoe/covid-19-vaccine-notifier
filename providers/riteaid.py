from common.http_request import HttpRequest

import json
import os

class RiteAid:
    search_radius = os.environ['SEARCH_RADIUS']
    zip_code = os.environ['ZIP_CODE']

    @classmethod
    def build_message(cls):
        print("Building message for Rite Aid")
        stores = cls.vaccine_availability()
        message = ''

        if len(stores) == 0:
            message += "No Rite Aid stores have available COVID-19 vaccine appointments.\n\n"
            return message

        message += "Rite Aid Stores:\n\n"

        for store in stores.items():
            message += f"Store Number: {store['store_number']}\n"\
                     + f"Address: {store['address']}\n"\
                     + f"Phone Number: {store['phone_number']}\n\n"

        message += "Rite Aid Appointment Scheduler: https://www.riteaid.com/pharmacy/covid-qualifier\n\n"

        return message

    @classmethod
    def vaccine_availability(cls):
        print("Retrieving Rite Aid COVID-19 vaccine appointment availablity data")
        appts = []
        stores = cls._stores()

        for store in stores:
            store_number = store['storeNumber']
            url = f"https://www.riteaid.com/services/ext/v2/vaccine/checkSlots?storeNumber={store_number}"
            resp = HttpRequest.get(url)
            slots = json.loads(resp.data.decode('utf-8'))['Data']['slots']
            if (slots["1"] == True or slots["2"] == True):
                address = f"{store['address']} {store['city']}, {store['state']} {store['zipcode']}"
                phone_number = store['fullPhone']
                print(f"Found available appointment at Rite Aid store {store_number}!")
                appts.append({ 'address': address, 'phone_number': phone_number, 'store_number': store_number })

        if len(appts) == 0:
            print(f"No Rite Aid stores have available appointments in a {cls.search_radius} mile radius of {cls.zip_code}.")

        return appts

    @classmethod
    def _stores(cls):
        print(f"Retrieving Rite Aid stores within a {cls.search_radius} mile radius in {cls.zip_code}")
        url = f"https://www.riteaid.com/services/ext/v2/stores/getStores?address={cls.zip_code}&attrFilter=PREF-112&fetchMechanismVersion=2&radius={cls.search_radius}"
        resp = HttpRequest.get(url)
        stores = json.loads(resp.data.decode('utf-8'))['Data']['stores']
        return stores
