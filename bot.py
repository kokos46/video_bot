import telebot
import config
import mysql.connector

token = config.token
bot = telebot.TeleBot(token)
connection = mysql.connector.connect(
    user = config.db_user,
    password=config.db_pass,
    host=config.db_host,
    database=config.db_name
)

cur = connection.cursor()

@bot.message_handler(commands=['start'])
def start_command(message):
    # Получаем параметр из команды /start
    if len(message.text.split()) > 1:
        file_id = message.text.split()[1]
        cur.execute(f'select id from ids where shortid = {file_id[:31:]}')
        bot.send_video(message.chat.id, video=cur.fetchone())
    else:
        bot.send_message(message.chat.id, "Пожалуйста, укажите file_id после команды /start.")

@bot.message_handler(content_types=['video'])
def send_id(message):
    # Получаем file_id из полученного видео
    id_video = message.video.file_id
    cur.execute(f'insert into ids (id, shortid) values ({id_video}, {id_video[:31:]})')
    bot.send_message(message.chat.id, text=f'Ваш file_id: {id_video[:31:]}')

if __name__ == '__main__':
    bot.polling(none_stop=True)