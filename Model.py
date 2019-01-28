import json

from db import sessionScope, Model as DBModel, InitialValueSet, ParameterSet
from values import SimulationTypes

class Model:

    @classmethod
    def _getODENamesFromInitialValueSet(cls, initialValueSet):
        """Retrieves the ODE names for a model from the initial values set."""
        return [initialValue.testcd for initialValue in initialValueSet.values]

    @classmethod
    def getModelFromDb(cls, typeAsString, version, initialValueVersion, parameterVersion):
        # Assertions to make sure the arguments are not misused
        assert isinstance(typeAsString, str) and typeAsString in [type.value for type in SimulationTypes]
        assert isinstance(version, int)
        assert isinstance(initialValueVersion, int)
        assert isinstance(parameterVersion, int)

        # translate the type from string into an instance of SimulationTypes.
        type = SimulationTypes(typeAsString)

        # create a session and query additional data from the database
        with sessionScope() as session:
            # get the model
            model = session.query(DBModel) \
                    .filter(DBModel.version == version) \
                    .filter(DBModel.type == type) \
                    .scalar()
            id = model.id
            json = model.json

            # get the initial values
            initialValueSet = session.query(InitialValueSet) \
                    .filter(InitialValueSet.version == initialValueVersion) \
                    .filter(InitialValueSet.type == type) \
                    .scalar()
            initialValueSetId = initialValueSet.id
            odeNames = cls._getODENamesFromInitialValueSet(initialValueSet)

            # get the parameters
            parameterSet = session.query(ParameterSet) \
                    .filter(ParameterSet.version == parameterVersion) \
                    .filter(ParameterSet.type == type) \
                    .scalar()
            parameterSetId = parameterSet.id

        # actaully create and return the new Model instance with the data prepared / queried / given.
        return Model(type, id, version, initialValueSetId, parameterSetId, json, odeNames)

    def __init__(self, type, id, version, initialValueSetId, parameterSetId, json, odeNames):
        # Assertions to make sure the arguments are not misused
        assert isinstance(type, SimulationTypes)
        assert isinstance(id, int)
        assert isinstance(version, int)
        assert isinstance(initialValueSetId, int)
        assert isinstance(parameterSetId, int)

        # assign the given arguments to the instance for later use throughout the instance
        self.type = type
        self.id = id
        self.version = version
        self.initialValueSetId = initialValueSetId
        self.parameterSetId = parameterSetId
        self.json = json
        self.odeNames = odeNames

    def isOfType(self, otherType):
        """Checks if this model is the same type as `otherType`.

        Keyword arguments:
            otherType -- the type to compare this models type against
        """
        # if we don't already have an instance of SimulationTypes passed,
        # try to make it one
        if not isinstance(otherType, SimulationTypes):
            otherType = SimulationTypes(otherType)

        # compare the two instances of SimulationTypes against eachother
        return self.type is otherType

    def isAnyOf(self, listOfTypes):
        """Checks if this model is any of the types you pass in as list.

        This function just iterates over the list you pass to it and delegates
        the checking to the `isOfType` method.

        Keyword arguments:
            otherType -- the type to compare this models type against
        """
        # Assertions to make sure the arguments are not misused
        assert isinstance(listOfTypes, list)

        for otherType in listOfTypes:
            # if any of the elements in the list match, we immediately stop and return true
            if self.isOfType(otherType):
                return True

        # if the loop went through without returning, we know there is nothing mathing in it
        # so we return false.
        return False

    def getType(self):
        return self.type

    def getTypeAsString(self):
        return self.type.value

    def getId(self):
        return self.id

    def getVersion(self):
        return self.version

    def getInitialValueSetId(self):
        return self.initialValueSetId

    def getParameterSetId(self):
        return self.parameterSetId

    def updateLocalJsonModel(self):
        with open('Single_Models/json_files/{0}_system.json'.format(self.getTypeAsString()), "w") as f:
            f.write(self.json)

    def getODENames(self):
        return self.odeNames

