from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = ''


async def help(update, context):
    print('help request recieved')
    await update.message.reply_text("what can i help you with?")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('start request recieved')
    await update.message.reply_text("Hello! Welcome to our E-shop.")


def load_commands(application):
    print('adding handlers...')
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler('help', help))


def main():
    application = Application.builder().token(TOKEN).concurrent_updates(True).build()
    load_commands(application)
    print("Telegram Bot started!", flush=True)
    application.run_polling()


if __name__ == '__main__':
    main()
