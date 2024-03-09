from .settings import Settings
from .email_client import EmailClient
from .steam_client import SteamClient
from .deal_client import DealClient

import pandas as pd
from pretty_html_table import build_table


def main():
    settings = Settings.create()
    with EmailClient(settings) as email_client:
        steam_client = SteamClient(settings.steam_user_id)
        deal_client = DealClient(settings.is_there_any_deal_key)

        wishlist = steam_client.fetch_wishlist()

        data = deal_client.process_items(list(wishlist.keys()))

        df = pd.DataFrame(data)
        email_client.send_message("Steam Deals", build_table(df, "green_light"), "html")


if __name__ == "__main__":
    main()
