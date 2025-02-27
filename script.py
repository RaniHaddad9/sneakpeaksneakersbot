from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = ''


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('start request recieved')
    await update.message.reply_text("Hello! Welcome to our E-shop.")


def main():
    application = Application.builder().token(TOKEN).concurrent_updates(True).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


if __name__ == '__main__':
    main()
