# meta developer: @idiotcoders
# scope: hikka_only
# scope: hikka_min 1.2.10

import asyncio
import functools

import requests
from telethon.tl.types import Message

from .. import loader, utils


async def photo(nsfw: bool):
    try:
        link = "https://api.lolicon.app/setu/v2"
        if nsfw:
            link += "?r18=1"
        img = (
            await utils.run_sync(
                requests.get,
                link
            )
        ).json()
        if img["error"] == "":
            return img["data"][0]["urls"]["original"]

    except:
        return (await photo(nsfw))
                        
@loader.tds
class loliMod(loader.Module):
    """Sends cute anime girl pictures"""

    strings = {"name": "loli"}
    strings_ru = {"_cls_doc": "Отправляет милые фотографии лолей"}

    @loader.command(
        ru_doc="[nsfw] - Показать лолю",
    )
    async def lolicmd(self, message: Message):
        """[nsfw] - Send loli picture"""
        await self.inline.gallery(
            caption=lambda: f"<i>{utils.ascii_face()}</i>",
            message=message,
            next_handler=functools.partial(
                photo,
                nsfw="nsfw" in utils.get_args_raw(message).lower(),
            ),
            preload=5,
        )
