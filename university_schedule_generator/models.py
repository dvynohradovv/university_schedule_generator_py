from datetime import datetime
import enum
import os


# Enums
class LessonType(enum.Enum):
    LECTURES = "L"
    PRACTICE = "P"
    EXERCISES = "E"

    @staticmethod
    def list():
        return list(map(lambda c: c, LessonType))


# Data structures
class Schedule:
    def __init__(self, *args, **kwargs):
        self.subject = kwargs.get("Subject", None)
        self.type = kwargs.get("Type", None)
        self.lecturer = kwargs.get("Lecturer", None)
        self.classroom = kwargs.get("Classroom", None)
        self.duration = kwargs.get("Duration", None)
        self.groups = kwargs.get("Groups", [])
        if self.groups:
            self.groups = self.groups.split(" ")

    @property
    def raw_groups(self):
        return " ".join(self.groups)

    @property
    def to_json_request(self):
        return {
            "Subject": self.subject,
            "Type": self.type,
            "Lecturer": self.lecturer,
            "Classroom": self.classroom,
            "Duration": self.duration,
            "Groups": self.groups,
        }


class Classroom:
    def __init__(self, *args, **kwargs):
        self.classroom = kwargs.get("Classroom", None)
        self.rooms = kwargs.get("Rooms", [])
        if self.rooms:
            self.rooms = self.rooms.split(" ")

    @property
    def raw_rooms(self):
        return " ".join(self.rooms)


class ScheduleReport:
    def __init__(self, *args, **kwargs):
        self.file_path = kwargs.get("file_path", None)

    @property
    def file_name(self):
        return os.path.basename(self.file_path) if self.file_path else ""

    @property
    def created_at(self):
        date_string = self.file_name.split("|")[2].removesuffix(".xlsx")
        datetime_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return datetime_object


# DB models
