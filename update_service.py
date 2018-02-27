class UpdateService(object):

    def __init__(self, requirement_interpreter, version_matcher, package_service):
        self.requirement_interpreter = requirement_interpreter
        self.version_matcher = version_matcher
        self.package_service = package_service

    def _find_updates(self, requirement):
        try:
            package_name, package_version = self.requirement_interpreter.parser(requirement)
            available_version = self.package_service.last_version_for(package_name)
            if self.version_matcher.greather_than(available_version, package_version):
                return {'package_name': package_name,
                        'current_version': package_version,
                        'available_version': available_version}
        except Exception as e:
            print ("Error with requirement {}: {}".format(requirement, e))


    def remove_returns(self, requirements):
        for index, requirement in enumerate(requirements):
            requirements[index] = requirement.replace("\n",'')

    def clear_blacklisted(self, requirements):
        for requirement in requirements:
            if requirement.startswith('pkg-resource'):
                requirements.remove(requirement)

    def find_updates_for(self, requirements):
        updates_available = []
        self.remove_returns(requirements)
        self.clear_blacklisted(requirements)
        for requirement in requirements:
            update = self._find_updates(requirement)
            if update:
                updates_available.append(update)
        return updates_available
