import telebot
from flask import Flask, request
import os

API_TOKEN = '8056443890:AAF96YkdQLiYXy0-hwSRVE2jUlNaLqXU5oM'
GROUP_ID = 213188977  # إذا لم تصلك الرسائل للمجموعة، استخدم ID يبدأ بـ -100

bot = telebot.TeleBot(API_TOKEN)
app = Flask(_name_)

user_map = {}

@bot.message_handler(func=lambda message: True, content_types=['text'])
def forward_to_group(message):
    user_id = message.chat.id
    user_name = message.from_user.first_name or "زبون"
    msg = f"💬 رسالة جديدة من {user_name}:\n\n{message.text}"
    user_map[message.message_id] = user_id

    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton(text="✉ الرد", callback_data=f"reply_{user_id}")
    markup.add(btn)

    bot.send_message(GROUP_ID, msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def reply_handler(call):
    user_id = int(call.data.split("_")[1])
    msg = bot.send_message(call.message.chat.id, "📝 اكتب ردك:")
    bot.register_next_step_handler(msg, forward_reply, user_id)

def forward_reply(message, user_id):
    bot.send_message(user_id, f"📩 رد من فريق الدعم:\n\n{message.text}")
    bot.send_message(message.chat.id, "✅ تم إرسال الرد للزبون.")

@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok"

@app.route('/')
def index():
    return "البوت يعمل ✅"

if _name_ == "_main_":
    bot.remove_webhook()
    webhook_url = 'https://roobystorebot.repl.co/' + API_TOKEN  # This should point to your Replit URL
    bot.set_webhook(url=webhook_url)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
