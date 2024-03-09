from typing import Optional

import requests
from pydantic import Field, BaseModel, AliasPath

from .steam_client import WishlistItem


STEAM_STORE_ID = 61
COUNTRY = "US"


class DealLookup(BaseModel):
    title: str = Field(validation_alias=AliasPath("game", "title"))
    id: str = Field(validation_alias=AliasPath("game", "id"))


class DealPrices(BaseModel):
    id: str
    price: float = Field(validation_alias=AliasPath("deals", 0, "price", "amount"))
    regular: float = Field(validation_alias=AliasPath("deals", 0, "regular", "amount"))
    cut: int = Field(validation_alias=AliasPath("deals", 0, "cut"))
    store_low: float = Field(validation_alias=AliasPath("deals", 0, "storeLow", "amount"))
    expiry: str = Field(validation_alias=AliasPath("deals", 0, "expiry"))


class DealClient:
    def __init__(self, key: str):
        self.key = key
        self.key_header = {"key": self.key}

    def process_item(self, id: int, item: WishlistItem):
        lookup = self.lookup(id)
        return lookup.title, self.prices(lookup.id)

    def lookup(self, id: int):
        response = requests.get("https://api.isthereanydeal.com/games/lookup/v1", params={"appid": id} | self.key_header)
        return DealLookup.model_validate(response.json())

    def prices(self, id: str):
        response = requests.post("https://api.isthereanydeal.com/games/prices/v2", params={"country": COUNTRY, "shops": [STEAM_STORE_ID]} | self.key_header, json=[id])
        return DealPrices.model_validate(response.json()[0])
