import pytest
from helpers.date_validator import validate_iso8601_date_and_transform, validate_date_range


class TestDateValidation:
    def test_valid_date_format(self):
        date_str = "2023-08-26"
        assert validate_iso8601_date_and_transform(date_str) == "26-08-2023"

    def test_invalid_date_format(self):
        date_str = "08-26-2023"
        with pytest.raises(ValueError):
            validate_iso8601_date_and_transform(date_str)

    def test_valid_date_range(self):
        start_date_str = "2023-08-26"
        end_date_str = "2023-08-30"
        validate_date_range(start_date_str, end_date_str)  # Should not raise an exception

    def test_invalid_date_range(self):
        start_date_str = "2023-08-30"
        end_date_str = "2023-08-26"
        with pytest.raises(ValueError):
            validate_date_range(start_date_str, end_date_str)
