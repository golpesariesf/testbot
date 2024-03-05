import uuid
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# تنظیمات
bot_token = "YOUR_BOT_TOKEN"

# تابع برای ساخت کد UUID
def generate_uuid(update: Update, context: CallbackContext) -> None:
    unique_id = uuid.uuid4()
    unique_id_str = unique_id.hex
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"سلام! این کد UUID شماست: {unique_id_str}")

# تابع برای استارت ربات
def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="سلام! ربات شروع به کار کرد. برای دریافت کد UUID از دستور /generate_uuid استفاده کنید.")

# ساخت ربات و اتصال به تلگرام
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# تعریف دستورها
dispatcher.add_handler(CommandHandler("generate_uuid", generate_uuid))
dispatcher.add_handler(CommandHandler("start", start))

# شروع گوش کردن به دستورات
updater.start_polling()

# اجرای ربات تا زمانی که متوقف شود
updater.idle()
