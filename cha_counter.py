from os import path
import json
import codecs
import sys
from glob import glob


def inGroup(group, name):
    for per in group:
        if per.name == name:
            return True
    return False


def findIndex(group, name):
    for num, person in enumerate(group):
        if person.name == name:
            return num
    return -1


class Person():
    def __init__(self, name):
        self.name = name
        # number of given chas to each participant will be stored in this dictionary
        self.gaveCha = {}
        # number of received chas from each participant will be stored in this dictionary
        self.receiveCha = {}
        self.numMessages = 0
        self.numReceivedCha = 0
        self.numGivenCha = 0

    def return_data(self):
        return "{}\n{}\n{}\n{}\n".format(self.name, self.numMessages,  self.numGivenCha, self.numReceivedCha)

    def return_csv(self):
        return "{},{},{},{}\n".format(self.name, self.numMessages, self.numReceivedCha, self.numGivenCha)


def main():
    # check if path argument is provided
    if len(sys.argv) < 2:
        sys.exit(
            'Too few arguments provided.\nCommand exmaple:\n\tpython3 cha_counter.py <relative path to the specific chat folder>')

    # check if path exists
    if not path.exists(sys.argv[1]):
        sys.exit('Provided relative path does not exist.')

    pattern = path.join(
        sys.argv[1], '*.json')

    group = []

    for file_name in glob(pattern):
        # iterate through each *.json file
        with open(file_name) as f:
            data = json.load(f)
            # check if there are any new participants in the group
            for person in data["participants"]:
                if not inGroup(group, person["name"]):
                    # new participant detected
                    group.append(Person(person["name"]))

            for person in group:
                for per in data["participants"]:
                    if per["name"] not in person.gaveCha:
                        person.gaveCha[per["name"]] = 0
                        person.receiveCha[per["name"]] = 0

            for message in data["messages"]:
                # increment the sent messages counter
                senderIndex = findIndex(group, message["sender_name"])
                group[senderIndex].numMessages += 1

                # search for cha reactions
                if "reactions" in message:
                    for reaction in message["reactions"]:
                        if reaction["reaction"] == u"\u00f0\u009f\u0098\u0086":
                            giverIndex = findIndex(group, reaction["actor"])
                            giverName = group[giverIndex].name
                            group[senderIndex].numReceivedCha += 1
                            group[senderIndex].receiveCha[giverName] += 1

                            group[giverIndex].numGivenCha += 1
                            group[giverIndex].gaveCha[message["sender_name"]] += 1
            file = codecs.open(
                "stats.csv", "w", "iso-8859-1")
            for person in group:
                file.write(person.return_csv())
            file.close()


if __name__ == "__main__":
    main()
