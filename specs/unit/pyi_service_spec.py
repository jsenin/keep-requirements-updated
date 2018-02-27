from mamba import description, context, it 
from expects import expect, equal
from doublex import Spy, when
from doublex_expects import have_been_called_with

from pypi_service import PyPiService
from http_client import HttpClient

A_PACKAGE_NAME = 'a_package_name'
A_PACKAGE_VERSION = 'a_package_version'

with description('PyPi Service'):
    with context('requesting latest version for package'):
        with it('should return a json with property version'):
            a_http_client = Spy(HttpClient)
            a_pypi_info  = {'info': {'version': A_PACKAGE_VERSION}}
            expected_url = _build_expected_url(A_PACKAGE_NAME)
            when(a_http_client).request(expected_url).returns(a_pypi_info)
            pypi_service = PyPiService(a_http_client)

            available_version = pypi_service.last_version_for(A_PACKAGE_NAME)

            expect(available_version).to(equal(A_PACKAGE_VERSION))

def _build_expected_url(package):
    return 'https://pypi.python.org/pypi/{}/json'.format(package)
