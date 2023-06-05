from typing import Any

from django.shortcuts import render
from django.views import View

from university_schedule_generator.forms import GenerateScheduleForm
from university_schedule_generator.models import LessonType
from university_schedule_generator.services import PresetService, ScheduleReportService


class GenerateScheduleView(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.report_service = ScheduleReportService()
        self.preset_service = PresetService()

        self.data = {
            "preset_schedule": self.preset_service.get_schedule(),
            "preset_classrooms": self.preset_service.get_classrooms(),
            "lesson_types": LessonType.list(),
        }

    template_name = "university_schedule_generator/index.html"

    def get(self, request):
        data = self.data

        data["form"] = GenerateScheduleForm()
        data["schedule_reports"] = self.report_service.get_all_schedule_reports()

        return render(request, self.template_name, data)

    def post(self, request):
        data = self.data

        form = GenerateScheduleForm(request.POST, request.FILES)
        data["form"] = form

        if form.is_valid():
            csv_file = form.cleaned_data["csv_file"]

        data["schedule_reports"] = self.report_service.get_all_schedule_reports()

        return render(request, self.template_name, data)
