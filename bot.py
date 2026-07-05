import telebot

TOKEN = "ТУТ_ВСТАВ_СВІЙ_ТОКЕН"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Натисни /buy щоб купити доступ ⭐")

@bot.message_handler(commands=['buy'])
def buy(message):
    bot.send_message(message.chat.id, "Тут буде оплата (далі додамо ⭐)")

bot.polling()
