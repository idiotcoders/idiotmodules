# ---------------------------------------------------------------------------------
# Name: promote
# Description: Promote/demote users
# Author: hikkikomoa
# Commands:
# .promote | .demote | .fullrights
# ---------------------------------------------------------------------------------

# -*- coding: utf-8 -*-

# meta developer: @hikkikomoa

import io
import time

from telethon.errors import (
    ChatAdminRequiredError,
    UserAdminInvalidError,
)
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
)
from telethon.tl.functions.messages import EditChatAdminRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights

from .. import loader, utils

# ================== CONSTANS ========================

DEMOTE_RIGHTS = ChatAdminRights(
    post_messages=None,
    add_admins=None,
    invite_users=None,
    change_info=None,
    ban_users=None,
    delete_messages=None,
    pin_messages=None,
    edit_messages=None,
)

# =====================================================


@loader.tds
class PromoteMod(loader.Module):
    """Promote/demote users"""

    strings = {
        "name": "Promote",
        "promote_none": "<b>🫤 No one to promote.</b>",
        "who": "<b>❓ Who is it?</b>",
        "this_isn`t_a_chat": "<b>🧐 This isn`t a chat!</b>",
        "no_rights": "<b>🫤 I don`t have rights.</b>",
        "no_args": "<b>🫤 Invalid arguments specified.</b>",
        "not_admin": "<b>🤬 I`m not an admin here.</b>",
        "promoted": "<b>🫣 {} promoted to admin rights.\n✍️ Rank: {}</b>",
        "promotedfull": "<b>🫣 {} promoted to admin with full rights.\n✍️ Rank: {}</b>",
        "demote_none": "<b>🤬No one to demote.</b>",
        "demoted": "<b>😂 {} demoted to admin rights. 👎</b>",
    }

    strings_ru = {
        "name": "Promote",
        "promote_none": "<b>🫤 Укажите кого повышать.</b>",
        "who": "<b>❓ Это кто?</b>",
        "this_isn`t_a_chat": "<b>🧐 Это не чат!</b>",
        "no_rights": "<b>🫤 У меня нет прав потому что я ФЕМИНИСТКА!</b>",
        "no_args": "<b>🫤 Указаны неверные аргументы</b>",
        "not_admin": "<b>🤬 Я не админ в этом чате.</b>",
        "promoted": "<b>🫣 {} повышен до администратора.\n✍️ Должность: {}</b>",
        "promotedfull": "<b>🫣 {} повышен до администратора с полными правами.\n✍️ Должность: {}</b>",
        "demote_none": "<b>🤬Укажите кого понижать.</b>",
        "demoted": "<b>😂 С {} сняты права администратора. 👎</b>",
        "_cmd_doc_promote": "Команда .promote для повышения пользователя до администратора.\n Используйте: .promote <@ или ответ> <должность>.",
        "_cmd_doc_demote": "Команда .demote для понижения администратора до пользователя.\n Используйте .demote <@ или ответ>",
        "_cmd_doc_fullrights": "Команда .fullrights для выдачи полный прав администратора.\n Используйте .fullrights <@ или ответ> <долнжость>."
    }

    strings_ua = {
        "name": "Promote",
        "promote_none": "<b>🫤 Вкажіть кого пiдвищувати.</b>",
        "who": "<b>❓ Це хто?</b>",
        "this_isn`t_a_chat": "<b>🧐 Це не чат!</b>",
        "no_rights": "<b>🫤 Я не маю прав, тому що я ФЕМІНІСТКА!</b>",
        "no_args": "<b>🫤 Указані неправильні аргументи. </b>",
        "not_admin": "<b>🤬 Я не адміністратор у цьому чаті.</b>",
        "promoted": "<b>🫣 {} Підвищено до адміністратора.\n✍️ Посада: {}</b>",
        "promotedfull": "<b>🫣 {} Підвищений до адміністратора з повними правами.\n✍️ Посада: {}</b>",
        "demote_none": "<b>🤬Уточніть, кого кого знижувати в посаді.</b>",
        "demoted": "<b>😂 З {} Знятий з прав адміністратора. 👎</b>",
        "_cmd_doc_promote": "Команда .promote для пiдвищення користувача до адміністратора.\n Використовувати: .promote <@ або відповідь> <посада>.",
        "_cmd_doc_demote": "Команда .demote  щоб знизити рівень адміністратора до користувача.\n Використовувати .demote <@ або відповідь>",
        "_cmd_doc_fullrights": "Команда .fullrights для надання повних прав адміністратора.\n Використовувати: .fullrights <@ або відповідь > <посада>."
    }


    async def promotecmd(self, message):
        """Command .promote for promote user to admin rights.\nUse: .promote <@ or reply> <rank>."""
        if not message.chat:
            return await utils.answer(
                message, self.strings("this_isn`t_a_chat", message)
            )
        try:
            args = utils.get_args_raw(message).split(" ")
            reply = await message.get_reply_message()
            rank = "Admin"

            chat = await message.get_chat()
            adm_rights = chat.admin_rights
            if not adm_rights and not chat.creator:
                return await utils.answer(message, self.strings("not_admin", message))

            if reply:
                args = utils.get_args_raw(message)
                rank = args or rank
                user = await message.client.get_entity(reply.sender_id)
            else:
                user = await message.client.get_entity(
                    args[0] if not args[0].isnumeric() else int(args[0])
                )
                if len(args) == 1:
                    rank = rank
                elif len(args) >= 2:
                    rank = utils.get_args_raw(message).split(" ", 1)[1]
            try:
                await message.client(
                    EditAdminRequest(
                        message.chat_id,
                        user.id,
                        ChatAdminRights(
                            change_info=False,
                            post_messages=False,
                            edit_messages=False,
                            delete_messages=False,
                            ban_users=False,
                            invite_users=True,
                            pin_messages=False,
                            add_admins=False,
                            anonymous=False,
                            manage_call=False,
                            other=False
                        ),
                        rank,
                    )
                )
            except ChatAdminRequiredError:
                return await utils.answer(message, self.strings("no_rights", message))
            else:
                return await utils.answer(
                    message,
                    self.strings("promoted", message).format(user.first_name, rank),
                )
        except ValueError:
            return await utils.answer(message, self.strings("no_args", message))

    async def demotecmd(self, message):
        """Command .demote for demote user to admin rights.\nUse: .demote <@ or reply>."""
        if message.is_private:
            return await utils.answer(
                message, self.strings("this_isn`t_a_chat", message)
            )
        try:
            reply = await message.get_reply_message()

            chat = await message.get_chat()
            if not chat.admin_rights and not chat.creator:
                return await utils.answer(message, self.strings("not_admin", message))

            if reply:
                user = await message.client.get_entity(reply.sender_id)
            else:
                args = utils.get_args_raw(message)
                if not args:
                    return await utils.answer(
                        message, self.strings("demote_none", message)
                    )
                user = await message.client.get_entity(
                    args if not args.isnumeric() else int(args)
                )

            try:
                if message.is_channel:
                    await message.client(
                        EditAdminRequest(message.chat_id, user.id, DEMOTE_RIGHTS, "")
                    )
                else:
                    await message.client(
                        EditChatAdminRequest(message.chat_id, user.id, False)
                    )
            except ChatAdminRequiredError:
                return await utils.answer(message, self.strings("no_rights", message))
            else:
                return await utils.answer(
                    message, self.strings("demoted", message).format(user.first_name)
                )
        except ValueError:
            return await utils.answer(message, self.strings("no_args"))

    async def fullrightscmd(self, message):
        """Command .fullrights use it to grant full rights.\nUse: .promote <@ or reply> <rank>."""
        if not message.chat:
            return await utils.answer(
                message, self.strings("this_isn`t_a_chat", message)
            )
        try:
            args = utils.get_args_raw(message).split(" ")
            reply = await message.get_reply_message()
            rank = "Admin"

            chat = await message.get_chat()
            adm_rights = chat.admin_rights
            if not adm_rights and not chat.creator:
                return await utils.answer(message, self.strings("not_admin", message))

            if reply:
                args = utils.get_args_raw(message)
                rank = args or rank
                user = await message.client.get_entity(reply.sender_id)
            else:
                user = await message.client.get_entity(
                    args[0] if not args[0].isnumeric() else int(args[0])
                )
                if len(args) == 1:
                    rank = rank
                elif len(args) >= 2:
                    rank = utils.get_args_raw(message).split(" ", 1)[1]
            try:
                await message.client(
                    EditAdminRequest(
                        message.chat_id,
                        user.id,
                        ChatAdminRights(
                            change_info=True,
                            post_messages=True,
                            edit_messages=True,
                            delete_messages=True,
                            ban_users=True,
                            invite_users=True,
                            pin_messages=True,
                            add_admins=True,
                            anonymous=False,
                            manage_call=True,
                            other=False
                        ),
                        rank,
                    )
                )
            except ChatAdminRequiredError:
                return await utils.answer(message, self.strings("no_rights", message))
            else:
                return await utils.answer(
                    message,
                    self.strings("promotedfull", message).format(user.first_name, rank),
                )
        except ValueError:
            return await utils.answer(message, self.strings("no_args", message))

   
