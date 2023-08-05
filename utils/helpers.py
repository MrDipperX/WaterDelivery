from loader import bot
from db.db import PgConn
from keyboards.keyboards import setting_buttons, iter_buttons, count_buttons, set_name_button, location_button
from utils.lang import file
from keyboards.media import input_media


def settings(message):
    try:
        db = PgConn()
        db.set_user_temp(message.from_user.id, "settings")
        user_lang = db.get_user_lang(message.from_user.id)
        bot.send_message(message.from_user.id, file[user_lang]['Settings_btn'],
                         reply_markup=setting_buttons(user_lang))

    except Exception as e:
        print(e)


def products(message, user_lang):
    try:
        db = PgConn()
        db.set_user_temp(message.from_user.id, "choose_product")

        product_names = db.get_products_name_by_category(message.from_user.id, user_lang)
        bot.send_message(message.from_user.id, file[user_lang]['Products'],
                         reply_markup=iter_buttons(product_names, user_lang, True))
    except Exception as e:
        print(e)


def set_count_product(message):
    try:
        db = PgConn()
        user_lang = db.get_user_lang(message.from_user.id)
        db.set_user_temp(message.from_user.id, "choose_count")
        product_info = db.get_product_info(message.from_user.id, user_lang)
        if product_info[0] in ['Kuler', 'Cooler', 'Кулер']:
            photos = product_info[3].split("|")
            pics = input_media(photos)
            bot.send_media_group(message.from_user.id, pics)
            bot.send_message(message.from_user.id, f'{product_info[0]}\n--------------------------------------\n'
                                                   f'{product_info[1]}\n--------------------------------------\n'
                                                   f'{product_info[2]} '
                                                   f'{file[user_lang]["Sum"]}', reply_markup=count_buttons(user_lang))
        else:
            bot.send_photo(message.from_user.id, open(f'photos/{product_info[3]}', 'rb'),
                           f'{product_info[0]}\n--------------------------------------\n'
                           f'{product_info[1]}\n--------------------------------------\n'
                           f'{product_info[2]} '
                           f'{file[user_lang]["Sum"]}', reply_markup=count_buttons(user_lang))

    except Exception as e:
        print(e)


def set_fio(message, user_lang, in_settings=True):
    try:
        db = PgConn()
        db.set_user_temp(message.from_user.id, "edit_fullname")
        name = db.get_name_n_surname(message.from_user.id)
        if in_settings:
            bot.send_message(message.from_user.id, f"{file[user_lang]['Set_fio']}",
                             reply_markup=set_name_button(user_lang, None))
        else:
            db.set_user_temp(message.from_user.id, "set_fullname")
            if None in name:
                bot.send_message(message.from_user.id, f"{file[user_lang]['Set_fio']}",
                                 reply_markup=set_name_button(user_lang, None))
            else:
                bot.send_message(message.from_user.id, f"{file[user_lang]['Set_fio']}",
                                 reply_markup=set_name_button(user_lang, name))
        bot.register_next_step_handler(message, set_fullname, user_lang)
    except Exception as e:
        print(e)


def set_fullname(message, user_lang):
    try:
        db = PgConn()
        if db.get_user_temp(message.from_user.id) in ['edit_fullname', 'set_fullname']:
            # user_lang = db.get_user_lang(message.from_user.id)

            if message.text.strip() == f"⬅ {file[user_lang]['Back_btn']}":
                if db.get_user_temp(message.from_user.id) == 'edit_fullname':
                    settings(message)
                else:
                    set_count_product(message)

            else:
                data = message.text.strip().split(" ")
                if len(data) == 2:
                    db.set_name_n_surname(data[0], data[1], message.from_user.id)
                    bot.send_message(message.from_user.id, file[user_lang]['Fullname_updated'])
                else:
                    bot.send_message(message.from_user.id, file[user_lang]['Error_in_fio'])
                if db.get_user_temp(message.from_user.id) == 'edit_fullname':
                    settings(message)
                else:
                    db.set_user_temp(message.from_user.id, 'send_location')
                    bot.send_message(message.from_user.id, file[user_lang]['Send_location'],
                                     reply_markup=location_button(user_lang))

    except Exception as e:
        print(e)
