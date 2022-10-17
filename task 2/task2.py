import pickle
from os import listdir
from os.path import isfile, join

import pandas as pd

from urls import file_names, file_paths

data = None
DATA_PATH = "data/"
SUMMARY_PATH = "reports/"
model = None


def timestamp_calc(df):
    start_timestamp = df["timestamp"].min()
    end_timestamp = df["timestamp"].max()
    return end_timestamp - start_timestamp


def cmd_get_status():
    current_date = data["timestamp"].max()
    cut_off = current_date - pd.offsets.Day(7)
    filtered_df = data[data["timestamp"] > cut_off]

    total_sesstions = filtered_df["session_id"].unique().shape[0]

    timestamps = filtered_df.groupby(by=["session_id"]).apply(timestamp_calc)
    timestamps = timestamps.to_frame()

    avg_time = timestamps[0].mean()
    hours_spend = timestamps[0].sum()

    s = "Statistics for the past 7 days:\n"
    s += f"\tTotal sessions : {total_sesstions}\n"
    s += f"\tAverage time spent per session : {avg_time}\n"
    s += f"\tSum of hours spent by all users : {hours_spend}\n"

    print(s)

    print("Save summary? (yes/no)")
    is_saving_summary = input()
    if is_saving_summary == "yes" or is_saving_summary == "y":
        with open(
            SUMMARY_PATH + f"statistics_last_7_{current_date}" + ".txt", "w"
        ) as f:
            f.write(s)


def cmd_print_summary():
    while True:
        print("Enter user id:")
        user_id = input()
        print("Enter period (dd/mm/yy - dd/mm/yy) :")
        period = input().split()
        start_date = pd.Timestamp(period[0])
        finish_date = pd.Timestamp(period[-1])

        mask = (data["timestamp"] >= start_date) & (data["timestamp"] <= finish_date)
        filtered_data = data.loc[mask]
        is_user_found = (
            filtered_data[filtered_data["client_user_id"] == user_id].shape[0] > 0
        )
        if is_user_found:
            print("User found!")
        else:
            print("User not found!")
            continue

        sess_count = (
            filtered_data.loc[filtered_data["client_user_id"] == user_id]["session_id"]
            .unique()
            .shape[0]
        )

        sess_first = sorted(
            filtered_data.loc[filtered_data["client_user_id"] == user_id][
                "timestamp"
            ].dt.date.unique()
        )[0]

        sess_recent = sorted(
            filtered_data.loc[filtered_data["client_user_id"] == user_id][
                "timestamp"
            ].dt.date.unique()
        )[-1]

        timestamps = filtered_data.groupby(by=["client_user_id", "session_id"]).apply(
            timestamp_calc
        )
        timestamps = timestamps.to_frame()
        avg_timedelta = timestamps.mean(level=0).loc[user_id][0].total_seconds() / 60

        frequent_device = (
            filtered_data.loc[filtered_data["client_user_id"] == user_id]["device"]
            .value_counts(normalize=True)
            .index.values[0]
        )

        used_devices = filtered_data.loc[filtered_data["client_user_id"] == user_id][
            "device"
        ].unique()[0]

        rtt = filtered_data[filtered_data["client_user_id"] == user_id]["RTT"].mean()
        fps = filtered_data[filtered_data["client_user_id"] == user_id]["FPS"].mean()
        dropped_frames = filtered_data[filtered_data["client_user_id"] == user_id][
            "dropped_frames"
        ].mean()
        bitrate = filtered_data[filtered_data["client_user_id"] == user_id][
            "bitrate"
        ].mean()

        current_date = filtered_data["timestamp"].max()
        cut_off = current_date - pd.offsets.Day(7)
        filtered_df = (
            filtered_data[
                (filtered_data["timestamp"] > cut_off)
                & (filtered_data["client_user_id"] == user_id)
            ]
            .groupby(by=["session_id"])
            .apply(timestamp_calc)
        )
        is_super_user = all(filtered_df > pd.Timedelta(60, "m"))

        X_predict = (
            filtered_data[filtered_data["client_user_id"] == user_id]
            .groupby(by="session_id")
            .mean()[["FPS", "RTT", "dropped_frames", "bitrate"]]
            .to_numpy()
        )
        num_bad_sessions = model.predict(X_predict)

        s = f"User with id : {user_id}\n"
        s += f"\tNumber of sessions : {sess_count}\n"
        s += f"\tDate of first session : {sess_first}\n"
        s += f"\tDate of most recent session : {sess_recent}\n"
        s += f"\tAverage time spent per session : {avg_timedelta:.2f} min\n"
        s += f"\tMost frequently used device : {frequent_device}\n"
        s += f"\tUsed devices: {used_devices}\n"
        s += f"\tAverage of:\n"
        s += f"\t\tRound trip time (RTT): {rtt:.2f}\n"
        s += f"\t\tFrames per Second: {fps:.2f}\n"
        s += f"\t\tDropped Frames: {dropped_frames:.2f}\n"
        s += f"\t\tBitrate: {bitrate:.2f}\n"
        s += f"\tTotal number of bad sessions: {sum(num_bad_sessions)}\n"
        s += f"\tEstimated next session time: {timestamps[0].dt.total_seconds().sample().values[0]/60:.2f} min\n"
        s += f"\tSuper user : {is_super_user}"

        print(s)

        print("Save summary ? (yes/no)")
        is_saving_summary = input()
        if is_saving_summary == "yes" or is_saving_summary == "y":
            with open(SUMMARY_PATH + user_id + ".txt", "w") as f:
                f.write(s)

        print("Find another user ? (yes/no)")
        is_another = input()
        if is_another == "no" or is_another == "n":
            break


def cmd_predict_next_session():
    while True:
        print("Enter user id:")
        user_id = input()
        is_user_found = data[data["client_user_id"] == user_id].shape[0] > 0
        if is_user_found:
            print("User found!")
        else:
            print("User not found!")
            continue

        predicted_time = (
            data[data["client_user_id"] == user_id]
            .groupby(by=["session_id"])
            .apply(timestamp_calc)
        ).to_frame().mean().dt.total_seconds().values[0] / 60
        print(f"Predicted next session duration: {predicted_time} min")

        print("Find another user ? (yes/no)")
        is_another = input()
        if is_another == "no" or is_another == "n":
            break


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
    timestamps = data.groupby(by=["client_user_id", "session_id"]).apply(timestamp_calc)
    timestamps = timestamps.to_frame()
    timestamps = timestamps.sum(level=0).sort_values(by=[0], ascending=False)
    print(timestamps.head(5))


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

    model = pickle.load(open("clf.model", "rb"))

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
            break
        else:
            print("Invalid input command")
