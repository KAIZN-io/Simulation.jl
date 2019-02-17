from values import SimulationTypes


class ModelData:
    """
    A calss to model the initial data for the database

    It stores the type, default parameters and default initial values for a model.
    It is only used to populate the database in order to have values to work with.
    """
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
    """
    A class for modelling default parameters as well as default initial values

    This class works as a wrapper for a single parameter or initial value. Don't
    confuse it with the database models! This class is much simpler, in order to
    make the creation of default parameters or initial values easier to read. It
    is basically a specialised dictionary, tailored to this one task of aiding
    in the definition of default parameters and default initial values.
    """

    # var to count up so that each new value gets a unique precedence value
    # and thus the values can be ordered by precedence
    precedenceCounter = 0

    def __init__(self, testcd, orres, orresu, comment = ''):
        assert isinstance(testcd, str)
        assert type(orres) is float or int or str
        assert isinstance(orresu, str)
        assert isinstance(comment, str)

        self.testcd  = testcd
        self.orres   = orres
        self.orresu  = orresu
        self.comment = comment

        """
        Set the precedence to ensure order of values

        The precedence of a value is set to be able to query these values
        in an oredered fashion from the database and ensure the correct evaluation.
        """
        self.precedence = self.getNextPrecedence()

    @classmethod
    def getNextPrecedence(cls):
        cls.precedenceCounter = cls.precedenceCounter +1
        return cls.precedenceCounter

class ParameterData(ValueData):
    pass

class InitialValueData(ValueData):
    pass

