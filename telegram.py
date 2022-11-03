from os import getenv

# библиотека для загрузки данных из env
from dotenv import load_dotenv
import telebot


# метода ищет файл env и переменные из него
load_dotenv()

# достает из файла переменную token
token = getenv('token')
orig_id = getenv('original_id')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = message.text.split()
    if len(text) > 1:
        bot.reply_to(message, text[1][::-1])


@bot.message_handler(content_types=['text'])
def echo(message):
    print(message.from_user.id, message.from_user)
    bot.reply_to(message, message.text.upper())
    name = (n for n in (message.from_user.first_name, message.from_user.last_name)
            if n is not None)
    message_text = f'Пользователь: {message.from_user.id} с именем {" ".join(name)}' \
                   f' @{message.from_user.username if message.from_user.username else "Не указан"} ' \
                   f'отправил текст: "{message.text}"'
    bot.send_message(chat_id=orig_id, text=message_text)


bot.infinity_polling()
