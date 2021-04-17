import pandas as pd
import json
import os
from glob import glob
from datetime import datetime, date


def read_json(filename: str) -> dict:
    """
        Takes in filename, loads a json containing the file,
        returns as a dict/list.
    """
    if not os.path.isfile(filename):
        print(f'{filename} is not a valid file. Exiting...')
        sys.exit(1)

    with open(filename, "r") as infile:
        data = json.load(infile)
        return data


def load_group_messages(folder_path: str) -> list:
    """
        Takes in folder_path where the Messenger group 
        chats are stored, and returns all messages from the group.
    """
    pattern = os.path.join(folder_path, '*.json')

    messages = []

    for file_name in glob(pattern):

        message_file = read_json(file_name)
        for message in message_file["messages"]:
            # Convert timestamp to local datetime.
            message["date_local"] = datetime.fromtimestamp(
                message["timestamp_ms"]/1000)
            # Change encoding from iso-8859-1 to utf-8
            message["sender_name"] = bytes(
                message["sender_name"], 'iso-8859-1').decode('utf-8')

            messages.append(message)

    return messages


def load_group_reactions_sent(folder_path: str) -> list:
    """
        Takes in folder_path where the Messenger group 
        chats are stored, and returns all reactions 
        that were sent by each participant of the group. 
    """
    messages = load_group_messages(folder_path)
    ret_data = []
    for message in messages:
        if "reactions" in message:
            for reaction in message["reactions"]:
                _reaction = {
                    "participant": bytes(
                        reaction["actor"], 'iso-8859-1').decode('utf-8'),
                    "reaction": reaction["reaction"],
                    "date_local": message["date_local"]
                }
                ret_data.append(_reaction)

    return ret_data


def load_group_reactions_received(folder_path: str) -> list:
    """
        Takes in folder_path where the Messenger group 
        chats are stored, and returns all reactions 
        that were received by each participant of the group. 
    """
    messages = load_group_messages(folder_path)
    ret_data = []
    for message in messages:
        if "reactions" in message:
            for reaction in message["reactions"]:
                _reaction = {
                    "participant": message["sender_name"],
                    "reaction": reaction["reaction"],
                    "date_local": message["date_local"]
                }
                ret_data.append(_reaction)

    return ret_data


def json_serial(obj):
    """
        JSON serializer for objects not serializable by default json code.
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def dump_json(output_data, output_file: str):
    """
        Outputs list/dictionary to a json file.
    """
    with open(output_file, "w") as outfile:
        json.dump(output_data, outfile, default=json_serial)


def output_df_to_csv(df: pd.DataFrame, output_file: str):
    """
        Takes in pd.DataFrame and outputs it to specified output_file.
    """
    print(f"Dumping data to {output_file}...")
    df.to_csv(output_file, sep=',', index=False, encoding="utf-8")
