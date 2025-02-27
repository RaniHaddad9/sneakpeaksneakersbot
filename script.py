from telegram.ext import Application

TOKEN = ''


def main():
    application = Application.builder().token(TOKEN).concurrent_updates(True).build()
    application.run_polling()


if __name__ == '__main__':
    main()
