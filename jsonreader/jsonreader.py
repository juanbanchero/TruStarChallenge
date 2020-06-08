import json
import logging
import re


class JsonReader:
    def read_json(self, json_string, json_properties):
        """Returns a dict with the accepted arguments"""
        logger = logging.getLogger()
        json_object = json.loads(json_string)
        result = {}
        for prop in json_properties:
            try:
                result[prop] = self.read_json_recursive(json_object, [prop])
            except Exception:
                logger.warning("The inserted command: {command} is incorrect".format(command=prop))

        return result

    def read_json_recursive(self, json_dict, commands):
        """Finds a property in a dict from a list of properties"""
        if not commands:
            return json_dict
        new_list = commands[0].split(".")
        new_command = new_list.pop(0)
        if self.is_array(new_command):
            index = new_command[new_command.find("[") + 1:new_command.find("]")]
            command = re.sub(r"\[([0-9])\]", "", new_command)
            result = json_dict.get(command)[int(index)]
        else:
            result = json_dict.get(new_command)
        return self.read_json_recursive(result, new_list)

    def is_array(self, string):
        return "[" and "]" in string


def main():
    json_test = JsonReader()
    a = '{ "guid": 1234, "content": { "type": "text/html", "entities": ["1.2.3.4", "wannacry", "malware.com"]}, ' \
        '"score": 74, "time": 1574897179 } '
    b = ["guid", "content.entities[0]", "score", "score.sign"]
    print(json_test.read_json(a, b))


if __name__ == "__main__":
    main()
