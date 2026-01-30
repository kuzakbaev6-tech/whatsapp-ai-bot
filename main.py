import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сәлем 👋 Мен тірімін")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "мен туралы не білесің" in text:
        await update.message.reply_text(
            "Сен Telegram бот жасап жатқан, беріспейтін адамсың 😎\n"
            "Қалғанын біртіндеп үйреніп жатырмын."
        )
    else:
        await update.message.reply_text(f"Сен жаздың: {update.message.text}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
