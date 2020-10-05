import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

# Отправляем результаты игры
#@bot.message_handler(commands=['result'])
def result(message):
    pic = open('static/spot.png', 'rb')
    bot.send_document(message.chat.id, pic)
    bot.send_document(message.chat.id, "FILEID")