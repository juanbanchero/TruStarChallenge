import unittest
from jsonreader.jsonreader import JsonReader


class TestJsonReader(unittest.TestCase):
    def test_read_json(self):
        """Should return a dict with the properties of interest"""
        test_json = '{ "guid": 1234, "content": { "type": "text/html", "entities": ["1.2.3.4", "wannacry", ' \
                    '"malware.com"]}, ' \
                    '"score": 74, "time": 1574897179 } '
        json_properties = ["guid", "content.entities[0]", "score"]
        result = JsonReader().read_json(test_json, json_properties)
        expected_result = {'guid': 1234, 'content.entities[0]': '1.2.3.4', 'score': 74}
        self.assertEqual(result, expected_result)
