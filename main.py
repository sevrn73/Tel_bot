import telebot
import config
import game
import generator

bot = telebot.TeleBot(config.TOKEN)

# Стартовая информация и управление
@bot.message_handler(commands=['start'])
def start(message):
    # Создание кнопок
    markup = telebot.types.ReplyKeyboardMarkup(True, True)
    item1 = telebot.types.KeyboardButton('Создать модель')
    item2 = telebot.types.KeyboardButton('Поиграть в SimGame')
    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Привет, ты написал боту SimGame2020. "
                                      "Я могу создать простую модель для симулятора OPM и поиграть в игру.",
                     parse_mode='html', reply_markup=markup)


# Стартуем события
def start_funk(message):
    if message.chat.type == 'private':
        if message.text == 'Создать модель':
            generator.create_model()

        if message.text == 'Поиграть в SimGame':
            pass
        else:
            bot.send_message(message.chat.id, 'Таким вещам меня не учиил')

if __name__ == '__main__':
    #RUN
    bot.polling(none_stop=True)
