from loader import bot
from db.db import PgConn
from keyboards.keyboards import menu_buttons, iter_buttons
from utils.lang import file


@bot.message_handler(commands=['menu'])
def menu(message):
    try:
        db = PgConn()
        db.set_user_temp(message.from_user.id, "menu")
        user_lang = db.get_user_lang(message.from_user.id)
        bot.send_message(message.from_user.id, file[user_lang]['Menu'],
                         reply_markup=menu_buttons(user_lang))

    except Exception as e:
        print(e)


@bot.message_handler(commands=['order'])
def categories(message, user_lang):
    try:
        db = PgConn()
        db.set_user_temp(message.from_user.id, "choose_category")
        categories_name = db.get_all_categories(user_lang)
        bot.send_message(message.from_user.id, file[user_lang]['Categories'],
                         reply_markup=iter_buttons(categories_name, user_lang, True))
    except Exception as e:
        print(e)
