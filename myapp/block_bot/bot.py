import time
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from django.conf import settings
from telegram_bot_pagination import InlineKeyboardPaginator
import random
from ..models import *


bot = Bot(token='5165224717:AAE_8zHzEOMaaMLee4ME7_TbM8q65iR67YI')

hostname = f'{settings.HOST}/bot'
print(f'Working host at: {hostname}')
bot.set_webhook(hostname)

dispatcher = Dispatcher(bot, None)
global_response = {}
global_page = {}
question_id = {}
stop = {}
test_name = {}


def userid(update):
    return update.effective_user.id


def start(update, context):
    update.message.reply_text(f'Abyuturentlar uchun teslar.\n\n'
                              f'Testni boshalsh -- /test\n'
                              f'Qo\'shimcha malumot -- /contact')


def test(update, context):
    keyboard = [
        [KeyboardButton('Kimyo',),
         KeyboardButton('Bioloyiya')],
        [KeyboardButton('Matematika')],
        [KeyboardButton('Ingliz tili'),
         KeyboardButton('Tarix')],
    ]
    update.message.reply_text(text='Bizda mavjud testlar',
                              reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))


def begin(update, context):
    course = update.message.text
    if course == 'Kimyo':
        random_base = [i for i in Kimyo.objects.all().values()]
        question_id[userid(update)] = (random.sample(random_base, 5))
        for x in range(1, len(random_base)):
            question_id[userid(update)][x - 1].setdefault("nomer", x)
        test_name[userid(update)] = course
        keyboard = [
            [KeyboardButton(text='Testni boshlash')],
            [KeyboardButton(text='Orqaga')]
        ]
        update.message.reply_text(text=f'Ism: {update.effective_user.first_name}\n'
                                       f'Fan: {course}\n'
                                       f'Vaqt: 30 minut',
                                  reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True,
                                                                   one_time_keyboard=True))
        return middle_handler(update, context)
    elif course == 'Tarix':
        pass
    elif course == 'Ingliz tili':
        pass
    elif course == 'Matematika':
        pass
    elif course == 'Bioloyiya':
        pass
        # test_name[userid(update)] = course
        # keyboard = [
        #     [KeyboardButton(text='Bowlash')],
        #     [KeyboardButton(text='Orqaga')]
        # ]
        # update.message.reply_text(text=f'Ism: {update.effective_user.first_name}\n'
        #                                f'Fan: {course}\n'
        #                                f'Vaqt: 30 minut',
        #                           reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True,
        #                                                            one_time_keyboard=True))
        return middle_handler(update, context)
    else:
        return middle_handler(update, context)


def middle_handler(update, context):
    course = update.message.text
    if course == 'Testni boshlash' or course == 'Orqaga':
        if course == 'Testni boshlash':
            Users.objects.create(username=update.effective_user.username, test_name=test_name[userid(update)])
            return countdown(update, context)
        elif course == 'Orqaga':
            return test(update, context)
    else:
        pass


def test_begin(update, context):
    global_response[userid(update)] = {}
    global_page[userid(update)] = 1
    stop[userid(update)] = None
    paginator = InlineKeyboardPaginator(
        len(question_id[userid(update)]),
    )

    random_answer = ['a_answer', 'b_answer', 'c_answer', 'd_answer']
    selected_random_answer = random.sample(random_answer, 4)
    paginator.add_before(
        InlineKeyboardButton(text=question_id[userid(update)][0][selected_random_answer[0]],
                             callback_data=selected_random_answer[0]))
    paginator.add_before(
        InlineKeyboardButton(text=question_id[userid(update)][0][selected_random_answer[1]],
                             callback_data=selected_random_answer[1]))
    paginator.add_before(
        InlineKeyboardButton(text=question_id[userid(update)][0][selected_random_answer[2]],
                             callback_data=selected_random_answer[2]))
    paginator.add_before(
        InlineKeyboardButton(text=question_id[userid(update)][0][selected_random_answer[3]],
                             callback_data=selected_random_answer[3]))
    # update.message.reply_photo(photo=open(question_id[userid(update)][0]['question_image'], 'rb'))
    update.message.reply_text(
        f"№ {question_id[userid(update)][0]['nomer']}\n{question_id[userid(update)][0]['question']}",
        reply_markup=paginator.markup,
    )


def test_query(update, context):
    query = update.callback_query
    query.answer()
    data = query.data
    if data == 'a_answer' or data == 'b_answer' or data == 'c_answer' or data == 'd_answer':
        global_response[userid(update)][question_id[userid(update)][global_page[userid(update)] - 1]['id']] = data
        if question_id[userid(update)][-1] == question_id[userid(update)][int(global_page[userid(update)] - 1)]:
            pop = int(global_page[userid(update)] - 1)
            global_page[userid(update)] = pop
            question_id[userid(update)].pop(pop)
            paginator = InlineKeyboardPaginator(
                page_count=len(question_id[userid(update)]),
                current_page=pop,
            )
            response = pop - 1
            random_answer = ['a_answer', 'b_answer', 'c_answer', 'd_answer']
            selected_random_answer = random.sample(random_answer, 4)

            paginator.add_before(
                InlineKeyboardButton(text=question_id[userid(update)][response][selected_random_answer[0]],
                                     callback_data=selected_random_answer[0]))
            paginator.add_before(
                InlineKeyboardButton(text=question_id[userid(update)][response][selected_random_answer[1]],
                                     callback_data=selected_random_answer[1]))
            paginator.add_before(
                InlineKeyboardButton(text=question_id[userid(update)][response][selected_random_answer[2]],
                                     callback_data=selected_random_answer[2]))
            paginator.add_before(
                InlineKeyboardButton(text=question_id[userid(update)][response][selected_random_answer[3]],
                                     callback_data=selected_random_answer[3]))
            paginator.add_after(
                InlineKeyboardButton(text='🛑 Testni yakunlash 🛑', callback_data='stop'))
            # update.message.reply_photo(photo=open(question_id[userid(update)][response]['question_image'], 'rb'))
            query.edit_message_text(
                text=f"№ {question_id[userid(update)][response]['nomer']}\n{question_id[userid(update)][response]['question']}",
                reply_markup=paginator.markup,
                parse_mode='Markdown'
            )
        else:
            page_num = int(global_page[userid(update)])
            question_id[userid(update)].pop(page_num - 1)
            paginator = InlineKeyboardPaginator(
                page_count=len(question_id[userid(update)]),
                current_page=page_num,
            )
            response = page_num - 1
            random_answer = ['a_answer', 'b_answer', 'c_answer', 'd_answer']
            selected_random_answer = random.sample(random_answer, 4)

            paginator.add_before(
                InlineKeyboardButton(text=question_id[userid(update)][response][selected_random_answer[0]],
                                     callback_data=selected_random_answer[0]))
            paginator.add_before(
                InlineKeyboardButton(text=question_id[userid(update)][response][selected_random_answer[1]],
                                     callback_data=selected_random_answer[1]))
            paginator.add_before(
                InlineKeyboardButton(text=question_id[userid(update)][response][selected_random_answer[2]],
                                     callback_data=selected_random_answer[2]))
            paginator.add_before(
                InlineKeyboardButton(text=question_id[userid(update)][response][selected_random_answer[3]],
                                     callback_data=selected_random_answer[3]))
            paginator.add_after(
                InlineKeyboardButton(text='🛑 Testni yakunlash 🛑', callback_data='stop'))
            # update.message.reply_photo(photo=open(question_id[userid(update)][response]['question_image'], 'rb'))
            query.edit_message_text(
                text=f"№ {question_id[userid(update)][response]['nomer']}\n{question_id[userid(update)][response]['question']}",
                reply_markup=paginator.markup,
                parse_mode='Markdown'
            )
    elif data == 'stop':
        stop[userid(update)] = 'stop'
    elif data == 'Ha':
        error(update, context)
    else:
        int_data = int(data)
        global_page[userid(update)] = int_data
        paginator = InlineKeyboardPaginator(
            page_count=len(question_id[userid(update)]),
            current_page=int_data,
        )
        response = global_page[userid(update)] - 1
        random_answer = ['a_answer', 'b_answer', 'c_answer', 'd_answer']
        selected_random_answer = random.sample(random_answer, 4)

        paginator.add_before(
            InlineKeyboardButton(text=question_id[userid(update)][response][selected_random_answer[0]],
                                 callback_data=selected_random_answer[0]))
        paginator.add_before(
            InlineKeyboardButton(text=question_id[userid(update)][response][selected_random_answer[1]],
                                 callback_data=selected_random_answer[1]))
        paginator.add_before(
            InlineKeyboardButton(text=question_id[userid(update)][response][selected_random_answer[2]],
                                 callback_data=selected_random_answer[2]))
        paginator.add_before(
            InlineKeyboardButton(text=question_id[userid(update)][response][selected_random_answer[3]],
                                 callback_data=selected_random_answer[3]))
        paginator.add_after(
            InlineKeyboardButton(text='🛑 Testni yakunlash 🛑', callback_data='stop'))
        # update.message.reply_photo(photo=open(question_id[userid(update)][response]['question_image'], 'rb'))
        query.edit_message_text(
            text=f"№ {question_id[userid(update)][response]['nomer']}\n{question_id[userid(update)][response]['question']}",
            reply_markup=paginator.markup,
            parse_mode='Markdown'
        )


def countdown(update, context):
    time_sec = 19
    b = update.message.reply_text(text="00:20")
    test_begin(update, context)
    for x in range(time_sec):
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        context.bot.edit_message_text(text=timeformat, message_id=b.message_id,
                                      chat_id=update.message.chat_id)
        time.sleep(1)
        time_sec -= 1
        if time_sec == 0 or len(global_response[userid(update)]) == 5 or stop[userid(update)] == 'stop':
            context.bot.delete_message(chat_id=b.chat_id, message_id=b.message_id)
            context.bot.delete_message(chat_id=b.chat_id, message_id=b.message_id + 1)
            return help(update, context)


def help(update, context):
    summa = 0
    for key, value in global_response.items():
        if key == userid(update):
            for kalit, qiymat in value.items():
                if qiymat == 'a_answer':
                    summa += 1
    keyboard = [
                   InlineKeyboardButton(text='❌ Xatolarni ko\'rish ❌', callback_data='Ha'),
               ],
    update.message.reply_text(f'Test Yakunlandi\n\nTo`g`ri javoblar: {summa} ta\n'
                              f'Noto`g\'ri javoblar: {len(global_response[userid(update)]) - summa} ta\n'
                              f'Javobsiz testlar: {len(question_id[userid(update)])} ta',
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))


def error(update, context):
    query = update.callback_query
    query.answer()
    for key, value in global_response.items():
        if key == userid(update):
            for kalit, qiymat in value.items():
                if qiymat == 'b_answer':
                    sav = Kimyo.objects.get(id=kalit)
                    query.message.reply_text(
                        f"{sav.question}\n) {sav.a_answer}✅\n) {sav.b_answer}❌\n) {sav.c_answer}\n) {sav.d_answer}")
                elif qiymat == 'c_answer':
                    sav = Kimyo.objects.get(id=kalit)
                    query.message.reply_text(
                        f"{sav.question}\n) {sav.a_answer}✅\n) {sav.b_answer}\n) {sav.c_answer}❌\n) {sav.d_answer}")
                elif qiymat == 'd_answer':
                    sav = Kimyo.objects.get(id=kalit)
                    query.message.reply_text(
                        f"{sav.question}\n) {sav.a_answer}✅\n) {sav.b_answer}\n) {sav.c_answer}\n) {sav.d_answer}❌")
    global_response[userid(update)] = {}


def contact(update, context):
    update.message.reply_text(f'Q\'oshimcha malumot uchun: admin\n'
                              f'Test haqida malumot uchun: test admin')


dispatcher.add_handler(CommandHandler('contact', contact))
dispatcher.add_handler(CommandHandler('start', start))

dispatcher.add_handler(CommandHandler('test', test))
dispatcher.add_handler(MessageHandler(Filters.text, begin))

dispatcher.add_handler(MessageHandler(Filters.text, middle_handler))
dispatcher.add_handler(CommandHandler('test_begin', test_begin))

dispatcher.add_handler(CallbackQueryHandler(test_query))
dispatcher.add_handler(CommandHandler('countdown', countdown))

dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CallbackQueryHandler(error))


