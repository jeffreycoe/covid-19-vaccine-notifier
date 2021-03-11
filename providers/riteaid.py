from common.http import Http

import json
import os

class RiteAid:
    search_radius = os.environ['SEARCH_RADIUS']
    zip_code = os.environ['ZIP_CODE']

    @classmethod
    def vaccine_availability(cls):
        print("Retrieving Rite Aid COVID-19 vaccine appointment availablity data")
        appts = []
        stores = cls._stores()
        
        for store in stores:
            store_number = store['storeNumber']
            url = f"https://www.riteaid.com/services/ext/v2/vaccine/checkSlots?storeNumber={store_number}"
            resp = Http.get(url)
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
        resp = Http.get(url)
        stores = json.loads(resp.data.decode('utf-8'))['Data']['stores']
        return stores
        