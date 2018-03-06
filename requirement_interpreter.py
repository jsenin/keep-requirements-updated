class RequirementInterpreter(object):
    OPERATOR = "=="

    def parser(self, requirement):
        return requirement.split(self.OPERATOR)
