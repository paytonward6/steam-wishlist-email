FROM docker.io/python:3.12-slim

RUN apt update && apt upgrade -y

COPY ./src/ /app
COPY ./requirements.txt /app

WORKDIR /app

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "-m", "steam_wishlist_api"]
