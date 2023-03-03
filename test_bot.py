import telegram
import requests

from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# Здесь нужно вставить ваш API-ключ Telegram Bot API
bot = telegram.Bot(token='6264193974:AAE2WYTVDf9GT6BYTgH3JgOqhPqXHKDyUzE')

# Здесь нужно вставить ваш API-ключ OpenWeatherMap
weather_api_key = '557c36fe7d6d540b386ed61783c856a1'

# Получение данных о погоде
def get_weather_data(city_name):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(city_name, weather_api_key)
    response = requests.get(url)

    if response.status_code == 200:
        weather_info = response.json()
        temperature = weather_info['main']['temp']
        weather_description = weather_info['weather'][0]['description']
        return 'Температура в городе {} сейчас составляет {}°C. {}'.format(city_name, temperature, weather_description)
    else:
        return None

# Обработчик команды /start
def start(update, context):
    update.message.reply_text('Привет! Я бот для получения прогноза погоды. Просто отправь мне название города.')

# Обработчик текстовых сообщений
def text(update, context):
    city_name = update.message.text
    weather_data = get_weather_data(city_name)

    if weather_data:
        update.message.reply_text(weather_data)
    else:
        update.message.reply_text('Не удалось получить данные о погоде для города {}'.format(city_name))

# Создание объекта Updater и добавление обработчиков
updater = Updater(token='6264193974:AAE2WYTVDf9GT6BYTgH3JgOqhPqXHKDyUzE', use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Вызов функции start для обработки команды /start
start()

text_handler = MessageHandler(Filters.text & ~Filters.command, text)
dispatcher.add_handler(text_handler)

# Запуск бота
updater.start_polling()
