import datetime
import logging
import asyncio

from helpers.coin_data_downloader import CoinDataDownloader
from helpers.coin_data_storer import LocalDataStorer, DatabaseDataStorer


class CoindDataDownloaderAndStorer:
    def __init__(self, coin_data_storer_type):
        storer_classes = {
            "locally": LocalDataStorer,
            "database": DatabaseDataStorer
        }

        self.coin_data_storer = storer_classes.get(coin_data_storer_type)()

        self.coin_data_downloader = CoinDataDownloader()

    async def download_and_store(self, date: str, coin_id: str) -> None:
        data = self.coin_data_downloader.download(date, coin_id)

        if data:
            self.coin_data_storer.store(data, date, coin_id)

    async def bulk_download_and_store(self, start_date_str: str, end_date_str: str, coin_id: str) -> None:
        start_date = datetime.datetime.strptime(start_date_str, "%d-%m-%Y")
        end_date = datetime.datetime.strptime(end_date_str, "%d-%m-%Y")

        delta = datetime.timedelta(days=1)

        logging.info("Starting bulk processing")
        tasks = []
        while start_date <= end_date:
            formatted_date = str(start_date.strftime("%d-%m-%Y"))
            tasks.append(self.download_and_store(formatted_date, coin_id))
            start_date += delta

        await asyncio.gather(*tasks)
        if isinstance(self.coin_data_storer, DatabaseDataStorer):
            self.coin_data_storer.close_connection()
