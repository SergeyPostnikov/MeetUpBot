import datetime as dt
import bot_functions as calls
import db_functions

from globals import (
    bot, telebot, date_now,
    date_end, payload, markup_add_meetup, markup_stat_donate
)
from bot_functions import shipping_options
from telegram_bot_calendar import LSTEP
from telegram_bot_calendar.base import DAY
from telegram_bot_calendar.detailed import DetailedTelegramCalendar


calls_map = {
    'get_faq': calls.get_faq,
    'faq_question': calls.get_faq_question,
    'faq_communicate': calls.get_faq_communicate,
    'faq_start_report': calls.get_faq_start_report,
    'main_menu': calls.main_menu,
    'donate': calls.get_donate,
    'registration_pay': calls.get_registration_pay,
    'communicate': calls.get_communicate,
    'ask_question': calls.ask_question,
    'ask_question_a_speaker': calls.ask_question_a_speaker,
    'choice_speaker': calls.get_speaker_buttons,
    'fill_out_a_form': calls.fill_out_a_form,
    'write_in_private': calls.write_in_private,
    'start_report': calls.start_report,
    'get_registration': calls.get_registration,
    'enroll_meetup': calls.get_enroll_meetup,
    'enter_meetup': calls.main_menu,
    'finished_report': calls.finished_report,
    'questions_asked': calls.get_questions_asked,
    'close_question': calls.get_set_answered,
    'next_questions': calls.get_questions_asked,
    'start_admin_menu': calls.start_admin_menu,
    'next_meetup': calls.get_control_meetup,
    'control_meetup': calls.get_control_meetup,
    'del_report': calls.del_report,
    'edit_meetup': calls.edit_meetup,
    'next_report': calls.edit_meetup,
    'new_meetup': calls.get_new_meetup,
    'recording_time': calls.get_recording_time,
    'add_meetup': calls.add_meetup,
    'new_report': calls.get_new_report,
    'next_speaker': calls.get_new_report,
    'new_speaker': calls.add_new_speaker,
    'del_meetup': calls.del_meetup,
    'del_speaker': calls.del_speaker,
    'send_mail': calls.send_mail,
    'add_message': calls.prepare_mail,
    'donat_statistic': calls.select_date_statistic,
    'statistic': calls.get_statistic



}



class WMonthTelegramCalendar(DetailedTelegramCalendar):
    first_step = DAY


@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    calls.start_bot(message)


@bot.message_handler()
def get_text(message):
    if calls.check_user_in_cache(message):
        bot.delete_message(message.chat.id, message.message_id)


#для календаря при регистрации ивента
@bot.callback_query_handler(func=WMonthTelegramCalendar.func())
def cal(c):
    user = payload[c.message.chat.id]
    result, key, step = WMonthTelegramCalendar(locale='ru', min_date=date_now, max_date=date_end).process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        if user['status'] == 'statistic':
            markup = markup_stat_donate
        else:
            markup = markup_add_meetup
        bot.edit_message_text(f"Вы выбрали {result}",
                              c.message.chat.id,
                              c.message.message_id, reply_markup=markup)
    user['date'] = result


@bot.callback_query_handler(func=lambda call: call.data)
def handle_buttons(call):
    user = calls.check_user_in_cache(call.message)
    if not user:
        return
    source = user['callback_source']
    if source and not call.message.id in user['callback_source']:
        bot.send_message(call.message.chat.id, 'Кнопка не актуальна')
        return
    elif (dt.datetime.now()-dt.timedelta(0, 180)) > dt.datetime.fromtimestamp(call.message.date):
        bot.send_message(call.message.chat.id, 'Срок действия кнопок истек. Нажмите /start и начните заново')
        return
    if user['callback']:
        bot.send_message(call.message.chat.id,
                         f'Вы находитесь в режиме '
                         f'ввода данных другой команды.\n'
                         f'Сначала завершите ее или отмените')
        return
    if call.data in user['code_speakers']:
        speakers = user['code_speakers']
        calls_speaker = calls.get_calls(speakers, calls.get_speaker)
        calls_speaker[call.data](call.message, call.data)
    elif call.data in user['code_users']:
        users = user['code_users']
        calls_user = calls.get_calls(users, calls.get_users)
        calls_user[call.data](call.message, call.data)
    elif call.data in user['code_meetups']:
        meetups = user['code_meetups']
        calls_meetup = calls.get_calls(meetups, calls.get_meetup)
        calls_meetup[call.data](call.message, call.data)
    elif call.data in user['code_reports']:
        reports = user['code_reports']
        calls_meetup = calls.get_calls(reports, calls.get_report)
        calls_meetup[call.data](call.message, call.data)
    elif call.data in user['last_msg']:
        time_reports = user['last_msg']
        calls_meetup = calls.get_calls(time_reports, calls.add_report)
        calls_meetup[call.data](call.message, call.data)
    else:
        calls_map[call.data](call.message, call.data)


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Повторите попытку позже!')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message='Инопланетяне пытались украсть CVV вашей карты, но мы успешно защитили '
                                                'ваши учетные данные. Попробуй заплатить еще раз через несколько минут, '
                                                'нам нужен небольшой отдых.')


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    user = payload[message.chat.id]
    db_functions.add_donate(message.chat.id, user['donate'])
    calls.start_bot(message)


bot.polling(none_stop=True, interval=1)
