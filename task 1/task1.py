import pickle
import datetime
from os import listdir
from os.path import isfile, join
from xmlrpc.client import DateTime

DATABASE_PATH = "database"
institutions = {}


class EdInstitution:
    def __init__(self, name, classrooms, lectures):
        self.name = name
        self.classrooms = classrooms
        self.lectures = lectures

    def add(self, room, type):
        if type == 1:
            self.classrooms.append(room)
        elif type == 2:
            self.lectures.append(room)
        else:
            print("Given incorrect type of room")

    def remove(self, idx, type):
        if type == 1:
            self.classrooms.remove(idx)
        elif type == 2:
            self.lectures.remove(idx)
        else:
            print("Given incorrect type of room")

    def save_to_file(self):
        with open(f"{DATABASE_PATH}/{self.name}.pickle", "wb") as f:
            pickle.dump(self, f)

    def restore_from_file(self):
        with open(f"{DATABASE_PATH}/{self.name}.pickle", "rb") as f:
            obj = pickle.load(f)

        self.classrooms = obj.classrooms
        self.lectures = obj.lectures

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

    def add_activity_by_room_number(self, activity, room_number):
        for lecture in self.lectures:
            if lecture.get_number() == room_number:
                lecture.append_activity(activity)

        for classroom in self.classrooms:
            if classroom.get_number() == room_number:
                classroom.append_activity(activity)

    def __str__(self) -> str:
        now = datetime.datetime.now()

        available_classrooms = 0
        available_lectures = 0

        for classroom in self.classrooms:
            available_classrooms += 1 - sum(classroom.is_available(now))

        for lectures in self.lectures:
            available_lectures += 1 - sum(lectures.is_available(now))

        s = f"{self.name}\n"
        s += f"Classroom(s) : {len(self.classrooms)}\n"
        s += f"Auditorium(s) : {len(self.lectures)}\n"
        s += f"Status for today (now) : {available_classrooms} available classroom(s) and {available_lectures} available auditorium(s)"
        return s

    def get_full_info(self):
        s = f"{self.name}\n"
        s += "Classrooms: \n"
        for classroom in self.classrooms:
            s += str(classroom)

        for auditorium in self.lectures:
            s += str(auditorium)

        return s


class Room:
    def __init__(self, capacity, number, is_has_air_conditioner, activities):
        self.capacity = capacity
        self.number = number
        self.is_has_air_conditioner = is_has_air_conditioner
        self.activities = activities

        self.check_activities(activities)

    def check_activities(self, activities):
        is_all_activities_in_working_hours = True
        for activity in activities:
            start_time, end_time = activity.get_time_interval()
            is_all_activities_in_working_hours *= Room.is_in_working_hours(start_time)
            is_all_activities_in_working_hours *= Room.is_in_working_hours(end_time)

            assert (
                is_all_activities_in_working_hours
            ), "Activity is not in working hours"

        is_has_overlap = Room.is_activities_overlap(activities)
        assert not is_has_overlap, "Activities overlap"

        return is_all_activities_in_working_hours and not is_has_overlap

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
        self.check_activities(self.activities)

    def get_activities(self):
        return self.activities

    def append_activity(self, activity):
        new_activities = self.activities + [activity]
        if self.check_activities(new_activities):
            self.activities = new_activities

    @staticmethod
    def is_activities_overlap(activities):
        is_has_overlap = False
        for i in range(len(activities)):
            for j in range(len(activities)):
                i_start, i_end = activities[i].get_time_interval()
                j_start, j_end = activities[j].get_time_interval()
                if i != j and (
                    i_start <= j_start <= i_end or j_start <= i_start <= j_end
                ):
                    is_has_overlap = True

        return is_has_overlap

    def is_available(self, time):
        available_activities = []
        for activity in self.activities:
            start_time, end_time = activity.get_time_interval()
            available_activities.append(start_time <= time <= end_time)
        return available_activities

    @staticmethod
    def is_in_working_hours(time):
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
    def __init__(self, capacity, number, is_has_air_conditioner, activities):
        super().__init__(capacity, number, is_has_air_conditioner, activities)

    def __str__(self) -> str:
        s = "Klassroom\n"
        s += super().__str__()
        return s


class LectureAuditorium(Room):
    def __init__(self, capacity, number, is_has_air_conditioner, activities):
        super().__init__(capacity, number, is_has_air_conditioner, activities)

    def __str__(self) -> str:
        s = "Lecture Auditorium\n"
        s += super().__str__()
        return s


def is_institution_exist(name):
    return name in institutions.keys()


def room_builder(type, capacity, number, has_air_conditioner):
    room = None
    if type == 1:
        room = Klassroom(capacity, number, has_air_conditioner, [])
    elif type == 2:
        room = LectureAuditorium(capacity, number, has_air_conditioner, [])
    else:
        print(f"Incorrect type of room: {type}")

    return room


def cmd_add_room():
    while True:
        print("Enter institution name :")
        institution_name = input()
        print("Enter (classroom - 1 or Auditorium - 2):")
        type_of_room = int(input())
        print("Enter (capacity, number, air conditioner- yes/no):")
        capacity, number, has_air_conditioner = input().split(" ")
        print(f"Auditorium succesfully added to {institution_name}")

        if not is_institution_exist(institution_name):
            institutions[institution_name] = EdInstitution(institution_name, [], [])

        room = room_builder(type_of_room, capacity, number, has_air_conditioner)
        institutions[institution_name].add(room, type_of_room)

        print("Add another Auditorium to Innopolis University? (yes/no)")
        continue_condition = input()
        if continue_condition == "no":
            break


def cmd_print_summary():
    while True:
        print("Enter institution name :")
        institution_name = input()

        if institution_name in institutions.keys():
            print(institutions[institution_name])
        else:
            print(f"Instituion {institution_name} not found!")

        print("Print another institution summary? (yes/no)")
        continue_condition = input()
        if continue_condition == "no":
            break


def cmd_assign_activity_to_classroom():
    while True:
        print("Enter institution name :")
        institution_name = input()

        if institution_name in institutions.keys():
            print("Enter activity name :")
            activity_name = input()
            print("Enter time interval: (10:00-11:30)")
            time_interval = input()
            start_time, end_time = time_interval.split("-")
            s_hour, s_min = start_time.split(":")
            e_hour, e_min = end_time.split(":")
            start_time = datetime.time(int(s_hour), int(s_min), 0)
            end_time = datetime.time(int(e_hour), int(e_min), 0)

            activity = Activity(activity_name, start_time, end_time)
            institution = institutions[institution_name]

            print("Enter room number:")
            room_number = input()
            institution.add_activity_by_room_number(activity, room_number)
            print("Activity succesfully added!")
        else:
            print(f"Instituion {institution_name} not found!")

        print("Add another another activity to room? (yes/no)")
        continue_condition = input()
        if continue_condition == "no":
            break


def cmd_assign_activity_to_lecture_auditorium():
    pass


def cmd_exit():
    save_institutions()

    print("In database you have :")
    for institution in institutions.values():
        print(institution)
        print()


def restore_institutions():
    files = [f for f in listdir(DATABASE_PATH) if isfile(join(DATABASE_PATH, f))]
    files = [file.split(".")[0] for file in files]

    for file in files:
        institution = EdInstitution(file, [], [])
        institution.restore_from_file()
        institutions[file] = institution


def save_institutions():
    for inst in institutions.values():
        inst.save_to_file()


def cmd_get_institution_full_info():
    while True:
        print("Enter institution name :")
        institution_name = input()

        if institution_name in institutions.keys():
            print(institutions[institution_name].get_full_info())
        else:
            print(f"Instituion {institution_name} not found!")

        print("Print another institution info? (yes/no)")
        continue_condition = input()
        if continue_condition == "no":
            break


if __name__ == "__main__":
    restore_institutions()

    while True:
        print(
            """Choose one one operation from below :
                1 : Add classroom or Auditorium to institution
                2 : Print institution summary
                3 : Get institution full info
                4 : Assign activity to classroom
                5 : Assign activity to LectureAuditorium
                6 : Exit program"""
        )

        input_number = int(input())

        if input_number == 1:
            cmd_add_room()
        elif input_number == 2:
            cmd_print_summary()
        elif input_number == 3:
            cmd_get_institution_full_info()
        elif input_number == 4:
            cmd_assign_activity_to_classroom()
        elif input_number == 5:
            cmd_assign_activity_to_lecture_auditorium()
        elif input_number == 6:
            cmd_exit()
            break
        else:
            print("Invalid input command")
