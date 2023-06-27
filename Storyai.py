import telegram
from telegram.ext import Updater, CommandHandler
import tensorflow as tf
import numpy as np
import requests
from PIL import Image
import io

# вставьте свой API-ключ
telegram_bot_token = '6064933243:AAEgWPjI8DAhffvpKvIXVf8BDBzknzZ0sqI'
bot = telegram.Bot(token=telegram_bot_token)

# загрузка нейросети pastel mix
model_url = 'https://github.com/reiinakano/pastel/releases/download/v0.1.0/model_f16_1024.pb'
model_file = requests.get(model_url).content
sess = tf.compat.v1.Session()
graph = tf.compat.v1.get_default_graph()
graph_def = tf.compat.v1.GraphDef()
graph_def.ParseFromString(model_file)
sess.graph.as_default()
tf.import_graph_def(graph_def)

# функция для генерации изображения
def generate_image():
    global graph
    global sess

    # загрузка изображения в формате numpy array
    img = Image.open('input.jpg')
    img_array = np.array(img)/255.

    # ресайз изображения
    img_resized = tf.image.resize_images(tf.convert_to_tensor(img_array), (256, 256))

    # подготовка данных для нейросети
    inputs = np.expand_dims(img_resized.eval(session=sess), axis=0)

    # запуск нейросети
    with sess.as_default():
        with graph.as_default():
            output_image = sess.run('generator/Tanh:0', {'input_image:0': inputs})

    # сохранение сгенерированного изображения
    output_image = output_image[0, :, :, :]
    output_image = ((output_image + 1) / 2) * 255
    output_image = output_image.astype(np.uint8)
    Image.fromarray(output_image).save('output.jpg')

# обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я могу сгенерировать картинку с помощью нейросети pastel mix. Напиши мне /generate, чтобы начать.")

# добавление обработчика команды /start
updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# обработчик команды /generate
def generate(update, context):
    # получение фото из последнего сообщения
    message = update.message
    file_id = message.photo[-1].file_id
    newFile = bot.get_file(file_id)
    newFile.download('input.jpg')

    # генерация нового изображения
    generate_image()

    # отправка сгенерированного изображения пользователю
    with open('output.jpg', 'rb') as f:
        context.bot.send_photo(chat_id=message.chat_id, photo=f)

# добавление обработчика команды /generate
generate_handler = CommandHandler('generate', generate)
dispatcher.add_handler(generate_handler)

# запуск бота
updater.start_polling()
updater.idle()
