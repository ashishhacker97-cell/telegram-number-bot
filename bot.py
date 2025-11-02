import os
import time
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ready hai!\nUse: /num <mobile_number>")

async def num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Use: /num <mobile_number>")
        return
    number = context.args[0]
    api_url = f"https://number-api.gauravyt566.workers.dev/?number={number}"
    await update.message.reply_text(f"🔍 Searching for: {number}...")

    try:
        r = requests.get(api_url, timeout=10)
        data = r.json()
        results = data.get("result") or data.get("data") or []
        if not results:
            await update.message.reply_text("😕 Koi data nahi mila.")
            return
        msg = ""
        for d in results:
            msg += (
                f"👤 Name: {d.get('name')}\n"
                f"👨‍👦 Father: {d.get('father_name', 'N/A')}\n"
                f"📱 Mobile: {d.get('mobile')}\n"
                f"📞 Alt: {d.get('alt_mobile', 'N/A')}\n"
                f"📍 Address: {d.get('address', '').replace('!', ', ')}\n"
                f"🌐 Circle: {d.get('circle', 'N/A')}\n"
                f"🆔 ID: {d.get('id_number', 'N/A')}\n\n"
                "------------------------\n"
            )
        await update.message.reply_text(msg[:3900])
    except Exception as e:
        await update.message.reply_text(f"⚠️ API Error: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("num", num))
    app.run_polling()

if name == "main":
    main()
