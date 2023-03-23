import json
from typing import Optional
import csv
import typer

app = typer.Typer()


def file_parse(f) -> dict:
    data = json.load(f)
    results = dict()
    for entry in data:

        fields = entry["fields"]
        pole_id = None
        accuracy = None

        for field in fields:
            if field["field"] == "poleID":
                pole_id = get_pole_id(field)

            if field["field"] == "geographicCoordinate":
                accuracy = get_accuracy(field)

            if pole_id and accuracy:
                results[pole_id] = accuracy

    return results


def get_pole_id(parsable: dict) -> Optional[str]:
    value = parsable.get("value")
    return value


def get_accuracy(parsable: dict) -> Optional[str]:
    value = parsable.get("value")
    accuracy = value.get("accuracy")
    return accuracy


def dict_to_list(results: dict) -> list[list[str, str]]:
    output = []
    for k, v in results.items():
        output.append([k, v])
    return output


def write_csv(name: str, results_list: list[list[str, str]]) -> None:
    with open(f"{name}_PARSED.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["pole_id", "accuracy"])
        writer.writerows(results_list)


@app.command()
def parse(filename: str):
    with open(filename, encoding="utf-8") as f:
        results = file_parse(f)

    list_results = dict_to_list(results)
    write_csv(filename, list_results)
