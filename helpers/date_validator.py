import datetime
import re


def validate_iso8601_date_and_transform(date_str: str) -> str:
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if not date_pattern.match(date_str):
        raise ValueError("Invalid date format, please use ISO8601 format (YYYY-MM-DD).")
    else:
        return format_date(date_str)


def format_date(date_str: str) -> str:
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return str(date_obj.strftime("%d-%m-%Y"))


def validate_date_range(start_date_str: str, end_date_str: str) -> None:
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

    if end_date < start_date:
        raise ValueError("End date should be greater than or equal to the start date")
