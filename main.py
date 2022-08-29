import telebot
from telebot import types
import sql
from sql import add_user, set_user_estate_type, set_user_repair, set_user_zagorod_place, set_user_budget, \
    set_user_city_type, set_user_city_apartment_type, set_user_phone, set_user_catalog
from keyboards import data_start, data_zagorod_choose, data_city_choose, data_city_type, data_city_repair, \
    data_zagorod_place, data_city_budget, data_zagorod_budget, data_catalogs, data_contacts

bot = telebot.TeleBot('5644721445:AAH3pUrP793hfr--oqg2eoMe9K9fD9lJU2M')


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start' or message.text == 'Вернуться назад':
        add_user(message.from_user.id)
        question = "Какую недвижимость вы ищите?"
        bot.send_message(message.from_user.id, text=question, reply_markup=gen_markup(data_start))
    elif message.text == "/catalogs":
        question = "Выберите подборку из списка, чтобы заказать бесплатный PDF-каталог с описанием и фотографиями жилых комплексов."
        bot.send_message(message.from_user.id, text=question, reply_markup=gen_markup(data_catalogs))
    elif message.text == "/expert":
        question = "Перейдите в чат-бота (https://t.me/whitewillestatebot?start=_c2NlbmFyaW89ZXhwZXJ0) для связи с экспертом компании."
        bot.send_message(message.from_user.id, text=question)
    elif message.text == "/call":
        question = "Metrium — международная компания с офисами в Дубае, Москве и Лондоне. Выберите подходящий город"
        bot.send_message(message.from_user.id, text=question, reply_markup=gen_markup_keyboard(data_contacts))
    elif message.text == "Москва" or message.text == "Дубай" or message.text == "Лондон":
        question = "Отвечаем на вопросы ежедневно с 10 до 20 часов по телефону +7 (495) 032-51-11. Встречаем гостей в офисе по адресу: Москва, Пресненская набережная, 6с2, башня «Империя», 3-й подъезд, офис 4315. (https://goo.gl/maps/TgdPceHcQ92NMaa37)"
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_phone = types.KeyboardButton(text="Вернуться назад")
        keyboard.add(button_phone)
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Напишите /start')


def gen_markup(data):
    markup = types.InlineKeyboardMarkup()
    for item in data:
        markup.add(types.InlineKeyboardButton(item.get('text'), callback_data=item.get('callback_data')))
    return markup


def gen_markup_keyboard(data):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    for item in data:
        keyboard.add(types.KeyboardButton(item.get('text')))
    return keyboard


def zagorod_choose(message):
    question = "Какой тип недвижимости вы ищете?"
    bot.send_message(message.from_user.id, text=question, reply_markup=gen_markup(data_zagorod_choose))


def city_choose(message):
    question = "Какой тип недвижимости вы ищете?"
    bot.send_message(message.from_user.id, text=question, reply_markup=gen_markup(data_city_choose))


def city_type(message):
    question = "Какой тип недвижимости вы ищете?"
    bot.send_message(message.from_user.id, text=question, reply_markup=gen_markup(data_city_type))


def city_repair(message):
    question = "Выберите желаемое состояние жилья"
    bot.send_message(message.from_user.id, text=question, reply_markup=gen_markup(data_city_repair))


def zagorod_place(message):
    question = "Какую местность вы предпочитаете?"
    bot.send_message(message.from_user.id, text=question, reply_markup=gen_markup(data_zagorod_place))


def city_budget(message):
    question = "Примерный бюджет?"
    bot.send_message(message.from_user.id, text=question, reply_markup=gen_markup(data_city_budget))


def zagorod_budget(message):
    question = "Примерный бюджет?"
    bot.send_message(message.from_user.id, text=question, reply_markup=gen_markup(data_zagorod_budget))


def get_phone(message):
    text = "Спасибо. Чтобы получить подборку, нажмите на кнопку «номер телефона» или отправьте сообщение с ним. В течение нескольких минут с вами свяжется брокер и пришлет подходящие варианты.";
    bot.send_message(message.from_user.id, text)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.from_user.id, 'Номер телефона', reply_markup=keyboard)
    bot.register_next_step_handler(message.message, result)


def get_catalog(message):
    text = "Чтобы скачать каталог, поделитесь телефоном по кнопке или отправьте номер текстовым сообщением. В течение 20 минут вам напишет эксперт по недвижимости, чтобы отправить цены и планировки проектов.";
    bot.send_message(message.from_user.id, text)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.from_user.id, 'Номер телефона', reply_markup=keyboard)
    bot.register_next_step_handler(message.message, result)


def result(message):
    if message.contact is not None:
        set_user_phone(message.from_user.id, message.contact.phone_number)
    else:
        set_user_phone(message.from_user.id, message.text)
    text = "Спасибо, мы свяжемся с вами в ближайшее время"
    bot.send_message(message.from_user.id, text)


def get_text(data, find):
    for item in data:
        if item.get('callback_data') == find:
            text = item.get('text')
    return text


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "city":
        set_user_estate_type(call.from_user.id, get_text(data_start, call.data), 1)
        city_choose(call)
    elif call.data == "zagorod":
        set_user_estate_type(call.from_user.id, get_text(data_start, call.data), 2)
        zagorod_choose(call)
    elif call.data == "house_key" or call.data == "house_repair" or call.data == "house_field":
        set_user_repair(call.from_user.id, get_text(data_zagorod_choose, call.data))
        zagorod_place(call)
    elif call.data == "quit_place" or call.data == "wood_place" or call.data == "water_place" or call.data == "other_place":
        set_user_zagorod_place(call.from_user.id, get_text(data_zagorod_place, call.data))
        zagorod_budget(call)
    elif call.data == "from_fifth" or call.data == "from_seventh" or call.data == "from_hundred" or call.data == "from_hundred_fifth" or call.data == "more_two_hundred":
        set_user_budget(call.from_user.id, get_text(data_zagorod_budget, call.data))
        get_phone(call)
    elif call.data == "flat" or call.data == "apartments" or call.data == "penthouse" or call.data == "tanhouse" or call.data == "detached_house" or call.data == "flat_apartments":
        set_user_city_apartment_type(call.from_user.id, get_text(data_city_choose, call.data))
        city_type(call)
    elif call.data == "new" or call.data == "old":
        set_user_city_type(call.from_user.id, get_text(data_city_type, call.data))
        city_repair(call)
    elif call.data == "finished" or call.data == "not_finished" or call.data == "dont_care":
        set_user_repair(call.from_user.id, get_text(data_city_repair, call.data))
        city_budget(call)
    elif call.data == "city_before_hundred" or call.data == "city_from_hundred" or call.data == "city_from_two_hundred" or call.data == "city_from_fifth_hundred":
        set_user_budget(call.from_user.id, get_text(data_city_budget, call.data))
        get_phone(call)
    elif call.data == "catalog_invest" or call.data == "catalog_life" or call.data == "catalog_facilities" or call.data == "catalog_circle" or call.data == "catalog_start":
        set_user_catalog(call.from_user.id, get_text(data_catalogs, call.data))
        get_phone(call)


bot.infinity_polling()
