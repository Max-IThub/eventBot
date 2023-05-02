import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import string
import urllib.parse
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token='5875098846:AAEJJsE24iKLC_Dk6H_Btd-gVRm_09UKi8k', use_context=True)

dispatcher = updater.dispatcher

admin_ids = ["453456091"]

promo_codes = {}

task_counter = {}

def start(update, context):
    update.message.reply_text('👾Добро пожаловать в игру!👾')

def about(update, context):
    update.message.reply_text('Правила просты - выполняй задания и присылай мне промокоды от организаторов!👾👾👾')

def generate_promo_code():
    promo_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return promo_code

def gen_promo(update, context):
    user_id = str(update.message.chat_id)
    if user_id in admin_ids:
        promo_code = generate_promo_code()
        promo_codes[promo_code] = False
        update.message.reply_text(f"{promo_code}")
    else:
        update.message.reply_text("Недостаточно прав для выполнения этой команды.🤯")

def handle_message(update, context):
    user_id = str(update.message.chat_id)
    message_text = update.message.text
    if message_text in promo_codes and not promo_codes[message_text]:
        promo_codes[message_text] = True
        if user_id in task_counter:
            task_counter[user_id] += 1
        else:
            task_counter[user_id] = 1
        update.message.reply_text(f"Вы выполнили {task_counter[user_id]} заданий.")
    else:
        update.message.reply_text("Неверный или не действительный промокод.🤯")

def get_stat(update, context):
    if str(update.message.chat_id) in admin_ids:
        stats = []
        for user_id, count in task_counter.items():
            user_link = f"@{context.bot.get_chat(user_id).username}" 
            stats.append(f"Участник: {user_link}, Выполнил: {count} заданий")
        if stats:
            update.message.reply_text("\n".join(stats))
        else:
            update.message.reply_text("Статистика пуста.")
    else:
        update.message.reply_text("Недостаточно прав для выполнения этой команды.🤯")

def danger_delete(update, context):
    if str(update.message.chat_id) in admin_ids:
        task_counter.clear()
        promo_codes.clear()
        update.message.reply_text('Все данные были удалены.')
    else:
        update.message.reply_text('ACCESS DENIED!!! ОБНАРУЖЕН ДИВЕРСАНТ!!!🤯')


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('about', about))
dispatcher.add_handler(CommandHandler('gen_promo', gen_promo))
dispatcher.add_handler(CommandHandler('get_stat', get_stat))
dispatcher.add_handler(CommandHandler('DangerDeleteEverythingNow', danger_delete))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling()
