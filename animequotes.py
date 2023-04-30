# meta developer: @idiotcoders
# scope: hikka_only
# scope: hikka_min 1.2.10

import asyncio
import functools
from deep_translator import GoogleTranslator
from typing import Optional

import requests
from telethon.tl.types import Message

from .. import loader, utils



async def quotes(title: str = None) -> dict:
    link = "https://animechan.vercel.app/api/random"
    if title:
        link += f"/anime?title={title}"
    quote_data = (await utils.run_sync(requests.get, link)).json()
    try:
        quote_data["quote"] = GoogleTranslator(source="auto", target="ru").translate(quote_data["quote"])
    except KeyError:
        return {"quote": "no_results", "character": "no_results", "anime": "no_results"}
    return quote_data

async def get_character_quote(character_name: str) -> dict:
        """Returns random quote data for given character"""
        link = f"https://animechan.vercel.app/api/random/character?name={character_name}"
        response = await utils.run_sync(requests.get, link)
        quote_data = response.json()
        try:
            quote_data["quote"] = GoogleTranslator(source="auto", target="ru").translate(quote_data["quote"])
        except KeyError:
            return {"quote": "no_results", "character": "no_results", "anime": "no_results"}
        return quote_data


@loader.tds
class animequotesMod(loader.Module):
    """Sends anime quotes ☺"""

    strings = {
        "name": "AnimeQuotes",
        "no_results": "<b>❌ | No results found.</b>",
        "character": "\n<b>👤Character:</b> ",
        "quote": "\n<b>💭Quote:</b> ",
        "anime": "\n<b>🔆Anime:</b> "
    }

    @loader.command(alias="aq")
    async def animequotecmd(self, message: Message):
        """Sends random anime quotes or for specific anime"""
        args = utils.get_args_raw(message)
        quote_data = await quotes(title=args)
        quote, character, anime = quote_data["quote"], quote_data["character"], quote_data["anime"]
        quote_message = f"{self.strings['quote']}<i>{quote}</i>{self.strings['character']}<i>{character}</i>"
        if anime:
            quote_message += f"{self.strings['anime']}<i>{anime}</i>"

        if not quote_data.get("quote") or "no_results" in [quote_data.get("quote"), quote_data.get("character"), quote_data.get("anime")]:
            await utils.answer(message, self.strings["no_results"])
            return
        
        await utils.answer(message, quote_message)
    
    @loader.command(alias="ac")
    async def animechar(self, message: Message):
        """Sends random anime quotes for specific character"""
        character_name = utils.get_args_raw(message)
        if not character_name:
            await message.edit("<b>You must specify a character name!</b>")
            return
        quote_data = await get_character_quote(character_name)
        if not quote_data.get("quote") or "no_results" in [quote_data.get("quote"), quote_data.get("character"), quote_data.get("anime")]:
            await utils.answer(message, self.strings["no_results"])
            return
        quote, character, anime = quote_data["quote"], quote_data["character"], quote_data["anime"]
        quote_message = f"{self.strings['quote']}<i>{quote}</i>{self.strings['character']}<i>{character}</i>{self.strings['anime']}<i>{anime}</i>"
        await utils.answer(message, quote_message)

