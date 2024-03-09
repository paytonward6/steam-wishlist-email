from collections.abc import Sequence
from typing import Any

import requests
from pydantic import Field, BaseModel, AliasPath

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

    def process_items(self, ids: Sequence[int]):
        items: dict[str, dict[str, Any]] = {}

        for id in ids:
            item = self.lookup(id)
            items[item.id] = {"title": item.title}

        prices = self.prices(list(items.keys()))

        for price in prices:
            items[price.id] |= price.model_dump(exclude={"id"})

        return list(items.values())

    def lookup(self, id: int):
        response = requests.get("https://api.isthereanydeal.com/games/lookup/v1", params={"appid": id} | self.key_header)
        return DealLookup.model_validate(response.json())

    def prices(self, ids: Sequence[str]):
        response = requests.post("https://api.isthereanydeal.com/games/prices/v2", params={"country": COUNTRY, "shops": [STEAM_STORE_ID]} | self.key_header, json=ids)

        to_return: list[DealPrices] = []
        for item in response.json():
            to_return.append(DealPrices.model_validate(item))

        return to_return
