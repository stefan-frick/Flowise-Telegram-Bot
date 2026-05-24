import os
import requests
import telebot

TOKEN = os.getenv('TELEGRAM_TOKEN')
FLOWISE_URL = os.getenv('FLOWISE_URL')
FLOWISE_API_KEY = os.getenv('FLOWISE_API_KEY')
MY_TELEGRAM_ID = int(os.getenv('TELEGRAM_USER_ID'))

bot = telebot.TeleBot(TOKEN)
headers = {"Authorization": f"Bearer {FLOWISE_API_KEY}"}

# ==========================================
# /CLEAR COMMAND
# ==========================================
@bot.message_handler(commands=['clear'])
def clear_memory(message):
    if message.from_user.id != MY_TELEGRAM_ID:
        return

    print(f"\n--- Wiping Memory ---")
    memory_url = FLOWISE_URL.replace('/prediction/', '/chatmessage/')
    try:
        response = requests.delete(memory_url, params={"sessionId": str(message.chat.id)}, headers=headers)
        if response.status_code == 200:
            bot.reply_to(message, "🧹 Memory cleared!")
        else:
            bot.reply_to(message, f"⚠️ Error clearing memory. Status code: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, f"Connection Error: {str(e)}")

# ==========================================
# NORMAL TEXT HANDLER
# ==========================================
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.from_user.id != MY_TELEGRAM_ID:
        return

    bot.send_chat_action(message.chat.id, 'typing')
    print(f"\n--- New Text Message ---\nYou asked: {message.text}")

    payload = {
        "question": message.text,
        "overrideConfig": {"sessionId": str(message.chat.id)}
    }

    try:
        response = requests.post(FLOWISE_URL, json=payload, headers=headers)
        answer = response.json().get('text', "Sorry, I couldn't get an answer.")
        print(f"Agent answered: {answer}\n-------------------")
        bot.reply_to(message, answer)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        bot.reply_to(message, f"Connection Error: {str(e)}")

print("Telegram Bot is running and waiting for messages...")
bot.infinity_polling()