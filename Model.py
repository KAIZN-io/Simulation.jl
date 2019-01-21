import json

from db import sessionScope, Model as DBModel, InitialValues
from values import SimulationTypes

class Model:

    @classmethod
    def _getJsonFromDb(cls, session, type, version):
        assert isinstance(type, SimulationTypes)
        assert isinstance(version, int)

        q = session.query(DBModel.json) \
                .filter(DBModel.version == version) \
                .filter(DBModel.type == type)

        return q.one()[0]

    @classmethod
    def _getODENamesFromDb(cls, session, type, version):
        assert isinstance(type, SimulationTypes)
        assert isinstance(version, int)

        with sessionScope() as session:
            q = session.query(InitialValues.testcd) \
                    .filter(InitialValues.version == version) \
                    .filter(InitialValues.type == type)

        return [x[0] for x in q.all()]

    @classmethod
    def getModelFromDb(cls, typeAsString, version, initialValueVersion, parameterVersion):
        assert isinstance(typeAsString, str) and typeAsString in [type.value for type in SimulationTypes]
        assert isinstance(version, int)
        assert isinstance(initialValueVersion, int)
        assert isinstance(parameterVersion, int)

        type = SimulationTypes(typeAsString)

        with sessionScope() as session:
            json = cls._getJsonFromDb(session, type, version)
            odeNames = cls._getODENamesFromDb(session, type, initialValueVersion)

        return Model(type, version, initialValueVersion, parameterVersion, json, odeNames)

    def __init__(self, type, version, initialValueVersion, parameterVersion, json, odeNames):
        assert isinstance(type, SimulationTypes)
        assert isinstance(version, int)
        assert isinstance(initialValueVersion, int)
        assert isinstance(parameterVersion, int)

        self.type = type
        self.version = version
        self.initialValueVersion = initialValueVersion
        self.parameterVersion = parameterVersion
        self.json = json
        self.odeNames = odeNames

    def isOfType(self, otherType):
        if not isinstance(otherType, SimulationTypes):
            otherType = SimulationTypes(otherType)
        return self.type is otherType

    def isAnyOf(self, listOfTypes):
        assert isinstance(listOfTypes, list)

        for otherType in listOfTypes:
            if self.isOfType(otherType):
                return True

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

