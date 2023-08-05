from loader import bot
from db.db import PgConn
from keyboards.keyboards import language_buttons


@bot.message_handler(commands=['start'])
def start(message):
    db = PgConn()
    db.create_tables()
    db.add_user(message.from_user.id, message.from_user.username, message.date)
    db.set_user_temp(message.from_user.id, "start")
    lang = db.get_user_lang(message.from_user.id)
    bot.send_message(message.from_user.id, "Salom 🇺🇿  Привет 🇷🇺  Hello 🇬🇧",
                     reply_markup=language_buttons(lang, False))