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
        print(self.file_path)
        return os.path.basename(self.file_path) if self.file_path else ""


# DB models
