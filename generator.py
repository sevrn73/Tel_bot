import telebot
import config
from generator_path.model_create import ModelGenerator
import dbworker
bot = telebot.TeleBot(config.TOKEN)

    
@bot.message_handler()

class Model:

    # подумать над этим
    keys = ["WOPR:*", "WWPR:*", "WLPR:*",
            "WGPR:*", "WWIR:*", "WGOR:*", "WBHP:*",
            "WOPT:*", "WWPT:*", "WLPT:*", "WGPT:*",
            "WWIT:*", "FOPT", "FWPT", "FLPT", "FGPT",
            "FWIT"]

    def __init__(self):
        self.model_name = None
        self.result_name = None
        self.start_date = "1 'JAN' 2020"
        self.mounths = None
        self.nx = None
        self.ny = None
        self.nz = None
        self.dx = None
        self.dy = None
        self.dz = None
        self.por = None
        self.permx = None
        self.permy = None
        self.permz = None
        self.oil_den = None
        self.wat_den = None
        self.gas_den = None
        self.density = [self.oil_den, self.wat_den, self.gas_den]
        self.prod_names = [None]
        self.prod_xs = [None]
        self.prod_ys = [None]
        self.prod_z1s = [None]
        self.prod_z2s = [None]
        self.prod_q_oil = [None]
        self.inj_names = [None]
        self.inj_xs = [None]
        self.inj_ys = [None]
        self.inj_z1s = [None]
        self.inj_z2s = [None] # вскроем разные пропластки для реализации вертикально-латерального заводнения
        self.inj_bhp = [None]
        self.skin = [None]

    # Создаем собственную модель
    def create_model(self, message):
        pass
        # bot.send_message(message.chat.id, 'Количество ячеек по х:')
        # self.nx = int(message.text)
        # bot.send_message(message.chat.id, 'Количество ячеек по y:')
        # self.ny = int(message.text)
        # bot.send_message(message.chat.id, 'Количество ячеек по z:')
        # self.nz = int(message.text)
        # bot.send_message(message.chat.id, 'Размер ячейки по x:')
        # self.dx = int(message.text)
        # bot.send_message(message.chat.id, 'Размер ячейки по y:')
        # self.dy = int(message.text)
        # bot.send_message(message.chat.id, 'Размер ячейки по z:')
        # self.dz = int(message.text)
        # bot.send_message(message.chat.id, 'Пористость:')
        # self.por = int(message.text)
        # bot.send_message(message.chat.id, 'Проницаемость по х:')
        # self.permx = int(message.text)
        # bot.send_message(message.chat.id, 'Проницаемость по y:')
        # self.permy = int(message.text)
        # bot.send_message(message.chat.id, 'Проницаемость по z = 0.1*permx')
        # self.permz = 0.1*self.permx
        # bot.send_message(message.chat.id, 'Плотность нефти')
        # self.oil_den = int(message.text)
        # bot.send_message(message.chat.id, 'Плотность воды')
        # self.wat_den = int(message.text)
        # bot.send_message(message.chat.id, 'Плотность газа')
        # self.gas_den = int(message.text)
        # self.density = [self.oil_den, self.wat_den, self.gas_den]

        # markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        # item1 = telebot.types.InlineKeyboardButton('Создадим добывающую скважину', callback_data='prod')
        # item2 = telebot.types.InlineKeyboardButton('Создадим нагнетательную скважину', callback_data='inj')
        # item3 = telebot.types.InlineKeyboardButton('Готово', callback_data='complete')
        # markup.add(item1, item2, item3)
        # bot.send_message(message.chat.id, 'Теперь разберемся со скважинами', reply_markup=markup)


        # new_model = ModelGenerator(init_file_name='generator_path/RIENM1_INIT.DATA',start_date=self.start_date, mounths=self.mounths, nx=self.nx, ny=self.ny, nz=self.nz, dx=self.dx, dy=self.dy, dz=self.dz, por=self.por, permx=self.permx,
        #              permy=self.permy, permz=self.permz, prod_names=self.prod_names, prod_xs=self.prod_xs, prod_ys=self.prod_ys, prod_z1s=self.prod_z1s, prod_z2s=self.prod_z2s, prod_q_oil=self.prod_q_oil,
        #              inj_names=self.inj_names, inj_xs=self.inj_xs, inj_ys=self.inj_ys, inj_z1s=self.inj_z1s, inj_z2s=self.inj_z2s, inj_bhp=self.inj_bhp, skin=self.skin, density=self.density)

        # print(self.prod_names)
        # new_model.create_model(self.model_name, self.result_name, self.keys)


    @bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.Generator.model_name.value)
    def name_method(self, message):
        bot.send_message(message.chat.id, 'Задайте название модели:')
        self.model_name = message.text
        self.result_name = self.model_name + '_RESULT'
        dbworker.set_state(message.chat.id, config.Generator.time)

        
    @bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.Generator.time.value)
    def time_method(self, message):
        bot.send_message(message.chat.id, f'Дата начала расчета {self.start_date}. Количество месяцев:')
        self.mounths = message.text
        print(self.model_name)
        #dbworker.set_state(message.chat.id, config.Ge)
        
    # Создание скважины
    @bot.callback_query_handler(func=lambda call: True)
    def create_prod(self, call):
        try:
            if call.message:
                if call.data == 'prod':
                    bot.send_message(call.message.chat.id, 'Название скважины:')
                    self.prod_names.append(call.message.text)
                    bot.send_message(call.message.chat.id, 'Координата х:')
                    self.prod_xs.append(int(call.message.text))
                    bot.send_message(call.message.chat.id, 'Координата y:')
                    self.prod_ys.append(int(call.message.text))
                    bot.send_message(call.message.chat.id, 'Координата z1:')
                    self.prod_z1s.append(int(call.message.text))
                    bot.send_message(call.message.chat.id, 'Координата z2:')
                    self.prod_z2s.append(int(call.message.text))
                    bot.send_message(call.message.chat.id, 'Целевой дебит (м3/сут):')
                    self.prod_q_oil.append(int(call.message.text))
                    bot.send_message(call.message.chat.id, 'Скин-фактор:')
                    self.skin.append(int(call.message.text))

                elif call.data == 'inj':
                    bot.send_message(call.message.chat.id, 'Название скважины:')
                    self.inj_names.append(call.message.text)
                    bot.send_message(call.message.chat.id, 'Координата х:')
                    self.inj_xs.append(int(call.message.text))
                    bot.send_message(call.message.chat.id, 'Координата y:')
                    self.inj_ys.append(int(call.message.text))
                    bot.send_message(call.message.chat.id, 'Координата z1:')
                    self.inj_z1s.append(int(call.message.text))
                    bot.send_message(call.message.chat.id, 'Координата z2:')
                    self.inj_z2s.append(int(call.message.text))
                    bot.send_message(call.message.chat.id, 'Забойное давление (атм):')
                    self.inj_bhp.append(int(call.message.text))
                    bot.send_message(call.message.chat.id, 'Скин-фактор:')
                    self.skin.append(int(call.message.text))

                elif call.data == 'complete':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message_id, reply_markup=None)
        except Exception as e:
            print(repr(e))


    # Принимаем готовые модели (в разработке)
    @bot.message_handler(content_types=['document'])
    def get_model(message):
        pass

    # Отправляем результаты создания модели
    @bot.message_handler(commands=['result'])
    def result(message):
        pic = open('static/spot.png', 'rb')
        bot.send_document(message.chat.id, pic)
        bot.send_document(message.chat.id, "FILEID")
