from datetime import datetime
import dateutil.parser
import time
import uuid
import json
import time
from schema import Schema, And, Use, Optional


schema = Schema({
    '_id': And(str, len),
    '_created_at': And(str, lambda n: dateutil.parser.parse(n)),
    '__type__': 'EQObject'}, ignore_extra_keys=True)

class EQEncoder(json.JSONEncoder):

    def default(self, obj):
        return obj.__dict__


class EQDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        res = None
        
        if '__type__' in obj and obj['__type__'] == 'EQObject':
            o = EQObject()
            o.__dict__ = obj
            res = o
        
        return res


class EQObject:
    
    def __init__(self):
        self._id = uuid.uuid4().hex
        self._created_at = datetime.utcnow().isoformat()
        self.__type__ = self.__class__.__name__
        
    @property
    def id(self):
        return self._id
    
    @property
    def created_at(self):
        return self._created_at

    def json(self, as_string=False):
        obj_json = self.__dict__
        if as_string:
            obj_json = json.dumps(self, cls=EQEncoder, sort_keys=True)

        return obj_json
    
    @staticmethod
    def from_json(obj):
        return EQDecoder().object_hook(schema.validate(obj))
        
    def __str__(self):
        return str(self.__dict__)
        
    def __hash__(self):        
        raise hash()
    
    def __eq__(self, other):
        self.uid == self.uid
    
