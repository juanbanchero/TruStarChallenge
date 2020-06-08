from bs4 import BeautifulSoup
import requests

from jsonreader.jsonreader import JsonReader


def attack_pattern_list(fields_of_interest):
    """Returns a list of dicts with the fields of interest passed from a github repository"""
    source = requests.get('https://github.com/mitre/cti/tree/master/enterprise-attack/attack-pattern').text
    soup = BeautifulSoup(source, 'lxml')
    content_list = soup.find_all("td", class_="content")
    links_list = [item.span.a.text for item in content_list[1:]]
    json_reader = JsonReader()
    result = []

    for link in links_list:
        attack_pattern = requests.get(
            'https://github.com/mitre/cti/tree/master/enterprise-attack/attack-pattern' + '/' + link).text
        content = BeautifulSoup(attack_pattern, 'lxml')
        file = str(content.find('table').text)
        result.append(json_reader.read_json(file, fields_of_interest))
    return result


def main():
    json_test = JsonReader()
    a = '{ "guid": 1234, "content": { "type": "text/html", "entities": ["1.2.3.4", "wannacry", "malware.com"]}, ' \
        '"score": 74, "time": 1574897179 } '
    b = ["guid", "content.entities[0]", "score", "score.sign"]
    print(attack_pattern_list(["id", "objects[0].name", "objects[0].kill_chain_phases"]))


if __name__ == "__main__":
    main()