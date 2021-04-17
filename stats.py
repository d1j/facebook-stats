def add_to_key(obj, key, add):
    if key not in obj:
        obj[key] = add
    else:
        obj[key] += add


def number_of_messages(messages: list) -> int:
    """
        Returns stats about number of messages each participant has send.
        Also returns totals of the messages sent.
    """
    ret_data = {}
    total = {}

    for message in messages:
        sender = message["sender_name"]

        # Init participant
        if sender not in ret_data:
            ret_data[sender] = {}

        # Total messages
        add_to_key(ret_data[sender], "messages", 1)

        # Number of photos
        if "photos" in message:
            num_photos = len(message["photos"])
            add_to_key(ret_data[sender], "photos", num_photos)

        # Number of videos
        if "videos" in message:
            num_videos = len(message["videos"])
            add_to_key(ret_data[sender], "videos", num_videos)

        # Number of calls
        if message["type"] == "Call":
            add_to_key(ret_data[sender], "calls", 1)
            add_to_key(total, "call_duration", message["call_duration"])

    for name in ret_data:
        for key in ret_data[name]:
            add_to_key(total, key, ret_data[name][key])

    if "_total" not in ret_data:
        ret_data["_total"] = total

    return ret_data
