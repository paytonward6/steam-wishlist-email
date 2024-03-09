from pathlib import Path
from typing import Any, Self
import logging
import os


from pydantic import BaseModel, Field, field_validator


class Settings(BaseModel):
    email_address: str = Field(alias="SENDER_EMAIL_ADDRESS")
    email_password: str = Field(alias="SENDER_EMAIL_PASSWORD")

    steam_user_id: int = Field(alias="STEAM_USER_ID")

    is_there_any_deal_key: str = Field(alias="IS_THERE_ANY_DEAL_API_KEY")

    to_addresses: list[str] = Field(alias="EMAIL_TO_ADDRESSES")

    @field_validator("to_addresses", mode="before")
    @classmethod
    def validate_to_addresses(cls, v: Any):
        return [address.strip() for address in v.split(",")]

    @classmethod
    def create(cls, secrets_dir="/run/secrets", env_file=".env") -> Self:
        settings = {}

        # Read all secrets under secrets_dir
        secrets_path = Path(secrets_dir)
        try:
            for file in os.listdir(secrets_path):
                current_file = secrets_path/file
                if current_file.is_dir():
                    continue

                with open(current_file, "r") as file:
                    settings[file] = file.read().strip()

        except Exception:
            logging.debug("Failed to read secrets from '%s'" % secrets_dir)

        # Read all secrets from env file
        env_path = Path(env_file)
        try:
            with open(env_path, "r") as env:
                for line in env.readlines():
                    line = line.strip()
                    if not line:
                        continue

                    name, value = line.split("=", 1)
                    settings[name] = value.strip("\"").strip("\'")
        except Exception:
            logging.debug("Failed to read secrets from env file '%s'" % env_path.absolute())

        # Merge with environment variables
        settings |= os.environ

        return cls.model_validate(settings)

