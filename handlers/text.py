from loader import bot
from db.db import PgConn
from keyboards.keyboards import phone_button, language_buttons
from keyboards.media import input_media
from utils.lang import file
from handlers.commands import menu, categories
from utils.helpers import settings, set_fio, products, set_count_product

from datetime import datetime


@bot.message_handler(content_types=['text'])
def mess(message):
    try:
        text = message.text.strip()

        db = PgConn()
        user_lang = db.get_user_lang(message.from_user.id)

        if text in ["🇺🇿 O'zbekcha", "🇷🇺 Русский", "🇬🇧 English"] and db.get_user_temp(message.from_user.id) in \
                ['start', 'edit_lang']:

            if text == "🇺🇿 O'zbekcha":
                db.set_user_lang(message.from_user.id, 'uz')

            elif text == "🇷🇺 Русский":
                db.set_user_lang(message.from_user.id, 'ru')

            else:
                db.set_user_lang(message.from_user.id, 'en')

            if db.get_user_temp(message.from_user.id) == 'start':
                bot.send_message(message.from_user.id, file[db.get_user_lang(message.from_user.id)]['Set_phone'],
                                 reply_markup=phone_button(db.get_user_lang(message.from_user.id), False))
            else:
                bot.send_message(message.from_user.id, file[db.get_user_lang(message.from_user.id)]['Lang_updated'])
                settings(message)

        elif text == f"✅ {file[user_lang]['Accept']}" and db.get_user_temp(message.from_user.id) == 'send_location':
            db.create_order(datetime.now(), message.from_user.id)
            bot.send_message(message.from_user.id, "Спасибо за заказ! 🚛 Курьер с вами свяжится. ")
            info = db.get_order_for_sending_to_channel(message.from_user.id)
            bot.send_message(message.from_user.id, f"Заказ №{info[0]} \n{info[9]} \nЦена: {info[1]} сум\nКоличество: "
                                                   f"{info[2]}\nДата заказа: {info[3].strftime('%Y-%m-%d %H:%M:%S')}"
                                                   f"\nUser : {info[4]} {info[5]}\nНомер телефона : {info[6]}")
            bot.send_location(message.from_user.id, latitude=info[7], longitude=info[8])
            menu(message)

        elif text == f"❌ {file[user_lang]['Cancel']}" and db.get_user_temp(message.from_user.id) == 'send_location':
            db.cancel_order(message.from_user.id)
            menu(message)

        elif text == file[user_lang]['Cooler']:
            photos = ['kuler1.jpg', 'kuler2.jpg', 'kuler3.jpg']
            pics = input_media(photos)
            bot.send_media_group(message.from_user.id, pics)
            bot.send_message(message.from_user.id, file[user_lang]['About cooler'])

        elif text == file[user_lang]['Water']:
            bot.send_photo(message.from_user.id, open("photos/Suv.png", 'rb'), caption=file[user_lang]['About water'])

        elif text in [f"🛍 {file[user_lang]['Sell']}", f"⚙ {file[user_lang]['Settings_btn']}",
                      f"🏢 {file[user_lang]['About_btn']}"] and db.get_user_temp(message.from_user.id) == 'menu':
            if text == f"🛍 {file[user_lang]['Sell']}":
                categories(message, user_lang)
            elif text == f"⚙ {file[user_lang]['Settings_btn']}":
                settings(message)
            else:
                db.set_user_temp(message.from_user.id, 'about')
                bot.send_photo(message.from_user.id, open("photos/about.png", 'rb'), file[user_lang]['About'])

        elif text in [f"🇺🇿/🇷🇺/🇬🇧 {file[user_lang]['Edit_lang_btn']}", f"📱 {file[user_lang]['Edit_telp_numb_btn']}",
                      f"👤 {file[user_lang]['Edit_fio']}"] and db.get_user_temp(message.from_user.id) == 'settings':
            if text == f"🇺🇿/🇷🇺/🇬🇧 {file[user_lang]['Edit_lang_btn']}":
                db.set_user_temp(message.from_user.id, "edit_lang")
                bot.send_message(message.from_user.id, f"{file[user_lang]['Choose_lang']}",
                                 reply_markup=language_buttons(user_lang, True))
            elif text == f"📱 {file[user_lang]['Edit_telp_numb_btn']}":
                db.set_user_temp(message.from_user.id, "edit_numb")
                bot.send_message(message.from_user.id, f"{file[user_lang]['Set_phone']}",
                                 reply_markup=phone_button(user_lang, True))
            else:
                set_fio(message, user_lang, True)

        elif text == f"⬅ {file[user_lang]['Back_btn']}":
            if db.get_user_temp(message.from_user.id) == 'settings':
                menu(message)
            if db.get_user_temp(message.from_user.id) == 'about':
                menu(message)
            elif db.get_user_temp(message.from_user.id) in ['edit_lang', 'edit_numb', 'edit_fullname']:
                settings(message)
            elif db.get_user_temp(message.from_user.id) == 'choose_category':
                menu(message)
            elif db.get_user_temp(message.from_user.id) == 'choose_product':
                categories(message, user_lang)
            elif db.get_user_temp(message.from_user.id) == 'choose_count':
                products(message, user_lang)

        elif text[0] == "+" and db.get_user_temp(message.from_user.id) in ["start", "edit_numb"]:
            db.add_user_contact(message.from_user.id, text)
            if db.get_user_temp(message.from_user.id) == 'start':
                bot.send_message(message.from_user.id, file[db.get_user_lang(message.from_user.id)]['Numb_set'])
                menu(message)

            elif db.get_user_temp(message.from_user.id) == 'edit_numb':
                bot.send_message(message.from_user.id, file[db.get_user_lang(message.from_user.id)]['Numb_updated'])
                settings(message)

        elif text in list(map(lambda x: str(x), range(1, 100))) and \
                db.get_user_temp(message.from_user.id) == 'choose_count':
            db.set_last_quantity(message.from_user.id, int(text))
            set_fio(message, user_lang, False)

        elif text in db.get_all_categories(user_lang) and db.get_user_temp(message.from_user.id) == 'choose_category':
            db.set_last_category(message.from_user.id, text)
            products(message, user_lang)

        elif text in db.get_products_name_by_category(message.from_user.id, user_lang) and \
                db.get_user_temp(message.from_user.id) == 'choose_product':
            db.set_last_product(message.from_user.id, text)
            set_count_product(message)

    except Exception as e:
        print(e)
