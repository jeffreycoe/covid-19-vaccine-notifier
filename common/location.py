from common.http_request import HttpRequest

import urllib

class Location:
    API_BASE_URL = "https://nominatim.openstreetmap.org"

    @classmethod
    def latitude_longitude_from_address(cls, address):
        print(f"Retrieving latitude and longitude for address {address}")
        location = { 'latitude': '', 'longitude': '' }
        address = urllib.parse.quote(address)
        api_url = f"{cls.API_BASE_URL}/search/{address}%20USA?format=json&addressdetails=1&limit=1"

        resp = HttpRequest.get(api_url)
        loc_data = resp.json()[0]

        print(f"Found latitude {loc_data['lat']} and longitude {loc_data['lon']} for address {address}!")
        location['latitude'] = loc_data['lat']
        location['longitude'] = loc_data['lon']

        return location
