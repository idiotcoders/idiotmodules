# meta developer: @idiotcoders
# scope: hikka_only
# scope: hikka_min 1.2.10

import asyncio
import functools
from deep_translator import GoogleTranslator

import requests
from telethon.tl.types import Message

from .. import loader, utils



async def quotes() -> dict:
    link = "https://animechan.vercel.app/api/random"
    quote_data = (await utils.run_sync(requests.get, link)).json()
    quote_data["quote"] = GoogleTranslator(source="auto", target="ru").translate(quote_data["quote"])
    quote_data["character"] = GoogleTranslator(source="auto", target="ru").translate(quote_data["character"])
    return quote_data


@loader.tds
class animequotesMod(loader.Module):
    """Sends anime quotes ☺"""

    strings = {
        "name": "AnimeQuotes",
        "character": "\n<b>👤Character:</b> ",
        "quote": "\n<b>💭Quote:</b> ",
        "anime": "\n<b>🔆Anime:</b> "
    }

    @loader.command()
    async def animequotecmd(self, message: Message):
        """Sends anime quotes"""
        quote_data = await quotes()
        quote, character, anime = quote_data["quote"], quote_data["character"], quote_data["anime"]
        quote_message = f"{self.strings['quote']}<i>{quote}</i>{self.strings['character']}<i>{character}</i>{self.strings['anime']}<i>{anime}</i>"
        await utils.answer(message, quote_message)
