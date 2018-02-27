from mamba import description, context, it
from expects import expect, equal
from requirement_interpreter import RequirementInterpreter

A_PACKAGE_NAME = 'a_package_name'
A_PACKAGE_VERSION = 'a_package_version'

with description('Requirement Interpreter'):
    with context('Having a requirement with a exact match'):
        with it('returns the package and version'):

            a_requirement = '{}=={}'.format(A_PACKAGE_NAME, A_PACKAGE_VERSION)
            requirement_interpreter = RequirementInterpreter()

            package_name, package_version = requirement_interpreter.parser(a_requirement)

            expect(package_name).to(equal(A_PACKAGE_NAME))
            expect(package_version).to(equal(A_PACKAGE_VERSION))

    with context('having a return (\\n) ending the line'):
        with it('returns the version without the scape returnline'):
            a_requirement = '{}=={}\n'.format(A_PACKAGE_NAME, A_PACKAGE_VERSION)
            requirement_interpreter = RequirementInterpreter()

            package_name, package_version = requirement_interpreter.parser(a_requirement)

            expect(package_name).to(equal(A_PACKAGE_NAME))
            expect(package_version).to(equal(A_PACKAGE_VERSION))
