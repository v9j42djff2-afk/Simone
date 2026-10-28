import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token caché dans Render > Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8175306783"))

# === TON MESSAGE /START ICI ===
START_MESSAGE = """Bienvenue chez Simone
Service client disponible 👇

🕐 Horaires : 11h - 23h
💬 Support : @simone750
📢 Actualités : @simonecanal"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_MESSAGE)

async def handle_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"📩 MESSAGE CLIENT\n👤 {user.first_name} @{user.username}\nID: {user.id}\n\n{update.message.text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=text)
    await update.message.reply_text("✅ Message reçu, on te répond vite.")

async def handle_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return
    try:
        client_id = int(update.message.reply_to_message.text.split("ID: ")[1].split("\n")[0])
        await context.bot.send_message(chat_id=client_id, text=update.message.text)
        await update.message.reply_text("✅ Envoyé au client")
    except:
        await update.message.reply_text("Fais 'Répondre' sur le message du client pour répondre")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.User(user_id=ADMIN_ID) & filters.ChatType.PRIVATE, handle_client))
app.add_handler(MessageHandler(filters.TEXT & filters.User(user_id=ADMIN_ID), handle_admin))

print("Bot Simone lancé avec /start")
app.run_polling()
