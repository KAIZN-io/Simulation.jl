import json
import datetime
from schema import SchemaError, Schema, Use, Regex

from values import RFC3339_REGEX, RFC3339_DATE_FORMAT


class Event:
    routing_key = 'event'

    schema = Schema({
        'routing_key': Use(str),
        'emitted_at': Regex(RFC3339_REGEX),
        'payload': Use(dict)
    })

    payload_schema = Schema(Use(dict))

    @classmethod
    def is_valid_payload(cls, payload):
        try:
            cls.payload_schema.validate(payload)
        except SchemaError:
            return False

        return True

    @classmethod
    def is_valid_dict(cls, event_dict):
        # validate whether the dict has the correct event schema
        try:
            cls.schema.validate(event_dict)
        except SchemaError:
            return False

        # make sure it has the matching routing key
        if event_dict['routing_key'] != cls.routing_key:
            return False

        # make sure its payload is correct
        return cls.is_valid_payload(event_dict['payload'])

    @classmethod
    def from_dict(cls, event_dict):
        assert cls.is_valid_dict(event_dict)

        event = cls(event_dict['payload'])
        event.emitted_at = datetime.datetime.strptime(event_dict['emitted_at'], RFC3339_DATE_FORMAT)

        return event

    @classmethod
    def from_str(cls, event_string):
        return cls.from_dict(json.loads(event_string))

    @classmethod
    def get_routing_key(cls):
        return cls.routing_key

    def __init__(self, payload):
        assert self.is_valid_payload(payload)

        self.emitted_at = datetime.datetime.utcnow()
        self.payload = payload

    def get_payload(self):
        return self.payload

    def get_emitted_at(self):
        return self.emitted_at

    def to_dict(self, json_ready=False):
        return {
            'routing_key': self.get_routing_key(),
            'emitted_at': self.emitted_at.strftime(RFC3339_DATE_FORMAT) if json_ready else self.emitted_at,
            'payload': self.payload
        }

    def to_str(self):
        return json.dumps(self.to_dict(json_ready=True))

