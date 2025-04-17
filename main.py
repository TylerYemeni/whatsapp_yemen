import random
import time
import logging
from twilio.rest import Client
from textblob import TextBlob  # لاستخدام تحليل المشاعر
from faker import Faker
import requests

# تكوين Twilio
account_sid = 'YOUR_TWILIO_ACCOUNT_SID'  # استبدل بـ SID الخاص بك
auth_token = 'YOUR_TWILIO_AUTH_TOKEN'  # استبدل بـ Auth Token الخاص بك
client = Client(account_sid, auth_token)

# إعداد البروكسيات من الملف
proxies = []
with open('proxies.txt', 'r') as f:
    proxies = [line.strip() for line in f]

# إعداد سجل الأخطاء
logging.basicConfig(filename='whatsapp_report_logs.log', level=logging.INFO)

# توليد رقم من Twilio
def generate_twilio_phone_number():
    available_numbers = client.available_phone_numbers('US').local.list()
    random_number = random.choice(available_numbers)
    purchased_number = client.incoming_phone_numbers.create(phone_number=random_number.phone_number)
    return purchased_number.phone_number

# تحليل ردود الفعل
def analyze_response(response):
    blob = TextBlob(response)
    sentiment = blob.sentiment.polarity  # تحليل المشاعر
    if sentiment < -0.5:
        return "Negative"
    elif sentiment > 0.5:
        return "Positive"
    else:
        return "Neutral"

# إرسال بلاغ عبر واتساب
def send_report_twilio(phone_number, message):
    from_number = generate_twilio_phone_number()  # توليد رقم جديد من Twilio
    message = client.messages.create(
        body=message,
        from_=f'whatsapp:{from_number}',
        to=f'whatsapp:{phone_number}'
    )
    logging.info(f"Report sent to {phone_number} from {from_number}")
    print(f"Report sent to {phone_number} from {from_number}")

# تغيير البروكسي بشكل عشوائي
def switch_proxy():
    return random.choice(proxies)

# اختبار وظيفة تحليل الردود
def handle_response(response):
    sentiment = analyze_response(response)
    if sentiment == "Negative":
        print("Received negative feedback. Taking action...")

# اختبار وظيفة إرسال البلاغات
send_report_twilio('+1234567890', 'This is a test report message via WhatsApp.')
handle_response("I am very upset with this service!")
