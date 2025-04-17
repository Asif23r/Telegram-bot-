import telebot
import json
import os

# Replace with your bot token and Telegram ID
BOT_TOKEN = 'YOUR_BOT_TOKEN'
OWNER_ID = 123456789  # Replace with your Telegram numeric ID

bot = telebot.TeleBot(BOT_TOKEN)
DATA_FILE = 'finance.json'

# Create file if not exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"income": [], "expense": []}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Welcome Message
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id != OWNER_ID:
        return
    bot.reply_to(message, 
        "👋 *Welcome to Expense Tracker Bot!*\n\n"
        "Use /help to see all available commands.",
        parse_mode="Markdown")

# Help Command
@bot.message_handler(commands=['help'])
def help_command(message):
    if message.from_user.id != OWNER_ID:
        return
    help_text = (
        "🛠 *Bot Commands:*\n\n"
        "➕ `/addincome amount source`\n"
        "💰 Add new income entry\n\n"
        "➖ `/addexpense amount reason`\n"
        "💸 Add new expense entry\n\n"
        "📊 `/report`\n"
        "📈 Show total income, expenses & balance\n\n"
        "🔊 `/broadcast message`\n"
        "📢 Send a broadcast message to all users (owner-only)\n\n"
        "👋 `/start`\n"
        "🤖 Start the bot\n"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

# Add Income
@bot.message_handler(commands=['addincome'])
def add_income(message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        parts = message.text.split()
        amt = int(parts[1])
        source = " ".join(parts[2:])
        data = load_data()
        data["income"].append({"amount": amt, "source": source})
        save_data(data)
        bot.reply_to(message, f"✅ *Income Added!*\n💰 Amount: ₹{amt}\n📌 Source: {source}", parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ Format error!\nUse: `/addincome 500 Freelancing`", parse_mode="Markdown")

# Add Expense
@bot.message_handler(commands=['addexpense'])
def add_expense(message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        parts = message.text.split()
        amt = int(parts[1])
        reason = " ".join(parts[2:])
        data = load_data()
        data["expense"].append({"amount": amt, "reason": reason})
        save_data(data)
        bot.reply_to(message, f"📝 *Expense Added!*\n💸 Amount: ₹{amt}\n📌 Reason: {reason}", parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ Format error!\nUse: `/addexpense 200 Snacks`", parse_mode="Markdown")

# Financial Report
@bot.message_handler(commands=['report'])
def report(message):
    if message.from_user.id != OWNER_ID:
        return
    data = load_data()
    total_income = sum(i["amount"] for i in data["income"])
    total_expense = sum(e["amount"] for e in data["expense"])
    balance = total_income - total_expense

    status = "📈 *Profit!*" if balance >= 0 else "📉 *Loss!*"
    msg = (
        f"📊 *Financial Report*\n"
        f"💰 Total Income: ₹{total_income}\n"
        f"💸 Total Expenses: ₹{total_expense}\n"
        f"🧾 Balance: ₹{balance}\n\n"
        f"{status}"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

# Broadcast Command (only for owner)
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        msg = " ".join(message.text.split()[1:])
        if not msg:
            bot.reply_to(message, "⚠️ *Please provide a message to broadcast!*")
            return
        # Broadcasting message to all users (simplified approach)
        # You need to manually add users to a list or database
        users = [OWNER_ID]  # Add your users' IDs here
        for user_id in users:
            bot.send_message(user_id, f"📢 *Broadcast Message from Owner:*\n\n{msg}", parse_mode="Markdown")
        bot.reply_to(message, f"✅ *Broadcast Message Sent!*")
    except Exception as e:
        bot.reply_to(message, f"⚠️ *Error:* {str(e)}")

print("🚀 Bot is running...")
bot.infinity_polling()