from mamba import description, context, it
from expects import expect, contain_only, have_keys
from doublex import Spy, when

from update_service import UpdateService
from requirement_interpreter import RequirementInterpreter
from version_matcher import VersionMatcher
from pypi_service import PyPiService

A_PACKAGE_NAME = 'a_package_name'
A_PACKAGE_VERSION = 'a_package_version'
A_PACKAGE_AVAILABLE_VERSION = 'a_package_available_version'

with description('Update Service'):
    with context('Checking for requirement list'):
        with context('having available updates'):
            with it('returns package_name, current_version and available_version'):

                a_requirement = '{}=={}'.format(A_PACKAGE_NAME, A_PACKAGE_VERSION)
                any_requirements = [a_requirement]
                a_requirement_interpreter = Spy(RequirementInterpreter)
                a_version_matcher = Spy(VersionMatcher)
                a_package_service = Spy(PyPiService)
                when(a_requirement_interpreter).parser(a_requirement).returns((A_PACKAGE_NAME, A_PACKAGE_VERSION))
                when(a_package_service).last_version_for(A_PACKAGE_NAME).returns(A_PACKAGE_AVAILABLE_VERSION)
                when(a_version_matcher).greather_than(A_PACKAGE_AVAILABLE_VERSION, A_PACKAGE_VERSION).returns(True)
                update_service = UpdateService(a_requirement_interpreter, a_version_matcher, a_package_service)

                updates_available = update_service.find_updates_for(any_requirements)

                expect(updates_available).to(contain_only(have_keys(package_name=A_PACKAGE_NAME,
                                                                          current_version=A_PACKAGE_VERSION,
                                                                          available_version=A_PACKAGE_AVAILABLE_VERSION)))
