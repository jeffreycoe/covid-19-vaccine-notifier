import requests

class HttpRequest:
    user_agent = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.48"
    }

    @classmethod
    def get(cls, url, headers={}, session=None):
        headers.update(cls.user_agent)

        if session is None:
            resp = requests.get(url, headers=headers)
        else:
            resp = session.get(url, headers=headers)

        return resp

    @classmethod
    def post(cls, url, headers={}, body='', session=None):
        headers.update(cls.user_agent)

        if session is None:
            resp = requests.post(url, json=body, headers=headers)
        else:
            resp = session.post(url, json=body, headers=headers)

        return resp

    @staticmethod
    def session():
        return requests.Session()
