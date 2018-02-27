class PyPiService(object):
    PYPY_JSON_PACKAGE = 'https://pypi.python.org/pypi/{}/json'

    def __init__(self, http_client):
        self._http_client = http_client

    def _url_for(self, package):
        return self.PYPY_JSON_PACKAGE.format(package)

    def _get_info_version(self, package_info):
        return package_info['info']['version']

    def last_version_for(self, package):
        url = self._url_for(package)
        response = self._http_client.request(url) 
        return self._get_info_version(response)
