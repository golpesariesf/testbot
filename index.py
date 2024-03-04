import uuid
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# تنظیمات
bot_token = "7137673728:AAE85wL1RBYskkrlCZaIzhEbgKmiEBiefDI"
user_id = 5986365049

# تابع برای ساخت کد UUID
def generate_uuid(update: Update, context: CallbackContext) -> None:
    unique_id = uuid.uuid4()
    unique_id_str = unique_id.hex
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"UUID HEX: {unique_id_str}")

# تابع برای ارسال کد به یک کاربر خاص
def send_to_user(update: Update, context: CallbackContext) -> None:
    unique_id = uuid.uuid4()
    unique_id_str = unique_id.hex
    context.bot.send_message(chat_id=user_id, text=f"New UUID HEX: {unique_id_str}")

# ساخت ربات و اتصال به تلگرام
updater = Updater(bot=Bot(token=bot_token), use_context=True)
dispatcher = updater.dispatcher

# تعریف دستورها
dispatcher.add_handler(CommandHandler("generate_uuid", generate_uuid))
dispatcher.add_handler(CommandHandler("send_to_user", send_to_user))

# شروع گوش کردن به دستورات
updater.start_polling()

# اجرای ربات تا زمانی که متوقف شود
updater.idle()
