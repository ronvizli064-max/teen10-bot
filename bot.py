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
    bot.send_message(
        message.chat.id,
        "👋 Привіт!\n\n"
        "💎 Доступ до каналу\n"
        "⏳ 30 днів\n"
        "Натисни /buy"
    )

# 🔹 купити (РЕАЛЬНА ОПЛАТА)
@bot.message_handler(commands=['buy'])
def buy(message):
    bot.send_invoice(
        chat_id=message.chat.id,
        title="Доступ до каналу",
        description="30 днів доступу",
        invoice_payload="channel_access",
        provider_token="",  # для Stars пусто
        currency="XTR",
        prices=[{"label": "30 днів доступу", "amount": 100}]
    )

# 🔹 підтвердження перед оплатою
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# 🔹 після оплати
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    user_id = message.from_user.id
    give_access(user_id)

# 🔹 видати доступ
def give_access(user_id):
    expiry = time.time() + 30 * 24 * 60 * 60
    users[user_id] = expiry

    bot.send_message(user_id, "✅ Оплата пройшла!\nДоступ видано на 30 днів ⏳")

    try:
        # створюємо інвайт (разовий)
        invite = bot.create_chat_invite_link(
            CHANNEL_ID,
            member_limit=1
        )
        bot.send_message(user_id, f"🔗 Ось доступ: {invite.invite_link}")

    except Exception as e:
        bot.send_message(user_id, "⚠️ Бот має бути адміном каналу з правом запрошень")

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

# 🔹 запуск потоку
threading.Thread(target=check_subscriptions, daemon=True).start()

print("BOT STARTED")
bot.infinity_polling()
