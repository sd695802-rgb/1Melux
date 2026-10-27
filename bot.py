import os
import telebot
from openai import OpenAI

# قراءة المفاتيح من إعدادات الاستضافة (أو ضعها هنا مباشرة إذا كنت تختبره محلياً)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")

# تهيئة عميل OpenAI وبوت تلجرام
client = OpenAI(api_key=OPENAI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أنا بوت ذكاء اصطناعي مدعوم بنماذج OpenAI (GPT). كيف يمكنني مساعدتك اليوم؟ 🚀")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي ومفيد تتحدث باللغة العربية."},
                {"role": "user", "content": user_text}
            ]
        )
        reply_text = response.choices[0].message.content
        bot.reply_to(message, reply_text)
    except Exception as e:
        bot.reply_to(message, "عذراً، حدث خطأ أثناء الاتصال بخوادم OpenAI. حاول مرة أخرى.")

print("البوت يعمل الآن بنجاح باستخدام OpenAI...")
bot.infinity_polling()
