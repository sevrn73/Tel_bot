import telebot # pip install pyTelegramBotAPI
import config
from pathlib import Path
from game import simgame_run as game
import os
import subprocess
from generator_path import model_create as generator


bot = telebot.TeleBot(config.TOKEN)

# Стартовая информация
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, ты написал боту SimGame2020. "
                                      "Я могу создать простую модель для симулятора OPM и поиграть в игру. "
                    "Для этого необходимо прислать соответственно заполненные .dat или .xlsx файлы. Названия файлов без пробелов и прописными буквами!",
                     parse_mode='html')


# Стартуем события
@bot.message_handler(content_types=['document'])
def start_funk(message):
    try:
        save_dir = os.getcwd()
        file_name = message.document.file_name
        file_id = message.document.file_id
        file_id_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        if not os.path.isdir(f"cache"):
            os.mkdir(f"cache")
        scr = save_dir + f'/cache/{file_name}'
               
        # Opm simple model start
        if Path(scr).suffix == '.DATA':
            with open(scr, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(message.chat.id, "[*] File added:\nFile name - {}\nFile directory - {}".format(str(file_name), str(save_dir)))
            bot.send_message(message.chat.id, "Ожидайте результатов расчетов")

            subprocess.call(["cp", "-r" , f'cache/{file_name}', f'generator_path/{file_name}'])

            model = generator.ModelGenerator()
            result_name = file_name + '_RESULT'
            keys = ["WOPR:*", "WWPR:*", "WLPR:*",
                    "WGPR:*", "WWIR:*", "WGOR:*", "WBHP:*",
                    "WOPT:*", "WWPT:*", "WLPT:*", "WGPT:*",
                    "WWIT:*", "FOPT", "FWPT", "FLPT", "FGPT",
                    "FWIT"]
            model.calculate_prepared_model(file_name, result_name, keys)

            # Send results
            for filename in os.listdir(save_dir + f'/generator_path/snapshots/{file_name}'):
                with open(os.path.join(save_dir + f'/generator_path/snapshots/{file_name}', filename), 'rb') as f:
                    bot.send_document(message.chat.id, f)
            csv = open(f'generator_path/{result_name}.csv', 'rb')
            bot.send_document(message.chat.id, csv)

        
        # Simgame start
        elif Path(scr).suffix == '.xlsx':
            with open(scr, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(message.chat.id, "[*] File added:\nFile name - {}\nFile directory - {}".format(str(file_name), str(save_dir)))
            bot.send_message(message.chat.id, "Ожидайте результатов расчетов")
        
            if not os.path.isdir(f"game/dataspace/{file_name}"):
                os.mkdir(f"game/dataspace/{file_name}")
            subprocess.call(["cp", "-r" , f'cache/{file_name}', f'game/dataspace/{file_name}/Мероприятия РиЭНМ {file_name}'])
            
            game.start(file_name)
            
            # Send results
            for filename in os.listdir(save_dir + f'/game/workspace/snapshots/{file_name}'):
                with open(os.path.join(save_dir + f'/game/workspace/snapshots/{file_name}', filename), 'rb') as f:
                    bot.send_document(message.chat.id, f)
            tr = open(f'game/resultspace/{file_name}/201910_TR_1.xlsx', 'rb')
            bot.send_document(message.chat.id, tr)
            
        else:
            bot.send_message(message.chat.id, "Я не поддерживаю такой формат файлов ")
            

    except Exception as ex:
        bot.send_message(message.chat.id, "[!] error - {}".format(str(ex)))

if __name__ == '__main__':
    #RUN
    bot.polling(none_stop=True)
