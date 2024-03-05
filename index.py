import uuid
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# تنظیمات
bot_token = "7137673728:AAE85wL1RBYskkrlCZaIzhEbgKmiEBiefDI"
api_key = "D37DNS7-VH1MPNS-QGM99PV-SQZQG2A"
api_url = "https://api.nowpayments.io/v1"

# مقدار ثابت
fixed_amount = 25.0
currency_from = "usd"

# تابع برای ساخت کد UUID
def generate_uuid(update: Update, context: CallbackContext) -> None:
    unique_id = uuid.uuid4()
    unique_id_str = unique_id.hex
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"سلام! این کد UUID شماست: {unique_id_str}")

# تابع برای استارت ربات
def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="سلام! ربات شروع به کار کرد. برای دریافت کد UUID از دستور /generate_uuid استفاده کنید.")

# تابع برای ارسال لینک پرداخت
def create_and_send_payment_link(update: Update, context: CallbackContext, amount, currency_from, currency_to):
    estimated_amount = get_estimated_price(amount, currency_from, currency_to)

    if estimated_amount is not None:
        payment_info = create_payment(amount, currency_from, estimated_amount, currency_to, str(uuid.uuid4()), "")
        if payment_info:
            payment_id = payment_info['payment_id']
            payment_link = f"https://sandbox.nowpayments.io/payment/?iid={payment_id}"

            # ارسال لینک پرداخت به کاربر
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"برای پرداخت از لینک زیر استفاده کنید: {payment_link}")
            
            print(f"Payment ID: {payment_id}")
            print(f"Payment Status: {payment_info['payment_status']}")

            # برای پیگیری وضعیت پرداخت
            payment_status = get_payment_status(payment_id)
            print(f"Current Payment Status: {payment_status}")

# تابع برای دریافت مقدار تخمینی
def get_estimated_price(amount, currency_from, currency_to):
    endpoint = "/estimate"
    headers = {"x-api-key": api_key}
    params = {"amount": amount, "currency_from": currency_from, "currency_to": currency_to}

    response = requests.get(api_url + endpoint, headers=headers, params=params)

    if response.status_code == 200:
        estimated_amount = response.json().get("estimated_amount")
        return estimated_amount
    else:
        return None

# تابع برای ایجاد پرداخت
def create_payment(price_amount, price_currency, pay_amount, pay_currency, order_id, order_description):
    endpoint = "/payment"
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    data = {
        "price_amount": price_amount,
        "price_currency": price_currency,
        "pay_amount": pay_amount,
        "pay_currency": pay_currency,
        "order_id": order_id,
        "order_description": order_description
    }

    response = requests.post(api_url + endpoint, json=data, headers=headers)

    if response.status_code == 201:
        payment_info = response.json()
        return payment_info
    else:
        return None

# تابع برای دریافت وضعیت پرداخت
def get_payment_status(payment_id):
    endpoint = f"/payment/{payment_id}"
    headers = {"x-api-key": api_key}

    response = requests.get(api_url + endpoint, headers=headers)

    if response.status_code == 200:
        payment_status = response.json().get("payment_status")
        return payment_status
    else:
        return None

# ساخت ربات و اتصال به تلگرام
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# تعریف دستورها
dispatcher.add_handler(CommandHandler("generate_uuid", generate_uuid))
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("start_payment", lambda update, context: create_and_send_payment_link(update, context, fixed_amount, currency_from, currency_from)))

# شروع گوش کردن به دستورات
updater.start_polling()

# اجرای ربات تا زمانی که متوقف شود
updater.idle()
