import os

from university_schedule_generator.models import Classroom, Schedule
from university_schedule_generator.settings import BASE_DIR
from university_schedule_generator.utils import csv_to_dict


class PresetService:
    preset_dirpath = os.path.join(
        BASE_DIR, "university_schedule_generator", "data", "preset"
    )
    schedule_path = os.path.join(preset_dirpath, "schedule.csv")
    classrooms_path = os.path.join(preset_dirpath, "classrooms.csv")

    def get_schedule(self):
        data_dict = csv_to_dict(self.schedule_path)

        return [Schedule(**dict) for dict in data_dict]

    def get_classrooms(self):
        data_dict = csv_to_dict(self.classrooms_path)

        data = [Classroom(**dict) for dict in data_dict]
        print(data)

        return data
