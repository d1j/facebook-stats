from datetime import date, datetime
import pandas as pd
import numpy as np
import data_io as io
import matplotlib.pyplot as plt
plt.close("all")


def prepare_data_for_messages_per_period(folder_path: str) -> pd.DataFrame:
    """
    """
    # Load data.
    print("Loading data...")
    data = io.load_group_messages(folder_path)

    # Convert to pd.DataFrame.
    print("Converting data to pd.DataFrame...")
    df = pd.DataFrame(data)

    # Remove unnecessary columns.
    print("Removing unwanted columns...")
    remove_columns = ["videos", "photos", "reactions", "gifs", "share", "files",
                      "audio_files", "call_duration", "sticker", "users"]
    for column in remove_columns:
        try:
            df.pop(column)
        except KeyError:
            print(f"Failed to drop {column} column")

    # Drop duplicate rows.
    print("Dropping duplicate rows...")
    df = df.drop_duplicates()

    # Drop entries where messages were unsent.
    print("Dropping unsent messages...")
    df = df.drop(df[df.is_unsent].index)

    # Format datetimes.
    print("Formatting datetimes by removing time...")
    # Normalize dates so that HH:MM:SS are set to 00:00:00.
    df['date_local'] = df['date_local'].dt.normalize()

    return df


def group_data_for_messages_per_period(df: pd.DataFrame,
                                       from_date: pd.Timestamp,
                                       to_date: pd.Timestamp,
                                       period_days: int,
                                       period_months: int) -> pd.DataFrame:
    """
    """
    # Group data by sender name and date.
    print("Grouping data by sender name and date...")
    df1 = pd.DataFrame({'count': df.groupby(
        ["sender_name", "date_local"]).size()}).reset_index()

    # Prepare dates of the range we will extract data from.
    if not from_date:
        min_date = df1.date_local.min()
    else:
        min_date = from_date
    if not to_date:
        max_date = df1.date_local.max()
    else:
        max_date = to_date

    # Remove out of bound dates.
    df1 = df1[((df1.date_local >= min_date) & (df1.date_local <= max_date))]

    # Find distinct participants.
    participants = df1.sender_name.unique()

    # Ensure data continuity that there is a record for each day from min_date to max_date.
    print("Ensuring data continuity for each participant...")
    while min_date <= max_date:
        for participant in participants:
            # Check if entry for the min_date exists.
            if not ((df1.sender_name == participant) & (df1.date_local == min_date)).any():
                # Append new entry
                df1.loc[len(df1.index)] = [participant, min_date, 0]
        min_date += pd.DateOffset(months=period_months, days=period_days)

    df1 = df1.sort_values(by=["date_local"])

    return df1


def plot_messages_per_period(df: pd.DataFrame, period: str):
    """
        period is in ["day", "month"]
    """
    plt.close("all")
    participants = df.sender_name.unique()
    for participant in participants:
        _df = df.loc[df["sender_name"] == participant]

        x = _df['date_local']
        y = _df['count']

        plt.plot(x, y, label=participant)

    plt.ylabel(f'Number of messages per {period}')
    plt.grid(color='lightgrey', linestyle='--', linewidth=1)
    plt.legend()
    plt.show()


def number_of_messages_per_month(folder_path: str, from_date=None, to_date=None):
    """
        Reads Messenger data from specified folder and
        plots the number of messages each participant sent per month.
    """
    df = prepare_data_for_messages_per_period(folder_path)

    # Set all date days to 1.
    df['date_local'] = df['date_local'].apply(lambda dt: dt.replace(day=1))

    df1 = group_data_for_messages_per_period(
        df, from_date, to_date, period_days=0, period_months=1)

    plot_messages_per_period(df1, "month")


def number_of_messages_per_day(folder_path: str, from_date=None, to_date=None):
    """
        Reads Messenger data from specified folder and
        plots the number of messages each participant sent per day.
    """
    df = prepare_data_for_messages_per_period(folder_path)

    df1 = group_data_for_messages_per_period(
        df, from_date, to_date, period_days=1, period_months=0)

    plot_messages_per_period(df1, "day")

# ---------------- # ---------------- # ---------------- #

# ---------------- # ---------------- # ---------------- #


def prepare_data_for_rections_per_period(data: list) -> pd.DataFrame:
    """
        Converts list to pd.DataFrame, removes duplicate entries and 
        normalizes dates by removing time part of the date. 
    """
    # Convert list to dataframe
    df = pd.DataFrame(data)

    # Drop duplicate rows.
    print("Dropping duplicate rows...")
    df = df.drop_duplicates()

    print("Formatting datetimes by removing time...")
    # Normalize dates so that HH:MM:SS are set to 00:00:00.
    df['date_local'] = df['date_local'].dt.normalize()

    return df


def group_data_for_reactions_per_period(df: pd.DataFrame,
                                        from_date: pd.Timestamp,
                                        to_date: pd.Timestamp,
                                        period_days: int,
                                        period_months: int) -> pd.DataFrame:
    """
    """
    # Group data by sender name and date.
    print("Grouping data by participant and date...")
    df1 = pd.DataFrame({'count': df.groupby(
        ["participant", "date_local"]).size()}).reset_index()

    # Prepare dates of the range we will extract data from.
    if not from_date:
        min_date = df1.date_local.min()
    else:
        min_date = from_date
    if not to_date:
        max_date = df1.date_local.max()
    else:
        max_date = to_date

    # Remove out of bound dates.
    df1 = df1[((df1.date_local >= min_date) & (df1.date_local <= max_date))]

    # Find distinct participants.
    participants = df1.participant.unique()

    # Ensure data continuity that there is a record for each day from min_date to max_date.
    print("Ensuring data continuity for each participant...")
    while min_date <= max_date:
        for participant in participants:
            # Check if entry for the min_date exists.
            if not ((df1.participant == participant) & (df1.date_local == min_date)).any():
                # Append new entry
                df1.loc[len(df1.index)] = [participant, min_date, 0]
        min_date += pd.DateOffset(months=period_months, days=period_days)

    df1 = df1.sort_values(by=["date_local"])

    return df1


def plot_reactions_per_period(df: pd.DataFrame, period: str, switch: str):
    """
        period is in ["day", "month"]
        switch is in ["received, sent]
    """
    plt.close("all")
    participants = df.participant.unique()
    for participant in participants:
        _df = df.loc[df["participant"] == participant]

        x = _df['date_local']
        y = _df['count']

        plt.plot(x, y, label=participant)

    plt.ylabel(f'Number of {switch} reactions per {period}')
    plt.grid(color='lightgrey', linestyle='--', linewidth=1)
    plt.legend()
    plt.show()


def number_of_reactions_per_day(folder_path: str, switch: str, from_date=None, to_date=None):
    """
        Reads Messenger data from specified folder and
        plots the number of reactions each participant `swtich`[sent|received] per day.
    """
    # Load reactions.
    if switch == "sent":
        data = io.load_group_reactions_sent(folder_path)
    elif switch == "received":
        data = io.load_group_reactions_received(folder_path)
    else:
        print(
            f'Bad switch parameter provided: {switch}.\n'
            f'Please provide one of the valid parameters: [sent|received]')

    # Prepare data.
    df = prepare_data_for_rections_per_period(data)

    # Group data.
    df1 = group_data_for_reactions_per_period(
        df, from_date, to_date, period_days=1, period_months=0)

    # Plot data.
    plot_reactions_per_period(df1, "day", switch)


def number_of_reactions_per_month(folder_path: str, switch: str, from_date=None, to_date=None):
    """
        Reads Messenger data from specified folder and
        plots the number of reactions each participant `swtich`[sent|received] per day.
    """
    # Load reactions.
    if switch == "sent":
        data = io.load_group_reactions_sent(folder_path)
    elif switch == "received":
        data = io.load_group_reactions_received(folder_path)
    else:
        print(
            f'Bad switch parameter provided: {switch}.\n'
            f'Please provide one of the valid parameters: [sent|received]')

    # Prepare data.
    df = prepare_data_for_rections_per_period(data)
    # Set all date days to 1.
    df['date_local'] = df['date_local'].apply(lambda dt: dt.replace(day=1))

    # Group data.
    df1 = group_data_for_reactions_per_period(
        df, from_date, to_date, period_days=0, period_months=1)

    # Plot data.
    plot_reactions_per_period(df1, "month", switch)


# ---------------- # ---------------- # ---------------- #

# ---------------- # ---------------- # ---------------- #
