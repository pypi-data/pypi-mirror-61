import unittest
from easyqueue.core.base import EQObject

class TestEQObject(unittest.TestCase):

    def setUp(self):
        self.example_eqobject_json = {
            "_id": "9c482525eaa14c3d808de7d1d1a483ed",
            "__type__": "EQObject",
            "_created_at": "2020-02-03T16:57:53.501633"
        }

        self.example_eqobject = EQObject()
        self.example_eqobject.__dict__ = self.example_eqobject_json

    def test_init(self):
        self.assertEqual(self.example_eqobject.id, self.example_eqobject_json["_id"])
        self.assertEqual(type(self.example_eqobject), EQObject)
        self.assertEqual(self.example_eqobject.created_at, self.example_eqobject_json["_created_at"])

    def test_json(self):
        self.assertEqual(self.example_eqobject_json, self.example_eqobject.json())


if __name__ == '__main__':
    unittest.main()