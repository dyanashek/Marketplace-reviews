import random

import config

USERNAME_NEEDED = 'Для того, чтобы принять участие в нашей акции необходимо установить имя пользователя в *настройках Telegram*!'

PROHIBITED = 'К сожалению, Вы пока *не можете* принять участие в акции, мы пришлем Вам *уведомление*, когда ситуация изменится.'

ALREADY_ORDERED = 'К сожалению, Вы *уже заказывали* товары, участвующие в текущей акции. Мы пришлем Вам *уведомление*, когда ситуация изменится.'

OUTDATED = 'Данные устарели, воспользуйтесь командой */promo* для получения информации об актуальной акции!'

RESTRICTED = 'Недостаточно прав доступа.'

PAYMENT_METHOD = 'Пожалуйста, выберите *каким способом* Вам осуществить перевод:'

BANK = 'Выберите *банк*, на который нужно осуществить перевод:'

PHONE = 'Введите *номер телефона* для совершения перевода по СБП.\nВ формате: *79991234567*.'

CARD = 'Введите *номер карты* для совершения перевода.\nВ формате: *5555 4444 3333 2222*.'

WRONG_FORMAT = 'Введенные данные *не соответствуют формату*, попробуйте еще раз.'

UPDATED = 'Данные успешно обновлены.'

DONE = 'Спасибо за участие в акции! *Выплата поступит* на указанные Вами реквизиты после проверки администратором.\n\nВы можете воспользоваться командой */account* для просмотра указанных вами реквизитов.\nВ случае возникновения вопросов - воспользуйтесь командой */help* для связи с администратором.'

NO_PAYMENT_DATA = 'В вашем профиле не заполнены реквизиты для выплат.\nВ случае возникновения вопросов - воспользуйтесь командой */help* для связи с администратором.'

HELP = 'У Вас возникли сложности и Вы хотите, чтобы с вами *связался администратор*?'

NO_USERNAME = 'Пожалуйста, укажите *имя пользователя* в настройках telegram, чтобы администратор мог с Вами связаться.'

ADMIN_INFORMED = 'Ваш запрос передан *администратору*, он свяжется с вами в *ближайшее время*.'

IS_HELD_NEEDED = 'В случае возникновения вопросов - воспользуйтесь командой */help* для связи с администратором.'

NO_MEDIA_GROUP = 'Пожалуйста, отправляйте *по одному скриншоту за раз*.'

NO_DOCUMENT = 'Пожалуйста, прикрепите скриншот *изображением*, а не файлом.'

NEW_PROMO = 'Появились новые акции специально для Вас!\nХотите поучаствовать?'


def bought_products(products):
    reply_text = 'Вы отметили следующие товары как оплаченные:\n\n'

    smiles = ''
    for num, product in enumerate(products):
        smile = random.choice(config.SMILES)
        smiles += smile
        reply_text += f'{num + 1}. {product} {smile}\n'
    
    reply_text += '\nПосле получения товара, воспользуйтесь кнопкой *"Получено"*, вам понадобятся скриншоты выкупов и оставленных отзывов (напротив товара указан смайлик, который нужно будет включить в отзыв, чтобы мы смогли его идентифицировать). Пожалуйста, не завершайте и не удаляйте чат.'

    return reply_text, smiles


def receive_product(product):
    return f'Пожалуйста, отправьте скриншот, подтверждающий выкуп товара *{product}*.'


def review_product(product, smile):
    return f'Пожалуйста, отправьте скриншот c отзывом на товар *{product}*, он должен содержать смайлик {smile}.'


def payment_method(payment_method, bank, account):
    if payment_method == 'card':
        method_name = 'Банковская карта'
    elif payment_method == 'sbp':
        method_name = 'Номер телефона'
    
    reply_text = f'''
                \n*{config.PAYMENT_METHODS[payment_method]}*\
                \n\
                \n*Банк:* {config.BANKS[bank]}\
                \n*{method_name}:* {account}\
                '''
    
    return reply_text


def inform_manager(username, payment_method, bank, account, products, smiles):
    if payment_method == 'card':
        method_name = 'Банковская карта'
    elif payment_method == 'sbp':
        method_name = 'Номер телефона'
    
    reply_text = f'''
                \nПользователь @{username} отметил, что выполнил условия.\
                \n\
                \n*{config.PAYMENT_METHODS[payment_method]}*\
                \n*Банк:* {config.BANKS[bank]}\
                \n*{method_name}:* {account}\
                \n\
                \nТовары:\
                '''

    for num in range(len(products)):
        reply_text += f'\n{num + 1}. {products[num]} - {smiles[num]}'
    
    return reply_text


def asked_help(username):
    return f'Пользователь @{username} обратился за помощью.'