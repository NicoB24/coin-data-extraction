import pytest
from unittest.mock import Mock, patch

from constants.constants import BASE_URL
from helpers.coin_data_downloader import CoinDataDownloader


@patch("helpers.coin_data_downloader.requests.get")
def test_successful_download(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"data": "sample_data"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    downloader = CoinDataDownloader()
    result = downloader.download("2023-08-26", "bitcoin")

    assert result == {"data": "sample_data"}
    mock_get.assert_called_once_with(f"{BASE_URL}/coins/bitcoin/history?date=2023-08-26")
    mock_response.json.assert_called_once()


@patch("helpers.coin_data_downloader.requests.get")
def test_failed_request(mock_get):
    mock_get.side_effect = Exception("Request error")

    downloader = CoinDataDownloader()
    with pytest.raises(Exception):
        downloader.download("2023-08-26", "bitcoin")


@patch("helpers.coin_data_downloader.requests.get")
def test_nonexistent_coin_id(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"error": "error message"}
    mock_get.return_value = mock_response

    downloader = CoinDataDownloader()
    downloader.download("2023-08-26", "bitcoin33")

    assert mock_response.status_code == 404
