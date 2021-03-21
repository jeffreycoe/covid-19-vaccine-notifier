import requests

class HttpRequest:
    user_agent = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.48"
    }

    def __init__(self):
        self.session = requests.Session()

    def get(self, url, headers={}):
        headers.update(self.user_agent)
        resp = self.session.get(url, headers=headers)

        return resp

    def post(self, url, headers={}, body=''):
        headers.update(self.user_agent)
        resp = self.session.post(url, json=body, headers=headers)

        return resp
