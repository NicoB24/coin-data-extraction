import pytest
from unittest.mock import Mock, mock_open, patch
from helpers.coin_data_storer import LocalDataStorer, DatabaseDataStorer


@pytest.fixture
def local_data_storer():
    return LocalDataStorer()


@pytest.fixture
def db_data_storer():
    with patch("db.postgres_connection.PostgreSQLConnection") as mock_db:
        instance = mock_db.return_value
        instance.connect.return_value = None
        instance.get_session.return_value = Mock()
        yield DatabaseDataStorer()


def test_local_data_storer_store_success(local_data_storer):
    data = {"example": "data"}
    date = "2023-08-27"
    coin_id = "bitcoin"
    expected_filename = f"{date}_{coin_id}.json"

    with patch("builtins.open", mock_open()) as mock_file:
        local_data_storer.store(data, date, coin_id)

        mock_file.assert_called_once_with(expected_filename, "w")


def test_local_data_storer_store_error(local_data_storer):
    data = {"example": "data"}
    date = "2023-08-27"
    coin_id = "bitcoin"

    with patch("builtins.open", side_effect=Exception("File error")):
        with pytest.raises(Exception) as e:
            local_data_storer.store(data, date, coin_id)
            assert str(e.value) == "File error"


def test_db_data_storer_store_success(db_data_storer):
    data = {"id": "bitcoin", "market_data": {"current_price": {"usd": 50000}}}
    date = "27-08-2023"
    coin_id = "bitcoin"

    with patch.object(db_data_storer.session, "execute"), patch.object(db_data_storer.session, "commit"):
        db_data_storer.store(data, date, coin_id)


def test_db_data_storer_store_error(db_data_storer):
    data = {"id": "bitcoin", "market_data": {"current_price": {"usd": 50000}}}
    date = "27-08-2023"
    coin_id = "bitcoin"

    with patch.object(db_data_storer.session, "execute", side_effect=Exception("Database error")), patch.object(db_data_storer.session, "rollback"):
        with pytest.raises(Exception):
            db_data_storer.store(data, date, coin_id)
