from common.http_request import HttpRequest

import json
import os

class Walgreens:
    headers = {}

    @classmethod
    def build_message(cls):
        print("Building message for Walgreens")

    @classmethod
    def vaccine_availability(cls):
        token = cls._csrf_token()

    @classmethod
    def _stores(cls):
        stores = []

    @classmethod
    def _csrf_token(cls):
        url = "https://www.walgreens.com/browse/v1/csrf"
        resp = HttpRequest.get(url)
        data = resp.data.decode('utf-8')

        csrf_header = data['csrfHeaderName']
        csrf_token = data['csrfToken']
        cls.headers[csrf_header] = csrf_token
