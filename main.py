import telebot
from yt_dlp import YoutubeDL
import os

# Yangi bot tokeningiz
TOKEN = '8627827818:AAEVN8WucFss70yCTVTu3pmgBSygHlxMsCY'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Video linkini yuboring. 📥")

@bot.message_handler(func=lambda message: True)
def download_and_send(message):
    url = message.text
    if "http" in url:
        status_msg = bot.reply_to(message, "⏳ Tayyorlanmoqda...")
        try:
            file_name = 'video_file.mp4'
            ydl_opts = {
                'format': 'best',
                'outtmpl': file_name,
                'noplaylist': True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open(file_name, 'rb') as video:
                bot.send_video(message.chat.id, video)
            
            bot.delete_message(message.chat.id, status_msg.message_id)
            os.remove(file_name)
        except Exception as e:
            bot.reply_to(message, f"Xatolik yuz berdi: {e}")
            if os.path.exists(file_name):
                os.remove(file_name)
    else:
        bot.reply_to(message, "Iltimos, link yuboring. 🔗")

print("Bot ishga tushdi... ✅")
bot.polling()
