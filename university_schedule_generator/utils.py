import csv


def csv_to_dict(file_path):
    with open(file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        data = []
        for row in reader:
            data.append(row)
    return data
