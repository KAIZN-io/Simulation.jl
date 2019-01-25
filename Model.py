import json

from db import sessionScope, Model as DBModel, InitialValues
from values import SimulationTypes

class Model:

    @classmethod
    def _getJsonFromDb(cls, session, type, version):
        """Queries the databse for the JSON that describes the model.

        This functions retrieves the JSON that describes the calculations
        done in the model. The model to query is specified by the type of
        model and a version.

        Keyword arguments:
            session -- a SQL Alchemy session for accessing the database
            type -- the simulation type (hog, ion, volume, combined)
            version -- the version of the model
        """
        # Assertions to make sure the arguments are not misused
        assert isinstance(type, SimulationTypes)
        assert isinstance(version, int)

        # create the query
        q = session.query(DBModel.json) \
                .filter(DBModel.version == version) \
                .filter(DBModel.type == type)

        # exectue the query and directly retrieve the first result
        return q.scalar()

    @classmethod
    def _getODENamesFromDb(cls, session, type, version):
        """Retrieves the ODE names for a model from the database.

        This functions retrieves the ODE names from the initial values table
        for the model. The initial values to query are specified by the type of
        model and the initial value version.

        Keyword arguments:
            session -- a SQL Alchemy session for accessing the database
            type -- the simulation type (hog, ion, volume, combined)
            version -- the version of the initial values
        """
        # Assertions to make sure the arguments are not misused
        assert isinstance(type, SimulationTypes)
        assert isinstance(version, int)

        # create the query
        with sessionScope() as session:
            q = session.query(InitialValues.testcd) \
                    .filter(InitialValues.version == version) \
                    .filter(InitialValues.type == type)

        # query all rows and return the first (and only) column from each of them in a list.
        return [x[0] for x in q.all()]

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
            json = cls._getJsonFromDb(session, type, version)
            odeNames = cls._getODENamesFromDb(session, type, initialValueVersion)

        # actaully create and return the new Model instance with the data prepared / queried / given.
        return Model(type, version, initialValueVersion, parameterVersion, json, odeNames)

    def __init__(self, type, version, initialValueVersion, parameterVersion, json, odeNames):
        # Assertions to make sure the arguments are not misused
        assert isinstance(type, SimulationTypes)
        assert isinstance(version, int)
        assert isinstance(initialValueVersion, int)
        assert isinstance(parameterVersion, int)

        # assign the given arguments to the instance for later use throughout the instance
        self.type = type
        self.version = version
        self.initialValueVersion = initialValueVersion
        self.parameterVersion = parameterVersion
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

    def getVersion(self):
        return self.version

    def getInitialValueVersion(self):
        return self.initialValueVersion

    def getParameterVersion(self):
        return self.parameterVersion

    def updateLocalJsonModel(self):
        with open('Single_Models/json_files/{0}_system.json'.format(self.getTypeAsString()), "w") as f:
            f.write(self.json)

    def getODENames(self):
        return self.odeNames

