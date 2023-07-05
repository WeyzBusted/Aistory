python
import random
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

TOKEN = '6266894289:AAFqWeUo2gZTstXXm193AWGMF-yup-EuidM'
bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

power_dict = {}  # Словарь для хранения власти пользователей

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Отлично, теперь у меня больше власти.")

def vlast(update, context):
    user_id = update.effective_user.id
    power = random.randint(1, 10)
    if user_id in power_dict:
        power_dict[user_id] += power
    else:
        power_dict[user_id] = power
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вы получили {power} власти.")

def den(update, context):
    sorted_power = sorted(power_dict.items(), key=lambda x: x[1], reverse=True)
    top_players = []
    for i, (user_id, power) in enumerate(sorted_power):
        user = context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=user_id).user
        top_players.append(f"{i+1}. {user.username} - {power}")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Топ игроков власти за день:\n" + "\n".join(top_players))

def top(update, context):
    sorted_power = sorted(power_dict.items(), key=lambda x: x[1], reverse=True)
    top_players = []
    for i, (user_id, power) in enumerate(sorted_power):
        user = context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=user_id).user
        top_players.append(f"{i+1}. {user.username} - {power}")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Топ игроков за все время:\n" + "\n".join(top_players))

def duel(update, context):
    user_id = update.effective_user.id
    mentioned_user_id = update.message.reply_to_message.from_user.id
    if user_id not in power_dict or mentioned_user_id not in power_dict:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Участвующие пользователи должны иметь власть.")
        return
    user_power = power_dict[user_id]
    mentioned_user_power = power_dict[mentioned_user_id]
    if user_power > mentioned_user_power:
        power_dict[user_id] += random.randint(1, 10)
        power_dict[mentioned_user_id] -= random.randint(1, 10)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Победа! Вы получили власть.")
    elif user_power < mentioned_user_power:
        power_dict[user_id] -= random.randint(1, 10)
        power_dict[mentioned_user_id] += random.randint(1, 10)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Поражение! Вы потеряли власть.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ничья! Власть не изменилась.")

start_handler = CommandHandler('start', start)
vlast_handler = CommandHandler('vlast', vlast)
den_handler = CommandHandler('den', den)
top_handler = CommandHandler('top', top)
duel_handler = CommandHandler('duel', duel)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(vlast_handler)
dispatcher.add_handler(den_handler)
dispatcher.add_handler(top_handler)
dispatcher.add_handler(duel_handler)

updater.start_polling()
