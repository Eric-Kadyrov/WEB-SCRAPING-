import xml.etree.ElementTree as ET
import json


def parse_xml_1():
    tree = ET.parse('cats.xml')
    root = tree.getroot()

    facts = []

    for child in root:
        print(child.tag, child.attrib)
        for grandchild in child:
            if grandchild.tag == 'fact':
                facts.append(grandchild.text)

    with open('cats.txt', mode='w') as f:
        f.write('\n'.join(facts))


def parse_xml_2():
    tree = ET.parse('cats.xml')
    root = tree.getroot()

    facts = []

    for info in root.findall('info'):
        fact = info.find('fact').text
        facts.append(fact)

    with open('cats2.txt', mode='w') as f:
        f.write('\n'.join(facts))


def example_json():
    tree = ET.parse('cats.xml')
    root = tree.getroot()

    facts = []

    for info in root.findall('info'):
        fact = info.find('fact').text
        facts.append({"fact": fact})

    with open('cats.json', mode='w') as f:
        json.dump(facts, f, indent=4)


def read_json():
    with open('cats.json', mode='r') as f:
        data = json.load(f)
        print(data, type(data))


def compare():
    tree = ET.parse('cats.xml')
    root = tree.getroot()

    facts = {}

    for index, info in enumerate(root.findall('info'), 1):
        fact = info.find('fact').text
        facts[index] = {'fact': fact}

    print(type(facts), facts)
    with open('cats.json', mode='w') as f:
        json.dump(facts, f, indent=4)

    with open('cats.json', mode='r') as f:
        new_facts = json.load(f)

    print(type(new_facts), new_facts)

    print(facts == new_facts)


if __name__ == '__main__':
    # parse_xml_1()
    # parse_xml_2()
    # example_json()
    # read_json()
    compare()