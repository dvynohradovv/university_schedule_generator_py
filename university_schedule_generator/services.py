from datetime import datetime
import os
from algorithm.main import run

from university_schedule_generator.forms import GenerateScheduleForm
from university_schedule_generator.models import Classroom, Schedule, ScheduleReport
from university_schedule_generator.settings import BASE_DIR
from university_schedule_generator.utils import (
    file_csv_to_dict,
    file_path_csv_to_dict,
    save_as_json,
)


class PresetService:
    preset_dirpath = os.path.join(
        BASE_DIR, "university_schedule_generator", "data", "preset"
    )
    schedule_path = os.path.join(preset_dirpath, "schedule.csv")
    classrooms_path = os.path.join(preset_dirpath, "classrooms.csv")

    def get_schedule_by_path(self, schedule_path=None):
        if schedule_path is None:
            schedule_path = self.schedule_path
        data_dict = file_path_csv_to_dict(schedule_path)

        return [Schedule(**dict) for dict in data_dict]

    def get_schedule_by_csv_file(self, csv_file):
        data_dict = file_csv_to_dict(csv_file)

        return [Schedule(**dict) for dict in data_dict]

    def get_classrooms_by_path(self, classrooms_path=None):
        if classrooms_path is None:
            classrooms_path = self.classrooms_path
        data_dict = file_path_csv_to_dict(classrooms_path)

        return [Classroom(**dict) for dict in data_dict]

    def get_classrooms_by_csv_file(self, csv_file):
        data_dict = file_csv_to_dict(csv_file)

        return [Classroom(**dict) for dict in data_dict]


class ScheduleReportService:
    def __init__(self) -> None:
        self.preset_service = PresetService()

    schedule_report_dirpath = os.path.join(
        BASE_DIR, "university_schedule_generator", "data", "schedule_report"
    )
    schedule_request_dirpath = os.path.join(
        BASE_DIR, "university_schedule_generator", "data", "schedule_request"
    )

    def get_all(self):
        file_paths = []
        for root, directories, files in os.walk(self.schedule_report_dirpath):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_paths.append(file_path)

        schedule_reports = sorted(
            [ScheduleReport(file_path=fp) for fp in file_paths],
            key=lambda x: x.created_at,
            reverse=True,
        )
        return schedule_reports

    def generate(self, form: GenerateScheduleForm):
        schedule_request_path = self._save_as_json(form)
        workbook_path = run(schedule_request_path)

        return workbook_path

    def _save_as_json(self, form: GenerateScheduleForm):
        preset_schedule_csv_file = form.cleaned_data["preset_schedule_csv_file"]
        preset_classrooms_csv_file = form.cleaned_data["preset_classrooms_csv_file"]

        preset_schedules = self.preset_service.get_schedule_by_csv_file(
            preset_schedule_csv_file.file
        )
        preset_classrooms = self.preset_service.get_classrooms_by_csv_file(
            preset_classrooms_csv_file.file
        )

        schedule_request_dict = {
            "Schedule": [ps.to_json_request for ps in preset_schedules],
            "Classroom": {pc.classroom: pc.rooms for pc in preset_classrooms},
        }
        schedule_request_path = self._get_schedule_request_path(form)

        save_as_json(schedule_request_dict, schedule_request_path)

        return schedule_request_path

    def _get_schedule_request_path(self, form: GenerateScheduleForm):
        preset_schedule_csv_file = form.cleaned_data["preset_schedule_csv_file"]
        preset_classrooms_csv_file = form.cleaned_data["preset_classrooms_csv_file"]

        current_datetime = datetime.now()
        current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        preset_schedule_str = str(preset_schedule_csv_file).removesuffix(".csv")
        filenapreset_classrooms_str = str(preset_classrooms_csv_file).removesuffix(
            ".csv"
        )

        return os.path.join(
            self.schedule_request_dirpath,
            f"{str(preset_schedule_str)}|{str(filenapreset_classrooms_str)}|{current_datetime_str}.json",
        )
