from telebot import types
from utils.lang import file


def phone_button(lang, in_settings):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    telp_numb_btn = types.KeyboardButton(f"📱 {file[lang]['Telp_numb']}", request_contact=True)
    keyboard.add(telp_numb_btn)
    if in_settings:
        back = types.KeyboardButton(f"⬅ {file[lang]['Back_btn']}")
        keyboard.add(back)
    return keyboard


def location_button(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    loc_btn = types.KeyboardButton(f"📍 {file[lang]['Your_location']}", request_location=True)
    return keyboard.add(loc_btn)


def set_name_button(lang, name):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    if name:
        name = types.KeyboardButton(f"{name[0]} {name[1]}")
        keyboard.add(name)
    back = types.KeyboardButton(f"⬅ {file[lang]['Back_btn']}")
    keyboard.add(back)
    return keyboard


def count_buttons(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [types.KeyboardButton(str(numb)) for numb in range(1, 11)]
    back = types.KeyboardButton(f"⬅ {file[lang]['Back_btn']}")
    keyboard.add(*buttons, back)

    return keyboard


def iter_buttons(iterator, lang, instance_back):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(button) for button in iterator]
    keyboard.add(*buttons)
    if instance_back:
        back = types.KeyboardButton(f"⬅ {file[lang]['Back_btn']}")
        keyboard.add(back)

    return keyboard


def language_buttons(lang, in_settings):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    uz_btn = types.KeyboardButton(f"🇺🇿 O'zbekcha")
    ru_btn = types.KeyboardButton(f"🇷🇺 Русский")
    en_btn = types.KeyboardButton(f"🇬🇧 English")
    keyboard.add(uz_btn, ru_btn, en_btn)
    if in_settings:
        back = types.KeyboardButton(f"⬅ {file[lang]['Back_btn']}")
        keyboard.add(back)

    return keyboard


def confirm_buttons(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    ok_btn = types.KeyboardButton(f"✅ {file[lang]['Accept']}")
    nope_btn = types.KeyboardButton(f"❌ {file[lang]['Cancel']}")
    return keyboard.add(ok_btn, nope_btn)


def menu_buttons(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    order = types.KeyboardButton(f"🛍 {file[lang]['Sell']}")
    settings = types.KeyboardButton(f"⚙ {file[lang]['Settings_btn']}")
    about = types.KeyboardButton(f"🏢 {file[lang]['About_btn']}")
    water = types.KeyboardButton(f" {file[lang]['Water']}")
    cooler = types.KeyboardButton(f" {file[lang]['Cooler']}")
    keyboard.add(order)
    keyboard.add(settings, about)
    keyboard.add(water, cooler)
    return keyboard


def setting_buttons(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    edit_numb = types.KeyboardButton(f"📱 {file[lang]['Edit_telp_numb_btn']}")
    edit_name = types.KeyboardButton(f"👤 {file[lang]['Edit_fio']}")
    edit_lang = types.KeyboardButton(f"🇺🇿/🇷🇺/🇬🇧 {file[lang]['Edit_lang_btn']}")
    back = types.KeyboardButton(f"⬅ {file[lang]['Back_btn']}")
    keyboard.add(edit_name)
    keyboard.add(edit_numb, edit_lang)
    keyboard.add(back)
    return keyboard
