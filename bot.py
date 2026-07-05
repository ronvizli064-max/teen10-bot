import telebot
from telebot import types
import sqlite3
import time
import threading

TOKEN = "В8643989240:AAFQryzkUft_7e8apFVp_BPMSapKcTMu3Fs
CHANNEL_ID = "@vip_access_123"
PRICE = 100

bot = telebot.TeleBot(TOKEN)

# база
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER,
    expire_date INTEGER
)
""")
conn.commit()


# старт
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Купити доступ ⭐", callback_data="buy")
    markup.add(btn)

    bot.send_message(message.chat.id, "Доступ до VIP каналу 🔐", reply_markup=markup)


# купити
@bot.callback_query_handler(func=lambda call: call.data == "buy")
def buy(call):
    prices = [types.LabeledPrice(label="Підписка 30 днів", amount=PRICE)]

    bot.send_invoice(
        call.message.chat.id,
        title="VIP доступ",
        description="30 днів доступу",
        invoice_payload="sub",
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter="stars"
    )


# підтвердження
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True)


# після оплати
@bot.message_handler(content_types=['successful_payment'])
def success(message):
    user_id = message.from_user.id
    expire = int(time.time()) + 30 * 24 * 60 * 60

    cursor.execute("REPLACE INTO users (user_id, expire_date) VALUES (?, ?)", (user_id, expire))
    conn.commit()

    invite = bot.create_chat_invite_link(CHANNEL_ID, member_limit=1)

    bot.send_message(
        message.chat.id,
        f"✅ Оплата успішна!\n\nДоступ на 30 днів\n🔐 {invite.invite_link}"
    )


# перевірка
@bot.message_handler(commands=['check'])
def check(message):
    user_id = message.from_user.id

    cursor.execute("SELECT expire_date FROM users WHERE user_id=?", (user_id,))
    data = cursor.fetchone()

    if not data:
        bot.send_message(message.chat.id, "❌ Немає підписки")
        return

    if data[0] < int(time.time()):
        bot.send_message(message.chat.id, "⏳ Підписка закінчилась")
    else:
        bot.send_message(message.chat.id, "✅ Підписка активна")


# статистика
@bot.message_handler(commands=['stats'])
def stats(message):
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    bot.send_message(message.chat.id, f"👤 Користувачів: {count}")


# авто видалення
def check_subscriptions():
    while True:
        now = int(time.time())

        cursor.execute("SELECT user_id, expire_date FROM users")
        users = cursor.fetchall()

        for user_id, expire in users:
            if expire < now:
                try:
                    bot.ban_chat_member(CHANNEL_ID, user_id)
                    bot.unban_chat_member(CHANNEL_ID, user_id)
                except:
                    pass

                cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
                conn.commit()

        time.sleep(60)


threading.Thread(target=check_subscriptions).start()

print("BOT WORKING 🚀")
bot.infinity_polling()
