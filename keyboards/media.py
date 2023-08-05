from telebot.types import InputMediaPhoto


def input_media(photos):

    return [InputMediaPhoto(open(f"photos/{pic}", "rb")) for pic in photos]