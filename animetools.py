# meta developer: @idiotcoders
# scope: hikka_only
# scope: hikka_min 1.2.10

from deep_translator import GoogleTranslator
from typing import Optional

import requests
from telethon.tl.types import Message
from io import BytesIO


from .. import loader, utils


@loader.tds
class animetoolsMod(loader.Module):
    """AnimeTools"""

    strings = {
        "name": "AnimeTools",
        "no_results": "<emoji document_id=5210952531676504517>❌</emoji> No results found!",
        "character": "\n<emoji document_id=5370765563226236970>👤</emoji> <b>Character:</b> <i>{}</i>",
        "quote": "\n<emoji document_id=5465300082628763143>💬</emoji> <b>Quote:</b> <i>{}</i>",
        "anime": "\n<emoji document_id=6334664298710697689>🍿</emoji> <b>Anime:</b> <i>{}</i>",
        "enter_name": "<emoji document_id=5467928559664242360>❗</emoji> <b>You must specify a character name!</b>",
        "description": "\n<emoji document_id=5818865088970362886>ℹ️</emoji> <b>Description:</b> <i>{}</i>",
        "genres": "\n<emoji document_id=5359441070201513074>🎭 </emoji> <b>Genres:</b>  <i>{}</i>"
    }

    strings_ru = {
        "name": "AnimeTools",
        "no_results": "<emoji document_id=5210952531676504517>❌</emoji> Результатов не найдено!",
        "character": "\n<emoji document_id=5370765563226236970>👤</emoji> <b>Персонаж:</b> <i>{}</i>",
        "quote": "\n<emoji document_id=5465300082628763143>💬</emoji> <b>Цитата:</b> <i>{}</i>",
        "anime": "\n<emoji document_id=6334664298710697689>🍿</emoji> <b>Аниме:</b> <i>{}</i>",
        "description": "\n<emoji document_id=5818865088970362886>ℹ️</emoji> <b>Описание:</b>  <i>{}</i>",
        "genres": "\n<emoji document_id=5359441070201513074>🎭 </emoji> <b>Жанры:</b>  <i>{}</i>",
        "enter_name": "<emoji document_id=5467928559664242360>❗</emoji> <b>Вы должны указать имя персонажа!</b>",
        "_cmd_doc_animequote": "Отправляет аниме цитатки",
        "_cmd_doc_animechar": "Отправляет аниме цитатки определенного персонажа",
        "_cmd_doc_animeavailable": "Отправляет список всех доступных аниме на данный момент",
        "_cmd_doc_randomanime": "Отправляет случайное аниме",
        "_cmd_doc_characteravailable": "Отправляет список всех доступных персонажей на данный момент"
    }


    @loader.command(alias="aq")
    async def animequotecmd(self, message: Message):
        """Sends anime quotes"""
        args = utils.get_args_raw(message)
        link = "https://animechan.vercel.app/api/random"
        if args:
            link += "/anime?title={args}"
        qdata = (await utils.run_sync(requests.get, link)).json()

        try:
            qdata["quote"] = GoogleTranslator(source="auto", target="ru").translate(qdata["quote"])
        except KeyError:
            qdata = {"quote": "no_results", "character": "no_results", "anime": "no_results"}

        quote, chr, anime = qdata["quote"], qdata["character"], qdata["anime"]

        if not qdata.get("quote") or "no_results" in [qdata.get("quote"), qdata.get("character"), qdata.get("anime")]:
            await utils.answer(message, self.strings["no_results"])
            return

        quote = (
            self.strings['quote'].format(quote) +
            self.strings['character'].format(chr) +
            self.strings['anime'].format(anime)
        )
        await utils.answer(message, quote)


    @loader.command(alias="ac")
    async def animechar(self, message: Message):
        """Sends anime quotes for specific character"""
        character_name = utils.get_args_raw(message)
        if not character_name:
            await utils.answer(message, self.strings['enter_name'])
            return
        link = f"https://animechan.vercel.app/api/random/character?name={character_name}"
        qdata = (await utils.run_sync(requests.get, link)).json()

        try:
            qdata["quote"] = GoogleTranslator(source="auto", target="ru").translate(qdata["quote"])
        except KeyError:
            qdata = {"quote": "no_results", "character": "no_results", "anime": "no_results"}

        quote, chr, anime = qdata["quote"], qdata["character"], qdata["anime"]

        if not qdata.get("quote") or "no_results" in [qdata.get("quote"), qdata.get("character"), qdata.get("anime")]:
            await utils.answer(message, self.strings["no_results"])
            return

        quote = (
            self.strings['quote'].format(quote) +
            self.strings['character'].format(chr) +
            self.strings['anime'].format(anime)
        )
        await utils.answer(message, quote)


    @loader.command(alias="aa")
    async def animeavailable(self, message: Message):
        """Sends a list of available anime"""
        args = utils.get_args_raw(message)
        link = "https://animechan.vercel.app/api/available/anime"
        response = await utils.run_sync(requests.get, link)
        available_anime = response.json()
        if args:
            matching_anime = [anime for anime in available_anime if args.lower() in anime.lower()]
            if matching_anime:
                anime_message = "\n".join(matching_anime)
            else:
                await utils.answer(message, self.strings["no_results"])
                return
        else:
            anime_message = "\n".join(available_anime)
        await utils.answer(message, anime_message)    


    @loader.command(alias="ca")
    async def characteravailable(self, message: Message):
        """Sends a list of available characters"""
        args = utils.get_args_raw(message)
        link = "https://animechan.vercel.app/api/available/character"
        response = await utils.run_sync(requests.get, link)
        available_anime = response.json()
        if args:
            matching_anime = [anime for anime in available_anime if args.lower() in anime.lower()]
            if matching_anime:
                anime_message = "\n".join(matching_anime)
            else:
                await utils.answer(message, self.strings["no_results"])
                return
        else:
            anime_message = "\n".join(available_anime)
        await utils.answer(message, anime_message)

    @loader.command(alias="ra")
    async def randomanime(self, message: Message):
        """Sends a random anime"""
        link = "https://anime777.ru/api/rand"
        adata = (await utils.run_sync(requests.get, link)).json()
        title = adata["title"]
        genres = ", ".join(adata["material_data"]["anime_genres"])
        description = adata["material_data"]["anime_description"]
        anime_message = f"{self.strings['anime']}<i>{title}\n</i>{self.strings['genres']}<i>{genres}\n</i>{self.strings['description']}<i>{description}</i>"
        await utils.answer(message, anime_message)