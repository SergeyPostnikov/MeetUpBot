import datetime as dt
import db_test
import db_functions

from globals import (
bot, telebot, ACCESS_DUE_TIME, INPUT_DUE_TIME, payload, date_now, date_end, pay_token, markup_main_menu, markup_user,
markup_speaker, markup_registration, markup_faq, markup_report_true, markup_report_false, markup_form, markup_communicate,
markup_report, markup_admin_menu, markup_enroll_meetup, markup_start, markup_enter_meetup, markup_start_report,
markup_next_question, markup_start_admin_menu, markup_del_report, markup_edit_meetup)
from telebot.util import quick_markup
from telebot.types import LabeledPrice, ShippingOption
from telegram_bot_calendar.base import DAY
from telegram_bot_calendar.detailed import DetailedTelegramCalendar


admin = [933137433, ]
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


def get_report(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    user['sheet'] = 0
    reports = db_functions.get_reports()
    for report in reports:
        if report.id == int(call):
            text = f'Доклад {report.theme}\n---\n' \
                   f'{report.start_time} - {report.end_time}\n---\n' \
                   f'Ведет доклад - {report.speaker.name}\n---\n'
            user['report'] = report.id
            markup = markup_report_true
            if user['info'] == 1:
                markup = markup_start_report
            elif user['group'] == 'admin':
                markup = markup_del_report
            bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                  text=text, reply_markup=markup)


def get_users(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    user['sheet'] = 0
    users = db_functions.get_meetup_users(message.chat.id)
    for us in users:
        if us.id == int(call):
            text = f'{us.name}\n---\n' \
                   f'{us.job}\n---\n' \
                   f'{us.about}\n---\n'
            user['text'] = us.tg_name
            bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                  text=text, reply_markup=markup_communicate)



def get_markup(buttons, row_width=1):
    return quick_markup(buttons, row_width=row_width)


# Start========================================================================================
def start_bot(message: telebot.types.Message):
    tg_name = message.from_user.username
    msg = bot.send_message(message.chat.id, f'Здравствуйте, {tg_name} 😉')
    access_due = dt.datetime.now() + dt.timedelta(0, ACCESS_DUE_TIME)
    payload[message.chat.id] = {
        'callback': None,  # current callback button
        'last_msg': [],  # последние отправленные за один раз сообщения (для подчистки кнопок) -- перспектива
        'callback_source': [],  # если задан, колбэк кнопки будут обрабатываться только с этих сообщений
        'code_speakers': [],
        'code_users': [],
        'code_meetups': [],
        'code_reports': [],
        'meetup': None,
        'access_due': access_due,  # дата и время актуальности кэшированного статуса
        'form': None,
        'group': None,
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
        'report': None,
        'sheet': 0,
        'step_due': None,  # срок актуальности ожидания ввода данных (используем в callback функциях)
    }
    payload[message.chat.id]['msg_id_1'] = msg.id
    if message.chat.id in admin:
        markup = markup_start_admin_menu
        payload[message.chat.id]['group'] = 'admin'
    else:
        markup = markup_start
    msg = bot.send_message(message.chat.id, f'Вас приветствует MeetUpBot', reply_markup=markup)
    payload[message.chat.id]['msg_id_2'] = msg.id


def get_registration(message: telebot.types.Message, call, step=0):
    user = payload[message.chat.id]
    buttons = {}
    member = db_functions.search_user(user['tg_name'])
    if not member:
        if step == 0:
            msg = bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                  text=f'Введите имя')
            user['callback_source'] = [msg.id]
            bot.register_next_step_handler(message, get_registration, call, 1)
            user['step_due'] = dt.datetime.now() + dt.timedelta(0, INPUT_DUE_TIME)
        elif user['step_due'] < dt.datetime.now():
            bot.send_message(message.chat.id, 'Время ввода данных истекло. Нажмите /start')
            return
        elif step == 1:
            user['name'] = message.text
            bot.delete_message(message.chat.id, message.message_id)
            bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                  text=f'Введенное имя {user["name"]}', reply_markup=markup_start)
            db_functions.add_new_user(user['name'], message.from_user.username, message.chat.id)
        user['callback_source'] = []
    else:
        meetups = db_functions.search_meetup(date_now)
        for meetup in meetups:
            name = meetup.theme
            date = meetup.date
            user['code_meetups'].append(str(meetup.id))
            buttons.update({f'{name} - {date}': {'callback_data': meetup.id}})
        markup = get_markup(buttons)
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text=f'Выберите мероприятие из списка', reply_markup=markup)


def get_meetup(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    meetups = db_functions.search_meetup(date_now)
    for meetup in meetups:
        if str(meetup.id) == call:
            text = f'{meetup.theme}\n---\n' \
                   f'{meetup.date}\n---\n' \
                   f'{meetup.description}\n---\n'
            status = db_functions.get_status(message.chat.id, meetup)
            if not status:
                markup = markup_enroll_meetup
            elif status in ['1', '2'] and meetup.date == date_now and user['group'] != 'admin':
                markup = markup_enter_meetup
                user['group'] = status
            elif user['group'] == 'admin':
                markup = markup_edit_meetup
            else:
                markup = markup_start
            bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                  text=text, reply_markup=markup)
            user['meetup'] = call
    user['code_meetups'] = []

def get_enroll_meetup(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    meetup_theme, meetup_date = db_functions.enroll_meetup(user['meetup'], message.chat.id)
    text = f'Вы зарегистрировались на {meetup_theme} - {meetup_date}'
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                      text=text, reply_markup=markup_start)



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
    user['callback_source'] = []
    bot.clear_step_handler(message)
    if user['group'] == '1':
        markup = markup_user
    elif user['group'] == '2':
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
    member = db_functions.search_user(user['tg_name'])[0]
    if not member.job:
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text='Анкета не заполнена 😝', reply_markup=markup_form)
    else:
        buttons = {}
        users = db_functions.get_meetup_users(message.chat.id)
        for us in users[user['sheet']:user['sheet'] + 2]:
            name = us.name
            user['code_users'].append(str(us.id))
            job = us.job
            buttons.update({f'{name} - {job}': {'callback_data': us.id}})
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
        db_functions.add_user_info(user['tg_name'], user['job'], user['info'])
        user['info'] = []
    user['callback_source'] = []

def write_in_private(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Жмякни на @{user["text"]}', reply_markup=markup_main_menu)


#Ask_question======================================================================================
def ask_question(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    report = db_functions.get_current_report()
    if not report:
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text='Доклада нет 😞', reply_markup=markup_report_false)
    else:
        text = f'Идет доклад - {report.theme}\n---\n' \
               f'{report.start_time} - {report.end_time}\n---\n'\
               f'Читает доклад -  {report.speaker.name}\n---\n'
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
        db_functions.send_feedback(message.chat.id, message.text, user['report'])
    user['callback_source'] = []


def get_speaker_buttons(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    buttons = {}
    reports = db_functions.get_reports()
    for report in reports[user['sheet']:user['sheet']+2]:
        name = report.speaker.name
        user['code_speakers'].append(str(report.id))
        theme = report.theme
        buttons.update({f'{name} - {theme}': {'callback_data': report.id}})
    user['sheet'] += 2
    if user['sheet'] < len(reports):
        buttons.update({'Еще доклады': {'callback_data': 'choice_speaker'}})
    buttons.update({'Вернуться в меню': {'callback_data': 'main_menu'}})
    markup = get_markup(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Выберите доклад', reply_markup=markup)








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
    buttons = {}
    reports = db_functions.get_reports(message.chat.id)
    if reports:
        for report in reports[user['sheet']:user['sheet'] + 2]:
            name = report.speaker.name
            user['code_speakers'].append(str(report.id))
            theme = report.theme
            buttons.update({f'{name} - {theme}': {'callback_data': report.id}})
        user['sheet'] += 2
        if user['sheet'] < len(reports):
            buttons.update({'Еще доклады': {'callback_data': 'choice_speaker'}})
        buttons.update({'Вернуться в меню': {'callback_data': 'main_menu'}})
        markup = get_markup(buttons)
        user['info'] = 1

        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text=f'Выберите доклад', reply_markup=markup)
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text=f'Активных докладов нет', reply_markup=markup_main_menu)


def finished_report(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    db_functions.set_finished(user['report'])
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Доклад закончен\n'
                              , reply_markup=markup_main_menu)


def get_questions_asked(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    question = db_functions.get_current_question(user['report'])

    if question:
        user['info'] = question.id
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text=f'Вопрос от {question.member.name}\n'
                                   f'{question.text}'
                                  , reply_markup=markup_report)
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text=f'Вопросы закончились'
                              , reply_markup=markup_main_menu)

def get_set_answered(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    db_functions.set_answered(user['info'])
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Вопрос закрыт\n'
                              , reply_markup=markup_next_question)

# ADMIN MENU=======================================================================
# ADMIN MENU=======================================================================

#meetup button=======================================================================
def start_admin_menu(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    print(user['group'])
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Добро пожаловать в панель администратора, хозяин!', reply_markup=markup_admin_menu)



def get_control_meetup(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    buttons = {}
    meetups = db_functions.search_meetup(date_now)
    if meetups:
        for meetup in meetups:
            name = meetup.theme
            date = meetup.date
            user['code_meetups'].append(str(meetup.id))
            buttons.update({f'{name} - {date}': {'callback_data': meetup.id}})
        user['sheet'] += 2
        if user['sheet'] < len(meetups):
            buttons.update({'Еще мероприятия': {'callback_data': 'next_meetup'}})
    buttons.update({'Новое мероприятия': {'callback_data': 'new_meetup'}})
    buttons.update({'Вернуться в меню': {'callback_data': 'start_admin_menu'}})
    markup = get_markup(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Выберите мероприятие из списка или создайте новое', reply_markup=markup)

def get_new_meetup(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    calendar, step = WMonthTelegramCalendar(locale='ru', min_date=date_now, max_date=date_end).build()
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Выберите дату проведения мероприятия', reply_markup=calendar)


def get_recording_time(message: telebot.types.Message, call):
    pass




def edit_meetup(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    buttons = {}
    reports = db_functions.search_reports_for_id(user['meetup'])
    user['sheet'] = 0
    if reports:
        for report in reports:
            theme = report.theme
            start_time = report.start_time
            end_time = report.end_time
            name = report.speaker.name
            user['code_reports'].append(str(report.id))
            buttons.update({f'{theme} {start_time} - {end_time} {name}': {'callback_data': report.id}})
        user['sheet'] += 2
        if user['sheet'] < len(reports):
            buttons.update({'Еще доклады': {'callback_data': 'next_report'}})
    buttons.update({'Добавить доклад': {'callback_data': 'new_report'}})
    buttons.update({'Удалить мероприятие': {'callback_data': 'del_meetup'}})
    buttons.update({'Вернуться в меню': {'callback_data': 'start_admin_menu'}})
    markup = get_markup(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Выберите доклад из списка или создайте новое', reply_markup=markup)


def del_report(message: telebot.types.Message, call):
    pass

# def get_speaker(message: telebot.types.Message, call):
#     user = payload[message.chat.id]
#     user['sheet'] = 0
#     speakers = db_functions.get_meetup_users(message.chat.id)
#     for us in users:
#         if us.id == int(call):
#             text = f'{us.name}\n---\n' \
#                    f'{us.job}\n---\n' \
#                    f'{us.about}\n---\n'
#             user['text'] = us.tg_name
#             bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
#                                   text=text, reply_markup=markup_communicate)
#
# def get_control_speaker(message: telebot.types.Message, call):
#     user = payload[message.chat.id]



