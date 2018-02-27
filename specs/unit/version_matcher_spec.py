from mamba import description, context, it
from expects import expect, be_false, be_true

from version_matcher import VersionMatcher

A_PACKAGE_VERSION = 'a_package_version'
ANOTHER_PACKAGE_VERSION = 'another_package_version'

with description('Version Matcher'):
    with context('Evaluating greather_than'):
        with before.each:
            self.version_matcher = VersionMatcher()

        with context('having an equal versions'):
            with it('should return false'):

                evaluation = self.version_matcher.greather_than(A_PACKAGE_VERSION, A_PACKAGE_VERSION)

                expect(evaluation).to(be_false)

        with context('having diferent versions'):
            with it('should return true'):

                evaluation = self.version_matcher.greather_than(A_PACKAGE_VERSION, ANOTHER_PACKAGE_VERSION)

                expect(evaluation).to(be_true)
