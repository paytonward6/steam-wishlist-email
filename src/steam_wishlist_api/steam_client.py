import logging


import requests
from pydantic import BaseModel, AliasPath, Field, ValidationError


class WishlistItem(BaseModel):
    name: str
    discount_pct: int = Field(validation_alias=AliasPath("subs", 0, "discount_pct"), gt=0)
    discount_block: str = Field(validation_alias=AliasPath("subs", 0, "discount_block"))
    price: str = Field(validation_alias=AliasPath("subs", 0, "price"))


class SteamClient:
    def __init__(self, user_id: int):
        if not isinstance(user_id, int):
            raise TypeError("User ID must be an int")

        self.user_id = user_id
        self.wishlist_url = f"https://store.steampowered.com/wishlist/profiles/{user_id}/wishlistdata"

    def fetch_wishlist(self):
        response = requests.get(self.wishlist_url, headers={"Content-type": "application/json"})

        wishlist: dict[int, WishlistItem] = {}
        for id, item in response.json().items():
            try:
                wishlist[id] = WishlistItem.model_validate(item)
            except ValidationError:
                logging.debug("Failed to validate %s" % item["name"])

        return wishlist

