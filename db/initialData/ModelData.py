from values import SimulationTypes


class ModelData:
    def __init__(self, type, parameters, initialValues):
        assert isinstance(type, SimulationTypes)
        assert all(isinstance(parameter, ParameterData) for parameter in parameters)
        assert all(isinstance(value, InitialValueData) for value in initialValues)

        self.type = type
        self.parameters = parameters
        self.initialValues = initialValues

    def getType(self):
        return self.type

    def getParameters(self):
        return self.parameters

    def getInitialValues(self):
        return self.initialValues

class ValueData:
    def __init__(self, testcd, orres, orresu, comment = ''):
        assert isinstance(testcd, str)
        assert type(orres) is float or int
        assert isinstance(orresu, str)
        assert isinstance(comment, str)

        self.testcd  = testcd
        self.orres   = orres
        self.orresu  = orresu
        self.comment = comment

class ParameterData(ValueData):
    pass

class InitialValueData(ValueData):
    pass

