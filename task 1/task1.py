import datetime
from tracemalloc import start

institutions = []


class EdInstitution:
    def __init__(self, name, classrooms, lectures):
        self.name = name
        self.classrooms = classrooms
        self.lectures = lectures

    def add_classroom(self, classroom):
        self.classrooms.append(classroom)

    def add_lecture(self, lecture):
        self.lectures.append(lecture)

    def remove_classroom(self, idx):
        self.classrooms.remove(idx)

    def remove_lecture(self, idx):
        self.lectures.remove(idx)

    def save_to_file(self):
        pass

    def restore_from_file(self):
        pass

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_classrooms(self, classrooms):
        self.classrooms = classrooms

    def get_classrooms(self):
        return self.classrooms

    def set_lectures(self, lectures):
        self.lectures = lectures

    def get_lectures(self):
        return self.lectures

    def __str__(self) -> str:
        available_classrooms = None
        available_lectures = None

        s = f"{self.name}\n"
        s += f"classrooms : {len(self.classrooms)}\n"
        s += f"Auditorium(s) : {len(self.lectures)}\n"
        s += f"Status for today (now) : {available_classrooms} available classroom(s) and {available_lectures} available auditorium(s)"
        return s


class Room:
    def __init__(self, capacity, number, is_has_air_conditioner, activities):
        self.capacity = capacity
        self.number = number
        self.is_has_air_conditioner = is_has_air_conditioner
        self.activities = activities

    def __str__(self) -> str:
        s = f"Capacity: {self.capacity}\n"
        s += f"Number: {self.number}\n"
        s += f"Has air conditioner {self.is_has_air_conditioner}\n"
        s += f"Activities: [\n"
        for activity in self.activities:
            s += str(activity)
        s += "]\n"
        return s

    def set_capacity(self, capacity):
        self.capacity = capacity

    def get_capacity(self):
        return self.capacity

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_air_conditioner(self, is_has_air_conditioner):
        self.is_has_air_conditioner = is_has_air_conditioner

    def get_air_conditioner(self):
        return self.is_has_air_conditioner

    def set_activities(self, activities):
        self.activities = activities

    def get_activities(self):
        return self.activities

    @staticmethod
    def is_working_hours(time):
        start_working_hours = datetime(8, 0, 0)
        end_working_hours = datetime(21, 0, 0)
        return start_working_hours <= time <= end_working_hours


class Activity:
    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def set_time_interval(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def get_time_interval(self):
        return self.start_time, self.end_time

    def __str__(self) -> str:
        s = f"Activity name: {self.name}\n"
        s += f"Time interval: {self.start_time}:{self.end_time}\n"
        return s


class Klassroom(Room):
    def __init__(self):
        pass

    def __str__(self) -> str:
        s = "Klassroom\n"
        s += super().__str__()
        return s


class LectureAuditorium(Room):
    def __init__(self):
        pass

    def __str__(self) -> str:
        s = "Lecture Auditorium\n"
        s += super().__str__()
        return s


def cmd_add_room():
    while True:
        print("Enter institution name :")
        institution_name = input()
        print("Enter (classroom - 1 or Auditorium - 2):")
        type_of_room = int(input())
        print("Enter (capacity, number, air conditioner- yes/no):")
        capacity, number, has_air_conditioner = input().split(" ")
        print(f"Auditorium succesfully added to {institution_name}")

        print("Add another Auditorium to Innopolis University? (yes/no)")
        continue_condition = input()
        if continue_condition == "no":
            break


def cmd_print_summary():
    pass


def cmd_assign_activity_to_classroom():
    pass


def cmd_assign_activity_to_lecture_auditorium():
    pass


def cmd_exit():
    print("In database you have :")
    for institution in institutions:
        print(institution)


if __name__ == "__main__":
    while True:
        print(
            """Choose one one operation from below :
                1 : Add classroom or Auditorium to institution
                2 : Print institution summary
                3 : Assign activity to classroom
                4 : Assign activity to LectureAuditorium
                5 : Exit program"""
        )

        input_number = int(input())

        if input_number == 1:
            cmd_add_room()
        elif input_number == 2:
            cmd_print_summary()
        elif input_number == 3:
            cmd_assign_activity_to_classroom()
        elif input_number == 4:
            cmd_assign_activity_to_lecture_auditorium()
        elif input_number == 5:
            cmd_exit()
            break
        else:
            print("Invalid input command")
