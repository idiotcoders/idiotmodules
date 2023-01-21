#meta developer: @dend1yz
from .. import loader, utils
import asyncio


class IrisFarmMod(loader.Module):
    """Автоматизирует работу с Iris Chat Manager (автоматическая ферма)"""

    strings = {"name": "Irisfarm"}

    async def farmcmd(self, message):
        """Начинает автоматический фарм. """
        self.set("farm", True)
        while self.get("farm"):
            await message.reply("Ферма")
            await asyncio.sleep(14700)

    async def unfarmcmd(self, message):
        """какая-то хуйня от Захара"""
        self.set("farm", False)
        await utils.answer(
            message,
            "❗️ <b>Автоферма выключена.</b>",
        )