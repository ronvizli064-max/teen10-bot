import telebot

TOKEN = @BotFather

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Бот працює 🚀")

bot.polling()
