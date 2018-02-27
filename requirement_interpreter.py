class RequirementInterpreter(object):
    OPERATOR = "=="

    def parser(self, requirement):
 #        requirement = requirement.replace('\n', '')
        return requirement.split(self.OPERATOR)
