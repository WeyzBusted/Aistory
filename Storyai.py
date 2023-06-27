import logging
import requests
import urllib

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Настройка логгера
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Обработка команды /start
def start(update, context):
    update.message.reply_text("Привет! Я могу помочь тебе сгенерировать картинку с помощью нейросети Pastel Mix. Просто отправь мне текст, и я сгенерирую для тебя картинку.")

# Обработка сообщений с текстом
def text_message(update, context):
    text = update.message.text
    image_url = generate_image(text)

    # Отправляем картинку пользователю
    update.message.reply_photo(photo=image_url)

# Функция для генерации изображения с помощью нейросети Pastel Mix
def generate_image(text):
    api_url = 'https://api.nnsplit.com/pastelmix'

    # Создаем заголовок для запроса
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0'
    }

    # Кодируем текст в URL-подобную форму
    data = {'text': text}
    data = urllib.parse.urlencode(data).encode('ascii')

    # Отправляем POST-запрос на API нейросети
    response = requests.post(api_url, data=data, headers=headers)

    # Если ответ успешный, возвращаем URL изображения
    if response.status_code == 200:
        result = response.json()
        return result['image_url']

    # В противном случае возвращаем None
    else:
        return None

# Функция main, которая запускает бота
def main():
    # Создание экземпляра бота и его токена
    updater = Updater(token='6064933243:AAEgWPjI8DAhffvpKvIXVf8BDBzknzZ0sqI', use_context=True)
    dispatcher = updater.dispatcher

    # Добавление обработчиков команд и сообщений
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    text_handler = MessageHandler(Filters.text, text_message)
    dispatcher.add_handler(text_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
