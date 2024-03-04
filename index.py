import uuid
import telebot

bot = telebot.TeleBot(token="7137673728:AAE85wL1RBYskkrlCZaIzhEbgKmiEBiefDI")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "برای دریافت کد UUID، /generate را ارسال کنید.")

@bot.message_handler(commands=['generate'])
def generate(message):
    unique_id = uuid.uuid4()
    unique_id_str = unique_id.hex
    
    bot.send_message(message.chat.id, f"UUID: {unique_id}")
    bot.send_message(message.chat.id, f"UUID HEX: {unique_id_str}")

bot.polling()
