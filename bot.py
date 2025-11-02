import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔹 Environment se token aur API URL lena (Render me Environment Variable set karna zaruri)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
NUMBER_API_URL = os.getenv("NUMBER_API_URL", "https://number-api.gauravyt566.workers.dev/?number={}")

if not TELEGRAM_TOKEN:
    raise SystemExit("❌ TELEGRAM_TOKEN not set in environment variables.")

# 🔹 Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is online! Use /num <mobile_number>")

# 🔹 Number Command
async def num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚙️ Usage: /num <mobile_number>")
        return

    number = context.args[0]
    await update.message.reply_text(f"🔍 Searching info for: {number}")

    try:
        url = NUMBER_API_URL.format(number)
        response = requests.get(url, timeout=15)
        data = response.json()
    except Exception as e:
        await update.message.reply_text(f"❌ API error: {e}")
        return

    result = None
    if "data" in data:
        if isinstance(data["data"], dict) and "result" in data["data"]:
            result = data["data"]["result"]
        elif isinstance(data["data"], list):
            result = data["data"]
    elif "result" in data:
        result = data["result"]

    if not result:
        await update.message.reply_text("😕 No data found for that number.")
        return

    for record in result:
        text = (
            f"📞 Mobile: {record.get('mobile', 'N/A')}\n"
            f"👤 Name: {record.get('name', 'N/A')}\n"
            f"👨‍👦 Father: {record.get('father_name', record.get('fname', 'N/A'))}\n"
            f"📍 Address: {record.get('address', 'N/A').replace('!', ', ')}\n"
            f"📱 Alt: {record.get('alt_mobile', record.get('alt', 'N/A'))}\n"
            f"🌐 Circle: {record.get('circle', 'N/A')}\n"
            f"🆔 ID: {record.get('id_number', record.get('id', 'N/A'))}"
        )
        await update.message.reply_text(text)

# 🔹 Main Function
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("num", num))
    app.run_polling()

# ✅ Ye line sabse important hai (CORRECTED VERSION)
if __name__ == "__main__":
    main()
