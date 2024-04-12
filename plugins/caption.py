from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper.database import db

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    if len(message.command) == 1:
       return await message.reply_text("**Use this Command to Set the Custom Caption for Your Files. For Setting Your Caption Send Caption in the Format\n`/set_caption`\n\nFile Caption Keys\n• `{filename}` :- Replaced by the Filename.\n• `{filesize}` :- Replaced by the Filesize.\n• `{duration}` :- Replaced by the Duration of Videos.\n\nExamples :- `/set_caption <b>📁 File Name :- {filename}\n\n💾 File Size :- {filesize}\n\n⌛ Duration :- {duration}</b>`\n\n`/set_caption <b>{filename}</b>`\n\n⚠️ Note :- You Can Check the Current Caption using /get_caption**", parse_mode=enums.ParseMode.MARKDOWN)
    caption = message.text.split(" ", 1)[1]
    if "{filename}" not in caption and "{filesize}" not in caption and "{duration}" not in caption:
        return await message.reply_text("**❌ Please include at Least one of the Placeholders `{filename}` or `{filesize}` or `{duration}` in the caption. Example :-\n`/set_caption <b>{filename}</b>`**", parse_mode=enums.ParseMode.MARKDOWN)
    await db.set_caption(message.from_user.id, caption=caption)
    await message.reply_text(f"**✅ Caption saved for {message.from_user.mention}. Check Your Caption using /get_caption**")

@Client.on_message(filters.private & filters.command(['get_caption']))
async def see_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if caption:
        await message.reply_text(f"**--{message.from_user.mention}'s Caption :---**\n\n{caption}")
    else:
        await message.reply_text("**😔 You Don't have Any Caption. So You're Set Captain.\nExample :- `/set_caption <b>{filename}</b>`**", parse_mode=enums.ParseMode.MARKDOWN)

@Client.on_message(filters.private & filters.command('del_caption'))
async def delete_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if not caption:
       return await message.reply_text("**😔 You Don't have Any Caption**")
    await db.set_caption(message.from_user.id, caption=None)
    await message.reply_text("**❌️ Caption Deleted**")
