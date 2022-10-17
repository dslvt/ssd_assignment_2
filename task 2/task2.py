from urls import file_paths, file_names
from os import listdir
from os.path import isfile, join
import pandas as pd

data = None
DATA_PATH = "data/"


def timestamp_calc(df):
    start_timestamp = df["timestamp"].min()
    end_timestamp = df["timestamp"].max()
    return end_timestamp - start_timestamp


def cmd_get_status():
    current_date = data["timestamp"].max()
    cut_off = current_date - pd.offsets.Day(7)
    filtered_df = data[data["timestamp"] > cut_off]

    total_sesstions = filtered_df["session_id"].unique().shape[0]

    timestamps = filtered_df.groupby(by=["client_user_id", "session_id"]).apply(
        timestamp_calc
    )
    timestamps = timestamps.to_frame()

    avg_time = timestamps[0].mean()
    hours_spend = timestamps[0].sum()

    s = "Statistics for the past 7 days:\n"
    s += f"\tTotal sessions : {total_sesstions}\n"
    s += f"\tAverage time spent per session : {avg_time}\n"
    s += f"\tSum of hours spent by all users : {hours_spend}\n"
    print(s)


def cmd_print_summary():
    pass


def cmd_predict_next_session():
    pass


def cmd_fetch_new_data():
    downloaded_files = get_file_names(DATA_PATH)
    idx = len(downloaded_files)

    if idx < 30:
        new_frame = download_file(file_paths[idx], file_names[idx])
        new_frame["timestamp"] = pd.to_datetime(new_frame["timestamp"])

        return new_frame
    else:
        print("All files already downloaded!")


def cmd_get_top_users():
    pass


def cmd_exit():
    pass


def get_file_names(directory):
    return [f for f in listdir(directory) if isfile(join(directory, f))]


def download_file(path, file_name):
    url = "https://drive.google.com/uc?id="
    url_name = url + path.split("/")[-2]
    df = pd.read_csv(url_name)
    df.to_csv(DATA_PATH + file_name)
    return df


if __name__ == "__main__":
    downloaded_file_paths = get_file_names(DATA_PATH)
    print(downloaded_file_paths)
    if len(downloaded_file_paths) == 0:
        data = download_file(file_paths[0], file_names[0])
    else:
        downloaded_files = []
        for file_path in downloaded_file_paths:
            downloaded_files.append(pd.read_csv(DATA_PATH + file_path))
        data = pd.concat(downloaded_files, ignore_index=True)
    data["timestamp"] = pd.to_datetime(data["timestamp"])

    while True:
        print(
            """Choose one operation from below :
                1 : Get status for the past 7 days
                2 : Print user summary
                3 : Predict user next session duration
                4 : Fetch new data and update users data and ML model
                5 : Get top 5 users based on time spent gaming
                6 : Exit program"""
        )

        input_number = int(input())

        if input_number == 1:
            cmd_get_status()
        elif input_number == 2:
            cmd_print_summary()
        elif input_number == 3:
            cmd_predict_next_session()
        elif input_number == 4:
            new_frame = cmd_fetch_new_data()
            data = pd.concat([data, new_frame])
        elif input_number == 5:
            cmd_get_top_users()
        elif input_number == 6:
            cmd_get_status()
            cmd_exit()
            break
        else:
            print("Invalid input command")
