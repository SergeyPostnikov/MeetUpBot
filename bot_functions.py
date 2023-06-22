import datetime as dt
import db_test

from globals import (
bot, telebot, ACCESS_DUE_TIME, INPUT_DUE_TIME, payload, date_now, date_end, pay_token, markup_main_menu, markup_user,
markup_speaker, markup_registration, markup_faq, markup_report_true, markup_report_false, markup_form, markup_communicate,
markup_report, markup_question)
from telebot.util import quick_markup
from telebot.types import LabeledPrice, ShippingOption
from telegram_bot_calendar.base import DAY
from telegram_bot_calendar.detailed import DetailedTelegramCalendar


shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]


class WMonthTelegramCalendar(DetailedTelegramCalendar):
    first_step = DAY


def get_calls(var, func):
    calls = {}
    for id in var:
        calls.update({f'{id}': func})
    return calls


def get_speaker(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    user['sheet'] = 0
    speakers = db_test.speakers
    for speaker in speakers:
        if speaker['name'] == call:
            text = f'{speaker["name"]}\n---\n' \
                   f'{speaker["job"]}\n---\n' \
                   f'{speaker["info"]}\n---\n'
            bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                  text=text, reply_markup=markup_report_true)


def get_users(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    user['sheet'] = 0
    users = db_test.users
    for us in users:
        if us['name'] == call:
            text = f'{us["name"]}\n---\n' \
                   f'{us["job"]}\n---\n' \
                   f'{us["info"]}\n---\n'
            bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                  text=text, reply_markup=markup_communicate)

def get_markup(buttons, row_width=1):
    return quick_markup(buttons, row_width=row_width)


# Start========================================================================================
def start_bot(message: telebot.types.Message):
    tg_name = message.from_user.username
    msg = bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.username} 😉')
    access_due = dt.datetime.now() + dt.timedelta(0, ACCESS_DUE_TIME)
    user_group = 2
    payload[message.chat.id] = {
        'callback': None,  # current callback button
        'last_msg': [],  # последние отправленные за один раз сообщения (для подчистки кнопок) -- перспектива
        'callback_source': [],  # если задан, колбэк кнопки будут обрабатываться только с этих сообщений
        'code_speakers': [],
        'code_users': [],
        'access_due': access_due,  # дата и время актуальности кэшированного статуса
        'form': None,
        'name': None,
        'job': None,
        'date': None,
        'time': None,
        'donate': None,
        'msg_id_1': None,
        'msg_id_2': None,
        'tg_name': tg_name,
        'tg_id': message.chat.id,
        'text': None,
        'info': None,
        'report': False,
        'sheet': 0,
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
    user['sheet'] = 0
    user_group = 2
    user['callback_source'] = []
    bot.clear_step_handler(message)
    if user_group == 1:
        markup = markup_user
    elif user_group == 2:
        markup = markup_speaker
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Приветственное сообщение, рассказываю что могу 🥳', reply_markup=markup)

#FAQ
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




# Communicate========================================================================================
def get_communicate(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    if not user['form']:
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text='Анкета не заполнена 😝', reply_markup=markup_form)
    else:
        buttons = {}
        users = db_test.users
        for us in users[user['sheet']:user['sheet'] + 2]:
            name = us['name']
            user['code_users'].append(name)
            job = us['job']
            buttons.update({f'{name} - {job}': {'callback_data': name}})
        user['sheet'] += 2
        if user['sheet'] < len(users):
            buttons.update({'Еще анкеты': {'callback_data': 'communicate'}})
        buttons.update({'Вернуться в меню': {'callback_data': 'main_menu'}})
        markup = get_markup(buttons)
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text=f'Анкеты открытые для общения', reply_markup=markup)


def fill_out_a_form(message: telebot.types.Message, order_id, step=0):
    user = payload[message.chat.id]
    if step == 0:
        msg = bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                    text='Введите вашу профессию', reply_markup=markup_main_menu)
        user['callback_source'] = [msg.id]
        bot.register_next_step_handler(message, fill_out_a_form, order_id, 1)
        user['step_due'] = dt.datetime.now() + dt.timedelta(0, INPUT_DUE_TIME)
    elif user['step_due'] < dt.datetime.now():
        bot.send_message(message.chat.id, 'Время ввода данных истекло. Нажмите /start')
        return
    elif step == 1:
        user['job'] = message.text
        bot.delete_message(message.chat.id, message.message_id)
        msg = bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text=f'Введите краткую информацию о вас', reply_markup=markup_main_menu)
        user['callback_source'] = [msg.id]
        bot.register_next_step_handler(message, fill_out_a_form, order_id, 2)
        user['step_due'] = dt.datetime.now() + dt.timedelta(0, INPUT_DUE_TIME)
    elif step == 2:
        user['info'] = message.text
        bot.delete_message(message.chat.id, message.message_id)
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text=f'Анкета заполнена 🥳', reply_markup=markup_main_menu)
        user['form'] = True
    user['callback_source'] = []

def write_in_private(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Жмякни на @Sergey_Postnikov', reply_markup=markup_main_menu)


#Ask_question======================================================================================
def ask_question(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    speakers = db_test.speakers
    title = None
    for speaker in speakers:
        if speaker['report_now']:
            title = speaker['report_title']
            name = speaker['name']
            info = speaker['info']
    if not title:
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text='Доклада нет 😞', reply_markup=markup_report_false)
    else:
        text = f'Идет доклад - {title}\n---\n' \
               f'Читает доклад -  {name}\n---\n' \
               f'{info}\n---\n'
        # user['chat'] = spiker_id
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text=text, reply_markup=markup_report_true)

def ask_question_a_speaker(message: telebot.types.Message, order_id, step=0):
    user = payload[message.chat.id]
    if step == 0:
        msg = bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text='Введите вопрос', reply_markup=markup_main_menu)
        user['callback_source'] = [msg.id]
        bot.register_next_step_handler(message, ask_question_a_speaker, order_id, 1)
        user['step_due'] = dt.datetime.now() + dt.timedelta(0, INPUT_DUE_TIME)
    elif user['step_due'] < dt.datetime.now():
        bot.send_message(message.chat.id, 'Время ввода данных истекло. Нажмите /start')
        return
    elif step == 1:
        user['text'] = message.text
        bot.delete_message(message.chat.id, message.message_id)
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                    text=f'Вопрос отправлен', reply_markup=markup_main_menu)
        # msg = bot.send_message(message.chat.id, 'Вопрос спикеру 🥳')
    user['callback_source'] = []


def get_speaker_buttons(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    buttons = {}
    speakers = db_test.speakers
    for speaker in speakers[user['sheet']:user['sheet']+2]:
        name = speaker['name']
        user['code_speakers'].append(name)
        job = speaker['job']
        buttons.update({f'{name} - {job}': {'callback_data': name}})
    user['sheet'] += 2
    if user['sheet'] < len(speakers):
        buttons.update({'Еще спикеры': {'callback_data': 'choice_speaker'}})
    buttons.update({'Вернуться в меню': {'callback_data': 'main_menu'}})
    markup = get_markup(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Выберите спикера', reply_markup=markup)








#Donate========================================================================================
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


 # speaker button=========================================================================

def start_report(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    user['report'] = True if not user['report'] else False
    if user['report']:
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Ваш доклад стартует {dt.datetime.now().time()}\n'
                               f'По окончанию не забудьте кликнуть "закончить доклад"'
                              , reply_markup=markup_report)
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text=f'Ваш доклад закончен {dt.datetime.now().time()}'
                              , reply_markup=markup_report)
def get_question(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    users = db_test.questions
    if user['sheet'] < len(users):
        name = users[user['sheet']]['name']
        question = users[user['sheet']]['question']
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text=f'{name}\n\n'
                                   f'{question}'
                              , reply_markup=markup_question)
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text=f'Вопросы закончились', reply_markup=markup_main_menu)
    user['sheet'] += 1
