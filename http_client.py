import urllib.request
import json


class HttpClient(object):

    def _request(self, url):
        with urllib.request.urlopen(url) as response:
            content = response.read().decode()
            return json.loads(content)

    def request(self, url):
        try:
            return self._request(url)
        except Exception as e:
            raise Exception('Could not retrieve {}: {}'.format(url, e))
