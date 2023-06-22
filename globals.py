import telebot


from datetime import date, timedelta
from environs import Env
from telebot.util import quick_markup


# others
INPUT_DUE_TIME = 60     # time (sec) to wait for user text input
BUTTONS_DUE_TIME = 30   # time (sec) to wait for user clicks button
ACCESS_DUE_TIME = 300   # if more time has passed since last main menu we should check access again

env = Env()
env.read_env()

tg_bot_token = env('TG_BOT_KEY')
pay_token = env('PAYMENTS_TOKEN')
bot = telebot.TeleBot(token=tg_bot_token)

date_now = date.today()
date_end = date.today() + timedelta(days=14)

payload = {}

# main menu callback buttons

markup_user = quick_markup({
    'FAQ': {'callback_data': 'get_faq'},
    'Общаться с другими': {'callback_data': 'communicate'},
    'Задать вопрос докладчику': {'callback_data': 'ask_question'},
    'Задонатить организатору': {'callback_data': 'donate'},
}, row_width=1)

markup_speaker = quick_markup({
    'FAQ 🆘': {'callback_data': 'get_faq'},
    'Общаться с другими': {'callback_data': 'communicate'},
    'Задать вопрос докладчику': {'callback_data': 'ask_question'},
    'Задонатить организатору': {'callback_data': 'donate'},
    'Начать/закончить доклад': {'callback_data': 'start_report'},
}, row_width=1)

markup_faq = quick_markup({
    'Как задать вопрос докладчику': {'callback_data': 'faq_question'},
    'Как общаться с другими': {'callback_data': 'faq_communicate'},
    'Как начать/закончить доклад': {'callback_data': 'faq_start_report'},
    'Вернуться в меню': {'callback_data': 'main_menu'},
}, row_width=1)

markup_main_menu = quick_markup({
    'Вернуться в меню': {'callback_data': 'main_menu'},
})

markup_recording_time = quick_markup({
    'Выбрать время': {'callback_data': 'recording_time'},
    'Вернуться в меню': {'callback_data': 'cancel_step'},
}, row_width=1)

markup_registration = quick_markup({
    'Оплатить': {'callback_data': 'registration_pay', 'pay': True},
    'Вернуться в меню': {'callback_data': 'main_menu'},
}, row_width=1)

markup_report_true = quick_markup({
    'Задать вопрос 🤔': {'callback_data': 'ask_question_a_speaker'},
    'Выбор спикера': {'callback_data': 'choice_speaker'},
    'Вернуться в меню': {'callback_data': 'main_menu'},
}, row_width=1)

markup_report_false = quick_markup({
    'Выбор спикера': {'callback_data': 'choice_speaker'},
    'Вернуться в меню': {'callback_data': 'main_menu'},
}, row_width=1)


markup_form = quick_markup({
    'Заполнить анкету 📝': {'callback_data': 'fill_out_a_form'},
    'Вернуться в меню': {'callback_data': 'main_menu'},
}, row_width=1)

markup_communicate = quick_markup({
    'Написать в личку 🖊': {'callback_data': 'write_in_private'},
    'Вернуться в меню': {'callback_data': 'main_menu'},
}, row_width=1)

markup_report = quick_markup({
    'Прочитать вопросы': {'callback_data': 'get_question'},
    'Вернуться в меню': {'callback_data': 'main_menu'},
}, row_width=1)

markup_question = quick_markup({
    'Еще вопросы': {'callback_data': 'get_question'},
    'Вернуться в меню': {'callback_data': 'main_menu'},
}, row_width=1)