import os
from tempfile import NamedTemporaryFile
from typing import Any

import openpyxl
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views import View

from university_schedule_generator.forms import GenerateScheduleForm
from university_schedule_generator.models import LessonType
from university_schedule_generator.services import PresetService, ScheduleReportService
from university_schedule_generator.settings import BASE_DIR


class GenerateScheduleView(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.schedule_report_service = ScheduleReportService()
        self.preset_service = PresetService()

        self.data = {
            "preset_schedule": self.preset_service.get_schedule_by_path(),
            "preset_classrooms": self.preset_service.get_classrooms_by_path(),
            "lesson_types": LessonType.list(),
        }

    template_name = "university_schedule_generator/index.html"

    def get(self, request):
        data = self.data

        data["form"] = GenerateScheduleForm()
        data["schedule_reports"] = self.schedule_report_service.get_all()

        return render(request, self.template_name, data)

    def post(self, request):
        data = self.data

        print(request.POST)
        form = GenerateScheduleForm(request.POST, request.FILES)
        data["form"] = form

        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            workbook_path = self.schedule_report_service.generate(form)
            data["workbook_fname"] = os.path.basename(workbook_path)

        data["schedule_reports"] = self.schedule_report_service.get_all()

        return render(request, self.template_name, data)


class ScheduleReportView(View):
    def get(self, request, file_name):
        file_location = os.path.join(
            BASE_DIR,
            "university_schedule_generator",
            "data",
            "schedule_report",
            file_name,
        )

        try:
            workbook = openpyxl.load_workbook(file_location)
        except IOError:
            response = HttpResponseNotFound("File doesnt exist")

        with NamedTemporaryFile() as tmp:
            workbook.save(tmp.name)
            tmp.seek(0)
            stream = tmp.read()

        response = HttpResponse(
            content=stream,
            content_type="application/ms-excel",
        )
        response["Content-Disposition"] = f"attachment; filename={file_name}"
        return response
