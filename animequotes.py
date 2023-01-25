# meta developer: @idiotcoders
# scope: hikka_only
# scope: hikka_min 1.2.10

import asyncio
import functools

import requests
from telethon.tl.types import Message

from .. import loader, utils


async def quotes() -> dict:
    link = "https://animechan.vercel.app/api/random"
    quote_data = (await utils.run_sync(requests.get, link)).json()
    return {"quote": quote_data["quote"], "character": quote_data["character"], "anime": quote_data["anime"]}
                        
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
        """— Send anime quotes"""
        data = await quotes()
        quote, character, anime = data["quote"], data["character"], data["anime"]
        await utils.answer(message, self.strings("quote") + "<i>" + quote + "</i>" + self.strings("character") + "<i>" + character + "</i>" + self.strings("anime") + "<i>" + anime + "</i>")
