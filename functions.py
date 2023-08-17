import telebot
import time

import db_functions
import keyboards
import text
import config


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


def get_texts_from_google():
    texts = config.WORK_SHEET.col_values(1)[1::]

    return texts


def get_products_from_google():
    products = config.WORK_SHEET.col_values(2)[1::]
    photos = config.WORK_SHEET.col_values(3)[1::]

    return list(zip(products, photos))


def update_database(user_id):
    products = get_products_from_google()
    db_functions.drop_active_products()

    for product in products:
        if not db_functions.is_product_in_database(product[0]):
            db_functions.add_product(product)
        else:
            db_functions.activate_product(product[0])
    
    texts = get_texts_from_google()
    db_functions.update_text('start', texts[0])
    db_functions.update_text('sorry', texts[1])
    db_functions.update_text('rules', texts[2])
    db_functions.update_text('products', texts[3])

    try:
        bot.send_message(chat_id=user_id,
                         text=text.UPDATED,
                         parse_mode='Markdown',
                         )
    except:
        pass


def inform_manager(user_id):
    user_info = db_functions.select_user_info(user_id)

    username = user_info[2]

    payment_method = user_info[3]
    bank = user_info[4]
    account = user_info[5]

    products = eval(user_info[9])
    smiles = user_info[12]

    receive = eval(user_info[10])
    reviews = eval(user_info[11])
    
    reply_text = text.inform_manager(username, payment_method, bank, account, products, smiles)

    try:
        sended_message = bot.send_message(chat_id=config.MANAGER_ID,
                        text=reply_text,
                        parse_mode='Markdown',
                        )
    except:
        pass

    group_media = []
    for photo in receive:
        group_media.append(telebot.types.InputMediaPhoto(photo))

    try:
        bot.send_media_group(chat_id=config.MANAGER_ID,
                                media=group_media,
                                reply_to_message_id=sended_message.id,
                                timeout=30,
                                )
    except:
        pass
    
    group_media = []
    for photo in reviews:
        group_media.append(telebot.types.InputMediaPhoto(photo))

    try:
        bot.send_media_group(chat_id=config.MANAGER_ID,
                                media=group_media,
                                reply_to_message_id=sended_message.id,
                                timeout=30,
                                )
    except:
        pass

    db_functions.drop_settings(user_id)


def update_eligible():
    while True:
        products = db_functions.select_active_products()

        while len(products) < 3:
            products.append(products[0])

        users_ids = db_functions.select_again_eligible_users(products)

        for user_id in users_ids:
            db_functions.update_users_field(user_id, 'eligible', True)

            try:
                bot.send_message(chat_id=user_id,
                                text=text.NEW_PROMO,
                                reply_markup=keyboards.action_keyboard(),
                                parse_mode='Markdown',
                                disable_notification=False,
                                )
            except:
                pass
        
        time.sleep(86400)