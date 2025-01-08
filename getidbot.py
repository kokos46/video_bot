import telebot
import config

token = config.token
bot = telebot.TeleBot(token)

links = {

}

@bot.message_handler(commands=['start'])
def start_command(message):
    # Получаем параметр из команды /start
    if len(message.text.split()) > 1:
        file_id = message.text.split()[1]
        bot.send_video(message.chat.id, video=links[file_id])
    else:
        bot.send_message(message.chat.id, "Пожалуйста, укажите file_id после команды /start.")

@bot.message_handler(content_types=['video'])
def send_id(message):
    # Получаем file_id из полученного видео
    id_video = message.video.file_id
    links[f'{id_video[:31:]}'] = id_video
    bot.send_message(message.chat.id, text=f'Ваш file_id: {id_video[:31:]}')

if __name__ == '__main__':
    bot.polling(none_stop=True)