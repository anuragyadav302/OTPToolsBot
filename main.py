from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from telegram.error import TelegramError
from telegram.request import HTTPXRequest
from config import BOT_TOKEN


CHANNEL_ID = "@DealNova_Official"
CHANNEL_LINK = "https://t.me/DealNova_Official"

GROUP_ID = "@Friend_Zone_8Z_M3BVjMjk1"
GROUP_LINK = "https://t.me/Friend_Zone_8Z_M3BVjMjk1"

WEBSITE_LINK = "https://www.call-bomber.online/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("👥 Join Group", url=GROUP_LINK)],
        [InlineKeyboardButton("✅ Verify", callback_data="verify")]
    ]

    await update.message.reply_text(
        "🤖 Welcome!\n\n"
        "Bot use karne ke liye pehle Channel aur Group join karein.\n\n"
        "Join karne ke baad Verify button dabaye 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    try:
        channel_member = await context.bot.get_chat_member(
            CHANNEL_ID,
            user_id
        )

        group_member = await context.bot.get_chat_member(
            GROUP_ID,
            user_id
        )

        valid_status = [
            "member",
            "administrator",
            "creator"
        ]

        if (
            channel_member.status in valid_status
            and group_member.status in valid_status
        ):

            keyboard = [
                [
                    InlineKeyboardButton(
                        "🌐 Open Website",
                        url=WEBSITE_LINK
                    )
                ]
            ]

            await query.edit_message_text(
                "✅ Verification Successful!\n\n"
                "Ab aap website open kar sakte hain 👇",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        else:

            await query.edit_message_text(
                "❌ Aapne abhi Channel ya Group join nahi kiya.\n"
                "Pehle join karein aur fir Verify karein."
            )

    except TelegramError as e:

        await query.edit_message_text(
            "⚠️ Verification error.\n"
            "Bot ko admin permission check karein."
        )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✅ Bot Online"
    )


def main():

    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30
    )

    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .request(request)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("status", status)
    )

    app.add_handler(
        CallbackQueryHandler(verify)
    )


    print("✅ Bot Started...")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
