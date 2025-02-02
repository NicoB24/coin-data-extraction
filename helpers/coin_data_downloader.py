import logging
import requests

from constants.constants import BASE_URL


class CoinDataDownloader:
    def download(self, date: str, coin_id: str) -> dict:
        endpoint = f"/coins/{coin_id}/history"
        url = f"{BASE_URL}{endpoint}?date={date}"

        try:
            print(url)
            response = requests.get(url)
            print(url)
            response.raise_for_status()

            logging.info(f"Data downloaded from  {url}")
            return response.json()

        except requests.exceptions.RequestException as e:
            logging.error(f"Error while doing the request to {url}: {e}")
