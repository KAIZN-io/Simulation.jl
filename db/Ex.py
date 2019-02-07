from sqlalchemy import Column, String, DateTime, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY, REAL, DOUBLE_PRECISION
import datetime
import uuid
import simplejson as json

from db.base import base
from values import SimulationTypes


# Ex stands for 'Exposure' of an organism with a substance
class Ex(base):
    __tablename__ = 'ex'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    name = Column(String)
    image_path = Column(String)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)

    # every ex has exactly one model
    model_id = Column(Integer, ForeignKey('model.id'), nullable=False)
    model = relationship('Model', back_populates='exs')

    # foreign key referencing the initial value set used in the simulation
    initial_value_set_id = Column(Integer, ForeignKey('initial_value_set.id'), nullable=False)
    initial_value_set = relationship('InitialValueSet', back_populates='exs')

    # foreign key referencing the parameter set used in the simulation
    parameter_set_id = Column(Integer, ForeignKey('parameter_set.id'), nullable=False)
    parameter_set = relationship('ParameterSet', back_populates='exs')

    # relationship to this simulations impulses.
    impulses = relationship('Impulse', back_populates='ex')

    # relationship to the stimuli for this simulation.
    stimuli = relationship('Stimulus', back_populates='ex')

    # every ex has multiple results in the pd table
    pds = relationship('Pd', back_populates='ex')

    # Hog specific values
    hog_signal_type = Column(Integer)
    hog_nacl_impulse = Column(Integer)

    studyid = Column(String)
    domain = Column(String)
    usubjid = Column(String)
    excat = Column(String)
    extrt = Column(String)
    exdose = Column(REAL)
    exdosu = Column(String)
    exstdtc_array = Column(ARRAY(DOUBLE_PRECISION))
    start = Column(DOUBLE_PRECISION)
    stop = Column(DOUBLE_PRECISION)
    step_size = Column(DOUBLE_PRECISION)
    co = Column(String)

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
        return self.model.type is otherType

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
        return self.model.type

    def getTypeAsString(self):
        return self.getType().value

    def getOdeNames(self):
        return [initialValue.testcd for initialValue in self.initial_value_set.values]

    def hasStimuli(self):
        return len(self.stimuli) > 0

    def generate_dict_system_switch(self):
        return {
            'specificInitValuesVersionSEQ': [self.initial_value_set.version],
            'specificModelVersionSEQ': [self.model.version],
            'specificParameterVersionSEQ': [self.parameter_set.version]
        }

    def to_dict(self):
        d = {
            'id': self.id,
            'uuid': str(self.uuid),
            'type': self.getTypeAsString(),
            'start': float(self.start),
            'stop': float(self.stop),
            'step_size': float(self.step_size),
            'impulses': [impulse.to_dict() for impulse in self.impulses],
            'stimuli': [stimulus.to_dict() for stimulus in self.stimuli],
            'model': json.loads(self.model.json),
            'initial_value_set': [initial_value.to_dict() for initial_value in self.initial_value_set.values],
            'parameter_set': [parameter.to_dict() for parameter in self.parameter_set.values],
        }

        if self.isOfType(SimulationTypes.hog):
            d['signal_type'] = self.hog_signal_type
            d['nacl_impulse'] = self.hog_nacl_impulse

        return d

    def to_json_str(self):
        return json.dumps(self.to_dict(), use_decimal=True)

