import asyncio

from pyrogram import Client, filters
from pyrogram import Client as Client1
from pyrogram.errors import ApiIdInvalid as ApiIdInvalid1
from pyrogram.errors import PasswordHashInvalid as PasswordHashInvalid1
from pyrogram.errors import PhoneCodeExpired as PhoneCodeExpired1
from pyrogram.errors import PhoneCodeInvalid as PhoneCodeInvalid1
from pyrogram.errors import PhoneNumberInvalid as PhoneNumberInvalid1
from pyrogram.errors import SessionPasswordNeeded as SessionPasswordNeeded1
from pyrogram.errors import (
    ApiIdInvalid,
    FloodWait,
    PasswordHashInvalid,
    PhoneCodeExpired,
    PhoneCodeInvalid,
    PhoneNumberInvalid,
    SessionPasswordNeeded,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient
from telethon.errors import (
    ApiIdInvalidError,
    PasswordHashInvalidError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    PhoneNumberInvalidError,
    SessionPasswordNeededError,
)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest


from config import SUPPORT_GRP
from shizuchat import shizuchat
from StringBot.modules import retry_key


# BUTTON

retry_key = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="ᴛʀʏ ᴀɢᴀɪɴ ☹️", callback_data="gensession")]]
)

#__________

async def gen_session(
    message, user_id: int, telethon: bool = False, old_pyro: bool = False
):
    if telethon:
        ty = f"ᴛᴇʟᴇᴛʜᴏɴ"
    elif old_pyro:
        ty = f"ᴩʏʀᴏɢʀᴀᴍ v1"
    else:
        ty = f"ᴩʏʀᴏɢʀᴀᴍ v2"

    await message.reply_text(f"» ᴛʀʏɪɴɢ ᴛᴏ sᴛᴀʀᴛ {ty} sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ...")

    try:
        api_id = await shizuchat.ask(
            identifier=(message.chat.id, user_id, None),
            text="» ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴀᴘɪ ɪᴅ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ :",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await shizuchat.send_message(
            user_id,
            "» ᴛɪᴍᴇᴅ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏғ 5 ᴍɪɴᴜᴛᴇs.\n\nᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=retry_key,
        )

    if await cancelled(api_id):
        return

    try:
        api_id = int(api_id.text)
    except ValueError:
        return await shizuchat.send_message(
            user_id,
            "» ᴛʜᴇ ᴀᴘɪ ɪᴅ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs ɪɴᴠᴀʟɪᴅ.\n\nᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=retry_key,
        )

    try:
        api_hash = await shizuchat.ask(
            identifier=(message.chat.id, user_id, None),
            text="» ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴀᴘɪ ʜᴀsʜ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ :",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await shizuchat.send_message(
            user_id,
            "» ᴛɪᴍᴇᴅ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏғ 5 ᴍɪɴᴜᴛᴇs.\n\nᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=retry_key,
        )

    if await cancelled(api_hash):
        return

    api_hash = api_hash.text

    if len(api_hash) < 30:
        return await shizuchat.send_message(
            user_id,
            "» ᴛʜᴇ ᴀᴘɪ ʜᴀsʜ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs ɪɴᴠᴀʟɪᴅ.\n\nᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=retry_key,
        )

    try:
        phone_number = await shizuchat.ask(
            identifier=(message.chat.id, user_id, None),
            text="» ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ :",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await shizuchat.send_message(
            user_id,
            "» ᴛɪᴍᴇᴅ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏғ 5 ᴍɪɴᴜᴛᴇs.\n\nᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=retry_key,
        )

    if await cancelled(phone_number):
        return
    phone_number = phone_number.text

    await shizuchat.send_message(user_id, "» ᴛʀʏɪɴɢ ᴛᴏ sᴇɴᴅ ᴏᴛᴩ ᴀᴛ ᴛʜᴇ ɢɪᴠᴇɴ ɴᴜᴍʙᴇʀ...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="shizuchat", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()

    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
        await asyncio.sleep(1)

    except FloodWait as f:
        return await shizuchat.send_message(
            user_id,
            f"» ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴄᴏᴅᴇ ғᴏʀ ʟᴏɢɪɴ.\n\nᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ {f.value or f.x} sᴇᴄᴏɴᴅs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.",
            reply_markup=retry_key,
        )
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        return await shizuchat.send_message(
            user_id,
            "» ᴀᴘɪ ɪᴅ ᴏʀ ᴀᴘɪ ʜᴀsʜ ɪs ɪɴᴠᴀʟɪᴅ.\n\nᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=retry_key,
        )
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        return await shizuchat.send_message(
            user_id,
            "» ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪɴᴠᴀʟɪᴅ.\n\nᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=retry_key,
        )

    try:
        otp = await shizuchat.ask(
            identifier=(message.chat.id, user_id, None),
            text=f"ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ᴏᴛᴘ sᴇɴᴛ ᴛᴏ {phone_number}.\n\nɪғ ᴏᴛᴩ ɪs <code>96384</code>, ᴩʟᴇᴀsᴇ sᴇɴᴅ ɪᴛ ᴀs <code>9 6 3 8 4.</code>",
            filters=filters.text,
            timeout=600,
        )
        if await cancelled(otp):
            return
    except ListenerTimeout:
        return await shizuchat.send_message(
            user_id,
            "» ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏғ 10 ᴍɪɴᴜᴛᴇs.\n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=retry_key,
        )

    otp = otp.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, otp, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, otp)
    except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
        return await shizuchat.send_message(
            user_id,
            "» ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs <b>ᴡʀᴏɴɢ.</b>\n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=retry_key,
        )
    except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
        return await shizuchat.send_message(
            user_id,
            "» ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs <b>ᴇxᴩɪʀᴇᴅ.</b>\n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=retry_key,
        )
    except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
        try:
            pwd = await shizuchat.ask(
                identifier=(message.chat.id, user_id, None),
                text="» ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴛᴡᴏ sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴘᴀssᴡᴏʀᴅ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ :",
                filters=filters.text,
                timeout=300,
            )
        except ListenerTimeout:
            return shizuchat.send_message(
                user_id,
                "» ᴛɪᴍᴇᴅ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏғ 5 ᴍɪɴᴜᴛᴇs.\n\nᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
                reply_markup=retry_key,
            )

        if await cancelled(pwd):
            return
        pwd = pwd.text

        try:
            if telethon:
                await client.sign_in(password=pwd)
            else:
                await client.check_password(password=pwd)
        except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
            return await shizuchat.send_message(
                user_id,
                "» ᴛʜᴇ ᴩᴀssᴡᴏʀᴅ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs ᴡʀᴏɴɢ.\n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
                reply_markup=retry_key,
            )

    except Exception as ex:
        return await shizuchat.send_message(user_id, f"ᴇʀʀᴏʀ : <code>{str(ex)}</code>")

    try:
        txt = "ʜᴇʀᴇ ɪs ʏᴏᴜʀ {0} sᴛʀɪɴɢ sᴇssɪᴏɴ\n\n<code>{1}</code>\n\nᴀ sᴛʀɪɴɢ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ ʙʏ <a href={2}>ᴘʙx ᴛᴇᴀᴍ</a>\n☠ <b>ɴᴏᴛᴇ :</b> ᴅᴏɴ'ᴛ sʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ʏᴏᴜʀ ɢɪʀʟғʀɪᴇɴᴅ."
        if telethon:
            string_session = client.session.save()
            await client.send_message(
                "me",
                txt.format(ty, string_session, SUPPORT_GRP),
                link_preview=False,
                parse_mode="html",
            )
            await client(JoinChannelRequest("@HEROKUBIN_01"))
        else:
            string_session = await client.export_session_string()
            await client.send_message(
                "me",
                txt.format(ty, string_session, SUPPORT_GRP),
                disable_web_page_preview=True,
            )
            await client.join_chat("FallenAssociation")
    except KeyError:
        pass
    try:
        await client.disconnect()
        await shizuchat.send_message(
            chat_id=user_id,
            text=f"sᴜᴄᴄᴇssғᴜʟʟʏ ɢᴇɴᴇʀᴀᴛᴇᴅ ʏᴏᴜʀ {ty} sᴛʀɪɴɢ sᴇssɪᴏɴ.\n\nᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs ғᴏʀ ɢᴇᴛᴛɪɴɢ ɪᴛ.\n\nᴀ sᴛʀɪɴɢ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ ʙʏ <a href={SUPPORT_GRP}>ᴘʙx ᴛᴇᴀᴍ</a>.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs",
                            url=f"tg://openmessage?user_id={user_id}",
                        )
                    ]
                ]
            ),
            disable_web_page_preview=True,
        )
    except:
        pass


async def cancelled(message):
    if "/cancel" in message.text:
        await message.reply_text(
            "» ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀɪɴɢ ɢᴇɴᴇʀᴀᴛɪᴏɴ ᴩʀᴏᴄᴇss.", reply_markup=retry_key
        )
        return True
    elif "/restart" in message.text:
        await message.reply_text(
            "» sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇsᴛᴀʀᴛᴇᴅ ᴛʜɪs ʙᴏᴛ.", reply_markup=retry_key
        )
        return True
    elif message.text.startswith("/"):
        await message.reply_text(
            "» ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀɪɴɢ ɢᴇɴᴇʀᴀᴛɪᴏɴ ᴩʀᴏᴄᴇss.", reply_markup=retry_key
        )
        return True
    else:
        return False
