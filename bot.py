import telebot
import youtube_dl
import os
import re

bot = telebot.TeleBot("853823128:AAGPr4Voyzv8djrIptCBB9RMysovznjAijI")

YOUTUBE_REGEX = '^((http(s)?:\/\/)?)(www\.)?(m\.)?((youtube\.com\/)|(youtu.be\/))[\S]+'
#  Download data and config
# {}.format(info_dict['title'])
file_path = os.getcwd()
dl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '/songs/%(id)s.%(ext)s',
    'nocheckcetificate': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
@bot.message_handler(commands=['start'])
def welcome(message):

    sti = open(file_path + '\\welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    greeting = "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный для конвертации YouTube видео в mp3 формат.\nДля ознакомления с правилами пользования ботом отправьте мне \"/help\""

    bot.send_message(message.chat.id, greeting.format(
        message.from_user, bot.get_me()), parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):

    sti = open(file_path + '\\help.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    help = "Чтобы конвертировать видео в аудио в mp3 формате, скопируйте ссылку на YouTube видео сюда, <b>ВНИМАНИЕ для корректной работы бота не пишите ничего лишнего кроме ссылки. Обработка видео займет от 30 сек до 1 минуты, просим вас набраться терпения. Спасибо!!!</b>"

    bot.send_message(message.chat.id, help, parse_mode='html')

# Download song
@bot.message_handler(content_types=['text'])
def send_file(message):
    r = re.search(YOUTUBE_REGEX, message.text)
    cid = message.chat.id
    if r is not None:
        bot.reply_to(
            message, 'Работаем над вашим запросом, <b>ПОЖАЛУЙСТА</b>, Подождите обработки', parse_mode='html')
        song_url = message.text

        with youtube_dl.YoutubeDL(dl_opts) as dl:

            dl.download([song_url])

            info_dict = dl.extract_info(song_url, download=False)
            bot.send_audio(cid, audio=open(
                file_path + '\\songs\\' + info_dict['id'] + '.mp3', 'rb'), title=info_dict['title'])
    else:
        bot.send_message(
            cid, 'Извините, это недействительная ссылка на YouTube!')


bot.polling(none_stop=True)
