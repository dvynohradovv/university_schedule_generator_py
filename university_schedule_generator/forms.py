from django import forms


class GenerateScheduleForm(forms.Form):
    preset_schedule_csv_file = forms.FileField(
        label="Select a preset schedule CSV file", required=True
    )
    preset_classrooms_csv_file = forms.FileField(
        label="Select a preset classrooms CSV file", required=True
    )
