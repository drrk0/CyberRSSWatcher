import json
import asyncio
import aiohttp
import feedparser
from telegram import Bot
from telegram.helpers import escape_markdown
from entry_manager import EntryManager
from utils import rss_feed_list
import os
import logging

CHECK_INTERVAL = 60

CHANNEL_ID = os.getenv("CHANNEL_ID")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def read_secret(path):
    with open(path, "r") as f:
        return f.read().strip()

async def fetch_feed(session, url):
    async with session.get(url, headers=HEADERS) as response:
        response.raise_for_status()
        content = await response.read()
        return feedparser.parse(content)

def format_entry_message(entry, source):

    title = escape_markdown(entry.get("title", "No title"), version=2)
    published = escape_markdown(entry.get("published", entry.get("updated", "")), version=2)
    link = entry.get("link", "")

    if source == "TrendMicro":
        summary = escape_markdown(entry.get("summary", ""), version=2)
        msg = f"*{escape_markdown(source, version=2)}*\n\n*{title}*\nPublished: {published}\n\n{summary}\n\n[Read more]({link})"
    else:
        msg = f"*{escape_markdown(source, version=2)}*\n\n*{title}*\nPublished: {published}\n\n[Read more]({link})"

    return msg

async def post_new_entries(bot, feed, manager):
    for entry in reversed(feed.entries):
        entry_id = entry.get("link")
        if entry_id not in manager.entries:
            manager.add_entry_id(entry_id)
            message = format_entry_message(entry, source=manager.source)
            try:
                await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=message,
                    parse_mode="MarkdownV2",
                    disable_web_page_preview=False
                )
                logger.info(f"[{manager.source}] Posted new entry: {entry.get('title')}")
                await asyncio.sleep(3)
            except Exception as e:
                logger.error(f"[{manager.source}] Error posting entry: {e}")

async def monitor_feed():
    bot = Bot(token=TELEGRAM_TOKEN)
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        managers = {} 
        while True:
            for url, source in rss_feed_list:
                if source not in managers:
                    managers[source] = EntryManager("/app/data/entries.json", source)

                manager = managers[source]

                try:
                    feed = await fetch_feed(session, url)
                    await post_new_entries(bot, feed, manager)
                except Exception as e:
                    logger.error(f"Error fetching feed {source}: {e}")

            await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    logger = logging.getLogger(__name__)
    TELEGRAM_TOKEN = read_secret("/run/secrets/telegram_token")
    asyncio.run(monitor_feed())