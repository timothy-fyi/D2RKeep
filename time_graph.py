import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from datetime import datetime, date, timedelta
import os
import yaml


def time_graph():

    file_path = os.path.dirname(__file__)
    current_day = date.today()

    try:
        config_file = open(file_path + "\\config.yaml", "r")
    except FileNotFoundError:
        config_default = {"days_to_review": 7, "set_timeout": 5}
        with open(file_path + "\\config.yaml", "w") as new_config:
            new_config.write("# User Configuration\n\n")
            config_create = yaml.dump(config_default, new_config)
        config_file = open(file_path + "\\config.yaml", "r")

    try:
        play_data_file = open(file_path + "\\graph_data.txt", "r")
    except FileNotFoundError:
        with open(file_path + "\\graph_data.txt", "w") as play_data_file:
            play_data_file.write(str(current_day) + "," + "0" + "\n")

    config = yaml.safe_load(config_file)

    try:
        days_to_review = config["days_to_review"]
    except KeyError:
        print("Error in configuration file. Likely, the \"days_to_review\" line has been renamed or deleted. If you are unable to fix this error, delete \"config.yaml\" and rerun the Time Keeper.")
        quit()

    if isinstance(days_to_review, int):
        pass
    else:
        print("Invalid configuration for days_to_review, please review configuration file and ensure that you are using a whole number.")
        quit()

    try:
        play_data_file = open(file_path + "\\graph_data.txt", "r")
        play_data = pd.read_csv(file_path + "\\graph_data.txt", header=None)
    except pd.errors.ParserError:
        print("Data load error, check \"graph_data.txt\". Ensure each play time has its own line, and that there aren't multiple days/sessions on one line.")
        quit()
    play_data.columns = ["day", "time_played"]
    play_data["time_played"] = play_data["time_played"]/3600  # maybe don"t go by hours?

    # adjust dataframe to capture necessary data
    today = datetime.now().date()
    play_data_daily = play_data.groupby(pd.to_datetime(play_data["day"]).dt.date)["time_played"].sum()
    play_data_daily = play_data_daily.loc[today - pd.Timedelta(days=days_to_review):today]

    plt.title("Diablo 2 Resurrected: Play Time for the Last " + str(days_to_review) + " Days")
    plt.xlabel("day")
    plt.ylabel("time played (hours)")
    try:
        play_data_daily.plot(kind="bar", x=0, y=1)
    except IndexError:
        print("There is no play data specified within your days to review range. Please increase that range in order to see your play data.")
    plt.gcf().set_size_inches(10, 7)
    plt.xticks(rotation=25)

    plt.show()
