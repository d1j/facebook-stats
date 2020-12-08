from os import path
import json
import codecs
import sys
from glob import glob


def inGroup(group, name):
    for person in group:
        if person.name == name:
            return True
    return False


def findIndex(group, name):
    for idx, person in enumerate(group):
        if person.name == name:
            return idx
    return None


class Person():
    def __init__(self, name):
        self.name = name
        # Number of given chas to each participant will be stored in this dictionary
        self.gaveCha = {}
        # Number of received chas from each participant will be stored in this dictionary
        self.receivedCha = {}
        self.numMessages = 0
        self.numReceivedCha = 0
        self.numGivenCha = 0

    def return_basic_data(self):
        return "{}\n{}\n{}\n{}\n".format(self.name, self.numMessages,  self.numGivenCha, self.numReceivedCha)

    def return_csv(self):
        return_str = "{},{},{},{}".format(
            self.name, self.numMessages, self.numReceivedCha, self.numGivenCha)

        return_str += ",|"

        for item in sorted(self.receivedCha.items()):
            return_str += ",{}".format(item[1])

        return_str += ",|"

        for item in sorted(self.gaveCha.items()):
            return_str += ",{}".format(item[1])

        return_str += "\n"

        return return_str

    def print_data(self):
        print("Name: {}\nNumber of sent messages: {}\nNum of received chas: {}\nNumber of given chas:{}\n".format(
            self.name, self.numMessages, self.numReceivedCha, self.numGivenCha))

        print("Received chas from participants:")
        for item in sorted(self.receivedCha.items()):
            print("{}: {}".format(item[0], item[1]))

        print("\nGiven chas to participants:")
        for item in sorted(self.gaveCha.items()):
            print("{}: {}".format(item[0], item[1]))
        print("\n------------------------------------------")


def main():
    # Check if path argument is provided
    if len(sys.argv) < 2:
        sys.exit(
            'Too few arguments provided.\nCommand exmaple:\n\tpython3 cha_counter.py <relative path to the specific chat folder>')

    file_path = sys.argv[1]

    # Check if path exists
    if not path.exists(file_path):
        sys.exit('Provided relative path does not exist.')

    pattern = path.join(
        sys.argv[1], '*.json')

    group = []

    for file_name in glob(pattern):
        # Iterate through each *.json file
        with open(file_name) as f:
            data = json.load(f)
            # Check if there are any new participants in the group
            for person in data["participants"]:
                if not inGroup(group, person["name"]):
                    # New participant detected
                    group.append(Person(person["name"]))

            # Add new participants to Person.gaveCha/Person.receivedCha for each Person in group.
            for person in group:
                for per in data["participants"]:
                    if per["name"] not in person.gaveCha:
                        person.gaveCha[per["name"]] = 0
                        person.receivedCha[per["name"]] = 0

            # Iterate through each message in *.json file
            for message in data["messages"]:
                # Increment the sent messages counter
                senderIndex = findIndex(group, message["sender_name"])

                if senderIndex == None:
                    continue

                group[senderIndex].numMessages += 1

                # Search for cha reactions
                if "reactions" in message:
                    for reaction in message["reactions"]:
                        # Unicode for cha reaction
                        if reaction["reaction"] == u"\u00f0\u009f\u0098\u0086":
                            giverName = reaction["actor"]
                            giverIndex = findIndex(group, reaction["actor"])

                            if giverIndex == None:
                                continue

                            # Message sender receives a Cha react from giverName
                            group[senderIndex].numReceivedCha += 1
                            group[senderIndex].receivedCha[giverName] += 1

                            # Actor gives a Cha react to a sender
                            group[giverIndex].numGivenCha += 1
                            group[giverIndex].gaveCha[message["sender_name"]] += 1

    # Find group name
    last_slash_index = file_path.rfind("/") + 1
    group_name = file_path[last_slash_index:]

    file = codecs.open(
        "stats_{}.csv".format(group_name), "w", "iso-8859-1")

    # Constructing and writing header
    header_line = "Participant name,Number of sent messages,Number of received chas,Number of sent chas,|Received chas from"
    for item in sorted(group[0].receivedCha.items()):
        header_line += ",{}".format(item[0])
    header_line += ",|Sent chas to"
    for item in sorted(group[0].gaveCha.items()):
        header_line += ",{}".format(item[0])
    header_line += "\n"
    file.write(header_line)

    # Sort participant list by Person.name
    group.sort(key=lambda person: person.name)

    # Writing data
    for person in group:
        file.write(person.return_csv())
    file.close()

    print("Stats successfully calculated and saved to:\n\tstats_{}.csv".format(group_name))


if __name__ == "__main__":
    main()
