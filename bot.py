import telebot
import time
import threading

TOKEN = "8643989240:AAFQryzkUft_7e8apFVp_BPMSapKcTMu3Fs"
CHANNEL_ID = "@vip_access_123"

bot = telebot.TeleBot(TOKEN)

users = {}  # user_id: expiry_time

# 🔹 старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "👋 Привіт!\n\n"
                     "💎 Доступ до каналу\n"
                     "⏳ 30 днів\n"
                     "Натисни /buy")

# 🔹 купити
@bot.message_handler(commands=['buy'])
def buy(message):
    bot.send_message(message.chat.id,
                     "💰 Оплата через Telegram Stars ⭐\n"
                     "Після оплати ти отримаєш доступ")

    # ❗ ПОКИ ЩО емуляція оплати
    give_access(message.from_user.id)

# 🔹 видати доступ
def give_access(user_id):
    expiry = time.time() + 30 * 24 * 60 * 60
    users[user_id] = expiry

    bot.send_message(user_id, "✅ Оплата пройшла!\nДоступ видано на 30 днів ⏳")

    try:
        bot.unban_chat_member(CHANNEL_ID, user_id)
        bot.invite_link = bot.create_chat_invite_link(CHANNEL_ID)
        bot.send_message(user_id, f"🔗 Ось доступ: {bot.invite_link.invite_link}")
    except:
        bot.send_message(user_id, "⚠️ Додай бота адміном в канал")

# 🔹 перевірка підписки
def check_subscriptions():
    while True:
        now = time.time()

        for user_id in list(users.keys()):
            if users[user_id] < now:
                try:
                    bot.ban_chat_member(CHANNEL_ID, user_id)
                    bot.unban_chat_member(CHANNEL_ID, user_id)
                    bot.send_message(user_id, "🚫 Доступ закінчився")
                except:
                    pass
                del users[user_id]

        time.sleep(60)

# 🔹 запуск перевірки
threading.Thread(target=check_subscriptions).start()

print("BOT STARTED")
bot.infinity_polling()
