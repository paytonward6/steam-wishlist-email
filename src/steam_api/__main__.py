from .settings import Settings
from .email_client import EmailClient
from .steam_client import SteamClient
from .deal_client import DealClient

import pandas as pd


def main():
    settings = Settings.create()
    with EmailClient(settings) as email_client:
        steam_client = SteamClient(settings.steam_user_id)
        deal_client = DealClient(settings.is_there_any_deal_key)

        wishlist = steam_client.fetch_wishlist()

        data = []
        for id, item in wishlist.items():
            title, prices = deal_client.process_item(id, item)
            data.append({"title": title, **prices.model_dump(exclude={"id"})})

        email_client.send_message("Steam Deals", pd.DataFrame(data).to_html(), "html")


if __name__ == "__main__":
    main()
