import data_io as io
import plot
import stats

# def main():
#     start = pd.Timestamp(2019, 8, 1)
#     end = pd.Timestamp(2019, 9, 1)

#     # plot.number_of_messages_per_day('..\\baudykla\\', start, end)

#     plot.number_of_messages_per_day('..\\saulyte\\')


def main():
    # messages = io.load_group_messages("..\\saulyte\\")
    # num_messages = stats.number_of_messages(messages)
    # io.dump_json(num_messages, "num_messages.json")

    # reactions = io.load_group_reactions_received("..\\baudykla\\")
    # io.dump_json(reactions, "reactions_received.json")

    plot.number_of_reactions_per_month("..\\baudykla\\", "received")


if __name__ == "__main__":
    main()
