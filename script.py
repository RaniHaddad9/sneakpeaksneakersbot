from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes


TOKEN = ''


async def help(update, context):
    print('help request recieved')
    keyboard = [
        [InlineKeyboardButton("List all shoes", callback_data='button1')],
        [InlineKeyboardButton("Show shoe discriptions", callback_data='button2')],
        [InlineKeyboardButton("Order shoe", callback_data='button3')],
        [InlineKeyboardButton("Confirm payment", callback_data='button4')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("what do you want to do?", reply_markup=reply_markup)


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
