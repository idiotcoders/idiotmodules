#meta developer: @idiotcoders
from .. import loader, utils
import asyncio


class IrisfarmMod(loader.Module):
    """Автоматизирует работу с Iris Chat Manager (автоматическая ферма)"""

    strings = {"name": "Irisfarm"}

    async def farmcmd(self, message):
        """Начинает автоматический фарм. """
        self.set("farm", True)
        while self.get("farm"):
            await message.reply("Ферма")
            await asyncio.sleep(14700)

    async def unfarmcmd(self, message):
        """Выключает автоферму."""
        self.set("farm", False)
        await utils.answer(
            message,
            "❗️ <b>Автоферма выключена.</b>",
        )
