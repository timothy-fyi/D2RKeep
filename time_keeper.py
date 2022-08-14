import psutil
from datetime import datetime, date, timedelta
import time
import os
import yaml
import pandas as pd

def time_keeper():

    file_path = os.path.dirname(__file__)
    current_day = date.today()

    try:
        
        try:
            config_file = open(file_path + "\\config.yaml", 'r')
        except FileNotFoundError:
            config_default = {'days_to_review': 7, 'set_timeout': 5}
            with open(file_path + "\\config.yaml", "w") as new_config:
                new_config.write("# User Configuration\n\n")
                config_create = yaml.dump(config_default, new_config)
            config_file = open(file_path + "\\config.yaml", 'r')

        try:
            play_data_file = open(file_path + "\\graph_data.txt", "r")
        except FileNotFoundError:
            with open(file_path + "\\graph_data.txt", "w") as play_data_file:
                play_data_file.write(str(current_day) + "," + "0"  + "\n")

        config = yaml.safe_load(config_file)

        try:
            timeout = config["set_timeout"]
        except KeyError:
            print("Error in configuration file. Likely, the 'set_timeout' line has been renamed or deleted. If you are unable to fix this error, delete 'config.yaml' and rerun the Time Keeper.")
            quit()
        try:
            days_to_review = config["days_to_review"]
        except KeyError:
            print("Error in configuration file. Likely, the 'days_to_review' line has been renamed or deleted. If you are unable to fix this error, delete 'config.yaml' and rerun the Time Keeper.")
            quit()

        if isinstance(timeout, int):
            pass
        else:
            print("Invalid configuration for set_timeout, please review configuration file and ensure that you are using a whole number.")
            quit()
        if isinstance(days_to_review, int):
            pass
        else:
            print("Invalid configuration for days_to_review, please review configuration file and ensure that you are using a whole number.")
            quit()

        try:
            play_data_file = open(file_path + "\\graph_data.txt", "r")
            play_data = pd.read_csv(play_data_file, header=None)
        except pd.errors.ParserError:
            print("Data load error, check 'graph_data.txt'. Ensure each play time has its own line, and that there aren't multiple days/sessions on one line.")
            quit()

        play_data.columns =["day","time_played"]

        # break out into necessary data, x days to review, declared by user
        play_data_selection = play_data.groupby(pd.to_datetime(play_data["day"]).dt.date)["time_played"].sum()
        play_data_selection = play_data_selection.loc[current_day - pd.Timedelta(days=days_to_review):current_day]

        fmt = "%H:%M:%S"
        play_time_sum = play_data['time_played'].sum()
        play_time_convert = time.gmtime(play_time_sum)
        total_play_time = time.strftime(fmt, play_time_convert)

        selected_play_time = play_data_selection.sum()
        selected_play_time_convert = time.gmtime(selected_play_time)
        last_x_play_time = time.strftime(fmt, selected_play_time_convert)

        print(
            "D2R Play Stats:\n" +
            "Total play time: " + total_play_time + "\n" +
            "Last " + str(days_to_review) + " day(s) of play time: " + last_x_play_time + "\n"
            )
        print("Checking for D2R...")

        i=0
        while True:
            d2r_open = "D2R.exe" in (prog.name() for prog in psutil.process_iter())
            if d2r_open == False:
                time.sleep(1)
                i+=1
                # times out after x minutes to free up resources
                if i == timeout * 60:
                    print("D2R not opened within " + str(timeout) + " minute(s), please restart program to log playtime.")
                    quit()
            elif d2r_open == True:
                time_opened = datetime.now().strftime(fmt)
                print("D2R opened at " + time_opened)
                break

        while True:
            d2r_closed = "D2R.exe" in (prog.name() for prog in psutil.process_iter())
            if d2r_closed == True:
                pass
                time.sleep(1)
            elif d2r_closed == False:
                time_closed = datetime.now().strftime(fmt)
                print("D2R closed at " + time_closed)
                break

        # user time played
        time_played = datetime.strptime(time_closed, fmt) - datetime.strptime(time_opened, fmt)

        # time played for graphing purposes
        time_played_seconds = abs(int((datetime.strptime(time_closed, fmt) - datetime.strptime(time_opened, fmt)).total_seconds()))

        # handles instances when play time crosses 12:00 AM threshold
        if time_played.days < 0:
            time_played = timedelta(
                days=0,
                seconds=time_played.seconds,
                microseconds=time_played.microseconds
            )
            # this line added 2/21 to capture possibly graph data correctly when time passes midnight. log captures correctly (see above)
            time_played_seconds = time_played.seconds

        print("D2R time played: " + str(time_played))

        with open(file_path + "\\log.txt", "a") as log:
            log.write(str(current_day) + ": " + str(time_played) + "\n")

        with open(file_path + "\\graph_data.txt", "a") as log:
            log.write(str(current_day) + "," + str(time_played_seconds) + "\n")

    except KeyboardInterrupt:
        print("D2RKeep forced quit.")