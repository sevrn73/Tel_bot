import telebot # pip install pyTelegramBotAPI
import config
from pathlib import Path
from game import simgame_run as game


bot = telebot.TeleBot(config.TOKEN)

# Стартовая информация
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, ты написал боту SimGame2020. "
                                      "Я могу создать простую модель для симулятора OPM и поиграть в игру."
                    "Для этого необходимо прислать соответственно заполненные .dat или .xlsx файлы.",
                     parse_mode='html')


# Стартуем события
@bot.message_handler(content_types=['document'])
def start_funk(message):
    try:
        save_dir = os.getcwd()
        file_name = message.document.file_name
        file_id = message.document.file_name
        file_id_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        if not os.path.isdir(f"game/dataspace/{file_name}"):
             os.mkdir(f"game/dataspace/{file_name}")
        scr = save_dir + "/game/dataspace/" + file_name
        with open(scr, 'wb') as new_file:
            new_file.write(downloaded_file)
            os.rename(os.path.join(scr, f'{file_name}.xlsx'), f'Мероприятия РиЭНМ {file_name}.xlsx')
        bot.send_message(message.chat.id, "[*] File added:\nFile name - {}\nFile directory - {}".format(str(file_name), str(save_dir)))

        if Path(scr).suffix == '.DATA':
            pass
        elif Path(scr).suffix == '.xlsx':
            game.start(file_name)

    except Exception as ex:
        bot.send_message(message.chat.id, "[!] error - {}".format(str(ex)))

if __name__ == '__main__':
    #RUN
    bot.polling(none_stop=True)
