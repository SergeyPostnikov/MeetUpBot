import datetime as dt


from globals import (
bot, telebot, ACCESS_DUE_TIME, INPUT_DUE_TIME, payload, date_now, date_end, pay_token, markup_main_menu, markup_user,
markup_speaker, markup_registration, markup_faq)
from telebot.util import quick_markup
from telebot.types import LabeledPrice, ShippingOption
from telegram_bot_calendar.base import DAY
from telegram_bot_calendar.detailed import DetailedTelegramCalendar


shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]


class WMonthTelegramCalendar(DetailedTelegramCalendar):
    first_step = DAY


def start_bot(message: telebot.types.Message):
    tg_name = message.from_user.username
    msg = bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.username} 😉')
    access_due = dt.datetime.now() + dt.timedelta(0, ACCESS_DUE_TIME)
    user_group = 1
    payload[message.chat.id] = {
        'callback': None,  # current callback button
        'last_msg': [],  # последние отправленные за один раз сообщения (для подчистки кнопок) -- перспектива
        'callback_source': [],  # если задан, колбэк кнопки будут обрабатываться только с этих сообщений
        'access_due': access_due,  # дата и время актуальности кэшированного статуса
        'name': None,
        'date': None,
        'time': None,
        'donate': None,
        'msg_id_1': None,
        'msg_id_2': None,
        'tg_name': tg_name,
        'tg_id': message.chat.id,
        'text': None,
        'phone': None,
        'step_due': None,  # срок актуальности ожидания ввода данных (используем в callback функциях)
    }
    payload[message.chat.id]['msg_id_1'] = msg.id
    if user_group == 1:
        markup = markup_user
    elif user_group == 2:
        markup = markup_speaker
    msg = bot.send_message(message.chat.id, 'Приветственное сообщение, рассказываю что могу 🥳',
                           reply_markup=markup)
    payload[message.chat.id]['msg_id_2'] = msg.id


def check_user_in_cache(msg: telebot.types.Message):
    """проверят наличие user в кэше
    это на случай, если вдруг случился сбой/перезапуск скрипта на сервере
    и кэш приказал долго жить. В этом случае нужно отправлять пользователя в начало
    пути, чтобы избежать ошибок """
    user = payload.get(msg.chat.id)
    if not user:
        bot.send_message(msg.chat.id, 'Упс. Что то пошло не так.\n'
                                      'Нажмите /start')
        return None
    else:
        return user


def main_menu(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    user_group = 1
    if user_group == 1:
        markup = markup_user
    elif user_group == 2:
        markup = markup_speaker
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Приветственное сообщение, рассказываю что могу 🥳', reply_markup=markup)


def get_faq(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='FAQ ', reply_markup=markup_faq)


def get_faq_question(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Описываем как задать вопрос', reply_markup=markup_main_menu)


def get_faq_communicate(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Описываем как общаться', reply_markup=markup_main_menu)


def get_faq_start_report(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Описываем как начать/ закончить доклад ', reply_markup=markup_main_menu)

def get_communicate(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Кнопка пока не работает 😝', reply_markup=markup_main_menu)

def ask_question(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Кнопка пока не работает 😞', reply_markup=markup_main_menu)

def get_donate(message: telebot.types.Message, order_id, step=0):
    user = payload[message.chat.id]
    if step == 0:
        msg = bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text='Введите сумму доната в рублях', reply_markup=markup_main_menu)
        user['callback_source'] = [msg.id]
        bot.register_next_step_handler(message, get_donate, order_id, 1)
        user['step_due'] = dt.datetime.now() + dt.timedelta(0, INPUT_DUE_TIME)
    elif user['step_due'] < dt.datetime.now():
        bot.send_message(message.chat.id, 'Время ввода данных истекло. Нажмите /start')
        return
    elif step == 1:
        try:
            user['donate'] = int(message.text)
            bot.delete_message(message.chat.id, message.message_id)
            bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                        text=f'Введенная сумма {user["donate"]}', reply_markup=markup_registration)
        except ValueError:
            bot.delete_message(message.chat.id, message.message_id)
            bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                        text=f'Введенная сумма некорректна', reply_markup=markup_main_menu)
    user['callback_source'] = []


def get_registration_pay(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    price = LabeledPrice(label='Донатик братюням', amount=int(user['donate']) * 100)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text="Со мной не будут работать настоящие карты, никакие деньги не будут списаны с вашего счета."
                     " Используйте этот номер тестовой карты для оплаты: `4242 4242 4242 4242`"
                     "\n\nДля отмены платежа нажмите кнопку /start"
                     "\n\nЭто ваш демонстрационный счет:", parse_mode='Markdown')
    bot.send_invoice(
        message.chat.id,
        title='Донатик братюням',
        description='Оплата братюням',
        provider_token=pay_token,
        invoice_payload='Оплата братюням',
        currency='rub',
        prices=[price],
        photo_url='https://mirpozitiva.ru/wp-content/uploads/2019/11/1542866820_0019.jpg',
        photo_height=512,
        photo_width=512,
        photo_size=512,
        is_flexible=False,  # True If you need to set up Shipping Fee
        start_parameter='test-invoice-payload')
