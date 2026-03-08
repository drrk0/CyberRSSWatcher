# RSS → Telegram Automation (Docker)

Simple automation service that reads RSS feeds and posts new items to a
Telegram channel using a bot.\
The project runs fully in **Docker** using **docker-compose**.

------------------------------------------------------------------------

## Features

-   Monitor multiple RSS feeds
-   Automatically post new entries to a Telegram channel
-   Fully containerized with Docker
-   Easy configuration via environment variables and secrets

------------------------------------------------------------------------

# Project Structure

    .
    ├── data
    │   └── entries.json          # Stores processed RSS entries
    │
    ├── secrets
    │   └── telegram_token.txt    # Telegram bot token
    │
    ├── utils
    │   └── rss.py                # RSS feed configuration
    │
    ├── .dockerignore
    ├── .gitignore
    ├── Dockerfile                # Docker image definition
    ├── docker-compose.yml        # Docker compose configuration
    ├── entry_manager.py          # Handles RSS entry processing
    ├── main.py                   # Main application entrypoint
    ├── requirements.txt          # Python dependencies

------------------------------------------------------------------------

# Requirements

-   Docker
-   Docker Compose

Install:

https://docs.docker.com/get-docker/

------------------------------------------------------------------------

# Setup

## 1. Telegram Bot Token

Create the file:

    secrets/telegram_token.txt

Paste your **Telegram Bot Token** inside the file.

Example:

    123456789:AAExampleTelegramBotToken

You can obtain a bot token from **@BotFather** on Telegram.

------------------------------------------------------------------------

## 2. Configure Telegram Channel

Open:

    docker-compose.yml

Add your Telegram **Channel ID** in the environment variables:

``` yaml
environment:
  CHANNEL_ID: "-100XXXXXXXXXX"
```

Example:

    CHANNEL_ID="-1001234567890"

Your bot must be **admin of the channel** to send messages.

------------------------------------------------------------------------

# RSS Feed Configuration

RSS feeds are defined in:

    utils/rss.py

Example feeds are already included in the file.

To add a new feed, append a new entry in the format:

    [url, name]

Where:

-   `url` → RSS feed URL
-   `name` → Display name for the source

------------------------------------------------------------------------

# Build and Run

## Build the Docker image

    docker compose build

------------------------------------------------------------------------

## Start the service

    docker compose up -d

This will start the RSS automation container in the background.

------------------------------------------------------------------------

## View Logs

    docker compose logs -f

------------------------------------------------------------------------

## Stop the Service

    docker compose down

------------------------------------------------------------------------

# Updating Feeds

After modifying `utils/rss.py`, rebuild and restart the container:

    docker compose up -d --build

This ensures the updated RSS feed configuration is included in the
Docker image.

------------------------------------------------------------------------

# Notes

-   Example RSS feeds are included to help you get started.
-   Make sure the bot has permission to post messages in your Telegram
    channel.
-   The bot token **must remain inside `secrets/telegram_token.txt`**.

------------------------------------------------------------------------
