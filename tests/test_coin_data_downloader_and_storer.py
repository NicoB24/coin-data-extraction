import pytest
from unittest.mock import MagicMock
from helpers.coin_data_downloader_and_storer import CoindDataDownloaderAndStorer


class TestCoinDataDownloaderAndStorer:
    @pytest.fixture
    def mock_coin_data_downloader(self):
        return MagicMock()

    class MockStorer:
        def __init__(self):
            self.store_called = False
            self.close_connection_called = False

        def store(self, data, date, coin_id):
            self.store_called = True

        def close_connection(self):
            self.close_connection_called = True

    @pytest.mark.asyncio
    async def test_download_and_store_success_locally(self, mock_coin_data_downloader):
        mock_coin_data_downloader.download.return_value = {"data": "example"}
        downloader_storer = CoindDataDownloaderAndStorer("locally")
        downloader_storer.coin_data_downloader = mock_coin_data_downloader
        downloader_storer.coin_data_storer = self.MockStorer()

        await downloader_storer.download_and_store("27-08-2023", "bitcoin")

        assert downloader_storer.coin_data_storer.store_called

    @pytest.mark.asyncio
    async def test_download_and_store_no_data_locally(self, mock_coin_data_downloader):
        mock_coin_data_downloader.download.return_value = None
        downloader_storer = CoindDataDownloaderAndStorer("locally")
        downloader_storer.coin_data_downloader = mock_coin_data_downloader
        downloader_storer.coin_data_storer = self.MockStorer()

        await downloader_storer.download_and_store("27-08-2023", "bitcoin")

        assert not downloader_storer.coin_data_storer.store_called

    @pytest.mark.asyncio
    async def test_bulk_download_and_store_locally(self, mock_coin_data_downloader):
        mock_coin_data_downloader.download.return_value = {"data": "example"}
        downloader_storer = CoindDataDownloaderAndStorer("locally")
        downloader_storer.coin_data_downloader = mock_coin_data_downloader
        downloader_storer.coin_data_storer = self.MockStorer()

        await downloader_storer.bulk_download_and_store("27-08-2023", "29-08-2023", "bitcoin")

        assert downloader_storer.coin_data_storer.store_called

    @pytest.mark.asyncio
    async def test_download_and_store_success_database(self, mock_coin_data_downloader):
        mock_coin_data_downloader.download.return_value = {"data": "example"}
        downloader_storer = CoindDataDownloaderAndStorer("database")
        downloader_storer.coin_data_downloader = mock_coin_data_downloader
        downloader_storer.coin_data_storer = self.MockStorer()

        await downloader_storer.download_and_store("27-08-2023", "bitcoin")

        assert downloader_storer.coin_data_storer.store_called

    @pytest.mark.asyncio
    async def test_download_and_store_no_data_database(self, mock_coin_data_downloader):
        mock_coin_data_downloader.download.return_value = None
        downloader_storer = CoindDataDownloaderAndStorer("database")
        downloader_storer.coin_data_downloader = mock_coin_data_downloader
        downloader_storer.coin_data_storer = self.MockStorer()

        await downloader_storer.download_and_store("27-08-2023", "bitcoin")

        assert not downloader_storer.coin_data_storer.store_called

    @pytest.mark.asyncio
    async def test_bulk_download_and_store_database(self, mock_coin_data_downloader):
        mock_coin_data_downloader.download.return_value = {"data": "example"}
        downloader_storer = CoindDataDownloaderAndStorer("database")
        downloader_storer.coin_data_downloader = mock_coin_data_downloader
        downloader_storer.coin_data_storer = self.MockStorer()

        await downloader_storer.bulk_download_and_store("27-08-2023", "29-08-2023", "bitcoin")

        assert downloader_storer.coin_data_storer.store_called
