import csv
import io
import json


def file_path_csv_to_dict(file_path):
    with open(file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        data = []
        for row in reader:
            data.append(row)
    return data


def file_csv_to_dict(file_bytesio):
    file_bytes = file_bytesio.getvalue()
    file_wrapper = io.TextIOWrapper(
        io.BytesIO(file_bytes), encoding="utf-8", newline=""
    )
    reader = csv.DictReader(file_wrapper)
    data = []
    for row in reader:
        data.append(row)
    return data


def save_as_json(
    dict_data,
    file_path,
):
    with open(file_path, "w") as file:
        json.dump(dict_data, file)
