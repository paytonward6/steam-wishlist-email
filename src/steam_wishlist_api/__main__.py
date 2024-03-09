import signal
import time
import logging
import sys
import os

from .settings import Settings
from .email_client import EmailClient
from .steam_client import SteamClient
from .deal_client import DealClient

import pandas as pd
from pretty_html_table import build_table
import schedule


class SteamWishlistEmailer:
    def __init__(self):
        self.settings = Settings.create()
        self.running = True

    def shutdown(self, *_):
        self.running = False

    def run(self):
        logging.info("Running...")
        with EmailClient(self.settings) as email_client:
            steam_client = SteamClient(self.settings.steam_user_id)
            deal_client = DealClient(self.settings.is_there_any_deal_key)

            wishlist = steam_client.fetch_wishlist()

            data = deal_client.process_items(list(wishlist.keys()))

            df = pd.DataFrame(data)
            email_client.send_message("Steam Deals", build_table(df, "green_light"), "html")


def log_level():
    match os.getenv("LOG_LEVEL"):
        case "DEBUG":
            return logging.DEBUG
        case "WARNING":
            return logging.WARNING
        case "CRITICAL":
            return logging.CRITICAL
        case _:
            return logging.INFO


def main():
    logging.basicConfig(level=log_level(), handlers=[logging.StreamHandler(sys.stdout)])

    steam_wishlist_emailer = SteamWishlistEmailer()
    signal.signal(signal.SIGINT, steam_wishlist_emailer.shutdown)
    signal.signal(signal.SIGTERM, steam_wishlist_emailer.shutdown)

    schedule.every().day.at("07:30:00").do(steam_wishlist_emailer.run)

    logging.info("Entering main loop...")

    while steam_wishlist_emailer.running:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
