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
date_end = date.today() + timedelta(days=28)
time_report = [
    '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
    '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00'
]

payload = {}

# main menu callback buttons
# user buttons# =======================================================================

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

markup_registration = quick_markup({
    'Оплатить': {'callback_data': 'registration_pay', 'pay': True},
    'Вернуться в меню': {'callback_data': 'main_menu'},
}, row_width=1)

markup_report_true = quick_markup({
    'Задать вопрос 🤔': {'callback_data': 'ask_question_a_speaker'},
    'Выбор доклада': {'callback_data': 'choice_speaker'},
    'Вернуться в меню': {'callback_data': 'main_menu'},
}, row_width=1)

markup_report_false = quick_markup({
    'Выбор доклада': {'callback_data': 'choice_speaker'},
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
    'Закрыть вопрос': {'callback_data': 'close_question'},
    'Вернуться в меню': {'callback_data': 'main_menu'},
}, row_width=1)

markup_enroll_meetup = quick_markup({
    'Записаться': {'callback_data': 'enroll_meetup'},
    'Назад': {'callback_data': 'get_registration'},
}, row_width=1)

markup_enter_meetup = quick_markup({
    'Войти в меню': {'callback_data': 'enter_meetup'},
    'Назад': {'callback_data': 'get_registration'},
}, row_width=1)

markup_start = quick_markup({
    'Посмотреть события': {'callback_data': 'get_registration'},
}, row_width=1)

markup_start_report = quick_markup({
    'Завершить доклад': {'callback_data': 'finished_report'},
    'Вопросы по докладу': {'callback_data': 'questions_asked'},
    'Вернуться в меню': {'callback_data': 'main_menu'},
}, row_width=1)

markup_next_question = quick_markup({
    'Следующий вопрос': {'callback_data': 'next_questions'},
    'Вернуться в меню': {'callback_data': 'main_menu'},
}, row_width=1)

# ADMIN buttons=============================================================================

markup_start_admin_menu = quick_markup({
    'Главное меню': {'callback_data': 'start_admin_menu'},
}, row_width=1)

markup_admin_menu = quick_markup({
    'Мероприятия': {'callback_data': 'control_meetup'},
    'Создать рассылку': {'callback_data': 'add_message'},
    'Статистика доната': {'callback_data': 'donat_statistic'},
}, row_width=1)

markup_edit_meetup = quick_markup({
    'Управление мероприятие': {'callback_data': 'edit_meetup'},
    'Главное меню': {'callback_data': 'start_admin_menu'}
}, row_width=1)

markup_add_meetup = quick_markup({
    'Ввести название мероприятия': {'callback_data': 'add_meetup'},
    'Вернуться в меню': {'callback_data': 'start_admin_menu'},
}, row_width=1)

markup_del_report = quick_markup({
    'Удалить доклад': {'callback_data': 'del_report'},
    'Главное меню': {'callback_data': 'start_admin_menu'}
}, row_width=1)

markup_recording_time = quick_markup({
    'Выбрать время': {'callback_data': 'recording_time'},
    'Главное меню': {'callback_data': 'start_admin_menu'}
}, row_width=1)

markup_choose_speaker = quick_markup({
    'Выбрать спикера': {'callback_data': 'recording_time'},
    'Удалить спикера': {'callback_data': 'del_speaker'},
    'Главное меню': {'callback_data': 'start_admin_menu'}
}, row_width=1)

markup_add_speaker = quick_markup({
    'Добавить спикера': {'callback_data': 'new_speaker'},
    'Назад': {'callback_data': 'new_report'}
}, row_width=1)

markup_mail = quick_markup({
    'Выбрать мероприятие': {'callback_data': 'control_meetup'},
    'Главное меню': {'callback_data': 'start_admin_menu'}
}, row_width=1)

markup_send_mail = quick_markup({
    'Ввести текст рассылки': {'callback_data': 'send_mail'},
    'Главное меню': {'callback_data': 'start_admin_menu'},
}, row_width=1)

markup_stat_donate = quick_markup({
    'Вывести статистику': {'callback_data': 'statistic'},
}, row_width=1)
