FROM docker.io/python:3.12-slim

RUN apt update && apt upgrade -y

COPY ./ /app

WORKDIR /app

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "-m", "src.steam_wishlist_api"]
