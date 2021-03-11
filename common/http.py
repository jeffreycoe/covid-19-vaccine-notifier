import urllib3

class Http:
    user_agent = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.48"
    }

    @classmethod
    def get(cls, url, headers={}, opts={}):
        headers.update(cls.user_agent)
        http = urllib3.PoolManager()
        resp = http.request('GET', url, headers=headers)
        
        return resp
