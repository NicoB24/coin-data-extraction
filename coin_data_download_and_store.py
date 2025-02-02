import argparse
import asyncio
import logging

from helpers.calculate_aggregated_data_from_coin_data import calculate_aggregated_data_from_coin_data
from helpers.coin_data_downloader_and_storer import CoindDataDownloaderAndStorer
from helpers.date_validator import validate_iso8601_date_and_transform, validate_date_range


async def main():
    logging.basicConfig(level=logging.INFO)

    args_parser = argparse.ArgumentParser(description="Date and coin identifier parser")
    args_parser.add_argument("coin_id", type=str, help="Coin identifier")
    args_parser.add_argument("--date", type=str, help="ISO8601 date")
    args_parser.add_argument("--start_date", type=str, help="ISO8601 start date for bulk reprocessing")
    args_parser.add_argument("--end_date", type=str, help="ISO8601 end date for bulk reprocessing")
    args_parser.add_argument("--storage_type", type=str, choices=["locally", "database"], default="locally", help="Type of storager: 'locally' or 'database'")

    args = args_parser.parse_args()

    try:
        if not args.date and (not args.start_date or not args.end_date):
            raise ValueError("Either --date or --start_date and --end_date must be provided.")

        coin_id = args.coin_id

        if args.start_date and args.end_date:
            validate_date_range(args.start_date, args.end_date)
            start_date = validate_iso8601_date_and_transform(args.start_date)
            end_date = validate_iso8601_date_and_transform(args.end_date)

            coin_data_downloader_and_storer = CoindDataDownloaderAndStorer(coin_data_storer_type=args.storage_type)
            await coin_data_downloader_and_storer.bulk_download_and_store(start_date, end_date, coin_id)
        else:
            date = validate_iso8601_date_and_transform(args.date)

            coin_data_downloader_and_storer = CoindDataDownloaderAndStorer(coin_data_storer_type=args.storage_type)
            await coin_data_downloader_and_storer.download_and_store(date, coin_id)

        if args.storage_type == 'database':
            calculate_aggregated_data_from_coin_data(coin_id)

    except ValueError as value_error:
        logging.error(str(value_error))

if __name__ == "__main__":
    asyncio.run(main())
