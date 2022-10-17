data = None

def cmd_get_status():
    pass


def cmd_print_summary():
    pass


def cmd_predict_next_session():
    pass


def cmd_fetch_new_data():
    pass


def cmd_get_top_users():
    pass


def cmd_exit():
    pass


if __name__ == "__main__":
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
            cmd_fetch_new_data()
        elif input_number == 5:
            cmd_get_top_users()
        elif input_number == 6:
            cmd_exit()
            break
        else:
            print("Invalid input command")
