from loader import bot
from db.db import PgConn
from utils.lang import file
from handlers.commands import menu
from utils.helpers import settings
from keyboards.keyboards import confirm_buttons


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    try:
        db = PgConn()
        db.add_user_contact(message.from_user.id, message.contact.phone_number)
        if db.get_user_temp(message.from_user.id) == 'start':
            bot.send_message(message.from_user.id, file[db.get_user_lang(message.from_user.id)]['Numb_set'])
            menu(message)
        elif db.get_user_temp(message.from_user.id) == 'edit_numb':
            bot.send_message(message.from_user.id, file[db.get_user_lang(message.from_user.id)]['Numb_updated'])
            settings(message)

    except Exception as e:
        print(e)


@bot.message_handler(content_types=['location'])
def location_handler(message):
    try:
        db = PgConn()
        if db.get_user_temp(message.from_user.id) == 'send_location':
            db.set_location(message.location.latitude, message.location.longitude, message.from_user.id)
            bot.send_message(message.from_user.id, file[db.get_user_lang(message.from_user.id)]['Your_order_is_ready'],
                             reply_markup=confirm_buttons(db.get_user_lang(message.from_user.id)))

            # set_count_product(message)

    except Exception as e:
        print(e)
