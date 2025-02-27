from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.ext import MessageHandler, ConversationHandler
from telegram.ext.filters import Text
from functools import partial


TOKEN = ''
shoes = {
    '1': {
        'brand': 'nike',
        'size': '42',
        'image': 'images\\shoe1 .jpeg',
        'condition': 'like new',
        'Price': 25,
    },
    '2': {
        'Brand': 'nike',
        'Size': '41',
        'image': 'images\\shoe2.jpeg',
        'Condition': 'new',
        'Price': 40,
    },
    '3': {
        'brand': 'adidas',
        'size': '43',
        'image': 'images\\shoe3.jpeg',
        'condition': 'slightly used',
        'Price': 20,
    },
    '4': {
        'brand': 'new balance',
        'size': '44',
        'image': 'images\\shoe4.jpeg',
        'condition': 'used',
        'Price': 15,
    }
}


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


async def button(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'button1':
        for shoe in shoes.values():
            image_url = shoe.get('image')
            await query.message.reply_photo(photo=image_url)

        await query.edit_message_text(text="Here are all the availabe shoes")
    elif query.data == 'button2':
        await query.edit_message_text(text="send me the number of the shoe")
        return 1
    elif query.data == 'button3':
        await query.edit_message_text(text="send me the number of the shoe you want to buy")
        return 2
    elif query.data == 'button4':
        await query.edit_message_text(text="send me the number of the shoe you want to buy")
        return 3


def get_choice(num):
    choice = shoes.get(str(num), 'wrong input')
    return choice if choice == 'wrong input' else choice


def generate_msg(obj, type='show'):
    msg = ''
    if not type == 'show':
        payment_msg = ""
        return payment_msg
    for k, v in obj.items():
        if k == 'image':
            continue
        msg += f'{k} : {v}\n'
    return msg


async def action(update, context, type='show'):
    while True:
        try:
            num = int(update.message.text)
            shoe = get_choice(num)
            if not shoe == 'wrong input':
                msg = generate_msg(shoe, type=type)
                await update.message.reply_text(msg)
                if type == 'pay':
                    await update.message.reply_text('when you send the money confirm it from the *help* list\nor contact us for confirmation and shipment')
                else:
                    await update.message.reply_photo(photo=shoes.get(str(num))['image'])
            else:
                await update.message.reply_text('there is no shoes with this number')
            return ConversationHandler.END
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")
            num = int(update.message.text)


async def cancel(update, context):
    await update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('start request recieved')
    await update.message.reply_text("Hello! Welcome to our E-shop.")


def load_commands(application):
    print('adding handlers...')

    payment_info = partial(action, type='pay')
    get_description = partial(action, type='show')

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            1: [MessageHandler(Text(), get_description),],
            2: [MessageHandler(Text(), payment_info,),]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(conv_handler)


def main():
    application = Application.builder().token(TOKEN).concurrent_updates(True).build()
    load_commands(application)
    print("Telegram Bot started!", flush=True)
    application.run_polling()


if __name__ == '__main__':
    main()
